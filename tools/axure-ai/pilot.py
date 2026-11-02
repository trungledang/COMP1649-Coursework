import sys, json, os, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'native-cli'))
os.environ['REVERSE_CLI_CACHE_DIR'] = str(ROOT/'cache')
import axure_cli as ax
OUT = Path(os.environ.get('AXURE_PILOT_OUTPUT', str(ROOT / 'runs' / time.strftime('%Y%m%d-%H%M%S'))))
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT/'native-evidence.jsonl'
def call(op, **kw):
    result = ax.request(dict(op=op, **kw))
    with LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(dict(op=op, response=result), ensure_ascii=False)+'\n')
    if not result.get('ok'): raise RuntimeError(result)
    return result['result']
def widget(kind, name, text, x, y, w, h, **kw):
    return call('widget.create', kind=kind, name=name, text=text, x=x, y=y, width=w, height=h, **kw)['id']
def build():
    status=call('status')
    assert not status['project']['dirty'], 'Do not replace an unsaved document'
    pages=call('page.list')
    login=pages['activeId']
    success=call('page.create', name='Hoàn tất')['page']['Id']
    call('page.open', id=success)
    widget('paragraph','success_heading','Đã tạo prototype thành công',160,160,620,55)
    widget('paragraph','success_note','File .rp này có widget và tương tác gốc của Axure. Bạn có thể chỉnh sửa từng phần tử.',160,230,600,65)
    back=widget('button','back','Quay lại',160,330,220,48)
    call('interaction.set', id=back, spec={'event':'click','cases':[{'name':'Về trang nhập','actions':[{'type':'navigate','page':login}]}]})
    call('page.open', id=login)
    widget('paragraph','eyebrow','AXURE / THỬ NGHIỆM TẠO FILE',160,80,620,30)
    widget('paragraph','heading','Chào bạn, bắt đầu nhé.',160,130,620,55)
    widget('paragraph','description','Nhập tên để kiểm tra ô nhập, báo lỗi và chuyển trang.',160,195,620,35)
    widget('paragraph','name_label','Tên của bạn',160,260,400,25)
    name=widget('input','name_input','',160,300,420,48,placeholder='Ví dụ: Trung')
    feedback=widget('paragraph','feedback','',160,365,580,36)
    submit=widget('button','continue','Tiếp tục',160,425,260,48)
    reset=widget('button','reset','Nhập lại',440,425,140,48)
    widget('paragraph','footer','Bản thử kỹ thuật • Dữ liệu chỉ dùng trong prototype',160,530,620,32)
    call('interaction.set', id=submit, spec={'event':'click','cases':[
      {'name':'Tên còn trống','when':{'widget':name,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Bạn hãy nhập tên trước khi tiếp tục.'}]},
      {'name':'Mở trang hoàn tất','actions':[{'type':'navigate','page':success}]}]})
    call('interaction.set', id=reset, spec={'event':'click','cases':[{'name':'Xóa nội dung','actions':[{'type':'setText','target':name,'text':''},{'type':'setText','target':feedback,'text':''}]}]})
    metadata={'login':login,'success':success,'name':name,'feedback':feedback,'submit':submit,'reset':reset,'back':back}
    (OUT/'ids.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    before=call('widget.list')
    call('project.save', path=str(OUT/'Axure-native-pilot.rp'))
    call('export.html',output=str(OUT/'html'))
    call('project.new')
    call('project.open',path=str(OUT/'Axure-native-pilot.rp'))
    call('page.open',id=login)
    after=call('widget.list')
    assert before==after, 'Widget data changed after native reopen'
    assert call('interaction.get',id=submit)['events'], 'Missing interaction after reopen'
    print(json.dumps({'ok':True,'output':str(OUT),'widgets':len(after),'nativeReopen':True},ensure_ascii=False))
if __name__=='__main__': build()
