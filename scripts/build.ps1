# Orchestrates only official SDK tools; does not edit mod/SDK files. Args per SDK DefaultScript.cs step 6.
$ErrorActionPreference='Stop'
$root='E:\RA3ModBuild'; $sdk="$root\RA3ModSDK"; $mod='RA3_V2.0_Mod'; $logs="$root\logs"
New-Item -ItemType Directory -Force $logs | Out-Null
function Run($name,$exe,$argList,$timeoutSec){
  $p=Start-Process -FilePath $exe -ArgumentList $argList -WorkingDirectory $sdk -NoNewWindow -PassThru -RedirectStandardOutput "$logs\$name.stdout.txt" -RedirectStandardError "$logs\$name.stderr.txt"
  if(-not $p.WaitForExit($timeoutSec*1000)){ Stop-Process -Id $p.Id -Force; "$name TIMEOUT after $timeoutSec s" | Tee-Object -Append "$logs\summary.txt"; return }
  "$name exit=$($p.ExitCode)" | Tee-Object -Append "$logs\summary.txt"
}
"cmd: $sdk\Tools\BinaryAssetBuilder.exe /?" | Out-File -Append "$logs\summary.txt"
Run 'smoke' "$sdk\Tools\BinaryAssetBuilder.exe" '/?' 60
$a="`"Mods\$mod\data\Mod.xml`" /od:`"$sdk\builtmods`" /iod:`"$sdk\builtmods`" /csc:false /ls:true /osh:false /pc:true /res:true /slowclean:true /ss:true /art:`".;.\Mods\$mod\Art;.\Mods;.\Art`" /audio:`".;.\Mods\$mod\Audio;.\Mods;.\Audio`" /data:`".;.\Mods\$mod\Data;.\Mods;.\SageXml`""
"cmd: BinaryAssetBuilder.exe $a" | Out-File -Append "$logs\summary.txt"
Run 'build' "$sdk\Tools\BinaryAssetBuilder.exe" $a 1800
