> **PARKED (doc 第二批; not scheduled; superseded as "next" by NEXT_R83).**

# NEXT R82 — Mirage tank fires while moving (read-only research)

## User wording
- doc L589: "幻影坦克可以移动开火（本人补充：而且别忘了它和幻影坦克都能移动同时攻击而不是停下才能攻击…）（本人确认方案：好，就这样改）"
- doc L10 (2026-11-06 revision): "AlliedAntiVehicleVehicleTech3PrismCannon 与 _Veteran 的 AcceptableAimDelta 都由 10d 改为 180d，_Veteran 的 CanFireWhileMoving 由 false 改为 true；幻影坦克与先进幻影坦克同时生效。第七章保留外观实测项（…不行退到 90d）"
- Batch: 二. Difficulty: easy.

## Current state (package == SDK, content identical)
- GlobalData/Weapon.xml `AlliedAntiVehicleVehicleTech3PrismCannon`: CanFireWhileMoving="true", AcceptableAimDelta="10d" (package ~L2474-2480).
- `..._Veteran`: CanFireWhileMoving="false", AcceptableAimDelta="10d" (~L2550-2556).

## Minimal change (values come from the user-confirmed doc, not invented)
1. PrismCannon: `AcceptableAimDelta="10d"` → `"180d"`.
2. PrismCannon_Veteran: `AcceptableAimDelta="10d"` → `"180d"`.
3. PrismCannon_Veteran: `CanFireWhileMoving="false"` → `"true"`.

Nothing else changes: range, damage, laser, OCL, FX, force-field (GENERIC_TOGGLE_STATE still forbids firing).

## Evidence and dependencies
- **Schema:** AssetTypeWeaponTemplate.xsd L902 `AcceptableAimDelta` type Angle. **Precedent:** 34 SDK weapons use `180d`.
- **Who uses these weapons:**
  - Allied/Units/AlliedAntiVehicleVehicleTech3.xml (WeaponSlotHardpoint L485 / L489; L607 laser ref);
  - SDK Allied/Units_Campaign/CAMP_A08_SpecialMirageTank.xml (inherits AlliedAntiVehicleVehicleTech3; the Havana campaign tank also gains this — consistent with "同时生效");
  - a future AlliedAdvancedMirageTank would inherit it.
- The unit file is not touched. The package currently has 130 XML; the change stays inside Weapon.xml.

## Runtime only (ch.7 L1596)
- How the beam looks firing sideways from the nose at 180d (fallback 90d is the user's own stated alternative).
- Whether the veteran weapon fires while moving correctly.

## Refs
r82_sdk_refs.tar.gz.
