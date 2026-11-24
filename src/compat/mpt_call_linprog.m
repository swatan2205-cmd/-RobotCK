function R=mpt_call_linprog(S)
% Compatibility adapter for MPT3 on MATLAB R2023a (removed x0 argument).
% Derived from kvasnica/mpt3 mpt_call_linprog, licensed with upstream MPT3.
% Only the call signature/options are adapted; upstream files are unmodified.
global MPTOPTIONS
if isempty(MPTOPTIONS) && ~S.test, MPTOPTIONS=mptopt; end
assert(strcmpi(S.problem_type,'LP'),'Adapter supports LP only');
options=optimoptions('linprog','Display','none');
[R.xopt,R.obj,flag,~,R.lambda]=linprog(S.f,S.A,S.b,S.Ae,S.be,S.lb,S.ub,options);
if flag>0
 R.how='ok'; if S.test, R.exitflag=1; else, R.exitflag=MPTOPTIONS.OK; end
else
 R.how='infeasible'; if S.test, R.exitflag=2; else, R.exitflag=MPTOPTIONS.INFEASIBLE; end
end
end
