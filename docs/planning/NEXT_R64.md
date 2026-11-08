# Next (R64): Century Bomber "投弹速度加倍" — decided (phase 一), not implemented
Refs: `century_sdk_refs.tar.gz` (SDK Weapon.xml, AlliedBomberAircraft.xml, CampaignOverrides.xml, AssetTypeWeaponTemplate.xsd).

## Requirement — correct rows
- **5.4 #29, L622 (user):** "世纪轰炸机投弹速度加倍". Difficulty 容易, phase 一 (L623-624).
- **L626 (plan):** `AlliedBomberAircraftBombWeapon ClipSize 6，FiringDuration .25s → .125s`.
- These are the only rows for this request; no later revision.
- **Not to confuse with:**
  - L242-247 (Proton Collider shots ×2, a different item);
  - L604 (Vindicator clip 3/4, done);
  - L890-891 (Badger plan "像世纪轰炸机一样投弹", which copies this bomber; not implemented, see Dependencies).

## Package state b98
- **Weapon.xml `AlliedBomberAircraftBombWeapon`** (L1648-1676), same as SDK:
  - ClipSize 6; `FORCE_EMPTY_ENTIRE_CLIP`; AutoReloadsClip RETURN_TO_BASE; CanFireWhileMoving; AcceptableAimDelta 180d; ScaleAttackRangeByAmmoRemaining;
  - **FiringDuration Min/Max .25s (L1661-1662)**; ClipReloadTime 15s;
  - projectile AlliedBomberAircraftBombProjectile (+_Vet HEROIC).
- **Child `AlliedBomberAircraftBombWeapon_AirPower`** (L1680-1689): ClipSize 9, ClipReloadTime 10s, FinishAttackOnceStarted, +SYNC_AMMO_ON_ACTIVATE. **No FiringDuration of its own**, so it inherits.
- **Users:** only package `Allied/Units/AlliedBomberAircraft.xml` hardpoint (L221 normal, L225 AirPower with WEAPON_UPGRADED_01).
- **Campaign:** SDK CampaignOverrides L1035-1040 redefines the same id, inheriting and overriding only ClipReloadTime 10s. The new FiringDuration flows through. Map overrides are not in this package.

## Why FiringDuration, both Min and Max
- A clip of 6 bombs is dropped one per FiringDuration while the bomber passes (FORCE_EMPTY_ENTIRE_CLIP). Halving .25 → .125 doubles the drop rate. Clip size, damage and reload stay unchanged.
- Min and Max are both .25 in the original (fixed value). Setting both to .125 keeps it fixed; changing only one would make it random.
- Schema: FiringDuration is a RangeDuration (AssetTypeWeaponTemplate.xsd L840).

## Minimal Batch 64
- Package Weapon.xml text edit: L1661 `MinSeconds=".25s"` → `".125s"`, L1662 `MaxSeconds=".25s"` → `".125s"`.
- Expected diff vs 63: exactly 2 lines. No other file; 112 XML.

## Dependencies / native test
- **AirPower inherits**, so its 9 bombs also drop at .125. That is the same bomber's upgrade, so it is in scope.
- **Future buildable Badger (L891):** if it later copies this weapon, it inherits the new rate. Record for that batch.
- **Test:**
  - bomb spacing becomes tighter (pattern shorter: 6×.125 = 0.75 s vs 1.5 s);
  - projectile queueing / drop sound overlap (FireSound SOV_Kirov_BombDrop per shot);
  - range scaling with ammo; AI bombing runs;
  - whether the engine has a minimum per-shot interval.
