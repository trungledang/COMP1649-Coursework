import {writeFileSync} from 'node:fs';
import {rect,text,frame,composeDesign,hex} from './axvg-build.ts';
const box=(x,y,w,h,color,corners=0)=>rect({x,y,w,h,fill:hex(color),corners});
const label=(x,y,w,h,content,size=16,color='#172C29',weight=400)=>text({x,y,w,h,content,size,color:hex(color),weight});
const design=composeDesign(frame({name:'Không gian học tập',w:1100,h:720,bg:hex('#F7F7F2'),children:[
box(0,0,390,720,'#153E36'),
label(48,48,290,32,'MỞ / KHÔNG GIAN HỌC',15,'#D6E9A3',700),
label(48,182,300,116,'Một ý tưởng.\nNhiều khả năng.',36,'#FFFFFF',700),
label(48,332,290,90,'Từ phác thảo đến prototype.\nTừng phần tử đều có thể sửa\nngay trong Axure.',17,'#D5E3DC'),
box(48,565,294,1,'#52736A'),
label(48,594,290,52,'01 / BẢN THỬ TẠO THIẾT KẾ\nAxvg + Axure RP 11',13,'#D5E3DC'),
box(454,92,582,524,'#FFFFFF',20),
label(502,136,470,26,'BẮT ĐẦU HÀNH TRÌNH',13,'#547B56',700),
label(502,183,470,54,'Chào bạn, bắt đầu nhé.',30,'#172C29',700),
label(502,251,470,48,'Giao diện được tạo bằng dữ liệu có cấu trúc,\nsau đó chuyển thành phần tử Axure.',16,'#64756E'),
label(502,332,460,24,'Tên của bạn',14,'#172C29',500),
box(502,374,470,52,'#F4F6F2',8),
label(518,390,430,26,'Ví dụ: Trung',15,'#7B8781'),
box(502,456,470,52,'#153E36',8),
label(502,473,470,24,'Tiếp tục  →',15,'#FFFFFF',700),
label(502,552,470,26,'Bản thử giao diện • Các chữ và hình đều sửa được',12,'#64756E'),
label(454,658,582,24,'TẠO BẰNG AXVG  /  LƯU BẰNG AXURE  /  CHỈNH SỬA TỪNG PHẦN',11,'#64756E'),
]}));
writeFileSync(new URL('./design.axvg.json', import.meta.url),'// axvg\n'+JSON.stringify(design));
