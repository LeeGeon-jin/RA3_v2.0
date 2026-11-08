# BATCH51 AUDIT — SOURCE PASS (native-compile candidate)
Source check only; not full XSD, not compiled, not tested. Phase 1 not complete.
- 259698 B, sha256 `7a4c956ef519d78d60da879200f4c9fcfd962eb34795eb36b6a9987e64a6ea0d` match; saved `batch51.tar.gz`; safe paths.
- vs 50: only `Allied/Structures/AlliedTechStructure.xml` L17 BuildTime 15→30, L36 Amount 1000→1500. Other 97 files byte-identical (Mod, LogicCommand/Set unchanged). 98 XML parse; Mod 97 all + 3 ref.
- vs SDK: now identical except removal of 7 ART type="all" includes (established ART rule since batch2). GameDependency AlliedAirfield + AlliedRefinery, no licence dependency — unchanged.
- Basis: main assistant's search of visible user history (only licence/unlock requests), doc L459-464 (no cost/time change), cloud artifacts FINAL_SUMMARY L81 / PHASE1_REGRESSION_REPORT L145-147 misapplying the neutral tech rule.
