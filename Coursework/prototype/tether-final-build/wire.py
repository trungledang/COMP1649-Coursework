import json, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools/axure-ai/native-cli'))
os.environ['REVERSE_CLI_CACHE_DIR']='E:/ai-cache/axure-pilot/cache'
import axure_cli as ax

def call(op,**kw):
 r=ax.request(dict(op=op,**kw))
 if not r.get('ok'):raise RuntimeError(f'{op}: {r}')
 return r['result']
def click_action(wid, actions, name='Open'):
 call('interaction.set',id=wid,spec={'event':'click','cases':[{'name':name,'actions':actions}]})
def go(wid,target):click_action(wid,[{'type':'navigate','page':target}])
def hotspot(name,y):
 return call('widget.create',kind='paragraph',name='hit_'+name,text='',x=28,y=y,width=374,height=54)['id']
def input_box(name,y,placeholder):
 return call('widget.create',kind='input',name=name,text='',placeholder=placeholder,x=78,y=y,width=286,height=50)['id']

pages=call('page.list')['pages']; assert len(pages)==5
home,work,stuck,pause,saved=[p['Id'] for p in pages]
items=[]
call('page.open',id=home)
for n,y,dest in [('continue',705,work),('pause',774,pause)]:
 h=hotspot(n,y);go(h,dest);items.append((n,h))
call('page.open',id=work)
for n,y,dest in [('stuck',670,stuck),('pause',739,pause),('done',808,saved)]:
 h=hotspot(n,y);go(h,dest);items.append((n,h))
call('page.open',id=stuck)
ws=call('widget.list')
helpid=next(w['id'] for w in ws if w.get('text') and 'finding one sentence' in w['text'])
for name,y,message in [('start',305,'Try opening your notes and choosing one sentence.'),('small',390,'Try writing just the first line of this step.'),('source',475,'Try opening the reading list and finding one source.')]:
 h=call('widget.create',kind='paragraph',name='hit_'+name,text='',x=66,y=y,width=324,height=72)['id']
 click_action(h,[{'type':'setText','target':helpid,'text':message}],name);items.append((name,h))
for n,y,dest in [('try',722,work),('back',791,work)]:
 h=hotspot(n,y);go(h,dest);items.append((n,h))
call('page.open',id=pause)
where=input_box('where_stopped',354,'e.g. halfway through a paragraph')
nxt=input_box('next_move',484,'e.g. find one supporting example')
ws=call('widget.list');feedback=next(w['id'] for w in ws if w.get('text') and 'Think of an action' in w['text'])
save=hotspot('save',711)
call('interaction.set',id=save,spec={'event':'click','cases':[
 {'name':'Missing position','when':{'widget':where,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Add where you stopped first.'}]},
 {'name':'Missing next move','when':{'widget':nxt,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Add the next small move first.'}]},
 {'name':'Finish','actions':[{'type':'navigate','page':saved}]}]})
back=hotspot('back',780);go(back,work)
call('page.open',id=saved);h=hotspot('home',738);go(h,home)
call('page.open',id=home);call('project.save')
(Path(__file__).parent/'wired-ids.json').write_text(json.dumps({'pages':[home,work,stuck,pause,saved],'items':items,'inputs':[where,nxt]},indent=2),encoding='utf-8')
print('Saved all five pages with native click actions and two native inputs.')
