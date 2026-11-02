import sys,json
from pathlib import Path
H=Path('Coursework/prototype/tether-final-build');sys.path.insert(0,str((H/'bridge-research/native-cli').resolve()));import axure_cli as a
P=json.loads((H/'app-page-ids.json').read_text())
def c(op,**kw):
 r=a.request(dict(op=op,**kw));assert r.get('ok'),r;return r['result']
def open(k):c('page.open',id=P[k])
def ws():return c('widget.list')
def name(s):return next(w['id'] for w in ws() if w['name']==s)
def act(id,actions,event='click',cases=None):c('interaction.set',id=id,replace=True,spec={'event':event,'cases':cases or [{'name':'Continue','actions':actions}]})
f=(H.parent/'final-coursework.rp').resolve();c('project.open',path=str(f));open('assignment');title=name('assignment_title');old=next(w['id'] for w in ws() if w['name']=='legacy_hidden_input')
brief=name('assignment_brief')
c('debug.page_load',replace=True,actions=[{'type':'showGlobalInput','variable':'TetherDraftAssignment','widget':title},{'type':'showGlobalInput','variable':'TetherDraftBrief','widget':brief}])
feedback=next(w['id'] for w in ws() if w.get('text')=='Check the requirements before building your plan.')
act(brief,[{'type':'setText','target':feedback,'text':'Check the requirements before building your plan.'}],event='change')
cases=[{'name':'Enter title','when':{'widget':title,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Enter an assignment title first.'}]},{'name':'Enter requirements','when':{'widget':brief,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Add the key requirements first.'}]},{'name':'Review','actions':[{'type':'storeGlobal','variable':'TetherDraftAssignment','widget':title},{'type':'storeGlobal','variable':'TetherDraftBrief','widget':brief},{'type':'navigate','page':P['review']}]}]
act(name('app_review'),[],cases=cases)
open('review');oldbody=next(w['id'] for w in ws() if w['bounds']['y']==345 and w.get('text'));c('widget.text',id=oldbody,text='')
review=c('widget.textarea',name='review_requirements',placeholder='Your key requirements',x=42,y=352,width=346,height=42)['id'];c('widget.style_basic',id=review)
c('debug.page_load',replace=True,actions=[{'type':'showGlobalInput','variable':'TetherDraftBrief','widget':review}]);act(review,[{'type':'storeGlobal','variable':'TetherDraftBrief','widget':review}],event='change')
open('welcome');print(c('project.save'));c('project.new');c('project.open',path=str(f));c('export.html',output=str((H/'final-preview-v4').resolve()));print('Multiline native controls exported')
