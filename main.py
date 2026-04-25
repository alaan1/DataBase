import subprocess

p1 = subprocess.Popen(["python", "bot1.py"])
p2 = subprocess.Popen(["python", "botdata.py"])

p1.wait()
p2.wait()
