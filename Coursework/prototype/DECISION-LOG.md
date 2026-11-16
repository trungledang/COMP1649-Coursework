# Tether — Decision log (dùng để viết Ch.3 & Ch.4 của report)

> **Mục đích:** mỗi dòng là một quyết định thiết kế *đã có trong prototype*, kèm nguyên lý Norman
> và bằng chứng cụ thể (tên trang / tên widget trong file `.rp`). Đây là **nguyên liệu để bạn tự diễn giải**,
> không phải văn bản nộp. Khi viết report, hãy diễn giải lại bằng lời của bạn và ghi rõ nguồn lý thuyết.
>
> File `.rp` tham chiếu: `Coursework/prototype/Tether-ADHD-Companion-Prototype.rp` (17 trang, 430×932).

---

## A. Các quyết định thiết kế trong sản phẩm

| # | Tính năng | Vấn đề thiết kế giải quyết | Nguyên lý Norman | Bằng chứng trong prototype |
|---|---|---|---|---|
| 1 | **Tách bài lớn thành 3 hành động nhỏ** | ADHD / rối loạn chức năng điều hành: người dùng không bắt đầu được vì "bài quá lớn" | **Constraints** (giới hạn số bước), **Visibility** (thấy đúng 1 việc tiếp theo) | Trang `07 Your plan`: 3 thẻ Step 1–3, mỗi thẻ 1 ô nhập sửa được (`v2_start_1..3`) |
| 2 | **Chỉ hiện "bước hiện tại"** | Mất dấu khi làm việc dài → cần luôn biết đang ở đâu | **Visibility**, **Consistency** | Biến toàn cục `TetherCurrent` + overlay `v2_start_1..3` chỉ bật nút của bước đang làm |
| 3 | **Ghi lại manh mối khi nghỉ ("leave a thread")** | "Save & exit" làm mất ngữ cảnh → quay lại không biết đang làm gì | **Visibility**, **Feedback** | Trang `04 Leave a thread`: 2 ô (`where_stopped`, `next_move`) → `TetherWhere`, `TetherNext`; trang `01 My study desk` hiện lại đúng nội dung đó |
| 4 | **Đề xuất bước nhỏ hơn khi kẹt** | Người dùng đứng yên khi bài quá lớn → cần lối ra khỏi bế tắc | **Affordance** (nút "Use smaller step"), **Feedback** | Trang `03 When you are stuck`: `v2_choice_start/small/source`, `v2_try_suggestion` |
| 5 | **Chọn khối thời gian có thật** | "Cả ngày" quá lớn → cam kết thời gian cụ thể | **Constraints** (3 lựa chọn giới hạn), **Consistency** | Trang `08 Study time`: 3 thẻ giờ → `TetherStudyTime` |
| 6 | **Đặt nhịp độ (pace)** | Người ADHD không có nhịp cố định → nhịp phải chỉnh được | **Consistency**, **User control** | Trang `03 Set your pace` → `TetherPace` |
| 7 | **Cảnh báo trước khi ghi đè kế hoạch** | Ghi đè mất công sức → cần cảnh báo trước | **Feedback**, **Constraints** | Trang `06 Check requirements`: dòng cảnh báo đỏ + overlay `v2_build_reset` |
| 8 | **Điều hướng 2 tầng: thanh 3 tab + luồng tập trung** | Tránh mất phương hướng trong app nhiều màn hình | **Consistency**, **Visibility of alternatives** | Thanh `Today/Plan/Me` ở 4 trang chính; nhóm `02 Pause and return` là luồng tập trung không có thanh tab (xem mục C) |
| 9 | **Ghi chú nếp học thật của người dùng** | Demo phải cảm nhận được dữ liệu người nhập, không phải ảnh chụp màn hình | **Feedback** (state thật), **User control** | `TetherAssignment`, `TetherBrief`, `TetherDraftAssignment`, `TetherDraftBrief`, `TetherStep1..3` |
| 10 | **Đánh dấu bước đã xong (step tracking)** | Người dùng không tin app là đã làm được phần nào | **Feedback** | `TetherDone1..3` + overlay `v2_done` (trang `02 Continue your work`) |

## B. Vòng lặp thiết kế (để viết Ch.4 — "Demonstrate how the design progressed")

| Mốc | Trạng thái | Bằng chứng trong repo |
|---|---|---|
| 2026-10-19 | Bản web `studyflow-web-v3.rp` — thử nghiệm, **không dùng để nộp** | `studyflow-web-v3.rp`, `STUDYFLOW-WEB-STATUS.md` |
| 2026-11-01 | Bản "anchor" đầu tiên trong Axure (2 trang) | `anchor-adhd-companion/anchor-prototype.rp` |
| 2026-11-02 | Dựng 17 trang + 17 biến toàn cục, đổi "Settings" → "Me", thêm avatar | `final-coursework.rp`, `final-configure.log`, `final-improvements.log` |
| 2026-11-08 | Gom trang theo 3 nhóm trong sitemap, bỏ nút trùng | `Tether_ADHD_Companion_Final.rp` |
| 2026-11-09 | Thêm **step tracking** (theo dõi bước) — bản vá bằng script qua native bridge | `tether-revision-2026-11-09.rp`, `apply-step-tracking-revision.py`, `.log.md` |
| 2026-11-16 | **Sửa lỗi canvas 1001 px** (xoá 15 widget trùng bị "park" ở x=1000), thêm hướng dẫn cho ô nhập đề bài, nối `TetherName`, chụp lại ảnh | `Tether-ADHD-Companion-Prototype.rp`, `fix-canvas-width.py`, `apply-tasks.py`, `demo/screens-2026-11-16/` |

**Câu chuyện iteration đáng kể trong báo cáo (và là điểm mạnh khi GV hỏi):**
> Bản 09/11 sửa lỗi "nút đè 3 lớp" bằng cách **dời các widget cũ ra x=1000** thay vì xoá. Việc này làm
> Axure tính chiều rộng adaptive view thành **1001 px**, và bản export HTML sau đó bị **sửa tay CSS**
> để ép về 430 px để "trông đúng". Ngày 16/11, bản sửa này được phát hiện và làm lại đúng cách:
> **xoá** 15 widget trùng bằng API delete gốc của Axure, export lại bằng generator gốc, và kiểm chứng
> bằng `data.js` rằng cả 17 trang đều báo `adaptive view width = 430`. Bài học này rất đáng kể trong Ch.4:
> *một prototype chỉ đáng tin khi bằng chứng được tạo ra từ chính artefact được nộp, không phải từ
> bản export đã sửa tay.*

## C. Quyết định cố ý giữ lại (để phản biện khi GV hỏi)

| Điểm | Quyết định | Lý do |
|---|---|---|
| Nhóm `02 Pause and return` **không có** thanh tab | Giữ luồng tập trung, thoát bằng nút "Pause and leave a thread" | Tránh cạnh tranh với CTA chính ("Continue this step"); đánh đổi có ý thức giữa *focus mode* và *persistent navigation* → **câu hỏi nghiên cứu RQ3** |
| Khung cố định **430 px** (không responsive 390 px) | Mid-fidelity prototype, không phải bản production | Ghi rõ giới hạn trong report thay vì giấu; cũng là một câu hỏi nghiên cứu |
| Chữ động `[[TetherName]]` trong avatar | **Chưa làm** — bridge không tạo được inline expression của Axure | Làm thủ công trong Axure trong 2 phút nếu muốn (gõ `[[TetherName]]` vào ô text của `profile_avatar_initial`) |
| Đồng hồ đếm ngược 10 phút | **Chưa làm** — bridge chưa hỗ trợ dynamic panel/timer | Nếu thêm, làm tay trong Axure; hoặc bỏ và nói rõ trong report |
| AI, đăng nhập, lưu trữ | Mô phỏng | Đề tài là thiết kế trải nghiệm, không phải sản phẩm chạy được |

## D. Khoảng trống cần bạn lấp (không làm được bằng tool, nhưng bắt buộc cho report)

1. **Không có tài liệu nào trong `Coursework/report/` và `Coursework/research/`** — 70/100 điểm rubric.
2. Mỗi dòng ở mục A cần **1–2 câu diễn giải của bạn** + **1 trích dẫn học thuật** (mục 2 đã có sẵn 2 nguồn: Zhu et al. CHI '26; Parmar et al. 2026 — cần thêm 4–6 nguồn).
3. Cần **AI-use reflection 60–100 từ** (đặt trước References) + **AI-use declaration page** trong Appendix.
4. Cần xác nhận **deadline thật** (brief trong repo đang để placeholder).
