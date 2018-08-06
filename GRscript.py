from subprocess import call

call("python GR.py 0.080901699437494756 whfast euler 2e10 1 1 &", shell=True)
call("python GR.py 0.080901699437494756 whfast rk2 2e10 1 1 &", shell=True)
call("python GR.py 0.080901699437494756 whfast rk4 2e10 1 1 &", shell=True)
call("python GR.py 0.080901699437494756 whfast implicit_midpoint 2e10 1 1 &", shell=True)
