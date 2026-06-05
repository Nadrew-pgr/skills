# Math Primitives For Motion

Use this reference internally. Do not expose formulas to the user unless asked. Goal: translate visual language into precise movement.

## Coordinate Systems

2D screen space:

- `x`: horizontal, positive right.
- `y`: vertical, positive down in CSS/HTML canvas, often positive up in abstract math.
- `origin`: anchor point used for rotation/scale.
- `viewport`: `{ width, height }`.
- `center`: `{ x: width / 2, y: height / 2 }`.

3D reminder:

- `x`: horizontal.
- `y`: vertical.
- `z`: depth.

Always specify which space is being used: CSS pixels, normalized `0..1`, viewport-relative, world units, or composition pixels.

## Interpolation

Linear interpolation:

```ts
lerp(a, b, t) = a + (b - a) * t
```

Vector interpolation:

```ts
p(t) = {
  x: lerp(p0.x, p1.x, t),
  y: lerp(p0.y, p1.y, t)
}
```

Clamp progress:

```ts
u = clamp((time - start) / duration, 0, 1)
```

Apply easing:

```ts
t = ease(u)
p = lerp(start, end, t)
```

Use linear values for exact data. Use eased values for perceived motion.

## Common Easing Shapes

Ease out:

```ts
easeOutCubic(t) = 1 - (1 - t)^3
```

Ease in-out:

```ts
easeInOutCubic(t) =
  t < 0.5 ? 4t^3 : 1 - ((-2t + 2)^3) / 2
```

Exponential settle:

```ts
settle(t) = 1 - exp(-k * t)
```

Use:

- ease-out for entrances and UI reveals;
- ease-in for exits;
- ease-in-out for camera/crop moves;
- spring/settle for physical follow-through.

## 2D Paths

Line:

```ts
p(t) = p0 + (p1 - p0) * t
```

Quadratic Bezier:

```ts
p(t) = (1 - t)^2 * p0 + 2(1 - t)t * p1 + t^2 * p2
```

Cubic Bezier:

```ts
p(t) =
  (1 - t)^3 * p0 +
  3(1 - t)^2t * p1 +
  3(1 - t)t^2 * p2 +
  t^3 * p3
```

Arc around center:

```ts
x = cx + cos(theta0 + deltaTheta * t) * r
y = cy + sin(theta0 + deltaTheta * t) * r
```

Use Bezier for cinematic swerves. Use arcs for orbit/halo motion. Use lines for product UI clarity.

## Direction, Angle, Normal, Tangent

Vector:

```ts
v = p1 - p0
```

Length:

```ts
len = sqrt(v.x^2 + v.y^2)
```

Normalize:

```ts
n = v / max(len, epsilon)
```

Angle:

```ts
angle = atan2(v.y, v.x)
```

Tangent on a path:

```ts
tangent = normalize(p(time + dt) - p(time - dt))
```

2D normal:

```ts
normal = { x: -tangent.y, y: tangent.x }
```

Use tangent for element rotation along a path. Use normal for impact deformation, offset trails, shadows, and side labels.

## Impact And Contact

Do not animate an impact before contact.

Contact starts when distance to surface/target is below threshold:

```ts
d = distance(point, surfacePoint)
contact = d <= radius + epsilon
```

Impact compression:

```ts
compression = max(0, 1 - d / impactRadius)
```

Recovery:

```ts
recovery(t) = exp(-damping * t) * cos(frequency * t)
```

For a surface hit:

- contact point = closest point on surface;
- normal = direction away from surface;
- compression moves surface inward along normal;
- recovery returns along same normal;
- tangential drag can stretch the deformation along the incoming tangent.

Impact sequence:

1. approach;
2. contact;
3. compression;
4. absorption or bounce;
5. recovery/settle.

## Parallax

Layer position:

```ts
xLayer = xBase + cameraX * depthFactor
yLayer = yBase + cameraY * depthFactor
```

Typical factors:

- far background: `0.05..0.15`;
- mid layer: `0.2..0.45`;
- subject: `0.7..1.0`;
- foreground: `1.1..1.6`.

Use parallax to create spatial progress without moving every element.

## Crop, Pan, And 2D Camera

2D camera is usually a wrapper transform or crop window:

```ts
screenX = (worldX - cameraX) * zoom + viewportCenterX
screenY = (worldY - cameraY) * zoom + viewportCenterY
```

Use:

- pan: animate `cameraX/cameraY`;
- crop zoom: animate `zoom` around a focal point;
- graphic scale: animate element scale only when the element itself should grow.

To zoom toward a focal point without drift:

```ts
cameraX = focalX - (focalScreenX - viewportCenterX) / zoom
cameraY = focalY - (focalScreenY - viewportCenterY) / zoom
```

## Stagger

Index-based stagger:

```ts
delay_i = i * stagger
```

Distance-based stagger:

```ts
delay_i = distance(point_i, origin) / waveSpeed
```

Use distance-based stagger for waves, attraction, liquid, and magnetic motion. Use index-based stagger for lists and text.

## Text Reveal

Per-character or per-word reveal:

```ts
delay_i = i * 0.015s
y_i = startY + overshoot * (1 - t)
opacity_i = t
```

Rules:

- reveal text fast enough to read;
- do not move body text while user must understand it;
- preserve final static readability.

## Product UI Focus

Focus motion:

```ts
focusScale = lerp(1, 1.02, t)
backgroundOpacity = lerp(0.4, 0.7, t)
unfocusedOpacity = lerp(1, 0.45, t)
```

Use focus rings, cursor movement, panel masks, and data-flow arrows before cinematic camera moves.

## Agent Prompt Translation

When user says:

- "enter" -> define boundary, camera/crop path, parallax, contact/threshold.
- "liquid" -> define delayed follow-through, distance-based stagger, deformation normal.
- "magnetic" -> define attractor point, acceleration, overshoot, settle.
- "impact" -> define contact time, normal, compression, recovery.
- "horizontal story" -> define track axis, section width, cameraX curve, parallax factors.
- "precise" -> provide coordinates, durations, easing, timestamps.
