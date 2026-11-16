# Ghi nhớ demo Tether

Tờ này để luyện nói và giải thích prototype với giảng viên. Không phải nội dung báo cáo nộp.

## Câu chuyện trong khoảng một phút

Tether hỗ trợ sinh viên đại học có ADHD bắt đầu một bài lớn và quay lại sau khi nghỉ. Demo ba hành trình: từ đề bài đến kế hoạch; xử lý lúc bị mắc; lưu chỗ đang làm và tiếp tục sau.

## Luồng chính

```text
Welcome
  → Today
  → Add assignment (nhập bài hoặc dùng ví dụ)
  → Check requirements (đọc lại / sửa / xác nhận)
  → Your plan (xem và sửa ba bước gợi ý)
  → Start this step
  → I feel stuck? → chọn vướng mắc → thử việc nhỏ hơn
  → Pause and leave a thread
  → ghi chỗ dừng + việc tiếp theo
  → quay lại Study desk và tiếp tục
```

## Câu tiếng Anh ngắn để tự luyện

- “This is Tether. It helps students start a large assignment.” — Đây là Tether, giúp sinh viên bắt đầu bài lớn.
- “First, I add an assignment and check its requirements.” — Đầu tiên, tôi thêm bài và kiểm tra yêu cầu.
- “The plan has three suggested steps. I can edit them.” — Kế hoạch có ba bước gợi ý. Tôi có thể sửa chúng.
- “If I feel stuck, I can choose a smaller action.” — Nếu bị mắc, tôi có thể chọn một hành động nhỏ hơn.
- “Before a break, I save where I stopped and what to do next.” — Trước khi nghỉ, tôi lưu chỗ đã dừng và việc tiếp theo.
- “When I return, I can continue from my study desk.” — Khi quay lại, tôi có thể tiếp tục từ bàn học.

## Nếu thầy hỏi về công nghệ / chức năng

- **Dynamic panel:** “This prototype does not use a dynamic panel. It uses separate Axure pages and clickable hotspots.” *(Prototype này không dùng dynamic panel. Nó dùng các trang Axure riêng và vùng bấm.)*
- **Tương tác:** “The buttons navigate between pages. Global variables carry the example assignment, suggested steps and saved notes during the preview.” *(Nút chuyển trang. Biến toàn cục giữ bài mẫu, bước gợi ý và ghi chú trong lúc Preview.)*
- **AI:** “The AI is not connected. The assignment and suggested steps are prepared examples.” *(AI chưa kết nối. Bài và các bước gợi ý là ví dụ soạn sẵn.)*
- **Lưu dữ liệu:** “This is a prototype. Data is only available in the preview session; there is no real account or database.” *(Đây là prototype. Dữ liệu chỉ có trong phiên Preview; không có tài khoản hay cơ sở dữ liệu thật.)*
- **Avatar:** “The avatar is a shortcut to the profile page.” *(Avatar là lối tắt đến trang hồ sơ.)*
- **Quyết định thiết kế:** “I kept the suggested steps editable so the student stays in control.” *(Tôi để các bước gợi ý có thể sửa để sinh viên giữ quyền quyết định.)*

## Từ khóa dễ nhớ

`assignment` = bài tập · `requirements` = yêu cầu · `suggested steps` = các bước gợi ý · `edit` = sửa · `feel stuck` = cảm thấy bị mắc · `save my place` = lưu chỗ đang làm · `continue` = tiếp tục · `preview` = bản xem thử.

Nếu không nghe rõ: “Sorry, could you say that again, please?”

## Lưu ý trước khi demo

1. Mở `.rp`, bắt đầu Preview từ Welcome và mở Preview mới để phiên demo bắt đầu sạch.
2. Chọn trước luồng muốn trình bày; nói một câu ngắn rồi mới bấm mỗi màn hình.
3. Nói rõ AI, đăng nhập và lưu trữ thật chưa được triển khai.
4. Bản Preview desktop từng kiểm tra ở 430 × 932. Ở viewport 390 px, layout cố định bị cắt ngang; không nên trình bày nó như responsive hoàn chỉnh.

