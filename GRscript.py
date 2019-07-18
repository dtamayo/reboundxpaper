from subprocess import call

call("python GR.py binaries/rk4 0.080901699437494756 rk4 1 1 1e11 0.01 &", shell=True)
call("python GR.py binaries/rk2 0.080901699437494756 rk2 1 1 1e11 0.01 &", shell=True)
call("python GR.py binaries/euler 0.080901699437494756 euler 1 1 1e11 0.01 &", shell=True)
call("python GR.py binaries/implicit_midpoint 0.080901699437494756 implicit_midpoint 1 1 1e11 0.01 &", shell=True)
