import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'bridge-research/native-cli'))
import axure_cli as ax
def call(op,**kw):
 r=ax.request(dict(op=op,**kw))
 if not r.get('ok'):raise RuntimeError(f'{op}: {r}')
 return r['result']
pages=call('page.list')['pages'];assert len(pages)==6
home,work,stuck,pause,saved,completed=[p['Id'] for p in pages]
def h(name,y):return call('widget.create',kind='paragraph',name=name,text='',x=28,y=y,width=374,height=54)['id']
def actions(id,things):call('interaction.set',id=id,spec={'event':'click','cases':[{'name':'Continue','actions':things}]})
call('page.open',id=completed)
actions(h('complete_next',700),[{'type':'navigate','page':pause}])
actions(h('complete_home',769),[{'type':'navigate','page':home}])
call('page.open',id=work)
actions(h('v3_finish_step',808),[{'type':'storeLiteral','variable':'TetherWhere','value':'Finished the last step.'},{'type':'storeLiteral','variable':'TetherNext','value':'Decide what to do next.'},{'type':'navigate','page':completed}])
call('page.open',id=home);print(call('project.save'))
