#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
import socket

class rndc:

    def __init__(self,host,port,algo,secret):
        self.err_msg = ''
        try:
            from isc.rndc import rndc as isc_rndc
            self.rndc = isc_rndc((host, int(port)), algo, secret)
        except ImportError:
            self.err_msg = 'Not Found ISC (RNDC) Module'
            print self.err_msg
            self.rndc = None
        except socket.error, e: # 网络层问题，rndc_host或者rndc_port错了
            self.err_msg = 'RNDC: Can not connect to DNS Server'
            print 'Socket Error'
            #print e # [Errno 111] Connection refused
            self.rndc = None
        except Exception, e: # Key错误时有出现该错误
            self.err_msg = 'RNDC Config Error'
            print type(e) # <type 'exceptions.TypeError'>
            print e # Incorrect padding
            self.rndc = None


    def call(self,arg):
        if self.rndc:
            data = self.rndc.call(arg)
        else:
            data = {}
        return data


    def get_status(self):
        _st = self.call('status')
        if 'text' in _st:
            status = _st['text'].split('\n')
            return self.parse_status(status)
        else:
            return {}


    def parse_status(self,status):
        data = {'version':'','uptime':'','running':'Unknown'}
        for i in status:
            i = str(i)
            if 'version:' in i:
                v = i.split('version: ')[1]
                data['version'] = v.split(' ')[1]
            elif 'boot time: ' in i:
                data['uptime'] = i.split('boot time: ')[1]
            elif 'boot time: ' in i:
                data['uptime'] = i.split('boot time: ')[1]
            elif i == 'server is up and running':
                data['running'] = 'Running'
        return data


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 953
    algo = 'md5'
    secret = 'kzIcztY4+xH0Px2SrsZyGQ=='
    r = rndc(host,port,algo,secret)
    print r.get_status()
