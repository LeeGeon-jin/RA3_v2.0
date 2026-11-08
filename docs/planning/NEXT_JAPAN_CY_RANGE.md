# Next item: Empire Construction Yard initial build range = Soviet (5.6 #26, doc L1091-L1096)
Status: decided, "容易", batch 一, no user value pending. Not in package (no JapanConstructionYard.xml in b81).

## Decision (L1095, quote)
"旧 → 新（只改 JapanConstructionYard）：①BuildPlacementTypes "OTHER_STRUCTURE" → "MAIN_STRUCTURE OTHER_STRUCTURE"（480 / 465 不变）；②新增与苏军相同的 600 / 585 船厂圈（参数照抄苏军）。视野…MCV 移速、核心自由展开、其他阵营范围及其他帝国建筑自身半径（兵营 105 等）都不动；任务 overrides.xml 中的建筑副本按已定例外不改。" Other Japan buildings' own ranges adding MAIN_STRUCTURE = "不在本要求内（待定）" → do NOT touch.

## SDK verified
- `Japan/Structures/JapanConstructionYard.xml` ~L654-657: single `<ProjectedBuildabilityInfo Radius="480" RadiusY="465" BuildPlacementTypes="OTHER_STRUCTURE" />`, last node before `</GameObject>`.
- `Soviet/Structures/SovietConstructionYard.xml` L570-585: first 480/465 `MAIN_STRUCTURE OTHER_STRUCTURE`; second 600/585 same types, `AllowedBuildabilityHeightVariation="-1.0"`, `AllowedObjectFilter Rule="NONE"` IncludeThing AlliedNavalYard/SovietNavalYard/JapanNavalYard.

## Minimal batch 50
1. Full verbatim copy of SDK JapanConstructionYard.xml into `data/Japan/Structures/JapanConstructionYard.xml` (keep all includes/xi; root has no xmlns:xai — none needed).
2. Change only `BuildPlacementTypes="OTHER_STRUCTURE"` → `"MAIN_STRUCTURE OTHER_STRUCTURE"` on the existing node.
3. Append second ProjectedBuildabilityInfo copied byte-for-byte from Soviet L574-585, right after the first (end of GameObject; schema position same as Soviet).
4. Mod +1 include → 97 all + 3 ref. No CommandSet/LogicCommand change.
Audit points: only these two node changes; VisionRange 100 unchanged; no other Japan building touched; CampaignOverrides untouched.
Attach (SDK XMLFiles/): Japan/Structures/JapanConstructionYard.xml; Soviet/Structures/SovietConstructionYard.xml (L570-585 reference only).
Test: placement of MAIN_STRUCTURE buildings in 480×465; naval ring effect for Japan yard cores (may be inert).

## Not chosen / still blocked
- RA2-style expandable range (5.4 #3, L465): medium, batch 二, needs more design → later.
- Neutral tech buildings (5.2): many values; needs a separate read.
- Quick-production: 2 s aura expiry ≠ "立即恢复" → unresolved; health 待定. Clone health, Guard02 health, Rushmore Japan split: user.
