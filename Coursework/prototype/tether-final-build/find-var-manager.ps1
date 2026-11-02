$a=[Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll')
try {$ts=$a.GetTypes()} catch [Reflection.ReflectionTypeLoadException] {$ts=$_.Exception.Types | Where-Object {$_}}
$f=[Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly'
foreach($t in $ts){try { foreach($m in $t.GetMethods($f)){if($m.ReturnType.FullName -eq 'mthl.uths' -and $m.GetParameters().Count -eq 0){$t.FullName+' '+$m.ToString()}};foreach($p in $t.GetProperties($f)){if($p.PropertyType.FullName -eq 'mthl.uths'){$t.FullName+' PROPERTY '+$p.Name}} } catch {}}
