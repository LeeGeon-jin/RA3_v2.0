# Next (R57): V4 speed + Apocalypse cost/speed — decided, not implemented
Refs: `apoc_v4_sdk_refs.tar.gz` (11 SDK files, read-only).
**Not in the package:** b91 has no `Soviet/Units/SovietAntiStructureVehicle.xml` or `SovietAntiVehicleVehicleTech3.xml`, and no Locomotor.xml.

## Requirement quotes (devdoc)
- **L815 (user):** "v4发射器若价格超过1500，改为1500，若建造时间超过15秒…天启坦克若建造时间超过20秒…（本人补充：v4发射车的速度若低于70改成70）". Difficulty 容易, phase 一.
- **L818-819:**
  - V4 is 1200 / 15 s → no change; LocomotorSet Speed 50.0 → **70**. Its locomotor is used only by V4, so no Locomotor edit is needed.
  - Apocalypse BuildTime 20 → no change.
  - The Heidelberg map `overrides.xml` has Apocalypse BuildTime 60 → 20. That is a campaign map file outside this XML package → **separate item, not in this batch**.
- **L821 (user):** "天启坦克移动速度1.5倍，可移动攻击，增加对空能力，对空用打击者vx的导弹，同时多辆天启可以用磁力鱼叉…造价改为1750，建造时间20秒". Phase 一/二.
- **L825:** Cost 2000 → **1750**; BuildTime 20 (unchanged); Speed 50 → **75**. The main gun already has CanFireWhileMoving="true", so nothing to do. AA reuses JapanAntiAirVehicleTech1_LandMissileLauncher. Multi-harpoon on one target: no XML limit found → test.

## SDK (both inherit BaseVehicle, include GlobalDefines directly; loaded via Soviet/Soviet.xml L20/L23)
- **SovietAntiStructureVehicle.xml** (398 lines): BuildTime 15 (L46), cost 1200 (L62), one LocomotorSet Speed="50.0" (L67-70).
- **SovietAntiVehicleVehicleTech3.xml** (777 lines): BuildTime 20 (L64), cost 2000 (L80), one LocomotorSet Speed="50.0" (L85-88).

## Minimal Batch 57 (values only; same convention as Batch49 SovietMCV)
- Full SDK copy at the same path, value edits only, `Mod.xml` +1 `type="all"` include each:
  - `data/Soviet/Units/SovietAntiStructureVehicle.xml`: L70 Speed 50.0 → 70.0.
  - `data/Soviet/Units/SovietAntiVehicleVehicleTech3.xml`: L80 Amount 2000 → 1750; L88 Speed 50.0 → 75.0.
- Expected `diff -w` vs SDK: exactly those 3 value lines. Mod 104 all.
- **Deferred to a later batch (decided but needs weapon-slot work):** Apocalypse AA. It means adding a WeaponSetUpdate slot that reuses the Striker-VX land missile, its targeting/turret, and AI. Plan it separately and don't mark row 20 complete.
- **Deferred to a separate test item:** the multi-harpoon check, and the Heidelberg overrides fix.

## Open
- None for the values.
- Campaign variants: doc L818 found no other inheriting variants or cost overrides.
- Test: V4/Apocalypse movement at the new speeds, crush/pathing.
