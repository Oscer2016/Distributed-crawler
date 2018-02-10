import os 
mydir =  os.getcwd()
os.system('./setup.sh')
cmd = "sed -i '11s#obj#" + mydir + "/#' ./launcher.py"
os.system(cmd)
cmd = "sed -i '11s#obj#" + mydir + "/#' ./taobao/taobao/watchdog.py"
os.system(cmd)
