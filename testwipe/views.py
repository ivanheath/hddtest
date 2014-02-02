from django.shortcuts import render
from django.http import HttpResponse
import os
import subprocess

def index(request):
    hddlist = []
    for i in range(97, 113):
	hddletter = chr(i)
        hdd = subprocess.Popen(["ls /sys/block | grep sd%s" %hddletter], stdout=subprocess.PIPE, shell=True)
        hdd = hdd.stdout.read().strip()
	if hdd != '':
	    hddmodel = subprocess.Popen(["sudo smartctl -a /dev/%s | grep 'Device Model'" %hdd], stdout=subprocess.PIPE, shell=True)
	    hddmodel = hddmodel.stdout.read()[14:].strip()
	    hddserial = subprocess.Popen(["sudo smartctl -a /dev/%s | grep 'Serial Number'" %hdd], stdout=subprocess.PIPE, shell=True)
	    hddserial = hddserial.stdout.read()[14:].strip()
	    hddhours = subprocess.Popen(["sudo smartctl -a /dev/%s | grep Power_On_Hours" %hdd], stdout=subprocess.PIPE, shell=True)
	    hddhours = hddhours.stdout.read()[-10:].strip()
	    hddsmart = subprocess.Popen(["sudo smartctl -H /dev/%s" %hdd], stdout=subprocess.PIPE, shell=True)
	    hddsmart = hddsmart.stdout.read()[-8:].strip()
	    if hddsmart != 'PASSED':
		hddsmart = 'FAILED'
       	    if hddserial != 'WD-WCAV90166138':
		hddlist.append(hdd)
		hddlist.append(hddmodel)
		hddlist.append(hddserial)
		hddlist.append(hddhours)
  		hddlist.append(hddsmart)
    return render(request, 'testwipe/index.html',
	{"hddlist": hddlist,
	})

def wipe(request):
    hddlist = []
    for i in range(97, 113):
        hddletter = chr(i)
        hdd = subprocess.Popen(["ls /sys/block | grep sd%s" %hddletter], stdout=subprocess.PIPE, shell=True)
        hdd = hdd.stdout.read().strip()
        if hdd != '':
            hddserial = subprocess.Popen(["sudo smartctl -a /dev/%s | grep 'Serial Number'" %hdd], stdout=subprocess.PIPE, shell=True)
            hddserial = hddserial.stdout.read()[14:].strip()
	    if hddserial != 'WD-WCAV90166138':
		subprocess.call(["dd if=/dev/zero of=/dev/%s" %hdd], shell=True)
		

    return render(request, 'testwipe/wipe.html')
