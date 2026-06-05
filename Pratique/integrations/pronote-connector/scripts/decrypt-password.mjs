#!/usr/bin/env node
/**
 * Decrypts the stored Pronote password for a given profile.
 * Outputs just the raw password to stdout.
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';

const CONFIG_DIR = path.join(os.homedir(), '.openclaw', 'pronote-connector');
const CONFIG_FILE = path.join(CONFIG_DIR, 'profiles.json');
const MASTER_KEY_FILE = path.join(CONFIG_DIR, 'master.key');

const profileName = process.argv[2] || 'default';

const masterKey = fs.readFileSync(MASTER_KEY_FILE, 'utf8').trim();
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
const profile = config.profiles[profileName];

if (!profile) {
  console.error(`Profile ${profileName} not found`);
  process.exit(1);
}

const payload = profile.password;
const key = Buffer.from(masterKey, 'hex');
const iv = Buffer.from(payload.iv, 'base64');
const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
decipher.setAuthTag(Buffer.from(payload.tag, 'base64'));
const decrypted = Buffer.concat([
  decipher.update(Buffer.from(payload.ciphertext, 'base64')),
  decipher.final()
]);

process.stdout.write(decrypted.toString('utf8'));
