# Next (R71): default music 0% (L272) and default classic mouse (L278) — research
Refs: `r71_sdk_refs.tar.gz` (9588 B, sha256 23b5e0da…2a89fbf086):
- AudioSettings, MasterAudioEvents, global.xml, Static.xml, static_platformspecific.xml;
- UIConfigs, UIComponentOptionsSettingsGeneral (.xml + .xsd), AssetTypeUIConfigList.xsd;
- Documentation Mod_XML / UI_Modification; samplemod Mod.xml.

No PC / player profile touched. No promise that the user's current profile changes: Options.ini (MusicVolume, mouse setting) overrides defaults. Only new or reset profiles would see them.

## User requirements (phase 一)
- **L272:** "红警3默认的背景音乐特别吵特别烦人，能不能默认全关上，像ra2那样".
  - Plan: DefaultMusicVolume 50% → 0%.
  - Movie volume is not touched.
- **L278:** "把ra3里面选中单位后命令其移动或攻击的按键从反人类的鼠标右键改回唯一的鼠标左键".
  - Plan: DefaultAlternateMouse false → true.
  - The semantics come from the doc's external sources [S20-S22]: Alternate Mouse = classic C&C left-click.
  - **The SDK has no string/UI text confirming that false/true mapping** (none found in the SDK string tables/UIScreens). → native check of the Options screen required.

## A. Music — global stream
- **Load chain:** global.xml L19 `DATA:Sounds/MasterAudioEvents.xml` → its L19 `DATA:Sounds/AudioSettings.xml`. Asset `AudioSettings:TheAudioSettings` (in Builtmods/global.manifest).
- **Field:** AudioSettings.xml L48 `DefaultMusicVolume="50%"`. Its Includes (L4-8) need the PlatformSpecificAudioDefines instance include (`$PLATFORM_SPECIFIC_*` defines).
- **Precedent:**
  - samplemod Mod.xml L46 overrides `SoundEffects.xml`, which is also in MasterAudioEvents, the global stream, through a plain `type="all"` include. So overriding global-stream audio files from a mod is SDK-precedented.
  - **No precedent for the singleton TheAudioSettings**, and global.xml says it is loaded first at startup for subsystem setup. Whether a mod copy is picked up before the audio subsystem reads the default is unproven.
- **Minimal (if implemented):**
  - new `data/Sounds/AudioSettings.xml` = full SDK copy, only L48 → `0%`, with the original instance include kept;
  - Mod +1;
  - → 116 XML / Mod 115 all.
- **Native test:**
  - a fresh profile shows the music slider at 0;
  - no build error for a duplicate singleton.

## B. Mouse — static stream (UI component, not a standalone asset)
- **Load chain:** Static.xml L18 → static_platformspecific.xml L28 → `GlobalData/UIConfigs.xml` (165 lines, UIConfigList id `DynamicUIConfigList`).
  - That file **xi:includes** `UI/Mouse/Components/UIComponentOptionsSettingsGeneral.xml` twice: L106 MouseTactical (INGAME), L142 MouseShell (SHELL).
- **The component file is not an AssetDeclaration** (root `<UIComponentOptionsSettingsGeneral>`, 8 required elements per its xsd). It cannot be included in Mod.xml on its own; a lone include would do nothing or error.
- **Minimal technical route:**
  1. Full SDK copy of `data/GlobalData/UIConfigs.xml`: same id, 8 ART includes, 107 xi:includes unchanged.
  2. Plus `data/UI/Mouse/Components/UIComponentOptionsSettingsGeneral.xml`: full copy with only L15 → `true`.
  3. Mod +1 (UIConfigs only).
  - **Why this works:** the package's DATA: xi:includes resolve to package files first (the established package pattern, e.g. Includes/GenericEngineerContain). The other 106 includes would fall back to SDK data.
  - **Alternative without the second file:** inline the element in the UIConfigs copy. Rejected: it changes more text.
- **Precedent:**
  - same-id override of a static-stream asset (Weapon.xml / Armor.xml pattern; samplemod Weapon.xml);
  - **no SDK precedent for overriding UIConfigList.** UI_Modification.htm says UI changes beyond textures are "not possible" with the SDK tools; that refers to Apt screens, but treat as a risk.
- **Expected:** +2 files (116→117 XML), Mod 115 all.
- **Native test:**
  - the build succeeds;
  - a fresh profile's Settings→General shows the alternate/classic mouse on;
  - left-click move/attack works.

## Recommendation
- Split. **B (mouse) first:** static stream, same mechanism as existing overrides.
- **A (music):** a separate small batch, flagged "global singleton override unproven".
- Neither can be guaranteed from XML; both only affect new/reset profiles.
