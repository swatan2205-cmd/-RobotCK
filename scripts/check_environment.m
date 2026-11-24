function env = check_environment()
root=setup_project();
env.matlab=version; env.release=version('-release'); env.toolboxes=ver;
env.computer=computer; env.os=system_dependent('getos');
[~,env.hardware]=system('powershell -NoProfile -Command "Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors; Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory"');
[~,cpuJSON]=system('powershell -NoProfile -Command "Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors | ConvertTo-Json -Compress"');
env.cpu=jsondecode(cpuJSON);
[~,ramText]=system('powershell -NoProfile -Command "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory"');
env.ramBytes=str2double(strtrim(ramText));
env.fmincon=which('fmincon'); env.quadprog=which('quadprog');
env.ellipsoid=which('ellipsoid'); env.Polyhedron=which('Polyhedron');
env.optimizationLicense=license('test','Optimization_Toolbox');
env.etOK=false; env.mptOK=false;
try, e=ellipsoid(eye(2)); env.etOK=isa(e,'ellipsoid'); catch ME, env.etError=ME.message; end
try, p=Polyhedron('lb',[-1;-1],'ub',[1;1]); env.mptOK=isa(p,'Polyhedron'); catch ME, env.mptError=ME.message; end
env.ready=env.etOK && env.mptOK && env.optimizationLicense;
env.timestamp=char(datetime('now','TimeZone','Asia/Bangkok','Format','yyyy-MM-dd HH:mm:ss Z'));
save(fullfile(root,'results','environment.mat'),'env');
fid=fopen(fullfile(root,'results','environment.json'),'w','n','UTF-8');
fprintf(fid,'%s',jsonencode(env,PrettyPrint=true)); fclose(fid);
disp(env);
end
