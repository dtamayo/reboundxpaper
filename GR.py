import rebound
import reboundx
import numpy as np
import sys
import time

def epic(dtfactor, integrator):
    sim = rebound.Simulation()
    sim.G = 4*np.pi**2
    sim.add(m=0.93)
    sim.add(m=4.5*3.e-7, P=0.571/365.25, e=0.01)
    sim.add(m=41.*3.e-7, P=13.34/365.25, e=0.01)
    sim.move_to_com()
    sim.integrator=integrator
    sim.dt = dtfactor*sim.particles[1].P
    return sim

def addGR(sim, rebxintegrator, order, cfac):
    rebx = reboundx.Extras(sim)
    gr = rebx.add("gr")
    gr.params["c"] = 63197.8*cfac # AU/yr
    if rebxintegrator != "naive":
        rebx.integrator=rebxintegrator
        gr.operator_order = order 
        gr.force_as_operator = 1
    return rebx

dtfactor = float(sys.argv[1])
integrator = sys.argv[2]
rebxintegrator = sys.argv[3]
tmax = float(sys.argv[4])
order = int(sys.argv[5])
cfac = float(sys.argv[6])
filename = 'data/GRcfac{0}{1}rebx{2}dt{3:.3e}order{4}'.format(cfac, integrator, rebxintegrator, dtfactor, order)

Nout = 10000
sim = epic(dtfactor, integrator)
rebx = addGR(sim, rebxintegrator, order, cfac)
rebx.save(filename+'.rebx')
sim.simulationarchive_snapshot(filename+".sa")

times = np.logspace(0, np.log10(tmax), Nout)*sim.particles[1].P
for i, time in enumerate(times):
    sim.integrate(time, exact_finish_time=0)
    sim.simulationarchive_snapshot(filename+".sa")