# Hướng dẫn cải thiện `final-coursework.rp`

Có 7 cải thiện. Mục 4 có script tự chạy, các mục còn lại bạn làm tay trong Axure RP 11 (vừa sửa file, vừa luyện kỹ năng).

**Trước khi bắt đầu:** copy `final-coursework.rp` ra một bản dự phòng (ví dụ `final-coursework.backup.rp`). Làm xong mỗi mục thì bấm **Preview (Ctrl+.)** kiểm tra và **Ctrl+S**.

Thứ tự nên làm: **4 (script) → 1 → 2 → 6 → 7 → 3 → 5** (dễ đến khó).

---

## Mục 4: Hiện đề bài ở trang Plan (chạy script)

Biến `TetherBrief` được lưu ở trang 06 nhưng chưa trang nào hiển thị. Script thêm một dòng chữ `plan_brief` ở cuối trang **07 Your plan** (trên thanh nav) và cho nó đọc `TetherBrief` khi trang tải.

1. `git pull` để lấy file mới.
2. Mở Axure qua native CLI như trong `tools/axure-ai/README.md` (lệnh `launch`), đợi `status` báo bridge sẵn sàng. **Đóng mọi phiên Axure khác đang mở `final-coursework.rp`.**
3. Ở thư mục gốc của môn học (COMP1649_HCI), chạy:
   ```powershell
   & 'E:/Runtimes/python312-3.12.14/python.exe' Coursework/prototype/tether-final-build/improve-plan-brief.py
   ```
4. Kết quả đúng sẽ in ra `Backup`, `plan_brief`, `OnLoad`, `Saved`, `Exported`. Nếu lỗi, copy toàn bộ log gửi lại cho Claude.
5. Kiểm tra: Preview → 05 Add assignment → gõ title và brief → Review → Confirm → trang Plan phải hiện đúng brief vừa gõ ở phía dưới.

Script tự tạo bản dự phòng `final-coursework.before-brief.rp`. Muốn hoàn tác thì đổi tên file đó lại.

**Tự chỉnh thêm (nên làm):** dòng mới dùng font mặc định Arial. Chọn `plan_brief` → panel **Style** → font **Inter**, cỡ **13**, màu `#526B70` cho đồng bộ với phần chữ phụ.

---

## Mục 1: Đổi tên và sắp xếp trang

1. Panel **Pages** (bên trái): double-click **Page 1** → đổi thành `01b Study desk`.
2. Kéo thả để thứ tự trang theo đúng luồng người dùng:
   ```
   00 Welcome, 01 Log in, 02 Create account, 03 Set your pace,
   04 Today, 05 Add assignment, 06 Check requirements, 07 Your plan,
   08 Study time, 09 Study time saved, 10 Your space,
   01b Study desk, 02 Continue your work, 03 When you are stuck,
   04 Leave a thread, 05 Ready to return, 06 Step complete
   ```
3. (Tuỳ chọn) Gom 6 trang cuối vào một **folder** tên `Work session`: chuột phải trong panel Pages → **Add → Folder**.

Đổi tên trang không làm hỏng link vì Axure link theo ID trang, không theo tên.

---

## Mục 2: Xóa các nút cũ nằm chồng bên dưới

Một số trang có hai vùng bấm trùng vị trí. Lớp trên (mới) đang hoạt động, lớp dưới (cũ) thừa.

| Trang | Xóa (cũ) | Giữ (mới) |
|---|---|---|
| 02 Continue your work | `hit_done` | `v3_finish_step` |
| 03 When you are stuck | `hit_start`, `hit_small`, `hit_source`, `hit_try` | `v2_choice_*`, `v2_try_suggestion` |
| 04 Leave a thread | `hit_save` | `hit_save_with_variables` |
| 07 Your plan | `app_step1`, `app_step2`, `app_step3`, `app_schedule` | `personalized_start_*`, `personalized_schedule` |

Cách làm: panel **Outline** (bên phải) → tìm tên → chọn → **Delete**. Xóa xong mỗi trang, Preview và bấm lại các nút để chắc vẫn chạy.

⚠️ Đừng xóa `hit_back`, `hit_stuck`, `hit_pause`: chúng không có bản trùng.

---

## Mục 6: Hướng dẫn nhập đề bài theo dòng

Hàm `replace` của Axure chỉ thay lần xuất hiện đầu tiên, nên không tự tách đề bài thành gạch đầu dòng được. Cách đơn giản và hiệu quả là hướng dẫn người dùng nhập mỗi yêu cầu một dòng. Ô `assignment_brief` là ô nhiều dòng, nên trang 06 sẽ tự hiện đúng các dòng đó.

1. Trang **05 Add assignment** → chọn ô `assignment_brief` → panel **Style/Properties** → **Hint text** (placeholder): `One requirement per line, e.g. Report: 2,000–3,000 words`.
2. Đổi nhãn `What do you need to do?` thành `Key requirements (one per line)`.
3. Trang **05 Add assignment**, nút `app_example`: mở case trong panel **Interactions**, sửa giá trị gán cho `TetherDraftBrief` thành nhiều dòng (dùng **Shift+Enter** để xuống dòng trong ô giá trị):
   ```
   Report: 2,000–3,000 words
   Axure prototype with 2–3 journeys
   Deadline: Friday, 16:00
   ```
4. Preview: bấm **Use HCI example** → trang 06 hiện 3 dòng riêng biệt.

---

## Mục 3: Thẻ được chọn đổi màu (Selected state)

Áp dụng cho 3 trang: **03 Set your pace** (thẻ `light`, `steady`, `flexible`), **08 Study time** (`morning`, `afternoon`, `evening`), **03 When you are stuck** (3 thẻ gợi ý). Ví dụ dưới đây là trang 03 Set your pace.

### Bước 1: Tạo kiểu Selected cho thẻ
1. Panel Outline → chọn thẻ nền `light` (hình chữ nhật bo góc, **không phải** hotspot `app_light`).
2. Panel **Interactions** → **Interactive Styles** (hoặc nút **+ Add interactive style**) → **Selected** → đặt **Border**: 3px, màu `#175C59`.
3. Làm tương tự cho `steady` và `flexible`.

### Bước 2: Chỉ cho chọn một thẻ cùng lúc
Chọn cả 3 thẻ `light`, `steady`, `flexible` → chuột phải → **Selection Group** (nếu không thấy thì tìm ô **Selection Group** trong panel Interactions) → đặt tên `pace`. Khi một thẻ được chọn, Axure tự bỏ chọn các thẻ còn lại.

### Bước 3: Bấm thì chọn thẻ
Chọn hotspot `app_light` → Interactions → mở case OnClick đang có → **Add action → Set Selected/Checked** → target `light` → **true**. Làm tương tự `app_steady → steady` và `app_flexible → flexible`.

### Bước 4: Khi vào trang, chọn sẵn thẻ đúng với biến
Bỏ chọn mọi widget (click vào canvas trống) → panel Interactions hiện **Page Interactions** → OnPageLoad → **Add case**:
- Case "Gentle": **Condition** `value of variable TetherPace` `equals` `A gentle start` → action **Set Selected** `light` = true.
- Case "Focus": condition `TetherPace equals Some room to focus` → Set Selected `steady` = true.
- Case "Flexible": condition `TetherPace equals Flexible study time` → Set Selected `flexible` = true.

⚠️ Axure nối các case có điều kiện thành `IF / ELSE IF`. Case cũ "Restore the saved thread" không có điều kiện nên phải để nó **riêng**: chuột phải case Gentle → **Toggle IF/ELSE IF** để nó bắt đầu một khối IF mới.

Preview: chọn "Some room to focus" → Open my study desk → Settings → Study pace → thẻ giữa phải đang viền xanh.

---

## Mục 5: Đánh dấu ✓ bước đã làm xong

**Ý tưởng:** cần nhớ người dùng đang làm *bước số mấy*. Khi bấm Finish thì đánh dấu đúng bước đó, và trang Plan hiện ✓.

### Bước 1: Thêm biến
**Project → Global Variables** → thêm: `TetherCurrent` (mặc định `0`), `TetherDone1`, `TetherDone2`, `TetherDone3` (mặc định để trống).

### Bước 2: Nhớ bước đang làm
Trang **07 Your plan** → hotspot `personalized_start_1` → case cuối (không điều kiện) → thêm action **Set Variable Value** `TetherCurrent` = `1`, đặt **trước** action Open Link. Làm tương tự `personalized_start_2` → `2`, `personalized_start_3` → `3`.

### Bước 3: Bấm Finish thì đánh dấu
Trang **02 Continue your work** → `v3_finish_step` → OnClick, thêm 3 case **đặt trên** case hiện tại:
- IF `value of TetherCurrent equals 1` → Set Variable `TetherDone1` = `done` → rồi Set `TetherWhere`, `TetherNext` và Open Link `06 Step complete` (copy từ case cũ).
- ELSE IF `TetherCurrent equals 2` → `TetherDone2` = `done` → (như trên).
- ELSE IF `TetherCurrent equals 3` → `TetherDone3` = `done` → (như trên).
- ELSE → giữ case cũ.

### Bước 4: Trang Plan hiện ✓
Trang **07 Your plan** → OnPageLoad → thêm 3 case, mỗi case là **khối IF riêng** (Toggle IF/ELSE IF):
- IF `TetherDone1 equals done` → **Set Text** trên nhãn `Step 1: edit the action below` = `✓ Step 1 done`.
- Tương tự cho bước 2 và 3.

### Bước 5: Bài mới thì xóa dấu ✓
Trang **06 Check requirements** → `app_build` → thêm action: Set `TetherDone1`, `TetherDone2`, `TetherDone3` = (trống), `TetherCurrent` = `0`.

Preview: Plan → Start step 2 → Finish this step → về Plan → Step 2 hiện ✓.

---

## Mục 7: Avatar ở góc phải và lời chào theo tên

Lúc tạo tài khoản app bắt nhập tên, nhưng sau đó không hiện tên ở đâu. Đặt avatar ở góc **trên bên phải** (vị trí quen thuộc như Gmail, YouTube; góc trái đã có logo và thường dành cho nút quay lại).

1. **Project → Global Variables** → thêm `TetherName`, mặc định `Alex`.
2. Trang **02 Create account** → nút `app_signup` → case cuối (không điều kiện) → thêm **Set Variable Value** `TetherName` = **text on widget** `signup_name`, đặt **trước** Open Link.
3. Trang **04 Today**:
   - Ẩn hoặc xóa chữ `Today` ở góc phải trên.
   - Vẽ **Ellipse** 40×40 ở x=360, y=62, màu nền `#175C59`, chữ trắng đậm cỡ 18, đặt tên `avatar`.
   - Thêm text `greeting` dưới logo (x=28, y=100), cỡ 15, màu `#526B70`.
4. **OnPageLoad** của trang 04 (thêm action vào case đang có):
   - Set Text `avatar` = bấm **fx** → `[[TetherName.substr(0,1)]]` (lấy chữ cái đầu).
   - Set Text `greeting` = **fx** → `Hi, [[TetherName]]`.
5. `avatar` → OnClick → **Open Link** → `10 Your space`.

Preview: Welcome → Create account → gõ tên `Minh` → … → Today hiện `Hi, Minh` và avatar chữ `M`.

---

## Kiểm tra cuối

Chạy lại 3 luồng chính trong Preview:
1. **Bài tập → Plan:** Today → Add assignment → Review → Confirm → Plan (hiện brief) → Choose study time → Saved.
2. **Bị kẹt:** Plan → Start step → I feel stuck → chọn gợi ý (thẻ viền xanh) → Try this.
3. **Nghỉ và quay lại:** Continue → Pause → ghi 2 dòng → Done → Study desk hiện đúng 2 dòng.
