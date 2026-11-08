# NEXT R92: 苏联间谍 (new unit). Base: batch89. Read-only spec
## devdoc conventions (verbatim facts, not defaults)
- L905 "新增间谍，和盟军一样". L908 "复用盟军间谍逻辑".
- L909: copy Allied/Units/AlliedInfiltrationInfantry.xml, keep the skills SpecialPower_Bribe / SpecialPower_InfantryDisguise and the infiltration effects, **change it to the Soviet side and add it to the Soviet barracks CommandSet; reuse the Allied spy's model and voices.**
- BuildTime 8s, **prerequisite RequiredObject SovietWarFactory** (the copied Upgrade_AlliedTech2 must be replaced, L902), cost 1000.
- So: **produced at the Soviet barracks, with the war factory as the prerequisite.** "战车工厂" is the prerequisite, not the production building.
- **The original Allied spy is not edited** (Side stays Allies). In b89 it is already 1000 / 8s / RequiredObject AlliedWarFactory.
- Shared skill templates mean the existing bribe/steal/cooldown changes apply automatically.
- devdoc gives no new ID or strings. Inferred: id `SovietInfiltrationInfantry`, with Name/Desc/Type keys of the same name (same unresolved-string issue as other new units).

## New file Soviet/Units/SovietInfiltrationInfantry.xml
Full copy of b89 Allied/Units/AlliedInfiltrationInfantry.xml (31070 B). Change only:
- id, EditorName, DisplayName, Description, TypeDescription → SovietInfiltrationInfantry.
- Side Allies→Soviet.
- RequiredObject AlliedWarFactory→SovietWarFactory.
- L844 ThingToSpawn="AlliedInfiltrationInfantry" → SovietInfiltrationInfantry. This is the spawn/clone self-reference; check which module it is during the build, and otherwise copy unchanged.

Keep unchanged:
- BuildCost 1000, BuildTime 8.
- KindOf (DISGUISER INFILTRATOR …), armor AlliedInfiltrationInfantryArmor, weapons, the AlliedInfiltrationInfantryDisguiser weapon.
- Portrait/Button (Allied spy), UnitIntro, voices.
- CommandSet AlliedInfiltrationInfantryCommandSet: reuse, since it only holds abilities.
- All Draws, including xi:include ParachuteDrawAllied, plus ClientBehaviors, modules and includes.

## Other files
- LogicCommand (package): new `Command_ConstructSovietInfiltrationInfantry` (Type UNIT_BUILD, Object SovietInfiltrationInfantry), copied from SDK L409.
- LogicCommandSet (package): it has no SovietBarracksCommandSet. Add the full set from SDK L375–382 and append the new Cmd. Keep the clone-center related cmds if the package elsewhere relies on them; they are not in that set.
- Mod.xml: +1 include type="all" (139→140 XML; 141 if R-mirage is already in).

## Full functional equivalence (corrects the previous "optional" wording: these are required)
| Function | Allied-spy chain (static) | Required for the Soviet spy |
|---|---|---|
| **Cloning** | Spy L842–846 `ObjectCreationUpgrade id=ModuleTag_Clone ThingToSpawn=AlliedInfiltrationInfantry TriggeredBy Upgrade_CloneMe`. Soviet barracks (b89 L446–448) turns Upgrade_SovietCloning (cloning center) into Upgrade_CloneMe for produced units. **L844 is the cloning-center copy spawn.** | ThingToSpawn → **SovietInfiltrationInfantry**. If it isn't changed, the Soviet barracks would clone an Allied spy. Cloning center limit 1 stays. |
| **Rank/veterancy** | ExperienceLevels L833–862: 4 templates whose Target is the Allied spy, inheritFrom ExperienceLevel_AlliedRank1–4, RequiredExperience 1/3000/6000/9000, Award 1000/2000/3000/4000. Static.xml L30 (Static stream). | New package file GlobalData/ExperienceLevels_SovietSpy.xml with 4 new templates `SovietInfiltrationInfantryExperienceLevel_1..4`: inheritFrom ExperienceLevel_SovietRank1–4 (Soviet rank chevrons, as for other Soviet units), same Required/Award/Prerequisite chain, Target SovietInfiltrationInfantry. Mod.xml +1 all. The Allied templates are not touched. Production veterancy (barracks GiveUpgradeToProduced Upgrade_CreationVeterancy_*) carries over through the copied unit modules. **Unproven:** an ExperienceLevelTemplate outside the Static stream has no package precedent. Compile and runtime must confirm. |
| **IFV / multigunner golden gun** | Includes/InfantryFighting/IF_SecondaryObjectListener.xml L16–22: tuple IncludeThing AlliedInfiltrationInfantry → UpgradeSelf Uprade_IFV_GoldenGun. Pulled in by xi:include from package AlliedAntiAirVehicleTech1 L726 and AlliedBaseDefense L573. Weapon slots (AAAVT1_PistolWeapon / ABD_SpyPistolWeapon) and IF_SubObjectsUpgrade are keyed by upgrade, not ID. | New package copy of IF_SecondaryObjectListener.xml (SDK verbatim) + `<IncludeThing>SovietInfiltrationInfantry</IncludeThing>` in the Allied-spy tuple (Rule NONE allows several). Matters when a Soviet player owns an IFV/multigunner, e.g. by bribe. Both including files are already in the package and get rebuilt. Override precedence of a package Includes/ file vs SDK: unproven, check at compile. |
| **Bribe immunity** | SpecialPower_Bribe filter ExcludeThing AlliedInfiltrationInfantry (package SPT L813) | Add ExcludeThing SovietInfiltrationInfantry |
| **Hotkey select-spies** | UIInGame/UIComponentObjectSelector L61–64 ShortcutObjects | Parity: add IncludeThing in a package copy. Low risk, UI only. Include if full parity is wanted. |
| Building infiltration / steal / disguise / bribe skills | Keyed by KindOf INFILTRATOR/DISGUISER and the INFANTRY filter, plus shared templates | Automatic |
| Parachute draw, Allied-faction MC upgrades | Copied modules | Unchanged |
| InfiltrationCanEnterObjectFilter | Defined, no consumer | Ignore |

**No implicit override of the Allied spy:**
- The new id is unique. The Allied file, its ExperienceLevels, armor and weapons are not edited.
- Shared assets (armor, disguiser weapon, CommandSet, templates) are referenced, not redefined.
- The only shared files edited are additive (an extra ExcludeThing / IncludeThing).

## Unproven
- Runtime: whether disguise works for Soviet-side ownership, bribe use, voices.
- AI won't build it (no AI state). Not required.
