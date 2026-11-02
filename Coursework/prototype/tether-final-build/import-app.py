import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'bridge-research/native-cli'));import axure_cli as a
def c(op,**kw):
 r=a.request(dict(op=op,**kw));assert r.get('ok'),r;return r['result']
f=(H.parent/'final-coursework.rp').resolve();s=c('status'); c('project.save') if s['project']['dirty'] and Path(s['project']['file'])==f else None
if Path(s['project']['file'])!=f:c('project.open',path=str(f))
existing=c('page.list')['pages'];old={k:p['Id'] for k,p in zip(['desk','work','stuck','pause','saved','completed'],existing[:6])}
manifest=json.loads((H/'app-pages.json').read_text());ids=dict(old)
for p in manifest:
 found=next((x for x in existing if x['Name']==p['name']),None)
 if found:
  ids[p['id']]=found['Id'];c('page.open',id=found['Id'])
  if not c('widget.list'):c('design.import',path=str((H/(p['id']+'.axvg.json')).resolve()));c('project.save')
  continue
 new=c('page.create',name=p['name']);print('create',p['id'],new,flush=True)
 ids[p['id']]=new['page']['Id']
 c('page.open',id=ids[p['id']]);r=c('design.import',path=str((H/(p['id']+'.axvg.json')).resolve()));assert len(r['widgets'])>15
 c('project.save')
(H/'app-page-ids.json').write_text(json.dumps(ids,indent=2))
print('Imported',len(ids),'pages',flush=True)
