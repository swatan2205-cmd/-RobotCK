function root = setup_project()
% Session-local paths only; never calls savepath or changes startup.m.
persistent etInitialized
root=fileparts(mfilename('fullpath'));
addpath(root,fullfile(root,'src'),fullfile(root,'config'),fullfile(root,'scripts'));
deps=dir(fullfile(root,'external','mpt3','mpt3-*'));
if ~isempty(deps), addpath(genpath(fullfile(deps(1).folder,deps(1).name,'source'))); end
deps=dir(fullfile(root,'external','et','ellipsoids-*'));
if ~isempty(deps)
    p=fullfile(deps(1).folder,deps(1).name);
    % Package directories themselves must not be added to MATLAB's path.
    addpath(genpath(fullfile(p,'products')),genpath(fullfile(p,'lib')),fullfile(p,'install'));
    jar=fullfile(p,'lib','jmodgen','FileUtils','bin','modgenfileutils.jar');
    if ~any(strcmp(javaclasspath('-dynamic'),jar)), javaaddpath(jar); end
    % Only ET construction/plotting is used. Initialize its configuration via
    % the public API without requesting unrelated CVX/SDP methods.
    if isempty(etInitialized)
        crm=elltool.conf.ConfRepoMgr(); crm.selectConf('default');
        elltool.conf.Properties.setConfRepoMgr(crm);
        elltool.logging.Log4jConfigurator.configure(crm,'islockafterconfigure',true);
        etInitialized=true;
    end
end
addpath(fullfile(root,'src','compat'),'-begin');
end
