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
call('page.open',id=work);ws=call('widget.list')
task=next(w['id'] for w in ws if w.get('text') and 'Add one example' in w['text'])
print('Work load',call('debug.page_load',actions=[{'type':'showGlobal','variable':'TetherNext','widget':task}]))
call('page.open',id=saved);ws=call('widget.list')
changes={'This prototype uses an example thread on the desk.':'Your notes stay available during this preview.',
         'You can step away without losing the thread.':'Your note is ready on your desk.'}
for w in ws:
 if w.get('text') in changes:print('Copy',call('widget.text',id=w['id'],text=changes[w['text']]))
call('page.open',id=home);print('Saved',call('project.save'))
