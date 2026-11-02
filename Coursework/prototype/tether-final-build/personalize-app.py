import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'bridge-research/native-cli'));import axure_cli as a
P=json.loads((H/'app-page-ids.json').read_text())
def c(op,**kw):
 r=a.request(dict(op=op,**kw));assert r.get('ok'),r;return r['result']
def open(k):c('page.open',id=P[k])
def ws():return c('widget.list')
def bytext(s):return next(w['id'] for w in ws() if w.get('text')==s)
def rename(s,t):
 found=next((w for w in ws() if w.get('text')==s),None)
 if found:c('widget.text',id=found['id'],text=t)
def show(v,id):return {'type':'showGlobal','variable':v,'widget':id}
def load(actions):c('debug.page_load',actions=actions,replace=True)
def hotspot(n,x,y,w,h,actions):
 z=c('widget.create',kind='paragraph',name=n,text='',x=x,y=y,width=w,height=h)['id'];c('interaction.set',id=z,spec={'event':'click','cases':[{'name':n,'actions':actions}]})
f=(H.parent/'final-coursework.rp').resolve();c('project.open',path=str(f))
open('plan');known={v['name'] for v in c('debug.vars')['variables']}
for v,value in [('TetherStep1','Identify the main requirements.'),('TetherStep2','Find two useful sources.'),('TetherStep3','Draft one paragraph.')]:
 if v not in known:c('debug.var_add',name=v,value=value)
rename('A clear path.\nRoom to change it.','Your plan.\nYour next move.')
load_actions=[show('TetherAssignment',bytext('HCI coursework · choose a step to work on.'))]
for i,y in enumerate([313,415,517],1):
 old=[('1. Collect two useful studies','Suggested block: 10 minutes'),('2. Compare their findings','Suggested block: 15 minutes'),('3. Add one example to your argument','Suggested block: 10 minutes')][i-1]
 rename(old[0],f'Step {i}: edit the action below')
 title=bytext(f'Step {i}: edit the action below');c('widget.bounds',id=title,y=y+7,height=21)
 rename(old[1],'Start this step')
 desc=bytext('Start this step') if i==1 else next(w['id'] for w in ws() if w.get('text')=='Start this step' and w['bounds']['y']==y+46)
 c('widget.bounds',id=desc,x=257,y=y+58,width=126,height=22)
 field=c('widget.create',kind='input',name=f'plan_step_{i}',text='',placeholder='A small action you can do',x=42,y=y+29,width=346,height=29)['id'];c('debug.input_limit',id=field,limit=48)
 load_actions.append({'type':'showGlobalInput','variable':f'TetherStep{i}','widget':field})
 hotspot(f'personalized_start_{i}',250,y+58,142,26,[{'type':'storeGlobal','variable':f'TetherStep{i}','widget':field},{'type':'storeGlobal','variable':'TetherNext','widget':field},{'type':'navigate','page':P['work']}])
# Save all edits when scheduling, even if the student did not start a step.
fields={w['name']:w['id'] for w in ws()}
saves=[{'type':'storeGlobal','variable':f'TetherStep{i}','widget':fields[f'plan_step_{i}']} for i in range(1,4)]
hotspot('personalized_schedule',28,649,374,54,saves+[{'type':'navigate','page':P['schedule']}]);load(load_actions)
open('assignment')
rename('Start with\nthe brief.','What are you\nworking on?')
rename('Paste the key requirements or use the example.','Add a task from any course. Use the example if you want a starting point.')
for w in ws():
 if w['name']=='assignment_title':c('debug.input_limit',id=w['id'],limit=48)
load([{'type':'showGlobalInput','variable':'TetherAssignment','widget':next(w['id'] for w in ws() if w['name']=='assignment_title')},{'type':'showGlobalInput','variable':'TetherBrief','widget':next(w['id'] for w in ws() if w['name']=='assignment_brief')}])
open('review')
rename('Does this match\nyour assignment?','Keep what matters.\nCheck the details.')
rename('Review the example requirements before continuing.','Read your requirements, then edit the suggested steps to fit your task.')
rename('Two or three core journeys','You decide the next steps')
rename('Focus on neurodiverse university learners.','Edit each action before you start.')
rename('Friday, 16:00','Choose a study time next')
rename('Example date for planning this study session.','A short block can be a useful starting point.')
body=next(w['id'] for w in ws() if w['bounds']['y']==345 and w.get('text'));c('widget.bounds',id=body,height=60)
open('dashboard');rename('Coming up: HCI report','Your current assignment');rename('Example deadline: Friday, 16:00','View your steps and choose study time')
rename('One assignment. Three small steps.\nStart with the time you have.','Three editable actions. One place to return.\nChoose a pace that works for you.')
load([show('TetherNext',bytext('Add one example to the\nsecond paragraph.')),show('TetherAssignment',bytext('HCI coursework'))])
open('scheduled');rename('Collect two useful studies\nHCI coursework','Your chosen study block');load([show('TetherStudyTime',bytext('Tomorrow, 09:00\n10 minutes')),show('TetherAssignment',bytext('Your chosen study block'))])
open('desk');rename('HCI coursework  /  Discussion','Your saved study thread')
# Move welcome to the first native sitemap position.
r=c('page.move_first',id=P['welcome']);assert r[0]['Id']==P['welcome'],r
open('welcome');print(c('project.save'));print('Personalized steps saved; welcome is first')
