# NEXT R83 — Engineer instant capture (第一批, doc L185-186) — source candidate, loading route unproven

## Requirement
- **Doc L185:** 工程师即时占领.
- **Plan L186:** "G: System/UnitAISettings.xml：CaptureWaitTime="3s" → 0s。推测这就是占领等待时间（按名称推断，待实测）".
- **ch.7 L1595:** "工程师 CaptureWaitTime 改 0 后是否已完全无延迟".

## Field evidence
- **SDK `XMLFiles/System/UnitAISettings.xml`** (29 lines): one asset `<UnitAISettings id="Settings_UnitAI" …>`.
  - L12: `CaptureWaitTime="3s"`.
  - Other attributes: CompleteTargetingCompareList, MinLowEnergyProductionSpeed 0.3, MaxLowEnergyProductionSpeed 0.5, SelectionFlashSaturationFactor 0.5, GarrisonedRangeMultiplier 1.0, HumanIgnoreDuplicateMoveCommandDistance 2.0, ParachuteDriftSpeed 4.0.
  - Children: VictoryConditionUnitObjectFilter (3 MCVs) and VictoryConditionStructureObjectFilter.
- **Schema `Schemas/xsd/System/UnitAISettings.xsd`:**
  - L58-59 comment "time an engineer will wait outside a structure before capturing";
  - L60 `CaptureWaitTime` type Time, default 2s;
  - L56-57 `CaptureWaitDistance` default 20 (not changed);
  - L61-62 CaptureWaitModelConditions.
  - The xsd comment confirms the semantics, so this is no longer only "by name".
- **Registration:** `Schemas/xsd/CnC3Types.xsd` L627 includes the xsd; L1019 `<xs:element name="UnitAISettings">`.
- **Reference dependency:** `CompleteTargetingCompareList` is defined in `XMLFiles/GlobalData/UnitAITargetChooser.xml` L13 (global.xml L45). It resolves through Mod.xml's existing `reference DATA:global.xml`.

## Load chain and its limits
- **SDK:** `XMLFiles/global.xml` L50 `<Include type="all" source="System/UnitAISettings.xml"/>`, i.e. the **global** stream.
  - SDK Mod_XML.htm: mods reference static / global / audio.xml and build their own includes after them.
- **Package pattern already used:**
  - B71 `Sounds/AudioSettings.xml` (global stream via MasterAudioEvents) as a full copy + Mod `type="all"` include;
  - B72 UI options component.
  - Both are unverified in game.
- **Alternative route:** doc L78 cites community FAQ #36 / #57 / #58, "全局数据须放 AdditionalMaps/MapMetaData_*.xml 编译，放进 mod.xml 不生效" (examples given there: MpGameRules / W3DDeviceSettings / CameraSettings). The SDK has **no** sample or schema evidence of that route, and `XMLFiles/MapMetaData.xml` is only the map cache (TheMapCache). Not provable here, so not proposed.
- **Explicitly not done:** do not copy global.xml or any map metadata into the mod.

## Minimal source candidate
1. New `data/System/UnitAISettings.xml`: a byte copy of the SDK file. The only change is L12 `CaptureWaitTime="3s"` → `"0s"`. Keep every other attribute, both filters, the namespace and the BOM / encoding as in the SDK. The file has no ART includes.
2. `Mod.xml`: +1 line `<Include type="all" source="DATA:System/UnitAISettings.xml" />`, placed after the reference includes like the AudioSettings line.
- **Expected:** 136 XML files, 134 "all" includes; no other file changes.

## Status
- Source candidate. Whether the singleton override is used, whether the builder accepts a duplicate `Settings_UnitAI`, and whether 0s removes the whole delay are all **native test only**, same pattern as 71 / 72.
- Not claimed effective.
- Default lowest quality: unresolved, not part of this batch.

## Refs
`r83_engineer_sdk_refs.tar.gz`:
- `XMLFiles/System/UnitAISettings.xml`;
- `Schemas/xsd/System/UnitAISettings.xsd`;
- `Schemas/xsd/CnC3Types.xsd`;
- `XMLFiles/global.xml`;
- `XMLFiles/GlobalData/UnitAITargetChooser.xml`;
- `Documentation/Mod_XML.htm`;
- `Mods/samplemod/data/Mod.xml`.
