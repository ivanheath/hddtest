from django.shortcuts import render
from django.http import HttpResponse
import os
import subprocess

def index(request):
    harddrivelist = []
    for i in range(97, 114):
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
	    hddlocation = subprocess.Popen(["file /sys/block/%s" %hdd], stdout=subprocess.PIPE, shell=True)
	    hddlocation = hddlocation.stdout.read()[-20:-18].strip()
	    hddlocation = locator(hddlocation)
	    if hddsmart != 'PASSED':
		hddsmart = 'FAILED'
       	    if hddserial != 'WD-WCAV90166138':
		currenthdd = harddrive(hdd, hddmodel, hddserial, hddhours, hddsmart, hddlocation)
		harddrivelist.append(currenthdd)
   # harddrivelist.sort(key=lambda x: x.location)
    #for y in harddrivelist:
#	if y.location != y: 
 # 	    currenthdd = harddrive('empty', '', '', '', '', y)
  #          harddrivelist.append(currenthdd)

    harddrivelist.sort(key=lambda x: x.location)

    return render(request, 'testwipe/index.html',
	{"harddrivelist": harddrivelist,
	})

def wipe(request):
    hddlist = []
    wipestring = "dcfldd pattern=00 "
    for i in range(97, 113):
        hddletter = chr(i)
        hdd = subprocess.Popen(["ls /sys/block | grep sd%s" %hddletter], stdout=subprocess.PIPE, shell=True)
        hdd = hdd.stdout.read().strip()
        if hdd != '':
            hddserial = subprocess.Popen(["sudo smartctl -a /dev/%s | grep 'Serial Number'" %hdd], stdout=subprocess.PIPE, shell=True)
            hddserial = hddserial.stdout.read()[14:].strip()
	    if hddserial != 'WD-WCAV90166138':
		wipestring = wipestring + "of=/dev/%s " %hdd

    subprocess.call([wipestring], shell=True)
		

    return render(request, 'testwipe/wipe.html')

class harddrive:

    def __init__(self, sd, model, serial, hours, smart, location):
	self.sd = sd
	self.model = model
	self.serial = serial
	self.hours = hours
	self.smart = smart
	self.location = location

def locator(location):

    if location == '12':
	location = 1
    elif location == '13':
	location = 2
    elif location == '14':
	location = 3
    elif location == '15':
	location = 4
    elif location == '/8':
	location = 5
    elif location == '/9':
	location = 6
    elif location == '10':
	location = 7
    elif location == '11':
	location = 8
    elif location == '/4':
	location = 9
    elif location == '/5':
	location = 10
    elif location == '/7':
	location = 11
    elif location == '/6':
	location = 12
    elif location == '/0':
	location = 13
    elif location == '/1':
	location = 14
    elif location == '/2':
	location = 15
    elif location == '/3':
	location = 16
    return location
