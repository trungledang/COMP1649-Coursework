# Bản thử thiết kế trực tiếp trong Axure

- `Axure-designed-pilot.rp`: bản có bố cục và màu sắc, 2 trang; trang đầu có 21 phần tử (bao gồm group), chữ/hình sửa được, ô nhập gốc và nút chuyển trang.
- `Axure-native-pilot.rp`: bản kiểm tra kỹ thuật bằng CLI, có báo lỗi ô trống, nhập lại và chuyển trang.
- `designed-preview.png`: ảnh chụp thật từ HTML do Axure xuất.
- `html-designed/`, `html/`: HTML xuất bằng bộ sinh gốc của Axure; không sửa HTML để thêm chức năng.
- `native-evidence.jsonl`, `designed-cold-reopen.json`, `browser-evidence/`: bằng chứng kiểm tra.

Đã kiểm tra ngày 2026-10-31: tạo widget, lưu .rp, đóng hẳn phiên Axure do thử nghiệm mở, mở lại giữ nguyên ID/nội dung/tọa độ và tương tác. Trình duyệt chạy đúng báo lỗi ô trống, nhập tên -> chuyển trang, quay lại; bản CLI có thêm nút nhập lại đã kiểm tra.

Đây là mẫu xác nhận cách tự động hóa, chưa phải thiết kế sản phẩm theo yêu cầu cụ thể. Ô nhập của bản có thiết kế vẫn dùng kiểu mặc định của Axure. Dynamic panel và adaptive view chưa được thử.

## Công cụ dùng lại

Mã nguồn thử nghiệm và runtime nằm ở `E:/Hoc tap/Mon hoc/Năm 3 kì 1/COMP1649_HCI/tools/axure-ai/`.
Bridge dùng bản gốc reverse-cli-anything, chỉ đổi cách chọn đường dẫn app trong axure_cli.py sang E:/AxureRP11.exe. PowerShell 7.6.9 portable ở thư mục pwsh/, không thay cấu hình hệ thống. Cache ở ổ E:.

Nguồn:
- https://github.com/leileqiTHU/reverse-cli-anything/tree/main/axure-cli (MIT)
- https://github.com/FD-design/YPAxure (Axvg builders/clipboard; chưa thấy license công bố)

Không cần cài extension trình duyệt khi chạy HTML qua máy chủ HTTP nội bộ. Khi muốn xem lại từ trình duyệt, có thể chạy:

```powershell
python -m http.server 18766 --bind 127.0.0.1 --directory E:/Hoc tap/Mon hoc/Năm 3 kì 1/COMP1649_HCI/assets/Axure-AI-pilot-2026-10-31
```

Rồi mở http://127.0.0.1:18766/html-designed/page_1.html . File .rp mở trực tiếp bằng Axure.

Runtime PowerShell portable vẫn ở E:/ai-cache/axure-pilot/pwsh/. Hướng dẫn hiện hành: ../../tools/axure-ai/README.md .
