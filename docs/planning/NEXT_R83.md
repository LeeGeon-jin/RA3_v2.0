# NEXT R83 — 第一批 gaps: crush, instant capture, lowest quality (read-only SDK research)
Scope source: the parent-verified user scope "开工第一阶段" = 第一批, explicitly including 工程师即时占领 / 碾压不停顿 / 最低画质. NEXT_R82 (mirage) is parked as 第二批.

## A. Crush without stopping — RECOMMENDED next source batch (doc L206-212, batch 一)
**User wording (L206):** "红警3每次大车碾压小车的时候总是会先停在小车面前再开始碾压，能不能不停下来直接压过去？"
**Plan (L209):** all vehicles CrushDecelerationPercent → 0%; BaseVehicle SquishCollide CrushKillDelay 1.5s → 0s ("被压载具一压上就死"); AI hints not changed; crush levels not changed.

### Schema
- **`CrusherInfo`:** a GameObject element, not a module (AssetTypeGameObject.xsd L421, maxOccurs 1; type L669-686).
  - `CrushDecelerationPercent` is a Percentage, xsd default **0** (L682).
  - `CrusherLevel` / `CrushableLevel` are xs:byte and are **not touched**.
  - `CrushWhileStationary` default false (L685) — not requested, not added.
- **`SquishCollide`:** a Behavior (AssetTypeGameObject.xsd L167; Modules/SquishCollide.xsd L4-14).
  - `CrushKillDelay` is a Time, xsd default **.5s** (L9).
  - `CrushAnimTime` default 1s is not touched (not requested).

### SDK locations (complete SDK grep: CrushDecelerationPercent in 20 files)
- **Base:** `BaseObjects/BaseVehicle.xml` (191 lines)
  - L39-41 `<SquishCollide id="DefaultSquishCollide" CrushKillDelay="1.5s"/>` → `0s`. This is the only CrushKillDelay in the whole SDK.
  - L182-187 `<CrusherInfo id="id_CrusherInfo" CrusherLevel="10" CrushableLevel="20" CrushDecelerationPercent="80%">` (+ ExtraCrushLevels SHRINK_EFFECT) → `0%`.
- **18 explicit overrides** (L210 list; matches the SDK grep exactly):

| file | SDK value | in package? (b122 line) |
|---|---|---|
| Allied/Units/AlliedAntiNavyShipTech1 | 50% | yes L505 |
| Allied/Units/AlliedAntiStructureVehicle | 80% | yes L627 |
| Allied/Units/AlliedAntiVehicleVehicleTech1 | 80% | yes L477 |
| Allied/Units/AlliedAntiVehicleVehicleTech3 | 80% | yes L695 |
| Allied/Units/AlliedMCV | 80% | yes L667 |
| Allied/Units/AlliedMiner | 80% | yes L493 |
| Japan/Units/JapanMCV | 80% | yes L507 |
| Japan/Units/JapanMiner | 80% | yes L862 |
| Japan/Units_SinglePlayerCampaign/JapanEmperorMecha | 80% | yes L506 |
| Soviet/Units/SovietAntiStructureVehicle | 80% | yes L397 |
| Soviet/Units/SovietAntiVehicleVehicleTech3 | 80% (levels 30/31 kept) | yes L789 |
| Soviet/Units/SovietMCV | 80% | yes L593 |
| Soviet/Units/SovietMiner | 80% | yes L570 |
| Soviet/Units/SovietSurveyor | 80% | yes L339 |
| BaseObjects/BaseEgg | 80% (L52) | **no** — Japan eggs in package (JapanMechaKingCore, JapanWaveForceTripleCannonEgg) inherit it |
| Japan/Units/JapanAntiVehicleVehicleTech1 | 80% (L563) | **no** |
| Soviet/Units/SovietAntiVehicleVehicleTech1 | 80% (L1541) | **no** |
| Soviet/Units/SovietAntiVehicleVehicleTech2 | 80% (L425) | **no** |

- **Precedent:** JapanMechaKing L1155 `CrushDecelerationPercent="0%"` (already 0, unchanged).
- **Inheritance:** other vehicles' CrusherInfo blocks that omit the attribute (e.g. AlliedAntiInfantryVehicle id_CrusherInfo) get 0 either way — inherited from the new 0% base, or the xsd default 0. So base + the 18 explicit files cover every vehicle.
- **Campaign:** no CrusherInfo / SquishCollide in Includes/CampaignOverrides (0 hits). Doc L209 says the same about the 27 maps' overrides.
- **Victim side:** only BaseVehicle defines a vehicle SquishCollide. Civilian / wall / infantry SquishCollides are separate and **not changed** (the request is about vehicles crushing vehicles).
- **Alternative not chosen:** the MechaKing self-aura NO_SQUISHCOLLIDE_DELAY (JapanMechaKing L1052-1058, AttributeModifier L1163-1167) only applies to the crusher it's on. The global CrushKillDelay 0s matches the plan text.

### Minimal source candidate (one batch)
- 14 package files: change one attribute value each, nothing else.
- 5 new full SDK copies with only the listed values changed:
  - BaseVehicle (2 values);
  - BaseEgg, JapanAntiVehicleVehicleTech1, SovietAntiVehicleVehicleTech1, SovietAntiVehicleVehicleTech2 (1 value each).
  - Follow the existing package convention for full copies (ART includes stripped); Mod.xml gets +5 `type="all"` includes.
- **Base-object override precedent in the package:** BaseObjects/BaseMiner.xml and BaseOreNode.xml are already Mod-included (Mod.xml L62-63), and BaseMiner includes `DATA:BaseObjects/BaseVehicle.xml`.
- **Expected result:** 135 XML files, 133 "all" includes in Mod.xml.
- **Not touched:** CrusherLevel / CrushableLevel / CrushWeapon / CrushEqualLevelProps / ExtraCrushLevels, SkirmishAIInformation crush hints, infantry.
- **SovietAntiVehicleVehicleTech2** (Tesla tank) is a 第二批 unlock item; copying it for the 第一批 crush value only does **not** unlock it. Its BuildCost / Buildable / prereqs stay at SDK values.
- **Runtime only:**
  - whether the visible slowdown disappears (the doc admits a pathfinding pause may be engine-side);
  - the wreck / physics look at 0s;
  - whether duplicating base objects builds cleanly (same risk as the existing BaseMiner copy).

## B. Instant engineer capture — global-stream candidate, route unproven (doc L185-186)
- **Field:** SDK `System/UnitAISettings.xml` L12 `CaptureWaitTime="3s"` (singleton `UnitAISettings id="Settings_UnitAI"`).
- **Schema:** `Schemas/xsd/System/UnitAISettings.xsd` L60, type Time, default 2s.
- The doc itself says "推测这就是占领等待时间（按名称推断，待实测）".
- **Load path:** `XMLFiles/global.xml` L50 `<Include type="all" source="System/UnitAISettings.xml"/>`. That is the **global** stream (Mod_XML.htm: static / global / audio are the three streams; mods reference global.xml).
- **Precedent:** none in the SDK / samplemod for overriding a global singleton.
  - doc L78 cites community FAQ #36 / #57 / #58: global data like MpGameRules / W3DDeviceSettings / CameraSettings "必须放在 AdditionalMaps/MapMetaData_*.xml 中编译，放进 mod.xml 不生效".
  - The package's B71 AudioSettings and B72 UI options default already use the Mod.xml route; their effect is likewise unproven.
- **Classification:** a single-file candidate is possible (full copy of UnitAISettings.xml, L12 3s→0s, +1 Mod include). It must be labeled **"route unproven, may not take effect"**, and the MapMetaData route is not provable from the SDK. Do after A. It is not a user re-authorization issue.

## C. Default lowest quality — NONXML-dominant, not pushed as next
- **Data:** SDK `System/GameLOD.xml` (289 lines; GameLODPreset Low / Medium / High / UltraHigh L17-59; StaticGameLOD VeryLow… from L67) is loaded via **global.xml L27**.
- `System/GraphicsHardware.xml` (Device VendorId / DeviceId → Level table) is referenced only from GameLOD.xml.
- **Mechanism** (doc L197 / L1570): the player profile Options.ini stores StaticGameLOD / IdealStaticGameLOD. Mod data can only change the first-run auto-detect result (the hardware table Level / thresholds). So it affects **new profiles / first detection only**; existing profiles keep their setting.
- It is also a global-stream file (same unproven route as B), plus a first-run-detection dependency.
- **Classification:** source-possible but doubly unproven. Not recommended as the next batch; keep as a 第一批 open item.

## Refs
`r83_sdk_refs.tar.gz`:
- the SDK originals of all 20 crush files + JapanMechaKing;
- (the MechaKing AttributeModifier is inside JapanMechaKing.xml);
- AssetTypeGameObject.xsd, Modules/SquishCollide.xsd;
- System/UnitAISettings.xml + xsd, System/GameLOD.xml, GraphicsHardware.xml;
- global.xml, Documentation/Mod_XML.htm.
