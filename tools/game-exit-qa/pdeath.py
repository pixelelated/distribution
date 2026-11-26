#!/usr/bin/env python3
import ctypes,os,signal,sys
parent=int(sys.argv[1]);lib=ctypes.CDLL(None,use_errno=True)
if lib.prctl(1,signal.SIGKILL)!=0 or os.getppid()!=parent:os._exit(125)
os.execv(sys.argv[2],sys.argv[2:])
