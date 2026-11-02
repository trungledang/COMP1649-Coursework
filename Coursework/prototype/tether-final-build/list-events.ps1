$a=[Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll')
$t=$a.GetType('Axure.Constants.IxEventType')
[Enum]::GetNames($t) | Where-Object {$_ -match 'Text|Change|Load'}
