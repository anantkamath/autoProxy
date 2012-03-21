#!/usr/bin/env python
#    
#    Copyright (C) 2012 Anant Kamath
#    
#    Author: Anant Kamath <kamathanant@gmail.com>
#
#
#
#    This program changes detects change in the ip of the active network device and ascertains the location based on the ip, and sets the
#    system-wide & apt.conf proxies accordingly.
#


import dbus 
from xml.etree import ElementTree as ET #To parse dbus introspection xml output
import socket #Used here only to convert ip address to human readable form 
import struct #Used here only to convert ip address to human readable form
import gconf #Used to write settings to the gconf server
import time #Sleep

APT_CONFIG_FILE='/etc/apt/apt.conf.d/apt.conf' #Path to apt config file. Change according to your distro/DE

hostel_username='username'#Change this
hostel_password='password'#Change this


CHECK_INTERVAL=1 #In seconds

class locationSettings: #Elegance?  :)
	def __init__(self,proxy=None,port=None,user=None,pwd=None,apt_proxy=None,apt_port=None):
		
		self.proxy_ip=proxy
		self.proxy_port=port
		self.username=user
		self.password=pwd
		self.apt_proxy_ip=apt_proxy
		self.apt_proxy_port=apt_port
	
	
	
def currentIP(): #Functions on the internet to find the ip address usually require passing a device name as an argument. This one takes care of that automatically.
	element=ET.XML(dbus.SystemBus().get_object('org.freedesktop.NetworkManager','/org/freedesktop/NetworkManager/ActiveConnection').Introspect(dbus_interface='org.freedesktop.DBus.Introspectable'))

	l=[]
	for subelement in element:
		a= subelement.attrib
		l.append(a)
	
	if(len(l)<1):
		return ''
	a,b = l[0].popitem() #Get the object name of the active connection. There must be a simpler way than this, but this works.

  
	
	active_conn = dbus.SystemBus().get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager/ActiveConnection/'+b)
	properties_manager=dbus.Interface(active_conn, 'org.freedesktop.DBus.Properties')
	device_path= properties_manager.Get('org.freedesktop.NetworkManager.Connection.Active','Devices')

	device = dbus.SystemBus().get_object('org.freedesktop.NetworkManager',device_path[0])
	properties_manager=dbus.Interface(device, 'org.freedesktop.DBus.Properties')
	
	ip=properties_manager.Get('org.freedesktop.NetworkManager.Device','Ip4Address')
	
	
	ip=  socket.inet_ntoa(struct.pack("<L", ip)) # To convert ip to human readable form
	
	return ip
if(currentIP().startswith("10.")):
	print "in BITS"
else:
	print "datacard"

def setVars(): 
	
	if(currentIP().startswith("10.")):
		username=hostel_username
		password=hostel_password
		if(currentIP().startswith("10.3.1")): #AH1
			pIp='10.1.9.30'
			pPort='8080'
		elif(currentIP().startswith("10.3.3")):	 #AH2
			pIp='10.1.9.31'
			pPort='8080'
		elif(currentIP().startswith("10.3.6")):	 #AH3
			pIp='10.1.9.32'
			pPort='8080'
		
		elif(currentIP().startswith("10.3.8")):	 #AH4
			pIp='10.1.9.33'
			pPort='8080'
			
		elif(currentIP().startswith("10.3.10")): #AH5
			pIp='10.1.9.34'
			pPort='8080'
		elif(currentIP().startswith("10.3.11")): #AH6
			pIp='10.1.9.35'
			pPort='8080'
		elif(currentIP().startswith("10.3.12")):#AH7
			pIp='10.1.9.36'
			pPort='8080'
		
		elif(currentIP().startswith("10.3.14")):#AH8
			pIp='10.1.9.37'
			pPort='8080'
		elif(currentIP().startswith("10.4.1")):#CH1
			pIp='10.1.9.20'
			pPort='8080'
		elif(currentIP().startswith("10.4.3")):#CH2
			pIp='10.1.9.21'
			pPort='8080'
		elif(currentIP().startswith("10.4.5")):#CH3
			pIp='10.1.9.22'
			pPort='8080'
		elif(currentIP().startswith("10.4.12")):#CH4
			pIp='10.1.9.23'
			pPort='8080'
		elif(currentIP().startswith("10.4.9")):#CH5
			pIp='10.1.9.24'
			pPort='8080'
		elif(currentIP().startswith("10.4.14") or currentIP().startswith("10.4.15")):#CH6
			pIp='10.1.9.24'
			pPort='8080'	
			
		elif(currentIP().startswith("10.20.")):	 #AWing+CWing+Library Wifi ?
			pIp='10.1.1.26'
			pPort='8080'
			username='' #We don't want a username outside hostels
			password=''
			
		elif(currentIP().startswith("10.2.3.")):	 #VLSI Lab Wired connection
			pIp='10.1.1.25'
			pPort='8090'
			username='' #We don't want a username outside hostels
			password=''
			
		elif(currentIP().startswith("10.20.")):	 #Main building
			pIp='10.1.1.26'
			pPort='8080'
			username='' #We don't want a username outside hostels
			password=''
			
			
				
			
			
		current_location_settings=locationSettings(pIp,pPort,username,password,'10.1.1.224','3142')
		
		
	else:#Datacard or home net or anything else which doesn't need proxies...
		pIp=''
		pPort=''
		current_location_settings=locationSettings(pIp,pPort,'','','','')
	save(current_location_settings)
	
def save(settings):

	gconf_dir='/system/http_proxy'  # GConf prefix


	gclient = gconf.client_get_default()  # create a client object
	gclient.suggest_sync()
    

	gvalue = gconf.Value(gconf.VALUE_STRING)
	gvalue.set_string(settings.proxy_ip)
	gclient.set(gconf_dir+'/host', gvalue)

	gvalue = gconf.Value(gconf.VALUE_INT)
	gvalue.set_int(settings.proxy_port)
	gclient.set(my_gconf_dir+'/port', gvalue)
    
	gvalue = gconf.Value(gconf.VALUE_BOOL)
	gvalue.set_bool(True)
	gclient.set(my_gconf_dir+'/use_http_proxy', gvalue)

	gvalue = gconf.Value(gconf.VALUE_BOOL)
	gvalue.set_bool(True)
	gclient.set(my_gconf_dir+'/use_same_proxy', gvalue)

	if(settings.username!=''):
		gvalue = gconf.Value(gconf.VALUE_BOOL)
		gvalue.set_bool(True)
		gclient.set(my_gconf_dir+'/use_authentication', gvalue)
		gvalue = gconf.Value(gconf.VALUE_STRING)
		gvalue.set_string(settings.username)
		gclient.set(gconf_dir+'/authentication_user', gvalue)
		gvalue = gconf.Value(gconf.VALUE_STRING)
		gvalue.set_string(settings.password)
		gclient.set(gconf_dir+'/authentication_password', gvalue)		
     
	else:
		gvalue = gconf.Value(gconf.VALUE_BOOL)
		gvalue.set_bool(False)
		gclient.set(my_gconf_dir+'/use_authentication', gvalue)	     
	     


	gclient.suggest_sync()





	lines=''

	if(settings.apt_proxy_ip):
		line1 = 'Acquire::http::proxy "http://'+settings.apt_proxy_ip+':'+settings.apt_proxy_port+'/";'    
		line2 = 'Acquire::https::proxy "https://'+settings.apt_proxy_ip+':'+settings.apt_proxy_port+'/";'     
		line3 = 'Acquire::ftp::proxy "ftp://'+settings.apt_proxy_ip+':'+settings.apt_proxy_port+'/";'  
		line4 = 'Acquire::socks::proxy "socks://'+settings.apt_proxy_ip+':'+settings.apt_proxy_port+'/";' 
		
		lines = line1+'\n'+line2+'\n'+line3+'\n'+line4
	
	f = open(APT_CONFIG_FILE,'w')
        f.write(lines)
        f.close()	
          
	

	
while(1):	
	setVars()#If you want add something to check if ip has really changed in the last one second, to reduce number config file writes, but this works too	
	time.sleep(1)           
        



         