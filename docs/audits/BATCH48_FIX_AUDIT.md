# BATCH48_FIX AUDIT — SOURCE PASS (native-compile candidate)
Box-only read; not full XSD, not compiled, not tested in game. Phase 1 not complete.
- 249075 B, sha256 `782c36ddc0c3cfa1f7acd25705134e62aa357a87d350f0e44c5ce1c253fba78e` match; saved `batch48_FIX.tar.gz`; safe paths.
- Only `Allied/Structures/AlliedStatueOfLiberty.xml` differs from 48: KindOf → `-NOT_AUTOACQUIRABLE +AUTO_ACQUIRABLE_BY_AI`; DisplayName block (text, `xai:joinAction="Replace"` + inline xmlns:xai, byte-identical) moved ahead of ObjectResourceInfo; blank-line changes only. 93 other files identical.
- Order now DisplayName → ObjectResourceInfo → Draws (AssetTypeGameObject.xsd L385-389 sequence). Parent NOT_AUTOACQUIRABLE removed.
- Body ModuleTag_Body `=$CIV_HEALTH_MEDIUM` kept; single choice slot (xsd L301-303) → correct.
- 94 XML parse; Mod 93 all + 3 ref; all B48 verbatim/command/count (Allied CY 16, Crane 15) items unchanged.
- Test: ART/collapse resolution in native build log; ~270×278 footprint; UI assets; counts for defeat.
