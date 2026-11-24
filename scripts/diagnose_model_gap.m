function comparison=diagnose_model_gap()
% Diagnostic ablation only. Does not replace the physical evaluation plant.
root=setup_project(); ids={'circle_i3_w8_tstrhc','circle_i3_w10_tstrhc','circle_i3_w12_tstrhc'};
records=[];
for id=ids
 a=load(fullfile(root,'results',id{1},'run.mat'),'run'); physical=a.run;
 exactConfig=physical.config; exactConfig.integrator='exact';
 exact=simulate_case(exactConfig,physical.sets);
 save_run(exact,[id{1} '_exact_diagnostic']);
 design=physical; design.config.integrator='linearized_design_diagnostic';
 design=rmfield(design,{'timing','repeatTiming','repeatStatus','repeatMetrics','timingRepeats','run_id','source','timestamp'});
 c=physical.config; ref=physical.reference; N=numel(physical.t_control);
 design.q=nan(size(physical.q)); design.q(:,1)=c.q0; design.diagnostics=[];
 design.controlSeconds(:)=NaN;
 design.status='completed'; design.completedSteps=0; design.error=''; memory=struct();
 for k=1:N
  rk=struct('q',ref.q(:,k),'z',ref.z(:,k),'u',ref.u(:,k),'v',ref.v(k),'omega',ref.omega(k));
  try
   [req,w,memory,d]=controller_step(design.q(:,k),rk,c,physical.sets,memory);
   q=design.q(:,k); vw=wheel_to_body(w,c.robot); b=c.robot.b; th=q(3);
   z=q(1:2)+b*[cos(th);sin(th)];
   znext=z+c.Ts*[cos(th) -b*sin(th);sin(th) b*cos(th)]*vw;
   thnext=th+c.Ts*vw(2);
   design.q(:,k+1)=[znext-b*[cos(thnext);sin(thnext)];thnext];
   design.wheel_requested(:,k)=req; design.wheel_applied(:,k)=w;
   design.diagnostics=[design.diagnostics d]; %#ok<AGROW>
   design.completedSteps=k;
  catch ME
   design.status='failed'; design.error=getReport(ME,'extended','hyperlinks','off'); break
  end
 end
 design.errors.position=vecnorm(design.q(1:2,:)-ref.q(1:2,:));
 design.errors.heading=atan2(sin(design.q(3,:)-ref.q(3,:)),cos(design.q(3,:)-ref.q(3,:)));
 zdesign=design.q(1:2,:)+c.robot.b*[cos(design.q(3,:));sin(design.q(3,:))];
 design.errors.front=zdesign-ref.z;
 design.errors.linearizationResidual=zeros(2,N);
 design.metrics=compute_metrics(design); design.metrics.deadlineMisses=NaN;
 design.source=source_manifest();
 % Reference is sampled analytically, so its finite-difference step also has
 % a residual relative to Ts*u_r. This is retained rather than suppressed.
 design.referenceDiscretizationResidual=diff(ref.z,1,2)-c.Ts*ref.u(:,1:end-1);
 save(fullfile(root,'results',[id{1} '_design_diagnostic.mat']),'design');
 row=struct('run_id',id{1},'physicalRMSE',physical.metrics.rmse,...
     'physicalExactRMSE',exact.metrics.rmse,...
     'physicalExactMaxStateDifference',max(abs(physical.q-exact.q),[],'all'),...
     'designRMSE',design.metrics.rmse,'designStatus',design.status,...
     'physicalIndexIncreases',sum(diff([physical.diagnostics.index])>0),...
     'designIndexIncreases',sum(diff([design.diagnostics.index])>0),...
     'maxReferenceResidual',max(vecnorm(design.referenceDiscretizationResidual)));
 records=[records row]; %#ok<AGROW>
end
comparison=struct2table(records); writetable(comparison,fullfile(root,'tables','model_gap.csv'));
disp(comparison);
end
