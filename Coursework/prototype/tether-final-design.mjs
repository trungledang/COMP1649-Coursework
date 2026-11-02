import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const here=dirname(fileURLToPath(import.meta.url));
const kit=resolve(here,'../../tools/axure-ai/axvg/axvg-build.ts');
const {rect,text,circle,frame,composeDesign,hex}=await import(pathToFileURL(kit));
const out=resolve(here,'tether-final-build');mkdirSync(out,{recursive:true});
const C={paper:'#F1F6F5',white:'#FFFFFF',ink:'#132E39',soft:'#526B70',teal:'#175C59',mint:'#D9EBE5',lilac:'#E7DDF6',coral:'#D95747',sand:'#F5E6CC',line:'#9E84C7'};
const R=(name,x,y,w,h,color,r=0)=>rect({name,x,y,w,h,fill:hex(color),corners:r});
const T=(name,x,y,w,h,content,size=16,color=C.ink,weight=400,align='left')=>text({name,x,y,w,h,content,size,color:hex(color),weight,align,typeface:weight===700?'Inter - Bold':'Inter - Regular'});
const card=(name,x,y,w,h,col=C.white)=>R(name,x,y,w,h,col,20);
const dot=(name,x,y,d,col)=>circle({name,x,y,d,fill:hex(col)});
const button=(name,y,label,secondary=false)=>[
 R(name+'_bg',28,y,374,54,secondary?C.white:C.teal,15),
 T(name+'_label',28,y+16,374,24,label,16,secondary?C.teal:C.white,700,'center')];
const base=(kicker)=>[
 R('canvas',0,0,430,932,C.paper,0),
 R('island',162,11,106,24,C.ink,12),
 T('time',28,19,70,20,'9:41',13,C.ink,700),
 T('brand',28,66,180,28,'tether',22,C.teal,700),
 T('section',273,74,129,20,kicker,12,C.soft,400,'right'),
 R('thread',46,160,3,505,C.line,2), dot('thread_start',40,154,15,C.line),dot('thread_end',40,657,15,C.line),
 R('home_indicator',164,909,102,5,C.ink,3)
];
const pages=[
 {id:'desk',items:[...base('Your study desk'),
 T('title',76,148,310,72,'You can pick\nthis up again.',30,C.ink,700),
 T('intro',76,231,300,48,'A little context, right where you need it.',15,C.soft),
 card('paper_shadow',73,304,303,179,C.lilac),
 card('note_card',64,294,310,179,C.white),
 T('note_tag',87,315,255,22,'HCI coursework  /  Discussion',12,C.teal,700),
 T('note_title',87,346,260,48,'Where I left off',20,C.ink,700),
 T('note_body',87,383,255,64,'Connecting my evidence\nto the argument.',16,C.ink),
 card('next_card',88,496,300,91,C.sand),
 T('next_tag',108,511,255,18,'Your next move',12,C.soft,700),
 T('next_body',108,537,255,42,'Add one example to\nthe second paragraph.',15,C.ink,700),
 ...button('continue',705,'Continue this step'),...button('pause',774,'Leave a new thread',true)]},
 {id:'work',items:[...base('Continue'),
 T('title',76,148,300,72,'One step.\nAt your pace.',30,C.ink,700),
 T('intro',76,231,300,50,'You do not have to finish everything today.',15,C.soft),
 card('task_card',64,311,310,202,C.white),
 T('task_label',88,333,255,20,'Discussion section',13,C.teal,700),
 T('task',88,373,255,92,'Add one example\nto the second\nparagraph.',21,C.ink,700),
 T('task_hint',88,469,255,25,'A small move is enough.',13,C.soft),
 card('time_card',94,543,280,63,C.lilac),
 T('time_text',113,564,240,23,'Try it for a few minutes.',14,C.ink),
 ...button('stuck',670,'I feel stuck',true),...button('pause',739,'Pause and leave a thread'),...button('done',808,'Finish this step',true)]},
 {id:'stuck',items:[...base('Get unstuck'),
 T('title',76,148,305,72,'Let’s make\nthis lighter.',30,C.ink,700),
 T('intro',76,237,305,48,'Choose what feels hard right now.',15,C.soft),
 card('option1',66,305,310,72,C.white),T('opt1',86,327,270,25,'I do not know where to start',15,C.ink,700),
 card('option2',80,390,310,72,C.white),T('opt2',100,412,270,25,'This step feels too big',15,C.ink,700),
 card('option3',66,475,310,72,C.white),T('opt3',86,497,270,25,'I need a source or example',15,C.ink,700),
 card('help_card',79,575,309,87,C.mint),T('help',98,591,270,54,'Try finding one sentence\nin your notes to use.',15,C.teal,700),
 ...button('try',722,'Try this smaller step'),...button('back',791,'Back to my work',true)]},
 {id:'pause',items:[...base('Save your place'),
 T('title',76,145,305,75,'Leave a note\nfor future you.',29,C.ink,700),
 T('intro',76,232,305,50,'A sentence is enough. You can change it later.',15,C.soft),
 T('where_label',67,315,310,25,'Where did you stop?',16,C.ink,700),
 R('where_box',66,350,310,58,C.white,12),
 T('next_label',67,445,310,25,'What is the next small move?',16,C.ink,700),
 R('next_box',66,480,310,58,C.white,12),
 T('hint',67,555,310,55,'Think of an action you could do\nin a few minutes.',14,C.soft),
 ...button('save',711,'Save my place'),...button('back',780,'Back to my work',true)]},
 {id:'saved',items:[...base('Saved'),
 T('title',76,148,310,74,'Your place\nis here.',30,C.ink,700),
 T('intro',76,236,305,52,'You can step away without losing the thread.',15,C.soft),
 card('saved_card',68,323,310,187,C.lilac),
 T('saved_label',90,344,260,20,'A NOTE FOR LATER',12,C.teal,700),
 T('saved_title',90,381,260,58,'Ready when\nyou are.',22,C.ink,700),
 T('saved_desc',90,458,260,35,'Return to your desk anytime.',14,C.soft),
 T('honest',76,560,300,70,'This prototype uses an example thread on the desk.',13,C.soft),
 ...button('home',738,'Back to my desk')]}
];
pages.push({id:'completed',items:[...base('Step complete'),
 T('title',76,148,310,74,'That step\nis done.',30,C.ink,700),
 T('intro',76,236,305,52,'You made room for the next move.',15,C.soft),
 card('complete_card',68,323,310,187,C.mint),
 T('complete_label',90,344,260,20,'COMPLETED',12,C.teal,700),
 T('complete_title',90,381,260,58,'One step\nis enough.',22,C.ink,700),
 T('complete_desc',90,458,260,35,'Choose what happens next.',14,C.soft),
 T('note',76,560,300,70,'Leave the next move now or come back to the desk.',13,C.soft),
 ...button('next',700,'Leave my next step'),...button('home',769,'Back to my desk',true)]});
for (const p of pages){const d=composeDesign(frame({name:'Tether '+p.id,w:430,h:932,bg:hex(C.paper),children:p.items}));writeFileSync(resolve(out,p.id+'.axvg.json'),'// axvg\n'+JSON.stringify(d));}
console.log(JSON.stringify(pages.map(p=>p.id)));
export {C,R,T,card,dot,button,base};
