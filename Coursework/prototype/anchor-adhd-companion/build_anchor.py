import sys, json, os, time
from pathlib import Path

# Paths
KIT_ROOT = Path(r"E:\Hoc tap\Mon hoc\Năm 3 kì 1\COMP1649_HCI\tools\axure-ai")
sys.path.insert(0, str(KIT_ROOT / 'native-cli'))
os.environ['REVERSE_CLI_CACHE_DIR'] = 'E:/ai-cache/axure-pilot/cache'
import axure_cli as ax

OUT_DIR = Path(r"E:\Hoc tap\Mon hoc\Năm 3 kì 1\COMP1649_HCI\Coursework\prototype\anchor-adhd-companion")
OUT_DIR.mkdir(parents=True, exist_ok=True)
RP_PATH = OUT_DIR / 'anchor-prototype.rp'
HTML_DIR = OUT_DIR / 'html'
LOG_PATH = OUT_DIR / 'build-log.jsonl'

def call(op, **kw):
    payload = dict(op=op, **kw)
    result = ax.request(payload)
    with LOG_PATH.open('a', encoding='utf-8') as f:
        f.write(json.dumps({'op': op, 'payload': payload, 'response': result}, ensure_ascii=False) + '\n')
    if not result.get('ok'):
        raise RuntimeError(f"Operation '{op}' failed: {result}")
    return result['result']

def widget(kind, name, text, x, y, w, h, **kw):
    res = call('widget.create', kind=kind, name=name, text=text, x=x, y=y, width=w, height=h, **kw)
    return res['id']

def build_anchor():
    print("=== Launching Axure RP 11 ===")
    launch_res = ax.launch()
    assert launch_res['ok'], f"Launch failed: {launch_res}"
    print(f"Axure launched with PID: {launch_res['launchedPid']}")

    # Wait for editor to be ready
    ready = False
    for i in range(20):
        time.sleep(0.5)
        st = ax.request({'op': 'status'}, timeout=2)
        if st.get('ok'):
            insp = ax.request({'op': 'inspect'}, timeout=2)
            if insp.get('ok') and insp['result'].get('writable'):
                ready = True
                print(f"Editor ready and writable at {i*0.5:.1f}s.")
                break
    assert ready, "Axure editor did not become ready."

    # Get initial page
    pages_init = call('page.list')
    p1_id = pages_init['activeId']
    print(f"Initial active page (Page 1): {p1_id}")

    # Create remaining pages
    print("Creating pages...")
    p2_id = call('page.create', name='02 Thẻ đơn nhiệm 15 phút')['page']['Id']
    p3_id = call('page.create', name='03 Cứu kẹt Nano 3 phút')['page']['Id']
    p4_id = call('page.create', name='04 Chốt đà tiến độ')['page']['Id']

    print(f"Created: P2={p2_id}, P3={p3_id}, P4={p4_id}")

    # =========================================================================
    # BUILD PAGE 4: 04_Chot_Da_Tien_Do
    # =========================================================================
    print("Building Page 4 (Chốt đà tiến độ)...")
    call('page.open', id=p4_id)
    widget('paragraph', 'p4_eyebrow', 'ĐÃ PHÁ VỠ QUÁN TÍNH TRÌ HOÃN • CHIẾN THẮNG BƯỚC ĐẦU', 140, 60, 720, 25)
    widget('paragraph', 'p4_title', 'Xuất sắc! Bạn đã vượt qua rào cản tâm lý khó nhất.', 140, 95, 720, 48)
    widget('paragraph', 'p4_badge', 'ĐÀ TẬP TRUNG (MOMENTUM): ĐÃ KÍCH HOẠT • BƯỚC KHỞI ĐỘNG 1/1 HOÀN THÀNH', 140, 155, 720, 30)
    widget('paragraph', 'p4_desc', '80% sự mệt mỏi của người ADHD đến từ cảm giác dằn vặt trước khi bắt đầu. Giờ đây bạn đã hành động, não bộ đã giải phóng dopamine tích cực để tiếp tục.', 140, 195, 720, 48)
    widget('paragraph', 'p4_prompt', 'Chọn hướng đi tiếp theo phù hợp với thể trạng của bạn ngay lúc này:', 140, 258, 600, 25)
    
    p4_feedback = widget('paragraph', 'p4_feedback', '', 140, 292, 720, 38)
    p4_btn_break = widget('button', 'p4_btn_break', '☕ Nghỉ nạp năng lượng 5 phút (Hẹn giờ)', 140, 345, 330, 52)
    p4_btn_next = widget('button', 'p4_btn_next', '🚀 Mở bước tiếp theo ngay (Đang vào luồng)', 490, 345, 330, 52)
    p4_btn_restart = widget('button', 'p4_btn_restart', '← Hoàn thành phiên / Bắt đầu bài tập mới', 140, 425, 310, 44)
    widget('paragraph', 'p4_footer', 'Anchor • Thiết kế theo nguyên lý Don Norman & Lý thuyết Điều hành ADHD • COMP1649 HCI', 140, 500, 720, 28)

    # Interactions on Page 4
    call('interaction.set', id=p4_btn_break, spec={
        'event': 'click',
        'cases': [{
            'name': 'Nghỉ ngơi 5 phút',
            'actions': [{
                'type': 'setText',
                'target': p4_feedback,
                'text': '⏱️ Đã kích hoạt hẹn giờ 5 phút! Hãy đứng dậy vươn vai, uống nước và rời mắt khỏi màn hình.'
            }]
        }]
    })

    call('interaction.set', id=p4_btn_next, spec={
        'event': 'click',
        'cases': [{
            'name': 'Mở bước tiếp theo',
            'actions': [{
                'type': 'setText',
                'target': p4_feedback,
                'text': '🎯 Tuyệt vời! Bước tiếp theo: "Đọc lướt 2 trang đầu của brief và ghi lại 3 từ khóa cốt lõi".'
            }]
        }]
    })

    call('interaction.set', id=p4_btn_restart, spec={
        'event': 'click',
        'cases': [{
            'name': 'Bắt đầu bài tập mới',
            'actions': [{'type': 'navigate', 'page': p1_id}]
        }]
    })

    # =========================================================================
    # BUILD PAGE 3: 03_Cuu_Ket_Nano
    # =========================================================================
    print("Building Page 3 (Cứu kẹt Nano 3 phút)...")
    call('page.open', id=p3_id)
    widget('paragraph', 'p3_eyebrow', 'CỨU KẸT THÍCH ỨNG • NANO-ACTION: 3 PHÚT', 140, 60, 720, 25)
    widget('paragraph', 'p3_title', 'Hoàn toàn bình thường. Chúng ta hạ tiêu chuẩn xuống nhé!', 140, 95, 720, 48)
    widget('paragraph', 'p3_sub', 'Khi đối mặt với sự tê liệt (freeze mode), ý chí không có tác dụng — chỉ có việc giảm ma sát xuống mức KHÔNG THỂ THẤT BẠI mới giúp bạn bắt đầu.', 140, 155, 720, 45)
    widget('paragraph', 'p3_box_title', 'BƯỚC SIÊU NHỎ CỰC TIỂU (≤ 3 PHÚT):', 140, 218, 600, 25)
    widget('paragraph', 'p3_box_content', 'Hành động: Chỉ cần mở một file Word/Docs trắng và gõ đúng tiêu đề: "COMP1649 HCI Coursework".', 140, 248, 720, 52)
    widget('paragraph', 'p3_reassurance', 'Không cần viết thêm chữ nào. Không cần suy nghĩ dàn ý. Bạn chỉ cần tạo file và bấm Lưu (Save). Ngay khi file được lưu, bạn đã chính thức phá vỡ rào cản trì hoãn!', 140, 310, 720, 48)

    p3_btn_accept = widget('button', 'p3_btn_accept', 'Tôi đã tạo file trắng và lưu lại! Tiếp tục →', 140, 385, 420, 52)
    p3_btn_back = widget('button', 'p3_btn_back', '← Bước 15 phút ban đầu vẫn ổn, quay lại', 140, 455, 320, 44)
    widget('paragraph', 'p3_footer', 'Cơ chế Adaptive Chunk-Down: Giảm tải nhận thức để khôi phục quyền kiểm soát hành vi', 140, 530, 720, 28)

    # Interactions on Page 3
    call('interaction.set', id=p3_btn_accept, spec={
        'event': 'click',
        'cases': [{
            'name': 'Hoàn thành nano step',
            'actions': [{'type': 'navigate', 'page': p4_id}]
        }]
    })

    call('interaction.set', id=p3_btn_back, spec={
        'event': 'click',
        'cases': [{
            'name': 'Về bước 15 phút',
            'actions': [{'type': 'navigate', 'page': p2_id}]
        }]
    })

    # =========================================================================
    # BUILD PAGE 2: 02_The_Don_Nhiem
    # =========================================================================
    print("Building Page 2 (Thẻ đơn nhiệm 15 phút)...")
    call('page.open', id=p2_id)
    widget('paragraph', 'p2_eyebrow', 'BƯỚC DUY NHẤT LÚC NÀY • THỜI GIAN: 15 PHÚT', 140, 60, 720, 25)
    widget('paragraph', 'p2_title', 'Chỉ một việc này thôi. Không nhìn bước tiếp theo.', 140, 95, 720, 48)
    widget('paragraph', 'p2_sub', 'Bộ nhớ làm việc của người ADHD sẽ bị nghẽn nếu thấy quá nhiều đầu việc. Bạn chỉ cần hoàn thành duy nhất bước sau:', 140, 155, 720, 42)
    widget('paragraph', 'p2_box_title', 'NHIỆM VỤ THẢ NEO (ANCHOR ACTION):', 140, 215, 600, 24)
    widget('paragraph', 'p2_box_content', 'Bước 1: Mở file coursework-brief và tô vàng đúng 3 tiêu chí chấm điểm quan trọng nhất', 140, 245, 720, 52)
    widget('paragraph', 'p2_guidance', 'Không cần viết bài ngay. Không cần đọc hết 15 trang tài liệu. Chỉ cần mở file brief ra và highlight đúng 3 gạch đầu dòng bạn thấy quan trọng nhất trong rubric.', 140, 308, 720, 45)
    widget('paragraph', 'p2_tip', '💡 Mẹo chống phân tâm: Hãy mở đồng hồ hẹn giờ 15 phút và cất điện thoại ngoài tầm với.', 140, 362, 720, 28)

    p2_btn_done = widget('button', 'p2_btn_done', 'Đã hoàn thành bước này! →', 140, 410, 310, 52)
    p2_btn_stuck = widget('button', 'p2_btn_stuck', 'Bước này vẫn quá sức? Chia nhỏ nữa ⚡', 470, 410, 330, 52)
    p2_btn_back = widget('button', 'p2_btn_back', '← Quay lại sửa đề bài', 140, 485, 200, 42)
    widget('paragraph', 'p2_footer', 'Nguyên lý Monotasking: Loại bỏ hoàn toàn danh sách phân tâm • 1 Thẻ = 1 Hành động', 140, 550, 720, 28)

    # Interactions on Page 2
    call('interaction.set', id=p2_btn_done, spec={
        'event': 'click',
        'cases': [{
            'name': 'Hoàn thành bước 1',
            'actions': [{'type': 'navigate', 'page': p4_id}]
        }]
    })

    call('interaction.set', id=p2_btn_stuck, spec={
        'event': 'click',
        'cases': [{
            'name': 'Cứu kẹt chia nhỏ',
            'actions': [{'type': 'navigate', 'page': p3_id}]
        }]
    })

    call('interaction.set', id=p2_btn_back, spec={
        'event': 'click',
        'cases': [{
            'name': 'Về trang khởi động',
            'actions': [{'type': 'navigate', 'page': p1_id}]
        }]
    })

    # =========================================================================
    # BUILD PAGE 1: 01_Khoi_Dong
    # =========================================================================
    print("Building Page 1 (Khởi động)...")
    call('page.open', id=p1_id)
    widget('paragraph', 'p1_eyebrow', 'ANCHOR // ĐIỂM TỰA ĐIỀU HÀNH HỌC TẬP', 140, 60, 720, 25)
    widget('paragraph', 'p1_title', 'Vượt qua trì hoãn. Bắt đầu nhẹ nhàng.', 140, 95, 720, 48)
    widget('paragraph', 'p1_desc', 'Đừng cố nhìn toàn bộ bài tập lớn. Hãy để Anchor giúp bạn giải nén và thả neo đúng một bước khởi động khả thi trong 15 phút.', 140, 155, 720, 48)
    widget('paragraph', 'p1_label', 'Nhập tên môn học hoặc đề bài bạn đang thấy áp lực:', 140, 225, 520, 24)

    p1_input = widget('input', 'course_input', '', 140, 258, 520, 48, placeholder='Ví dụ: COMP1649 HCI Coursework')
    p1_btn_preset = widget('button', 'btn_preset', '✨ Chọn bài mẫu: COMP1649 HCI', 140, 320, 310, 42)
    p1_feedback = widget('paragraph', 'p1_feedback', '', 140, 375, 680, 32)
    p1_btn_start = widget('button', 'btn_start', 'Bắt đầu giải nén đề bài →', 140, 420, 310, 52)
    p1_btn_reset = widget('button', 'btn_reset', 'Nhập lại', 470, 420, 140, 52)
    widget('paragraph', 'p1_footer', 'Phương pháp Monotasking chống Executive Dysfunction • Thiết kế giảm quá tải nhận thức cho sinh viên đại học', 140, 515, 720, 30)

    # Interactions on Page 1
    call('interaction.set', id=p1_btn_preset, spec={
        'event': 'click',
        'cases': [{
            'name': 'Chọn đề bài mẫu',
            'actions': [
                {'type': 'setText', 'target': p1_input, 'text': 'COMP1649 HCI Coursework'},
                {'type': 'setText', 'target': p1_feedback, 'text': 'Đã chọn đề bài mẫu! Bấm "Bắt đầu giải nén đề bài" để tiếp tục.'}
            ]
        }]
    })

    call('interaction.set', id=p1_btn_reset, spec={
        'event': 'click',
        'cases': [{
            'name': 'Nhập lại',
            'actions': [
                {'type': 'setText', 'target': p1_input, 'text': ''},
                {'type': 'setText', 'target': p1_feedback, 'text': ''}
            ]
        }]
    })

    call('interaction.set', id=p1_btn_start, spec={
        'event': 'click',
        'cases': [
            {
                'name': 'Chưa nhập đề bài',
                'when': {'widget': p1_input, 'equals': ''},
                'actions': [{
                    'type': 'setText',
                    'target': p1_feedback,
                    'text': 'Bạn hãy nhập tên bài tập hoặc bấm "Chọn bài mẫu" để Anchor chia nhỏ giúp bạn.'
                }]
            },
            {
                'name': 'Bắt đầu giải nén',
                'actions': [{'type': 'navigate', 'page': p2_id}]
            }
        ]
    })

    # Save metadata
    metadata = {
        'project': str(RP_PATH),
        'html': str(HTML_DIR),
        'pages': {
            '01_Khoi_Dong': p1_id,
            '02_The_Don_Nhiem': p2_id,
            '03_Cuu_Ket_Nano': p3_id,
            '04_Chot_Da_Tien_Do': p4_id
        },
        'widgets': {
            'p1_input': p1_input,
            'p1_feedback': p1_feedback,
            'p1_btn_preset': p1_btn_preset,
            'p1_btn_start': p1_btn_start,
            'p1_btn_reset': p1_btn_reset,
            'p2_btn_done': p2_btn_done,
            'p2_btn_stuck': p2_btn_stuck,
            'p2_btn_back': p2_btn_back,
            'p3_btn_accept': p3_btn_accept,
            'p3_btn_back': p3_btn_back,
            'p4_feedback': p4_feedback,
            'p4_btn_break': p4_btn_break,
            'p4_btn_next': p4_btn_next,
            'p4_btn_restart': p4_btn_restart
        }
    }
    (OUT_DIR / 'metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')

    # Save Project
    print(f"Saving project to: {RP_PATH}")
    call('project.save', path=str(RP_PATH))

    # Export HTML
    print(f"Exporting HTML to: {HTML_DIR}")
    call('export.html', output=str(HTML_DIR))

    # Close and Cold Reopen Verification
    print("Performing cold reopen verification...")
    call('project.close')
    reopen_res = ax.launch(str(RP_PATH))
    assert reopen_res['ok'], f"Cold reopen failed: {reopen_res}"
    print(f"Reopened successfully with PID: {reopen_res['launchedPid']}")

    # Verify pages and widgets
    reopened_pages = call('page.list')
    print("Reopened pages count:", len(reopened_pages['pages']))
    assert len(reopened_pages['pages']) == 4, f"Expected 4 pages, got {len(reopened_pages['pages'])}"

    # Check widgets on Page 1
    call('page.open', id=p1_id)
    p1_widgets = call('widget.list')
    print("Page 1 widgets:", len(p1_widgets))
    assert len(p1_widgets) >= 8, f"Expected at least 8 widgets on Page 1, got {len(p1_widgets)}"

    # Check interaction on Page 1 start button
    start_ix = call('interaction.get', id=p1_btn_start)
    print("Page 1 start button interaction events:", len(start_ix['events']))
    assert len(start_ix['events']) >= 1, "Missing interaction on start button"

    # Close cleanly
    call('project.close')
    print("=== BUILD AND VERIFICATION COMPLETE SUCCESSFULLY ===")

if __name__ == '__main__':
    build_anchor()
