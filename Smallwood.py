# Smallwood algorithm for SRS
# Code based on "An Improved Recursive Formula For Calculating Shock Response Spectra" b David O Smallwood
from __future__ import division
import math


def get_fn():
    octave = 1/12  # a factor of 2 in frequency (next freq is twice prev) - reduces coupling of test support and electronics
    fn_min = 100
    fn_max = 100000
    n = math.ceil(math.log((fn_max/fn_min)/octave, 2))
    # import pdb
    # pdb.set_trace()
    fn = fn_min * 2 **(octave * range(0,n))
    return fn


def smallwood(input, fn):
    t_min = input[0, 0]
    t_max = input[0, -1]
    n = len(input[0])  # number time data points
    dt = (t_max - t_min) / (n-1)

    tmax1 = (t_max-t_min) + 1 / fn[1] # not sure whats this

    limit = round(t_max/dt)
    n = limit


    yy = []
    # for i in input[0]
    #    yy[i]= input[:,2]

    zeta = 0.05  # use default damping coeff

    # SRS transfer function calculations

    for i in range(1,len(fn)):
        omega_n = 2 * math.pi * fn[i]
        omega_d = omega_n * math.sqrt(1-zeta**2)
        print omega_d

#
# for i = 1:length(fn)
#     omega = 2.*pi*fn(i);
#     omegad = omega*sqrt(1.-(damp^2));
#     cosd=cos(omegad*dt);
#     sind=sin(omegad*dt);
#     domegadt=damp*omega*dt;
#
#     %smallwood algo calculations
#
#     E=exp(-damp*omega*dt);
#     K=omegad*dt;
# 	C=E*cos(K);
#     S=E*sin(K);
# 	Sp=S/K;
#
#     a1(i)=2*C;
# 	a2(i)=-E^2;
# 	b1(i)=1.-Sp;
# 	b2(i)=2.*(Sp-C);
# 	b3(i)=E^2-Sp;
#
#
#     %richman a;gp calculations
#
# %    a1(j)=2.*exp(-domegadt)*cosd;
# %    a2(j)=-exp(-2.*domegadt);
# %    b1(j)=2.*domegadt;
# %    b2(j)=omega*dt*exp(-domegadt);
# %    b2(j)=b2(j)*( (omega/omegad)*(1.-2.*(damp^2))*sind -2.*damp*cosd );
# %    b3(j)=0;
#
# %%
#
#     %transfer function values
#     forward=[ b1(i),  b2(i),  b3(i) ];
#     back   =[     1, -a1(i), -a2(i) ];
#
#
#     %MATLAB function, outputs the filtered vector 'resp' from 'y' values
#     resp = filter(forward,back,yy);
#
#     %primary response
#     primax = max(0, max(resp));
#     primin = abs(min(0,min(resp)));
#     priabs = max(primax, primin);
#
# %%
# %determination of how SRS data is selected - see SHSPEC.m for reference
#
#    jtype = abs(itype); datamax = max(abs(y));
#
#    %special case when input is zero
#    if datamax <= eps
#        if jtype < 10, SRS_data_vector(1); end
#        if jtype == 10; SRS_data_vector = zeros(1,length(fn)); end
#    end
#
#    error='error in Smallwood calculaton';
#    if jtype>10, error,itype, end
#    if itype==0, error, itype, end
#
#
#
#     SRS_data_vector(i)=priabs;
