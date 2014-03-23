from django.shortcuts import render
from django.http import HttpResponse
import os
import subprocess

def clean(request):
    #hddlist = []
    #cleanstring = "dcfldd pattern=00 bs=512 count=1024 "
    #raidstring = "dcfldd pattern=00 bs=512 count=2048 "
    for i in range(98, 122):
	hddletter = chr(i)
	hdd = subprocess.Popen(["ls /sys/block | grep sd%s" %hddletter], stdout=subprocess.PIPE, shell=True)
	hdd = hdd.stdout.read().strip()
	if hdd != '':
	    cleanstring = "dcfldd pattern=00 bs=512 count=1024 of=/dev/%s " %hdd
	    blockcount = subprocess.Popen(["blockdev --getsz /dev/%s" %hdd], stdout=subprocess.PIPE, shell=True)
	    blockcount = blockcount.stdout.read().strip()
	    blockcount = int(blockcount)
	    blockcount = blockcount - 2048
	    raidstring = "dcfldd pattern=00 bs=512 count=2048 seek=%s of=/dev/%s" %(blockcount, hdd)
	    subprocess.call([cleanstring], shell=True)
	    subprocess.call([raidstring], shell=True)

    return HttpResponse('works')
