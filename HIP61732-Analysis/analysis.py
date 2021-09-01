import matplotlib.pyplot as plt
import numpy as np
from astropy.timeseries import LombScargle
from lmfit import Model


t,v1,v2=np.loadtxt('HIP61732.csv',delimiter=',',unpack=True)
minP=300
maxP=900
guessV=-10
frequency1, power1 = LombScargle(t,v1).autopower(minimum_frequency=1/maxP, maximum_frequency=1/minP, samples_per_peak=20)
frequency2, power2 = LombScargle(t,v2).autopower(minimum_frequency=1/maxP, maximum_frequency=1/minP, samples_per_peak=20)

approx_period=((1/frequency2[np.argmax(power2)])+(1/frequency1[np.argmax(power1)]))*0.5
print("Initial Estimate of Period from the LombScargle(days): {}".format(approx_period))

def rad(tx,K,w,e,T0,Vo,P):
    """
    This function takes the orbital parameters as input and returns the 
    radial velocities (in km/s) as output. The input parameters are:
    tx: Array of time instants when the measurements were made (in days)
    K: Semi amplitude of the orbit (in km/s)
    w: Argument of periastron passage (in radians)
    T0: Time of periastron passage (in days)
    Vo: Systemic Velocity (in km/s)
    P: Orbital Period (in days)
    """

    M=2*np.pi*(tx-T0)/P #Mean anomaly
    E=np.pi
    for j in range(0,25):
        E=(M-e*(E*np.cos(E)-np.sin(E)))/(1-e*np.cos(E))
    th=2*np.arctan(((1+e)/(1-e))**0.5*np.tan(E/2))
    return K*(np.cos(th+w)+e*np.cos(w))+Vo

e_list=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
T0_list=np.linspace(0,max(t),25)
s1=[]
params1=[]
s2=[]
params2=[]
guessK=(max(v1)-min(v1))*0.5
for e in e_list:
    for T0 in T0_list:
        gmodel=Model(rad)
        #for Star1
        gmodel.set_param_hint('K', value=guessK, min=guessK*0.7, max=guessK*1.3)
        gmodel.set_param_hint('w', value=np.pi, min=0, max=2*np.pi)
        gmodel.set_param_hint('e', value=e, min=0, max=1)
        gmodel.set_param_hint('T0', value=T0, min=0, max=max(t))
        gmodel.set_param_hint('Vo', value=guessV,min=guessV-10,max=guessV+10)
        gmodel.set_param_hint('P', value=approx_period, min=approx_period*0.95, max=approx_period*1.05)
        result = gmodel.fit(v1, tx=t)
        K1=result.best_values['K']
        w1=result.best_values['w']
        e1=result.best_values['e']
        T01=result.best_values['T0']
        Vo1=result.best_values['Vo']
        P1=result.best_values['P']
        check=rad(t,K1,w1,e1,T01,Vo1,P1)
        sqdiff=(check-v1)**2
        s1.append(sum(sqdiff))
        params1.append([K1,w1,e1,T01,Vo1,P1])
        

        #for Star2
        guessK=(max(v2)-min(v2))*0.5
        gmodel.set_param_hint('K', value=guessK, min=guessK*0.7, max=guessK*1.3)
        gmodel.set_param_hint('w', value=np.pi, min=0, max=2*np.pi)
        gmodel.set_param_hint('e', value=e, min=0, max=1)
        gmodel.set_param_hint('T0', value=T0, min=0, max=max(t))
        gmodel.set_param_hint('Vo', value=guessV,min=guessV-10,max=guessV+10)
        gmodel.set_param_hint('P', value=approx_period, min=approx_period*0.95, max=approx_period*1.05)
        result = gmodel.fit(v2, tx=t)
        K2=result.best_values['K']
        w2=result.best_values['w']
        e2=result.best_values['e']
        T02=result.best_values['T0']
        Vo2=result.best_values['Vo']
        P2=result.best_values['P']
        check=rad(t,K2,w2,e2,T02,Vo2,P2)
        sqdiff=(check-v2)**2
        s2.append(sum(sqdiff))
        params2.append([K2,w2,e2,T02,Vo2,P2])

#The values corresponding to minimum deviation is taken as we iterate over eccentricity
K1,w1,e1,T01,Vo1,P1=params1[np.argmin(s1)]    
K2,w2,e2,T02,Vo2,P2=params2[np.argmin(s2)]

final_T0=np.mean((T01,T02))
final_Vo=np.mean((Vo1,Vo2))
final_e=np.mean((e1,e2))
final_P=np.mean((P1,P2))
final_w=np.mean((w1,w2))-np.pi/2

print("Semi Amplitudes(km/s); K1: {}".format(K1))
print("Semi Amplitudes(km/s); K2: {}".format(K2))
print("Time of Periastron passage(days); To: {}".format(final_T0))
print("Period(days); P: {}".format(final_P))
print("Systemic Velocity(km/s); Vo: {}".format(final_Vo))
print("Eccentricity; e: {}".format(final_e))
print("Argument of Periastro(degs); w: {}".format(final_w*180/np.pi))

time=np.linspace(0,max(t),300)

vr1=rad(time,K1,w1,e1,T01,Vo1,P1)
vr2=rad(time,K2,w2,e2,T02,Vo2,P2)    


plt.figure(figsize=(20,12))
plt.plot(time,vr1,'r')
plt.plot(time,vr2)
plt.plot(t,v1,'xk')
plt.plot(t,v2,'.k')
plt.grid()
plt.show()