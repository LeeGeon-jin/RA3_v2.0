# Remaining items after Batch73 — minimal user questions + native tests
Scan basis: all 72 phase 一 / 一/二 entries in devdoc.txt vs package b108. Every simple numeric item is implemented or closed.

## A. Questions only the user can answer (design)
1. **Guard02 / cloning center / quick production center health** — values never given.
   - Doc L34 decision text lists the other attributes but no HP.
   - Q: what MaxHealth for each (or "same as model source")?
2. **Quick production center "立即恢复"** (L34 point 7 context).
   - The aura implementation restores after a 2 s expiry; true "immediate" has no XML switch found.
   - Q: is ≤2 s acceptable?
3. **Apocalypse AA** (L821): turret facing / harpoon mode / launch point when adding the AA weapon.
   - Q: re-use the VX missile visually from the main turret, or a separate launch point? Values otherwise re-use VX.
4. **Sentry gun conscripts on death** (L707-708, "生成数量待定").
   - Q: how many conscripts (1 per original convention)?
5. **Natasha** (L737):
   - (a) "一枪打爆一辆" vehicles/ships — Q: include epic/hero units (e.g. Shogun Executioner) and Iron-Curtained targets? Explosion death (DeathType EXPLODED) or normal?
   - (b) "对付建筑距离增加" — Q: CallBombingRun range from 300 to what?
6. **MCV / Soviet miner machine gun** (L598, L743; second batch by doc). Bone/firing-point choice affects visuals.
   - Q: accept using the model origin, i.e. no turret?
7. **Paradrop button** (tech airfield) and **oil derrick** (L368). Q: confirm scope (still listed as undecided).

Not asked (already decided or technical):
- bunker time (L31 keeps it);
- Hammer ⅓ (user wording is clear — only the engine timing is unknown);
- music/mouse (implemented);
- all permit/upgrade items (L948/L978 final).

## B. Native tests that decide technical unknowns (no user decision)
- **Weapon interval model:** serial FiringDuration + ClipReloadTime vs overlap. This decides Batch73 and re-checks Guardian/spy/Tesla intervals.
- **Overrides:** same-id package overrides of Static / global singletons (Weapon, Armor, AudioSettings, UIConfigs) take effect; the DefaultAlternateMouse ↔ "Alternate Mouse Setup" mapping.
- **Behaviour:**
  - Proton 10 shots after the 8 s shroud;
  - Vacuum 16 s;
  - aircraft passengers (L179);
  - instant capture (L182);
  - crush-no-stop (L206).
