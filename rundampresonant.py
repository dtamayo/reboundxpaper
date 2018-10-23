import rebound
import reboundx
from celmech import Andoyer
import numpy as np
import sys

def damp(integrator, tmax, taue, scheme="", dtfactor=0.05, j=3, k=1):
    avars = Andoyer.from_elements(j=j, k=k, Zstar=0.1, libfac=0.2, m1=1.e-4, m2=1.e-12)
    sim = avars.to_Simulation()

    sim.integrator=integrator
    if integrator=="whfast":
        sim.dt = dtfactor*sim.particles[1].P

    ps = sim.particles
    P = ps[1].P
    tmax *= P
    rebx = reboundx.Extras(sim)
    mod = rebx.add("modify_orbits_forces")
    if scheme:
        rebx.integrator=scheme
        mod.operator_order = 1
        mod.force_as_operator = 1

    Nout = 1.e4
    filename = 'data/'+integrator+scheme+"taue{0:2e}.bin".format(taue)
    sim.automateSimulationArchive(filename,interval=tmax/Nout,deletefile=True)

    times = np.linspace(0, tmax, Nout)
    for i, time in enumerate(times):
        for p in ps[1:]:
            p.params['tau_e'] = -taue*ps[1].P
        ps[1].params['tau_a'] = taue*ps[1].P*100
        sim.integrate(time, exact_finish_time=0)

if __name__ == "__main__":
    integrator=sys.argv[1]
    tmax = float(sys.argv[2])
    taue = float(sys.argv[3])
    try:
        scheme = sys.argv[4]
    except:
        scheme = ''
    damp(integrator=integrator, tmax=tmax, taue=taue, scheme=scheme)
