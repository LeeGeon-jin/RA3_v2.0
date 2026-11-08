# Next (R62): Bullfrog flak can also hit ground — decided, not implemented
Refs: `bullfrog_sdk_refs.tar.gz` (7 SDK files: SovietAntiAirShip, Weapon, AlliedAntiAirVehicleTech1, AlliedBaseDefense, SovietAntiVehicleVehicleTech1, AssetTypeWeaponTemplate.xsd, WeaponSetUpdate.xsd).

## Requirement
- **5.5 #10, L761 (user):** "牛蛙载具不仅能对空，还能对地，对地伤害延续对空的设定". Difficulty 容易, phase 一. No later revision found.
- **L764 (plan):** `SovietAntiAirShipFlakCannon` air-only → add `ANTI_GROUND ANTI_WATER ANTI_STRUCTURE` to RequiredAntiMask; damage stays on the same weapon.

## Package state (b96), not done
- **Weapon** (Weapon.xml L3983-4005): `RequiredAntiMask="ANTI_AIRBORNE_VEHICLE ANTI_AIRBORNE_INFANTRY ANTI_PARACHUTE"` (L3988). Damage 15 / r15 FLAK, FiringDuration 0.2s, unlimited clip, CanFireWhileMoving. Same as SDK.
- **Unit:** `Soviet/Units/SovietAntiAirShip.xml` is in the package (BuildTime 8, passengers survive). Its turret ID1 = this weapon, **MinimumPitch 15d**, AllowsPitch true (L227-249).
- **CampaignOverrides** L898 overrides SovietAntiAirShip without touching weapons.

## Dependency found (important)
Three templates inherit this weapon fully, without their own RequiredAntiMask:

| Template | Weapon.xml line | Used by |
|---|---|---|
| `AAAVT1_SovietAntiVehicleFlakLauncher` | L5874 | IFV with flak trooper, AlliedAntiAirVehicleTech1 L530 |
| `ABD_SovietAntiVehicleFlakLauncher` | L6017 | Allied multigunner turret, AlliedBaseDefense L374 |
| `Leech_FlakCannon` | L7124 | Hammer leech, SovietAntiVehicleVehicleTech1 L868 |

Changing the parent alone would also give these three ground attack. That's an unrequested side effect.

## Minimal Batch 62 (Weapon.xml text edit only)
1. L3988 parent mask → `"ANTI_AIRBORNE_VEHICLE ANTI_AIRBORNE_INFANTRY ANTI_PARACHUTE ANTI_GROUND ANTI_WATER ANTI_STRUCTURE"`.
2. Add the original `RequiredAntiMask="ANTI_AIRBORNE_VEHICLE ANTI_AIRBORNE_INFANTRY ANTI_PARACHUTE"` as an attribute to each of the three children (L5874/6017/7124 opening tags), so their behaviour stays as before.
- **Expected:** Weapon.xml diff = 4 lines (or attribute-line additions). No other file; 111 XML.
- **Alternative (not recommended):** a new Bullfrog-only template + unit file edit. The doc says to use the same weapon.

## Open / native test (not decided, do not change now)
- **Turret MinimumPitch 15d may stop the barrel aiming at ground targets.** The doc's AA-gun row (L779) solved this with MinimumPitch -10d, but **for the Bullfrog no pitch value is decided** → test first. If it can't fire at ground, ask the user for a pitch.
- Ground damage uses FLAK armor coefficients (L781: infantry 10% / vehicle 150% / tank 100%), as "延续对空的设定" says.
- Whether the Hammer's leeched flak should also gain ground attack is not in the doc → kept unchanged.

## Exhaustion note (simple decided rows checked this round, already in package)
Stingray land 80 + Nova on land; Akula 15; Yari 5; Tesla trooper 500/8/0.25; Dreadnought drain 25 / 600%; Shogun 20 / 3.5; Twinblade 12; Kirov 2000/20; Japan miner 75; wave-gun premature removed; Yuriko delays.
Still blocked by a user decision:
- bunker (conflict L31/L215);
- Hammer Max reload;
- Apocalypse AA aim/mode/bone;
- AA-gun ground weapon variant (L779 offers a primary and an alternative: needs a choice, and the pitch -10d is plan text);
- Twinblade AA (L833: mask vs 2nd slot, unspecified);
- paradrop button;
- Guard02, cloning and quick-production health.
