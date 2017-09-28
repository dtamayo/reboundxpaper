import rebound
import reboundx
import numpy as np
import sys
import time

def wasp19b(dtfactor):
    sim = rebound.Simulation()
    sim.G = 4*np.pi**2
    sim.add(m=1.05)
    sim.add(m=1.1e-3, P=0.789/365.25, e=0.005)
    sim.move_to_com()
    sim.integrator="whfast"
    sim.dt = dtfactor*sim.particles[1].P
    return sim

def addGR(sim, integrator):
    rebx = reboundx.Extras(sim)
    gr = rebx.add("gr")
    gr.params["c"] = 63197.8 # AU/yr
    if integrator is not None:
        rebx.integrator=integrator
        gr.operator_order = 1
        gr.force_as_operator = 1
    return rebx

def makeSA(filename, dtfactor, integrator):
    sim = wasp19b(dtfactor)
    rebx = addGR(sim, integrator)
    
    sim.initSimulationArchive(filename+'.sa', interval=1.e6*sim.particles[1].P) 
    rebx.save(filename+'.rebx')
    return sim, rebx

dtfactor = float(sys.argv[1])
integrator = sys.argv[2]
tmax = float(sys.argv[3])
filename = 'data/{0}dt{1:.3e}'.format(integrator, dtfactor)

try:
    sim = rebound.Simulation.from_archive(filename+'.sa')
    sim.simulationarchive_filename = filename+'.sa'
    rebx = reboundx.Extras.from_file(filename+'.rebx')
except:
    sim, rebx = makeSA(filename, dtfactor, integrator)

t0 = time.time()
sim.integrate(tmax*sim.particles[1].P)
tf = time.time()
    
with open(filename+".txt", "a") as f:
    f.write("{0:e}\n".format(tf-t0))

