import rebound
import reboundx
import numpy as np
import sys

def k2137b(dtfactor, e):
    sim = rebound.Simulation()
    sim.G = 4*np.pi**2
    sim.add(m=0.463)
    sim.add(m=3.e-6, P=4.3/24/365.25, e=e)
    sim.move_to_com()
    sim.dt = dtfactor*sim.particles[1].P
    return sim

def addGR(sim, rebxintegrator, order):
    sim.integrator = "whfast"
    rebx = reboundx.Extras(sim)
    gr = rebx.load_force("gr")
    gr.params["c"] = 63197.8 # AU/yr
    intf = rebx.load_operator("integrate_force")
    intf.params['force'] = gr
    intf.params['integrator'] = reboundx.integrators[rebxintegrator]
    if order == 1:
        rebx.add_operator(intf, dt_fraction=1., timing="post")
    if order == 2:
        rebx.add_operator(intf, dt_fraction=1./2., timing="pre")
        rebx.add_operator(intf, dt_fraction=1./2., timing="post")
    return rebx, gr

filename = sys.argv[1]
dtfactor = float(sys.argv[2])
rebxintegrator = sys.argv[3]
order = int(sys.argv[4])
epsfac = float(sys.argv[5])
tmax = float(sys.argv[6])
e = float(sys.argv[7])

sim = k2137b(dtfactor=dtfactor, e=e)
rebx, gr = addGR(sim, rebxintegrator=rebxintegrator, order=order)
gr.params["c"] /= np.sqrt(epsfac)

sim.simulationarchive_snapshot(filename+".sa")
rebx.save(filename+'.rebx')

Nout = 10000
times = np.logspace(0, np.log10(tmax), Nout)*sim.particles[1].P
for i, time in enumerate(times):
    sim.integrate(time, exact_finish_time=0)
    sim.simulationarchive_snapshot(filename+".sa")