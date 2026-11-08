# BATCH79FIX AUDIT — SOURCE PASS (source candidate). No full XSD / compile / in-game test; not Phase1 complete.

## Package
- 321321 B, sha256 8fcee486…660ea2af14 match. data/ root, cumulative. 130 XML parse. Mod: 3 reference / 128 all.
- **vs 79:**
  - +3 infantry (AlliedScoutInfantry, SovietScoutInfantry, SovietAntiInfantryInfantry);
  - −2 (Civilian/Geneva.xml, Geneva_GE bunker);
  - modified: SovietCloningCenter, JapanScoutInfantry, Mod.
  - The other 124 files are byte-identical. The Mod diff is exactly −2 includes, +3 includes.
- vs 78FIX2, the old semantics are preserved. The only extra change is the Allied barracks veterancy restore, already noted in BATCH79_AUDIT.

## Fixes
1. **3 infantry:** full SDK copies. The diff against the SDK shows only ART include removals + one appended `ObjectCreationUpgrade ModuleTag_Clone` (own id, TriggeredBy Upgrade_CloneMe). All behaviors, models, draw and DATA includes are kept.
   - Dog and bear: all ART includes removed (41 / 49 lines), matching the package convention.
   - Conscript: **only 4 of 133** ART includes removed (NPSkeleton_SKN / DIEA, NPRadiation / DIEA); 129 kept. This is inconsistent with the convention but not a semantic loss: those NP models are shared and globally loaded by the base game. Non-blocking note.
2. **Duplicate OCL:** the center's OCL is renamed `SovietCloningCenter_Die_OCL` with its single reference updated. The bunker file defining the GE_ id is removed from package and Mod, so there is no duplicate.
3. **Geneva.xml and the original bunker object:** removed from package and Mod. The collapse object stays (used by the center's instance include).
4. **Restored:** debris `AlliedBarracks_Debris` (defined in SDK Allied/Props, loaded globally by Allied.xml L166) and the empty damage sounds = SDK original. The YU_HotelDebris instance include remains (unused, harmless).
5. **OwnershipAmount 1–6 → Upgrade_SovietCloning.** Schema: OwnershipAmount is a SageInt, with no exact-vs-threshold statement; the academy precedent (1/2/3 → different upgrades) does not settle it.
   - 6 is not a mathematical cap. Each player can build one, and centers can be captured and the loser rebuilds, so one player can hold >6 over time.
   - Under exact-count semantics, 7+ would be unmapped. This is a real but limited residual risk; it does not cover every case.
6. **Drone:** JapanScoutInfantry has no clone module. Its only difference from the 78FIX2 file is whitespace / indentation at L352-356 (`</FireWeaponWhenDead>`, a blank line, `</Behaviors>`), so it is semantically restored though not byte-identical.
- **18 true INFANTRY** now carry ModuleTag_Clone with their own id.
- **Unchanged from 79:** center build chain (Soviet CY / crane), BaseSovietStructure ACTIVATE_AFTER_UNPACK, 3 barracks translates, 2 upgrades in Mod-included upgrade.xml.

## Runtime only
- self-built grant;
- revocation on destroy / sell / capture;
- grant during the 30s unpack;
- OCU single fire / no recursion;
- clone owner and placement;
- queued units at loss;
- performance.
(Tanya / Yuriko / Natasha limits are already cancelled per doc L530 / L994 / L741 and are absent in the package.)
