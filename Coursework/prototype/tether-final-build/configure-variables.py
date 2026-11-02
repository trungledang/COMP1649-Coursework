import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(Path(__file__).resolve().parent/'bridge-research/native-cli'))
import axure_cli as ax
def call(op,**kw):
 r=ax.request(dict(op=op,**kw))
 if not r.get('ok'):raise RuntimeError(f'{op}: {r}')
 return r['result']
pages=call('page.list')['pages'];home,work,stuck,pause,saved=[x['Id'] for x in pages]
call('page.open',id=home)
vars=call('debug.vars')['variables'];known={v['name'] for v in vars}
for name,value in [('TetherWhere','Connecting my evidence to the argument.'),('TetherNext','Add one example to the second paragraph.')]:
 if name not in known:print('Added',call('debug.var_add',name=name,value=value),flush=True)
ws=call('widget.list')
where=next(w['id'] for w in ws if w.get('text') and 'Connecting my evidence' in w['text'])
nxt=next(w['id'] for w in ws if w.get('text') and 'Add one example' in w['text'])
print('OnLoad',call('debug.page_load',actions=[{'type':'showGlobal','variable':'TetherWhere','widget':where},{'type':'showGlobal','variable':'TetherNext','widget':nxt}]),flush=True)
print('Page map',json.dumps(call('debug.diagram')),flush=True)
call('page.open',id=pause);ws=call('widget.list')
i1=next(w['id'] for w in ws if w['name']=='where_stopped');i2=next(w['id'] for w in ws if w['name']=='next_move')
feedback=next(w['id'] for w in ws if w.get('text') and 'Think of an action' in w['text'])
h=call('widget.create',kind='paragraph',name='hit_save_with_variables',text='',x=28,y=711,width=374,height=54)['id']
spec={'event':'click','cases':[
 {'name':'Missing position','when':{'widget':i1,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Add where you stopped first.'}]},
 {'name':'Missing next move','when':{'widget':i2,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Add the next small move first.'}]},
 {'name':'Save and continue','actions':[{'type':'storeGlobal','variable':'TetherWhere','widget':i1},{'type':'storeGlobal','variable':'TetherNext','widget':i2},{'type':'navigate','page':saved}]}]}
print('Save map',json.dumps(call('interaction.set',id=h,spec=spec)),flush=True)
call('page.open',id=home);print('Saved',call('project.save'),flush=True)
