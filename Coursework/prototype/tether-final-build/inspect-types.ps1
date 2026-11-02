$ErrorActionPreference='Stop'
$assembly = [Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll')
try { $types = $assembly.GetTypes() } catch [Reflection.ReflectionTypeLoadException] { $types = $_.Exception.Types | Where-Object { $_ } }
$types | Where-Object { try { $_.GetInterfaces().FullName -contains 'XIGI.eIG1' } catch { $false } } | ForEach-Object { 'IMPLEMENTS '+$_.FullName }
foreach ($name in @('Axure.DocumentModel.Objects.TextBox')) {
  $t = $types | Where-Object FullName -eq $name | Select-Object -First 1
  Write-Output "TYPE $name"
  if ($null -eq $t) {continue}
  $flags=[Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly'
  'base '+$t.BaseType.FullName
  $t.GetInterfaces() | ForEach-Object { 'INTERFACE '+$_.FullName }
  $t.GetConstructors($flags) | ForEach-Object { $_.ToString() }
  $t.GetFields($flags) | ForEach-Object { $_.FieldType.FullName+' '+$_.Name }
  $t.GetProperties($flags) | ForEach-Object { $_.PropertyType.FullName+' '+$_.Name }
  $t.GetMethods($flags) | Where-Object { -not $_.IsSpecialName } | ForEach-Object { $_.ToString() }
}
