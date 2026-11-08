# Phase 1 — default lowest quality: research (read-only)
No source edits, no PC, no compile. Phase 1 is not complete.

**Legend:** [F] = fact checked this round · [I] = inference.

## 1. Requirement and agreed scope
- **[F] User request (devdoc 5.1 #6, L194):** "把默认的游戏画质设为最低。这样会把花哨的特效去掉，才有ra2的感觉如果玩家想手动调高画质可以手动调高，但默认是最低".
- **[F] Batch:** L196 "一（mod 数据）；启动脚本为可选附带".
- **[F] Agreed design:**
  - The 11-06 revision note (L39) and L197 already settle it: **"只影响新档案；已有档案保留原设置"**.
  - The default is VeryLow, falling back to Low if the in-game look is too poor.
  - Medium / High / UltraHigh / Custom and DynamicGameLOD keep their original values ("不封顶").
  - The launcher / .bat script is only an **optional** extra.
- **[F] ch.7 L1570:** "需实测首次检测是否读取 mod 数据；已有档案不受影响".
- **Scope conclusion [F]:** the authorized target is the **default for new profiles**. Overwriting existing profiles was never required; the script that would do so is optional and must back up the file first.
- R49 classified this item as "NONXML", which was too coarse. Part (a)+(b) is mod data; only the profile write is NONXML.

## 2. Where quality lives
- **[F] Player profile** `%APPDATA%\Red Alert 3\Profiles\<profile>\Options.ini`, shared by the base game and every mod.
  - Public sample (Revora forum topic 118367, a real RA3 Options.ini) contains: `StaticGameLOD = UltraHigh`, `IdealStaticGameLOD = VeryLow`, plus per-item `EffectsLOD`, `ShadowLOD`, `DecalLOD`, `AnimationLOD`, `ModelLOD`, `TextureQualityLOD`, `ShaderLOD`, `TerrainLOD`, `WaterLOD`, `AntiAliasingLOD`.
  - Revora topic 116021: `IdealStaticGameLOD` is the auto-detected / recommended value, while `StaticGameLOD` is the preset the user actually plays. Editing Ideal alone does not change the active preset.
  - [I] So once a profile has `StaticGameLOD`, mod data cannot override the player's chosen preset.
- **[F] SDK `XMLFiles/System/GameLOD.xml`** (289 lines), loaded from **global.xml L27** (global stream).
  - L6 `<Include type="all" source="GraphicsHardware.xml"/>` (relative, same folder).
  - L17-59: four `GameLODPreset` (Low / Medium / High / UltraHigh), SystemMemory 500 / 500 / 500 / 1000, Xres / YRes 1024×768, and Processor MinMHz per CPU type.
  - There is no VeryLow preset. [I] A machine failing the Low threshold is classed VeryLow.
  - L67+: `StaticGameLOD` VeryLow / Low / Medium / High / UltraHigh / Custom value blocks; DynamicGameLOD after that.
- **[F] Schema `Schemas/xsd/System/GameLOD.xsd`:**
  - GameLODPreset: Level (GameLODType, default MEDIUM), SystemMemory SageInt default 500, Xres / YRes, Processor 1..n.
  - Device: VendorId, DeviceId, Name, Level (all required), MacLevel.
  - GameLODType enum: UNKNOWN / VERY_LOW / LOW / MEDIUM / HIGH / ULTRA_HIGH / CUSTOM.
- **[F] SDK `System/GraphicsHardware.xml`:** 340 `<Device>` entries. Device Level (excluding MacLevel): VERY_LOW 47, LOW 162, MEDIUM 63, HIGH 38, ULTRA_HIGH 30.
  - [I] For known GPUs this table likely sets the recommended level. How it combines with the CPU / RAM thresholds is not documented (doc L197 says the same).

## 3. Can mod data alone do it reliably?
**Not provable statically. Possible as a source candidate, with two unproven layers:**
1. **Global stream:**
   - GameLOD is global-stream data. Same pattern as B71 AudioSettings / B72 mouse / B83 UnitAISettings (Mod.xml `type="all"` override), all unverified in game.
   - Doc L78 / L1570 cite community FAQ #36 / #57 / #58: global data needs `AdditionalMaps/MapMetaData_*.xml`. The SDK has no sample or schema for that route; SDK MapMetaData.xml is only the map cache.
2. **Timing:**
   - [I] Auto-detection runs when a profile is first created, or when Options.ini is missing.
   - Whether that runs after the `-modconfig` mod data loads is unknown.
   - If detection happens before mod data loads, the mod change has **no effect** even for new profiles.

**Minimal source candidate, if pursued** (doc plan a+b, nothing else):
- `data/System/GameLOD.xml`: full SDK copy, changing only `SystemMemory` of the 4 presets to an unreachable value (e.g. 999999) → detection result VeryLow.
  - The fallback-to-Low variant changes only Medium / High / UltraHigh.
  - All StaticGameLOD / DynamicGameLOD values stay as in the SDK.
- `data/System/GraphicsHardware.xml`: full SDK copy, changing only every `Device Level` → `VERY_LOW`.
  - That is 293 value edits; MacLevel is untouched.
  - The relative include in GameLOD.xml L6 then resolves to this copy [I].
- **Mod.xml:** +1 `type="all"` include for GameLOD.xml only. GraphicsHardware comes in through GameLOD's own include, so including it again would duplicate the asset [I]. **Do not** copy global.xml.
- **Effect claims:** none beyond "source candidate".
- **Practical limit [F]:** it never affects the user's existing profile.

## 4. Profile route (only once the user's PC is available again; do NOT run now)
- **Authorized fields only:** the user asked for "默认最低" with manual raising allowed, so a one-time write of the active preset is the minimal change:
  1. **Back up:** copy `Options.ini` → `Options.ini.bak_RA3V2` in the same profile folder.
  2. **Set** `StaticGameLOD = VeryLow`. Optionally also `IdealStaticGameLOD = VeryLow`, so a "Reset to recommended" in the options lands low.
     - Do not touch the individual `*LOD` lines, Resolution or any other key.
     - [I] With a non-Custom preset the game applies that preset's values.
  3. **Only once:** the doc's optional script uses a marker file and does not run again. The player can then raise quality manually and it sticks.
  4. **Undo:** restore `Options.ini.bak_RA3V2`.
- **Caveat [F]:** the profile is shared with the base game, so it will also be low there.
- This needs the user's computer and explicit approval at that time.

## 5. Verdict
- **New-profile default:** a mod-data source candidate is possible now (2 files + 1 include). It is unproven on two levels (global stream, detection timing), so the honest label is "candidate, may not take effect".
- **User's existing profile:** only via Options.ini, which needs the PC.
- **Not done; not claimed done.**

## 6. 第一批 boundary (accurate as of B84)
### Source candidates in the package (natively untested)
- ore, miner;
- build times (base buildings, super reactor 24, airfield 15, Battle Lab 2000/30, tech 1000/15, academy 1500);
- MCV 3000/30, speed 60;
- permits / RequiredObject;
- KillPassengersOnDeath;
- Premature discharge removed (B60);
- coastal gun homing; Ukraine cannon homing (B84);
- AI cheat 100%;
- directional damage removed (B69);
- music 0% (B71); classic mouse (B72);
- turbine 300/10 (B28/29); Kirov 2000/20 (B16FIX);
- timing batches 59-73; Natasha (68 / 70 / 76 / 81);
- crush 0% / 0s (B82FIX2);
- engineer CaptureWaitTime 0s (B83).

### Still open in 第一批
- default lowest quality (this file).

### Everything above needs native compile + in-game test
- Especially the global-stream overrides (71 / 72 / 83, and GameLOD if done).
