$a=[Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll');[Enum]::GetNames($a.GetType('Axure.DocumentModel.Objects.InputType'))
try{$ts=$a.GetTypes()}catch [Reflection.ReflectionTypeLoadException]{$ts=$_.Exception.Types|?{$_}}
$ts|?{$_.FullName -match 'DocumentModel.Objects.*(TextArea|Multiline)'}|%{$_.FullName}
