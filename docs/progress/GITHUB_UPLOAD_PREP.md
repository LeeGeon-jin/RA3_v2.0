# 公开 GitHub 仓库 RA3_v2.0：待上传资料清单与初筛（2026-11-09 09:18 UTC+10）
这份清单只在本地整理，没有创建仓库，也没有上传或编译。上传由主协调负责执行，用户只定了顺序（08:56）。初筛只是粗查，**发布前仍需要人工确认**，尤其是许可问题。

## A. 建议上传
1. **Mod 源码（最新基线 Batch102FIX）：** 解包后的 data/ 目录，153 个 XML（来自 batch102fix.tar.gz，sha256 053c6b49…bdca）。包内只有 XML，没有 w3x、dds 等美术文件。
2. **最新 md：**
   - 红警3_V2.0_开发进度_2026-11-08.md
   - NEXT_PHASE2_FINAL.md
   - NEXT_PRECISION_B101.md
   - PHASE2_KIROV_PRECISION_VERIFY.md
   - PHASE2_SCOPE_2026-11-08.md
   - USER_DECISIONS_2026-11-09_0354_0355.md
3. **审计记录：** BATCH*_AUDIT.md / .txt 共 156 个，覆盖第一阶段 B10 到第二阶段 102FIX（包括 FAIL 的批次，用来记录修复过程）。
4. **研究和规划文档：**
   - NEXT_*.md（R62–R94，以及机场、轰炸机、先进幻影等）
   - RESEARCH_*、COVERAGE_*、HOSPITAL_PLAN_*、HP_SOURCE_AUDIT_*、OPEN_QUESTIONS_*、PHASE1_*
5. **构建和工具脚本：**
   - build.ps1：只调用官方 SDK 工具。里面有本机路径 E:\RA3ModBuild，不含用户名，可以保留或改成参数。
   - phase2_refs_build.py
6. **包的哈希索引：** 建议从进度 md 附录 A 提取 batch 包的大小和 SHA 列表，生成一份 PACKAGES.md。batch*.tar.gz 本身共 155 个，见 C 项。

## B. 不应直接公开，或需要先确认
- **EA SDK 和游戏原文件（第三方版权）：**
  - 44 个 *_sdk_refs.tar.gz、refs_*.tar.gz、precision_b101_refs.tar.gz，里面是原样复制的 SDK XML；
  - ra3-sdk-build-input.zip（1158 个文件）、sagexml-fill.zip（6236 个文件）；
  - sbres/ 下的 mod.bin 编译产物。

  建议**不上传**，只在文档里写明它们的来源（RA3 Mod SDK）和对应的 SDK 行号。
- **Mod 的 XML 本身也是从 EA SDK XML 派生的。** RA3 Mod 圈公开 XML 很常见，但许可要由项目所有者确认。建议在 README 注明：需要另装官方 RA3 Mod SDK 和游戏，本仓库不含任何游戏美术。
- **游戏美术（ART）：** 当前包里没有。本机的 75 B w3x 占位文件不在这些包里，不要上传。
- **编译日志和结果包：** build_logs*.zip、*_result.zip、minimalfix_*.zip、mod_minimal / minfix / source.tar.gz。可能含本机路径和 SDK 输出，建议不上传，或只摘要。
- **devdoc.txt（1736 行）：** 用户原始的设计文档。是否公开要由用户确认。
- **临时文件：** _fd_main.txt、_fulldiff_b85.txt、*_PENDING.txt，建议不上传。
- **敏感信息初筛：** 用关键词（token、password、api key、ghp_、Users 路径、邮箱）扫描 md、py、ps1、xml，**没有命中**真实凭据或个人信息。命中的两处都是误报：BATCH76FIX 里普通文字的 “tokens”，以及 UIComponentOptionsSettingsGeneral 中 SDK 原有的 LoadVarQueryReturnToken。

## C. 待定
- 155 个历史 batch 包是否上传：体积大，而且 XML 内容和最终 data/ 重复。建议只上传最终源码和哈希索引，用 git 历史代替。
- 仓库要不要附 LICENSE、README 免责声明，由项目所有者决定。
