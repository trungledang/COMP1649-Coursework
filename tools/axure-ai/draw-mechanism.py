import json, random
from pathlib import Path
r=random.Random(31)
elements=[]
def element(kind,x,y,w,h,**kw):
    el=dict(id=f'axure-{len(elements)}',type=kind,x=x,y=y,width=w,height=h,angle=0,strokeColor='#243b53',backgroundColor='transparent',fillStyle='solid',strokeWidth=2,strokeStyle='solid',roughness=1,opacity=100,groupIds=[],frameId=None,index=None,roundness={'type':3} if kind=='rectangle' else None,seed=r.randrange(1,2000000000),version=1,versionNonce=r.randrange(1,2000000000),isDeleted=False,boundElements=None,updated=1793440800000,link=None,locked=False)
    el.update(kw); elements.append(el); return el
def text(x,y,w,h,content,size=22,color='#243b53',align='left'):
    return element('text',x,y,w,h,text=content,originalText=content,fontSize=size,fontFamily=2,textAlign=align,verticalAlign='top',containerId=None,autoResize=False,lineHeight=1.25,strokeColor=color,strokeWidth=1)
def box(x,y,w,h,title,body,color):
    element('rectangle',x,y,w,h,backgroundColor=color)
    text(x+18,y+16,w-36,32,title,24)
    text(x+18,y+60,w-36,h-65,body,20)
def arrow(points,color='#526777',dashed=False):
    x,y=points[0]; pts=[[a-x,b-y] for a,b in points]
    element('arrow',x,y,max(a for a,b in pts)-min(a for a,b in pts),max(b for a,b in pts)-min(b for a,b in pts),points=pts,lastCommittedPoint=None,startBinding=None,endBinding=None,startArrowhead=None,endArrowhead='arrow',elbowed=False,strokeColor=color,strokeStyle='dashed' if dashed else 'solid',roundness={'type':2})
text(40,25,1300,58,'AI thiết kế trực tiếp trong Axure như thế nào?',36)
text(40,87,1260,35,'Hai đường tạo phần tử — cùng dùng Axure để lưu file nguồn và chạy prototype.',21,'#526777')
box(40,320,210,150,'YÊU CẦU → AI','Mô tả màn hình,\nnội dung và hành vi.','#e5dbff')
box(350,180,250,160,'1. SINH AXVG','JSON chứa chữ, hình,\nvị trí, màu, kiểu chữ.','#d3f9d8')
box(700,180,250,160,'DÁN VÀO AXURE','Clipboard tên Axvg\n→ Ctrl+V trên canvas.','#d3f9d8')
box(350,460,250,160,'2. GỬI LỆNH CLI','Tạo ô nhập, trang,\nđiều kiện và hành động.','#d0ebff')
box(700,460,250,160,'BRIDGE NỘI BỘ','Nhận lệnh trong Axure,\ngọi hàm chỉnh sửa gốc.','#d0ebff')
box(1040,320,300,150,'PHẦN TỬ AXURE THẬT','Widget, group, ô nhập\nvà tương tác sửa được.','#fff3bf')
box(1040,570,300,205,'AXURE TỰ LƯU / XUẤT','.rp → mở và sửa tiếp\n\nHTML → chạy thử\ntrong trình duyệt','#ffecdf')
arrow([(250,365),(300,365),(300,260),(350,260)])
arrow([(250,425),(300,425),(300,540),(350,540)])
arrow([(600,260),(700,260)])
arrow([(600,540),(700,540)])
arrow([(950,260),(995,260),(995,365),(1040,365)])
arrow([(950,540),(995,540),(995,425),(1040,425)])
arrow([(1190,470),(1190,570)])
text(354,142,540,30,'ĐƯỜNG TẠO PHẦN NHÌN',18,'#2b8a3e')
text(354,421,600,30,'ĐƯỜNG TẠO ĐIỀU KHIỂN VÀ TƯƠNG TÁC',18,'#1864ab')
element('rectangle',40,690,910,145,backgroundColor='#f1f3f5',strokeStyle='dashed',strokeColor='#868e96')
text(60,707,860,32,'COMPUTER USE = TAY & MẮT HỖ TRỢ',23)
text(60,753,860,70,'Dán thiết kế • xem canvas • xử lý phần công cụ chưa hỗ trợ.\nKhông cần kéo thả thủ công từng widget trong bản thử này.',20)
text(40,876,1290,64,'ĐÃ CHẠY TRÊN MÁY ANH: chữ Việt + bố cục + ô nhập + báo lỗi + chuyển trang.\nĐã lưu .rp, đóng hẳn Axure, mở lại và kiểm tra tương tác trong trình duyệt.',20,'#2b8a3e')
text(40,960,1290,32,'Lưu ý: MCP chính thức hiện chỉ đọc; bridge đang ghim theo Axure RP 11.0.0.4150.',18,'#6c757d')
out=Path('E:/Hoc tap/Mon hoc/Năm 3 kì 1/COMP1649_HCI/assets/Axure-AI-pilot-2026-10-31/Co-che-AI-Axure.excalidraw')
out.write_text(json.dumps({'type':'excalidraw','version':2,'source':'https://excalidraw.com','elements':elements,'appState':{'viewBackgroundColor':'#ffffff','gridSize':None},'files':{}},ensure_ascii=False),encoding='utf-8')
print(out)
