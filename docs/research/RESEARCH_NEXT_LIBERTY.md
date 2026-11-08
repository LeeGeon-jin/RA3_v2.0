# Research: Allied Statue of Liberty (read-only, not implemented)
Doc location: **L694/L697/L698 (section 5.4)**, not L809/L812 (those are Soviet Kremlin/heroes statue; they only cross-reference 5.4).

## Settled by doc (L697 quote)
"本人已确认用大号 NY_Liberty" ; "造价 2000（BuildCost）；建造时间 20 秒（盟军自由女神像 BuildTime="20"，由建造厂直接建造…）；无前提（不写 GameDependency）；耗电 0（EnergyProduction="0"）；纯装饰…新对象须去掉 NOT_AUTOACQUIRABLE 并加 AUTO_ACQUIRABLE_BY_AI，保留 ActiveBody…血量…沿用原版（自由女神像…=$CIV_HEALTH_MEDIUM 3000）" ; "做法：新 id、Side Allies、盟军建造厂按钮、补建造效果". Limit 1 (decision 6).
Armor "建议用本阵营普通建筑护甲（待定）" → keep inherited StructureArmor (no change = no invention), same as Kremlin.

## Source (SDK `Civilian/New_York_NY/Buildings/NY_Liberty.xml`, 206 lines)
- Already inherits **BaseCivilianStructureNoGarrisonDestructible**; no garrison module exists → nothing to remove (L812-style garrison rule satisfied). Allied side: no Japan death-removal rule → **keep all death modules** (BuildingDestruction, FXList Replace, CreateObjectDie→NY_Liberty_Die_OCL, DestroyDie).
- Keep verbatim: ART includes `NY_Liberty.W3X`, `NY_LibertyBase.W3X`; instance include `NY_Liberty_Collapse.xml`; Draw (ExtraPublicBone 01–20, Model NY_Liberty); Physics; GenericEngineerContain/GenericBuildingRepair xi:includes (keep xmlns:xi); AIUpdate AutoAcquireEnemiesWhenIdle NO; 7 BOX shapes + offsets; AudioArraySound; OCL NY_Liberty_Die_OCL.
- Real UI kept: Description `Desc:LibertyStatue`, TypeDescription `Type:LibertyStatue`, SelectPortrait `Portrait_Special_StatueOfLiberty`, ButtonImage `Button_Special_StatueOfLiberty`, DisplayName Replace `Name:LibertyStatue`, HealthBoxHeightOffset -400. (Existence of the strings/images in the game assets is unverified → test.)

## Required changes (minimal)
1. id/EditorName new, e.g. `AlliedStatueOfLibertyBuildable`; Side `Allies`.
2. KindOf `+AUTO_ACQUIRABLE_BY_AI` → `-NOT_AUTOACQUIRABLE +AUTO_ACQUIRABLE_BY_AI` (Kremlin precedent).
3. Add BuildTime 20, EnergyProduction 0, MaxSimultaneousOfType 1, ProductionQueueType + BuildPlacementTypeFlag `OTHER_STRUCTURE`, `<ObjectResourceInfo><BuildCost Account="=$ACCOUNT_ORE" Amount="2000"/>`; include GlobalDefines; no GameDependency.
4. **Body id finding:** source uses `ActiveBody id="ModuleTag_Body"` while the parent chain defines `ActiveBody id="DefaultBody"` → original object effectively carries two Body entries (Body is single-slot). Fix technically: `ActiveBody id="DefaultBody" MaxHealth="=$CIV_HEALTH_MEDIUM"` (same value, Kremlin/Fuji precedent). Evidence: BaseCivilianStructureNoGarrisonDestructible L27-28, BaseObject L39.
5. Placement order: DisplayName → ObjectResourceInfo → (ArmorSet inherited) → Draws → Behaviors → AI → Body → Geometry.
6. No StructureUnpackUpdate (Allied direct build, L221 says Allied unpack is animation only).
7. Collapse file + its `ART:NY_Liberty_COL.w3x` resolved via the SDK DATA instance include (as Kremlin) → native build log.
8. Do not include `New_York.xml` (would load all NY objects); original NY_Liberty/S09 map untouched.

## Production chain
- `Command_ConstructAlliedStatueOfLiberty` Type `CONSTRUCTION_YARD_CONSTRUCT`, `<Object>`new id`</Object>`.
- Current real counts (b78): `AlliedConstructionYardCommandSetBase` **15→16**, `AlliedCraneCommandSet` **14→15** (both end in Command_ConstructAlliedRushmoreLaserHead; append after it). Mod +1 → 93 all + 3 ref.

## Risks/tests
Footprint ~270×278, height ~354 (top shape z 288 + 66) → placement; 7 boxes + collapse debris perf; AlliedBarracks_Debris (Allied/Props) & FX_StatueOfLiberty_BoneContactPointExplosion (GlobalData/FXListCivilian.xml L251) are global → confirm in build log; counts for defeat (no IGNORE_FOR_VICTORY in source either); UI strings test.

## SDK attachments (XMLFiles/)
Civilian/New_York_NY/Buildings/NY_Liberty.xml; Civilian/New_York_NY/Props/NY_Liberty_Collapse.xml; BaseObjects/BaseCivilianStructureNoGarrisonDestructible.xml; BaseObjects/BaseCivilianStructureNoGarrison.xml; BaseObjects/BaseObject.xml; Includes/GenericEngineerContain.xml; Includes/GenericBuildingRepair.xml; GlobalData/GlobalDefines.xml; GlobalData/FXListCivilian.xml (ref only); Allied/Props/AlliedBarracks_Debris.xml (ref only); package Soviet/Structures/SovietGreatKremlinPalace.xml (template). ART: NY_Liberty.W3X, NY_LibertyBase.W3X, NY_Liberty_COL.w3x.
Guard02 still undecided — not implemented.
