import json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/axure-ai/native-cli'))
os.environ['REVERSE_CLI_CACHE_DIR'] = 'E:/ai-cache/axure-pilot/cache'
import axure_cli as ax

def call(op, **kwargs):
    r = ax.request({'op': op, **kwargs})
    if not r.get('ok'):
        raise RuntimeError(f'{op}: {r}')
    return r['result']

def widget(kind, name, text, y, **extra):
    return call('widget.create', kind=kind, name=name, text=text, x=80, y=y, width=500, height=42, **extra)['id']

def link(button, page):
    call('interaction.set', id=button, spec={'event':'click','cases':[{'name':'Open','actions':[{'type':'navigate','page':page}]}]})

pages = call('page.list')
assert len(pages['pages']) == 1 and not call('widget.list')
home = pages['activeId']
work = call('page.create', name='02 Continue your work')['page']['Id']
stuck = call('page.create', name='03 When you are stuck')['page']['Id']
pause = call('page.create', name='04 Leave a thread')['page']['Id']
done = call('page.create', name='05 Ready to return')['page']['Id']

call('page.open', id=home)
widget('paragraph','brand','TETHER  |  Keep the thread',70)
widget('paragraph','title','Come back to where you left off.',140)
widget('paragraph','intro','Your work can wait. Your place will be here when you return.',200)
widget('paragraph','context','COURSEWORK · DISCUSSION SECTION',280)
widget('paragraph','last','Last time: I was connecting the evidence to my argument.',330)
widget('paragraph','next','Next move: add one example to the second paragraph.',390)
b = widget('button','continue','Continue this step',475); link(b,work)
b = widget('button','save_new','Leave a new thread',535); link(b,pause)

call('page.open', id=work)
widget('paragraph','title','One step, at your pace.',80)
widget('paragraph','context','Discussion section',155)
widget('paragraph','step','Add one example to the second paragraph.',220)
widget('paragraph','note','You can change the next step or leave it here for later.',280)
b=widget('button','stuck','I feel stuck',365); link(b,stuck)
b=widget('button','pause','Pause and leave a thread',425); link(b,pause)
b=widget('button','complete','Finish this step',485); link(b,done)
b=widget('button','home','Back to my desk',545); link(b,home)

call('page.open', id=stuck)
widget('paragraph','title','Let us make this easier.',80)
widget('paragraph','prompt','What is making the next step difficult?',150)
widget('paragraph','advice','Try this: open your notes and find one sentence you could use.',230)
widget('paragraph','hint','You can stop after that. A small step is still a step.',295)
b=widget('button','try','Try the smaller step',375); link(b,work)
b=widget('button','leave','Pause for now',435); link(b,pause)
b=widget('button','back','Back',495); link(b,work)

call('page.open', id=pause)
widget('paragraph','title','Leave a thread for future you.',80)
widget('paragraph','prompt','Where did you stop?',150)
widget('input','where','',205,placeholder='For example: halfway through the second paragraph')
widget('paragraph','prompt_next','What is the next physical step?',275)
widget('input','next','',330,placeholder='For example: find one supporting example')
widget('paragraph','limitation','These notes stay on this screen in this draft.',395)
b=widget('button','save','Done',470); link(b,done)
b=widget('button','back','Back to my work',530); link(b,work)

call('page.open', id=done)
widget('paragraph','title','A place to begin again.',90)
widget('paragraph','body','You have reached a stopping point. Return to the desk when you are ready.',170)
widget('paragraph','note','The example thread remains available on the desk.',255)
b=widget('button','home','Return to my desk',360); link(b,home)
call('page.open', id=home)
call('project.save')
print(json.dumps({'pages':call('page.list'),'file':'final-coursework.rp'},ensure_ascii=False))
