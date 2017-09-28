from subprocess import call

dtfactor = 0.1
tmax = 5.e10
integrators = [None, "implicit_midpoint", "rk4"]

for integrator in integrators:
    call("python GR.py {0} {1} {2} &".format(dtfactor, integrator, tmax), shell=True)
