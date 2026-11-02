from pilot import *
before=call('widget.list')
assert len(before)==19 and before[0]['type'].endswith('.Layer')
page=call('page.list')['activeId']
success=call('page.create',name='Hoàn tất')['page']['Id']
call('page.open',id=success)
widget('paragraph','success_title','Chào mừng bạn! Prototype đã hoạt động.',160,160,650,60)
widget('paragraph','success_note','Bố cục Axvg + ô nhập và tương tác gốc của Axure.',160,240,650,50)
back=widget('button','back','Quay lại',160,330,200,48)
call('interaction.set',id=back,spec={'event':'click','cases':[{'actions':[{'type':'navigate','page':page}]}]})
call('page.open',id=page)
placeholder=next(w for w in before if w['text']=='Ví dụ: Trung')
call('widget.text',id=placeholder['id'],text='')
name=widget('input','name_input','',518,384,438,32,placeholder='Ví dụ: Trung')
feedback=widget('paragraph','feedback','',502,515,470,28)
spec={'event':'click','cases':[
 {'name':'Tên còn trống','when':{'widget':name,'equals':''},'actions':[{'type':'setText','target':feedback,'text':'Bạn hãy nhập tên trước khi tiếp tục.'}]},
 {'name':'Tiếp tục','actions':[{'type':'navigate','page':success}]}]}
button=next(w for w in before if w['bounds']=={'x':502,'y':456,'width':470,'height':52})
button_text=next(w for w in before if w['text']=='Tiếp tục  →')
for item in (button,button_text): call('interaction.set',id=item['id'],spec=spec)
widgets=call('widget.list')
path=str(OUT/'Axure-designed-pilot.rp')
call('project.save',path=path)
call('export.html',output=str(OUT/'html-designed'))
metadata={'page':page,'success':success,'name':name,'feedback':feedback,'button':button['id'],'buttonText':button_text['id'],'back':back,'widgets':widgets}
(OUT/'designed-ids.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
call('project.close')
result=ax.launch(path)
assert result['ok'],result
assert call('widget.list')==widgets, 'Styled widget data changed on cold reopen'
assert len(call('interaction.get',id=button['id'])['events'])==1
(OUT/'designed-cold-reopen.json').write_text(json.dumps({'ok':True,'launch':result,'widgetCount':len(widgets)},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'ok':True,'path':path,'widgetCount':len(widgets),'pid':ax.endpoint()['pid']},ensure_ascii=False))
