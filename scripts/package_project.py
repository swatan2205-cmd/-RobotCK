from pathlib import Path
import zipfile,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
release=ROOT/'release';release.mkdir(exist_ok=True)
dest=release/'robotck_project.zip'
paths=[]
for directory in ['src','config','scripts','tests','docs','report','figures','tables','original','results','external','output']:
    for p in (ROOT/directory).rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(ROOT)
        if '__pycache__' in p.parts or p.name.startswith('~$'):continue
        if directory=='external' and (p.suffix=='.zip' or 'upstream' in rel.parts):continue
        paths.append(p)
for name in ['AGENTS.md','README.md','.gitignore','GITHUB_UPLOAD.md','setup_project.m','STMPC_tracking_robot2023.pdf','2 Rubric_danh_gia_bao_cao.docx']:
    paths.append(ROOT/name)
manifest=[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(paths):z.write(p,p.relative_to(ROOT).as_posix())
    z.writestr('PACKAGE_MANIFEST.json',json.dumps(manifest,indent=2,ensure_ascii=False))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for row in manifest:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
checksum=hashlib.sha256(dest.read_bytes()).hexdigest()
(release/'robotck_project.sha256').write_text(checksum+'  robotck_project.zip\n',encoding='ascii')
print(dest);print(f'{len(manifest)} files; {dest.stat().st_size/1024**2:.1f} MiB; SHA256 {checksum}')
