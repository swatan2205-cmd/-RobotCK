function checks=run_checks()
root=setup_project(); addpath(fullfile(root,'tests'));
checks=runtests(fullfile(root,'tests')); disp(checks);
save(fullfile(root,'results','tests.mat'),'checks');
summary=struct('passed',sum([checks.Passed]),'failed',sum([checks.Failed]),...
    'incomplete',sum([checks.Incomplete]),'names',{{checks.Name}});
fid=fopen(fullfile(root,'results','test_summary.json'),'w'); fprintf(fid,'%s',jsonencode(summary,PrettyPrint=true)); fclose(fid);
assert(all([checks.Passed]),'RobotCK:Tests','Some tests failed');
end
