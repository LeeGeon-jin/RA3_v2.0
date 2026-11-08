# R72 research: classic mouse semantics, UIConfigs route, Natasha one-shot, remaining blockers
Refs: `r72_sdk_refs.tar.gz` (46867 B, sha256 a8c3f915…ef266594):
- UIConfigs, UIComponentOptionsSettingsGeneral (.xml/.xsd), AssetTypeUIConfigList.xsd, static_platformspecific;
- SovietCommandoTech1, Weapon, Armor.

## 1. "Alternate Mouse" = classic left-click? (public sources, no game test)
- **GameReplays, RA3 thread "Why does deselecting not work with certain units?"** (Aug 2008): https://www.gamereplays.org/community/index.php?showtopic=398843
  - Derek: "The Classic Controls are currently broken, there is no way to deselect units… You'll just have to use right-click order mode for now."
  - VeDz in the same thread: "I'm using the Alternate Mouse Setup too."
  - Dibelius: "I also use classic mouse setup…".
  - → In RA3 the "Alternate Mouse Setup" option is the classic left-click-order mode (right-click = deselect); the default is right-click order mode.
- **CNCNZ, C&C3 news** https://forums.cncnz.com/topic/7381-cc-3s-leftright-click-issue/
  - EA (C&C3, same SAGE family): "implementing alternate mouse setup in patch 1.01" as the way back to the original left-click method.
- **C&C Labs** https://www.cnclabs.com/forums/posts/9566/particle-cannon-speed-and-alternate-mouse-setup/
  - Confirms the option name "Alternate Mouse Setup" in Options.
  - The user there is unsure which state is which → weak evidence; not relied on.
- **Conclusion:**
  - The option semantics (Alternate = classic left-click) are supported by public sources.
  - That the SDK field `DefaultAlternateMouse` is the default of *that* checkbox is only by name (no SDK string/UI binding found) → **native verification needed**. Technically plausible, not proven.
  - Public reports also note classic-mode quirks (e.g. deselect, fast scroll), which are original-game behaviour.

## 2. UIConfigs route (static stream)
- **Asset:** `GlobalData/UIConfigs.xml` (165 lines) is a normal AssetDeclaration with one `UIConfigList id="DynamicUIConfigList"` plus 8 ART includes.
  - Loaded by static_platformspecific.xml L28 (Static.xml L18).
  - As a package `type="all"` same-id copy it follows the Weapon/Armor pattern. It can enter Mod as an asset; whether it overrides the static one is unproven.
- **Its includes:** 107 xi:include, 70 unique DATA: targets — **all exist in SDK XMLFiles**. One differs only in case: `UIComponentMouseIngame.xml`, harmless on Windows.
  - xi:include paths need no rewriting: `DATA:` resolves to the package copy first, then SDK. The package already relies on this, e.g. `DATA:Includes/GenericEngineerContain.xml`.
- **Component:** `UIComponentOptionsSettingsGeneral.xml` is an xi:include fragment (root element, 8 required children per xsd; AssetTypeUIConfigList.xsd L163). It must NOT be put in Mod.xml.
- **Minimal batch:**
  - `data/GlobalData/UIConfigs.xml` = full SDK copy, unchanged; keep the 8 ART includes (UI decals, safest);
  - `data/UI/Mouse/Components/UIComponentOptionsSettingsGeneral.xml` = full copy, only L15 `false`→`true`;
  - Mod +1 (UIConfigs).
  - → 118 XML (116+2), Mod 116 all. Other files byte-identical.
- **Risks:**
  - no SDK precedent for overriding UIConfigList;
  - SDK UI_Modification.htm: "modification of the UI beyond texture replacement is not possible" (about Apt screens);
  - existing profiles keep their setting.
- **Classification:** implementable as a **test batch**, with semantics and override marked 待原生验证.

## 3. Natasha "对付载具、舰船改为用狙击枪一枪打爆一辆" (L737) — research only
- **Current:** SovietCommandoSniperRifle (Weapon L713-762): LineDamageNugget 1000 SNIPER with filter `Rule="NONE" Include="INFANTRY"` → infantry only.
  - Vehicle and ship armors also take SNIPER at 0% (BaseVehicleArmor, BaseSurfaceShipArmor).
  - So vehicles/ships currently take nothing.
- **"一枪打爆" without inventing a balance number:** "kill in one shot" is a kill semantic. SDK kill-precedents:
  - Tanya C4 AlliedCommandoDetonationWeapon `Damage="999999.0" DamageType="GRENADE" DeathType="DETONATED"`;
  - midget-sub UNRESISTABLE suicide.
  - A second nugget for VEHICLE (and ships) with 999999 and a DamageType that vehicle/ship armors do not reduce would implement "one shot" without choosing a damage value.
- **Open design points the user has not decided** (they change gameplay, not just technique):
  - **(a) Which targets:**
    - Epic/hero vehicles (e.g. Shogun Executioner, campaign units) — "一辆" literally means any.
    - Iron-Curtain / chronoshifted targets: Pilot Snipe excludes UNDER_IRON_CURTAIN.
    - Amphibious units: ships only on water?
  - **(b) Death presentation:** the user says "打爆" (explode), e.g. DeathType EXPLODED vs NORMAL.
  - **(c) Interaction:** with Pilot Snipe, which becomes largely redundant (the user still kept its cooldown change).
  - **(d) Fire rate:** stays 1.5 s FiringDuration + delays (unchanged).
- **Classification:** mechanism is technically clear; target scope and death type are user-design items. Not implemented; not a "damage number" question.

## Remaining blockers — three categories
**A. Technical unknowns that are still researchable:**
- the TheAudioSettings / UIConfigList override behaviour (only provable natively);
- Bunker repair-halving parameter location;
- Hammer "减三分之一" exact field reading.

**B. User design undecided:**
- Guard02 / clone center / quick production center health; quick-production "immediate restore" (2 s aura insufficient).
- Apocalypse AA design (heading, harpoon mode, launch point).
- Paradrop button; oil derrick (not explicitly decided).
- Sentry gun conscript count (L708 待定).
- Natasha:
  - one-shot target scope / death type (above);
  - bombing range: "距离增加", no value;
  - SovietCommandoCallBombingRun 300.
- MCV machine gun and miner MG mounting (second batch / bone choice).

**C. Only native test pending (implemented):**
- Batches 59-71 timing items: bomber, vacuum, spy, proton, Natasha timing.
- Armor override, music default.
- Aircraft passenger survival (L179, "需实测").
- Instant capture, crush-no-stop.
- UI mouse once built.
