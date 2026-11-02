# Prompt dán vào OpenCode (chạy 2 script cải thiện)

Mở OpenCode **trong thư mục môn học** (`E:\Hoc tap\Mon hoc\Năm 3 kì 1\COMP1649_HCI`), rồi dán nguyên khối dưới đây:

---

```text
Trong thư mục môn học COMP1649_HCI này, hãy chạy 2 script cải thiện prototype Axure. Làm đúng thứ tự, dừng lại và báo tôi nếu bước nào lỗi. Không tự sửa script, không xóa file nào.

1. Lấy code mới: nếu đây là git repo thì `git fetch origin` rồi `git checkout claude/brave-ramanujan-p2hvb2` rồi `git pull`. Nếu không phải git repo thì dừng và báo tôi.
2. Kiểm tra các file sau có tồn tại:
   - Coursework/prototype/final-coursework.rp
   - Coursework/prototype/tether-final-build/improve-plan-brief.py
   - Coursework/prototype/tether-final-build/improve-nav-me.py
   - Coursework/prototype/tether-final-build/app-page-ids.json
3. Copy Coursework/prototype/final-coursework.rp thành Coursework/prototype/final-coursework.backup.rp (nếu chưa có file backup này).
4. Hỏi tôi đã đóng hết cửa sổ Axure đang mở final-coursework.rp chưa. Chỉ làm tiếp khi tôi xác nhận.
5. Khởi động Axure có bridge, dùng ĐÚNG bản CLI trong bridge-research (các script dùng bản này):
   & "Coursework/prototype/tether-final-build/bridge-research/native-cli/axure-cli.ps1" launch --app E:/AxureRP11.exe
   Nếu báo thiếu bridge DLL thì chạy build bằng PowerShell 7 rồi launch lại:
   & 'E:/ai-cache/axure-pilot/pwsh/pwsh.exe' -NoProfile -File "Coursework/prototype/tether-final-build/bridge-research/native-cli/build.ps1"
   Sau đó chạy `... axure-cli.ps1 status` và đợi tới khi status báo ok.
6. Chạy lần lượt (đứng ở thư mục môn học):
   & 'E:/Runtimes/python312-3.12.14/python.exe' Coursework/prototype/tether-final-build/improve-plan-brief.py
   & 'E:/Runtimes/python312-3.12.14/python.exe' Coursework/prototype/tether-final-build/improve-nav-me.py
   Đặt biến môi trường PYTHONIOENCODING=utf-8 trước khi chạy.
7. Báo lại cho tôi TOÀN BỘ output của 2 script (kể cả lỗi), nguyên văn.
8. Xuất HTML mới để kiểm tra (thư mục phải chưa tồn tại):
   & "Coursework/prototype/tether-final-build/bridge-research/native-cli/axure-cli.ps1" export html --output "Coursework/prototype/tether-final-build/final-preview-v5"
   Rồi chạy `python -m http.server 18800 --bind 127.0.0.1` trong thư mục final-preview-v5, mở 04_today.html và 07_your_plan.html, xác nhận: thanh dưới ghi "Me" thay cho "Settings", và trang Plan có thêm dòng đề bài ở cuối (trên thanh dưới). Tắt server sau khi xong.

Không commit, không push. Không đóng tiến trình Axure nào khác ngoài phiên bạn vừa launch, và chỉ đóng sau khi project đã lưu.
```

---

Lưu ý:
- OpenCode dùng model và hạn mức của chính nó, không dùng credit Claude cloud.
- Có lỗi thì dán output vào chat Claude để sửa script.
