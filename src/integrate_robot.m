function next=integrate_robot(q,w,c)
vw=wheel_to_body(w,c.robot); v=vw(1); omega=vw(2);
switch c.integrator
    case 'author'
        [~,qs]=ode45(@(~,s)[v*cos(s(3));v*sin(s(3));omega],0:1e-5:c.Ts,q);
        next=qs(end,:)';
    case 'ode45'
        options=odeset('RelTol',c.RelTol,'AbsTol',c.AbsTol);
        [~,qs]=ode45(@(~,s)[v*cos(s(3));v*sin(s(3));omega],[0 c.Ts],q,options);
        next=qs(end,:)';
    case 'exact'
        angle=q(3)+omega*c.Ts;
        if abs(omega)<1e-10
            next=q+[v*c.Ts*cos(q(3));v*c.Ts*sin(q(3));omega*c.Ts];
        else
            next=q+[v/omega*(sin(angle)-sin(q(3)));v/omega*(cos(q(3))-cos(angle));omega*c.Ts];
        end
    case 'euler'
        next=q+c.Ts*[v*cos(q(3));v*sin(q(3));omega];
    otherwise, error('RobotCK:Integrator','Unknown integrator');
end
end
