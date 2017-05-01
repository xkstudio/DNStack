#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

class rndc:

    def __init__(self,host,port,algo,secret):
        try:
            from isc.rndc import rndc as isc_rndc
            self.rndc = isc_rndc((host, int(port)), algo, secret)
        except:
            print 'Not Found ISC Module'
            self.rndc = None


    def call(self,arg):
        if self.rndc:
            data = self.rndc.call(arg)
        else:
            data = {}
        return data


    def get_status(self):
        _st = self.call('status')
        status = _st['text'].split('\n')
        return self.parse_status(status)

    def parse_status(self,status):
        data = {'version':'','uptime':'','running':'Unknown'}
        for i in status:
            i = str(i)
            if 'version:' in i:
                data['version'] = i.split('version: ')[1]
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
