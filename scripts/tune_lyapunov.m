function selected=tune_lyapunov()
root=setup_project(); c=default_config(); c.duration=22; c.controller='lyapunov';
c.integrator='exact'; % Same zero-order-held kinematics; checked against ode45.
% Separate calibration poses and duration, never use the official test scores.
kgrid=[0.5 1 2]; gain=[0.5 1 2]; rows=[]; best=Inf; selected=c.lyap;
for aval=[2.1 7]
 for nval=[-1 0 1 2]
for kval=kgrid
 for kx=gain
  for ks=gain
   c.lyap=struct('k',kval,'kx',kx,'ks',ks,'a',aval,'n',nval);
   score=0;
   for trajectory={'eight','circle'}
    c.trajectory=trajectory{1}; ref=make_reference(0,c);
    for offset=[0.15 0.45]
     c.q0=ref.q(:,1)+[offset;-offset/2;pi/6];
     sets=struct(); r=simulate_case(c,sets);
     score=score+r.metrics.rmse;
    end
   end
   rows=[rows; kval kx ks aval nval score]; %#ok<AGROW>
   if score<best, best=score; selected=c.lyap; end
  end
 end
end
 end
end
calibration=array2table(rows,'VariableNames',{'k','kx','ks','a','n','sumRMSE'});
save(fullfile(root,'results','calibration.mat'),'calibration','selected');
writetable(calibration,fullfile(root,'tables','calibration.csv'));
disp(selected);
end
