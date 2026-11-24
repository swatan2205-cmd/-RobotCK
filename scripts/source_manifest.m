function manifest=source_manifest()
root=fileparts(fileparts(mfilename('fullpath')));
files=[dir(fullfile(root,'src','**','*.m'));dir(fullfile(root,'config','*.m'));dir(fullfile(root,'scripts','*.m'));dir(fullfile(root,'tests','*.m'));dir(fullfile(root,'setup_project.m'))];
manifest=struct('path',{},'sha256',{});
for k=1:numel(files)
    pathname=fullfile(files(k).folder,files(k).name);
    bytes=fileread(pathname); md=java.security.MessageDigest.getInstance('SHA-256');
    hash=typecast(md.digest(uint8(unicode2native(bytes,'UTF-8'))),'uint8');
    manifest(k).path=strrep(erase(pathname,[root filesep]),filesep,'/');
    manifest(k).sha256=lower(reshape(dec2hex(hash,2)',1,[]));
end
end
