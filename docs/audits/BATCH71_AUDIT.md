# BATCH71 AUDIT — SOURCE PASS (native-compile candidate; not natively verified)
No full XSD, compile or in-game test. Not claimed to run correctly. Phase 1 not complete.
Not claimed that the default is in effect or that any volume changed.

## Package
- 292561 B, sha256 38da62cc…78ed9cadb match.
  - The first copy attempt hit a mount I/O error ("Transport endpoint is not connected").
  - Retried the same path; size and SHA then matched.
- All entries under `data/`. 116 XML parse. Mod: 115 all.
- vs 70:
  - new `data/Sounds/AudioSettings.xml`;
  - Mod +1 at L7 `<Include type="all" source="DATA:Sounds/AudioSettings.xml" />`, right after the three references (a single tab-indented line; no extra blank line found in the diff);
  - the other 114 files are byte-identical (commands too).

## AudioSettings.xml vs SDK
- 115 lines each, same BOM. `diff` = only L48 DefaultMusicVolume 50% → 0%.
- **Kept:**
  - the default asset namespace header, `<Tags/>`;
  - the instance include `DATA:Includes/PlatformSpecificAudioDefines.xml`;
  - all other attributes/elements (Sound 75 / Ambient 60 / Movie 70 / Voice 70, VolumeSliderMultiplier…).
- **Closure:**
  - the include target exists in SDK `XMLFiles/Includes/` (the only copy; the package does not ship one → resolves to SDK);
  - all 6 `$PLATFORM_SPECIFIC_*` defines used by the file are defined there.
- UI mouse and Options.ini not touched.

## Native test
- **Startup timing:** whether the mod's TheAudioSettings singleton is used. It is normally loaded via global.xml → MasterAudioEvents, early at startup.
- **Possible build duplicate:** the asset builder may object to a duplicate singleton.
- **Fresh profile:** a new profile should show music at 0.
- **Existing profiles:** they keep their Options.ini MusicVolume.
