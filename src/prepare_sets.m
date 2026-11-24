function sets=prepare_sets(c,ref)
% Proposition 2: spherical sets only, Q_i=r_i^2 I. No general ellipsoid claim.
tic;
r=c.robot.r; d=c.robot.d; b=c.robot.b;
% Dense analytic reference bound, with outward numerical margin.
td=linspace(0,ref.t(end),max(20001,20*numel(ref.t)));
rdense=make_reference(td,c);
sets.referenceBound=max(vecnorm(rdense.u))*(1+1e-6);
sets.ru=2*c.wheelLimit*r*b/sqrt(4*b*b+d*d);
sets.r0=c.Ts*sets.referenceBound;
sets.growth=c.Ts*(sets.ru-sets.referenceBound);
sets.assumptionOK=sets.growth>0;
sets.radii=sets.r0+(0:c.Nsets)*sets.growth;
sets.Q=zeros(2,2,c.Nsets+1);
for j=1:c.Nsets+1, sets.Q(:,:,j)=sets.radii(j)^2*eye(2); end
z0=c.q0(1:2)+b*[cos(c.q0(3));sin(c.q0(3))]-ref.z(:,1);
sets.initialNorm=norm(z0); sets.initialInDomain=sets.assumptionOK && norm(z0)<=sets.radii(end);
sets.referenceWheelPeak=max(abs(ref.wheel),[],2);
sets.nominalWheelOK=all(sets.referenceWheelPeak<=c.wheelLimit+c.constraintTolerance);
sets.label='within_design_conditions';
if ~sets.assumptionOK || ~sets.initialInDomain, sets.label='outside_design_conditions'; end
sets.offlineSeconds=toc;
end
