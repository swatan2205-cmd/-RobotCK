"""Check preservation and structure of the report revision."""
from pathlib import Path
from collections import Counter
from zipfile import ZipFile
import hashlib, json, subprocess, re
from docx import Document

root=Path(__file__).resolve().parents[1]
old=root/'tmp/rubric_upgrade/before.docx'
new=root/'report/bao_cao_robot_cap_nhat.docx'
a,b=Document(old),Document(new)
def cells(t):return [[c.text for c in row.cells] for row in t.rows]
def media(path):
 with ZipFile(path) as z:
  return Counter(hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/'))
old_tables=[cells(t) for t in a.tables]
new_tables=[cells(t) for t in b.tables]
assert all(t in new_tables for t in old_tables),'Original table content changed'
assert not (media(old)-media(new)),'Original image missing'
assert [p.text for p in a.paragraphs[:15]]==[p.text for p in b.paragraphs[:15]],'Cover text changed'
pdf_path=new.with_suffix('.pdf')
text=subprocess.run(['pdftotext','-enc','UTF-8',str(pdf_path),'-'],capture_output=True,check=True).stdout.decode('utf-8')
info=subprocess.run(['pdfinfo',str(pdf_path)],capture_output=True,check=True).stdout.decode('utf-8')
pages=int(re.search(r'Pages:\s+(\d+)',info).group(1))
assert 'Error! Reference source not found.' not in text
assert 'Error! Bookmark not defined.' not in text
assert all(len(p.strip())>10 for p in text.split('\f') if p.strip()),'Empty page'
audit={
 'report':str(new.relative_to(root)),
 'pages':pages,'tables':len(b.tables),
 'native_math_objects':len(b._element.xpath('.//m:oMath')),
 'images_including_cover_logos':len(b.inline_shapes),
 'original_tables_preserved':True,'original_images_preserved':True,
 'cover_text_preserved':True,'broken_word_reference_detected':False,
 'sha256':hashlib.sha256(new.read_bytes()).hexdigest(),
 'validation':'Word COM export, visual page inspection, preservation assertions; no new controller changes',
 'limitations':['Numerical reference bound is not an analytic continuous certificate.',
 'No new stability theorem for held-wheel model or saturated Lyapunov law.',
 'Rubric quality does not guarantee an instructor score.']}
(root/'docs/rubric_upgrade_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
