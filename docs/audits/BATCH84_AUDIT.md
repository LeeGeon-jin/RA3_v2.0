# BATCH84 AUDIT — SOURCE PASS (source candidate). Ukraine cannon projectile path adjustment
Static check only: no compile, no in-game test, no PC. Not Phase 1 complete.

## Package
- Host asset = cloud handoff `RA3_V2.0_Batch84_UkraineCannonHoming.tar.gz` (cmp identical) → `batch84.tar.gz`.
- **Real size 336438 B, sha256 bf69de21c7faac387d727a48c44a660b9214b4ba2ca335b34614a1f919164d69.** The cloud's "336896" is wrong; the SHA prefix bf69 matches.
- 136 XML, 134 all; no non-XML files.
- vs 83: **only** `Civilian/Kremlin_KR/Buildings/KR_ArtilleryDome.xml`, +1 line L252 `FlightPathAdjustDistPerSecond="1000"` in the `BezierProjectile` of `KremlinArtilleryDomeMissleProjectile`. The other 135 XML files are byte-identical.

## Chain and shared scope (package file)
- `KR_ArtilleryDome` (campaign object) → WeaponSetUpdate → `KremlinArtilleryDomeMissle` (L161).
- `SovietArtilleryDome` (the buildable Soviet version, L377) → `SovietArtilleryDomeMissle` (L340, 25d aim).
- **Both** weapons use ProjectileNugget `ProjectileTemplate="KremlinArtilleryDomeMissleProjectile"`, `WarheadTemplate="KremlinArtilleryDomeMissleWarhead"`. So the change applies to both domes; nothing else references the projectile.
- **Unchanged:**
  - AttackRange 800, MinimumAttackRange 300, WeaponSpeed 500, RequiredAntiMask ANTI_GROUND ANTI_STRUCTURE ANTI_WATER;
  - warhead damage, collision, FX;
  - Bezier heights 50 / 50, indents 33 / 66, Flags ORIENT_TO_FLIGHT_PATH DETONATE_CALLS_KILL, GroundHitFX.

## Was it originally homing? Is it now like the Allied coastal gun?
### Schema (Modules/BezierProjectile.xsd)
- `FlightPathAdjustDistPerSecond` type Velocity, **no default** (L70).
- The flag list includes **`DONT_TRACK_TARGET`** (L24). That implies the Bezier projectile normally follows the target's position, and this attribute limits how far per second the flight path may be re-aimed.
- The xsd has no doc text, so this meaning is inferred from the names. There is no separate "TrackTarget" attribute.

### Original dome projectile (SDK)
- `DONT_TRACK_TARGET` is not set, but **FlightPathAdjustDistPerSecond is not set either**. With no default, that most likely means 0 adjustment.
- So it aims at the impact point computed at launch and does not correct, which matches the doc's description of the coastal gun "shooting where the unit was". Static inference, not proven in game.
- **Answer: originally effectively not homing.**

### Allied coastal gun (package, B-batch)
- `FXCostalGunProjectileHoming` is a **mod-created** projectile (0 hits in the SDK): BezierProjectile with flags ORIENT_TO_FLIGHT_PATH DETONATE_CALLS_KILL, heights 0 (flat), FlightPathAdjustDistPerSecond 1000, no DONT_TRACK_TARGET.
- Weapon WeaponSpeed 2000 (L367).

### Comparison
- **Same:** the same homing mechanism and the same correction rate (1000) — no DONT_TRACK_TARGET, an adjust value set.
- **Different (intended, untouched):** the dome keeps its 50-high arc and WeaponSpeed 500 (a slower shell, so more time to correct). The coastal gun flies flat at 2000.
- **SDK usage of this attribute:** 57 uses, most commonly 100 / 50 / 300. 1000 is far above them and matches only the mod's coastal gun.
- **Answer: now uses the same tracking setting as the coastal gun; trajectory / speed differ by design.**

## Runtime caveats
- whether 1000 is enough for an arcing shell to hit fast movers ("极快单位偏就偏");
- visible path bending;
- whether the minimum range (300) behaviour changes.
- Source candidate only.
