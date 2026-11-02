$ErrorActionPreference='Stop'
$a=[Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll')
try {$ts=$a.GetTypes()} catch [Reflection.ReflectionTypeLoadException] {$ts=$_.Exception.Types | Where-Object {$_}}
$flags=[Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly'
foreach ($t in $ts) {
 try {
  foreach ($m in $t.GetMethods($flags)) {
   $p=$m.GetParameters(); if ($p.Count -gt 0 -and ($p | Where-Object {$_.ParameterType.FullName -eq 'Lth0.zthm'})) { Write-Output ($t.FullName+' '+$m.ToString()) }
  }
 } catch {}
}
