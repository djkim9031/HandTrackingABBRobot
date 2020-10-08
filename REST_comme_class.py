# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 12:53:02 2020

@author: KRDOKIM13
"""
import requests
from requests.auth import HTTPDigestAuth

class methods:
    def __init__(self,username,password,address):
        self.host=''
        self.username=username
        self.password=password
        self.payload={}
        #self.dataType=''
        self.digest_auth=HTTPDigestAuth(self.username,self.password)
        self.session=requests.Session()
        self.post_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
        self.count=0
        self.count_closed=0
        self.count_opened=0
        self.count_ok=0
        self.address = address
                
    def post(self,host,payload):
        #POST Method to update data 
        self.host=host
        self.payload=payload
        self.session.post(self.host,auth=self.digest_auth,headers=self.post_headers,data=self.payload)
        #self.cookies='-http-session-={0}; ABBCX={1}'.format(temp.cookies['-http-session-'], resp.cookies['ABBCX']
    
    def get(self,host,payload):
        #in case get method is necessary in the future
        return
        
    def close(self):
        self.close()
        

def mastership_request(ROB):
    address = ROB.address
    host = 'http://'+address+'/rw/rapid/execution?action=request'
    payload={}
    resp = ROB.post(host, payload)
    return resp

def reset_pp(ROB):
    address = ROB.address
    host = 'http://'+address+'/rw/rapid/execution?action=resetpp'
    payload={}
    resp = ROB.post(host,payload)
    return resp

def set_signal(ROB,signal,value):
    address = ROB.address
    host = 'http://'+address+'/rw/iosystem/signals/'+signal+'?action=set'
    payload={'lvalue':str(value)}
    resp = ROB.post(host,payload)
    return resp

def execute(ROB,runmode):
    address=ROB.address
    host = 'http://'+address+'/rw/rapid/execution?action=start'
    payload = {'regain':'continue',
               'execmode':'continue',
               'cycle':runmode,
               'condition':'none',
               'stopatbp':'enabled',
               'alltaskbytsp':'true'}
    resp = ROB.post(host,payload)
    return resp

def stop(ROB):
    address=ROB.address
    host = 'http://'+address+'/rw/rapid/execution?action=stop'
    payload = {}
    resp = ROB.post(host,payload)
    return resp

def set_val(ROB,value,y,z):
    address=ROB.address
    host = 'http://'+address+'/rw/rapid/symbol/data/RAPID/T_ROB_L/Module1/'+value+'?action=set'
    print(y,z)
    payload={'value':'[0,'+str(-y/2)+','+str(z/2)+',0,0,0]'}
    resp = ROB.post(host,payload)
    return resp
    
