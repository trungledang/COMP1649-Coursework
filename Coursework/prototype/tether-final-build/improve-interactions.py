import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'bridge-research/native-cli'))
import axure_cli as ax
def call(op,**kw):
 r=ax.request(dict(op=op,**kw))
 if not r.get('ok'):raise RuntimeError(f'{op}: {r}')
 return r['result']
pages=call('page.list')['pages'];home,work,stuck,pause,saved=[x['Id'] for x in pages]
call('page.open',id=stuck)
known={x['name'] for x in call('debug.vars')['variables']}
if 'TetherSuggestion' not in known: print('Variable',call('debug.var_add',name='TetherSuggestion',value='Open your notes and choose one sentence.'))
ws=call('widget.list');helpid=next(w['id'] for w in ws if w.get('text') and 'finding one sentence' in w['text'])
choices=[('start',305,'Open your notes and choose one sentence.'),('small',390,'Write just the first line of this step.'),('source',475,'Open the reading list and find one source.')]
for name,y,value in choices:
 h=call('widget.create',kind='paragraph',name='v2_choice_'+name,text='',x=66,y=y,width=324,height=72)['id']
 call('interaction.set',id=h,spec={'event':'click','cases':[{'name':name,'actions':[{'type':'setText','target':helpid,'text':value},{'type':'storeLiteral','variable':'TetherSuggestion','value':value}]}]})
h=call('widget.create',kind='paragraph',name='v2_try_suggestion',text='',x=28,y=722,width=374,height=54)['id']
call('interaction.set',id=h,spec={'event':'click','cases':[{'name':'Use smaller step','actions':[{'type':'copyGlobal','variable':'TetherNext','source':'TetherSuggestion'},{'type':'navigate','page':work}]}]})
call('page.open',id=pause);ws=call('widget.list')
i1=next(w['id'] for w in ws if w['name']=='where_stopped');i2=next(w['id'] for w in ws if w['name']=='next_move')
for i in [i1,i2]:print('Input limit',call('debug.input_limit',id=i,limit=48))
print('Edit note load',call('debug.page_load',actions=[{'type':'showGlobalInput','variable':'TetherWhere','widget':i1},{'type':'showGlobalInput','variable':'TetherNext','widget':i2}]))
hint=next(w['id'] for w in ws if w.get('text') and 'Think of an action' in w['text'])
print('Hint',call('widget.text',id=hint,text='Keep each note under 48 characters.'))
call('page.open',id=home);print('Saved',call('project.save'))
