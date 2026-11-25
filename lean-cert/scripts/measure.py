#!/usr/bin/env python3
"""Run a command; print wall time, CPU time and peak RSS of the largest child (stderr)."""
import resource, subprocess, sys, time
t = time.time()
rc = subprocess.call(sys.argv[1:])
u = resource.getrusage(resource.RUSAGE_CHILDREN)
print("MEASURE cmd=%r rc=%d wall=%.1fs user=%.1fs sys=%.1fs maxrss=%dMB" % (
    " ".join(sys.argv[1:]), rc, time.time() - t, u.ru_utime, u.ru_stime, u.ru_maxrss // 1024), file=sys.stderr)
sys.exit(rc)
