$a=[Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll')
try {$ts=$a.GetTypes()} catch [Reflection.ReflectionTypeLoadException] {$ts=$_.Exception.Types | Where-Object {$_}}
$f=[Reflection.BindingFlags]'Public,NonPublic,Instance,DeclaredOnly'
foreach($t in $ts){try {foreach($m in $t.GetConstructors($f)){ $p=$m.GetParameters(); if(($p | Where-Object {$_.ParameterType.FullName -eq 'MJuB.gJuG'}).Count -gt 0){$t.FullName+' '+$m.ToString()}}}catch{}}
