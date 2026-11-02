# Axure AI — hướng dẫn dùng lại cho Claude, Codex và AI khác

Updated: 2026-10-31. Đây là bộ đã chạy trên máy Windows hiện tại, không phải hướng dẫn suy đoán. Đọc file này trước khi tiếp tục làm Axure. Không cần MCP hoặc plugin riêng của một hãng AI: cần khả năng chạy Python/PowerShell; thao tác dán và kiểm tra hình cần computer use hoặc người dùng.

Bộ cũ `../axure-native` đã được đưa vào Thùng rác theo yêu cầu người dùng ngày 2026-10-31. Bộ này là hướng mặc định cho công việc mới. Các prototype/bài tập cũ được giữ nguyên. Việc gỡ bộ cũ là lựa chọn quy trình, không phải kết quả đo chứng minh bộ mới bao phủ mọi tính năng: luồng biến toàn cục của StudyFlow cũ chưa được tái tạo bằng bộ mới.

## Vị trí chuẩn

- File môn học và ảnh/sơ đồ/bằng chứng: `../../assets/Axure-AI-pilot-2026-10-31/`.
- Bộ công cụ hiện hành: thư mục chứa README này. Các bản mã trong `E:/ai-cache/axure-pilot` là bản lịch sử của lần thử; chỉ runtime/cache vẫn dùng ở đó.
- Axure app: `E:/AxureRP11.exe`, library `E:/AxureRP11.dll`.
- Python: `E:/Runtimes/python312-3.12.14/python.exe`.
- PowerShell 7.6.9 portable: `E:/ai-cache/axure-pilot/pwsh/pwsh.exe`.
- Node: trên PATH (đã chạy Node 26.13.0, hỗ trợ chạy TypeScript trực tiếp).

## Cơ chế và cách chọn

1. **Axvg cho phần nhìn:** `axvg/axvg-build.ts` có builder rect/text/frame/composeDesign. Sinh JSON bắt đầu bằng `// axvg\n`, ghi vào định dạng clipboard tên `Axvg` bằng `axvg/set-axvg-clipboard.ps1`. Dán Ctrl+V trong canvas: Axure dựng group, hình và chữ có thể sửa. `axvg/create-design.mjs` là mẫu thực tế, chạy bằng Node; không cần qua Figma. Đây mới là phần nhìn: hình ô nhập và nút vẽ bằng Axvg chưa tự có chức năng nhập/bấm.
2. **Native CLI cho hành vi:** `native-cli/axure_cli.py` gửi JSON qua named pipe chỉ cho Windows user hiện tại. Bridge C# được nạp bằng DOTNET_STARTUP_HOOKS vào một phiên Axure riêng; gọi hàm chỉnh sửa của Axure trên UI thread, dùng transaction/undo, bộ lưu .rp và bộ xuất HTML gốc. Tạo ô nhập thật, trang, điều kiện và hành động rồi ghép vào layout Axvg.
3. **Computer use cho dán/quan sát/phần chưa hỗ trợ:** sau dán phải inspect/readback rồi xem screenshot thực tế. Cây accessibility của Axure rất nông. Orca --restore-window từng không đưa cửa sổ lên trước; một ảnh bị Edge che đã được loại khỏi bằng chứng. AppActivate đúng PID của phiên thử nghiệm rồi capture lại đã hoạt động.
4. **MCP chính thức:** chỉ đọc theo tài liệu đã kiểm tra 2026-10-31; không thay thế đường ghi trên.

## Chạy CLI trên máy này

Trong PowerShell, dùng đường dẫn có dấu cách bằng biến và dấu nháy:

```powershell
$kit = 'E:/Hoc tap/Mon hoc/Năm 3 kì 1/COMP1649_HCI/tools/axure-ai'
$env:REVERSE_CLI_CACHE_DIR = 'E:/ai-cache/axure-pilot/cache'
# Chỉ build lại khi thiếu bridge hoặc đổi source; đã build tại vị trí mới.
& 'E:/ai-cache/axure-pilot/pwsh/pwsh.exe' -NoProfile -File "$kit/native-cli/build.ps1"
& "$kit/native-cli/axure-cli.ps1" capabilities
& "$kit/native-cli/axure-cli.ps1" launch --app E:/AxureRP11.exe
& "$kit/native-cli/axure-cli.ps1" status
& "$kit/native-cli/axure-cli.ps1" widget list
```

Đã chạy build và capabilities thành công tại vị trí mới. Launch/edit/save/cold-reopen đã chạy trước khi chuyển tài liệu; không mở thêm phiên Axure chỉ để kiểm tra việc sắp xếp file. `status` báo NO_BRIDGE trước launch là bình thường. Phiên mở bằng shortcut hoặc bridge cũ trong cache không thuộc endpoint của bộ công cụ mới. Không đóng phiên có việc chưa lưu của người dùng để kết nối bridge; launch một phiên riêng.

```powershell
& "$kit/native-cli/axure-cli.ps1" widget create --kind input --name name --placeholder 'Tên của bạn' --x 100 --y 200 --width 320 --height 48
& "$kit/native-cli/axure-cli.ps1" widget create --kind button --name next --text 'Tiếp tục' --x 100 --y 280 --width 320 --height 48
# Dùng ID thật từ kết quả CLI; các path ví dụ dưới phải là đầu ra MỚI.
& "$kit/native-cli/axure-cli.ps1" project save --path 'E:/duong-dan-moi/prototype.rp'
& "$kit/native-cli/axure-cli.ps1" export html --output 'E:/duong-dan-moi/html'
```

Ví dụ JSON tương tác trong `finish-designed.py`: ô nhập trống -> setText feedback; nhánh còn lại -> navigate page ID. `interaction set --id <GUID> --spec <absolute-json-path>` cài tương tác, `interaction get --id <GUID>` đọc lại cây thật. Không dùng ID minh họa như ID thật.

## Axvg và ví dụ tái tạo

```powershell
node "$kit/axvg/create-design.mjs"
powershell -NoProfile -STA -File "$kit/axvg/set-axvg-clipboard.ps1" -Path "$kit/axvg/design.axvg.json"
```

Sau đó chọn canvas trong đúng phiên Axure thử nghiệm và Ctrl+V. Đọc `inspect`/`widget list` để biết vị trí thực tế trước khi đặt ô nhập/interaction. Trong lần thử, root group ở (0,0), chữ và hình đúng tọa độ. Clipboard được thay bằng dữ liệu thiết kế trong thao tác này.

- `pilot.py`: tạo bản native-only; mặc định đầu ra mới trong `runs/<timestamp>`. Có thể đặt `AXURE_PILOT_OUTPUT` thành thư mục mới. Chỉ chạy khi đúng phiên thử nghiệm đang active, đã sạch/đã lưu; script sẽ chuyển document đang active trong phiên bridge.
- `finish-designed.py`: **chỉ chạy sau** khi đã dán đúng mẫu Axvg vào một document trống riêng; nó kiểm tra 19 đối tượng đầu vào, thêm input và tương tác, lưu/xuất/cold-reopen. Đặt `AXURE_PILOT_OUTPUT` giống lần chạy đang làm. Đây là script tái tạo mẫu, không phải lệnh sửa một project bất kỳ.
- `draw-mechanism.py`: nguồn tạo sơ đồ `.excalidraw`; đổi output nếu muốn giữ bản cũ.
- `migration-evidence.json`: SHA256 của 293 file ở thời điểm chuyển từ Downloads vào thư mục môn. README được cập nhật đường dẫn sau đối chiếu này.

## Bằng chứng, phạm vi và lỗi cần tránh

Đã kiểm tra native .rp đóng hẳn app rồi mở lại; ID/text/bounds giữ nguyên. Hai mẫu có 2 trang; mẫu thiết kế có 21 đối tượng ở trang đầu (gồm group), nhập tên/báo lỗi/chuyển trang/quay lại chạy trong HTML gốc. Mẫu native-only thêm reset input/feedback. Ảnh `designed-preview.png` là ảnh thực tế; toàn bộ log nằm cạnh .rp. Không sửa HTML xuất để giả lập hành vi.

Bridge **ghim đúng** Axure 11.0.0.4150 và SHA256 DLL `dae5748f6be3e69c063ef117bab0b400586d94adf119f5a9ba260df59dc4e4a7`. App update thì kiểm tra lại entrypoint; không bỏ kiểm tra hash để ép chạy. PowerShell 5.1 không thay PowerShell 7.6 để build bridge.

Chỉ hỗ trợ paragraph/vector, button, input, bounds/text và click với equals/any/all, setText/navigation trong phạm vi đã thử. Có thể gắn click lên hình/text Axvg. Chưa nghiệm thu dynamic panel, adaptive view, phức tạp rich text hoặc thay tùy ý tương tác đã có. interaction set từ chối map không rỗng. SaveAs từ chối ghi đè file khác; export yêu cầu thư mục rỗng. Timeout mutation là kết quả chưa rõ: xem request journal/inspect trước khi thử lại.

Chỉ đóng/stop PID do tác vụ sở hữu sau khi đã lưu. HTML xem qua HTTP localhost không cần extension trình duyệt. Có thể dùng Python http.server --bind 127.0.0.1 và Playwright bất kỳ để kiểm tra; tắt server thử khi xong. Không cần cài background service hay sửa cấu hình MCP toàn cục.

## Nguồn và phần đã sửa

- Native bridge: https://github.com/leileqiTHU/reverse-cli-anything/tree/main/axure-cli (MIT). Source tải 2026-10-31. Pilot đổi APP trong axure_cli.py sang biến AXURE_PILOT_APP hoặc E:/AxureRP11.exe, tránh phải cài registry adapter của framework. Wrapper axure-cli.ps1 được sửa để gọi Python có sẵn; không phụ thuộc ../tools/resolve-python.ps1. reverse_cli/config.py và __init__.py được giữ cho directory/cache.
- Axvg builders và clipboard: https://github.com/FD-design/YPAxure . Chưa thấy license công bố; giữ provenance này khi dùng lại, kiểm tra quyền tái phân phối nếu cần chia sẻ thư viện.
- MCP: https://docs.axure.com/axure-rp/reference/mcp/ .
- Nghiên cứu và lịch sử: E:/AI-Company/knowledge/research/2026-10-31-axure-automation/README.md .

Mẫu prompt cho AI khác: "Đọc tools/axure-ai/README.md trong COMP1649_HCI, kiểm tra phiên bản app và trạng thái thật, rồi dùng Axvg + native CLI tạo prototype vào file mới. Giữ tài liệu đang làm của tôi; kiểm tra .rp mở lại và hành vi HTML."
