import {writeFileSync} from 'node:fs';
import {circle,text,hex} from '../../../tools/axure-ai/axvg/axvg-build.ts';
const bg=circle({name:'profile_avatar_bg',x:360,y:62,d:40,fill:hex('#175C59')});
const label=text({x:360,y:70,w:40,h:24,content:'A',size:18,color:hex('#FFFFFF'),weight:700,align:'center',typeface:'Inter - Bold'});
label.name='profile_avatar_initial';label.isNameDynamic=false;
writeFileSync(new URL('./profile-avatar.axvg.json',import.meta.url),'// axvg\n'+JSON.stringify({masters:{},imageMap:{},scene:{items:[bg,label]}}));
