function comparison=compare_baseline(profile)
if nargin<1, profile='author'; end
root=setup_project(); b=load(fullfile(root,'results','baseline','baseline.mat')); b=b.result;
assert(strcmp(b.status,'completed'),'Baseline did not complete');
c=default_config(); c.duration=numel(b.t)*b.Ts;
c.solverProfile=profile;
if strcmp(profile,'author'), c.integrator='author'; else, c.integrator='ode45'; end
ref=make_reference((0:numel(b.t))*c.Ts,c); sets=prepare_sets(c,ref);
% Exactly the author's sampled disturbance and matrices for this comparison.
sets.Q=reshape(b.Q_k,2,2,[]); sets.radii=squeeze(sqrt(sets.Q(1,1,:)))';
sets.r0=sets.radii(1); sets.referenceBound=sets.r0/c.Ts;
sets.growth=sets.radii(2)-sets.radii(1); sets.assumptionOK=sets.growth>0;
r=simulate_case(c,sets); save_run(r,['baseline_' profile]);
comparison.status=r.status;
comparison.maxStateDifference=max(abs(r.q-b.q),[],'all');
comparison.maxWheelDifference=max(abs(r.wheel_applied-b.wheel),[],'all');
comparison.stateTolerance=1e-3; comparison.wheelTolerance=0.1;
comparison.rationale='Match author solver options and ode45 output grid; 1 mm and 1 percent of 10 rad/s are predeclared numerical acceptance bounds.';
comparison.pass=strcmp(r.status,'completed') && comparison.maxStateDifference<=comparison.stateTolerance && comparison.maxWheelDifference<=comparison.wheelTolerance;
name='baseline_comparison';
if ~strcmp(profile,'author'), name=['baseline_comparison_' profile]; end
save(fullfile(root,'results',[name '.mat']),'comparison');
fid=fopen(fullfile(root,'results',[name '.json']),'w'); fprintf(fid,'%s',jsonencode(comparison,PrettyPrint=true)); fclose(fid);
disp(comparison);
end
