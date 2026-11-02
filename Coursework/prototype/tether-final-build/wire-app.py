import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'bridge-research/native-cli'));import axure_cli as a
P=json.loads((H/'app-page-ids.json').read_text())
def c(op,**kw):
 r=a.request(dict(op=op,**kw));assert r.get('ok'),r;return r['result']
def open(k):c('page.open',id=P[k])
def widgets():return c('widget.list')
def text(s):return next(w['id'] for w in widgets() if w.get('text')==s)
def hot(n,y,acts,x=28,w=374,h=54):
 old=next((z for z in widgets() if z['name']=='app_'+n),None)
 if old:return old['id']
 z=c('widget.create',kind='paragraph',name='app_'+n,text='',x=x,y=y,width=w,height=h)['id'];c('interaction.set',id=z,spec={'event':'click','cases':[{'name':n,'actions':acts}]});return z
def go(k):return {'type':'navigate','page':P[k]}
def store(v,s):return {'type':'storeLiteral','variable':v,'value':s}
def inp(n,y,ph,pw=False,h=44):
 old=next((z for z in widgets() if z['name']==n),None)
 if old:return old['id']
 return c('widget.create',kind='input',name=n,text='',placeholder=ph,password=pw,x=38,y=y,width=354,height=h)['id']
def validate(n,y,fields,feedback,acts):
 if any(w['name']=='app_'+n for w in widgets()):return
 z=c('widget.create',kind='paragraph',name='app_'+n,text='',x=28,y=y,width=374,height=54)['id']
 cases=[{'name':'Enter '+label,'when':{'widget':id,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Enter '+label+' to continue.'}]} for label,id in fields]
 cases.append({'name':'Continue','actions':acts});c('interaction.set',id=z,spec={'event':'click','cases':cases})
def load(actions):
 if not c('debug.diagram').get('events'):c('debug.page_load',actions=actions)
def show(v,id):return {'type':'showGlobal','variable':v,'widget':id}
open('dashboard');known={v['name'] for v in c('debug.vars')['variables']}
for v,s in [('TetherStudyTime','Tomorrow, 09:00 - 10 minutes'),('TetherPace','A gentle start'),('TetherAssignment','HCI coursework'),('TetherBrief','Report and prototype for neurodiverse university learners.')]:
 if v not in known:c('debug.var_add',name=v,value=s)
open('welcome')
for n,y,d in [('start',650,'signup'),('login',718,'login'),('demo',795,'dashboard')]:hot(n,y,[go(d)])
open('login');email=inp('login_email',362,'student@example.com');pw=inp('login_password',478,'Demo password',True)
feedback=text('Use the demo account to explore this prototype.')
validate('login',637,[('an email',email),('a demo password',pw)],feedback,[go('dashboard')]);hot('demo',705,[go('dashboard')]);hot('create',780,[go('signup')]);hot('back',92,[go('welcome')],h=30)
open('signup');name=inp('signup_name',345,'Alex');email=inp('signup_email',447,'student@example.com');pw=inp('signup_password',549,'Choose a demo password',True)
validate('signup',696,[('your first name',name),('an email',email),('a demo password',pw)],text('Demo setup only. Use sample details.'),[go('onboarding')]);hot('login',780,[go('login')])
open('onboarding');choice=text('Selected: a gentle start')
for n,y,s in [('light',323,'A gentle start'),('steady',426,'Some room to focus'),('flexible',529,'Flexible study time')]:hot(n,y,[store('TetherPace',s),{'type':'setText','target':choice,'text':'Selected: '+s}],h=84)
hot('continue',714,[go('dashboard')]);hot('skip',786,[go('dashboard')])
open('dashboard');load([show('TetherNext',text('Add one example to the\nsecond paragraph.'))]);hot('resume',261,[go('desk')],h=218);hot('add',741,[go('assignment')]);hot('due',500,[go('plan')],h=84)
open('assignment');title=inp('assignment_title',349,'e.g. HCI coursework');brief=inp('assignment_brief',463,'Paste key requirements',h=80)
for id in [title,brief]:c('debug.input_limit',id=id,limit=120)
validate('review',653,[('an assignment title',title),('the requirements',brief)],text('Check the requirements before building your plan.'),[{'type':'storeGlobal','variable':'TetherAssignment','widget':title},{'type':'storeGlobal','variable':'TetherBrief','widget':brief},go('review')])
hot('example',721,[store('TetherAssignment','HCI coursework'),store('TetherBrief','Report: 2,000-3,000 words; an Axure prototype with 2-3 journeys.'),go('review')]);hot('back',794,[go('dashboard')])
open('review')
c('widget.text',id=text('HCI report and prototype'),text='Assignment requirements')
body=text('Report: 2,000–3,000 words; prototype in Axure.');c('widget.bounds',id=body,height=46,y=345)
load([show('TetherBrief',body)])
hot('build',707,[go('plan')]);hot('edit',781,[go('assignment')])
open('plan');load([show('TetherAssignment',text('HCI coursework · choose a step to work on.'))])
for n,y,s in [('step1',313,'Collect two useful studies.'),('step2',415,'Compare the findings of two studies.'),('step3',517,'Add one example to your argument.')]:hot(n,y,[store('TetherNext',s),go('work')],h=84)
hot('schedule',649,[go('schedule')]);hot('resume',718,[go('desk')])
open('schedule');chosen=text('Selected: tomorrow, 09:00 · 10 minutes')
for n,y,s in [('morning',318,'Tomorrow, 09:00 - 10 minutes'),('afternoon',422,'Tomorrow, 14:00 - 25 minutes'),('evening',526,'Tomorrow, 19:00 - 10 minutes')]:hot(n,y,[store('TetherStudyTime',s),{'type':'setText','target':chosen,'text':'Selected: '+s}],h=84)
load([show('TetherStudyTime',chosen)]);hot('save',713,[go('scheduled')]);hot('back',785,[go('plan')])
open('scheduled');load([show('TetherStudyTime',text('Tomorrow, 09:00\n10 minutes'))]);hot('plan',666,[go('plan')]);hot('change',734,[go('schedule')])
open('settings');load([show('TetherPace',text('Current preference: a gentle start'))]);hot('pace',318,[go('onboarding')],h=84);hot('notes',424,[go('desk')],h=84);hot('logout',710,[go('welcome')])
for k in ['dashboard','plan','scheduled','settings']:
 open(k)
 for i,d in enumerate(['dashboard','plan','settings']):hot('nav_'+d,840,[go(d)],x=24+i*132,w=126,h=54)
# Preserve the working thread flow and add the missing way back into the app.
for k in ['desk','work','stuck','pause','saved','completed']:
 open(k);hot('dashboard',64,[go('dashboard')],x=269,w=135,h=43)
 if k=='work':
  for w in widgets():
   if w.get('text')=='Discussion section':c('widget.text',id=w['id'],text='Your current step')
open('welcome');print(c('project.save'))
print('Wired app shell and core journeys')
