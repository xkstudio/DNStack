#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

class rndc:

    def __init__(self,host,port,algo,secret):
        try:
            from isc.rndc import rndc as isc_rndc
        except:
            print 'Not Found ISC Module'
            isc_rndc = None
        self.rndc = isc_rndc((host,int(port)),algo,secret)
        self.call = self.rndc.call

    def get_status(self):
        _st = self.call('status')
        status = _st['text'].split('\n')
        return status



if __name__ == '__main__':
    host = '127.0.0.1'
    port = 953
    algo = 'md5'
    secret = 'kzIcztY4+xH0Px2SrsZyGQ=='
    r = rndc(host,port,algo,secret)
    print r.get_status()
