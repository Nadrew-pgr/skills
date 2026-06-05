#!/usr/bin/env node
'use strict';

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { execSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);

const BASE_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CONFIG_DIR = path.join(os.homedir(), '.openclaw', 'pronote-connector');
const CONFIG_FILE = path.join(CONFIG_DIR, 'profiles.json');
const MASTER_KEY_FILE = path.join(CONFIG_DIR, 'master.key');
const LOG_FILE = path.join(CONFIG_DIR, 'connector.log');
const FALLBACK_VAULT_DIRS = [
  path.join(os.homedir(), '.openclaw', 'workspace', 'main', 'obsidian-vault', '02 Projects', 'DSCG', '00 Pilotage', 'Cours Pronote'),
  '/root/.openclaw/workspace/main/obsidian-vault/02 Projects/DSCG/00 Pilotage/Cours Pronote',
  '/home/node/.openclaw/workspace/main/obsidian-vault/02 Projects/DSCG/00 Pilotage/Cours Pronote'
];

const DEFAULT_VAULT_DIR = FALLBACK_VAULT_DIRS.find(p => fs.existsSync(p)) || FALLBACK_VAULT_DIRS[0];
const PRONOTE_VERSION = '2.1.6';
const DEFAULT_MODE = 'timetable';
const DEFAULT_SYNC_WEEKS = 4;
const CLIENT_UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0';

function normalizePronoteUrl(rawUrl) {
  if (!rawUrl || typeof rawUrl !== 'string') {
    return rawUrl;
  }

  const input = rawUrl.trim();
  if (!input) {
    return input;
  }

  let parsed;
  try {
    parsed = new URL(input);
  } catch (err) {
    fail(`URL Pronote invalide: ${input}`);
  }

  let pathname = (parsed.pathname || '/').trim();
  if (!pathname) {
    pathname = '/';
  }

  // pronote-lib ajoute lui-même "/eleve.html?login=true".
  // Si l'utilisateur a fourni une URL déjà pointant sur eleve.html, on évite la duplication.
  pathname = pathname.replace(/\/?eleve\.html$/i, '').replace(/\/?eleve\.htm$/i, '');
  if (!pathname.endsWith('/')) {
    pathname += '/';
  }

  parsed.pathname = pathname;
  parsed.search = '';
  parsed.hash = '';

  return `${parsed.origin}${pathname}`;
}

async function assertPronoteReachable(url) {
  const probeUrl = `${url}eleve.html?login=true`;
  const response = await fetch(probeUrl, {
    headers: {
      'User-Agent': CLIENT_UA,
      Accept: 'text/html,application/xhtml+xml'
    },
    redirect: 'manual'
  });

  const body = await response.text();
  const hasIpBlock = /provisoirement\s+suspendue/i.test(body);
  if (hasIpBlock) {
    fail('Pronote bloque l\'accès depuis cette IP (message détecté: \"Votre adresse IP est provisoirement suspendue!\").');
  }

  if (!response.ok && response.status !== 302 && response.status !== 301 && response.status !== 307) {
    fail(`Connexion Pronote bloquée avant login: HTTP ${response.status}`);
  }

  if (!body.includes('Start(') && !body.includes('pronote') && response.status === 200) {
    log(`probe-unexpected-body: ${url} (${response.status})`);
  }
}

function hasFlag(args, key) {
  return args[key] === true || args[key] === 'true';
}

function log(...items) {
  const line = `${new Date().toISOString()} | ${items.join(' ')}`;
  fs.appendFileSync(LOG_FILE, `${line}\n`, { encoding: 'utf8' });
}

function fail(message, code = 1) {
  console.error(`\n❌ ${message}`);
  process.exit(code);
}

function parseArgs(argv) {
  const result = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];

    if (!token.startsWith('--')) {
      result._.push(token);
      continue;
    }

    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      result[key] = true;
      continue;
    }

    result[key] = next;
    i += 1;
  }

  return result;
}

function toLowerSafe(value) {
  return `${value || ''}`.toLowerCase();
}

function readJson(file, fallback) {
  if (!fs.existsSync(file)) {
    return fallback;
  }

  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (err) {
    fail(`Impossible de lire ${file} : ${err.message}`);
  }
}

function writeJson(file, value) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`, { encoding: 'utf8', mode: 0o600 });
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function ensureMasterKey() {
  ensureDir(CONFIG_DIR);
  if (fs.existsSync(MASTER_KEY_FILE)) {
    return fs.readFileSync(MASTER_KEY_FILE, 'utf8');
  }

  const generated = crypto.randomBytes(32).toString('hex');
  fs.writeFileSync(MASTER_KEY_FILE, generated, { encoding: 'utf8', mode: 0o600 });
  return generated;
}

function encryptSecret(secret) {
  const key = Buffer.from(ensureMasterKey(), 'hex');
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(`${secret}`, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();

  return {
    v: 1,
    iv: iv.toString('base64'),
    tag: tag.toString('base64'),
    ciphertext: encrypted.toString('base64')
  };
}

function decryptSecret(payload) {
  const key = Buffer.from(ensureMasterKey(), 'hex');
  const iv = Buffer.from(payload.iv, 'base64');
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(Buffer.from(payload.tag, 'base64'));

  const decrypted = Buffer.concat([
    decipher.update(Buffer.from(payload.ciphertext, 'base64')),
    decipher.final()
  ]);

  return decrypted.toString('utf8');
}

function toLocalIso(input) {
  const d = new Date(input);
  if (Number.isNaN(d.getTime())) {
    return null;
  }

  const y = d.getFullYear();
  const m = `${d.getMonth() + 1}`.padStart(2, '0');
  const dd = `${d.getDate()}`.padStart(2, '0');
  const hh = `${d.getHours()}`.padStart(2, '0');
  const mm = `${d.getMinutes()}`.padStart(2, '0');
  const ss = `${d.getSeconds()}`.padStart(2, '0');

  const offsetMin = -d.getTimezoneOffset();
  const sign = offsetMin >= 0 ? '+' : '-';
  const abs = Math.abs(offsetMin);
  const oz = `${Math.floor(abs / 60)}`.padStart(2, '0');
  const om = `${abs % 60}`.padStart(2, '0');

  return `${y}-${m}-${dd}T${hh}:${mm}:${ss}${sign}${oz}:${om}`;
}

function toMinutes(fromTs, toTs) {
  if (!fromTs || !toTs) {
    return 0;
  }

  return Math.max(0, Math.round((new Date(toTs).getTime() - new Date(fromTs).getTime()) / 60000));
}

function slug(text) {
  return `${text || 'cours'}`
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-zA-Z0-9\s._-]/g, '')
    .trim()
    .replace(/\s+/g, ' ')
    .slice(0, 70)
    .trim()
    .replace(/\s/g, '-');
}

function digest(content) {
  return crypto.createHash('md5').update(content).digest('hex').slice(0, 8);
}

function detectUE(value) {
  const normalized = toLowerSafe(value).normalize('NFKD').replace(/[\u0300-\u036f]/g, '');

  const rules = [
    { keys: ['ue2', 'finance', 'diagnostic'], label: 'UE2 Finance' },
    { keys: ['ue3', 'management', 'controle', 'contrôle', 'control', 'gestion'], label: 'UE3 Management et contrôle de gestion' },
    { keys: ['ue4', 'comptabil', 'audit'], label: 'UE4 Comptabilité et audit' },
    { keys: ['ue5', 'si', 'systeme', 'informatique', 'msi'], label: 'UE5 MSI' },
    { keys: ['ue6', 'anglais'], label: 'UE6 Anglais' },
    { keys: ['ue7', 'memoire'], label: 'UE7 Mémoire' }
  ];

  const hit = rules.find(rule => rule.keys.some(key => normalized.includes(key)));
  return hit ? hit.label : 'DSCG';
}

function getConfig() {
  return readJson(CONFIG_FILE, { version: 1, profiles: {} });
}

function writeConfig(config) {
  writeJson(CONFIG_FILE, config);
}

function setProfile(options) {
  const config = getConfig();
  const name = options.profile || 'default';

  if (!options.username || !options.password || !options['pronote-url']) {
    fail('setup requiert --username, --password et --pronote-url.');
  }

  const payload = {
    username: options.username,
    url: normalizePronoteUrl(options['pronote-url']),
    cas: options.cas || 'none',
    label: options.label || null,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    outputDir: options['output-dir'] || DEFAULT_VAULT_DIR,
    password: encryptSecret(options.password)
  };

  config.profiles[name] = { ...config.profiles[name], ...payload };
  writeConfig(config);

  return payload;
}

function getProfile(name = 'default') {
  const config = getConfig();
  const profile = config.profiles[name];

  if (!profile) {
    fail(`Profile ${name} introuvable. Lance d'abord: node ... setup --profile ${name} ...`);
  }

  if (!profile.password || !profile.password.ciphertext) {
    fail(`Le profile ${name} ne contient pas d'identifiants chiffrés.`);
  }

  return { ...profile, password: decryptSecret(profile.password), profileName: name };
}

function loadPronoteModule() {
  try {
    return require('pronote-lib');
  } catch (err) {
    if (err && err.code === 'MODULE_NOT_FOUND') {
      fail('Dependency manquante: pronote-lib. Exécute: node .../scripts/pronote-connector.mjs bootstrap');
    }
    fail(`Chargement pronote-lib impossible: ${err.message}`);
  }
}

function ensureOutputDir(profile) {
  const outputDir = profile.outputDir || DEFAULT_VAULT_DIR;
  if (!outputDir) {
    fail('Aucun dossier de sortie défini. Utilise --output-dir au setup.');
  }

  const homeworksDir = path.join(outputDir, 'Homework');
  ensureDir(outputDir);
  ensureDir(homeworksDir);
  return { outputDir, homeworksDir };
}

function connectUser(pronote, profile) {
  return new Promise((resolve, reject) => {
    let created;
    try {
      created = new pronote.User({
        username: profile.username,
        password: profile.password,
        url: profile.url,
        cas: profile.cas
      }, (ok) => {
        if (ok === true) {
          resolve(created);
          return;
        }

        const detail = (() => {
          if (!ok) {
            return 'bad login';
          }

          if (typeof ok === 'string') {
            return ok;
          }

          if (typeof ok === 'object') {
            if (typeof ok.message === 'string' && typeof ok.title === 'string') {
              return `${ok.title}: ${ok.message}`;
            }

            if (typeof ok.message === 'string') {
              return ok.message;
            }
          }

          try {
            return JSON.stringify(ok);
          } catch {
            return 'bad login';
          }
        })();

        reject(new Error(`Échec Pronote: ${detail}`));
      });
    } catch (err) {
      reject(err);
    }
  });
}

function normalizeTimetableWeeks(weeks) {
  const events = [];
  const blocks = Array.isArray(weeks) ? weeks : [];

  for (const week of blocks) {
    const rawItems = Array.isArray(week)
      ? week
      : Array.isArray(week?.content)
        ? week.content
        : [];
    for (const raw of rawItems) {
      if (!raw || !raw.from || !raw.to) {
        continue;
      }

      const start = new Date(raw.from);
      const end = new Date(raw.to);
      if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
        continue;
      }

      const ue = detectUE(raw.subject || raw.Matiere || raw.title || raw.name);
      const subject = raw.subject || 'Cours';
      const teacher = raw.teacher || 'Non spécifié';
      const room = raw.room || '';
      const startIso = toLocalIso(start);
      const endIso = toLocalIso(end);
      const keySeed = `${startIso}|${endIso}|${subject}|${teacher}|${room}`;
      const uid = digest(keySeed);

      events.push({
        uid,
        ue,
        subject,
        teacher,
        room,
        from: start,
        to: end,
        startIso,
        endIso,
        cancelled: Boolean(raw.cancelled),
        absent: Boolean(raw.away),
        durationMin: toMinutes(start, end),
        source: raw
      });
    }
  }

  const dedup = new Map();
  const output = [];

  for (const evt of events) {
    if (!dedup.has(evt.uid)) {
      dedup.set(evt.uid, true);
      output.push(evt);
    }
  }

  output.sort((a, b) => a.from.getTime() - b.from.getTime());
  return output;
}

function sanitizeHomeworkForPayload(homeworks) {
  return homeworks.map((item) => ({
    uid: item.uid,
    subject: item.subject,
    ue: item.ue,
    due: item.due,
    planned_for: item.since,
    to_give: item.toGive,
    delivered: item.delivered,
    can_give_late: item.canGiveLate,
    content_preview: item.content_preview
  }));
}

function normalizeHomework(homeworks) {
  return (Array.isArray(homeworks) ? homeworks : []).map((item) => {
    const due = item.until ? toLocalIso(item.until) : toLocalIso(item.since);
    const since = toLocalIso(item.since);
    const rawSubject = item.subject || 'Cours';

    return {
      uid: item.uid || digest(`${rawSubject}|${due || ''}|${item.content || ''}`),
      ue: detectUE(rawSubject),
      subject: rawSubject,
      since,
      due,
      toGive: Boolean(item.toGive),
      delivered: Boolean(item.delivered),
      canGiveLate: Boolean(item.can_give_late),
      content_preview: item.content ? item.content.slice(0, 240) : '',
      raw: {
        description: item.description,
        classes: item.classes,
        custom: item.custom
      }
    };
  });
}

function coerceMode(mode) {
  const m = toLowerSafe(mode || DEFAULT_MODE);
  if (!['timetable', 'homework', 'full'].includes(m)) {
    fail(`Mode invalide: ${mode}. Utilise timetable, homework ou full.`);
  }
  return m;
}

function sanitizeTimetableForPayload(events) {
  return events.map((event) => ({
    uid: event.uid,
    ue: event.ue,
    subject: event.subject,
    teacher: event.teacher,
    room: event.room,
    start_at: event.startIso,
    end_at: event.endIso,
    duration_min: event.durationMin,
    cancelled: event.cancelled,
    absent: event.absent,
    source: {
      type: event.source?.type,
      className: event.source?.classe || event.source?.className
    }
  }));
}

function toJsonPayload(profile, mode, weeks, startDate, timetable, homeworks, snapshot) {
  return {
    generated_at: toLocalIso(new Date()),
    profile: {
      name: profile.profileName,
      username: profile.username,
      url: profile.url,
      cas: profile.cas
    },
    mode,
    weeks,
    start_from: toLocalIso(startDate),
    counts: {
      timetable: timetable.length,
      homeworks: homeworks.length,
      snapshot: snapshot ? 1 : 0
    },
    timetable: sanitizeTimetableForPayload(timetable),
    homeworks: sanitizeHomeworkForPayload(homeworks),
    snapshot
  };
}

function collectPronoteData(pronote, user, profile, mode, weeks, startDate) {
  const normalizedWeeks = Math.max(1, parseInt(weeks || `${DEFAULT_SYNC_WEEKS}`, 10) || DEFAULT_SYNC_WEEKS);
  const normalizedMode = coerceMode(mode);
  const data = {
    timetable: [],
    homeworks: [],
    snapshot: null
  };

  const promises = [];

  if (normalizedMode === 'timetable' || normalizedMode === 'full') {
    for (let i = 0; i < normalizedWeeks; i += 1) {
      const date = new Date(startDate);
      date.setDate(date.getDate() + (i * 7));
      promises.push(user.get_timeplan(date).then((block) => block));
    }
  }

  return Promise.all(promises).then((timedata) => {
    if (normalizedMode === 'timetable' || normalizedMode === 'full') {
      let allWeeks = [];
      for (const block of timedata) {
        if (Array.isArray(block)) {
          allWeeks = allWeeks.concat(block);
        } else if (block && Array.isArray(block.content)) {
          allWeeks.push(block);
        } else if (block && block?.result && Array.isArray(block.result.content)) {
          allWeeks.push(block.result);
        }
      }
      data.timetable = normalizeTimetableWeeks(allWeeks);
    }

    if (normalizedMode === 'homework' || normalizedMode === 'full') {
      return user.get_homework().then((items) => {
        data.homeworks = normalizeHomework(items);
        return data;
      });
    }

    return data;
  }).then(async (result) => {
    if (normalizedMode !== 'full') {
      return result;
    }

    const snapshot = await collectFullSnapshot(pronote, user, profile);
    result.snapshot = snapshot;
    return result;
  }).then((result) => ({
    data: result,
    mode: normalizedMode,
    weeks: normalizedWeeks
  }));
}

function frontmatterLines(lines) {
  return ['---', ...lines, '---', ''].join('\n');
}

function formatHomeNoteText(event, profile, ue) {
  const state = event.cancelled ? 'Cours annulé' : event.absent ? 'Professeur absent / cours avec alerte' : 'Cours prévu';
  const body = [
    `# Cours Pronote — ${event.subject}`,
    '',
    '## Infos',
    '',
    `- UE : ${ue}`,
    `- Enseignant : ${event.teacher}`,
    `- Salle : ${event.room || 'Non précisée'}`,
    `- État : ${state}`,
    `- Début : ${event.startIso}`,
    `- Fin : ${event.endIso}`,
    `- Durée : ${event.durationMin} min`,
    `- Source : ${profile.url}`,
    '',
    '## Checklist',
    '',
    '- [ ] Extraire 2 questions essentielles',
    '- [ ] Noter 1 point de confusion réel',
    '- [ ] Créer 1 question dans questions-active-recall',
    '',
    `Source profile: ${profile.profileName}`
  ];

  return body.join('\n');
}

function formatHomeworkText(item, profile, ue) {
  const due = item.due || (item.until ? toLocalIso(item.until) : toLocalIso(item.since));
  const subject = item.subject || 'Cours';
  const isPreview = item.content_preview || item.content;
  const body = [
    `# Devoir Pronote — ${subject}`,
    '',
    '## Infos devoir',
    '',
    `- UE : ${ue}`,
    `- Sujet : ${isPreview ? 'Voir détails' : 'Non précisé'}`,
    `- Réalisé pour : ${due || 'non précisé'}`,
    `- À rendre : ${item.toGive ? 'oui' : 'non'}`,
    `- Source : ${profile.url}`,
    '',
    '## Contenu brut',
    '',
    item.content || item.content_preview || 'Aucun contenu détaillé reçu.',
    '',
    '## Actions',
    '',
    '- [ ] Ajouter une piste d’action',
    '- [ ] Relier à la session de révision correspondante',
    `Profile utilisé : ${profile.profileName}`
  ];

  return body.join('\n');
}

function writeMarkdown(filePath, content) {
  fs.writeFileSync(filePath, content, { encoding: 'utf8' });
  return true;
}

function buildClassFrontmatter(event, ue) {
  return frontmatterLines([
    `type: moment`,
    `status: planned`,
    `project: DSCG`,
    `workstream: rattrapage-niveau`,
    `casquette: Carrière & formation`,
    `priority: P1`,
    `moment_type: class_block`,
    `planned_for: ${event.startIso}`,
    `start_at: ${event.startIso}`,
    `due_at: ${event.endIso}`,
    `end_at: ${event.endIso}`,
    `duration_min: ${event.durationMin}`,
    `owner: Andrew`,
    `created_by: Sync`,
    `calendar_layer: dscg`,
    `source_profile: ${event.profileName || 'default'}`,
    `source_uid: ${event.uid}`,
    `proof_expected: capture_3_points_du_cours`,
    `rag: include`
  ]);
}

function buildHomeworkFrontmatter(item, ue, profileName) {
  const due = item.due || (item.until ? toLocalIso(item.until) : toLocalIso(item.since));
  const planned = item.since || item.due || null;
  return frontmatterLines([
    `type: task`,
    `status: planned`,
    `project: DSCG`,
    `workstream: pilotage`,
    `casquette: Carrière & formation`,
    `priority: P2`,
    `task_type: homework`,
    planned ? `planned_for: ${toLocalIso(planned)}` : '',
    due ? `due_at: ${due}` : '',
    `duration_min: 30`,
    `owner: Andrew`,
    `created_by: Sync`,
    `calendar_layer: dscg`,
    `source_profile: ${profileName}`,
    `rag: include`
  ].filter(Boolean));
}

function writeTimetableFiles(events, profile) {
  const { outputDir } = ensureOutputDir(profile);
  let created = 0;

  for (const evt of events) {
    const ue = evt.ue;
    const datePrefix = evt.startIso ? evt.startIso.slice(0, 10) : 'no-date';
    const hourPrefix = evt.startIso ? evt.startIso.slice(11, 16).replace(':', '-') : 'no-hour';
    const fileSlug = `${slug(evt.subject)}-${evt.uid}`;
    const fileName = `${datePrefix} ${hourPrefix} - ${fileSlug}.md`;
    const filePath = path.join(outputDir, fileName);

    const front = buildClassFrontmatter({ ...evt, profileName: profile.profileName }, ue);
    const body = formatHomeNoteText(evt, profile, ue);
    const payload = `${front}\n${body}\n`;

    writeMarkdown(filePath, payload);
    created += 1;
  }

  return { created, path: outputDir };
}

function writeHomeworkFiles(homeworks, profile) {
  const { homeworksDir } = ensureOutputDir(profile);
  let created = 0;

  for (const item of homeworks || []) {
    const ue = item.ue || detectUE(item.subject || item.title || 'cours');
    const base = item.due || item.until || item.since || Date.now();
    const d = new Date(base);
    const due = item.due || (item.until ? toLocalIso(item.until) : toLocalIso(base));
    const keySeed = `${due || item.subject || 'homework'}${item.content || item.content_preview || ''}`;
    const uid = digest(keySeed);
    const name = `${d.toISOString().slice(0, 10)}-${slug(item.subject)}-${uid}.md`;
    const filePath = path.join(homeworksDir, name);

    const front = buildHomeworkFrontmatter(item, ue, profile.profileName);
    const body = formatHomeworkText(item, profile, ue);
    writeMarkdown(filePath, `${front}\n${body}\n`);
    created += 1;
  }

  return { created, path: homeworksDir };
}

function writeSnapshot(profile, data, options) {
  const root = ensureOutputDir(profile).outputDir;
  const snapshotDir = path.join(root, 'Snapshots');
  ensureDir(snapshotDir);

  const ts = toLocalIso(new Date()) || new Date().toISOString();
  const fileName = `Pronote Snapshot - ${ts.replace(/[T:]/g, '-').replace(/\+..:../, '').replace(/\.\d+Z/, '')}.md`;
  const filePath = path.join(snapshotDir, fileName);

  const marksCount = Array.isArray(data.marks) ? data.marks.reduce((acc, p) => acc + (p.marks?.length || 0), 0) : 0;
  const homeworksCount = Array.isArray(data.homeworks) ? data.homeworks.length : 0;
  const absencesCount = Array.isArray(data.absences) ? data.absences.reduce((acc, p) => acc + (p.absences ? p.absences.length : 0), 0) : 0;

  const front = frontmatterLines([
    `type: note`,
    `status: planned`,
    `project: DSCG`,
    `workstream: pilotage`,
    `casquette: Carrière & formation`,
    `owner: Andrew`,
    `created_by: Sync`,
    `proof_expected: sync-check`,
    `source_profile: ${profile.profileName}`,
    `calendar_layer: dscg`,
    `rag: include`
  ]);

  const content = [
    '# Pronote Snapshot',
    '',
    `- Heure sync: ${ts}`,
    `- Élève: ${data.name || 'inconnu'}`,
    `- Classe: ${data.studentClass || 'inconnue'}`,
    `- Devoirs détectés: ${homeworksCount}`,
    `- Notes capturées: ${marksCount}`,
    `- Absences: ${absencesCount}`,
    `- Périodes: ${(data.periods || []).length}`,
    '',
    '## Recommandation',
    '',
    'Lancer une validation manuelle rapide puis intégrer les événements critiques dans `rattrapage-niveau`.',
    ''
  ];

  fs.writeFileSync(filePath, `${front}\n${content.join('\n')}`, { encoding: 'utf8' });
  return filePath;
}

async function collectFullSnapshot(pronote, user, profile) {
  const base = {
    name: profile.username,
    studentClass: 'inconnue',
    marks: [],
    homeworks: [],
    absences: [],
    periods: []
  };

  if (typeof pronote.fetch === 'function') {
    try {
      return await pronote.fetch(profile.username, profile.password, profile.url, profile.cas);
    } catch (err) {
      log(`fetch-failed: ${err.message}`);
    }
  }

  if (typeof user.fetch === 'function') {
    try {
      return await user.fetch();
    } catch (err) {
      log(`user-fetch-failed: ${err.message}`);
    }
  }

  return base;
}

function bootstrap() {
  console.log('Installing pronote-lib dependency...');
  const cmd = `cd ${JSON.stringify(BASE_DIR)} && npm install pronote-lib@${PRONOTE_VERSION}`;
  try {
    execSync(cmd, { stdio: 'inherit' });
    console.log('✅ Installation terminée.');
  } catch (err) {
    fail(`Impossible d’installer pronote-lib. Vérifie npm et permissions. (${err.message})`);
  }
}

function showStatus() {
  const config = getConfig();
  const profiles = Object.keys(config.profiles || {});
  if (profiles.length === 0) {
    console.log('Aucun profil Pronote configuré.');
    return;
  }

  console.log('Profiles Pronote configurés:');
  for (const name of profiles) {
    const p = config.profiles[name];
    console.log(`- ${name}`);
    console.log(`  username: ${p.username}`);
    console.log(`  url: ${p.url}`);
    console.log(`  cas: ${p.cas}`);
    console.log(`  output: ${p.outputDir || DEFAULT_VAULT_DIR}`);
  }
}

function printUsage() {
  console.log(`
Usage:
  pronote-connector setup    --username --password --pronote-url --cas --profile default
  pronote-connector test      --profile default [--json]
  pronote-connector query     --profile default [--weeks 4] [--mode timetable|homework|full] [--from YYYY-MM-DD] [--json]
  pronote-connector sync      --profile default [--weeks 4] [--mode timetable|homework|full] [--from YYYY-MM-DD] [--write-notes] [--json]
  pronote-connector status
  pronote-connector bootstrap
`);
}

async function cmdSetup(args) {
  const password = args.password || (args['password-env'] ? process.env[args['password-env']] : undefined);

  if (!args.username || !password || !args['pronote-url']) {
    fail('setup requiert --username --password --pronote-url.');
  }

  const profile = setProfile({
    profile: args.profile || 'default',
    username: args.username,
    password,
    'pronote-url': args['pronote-url'],
    cas: args.cas || 'none',
    label: args.label,
    'output-dir': args['output-dir']
  });

  console.log(`Profile ${args.profile || 'default'} enregistré.`);
  log(`setup: ${args.username} / ${profile.url}`);

  if (args.test) {
    await cmdTest(args);
  }
}

async function cmdTest(args) {
  const profileName = args.profile || 'default';
  const profile = getProfile(profileName);
  await assertPronoteReachable(profile.url);
  const pronote = loadPronoteModule();
  const user = await connectUser(pronote, profile);
  const week = await collectPronoteData(pronote, user, profile, 'timetable', 1, new Date());

  const eventCount = week?.data?.timetable?.length || 0;
  const msg = `Connexion ok. Étudiant: ${profile.username}\nÉvénements planning détectés: ${eventCount}`;

  if (hasFlag(args, 'json')) {
    const payload = {
      status: 'ok',
      profile: profileName,
      generated_at: toLocalIso(new Date()),
      timetable_count: eventCount,
      test_event: week?.data?.timetable?.[0] ? {
        uid: week.data.timetable[0].uid,
        subject: week.data.timetable[0].subject,
        start_at: week.data.timetable[0].start_at || week.data.timetable[0].startIso,
        duration_min: week.data.timetable[0].duration_min || week.data.timetable[0].durationMin
      } : null
    };
    console.log(JSON.stringify(payload, null, 2));
  } else {
    console.log(msg);
  }

  log(`test-success: ${profileName}`);
}

async function cmdSync(args) {
  const mode = coerceMode(args.mode || DEFAULT_MODE);
  const weeks = Math.max(1, parseInt(args.weeks || `${DEFAULT_SYNC_WEEKS}`, 10) || DEFAULT_SYNC_WEEKS);
  const profileName = args.profile || 'default';
  const profile = getProfile(profileName);
  await assertPronoteReachable(profile.url);
  const pronote = loadPronoteModule();
  const user = await connectUser(pronote, profile);
  const startDate = args.from ? new Date(args.from) : new Date();
  const writeNotes = hasFlag(args, 'write-notes');
  const outputJson = hasFlag(args, 'json');

  if (!Number.isFinite(startDate.getTime())) {
    fail(`Date --from invalide: ${args.from}`);
  }

  const { data, mode: normalizedMode } = await collectPronoteData(
    pronote,
    user,
    profile,
    mode,
    weeks,
    startDate
  );

  const summary = {
    mode: normalizedMode,
    requested_mode: mode,
    weeks,
    write_notes: Boolean(writeNotes),
    counts: {
      timetable: data.timetable.length,
      homework: data.homeworks.length,
      snapshot: data.snapshot ? 1 : 0
    },
    writes: { timetable: 0, homework: 0, snapshot: null },
    payload: null
  };

  if (writeNotes) {
    if (mode === 'timetable' || mode === 'full') {
      const result = writeTimetableFiles(data.timetable, profile);
      summary.writes.timetable = result.created;
      if (!outputJson) {
        console.log(`Timetable: ${result.created} notes -> ${result.path}`);
      }
    }

    if (mode === 'homework' || mode === 'full') {
      const result = writeHomeworkFiles(data.homeworks, profile);
      summary.writes.homework = result.created;
      if (!outputJson) {
        console.log(`Homework: ${result.created} notes -> ${result.path}`);
      }
    }

    if (mode === 'full') {
      const snapshotPath = writeSnapshot(profile, data.snapshot, { mode });
      summary.writes.snapshot = snapshotPath;
      if (!outputJson) {
        console.log(`Snapshot: ${snapshotPath}`);
      }
    }
  }

  if (outputJson) {
    summary.payload = toJsonPayload(
      profile,
      normalizedMode,
      weeks,
      startDate,
      data.timetable,
      data.homeworks,
      data.snapshot
    );
    console.log(JSON.stringify(summary, null, 2));
  } else {
    console.log(`Synchronisation ${writeNotes ? 'avec' : 'sans'} création de notes: ${JSON.stringify(summary)}`);
  }

  log(`sync-${mode}: ${profileName}`);
}

async function cmdQuery(args) {
  const mode = coerceMode(args.mode || DEFAULT_MODE);
  const weeks = Math.max(1, parseInt(args.weeks || `${DEFAULT_SYNC_WEEKS}`, 10) || DEFAULT_SYNC_WEEKS);
  const profileName = args.profile || 'default';
  const profile = getProfile(profileName);
  await assertPronoteReachable(profile.url);
  const pronote = loadPronoteModule();
  const user = await connectUser(pronote, profile);
  const startDate = args.from ? new Date(args.from) : new Date();
  const outputJson = hasFlag(args, 'json');

  if (!Number.isFinite(startDate.getTime())) {
    fail(`Date --from invalide: ${args.from}`);
  }

  const { data, mode: normalizedMode } = await collectPronoteData(
    pronote,
    user,
    profile,
    mode,
    weeks,
    startDate
  );

  const payload = toJsonPayload(profile, normalizedMode, weeks, startDate, data.timetable, data.homeworks, data.snapshot);

  if (outputJson) {
    console.log(JSON.stringify(payload, null, 2));
    log(`query-${mode}: ${profileName}`);
    return;
  }

  const sampleHomework = (data.homeworks || [])[0];
  const sampleText = sampleHomework
    ? `\nÉchantillon devoir: ${sampleHomework.subject || 'inconnu'} (UE ${sampleHomework.ue || 'inconnue'})`
    : '';

  console.log(`Connexion ok — mode ${normalizedMode}`);
  console.log(`Timetable détecté: ${payload.counts.timetable}`);
  console.log(`Devoirs détectés: ${payload.counts.homeworks}`);
  console.log(sampleText);
  log(`query-${mode}: ${profileName}`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0] || 'help';

  if (args.help || command === 'help') {
    printUsage();
    return;
  }

  if (command === 'bootstrap') {
    bootstrap();
    return;
  }

  if (command === 'setup') {
    await cmdSetup(args);
    return;
  }

  if (command === 'test') {
    await cmdTest(args);
    return;
  }

  if (command === 'sync') {
    await cmdSync(args);
    return;
  }

  if (command === 'status') {
    showStatus();
    return;
  }

  if (command === 'query') {
    await cmdQuery(args);
    return;
  }

  fail(`Commande inconnue: ${command}`);
}

main().catch((err) => {
  fail(`Erreur: ${err?.message || err}`);
});
