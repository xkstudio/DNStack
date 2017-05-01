#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

class rndc:

    def __init__(self):
        try:
            from isc.rndc import rndc as isc_rndc
        except:
            print 'Not Found ISC Module'


if __name__ == '__main__':
    r = rndc()
