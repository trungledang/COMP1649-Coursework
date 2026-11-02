import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'bridge-research/native-cli'));import axure_cli as a
P=json.loads((H/'app-page-ids.json').read_text())
def c(op,**kw):
 r=a.request(dict(op=op,**kw));assert r.get('ok'),r;return r['result']
def open(k):c('page.open',id=P[k])
def ws():return c('widget.list')
def named(n):return next(w['id'] for w in ws() if w['name']==n)
def txt(t):return next(w['id'] for w in ws() if w.get('text')==t)
def rename(old,new):
 f=next((w for w in ws() if w.get('text')==old),None)
 if f:c('widget.text',id=f['id'],text=new)
def install(id,actions,event='click',cases=None):c('interaction.set',id=id,replace=True,spec={'event':event,'cases':cases or [{'name':'Continue','actions':actions}]})
def load(actions):c('debug.page_load',replace=True,actions=actions)
def go(k):return {'type':'navigate','page':P[k]}
def store(v,s):return {'type':'storeLiteral','variable':v,'value':s}
def show(v,id):return {'type':'showGlobal','variable':v,'widget':id}
f=(H.parent/'final-coursework.rp').resolve();c('project.open',path=str(f))
# Apply the verified native input style; retain visible native focus feedback.
for k in ['login','signup','assignment','plan','pause']:
 open(k)
 for w in ws():
  if w['type'].endswith('.TextBox'):c('widget.style_basic',id=w['id'])
# Plan edits save as they are typed. Every way of starting a row uses the current field.
open('plan')
fields={i:named(f'plan_step_{i}') for i in range(1,4)}
saves=[{'type':'storeGlobal','variable':f'TetherStep{i}','widget':fields[i]} for i in range(1,4)]
for i,y in enumerate([290,406,522],1):
 field=fields[i];install(field,[{'type':'storeGlobal','variable':f'TetherStep{i}','widget':field}],event='change')
 actions=saves+[{'type':'storeGlobal','variable':'TetherNext','widget':field},go('work')]
 cases=[{'name':'Add an action','when':{'widget':field,'equals':''},'actions':[{'type':'setText','target':txt(f'Step {i}: edit the action below'),'text':'Add a small action first.'}]},{'name':'Start current action','actions':actions}]
 install(named(f'app_step{i}'),actions,cases=cases);install(named(f'personalized_start_{i}'),actions,cases=cases)
 c('widget.bounds',id=named(f'step{i}'),y=y,height=110)
 label=txt(f'Step {i}: edit the action below');c('widget.bounds',id=label,y=y+5,height=20)
 c('widget.bounds',id=field,y=y+26,height=40)
 link=next(w['id'] for w in ws() if w.get('text')=='Start this step' and 300+i*100-110 < w['bounds']['y'] < 400+i*100-110)
 c('widget.bounds',id=link,y=y+79,height=24)
 c('widget.bounds',id=named(f'personalized_start_{i}'),y=y+66,height=44)
for n,d in [('app_nav_dashboard','dashboard'),('app_nav_settings','settings'),('app_resume','desk'),('app_schedule','schedule'),('personalized_schedule','schedule')]:install(named(n),saves+[go(d)])
# A fresh plan is created only on explicit confirmation.
open('review');rename('Confirm and build my plan','Confirm and edit my steps')
rename('Read your requirements, then edit the suggested steps to fit your task.','Check the requirements. The next screen has starter steps for you to edit.')
reset=[store('TetherWhere','Ready to start this assignment.'),store('TetherNext','Identify the main requirements.'),store('TetherStep1','Identify the main requirements.'),store('TetherStep2','Find two useful sources.'),store('TetherStep3','Draft one paragraph.')]
install(named('app_build'),reset+[go('plan')])
# Restore the real preference on revisit.
open('onboarding');choice=txt('Selected: a gentle start');load([show('TetherPace',choice)])
rename('Choose a starting point. You can change it later.','Choose a starting preference. You can pick study times separately.')
# Clear stale validation feedback when the student edits a field.
for k,names,feedback,normal in [
('login',['login_email','login_password'],'Use the demo account to explore this prototype.','Use sample details. Sign-in is simulated.'),
('signup',['signup_name','signup_email','signup_password'],'Demo setup only. Use sample details.','Demo setup only. Use sample details.'),
('assignment',['assignment_title','assignment_brief'],'Check the requirements before building your plan.','Check the requirements before building your plan.'),
('pause',['where_stopped','next_move'],'Keep each note under 48 characters.','Keep each note under 48 characters.')]:
 open(k);target=txt(feedback)
 for name in names:install(named(name),[{'type':'setText','target':target,'text':normal}],event='change')
# Make the dashboard link on focus screens discoverable.
for k in ['desk','work','stuck','pause','saved','completed']:
 open(k)
 heading=next(w for w in ws() if w['bounds']['x']==273 and w['bounds']['y']==74)
 c('widget.text',id=heading['id'],text='My study desk')
# Avoid clipping the assignment name inside the resume card at the maximum input length.
open('dashboard');title=next(w for w in ws() if w['bounds']['y']==321 and w.get('text'))
c('widget.bounds',id=title['id'],height=62);body=next(w for w in ws() if w['bounds']['y']==367 and w.get('text'));c('widget.bounds',id=body['id'],y=385,height=43)
open('welcome');print(c('project.save'));print('Usability fixes committed')
