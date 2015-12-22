import subprocess

subprocess.Popen('python live_stream.py', shell=True)
subprocess.Popen('python processed_stream.py', shell=True)
subprocess.Popen('python database_lookup.py', shell=True)
subprocess.call('python trigger.py', shell=True)
