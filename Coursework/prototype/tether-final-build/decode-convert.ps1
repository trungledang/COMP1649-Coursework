$a=[Reflection.Assembly]::LoadFrom('E:/AxureRP11.dll')
$t=$a.GetType('Axure.Axvg.AxvgToRP.IntermediateFormatConverter');$m=$t.GetMethod('OJDl',[Reflection.BindingFlags]'Public,NonPublic,Static,Instance');$b=$m.GetMethodBody().GetILAsByteArray()
$ops=@{};[Reflection.Emit.OpCodes].GetFields([Reflection.BindingFlags]'Public,Static')|%{$o=$_.GetValue($null);$ops[[int]$o.Value]=$o}
$i=0;while($i -lt $b.Length){$pos=$i;$v=[int]$b[$i++];if($v -eq 254){$v= -512+[int]$b[$i++]};$o=$ops[$v];if(!$o){throw "opcode $v"};$arg='';$n=0;switch($o.OperandType.ToString()){
'InlineNone'{} 'ShortInlineI'{$n=1} 'ShortInlineVar'{$n=1} 'ShortInlineBrTarget'{$n=1} 'InlineVar'{$n=2} 'InlineI8'{$n=8} 'InlineR'{$n=8} 'ShortInlineR'{$n=4} 'InlineSwitch'{$n=4+4*[BitConverter]::ToInt32($b,$i)} default{$n=4}
};if($n -eq 4){$token=[BitConverter]::ToInt32($b,$i);try{if($o.OperandType.ToString() -eq 'InlineString'){$arg=$m.Module.ResolveString($token)}elseif($o.OperandType.ToString() -match 'Inline(Method|Field|Type|Tok)'){$arg=$m.Module.ResolveMember($token).ToString()}else{$arg=$token}}catch{$arg=$token}};$i+=$n;'{0:X4} {1} {2}' -f $pos,$o.Name,$arg}

