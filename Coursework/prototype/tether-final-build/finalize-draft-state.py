import sys,json
from pathlib import Path
H=Path('Coursework/prototype/tether-final-build');sys.path.insert(0,str((H/'bridge-research/native-cli').resolve()));import axure_cli as a
P=json.loads((H/'app-page-ids.json').read_text())
def c(op,**kw):
 r=a.request(dict(op=op,**kw));assert r.get('ok'),r;return r['result']
def open(k):c('page.open',id=P[k])
def ws():return c('widget.list')
def name(s):return next(w['id'] for w in ws() if w['name']==s)
def text(s):return next(w['id'] for w in ws() if w.get('text')==s)
def act(id,actions,cases=None):c('interaction.set',id=id,replace=True,spec={'event':'click','cases':cases or [{'name':'Continue','actions':actions}]})
def store(v,s):return {'type':'storeLiteral','variable':v,'value':s}
def go(k):return {'type':'navigate','page':P[k]}
open('dashboard');known={v['name'] for v in c('debug.vars')['variables']}
for v in ['TetherDraftAssignment','TetherDraftBrief']:
 if v not in known:c('debug.var_add',name=v,value='')
act(name('app_add'),[store('TetherDraftAssignment',''),store('TetherDraftBrief',''),go('assignment')])
open('assignment');title=name('assignment_title');brief=name('assignment_brief');feedback=text('Check the requirements before building your plan.')
c('debug.page_load',replace=True,actions=[{'type':'showGlobalInput','variable':'TetherDraftAssignment','widget':title},{'type':'showGlobalInput','variable':'TetherDraftBrief','widget':brief}])
cases=[{'name':'Enter a title','when':{'widget':title,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Enter an assignment title first.'}]},{'name':'Enter requirements','when':{'widget':brief,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Add the key requirements first.'}]},{'name':'Review draft','actions':[{'type':'storeGlobal','variable':'TetherDraftAssignment','widget':title},{'type':'storeGlobal','variable':'TetherDraftBrief','widget':brief},go('review')]}]
act(name('app_review'),[],cases)
act(name('app_example'),[store('TetherDraftAssignment','HCI coursework'),store('TetherDraftBrief','Report: 2,000-3,000 words; an Axure prototype with 2-3 journeys.'),go('review')])
open('review');body=next(w['id'] for w in ws() if w['bounds']['y']==345 and w.get('text'))
c('debug.page_load',replace=True,actions=[{'type':'showGlobal','variable':'TetherDraftBrief','widget':body}])
reset=[{'type':'copyGlobal','variable':'TetherAssignment','source':'TetherDraftAssignment'},{'type':'copyGlobal','variable':'TetherBrief','source':'TetherDraftBrief'},store('TetherWhere','Ready to start this assignment.'),store('TetherNext','Identify the main requirements.'),store('TetherStep1','Identify the main requirements.'),store('TetherStep2','Find two useful sources.'),store('TetherStep3','Draft one paragraph.'),store('TetherStudyTime','Tomorrow, 09:00 - 10 minutes'),go('plan')]
act(name('app_build'),reset)
open('schedule');c('widget.text',id=text('Tomorrow, 09:00'),text='Suggested: tomorrow, 09:00')
open('onboarding');c('widget.text',id=text('A gentle start'),text='Suggested: a gentle start')
open('welcome');print(c('project.save'))
c('project.new');c('project.open',path=str((H.parent/'final-coursework.rp').resolve()));c('export.html',output=str((H/'final-preview-app').resolve()));print('Final export ready')
