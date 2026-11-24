function summary=run_suite()
root=setup_project(); c0=default_config();
cal=load(fullfile(root,'results','calibration.mat'),'selected'); c0.lyap=cal.selected;
% Fixed before formal evaluation. Same pose offsets for every wheel limit.
offsets=[0.05 0.30 0.60;0 0 0;pi/12 pi/3 pi]; limits=[8 10 12];
records=[]; plan=struct('offsets',offsets,'wheelLimits',limits,'base',c0);
save(fullfile(root,'results','evaluation_design.mat'),'plan');
for traj={'eight','circle'}
 for initial=1:3
  for limit=limits
   c=c0; c.trajectory=traj{1}; c.wheelLimit=limit;
   ref=make_reference((0:ceil(c.duration/c.Ts))*c.Ts,c);
   c.q0=ref.q(:,1)+offsets(:,initial); sets=prepare_sets(c,ref);
   for controller={'tstrhc','lyapunov'}
    c.controller=controller{1};
    id=sprintf('%s_i%d_w%d_%s',c.trajectory,initial,limit,c.controller);
    fprintf('RUN %s\n',id);
    % Warm up the same controller and local problem before timing.
    warm=c; warm.duration=c.warmupSteps*c.Ts; simulate_case(warm,sets);
    repeats=cell(1,c.timingRepeats);
    for repetition=1:c.timingRepeats, repeats{repetition}=simulate_case(c,sets); end
    run=repeats{1}; run.timingRepeats=c.timingRepeats;
    run.repeatTiming=cellfun(@(r)r.controlSeconds,repeats,'UniformOutput',false);
    run.repeatStatus=cellfun(@(r)r.status,repeats,'UniformOutput',false);
    run.repeatMetrics=cellfun(@(r)r.metrics,repeats,'UniformOutput',false);
    allTimes=[run.repeatTiming{:}]; allTimes=allTimes(isfinite(allTimes));
    run.timing.mean=mean(allTimes); run.timing.p95=prctile(allTimes,95);
    run.timing.maximum=max(allTimes); run.timing.deadlineMisses=sum(allTimes>c.Ts);
    run.timing.repeatMeans=cellfun(@(r)r.metrics.meanControlSeconds,repeats);
    run.timing.stdRepeatMeans=std(run.timing.repeatMeans);
    if isempty(allTimes)
        run.timing.mean=NaN; run.timing.p95=NaN; run.timing.maximum=NaN; run.timing.deadlineMisses=NaN;
    end
    save_run(run,id);
    row=run.metrics; row.run_id=id; row.trajectory=c.trajectory; row.initial=initial;
    row.wheelLimit=limit; row.controller=c.controller; row.status=run.status;
    row.conditions=sets.label; row.completedSteps=run.completedSteps;
    row.timingMean5=run.timing.mean; row.timingP955=run.timing.p95;
    row.timingMax5=run.timing.maximum; row.deadlineMisses5=run.timing.deadlineMisses;
    row.timingStdMeans5=run.timing.stdRepeatMeans;
    records=[records row]; %#ok<AGROW>
   end
  end
 end
end
summary=struct2table(records); writetable(summary,fullfile(root,'tables','summary.csv'));
save(fullfile(root,'results','suite.mat'),'summary','plan');
disp(summary(:,{'run_id','status','rmse','iae','conditions'}));
end
