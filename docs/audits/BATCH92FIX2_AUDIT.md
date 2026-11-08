# BATCH92FIX2 AUDIT — STATIC PASS (candidate), 2026-11-08 22:56 UTC+10
## Package
- batch92fix2.tar.gz = store handoff/RA3_V2.0_Batch92FIX2_SovietSpy.tar.gz. 352367 B, sha256 9c5cd9fdab62f80595f030927e34e0d4f10aa823ba594918ea1f7e7317dee408. Matches; the host asset is identical.
- Root is data/. 143 XML. Mod.xml: 138 type="all" + 3 reference (static / global / audio).

## Checks
- vs 92FIX: only Mod.xml differs, and the only change is the deleted line `<Include type="all" source="DATA:UIInGame/UIComponentObjectSelector.xml" />`. The other 142 files are byte-identical and nothing was reverted.
- **All 138 type="all" targets exist in the package and have an AssetDeclaration root** (scripted check: 0 non-asset).
- The package has exactly 3 fragment files. None of them is in Mod.xml, and each is reached only by xi:include from a package file:
  - Includes/InfantryFighting/IF_SecondaryObjectListener.xml ← AlliedAntiAirVehicleTech1 L726, AlliedBaseDefense L573
  - UIInGame/UIComponentObjectSelector.xml ← UIConfigs L34
  - UI/Mouse/Components/UIComponentOptionsSettingsGeneral.xml ← UIConfigs (B72 precedent)
- The 92 / 92FIX conclusions on content carry over unchanged (content is byte-identical):
  - spy object diff limited to id / Side / names / prerequisite SovietWarFactory / clone ThingToSpawn; 1000 / 8; Draws and modules kept;
  - the cloning chain reaches the new spy;
  - 4 ranks with an instance include of SDK ExperienceLevels.xml, parents present, no cycle;
  - bribe exclusion; IFV golden-gun IncludeThing; hotkey-group IncludeThing;
  - LC / LCS single definitions.
- Constraints kept:
  - Cloning center MaxSimultaneousOfType=1.
  - Normal mirage Speed 80.
  - Weapon.xml (R89/R90), SovietBaseDefenseAir (R90) and the Tesla tank (R91) are byte-identical to 91.
  - Advanced mirage not created.

## Not proven (compile / runtime)
- Whether the package fragment copies (IFV listener, object selector) take precedence over the SDK copies for xi:include. Statically reachable, precedence unproven.
- Instance include of the Static-stream ExperienceLevels.xml from the mod stream, and rank display.
- All Soviet-spy game behaviour: production, disguise, bribe, infiltration, cloning, IFV golden gun, hotkey, voices, AI.
- R92 is a static candidate only, not final functional acceptance.
