from pathlib import Path
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn

root = Path(__file__).resolve().parent
doc = Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = section.bottom_margin = Inches(0.8)
section.left_margin = section.right_margin = Inches(0.85)
for name in ('Normal', 'Title', 'Heading 1', 'Heading 2'):
    style = doc.styles[name]
    style.font.name = 'Calibri'
    style.font.color.rgb = RGBColor(0, 0, 0)
normal = doc.styles['Normal']
normal.font.size = Pt(11)
normal.paragraph_format.line_spacing = 1.15
normal.paragraph_format.space_after = Pt(8)
doc.styles['Title'].font.size = Pt(20)
doc.styles['Title'].paragraph_format.space_after = Pt(8)
doc.styles['Heading 1'].font.size = Pt(13)
doc.styles['Heading 1'].paragraph_format.space_before = Pt(12)
doc.styles['Heading 1'].paragraph_format.space_after = Pt(6)
for line in (root / 'task-05-short.md').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    if line.startswith('# '):
        doc.add_paragraph(line[2:], 'Title')
    elif line.startswith('## '):
        doc.add_paragraph(line[3:], 'Heading 1')
    else:
        p = doc.add_paragraph(line)
        if line.startswith(('1. ', '2. ', '3. ')):
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.keep_together = True
doc.core_properties.title = 'Task 5 Prototype Idea and Research Questions'
doc.core_properties.subject = 'COMP1649 Topic A'
doc.core_properties.author = ''
doc.core_properties.last_modified_by = ''
doc.core_properties.comments = ''
for style in doc.styles:
    ppr = style.element.find(qn('w:pPr'))
    if ppr is not None:
        for border in list(ppr.findall(qn('w:pBdr'))):
            ppr.remove(border)
for para in doc.paragraphs:
    ppr = para._p.pPr
    if ppr is not None:
        for border in list(ppr.findall(qn('w:pBdr'))):
            ppr.remove(border)
output = root / 'Task5_Research_Questions.docx'
doc.save(output)
download_dir = Path('E:/Downloads/COMP1649_HCI')
download_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(output, download_dir / output.name)
print(output)
print('Words:', sum(len(p.text.split()) for p in doc.paragraphs))
assert not any('.md' in p.text or 'draft' in p.text.lower() for p in doc.paragraphs)
