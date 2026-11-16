# Tether — Trạng thái & bàn giao (2026-11-16)

> Tài liệu này **khôi phục lại** `HANDOFF.md` mà phiên Antigravity (`94711c51`) đã viết dở nhưng bị 429 quota,
> kèm phần kiểm chứng độc lập và kế hoạch tiếp theo.
> Người viết: OpenCode (MiniMax M3.1 Flash). Nguồn: transcript Antigravity `brain/94711c51.../logs/transcript_full.jsonl`.

---

## 0. File chuẩn (đã kiểm chứng)

| Vai trò | Đường dẫn |
|---|---|
| **.rp làm việc / sẽ nộp** | `Coursework/prototype/tether-revision-2026-11-09.rp` (365 534 B, mtime 2026-11-16 06:42:54) |
| **Backup trước lần sửa cuối** | `Coursework/prototype/tether-revision-2026-11-09.pre-fix.rp` (363 983 B, 2026-11-09 12:23) |
| **Export HTML mới nhất** | `Coursework/prototype/tether-final-build/export-step-tracking-2026-11-09/` (185 file, 17 trang + 4 boilerplate) |
| Export KHÔNG dùng (hỏng) | `Coursework/prototype/tether-final-build/bridge-research/export-step-tracking-2026-11-09/` (5 trang `width:-4570px`) |
| Bridge CLI đang dùng | `Coursework/prototype/tether-final-build/bridge-research/native-cli/` (bản fork, mới hơn `tools/axure-ai/native-cli/`) |

---

## 1. Phiên bên cạnh (Antigravity `94711c51` — "Kiểm Tra Tiến Độ Công Việc") làm gì

Các lượt user (tiếng Việt, rút gọn):

| Step | User | AG làm gì |
|---|---|---|
| 0 | "này hiện tại mình đến đâu rồi" | Chốt tiến độ: prototype gần xong, `Coursework/report/` + `Coursework/research/` **rỗng**. Đề xuất 4 giai đoạn (Chốt prototype → Khớp lý thuyết → Viết prototype+study → Hoàn thiện report). |
| 47 | "cái gì cũng nên có quy trình nhỉ và hoàn thành rp mới làm đc report chứ" | Xác nhận quy trình 4 giai đoạn, đồng thời nhắc rubric đòi hỏi "chứng minh thiết kế dựa trên bài báo Ch.2 + 5 nguyên lý Norman Ch.3". |
| 101 | "tao thấy nó chưa hoàn thiện đâu và có rất nhiều chỗ hỏng ấy ... m thử kiểm tra và rõ lỗi cũng như tìm lỗi đi" | **QA tự động bằng Edge headless** quét 17 trang → phát hiện 4 nhóm lỗi + 3 feature thiếu (mục 4.1). |
| 362 | "lưu lại đi để tao đưa sang opencode làm tiếp" | Viết handoff note → **file `HANDOFF.md` KHÔNG được ghi** (artifact path bị reject), rồi **429 QUOTA_EXHAUSTED** (claude-sonnet-4-6, reset 2026-11-18 17:02Z). Phiên chết ở đây. |

### 4.1. Bug AG phát hiện (step 172) và trạng thái xử lý

| # | Vấn đề | Xử lý của AG | Thực tế sau verify |
|---|---|---|---|
| BUG 1 | `02_continue_your_work` lệch layout (body width 230px) | đổi `step_state` từ (-200,-200) → (10,940) | ⚠️ xem mục 2.1 |
| BUG 2 | Nút đè chồng 3–4 lớp trên 5 trang (`plan`, `work`, `stuck`, `pause`, `review`) | **không xoá widget cũ**, dời sang x=1000 | ⚠️ xem mục 2.1 |
| BUG 3 | Biến `TetherName` không tồn tại | thêm qua bridge, default "Alex" | ✅ có, nhưng **chưa nối** (task B) |
| BUG 4 | Tràn ngang ở 390px (frame fix cứng 430px) | **không sửa** | ❌ vẫn còn (đã ghi nhận là giới hạn) |
| BUG 5 | Nav gap: Study Desk bị cô lập, lịch học không phản ánh ở Today | **không sửa** | ❌ còn (task C + task B') |
| MF 4 | `assignment_brief` thiếu placeholder | **không làm** | ❌ task A |
| MF 5 | Timer đếm ngược 10 phút | **không làm** | ❌ task D |
| MF 6 | Avatar/lời chào động theo tên | **không nối** | ❌ task B |

---

## 2. Đánh giá phản biện (đã kiểm chứng bằng dữ liệu, không chỉ tin transcript)

### 2.1. 🔴 NGHIÊM TRỌNG — "Fix" bug 2 đã **che** bug, và export đã bị sửa tay

Bằng chứng:

1. Export HTML gốc (native, 06:41) → 5 trang có `body { width: -4570px }`.
2. Export sau khi "fix" (06:43 native → **06:44:44 bị sửa tay**) → `body { width: 430px }`, và các widget bị dời đi xuất hiện ở `left:1000px; top:1000px`.
3. **`data.js` bản native** (không bị sửa tay, mtime 06:43:36) vẫn ghi:
   `defaultAdaptiveView … "size","width",m=1001`

| Trang | Adaptive view **native** trong .rp | `body{width}` trong CSS export | |
|---|---|---|---|
| `02_continue_your_work` | **1001** | 430 | ⚠️ lệch |
| `03_when_you_are_stuck` | **1001** | 430 | ⚠️ lệch |
| `04_leave_a_thread` | **1001** | 430 | ⚠️ lệch |
| `06_check_requirements` | **1001** | 430 | ⚠️ lệch |
| `07_your_plan` | **1001** | 430 | ⚠️ lệch |
| 12 trang còn lại | 430 | 430 | ✅ |

**Hệ quả:**
- File `.rp` được nộp có 5 trang rộng **1001px**. GV mở bằng Axure sẽ thấy canvas 1001px, mockup 430px nằm lệch trái, trống trải bên phải.
- Nếu GV tự export lại từ .rp → họ **không** được bản 430px mà mình đã quay và verify.
- "Bằng chứng đã verify" hiện tại **không còn đại diện cho .rp**.
- Vi phạm đúng nguyên tắc trong `tools/axure-ai/README.md`: *"exported HTML was never hand-edited to fake behaviour"*.

**Việc cần làm (đúng cách):** **xoá** widget cũ qua bridge (không dời), hoặc đặt `visible=false`, rồi export native lại và xác nhận `adaptiveViews.width == 430` **không cần sửa CSS tay**. Nếu bridge không xoá được → dời sang x âm (ví dụ -1000) để Axure không tính vào bbox, nhưng phải verify `data.js` ra 430.

### 2.2. 🟠 Cao — 70% điểm bài chưa có gì: report & bibliography

Rubric (`Coursework/docs/marking-criteria-and-rubric.txt`) = 100 điểm:

| Hạng mục | Điểm | Hiện trạng |
|---|---|---|
| Prototype mid-fidelity (P1) | **30** | ~80% — 17 trang, có global variables, step-tracking; nhưng còn lỗi 2.1 + task A/B/C/D |
| Annotated bibliography (R2) | **20** | **0%** — `Coursework/research/` rỗng; chỉ có 2 nguồn (Zhu et al. CHI'26; Parmar et al. 2026) |
| Thiết kế sản phẩm + nguyên lý Norman (R3) | **20** | **0%** — không có văn bản nào; chỉ có prototype làm "nguyên liệu" |
| Đề xuất nghiên cứu (R4) | **20** | **0%** — chỉ có 3 RQ trong `Weeks/Week-05/Task5_Research_Questions.docx`; thiếu questionnaire/interview guide/consent form |
| Chuyên nghiệp + Harvard referencing (R1) | **5** | **0%** |
| Conclusion (R5) | **5** | **0%** |

→ Điểm hiện tại ước tính **~24/100** nếu nộp ngay. Cần 70 điểm còn lại.

### 2.3. 🔴 Rủi ro liêm chính học học (academic integrity) — chưa ai xử lý

Brief (`Coursework/docs/coursework-brief-2026-27.txt`, mục "Use of Generative AI"):

> "Generative AI may be used only to support preparation for this assessment… **AI must not generate substantive assessment content.**
> All analysis, arguments, interpretations, and the final submission must be your own work."

Nhưng: **toàn bộ prototype là do agent AI sinh ra** (script + Axure bridge). Repo cũng tự cảnh báo ở `STUDYFLOW-WEB-STATUS.md`:
> "This is an AI-assisted development/practice version, not a verified submission-ready final. The brief limits generative AI to preparation and prohibits submitting AI-generated work as your own."

Hai việc bắt buộc, chưa làm:
1. **AI-use declaration page** trong Appendix (bắt buộc theo `annotated-table-of-contents-2026-27.txt`).
2. **Reflection 60–100 từ** về AI, đặt **trước References**.
3. **Quan trọng hơn:** report phải là của sinh viên. Agent có thể hỗ trợ *outline*, *checklist*, *gợi ý câu hỏi tự phản biện*, nhưng **không được viết thay** phần phân tích/lập luận/diễn giải.
4. Cần cân nhắc hỏi GV (Dr Annemarie Zijelma) về mức độ AI trong prototype có được chấp nhận không — đây là câu hỏi nên hỏi **sớm**, không phải cuối kỳ.

### 2.4. 🟠 Cao — Không có gì được commit/push từ 2026-11-02

- Branch `claude/brave-ramanujan-p2hvb2`, HEAD `7d1a603` (2026-11-02), **0 ahead / 0 behind** origin → **toàn bộ công việc 09/11 → 16/11 chưa commit, chưa push**.
- `.rp` chuẩn **untracked** → mất máy là mất toàn bộ.
- Repo bẩn: **2 183 file untracked** (1 144 file `.runtime/requests/*.json` + 87 file `.playwright-cli`), và **2 248 file `.runtime` đã bị commit** vào git trước đây. Không có `.gitignore`.
- 30 file `.rp` trùng tên trong `Coursework/prototype/` — không rõ file nào nộp.

### 2.5. 🟡 Trung bình — Deadline chưa xác định

Brief ghi `Submission Deadline: [Day, Date Month Year]` (placeholder). `README.md` cũng ghi cần cập nhật từ Moodle. **Không có ngày nộp ⇒ không lên được lịch chia điểm.** Đây là thông tin cần lấy từ Moodle/GV **trước khi làm bước tiếp theo**.

### 2.6. 🟡 Trung bình — Tài liệu demo trỏ sai file + ảnh cũ

- `KICH-BAN-DEMO.md`, `HUONG-DAN-CAI-THIEN.md`, `GHI-NHO-DEMO-TETHER.md` đều viết cho `final-coursework.rp` (bản 02/11), **không phải** bản chuẩn 16/11.
- 13 ảnh trong `Coursework/prototype/demo/` đều mtime **2026-11-02** → chụp từ bản cũ, **không khớp** prototype hiện tại. Rubric R3/R4 đòi "clear links between the coursework report and your prototype" → phải chụp lại.

### 2.7. 🟡 Trung bình — 2 bản bridge trôi dạt

`tools/axure-ai/native-cli/` (snapshot 31/10–01/11) vs `tether-final-build/bridge-research/native-cli/` (fork đã sửa `Backend.cs`, `InteractionExpressions.cs` ngày 02/11). Đang dùng bản fork. Không gộp lại → rủi ro "chạy được ở máy mình, hỏng ở máy khác".

---

## 3. Kế hoạch tiếp theo

### Ưu tiên 0 — Chặn, cần làm trong 30 phút
| # | Việc | Ai làm | Kiểm chứng |
|---|---|---|---|
| 0.1 | **Xác nhận deadline** từ Moodle/GV | Student | ghi vào `README.md` |
| 0.2 | Hỏi GV về mức độ AI được chấp nhận trong prototype (email 5 câu) | Student | bằng chứng đã hỏi |
| 0.3 | `git add` file chuẩn + commit "wip 2026-11-16" + push | Agent | `git log` có commit mới |
| 0.4 | Tạo `.gitignore` (`.runtime/`, `.playwright-cli/`, `export-*/`) — nhưng **chưa** `git rm` 2 248 file đã commit (làm ở đợt sau) | Agent | `git status` sạch |

### Ưu tiên 1 — Sửa prototype cho thật (1–2 buổi)
| # | Việc | Chi tiết |
|---|---|---|
| 1.1 | **Sửa 2.1 cho đúng** | Xoá/dời widget cũ, export native, xác nhận `data.js` có `width=430` cho cả 17 trang, **không sửa CSS tay** |
| 1.2 | Task A — `assignment_brief` | Page `489c9fbb`, widget `0ea5fb74-62b2-4c36-ac4c-087d0a45010d`: label → `"Key requirements (one per line)"`, placeholder → `"One requirement per line, e.g. Report: 2,000–3,000 words"` |
| 1.3 | Task B — nối `TetherName` | Signup `3bab9d97`: `app_signup` set `TetherName` = text `signup_name`; Today `5f19db87`: OnLoad set text `profile_avatar_initial` = `[[TetherName.substr(0,1)]]` |
| 1.4 | Task C — nav Study Desk | Thêm 1 nốt vào bottom nav (Today ↔ Study Desk) |
| 1.5 | Task D — timer 10 phút | Đồng hồ đếm ngược trên `08 Study time` |
| 1.6 | Chụp lại ảnh demo | 13 ảnh cũ (02/11) → chụp lại từ bản chuẩn, có highlight ô tương tác |
| 1.7 | Đặt tên file nộp | 1 file .rp duy nhất, tên rõ (vd `Tether-ADHD-Companion-Prototype.rp`), 1 export duy nhất |

**Điều kiện dừng (stop condition) của ưu tiên 1:** chỉ dừng khi `data.js` cả 17 trang = 430, không sửa CSS tay, và 2 luồng chính click được end-to-end.

### Ưu tiên 2 — Chốt prototype, khóa bản nộp (song song với ưu tiên 3)
- Ghi **decision log** (mỗi feature ↔ lý do thiết kế ↔ nguyên lý Norman) — đây là *nguyên liệu* để sinh viên tự viết Ch.3/Ch.4 mà không bị coi là AI-generated.

### Ưu tiên 3 — Report (70 điểm) — ưu tiên cao nhất về mặt điểm số
| Chương | Điểm | Việc cần làm | AI được phép làm gì |
|---|---|---|---|
| 2 Annotated bibliography | 20 | Tìm thêm 4–6 nguồn HCI/ADHD có thật, **verify từng nguồn** (DOI/URL), viết reflective commentary | AI **được** gợi ý từ khóa + danh sách ứng viên (đây là "preparation"); **sinh viên** phải đọc & viết nhận xét |
| 3 Design + Norman | 20 | 5 nguyên lý × ví dụ cụ thể trong Tether + ảnh | AI gợi ý mapping; SV tự diễn giải |
| 4 Prototype | 20 | Ảnh + lịch sử iteration + giải quyết rào cản tâm lý | SV tự viết narrative |
| 5 Research study | 20 | RQ/hypothesis, participants, procedure, data, analysis + questionnaire/interview/consent (Appendix) | AI **được** soạn bản nháp câu hỏi rồi SV sửa — nhưng bản cuối phải là SV |
| 1, 6, References, AI-reflection | 15 | Viết tay, đếm từ ≤3000, Harvard | Chỉ checklist |

> ⚠️ **Ranh giới đỏ:** không giao cho agent viết phần phân tích/lập luận. Agent được làm *scaffolding* (outline, checklist, câu hỏi gợi ý, đếm từ, kiểm tra reference khớp với trích dẫn) — còn lại là của SV.

### Ưu tiên 4 — Dọn repo & tài liệu
- `git rm --cached` 2 248 file `.runtime` đã commit; commit `.gitignore`.
- Gộp 2 bản bridge hoặc ghi rõ "bản nào là chuẩn".
- Cập nhật `KICH-BAN-DEMO.md` / `HUONG-DAN-CAI-THIEN.md` / `GHI-NHO-DEMO-TETHER.md` trỏ sang file chuẩn.

---

## 4. Câu hỏi cần Student quyết (chặn lịch)

1. Deadline thật là khi nào?
2. Trong 3 tuần tới, phân bổ thời gian: **50% prototype / 50% report** hay **30/70**? (mình khuyên **30/70** vì prototype đã ~80% còn report là 0%)
3. Có thể gửi email hỏi GV về mức độ AI trong prototype không?
4. Bản .rp nộp: giữ `tether-revision-2026-11-09.rp` hay đổi tên cho "chuyên nghiệp"?
