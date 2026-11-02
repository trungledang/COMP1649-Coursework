$a=[Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll')
foreach($n in @('FJlc.QJlk')){
$t=$a.GetType($n);$n;$t.GetConstructors([Reflection.BindingFlags]'Public,NonPublic,Instance')|%{$_.ToString()};$t.GetMethods([Reflection.BindingFlags]'Public,NonPublic,Static,Instance,DeclaredOnly')|%{$_.ToString()};$t.GetProperties()|%{$_.ToString()}
}


