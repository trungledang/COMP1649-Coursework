$a=[Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll')
[Enum]::GetNames($a.GetType('Axure.DocumentModel.Edit.TreeEditType'))
$t=$a.GetType('ESDL.lSDD');$t.GetMethods([Reflection.BindingFlags]'Public,NonPublic,Static,Instance,DeclaredOnly')|%{$_.ToString()}
