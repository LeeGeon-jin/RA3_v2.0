import os,shutil,hashlib,sys,glob
SDK='/workspace/ra3-sdk-tools/sdk'; PKG='/workspace/b99f/data'; X='/workspace/ra3xfer'
OUT='/tmp/p2refs/phase2_final'; shutil.rmtree('/tmp/p2refs',ignore_errors=True)
sdk_xml='''BaseObjects/BaseMountRushmoreHead.xml BaseObjects/BaseCollapsingObject.xml BaseObjects/BaseEgg.xml BaseObjects/BaseTechStructure.xml BaseObjects/BaseVehicle.xml
Civilian/Mount_Rushmore_MR/Buildings/MR_LaserMtRushmore_Lincoln_Ready.xml Civilian/Odessa_OD/Buildings/OD_Castle01.xml Civilian/Floating_Island_FI/Buildings/FI_FloatingFortressMainGun.xml Civilian/Yucatan_YU/Props/YU_HotelDebris.xml
Japan/Eggs/JapanBaseDefenseAdvancedEgg.xml Japan/Structures/JapanBaseDefenseAdvanced.xml Japan/Structures/JapanTechStructure.xml Japan/Structures/JapanConstructionYard.xml Japan/Units/JapanAntiInfantryInfantry.xml Japan/Units/JapanAntiVehicleInfantry.xml
Includes/GenericUnpackPower.xml Includes/JapanEnhancedKamikazeUpgradeDeathWeapon.xml Includes/JapanEnhancedKamikazeUpgradeStatus.xml Includes/GenericBuildingRepair.xml Includes/GenericEngineerContain.xml Includes/TechBuildingFlagDraw.xml Includes/AlliedAirPowerUpgrade.xml
Includes/SovietTerrorDroneSpawnUpgradePlayerPower.xml Includes/ParachuteDraw.xml Includes/ParachuteDrawAllied.xml Includes/ParachuteDrawSoviet.xml Includes/ParachuteDrawJapan.xml
Includes/CampaignOverrides/CampaignOverrides.xml Includes/CampaignOverrides/PlayerTechs_CAMP.xml
Neutral/Structures/AirportTechStructure.xml Neutral/Props/AirportTechStructure_Collapse.xml
Allied/AlliedMapSpecific.xml Allied/Units_Campaign/CAMP_PowerStore_AlliedBomberDrop.xml Allied/Units_Campaign/CAMP_AlliedBomberAircraft_Infantry_1.xml Allied/Units_Campaign/CAMP_AlliedBomberAircraft_Infantry_2.xml
Allied/Units/AlliedAntiInfantryInfantry.xml Allied/Units/AlliedAntiVehicleInfantry.xml Allied/Units/AlliedSupportAircraft.xml Allied/Units/AlliedBomberAircraft.xml
Soviet/Units/SovietAntiInfantryInfantry.xml Soviet/Units/SovietAntiVehicleInfantry.xml Soviet/Units/SovietSupportBomber.xml Soviet/Units/SovietAntiGroundAircraft.xml Soviet/Units/SovietAntiAirShip.xml Soviet/Units/SovietMCV.xml Soviet/Units/SovietAntiVehicleVehicleTech1.xml
System/PlayerTechs.xml System/PlayerTemplates.xml
GlobalData/GlobalDefines.xml GlobalData/LogicCommand.xml GlobalData/LogicCommandSet.xml GlobalData/SpecialPowerTemplates.xml GlobalData/Weapon.xml GlobalData/ObjectCreationLists.xml
UI/ButtonStateDataCommon.xml UI/RadiusCursors.xml UI/Mouse/UnitAbilityButtonTemplates.xml WorldBuilder.xml'''.split()
for s in 'PowerPlant Barracks Refinery WarFactory NavalYard Airfield TechStructure SuperWeapon SuperWeaponAdvanced BaseDefenseAdvanced ConstructionYard'.split():
    sdk_xml += [f'Allied/Structures/Allied{s}.xml', f'Soviet/Structures/Soviet{s}.xml']
sdk_xml += ['Allied/Structures/AlliedBaseDefense.xml','Allied/Structures/AlliedOutPost.xml','Allied/Structures/AlliedCrane.xml','Soviet/Structures/SovietBaseDefenseGround.xml','Soviet/Structures/SovietBaseDefenseAir.xml']
xsd='''AssetTypeGameObject.xsd AssetTypeSpecialPowerTemplate.xsd AssetTypeWeaponTemplate.xsd AssetTypeObjectCreationList.xsd AssetTypeLogicCommand.xsd AssetTypeLogicCommandSet.xsd AssetTypeButtonState.xsd AssetTypeUnitAbilityButtonTemplate.xsd AssetTypePlayerTech.xsd AssetTypePlayerTemplate.xsd AssetTypeExperienceLevelTemplate.xsd
Modules/OCLSpecialPower.xsd Modules/TransportContain.xsd Modules/OpenContain.xsd Modules/EjectPassengersSpecialAbilityUpdate.xsd Modules/RunOffMapBehavior.xsd Modules/FireWeaponWhenDeadBehavior.xsd Modules/SlowDeath.xsd Modules/HelicopterSlowDeathBehavior.xsd Modules/PassiveAreaEffectBehavior.xsd Modules/StructureUnpackUpdate.xsd Modules/ReplaceSelfSpecialAbility.xsd Modules/JetAIUpdate.xsd Modules/HordeTransportContainDamage.xsd UnitAbilityButtons/TargetedSpecialPowerUnitAbilityButtonTemplateData.xsd UnitAbilityButtons/SpecialPowerUnitAbilityButtonTemplateData.xsd
Includes/DieMux.xsd Includes/ButtonState.xsd Includes/KindOf.xsd Includes/Death.xsd'''.split()
# pkg: everything the doc touches incl. all pkg structures for build range
pkg=['Mod.xml','GlobalData/LogicCommand.xml','GlobalData/LogicCommandSet.xml','GlobalData/SpecialPowerTemplates.xml','GlobalData/Weapon.xml','GlobalData/ExperienceLevels_Badger.xml',
 'Japan/Eggs/JapanWaveForceTripleCannonEgg.xml','Civilian/Mount_Rushmore_MR/Buildings/MR_LaserMtRushmore_Lincoln_Ready.xml','Civilian/Floating_Island_FI/Buildings/FI_FloatingFortressMainGun.xml',
 'Neutral/Structures/AirportTechStructureBuildable.xml','Soviet/Units/SovietSupportBomber_Buildable.xml','Allied/Units/AlliedSupportAircraft.xml']
for d in ['Allied/Structures','Soviet/Structures','Japan/Structures']:
    pkg += sorted(os.path.relpath(f,PKG) for f in glob.glob(f'{PKG}/{d}/*.xml'))
for f in ['UI/ButtonStateDataCommon.xml','UI/Mouse/UnitAbilityButtonTemplates.xml','System/PlayerTechs.xml']:
    if os.path.exists(f'{PKG}/{f}'): pkg.append(f)
rows=[];miss=[]
def add(src,dst,origin):
    if not os.path.isfile(src) or os.path.getsize(src)==0: miss.append(src); return
    os.makedirs(os.path.dirname(dst),exist_ok=True); shutil.copy2(src,dst)
    rows.append((os.path.relpath(dst,'/tmp/p2refs'),os.path.getsize(dst),hashlib.sha256(open(dst,'rb').read()).hexdigest(),origin))
for f in dict.fromkeys(sdk_xml): add(f'{SDK}/XMLFiles/{f}',f'{OUT}/sdk/XMLFiles/{f}',f'SDK:XMLFiles/{f}')
for f in dict.fromkeys(xsd): add(f'{SDK}/Schemas/xsd/{f}',f'{OUT}/sdk/Schemas/xsd/{f}',f'SDK:Schemas/xsd/{f}')
for f in dict.fromkeys(pkg): add(f'{PKG}/{f}',f'{OUT}/b99fix/data/{f}',f'B99FIX:data/{f}')
for f in ['NEXT_PHASE2_FINAL.md','BATCH99FIX_AUDIT.md','BATCH99_AUDIT.md','BATCH98_AUDIT.md','BATCH97_AUDIT.md','BATCH96FIX_AUDIT.md','USER_DECISIONS_2026-11-09_0354_0355.md']: add(f'{X}/{f}',f'{OUT}/docs/{f}',f'DOC:{f}')
with open(f'{OUT}/MANIFEST.tsv','w') as m:
    m.write('member\tbytes\tsha256\torigin\n')
    for r in rows: m.write('\t'.join(map(str,r))+'\n')
print('files',len(rows),'missing',miss)
