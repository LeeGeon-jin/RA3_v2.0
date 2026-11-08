# BATCH73 AUDIT — FORMAT PASS / EFFECT UNPROVEN → experimental candidate only
No full XSD, compile or in-game test. Phase 1 not complete.
**Recommendation: keep Batch72 as the approved source baseline; keep Batch73 only as a test package.**

## Layer 1 — verified facts
- **Package:** 294179 B, sha256 c639a84d…3c00cd384 match. All entries under `data/`. 118 XML parse. Mod: 116 all.
- **vs 72:**
  - only GlobalData/Weapon.xml L6317-6318 change, `SovietAntiVehicleVehicleTech1CannonWeapon` ClipReloadTime Min 0.6s→0.333s, Max 1.0s→0.6s;
  - the other 117 files are byte-identical; Mod and commands unchanged.
- **Size:**
  - uncompressed Weapon.xml 268608 → 268610 B (+2: "0.6"→"0.333" +2, "1.0"→"0.6" ±0);
  - the tar.gz grew +4 B (294175→294179). That is a compression artefact, not equal to the text delta, so any claim tying the string-length change to the archive byte increase is wrong.
- **Inheritance:**
  - parent ScatterableWeapon (SDK Weapon.xml) contains only ScatterRadiusVsType (SHRINK_EFFECT), no timing elements;
  - child `Leech_SovietTankCannon` (L7093) has no timing → inherits the new reload;
  - the campaign Tutorial_SovietTech1Tank uses the same weapon;
  - FiringDuration 0.2/0.2, ClipSize 1, AutoReloadsClip AUTO unchanged;
  - no PreAttackDelay / CoolDownDelayBetweenShots (both optional, RangeDuration default 0s per AssetTypeWeaponTemplate.xsd L11-15 / L835-855).

## Layer 2 — NOT proven (the condition for implementing was not met)
- **Schema:** AssetTypeWeaponTemplate.xsd defines PreAttackDelay / FiringDuration / CoolDownDelayBetweenShots / ClipReloadTime only as optional RangeDuration elements. There is **no documentation of order or overlap**, and no Min/Max distribution. SDK Documentation/*.htm has no weapon timing page.
- **Public sources conflict:**
  - **GamerSky RA3 weapon tutorial** (https://www.gamersky.com/handbook/200906/142713.shtml): "ClipReloadTime：实际就是开火间隔比率…注意'数值必须大于等于上面的FiringDuration值'". This implies the reload time *is* the interval (overlapping FiringDuration), **not** FiringDuration + reload.
  - **BFME (SAGE INI) tutorials** (the3rdage.net item-75; Revora "Faramir attack speed") describe reload as the time to ready the next shot. They are a different game and data format, and give no proof of serial addition in RA3.
  - **ModDB "Research on the rate of fire of weapon" (RA3)** (https://www.moddb.com/mods/some-pack-patch/tutorials/research-on-the-rate-of-fire-of-weapon): WeaponTemplate fire rates are rounded **up to N/15 s**. This makes exact fractions such as ⅓ subject to frame rounding.
- **Consequence:**
  - **If serial** (0.2 + reload): 0.8–1.2 s → 0.533–0.8 s, i.e. ×2/3. In frames 12–18 → 8–12, exactly ⅔ if rounding holds.
  - **If reload = interval** (the GamerSky reading): 0.6–1.0 → 0.333–0.6, i.e. ×0.56–0.6 (≈ −40–44%), **not −⅓**.
  - Min/Max is presumably a per-shot random pick, distribution unknown.
- The cloud's "未见否定证据" is not evidence. My own NEXT_R73 assumed the serial addition — also only an inference, not accepted here because I proposed it.
- The same unproven serial assumption sits behind earlier interval items (Guardian 0.2+1.8→0.8, spy 0.5+0.5, Tesla tower). Their native tests should measure the actual interval too.

## Conclusion
- **Batch73:** XML-correct experimental package. "间隔恰减1/3" is **not confirmed**.
- Do not merge it into the approved baseline until a native measurement (old vs new Hammer shots per minute) decides between serial and overlap.
- **If overlap is proven,** the ⅓ target would need reload 0.4/0.667 (Min/Max ×2/3), still subject to N/15 rounding.
