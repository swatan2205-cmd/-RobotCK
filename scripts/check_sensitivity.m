function sensitivity=check_sensitivity()
root=setup_project(); c=default_config(); cal=load(fullfile(root,'results','calibration.mat')); c.lyap=cal.selected;
rows=[];
for traj={'eight','circle'}
 for ctrl={'tstrhc','lyapunov'}
  c.trajectory=traj{1}; c.controller=ctrl{1}; ref=make_reference(0,c);
  c.q0=ref.q+[.3;0;pi/3];
  c.integrator='ode45'; base=simulate_case(c); save_run(base,['sensitivity_' c.trajectory '_' c.controller '_ode45']);
  c.integrator='exact'; exact=simulate_case(c); save_run(exact,['sensitivity_' c.trajectory '_' c.controller '_exact']);
  row=struct('trajectory',c.trajectory,'controller',c.controller,'baseStatus',base.status,...
      'exactStatus',exact.status,'maxStateDifference',max(abs(base.q-exact.q),[],'all'),...
      'rmseDifference',abs(base.metrics.rmse-exact.metrics.rmse));
  rows=[rows row]; %#ok<AGROW>
 end
end
sensitivity=struct2table(rows); writetable(sensitivity,fullfile(root,'tables','sensitivity.csv'));
save(fullfile(root,'results','sensitivity.mat'),'sensitivity'); disp(sensitivity);
end
