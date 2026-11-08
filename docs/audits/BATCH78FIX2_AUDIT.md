# BATCH78FIX2 AUDIT — SOURCE PASS (source candidate only)
No full XSD / compile / in-game test. Not Phase1 complete.

## Package
- `batch78fix2.tar.gz`: 302157 B, sha256 9e8991d7…6660c479 match. data/ root, cumulative. 124 XML parse. Mod: 3 reference / 122 all.
- vs 78FIX: only the 3 centers differ. In each, the identical 3-line `<ObjectResourceInfo><BuildCost …2000/></ObjectResourceInfo>` block was moved after `</GameDependency>`; nothing else changed. The other 121 XML are byte-identical to 78FIX.
- Order now: DisplayName → GameDependency → ObjectResourceInfo → Draws → Behaviors → Body → ArmorSet → Geometry → AudioArraySound.

## Correction of my 78FIX verdict
- My only 78FIX FAIL reason ("ObjectResourceInfo before GameDependency violates the xs:sequence") was **over-strict**. SDK-wide scan: 71 of 4303 SDK GameObjects deviate from the xsd sequence order, including the shipped skirmish `Allied/Structures/AlliedAirfield.xml`, whose order is DisplayName → ObjectResourceInfo → ArmorSet → GameDependency (the same pattern), and AlliedSuperWeapon.
- So EA's builder evidently tolerates order deviations; 78FIX was effectively a source pass too. FIX2 is harmless and now matches the xsd order for those two elements.
- The remaining `Body → ArmorSet` order is verbatim from the SDK HQ original (same tolerated class).

## The 6 earlier fixes kept
ObjectResourceInfo cost 2000; no StartsActive; Soviet 28s; BuildPlacementTypeFlag OTHER_STRUCTURE; BaseStructure / BaseSovietStructure + repair / engineer includes + additive KindOf; ACTIVATE_AFTER_UNPACK (Soviet); 5 entry lists; HP 2000/2000, -75, limit 1, prereqs.

## Open (not source conditions)
- **No build/unpack animation:** user requirement for the quick production center ("直放无动画"), not a defect.
- **Missing Name/Type/Desc keys:** pending unified localization.
- **Runtime not proven:** PRODUCTION 200% halving; refresh vs stacking; Range 99999 map coverage; lapse ≤2s on death / sell / capture; Soviet aura before unpack completes.
