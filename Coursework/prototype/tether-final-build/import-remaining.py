import json, os, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'tools/axure-ai/native-cli'))
os.environ['REVERSE_CLI_CACHE_DIR']='E:/ai-cache/axure-pilot/cache'
import axure_cli as ax

def axcall(op,**kw):
    r=ax.request(dict(op=op,**kw))
    if not r.get('ok'): raise RuntimeError(r)
    return r['result']
def gui(*args):
    p=subprocess.run(['orca','computer',*args,'--json'],capture_output=True,encoding='utf-8-sig',errors='replace')
    if p.returncode: raise RuntimeError(p.stderr or p.stdout)
    r=json.loads(p.stdout)
    if not r.get('ok'):raise RuntimeError(r)
def clipboard(path):
    p=subprocess.run(['powershell','-NoProfile','-STA','-File',str(ROOT/'tools/axure-ai/axvg/set-axvg-clipboard.ps1'),'-Path',str(path)],capture_output=True,encoding='utf-8-sig',errors='replace')
    if p.returncode:raise RuntimeError(p.stderr)

pages=axcall('page.list')['pages']
assert len(pages)==5
out=Path(__file__).resolve().parent
for page,key in zip(pages[1:],['work','stuck','pause','saved']):
    axcall('page.open',id=page['Id'])
    gui('click','--app','pid:20620','--x','1070','--y','540')
    gui('hotkey','--app','pid:20620','--key','Ctrl+A')
    gui('press-key','--app','pid:20620','--key','Delete')
    if axcall('widget.list'): raise RuntimeError('Old widgets remain on '+key)
    clipboard(out/(key+'.axvg.json'))
    gui('hotkey','--app','pid:20620','--key','Ctrl+V')
    ws=axcall('widget.list')
    if len(ws)<10 or ws[0]['name']!='Tether '+key:raise RuntimeError('Unexpected paste '+key)
    gui('click','--app','pid:20620','--x','1295','--y','165')
    gui('hotkey','--app','pid:20620','--key','Ctrl+A')
    gui('type-text','--app','pid:20620','--text','0')
    gui('press-key','--app','pid:20620','--key','Return')
    ws=axcall('widget.list')
    if ws[0]['bounds']['x']!=0:raise RuntimeError('Unexpected x offset '+key)
    print(key,len(ws),flush=True)
    axcall('project.save')
print('Imported and saved four pages.')
