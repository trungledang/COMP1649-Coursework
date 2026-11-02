$a=[Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll')
try{$ts=$a.GetTypes()}catch [Reflection.ReflectionTypeLoadException]{$ts=$_.Exception.Types|Where-Object{$_}}
$ts|Where-Object{$_.FullName -match 'Axvg|Clipboard|Paste|Svg'}|ForEach-Object{$_.FullName}
