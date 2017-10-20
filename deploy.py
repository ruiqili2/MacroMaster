import os
import subprocess
import shlex
import signal
import sys
proc1 = subprocess.Popen(shlex.split('ps aux'), stdout = subprocess.PIPE)
proc2 = subprocess.Popen(shlex.split('grep main.py'), stdin = proc1.stdout,
                         stdout = subprocess.PIPE, stderr = subprocess.PIPE)
proc3 = subprocess.Popen(shlex.split('grep 8000'), stdin = proc2.stdout, 
			 stdout = subprocess.PIPE, stderr = subprocess.PIPE)

proc4 = subprocess.Popen(shlex.split("awk '{print $2}'"), stdin = proc3.stdout,
                         stdout = subprocess.PIPE, stderr = subprocess.PIPE)

proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
proc2.stdout.close()
proc3.stdout.close()

out, err = proc4.communicate()
proc4.stdout.close()
if out != '':
	pid = int(out)
	os.kill(pid, signal.SIGKILL)
	proc4.stdout.close()
	# check if kill complete
	proc1 = subprocess.Popen(shlex.split('ps aux'), stdout = subprocess.PIPE)
	proc2 = subprocess.Popen(shlex.split('grep main.py'), stdin = proc1.stdout,
	                         stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	proc3 = subprocess.Popen(shlex.split('grep 8000'), stdin = proc2.stdout,
	                         stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	
	proc4 = subprocess.Popen(shlex.split("awk '{print $2}'"), stdin = proc3.stdout,
	                         stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	
	proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
	proc2.stdout.close()
	proc3.stdout.close()
	
	out, err = proc4.communicate()
	
	if out == '':
		print '== KILL SUCCESS =='
	else:
		print '== KILL FAILURE =='
	proc4.stdout.close()
else:
	print "== PORT CLEAN RUNNING DIRECTLY =="

child = os.fork()
if child == 0:
	print "== SUBPROCESS FOR DEPLOY =="
	os.system("nohup python main.py 8000&")
else:
	print "== PARENT PROCESS FOR RECORDING PID =="
	print "+++++++++ pid +++++++++\n"
	print "|        ", child, "       |\n"
	print "+++++++++++++++++++++++\n"
	with open("running_pid.txt", "w") as f:
		f.write(str(child))
	f.close()
		
