#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# simplebin.py
# Simplier by 2D graph for binary data
# http://compute.2s.re.kr/pages/computing/simplebinary.php
#
# date: 2017-05-15
#
# 2017 Go Namhyeon <gnh1201@gmail.com>
#

def writeResult(data):
	print data
	
	#fh = open("./result/" + data['filename'] + ".computed.raw", 'a')
	
	#stime = data['stime']
	#svalue = data['svalue']
	
	#line = str(svalue) + '\n'
	#fh.write(line)

	return 0

def main(args):
	for dirname, dirnames, filenames in os.walk('./binaries'):
		for subdirname in dirnames:
			print(os.path.join(dirname, subdirname))

		for filename in filenames:
			fname = os.path.join(dirname, filename)
			fh = open(fname, 'rb')
			fsize = os.path.getsize(fname)
			
			if fsize <= 0:
				print str(fname) + "is 0 byte!"
				continue
			
			s_stime = 0
			s_cnt = 0
			s_odd = 0.0
			s_even = 0.0
			s_rate_odd = 0.0
			s_rate_even = 0.0
			s_rate_gap = 0.0
			s_rate_test = 0.0

			s_scan_unit = 16
			#s_scan_unit = scan_units[0] # default unit
			#for unit in scan_units:
			#	if int(fsize / unit) <= 512:
			#		s_scan_unit = unit

			isCompute = True
			while True:
				s = fh.read(1)
				if s == '':
					#break
					isCompute = False

				if isCompute == True:
					s2 = int(ord(s))
                                        if s2 >= 255:
                                            print "detected 255"
					if s2 < 128:
						s_odd += 1.0
					else:
						s_even += 1.0
					s_cnt += 1

				if isCompute == False or s_cnt >= s_scan_unit:
					if s_odd > s_even:
						s_rate_test = -( 1.0 - (s_even / s_odd) )
					elif s_odd < s_even:
						s_rate_test = 1.0 - (s_odd / s_even)
					else:
						s_rate_test = 0.0

					if s_even <= 0:
						s_rate_odd = 0.0
					else:
						s_rate_odd = s_odd / s_even

					if s_odd <= 0:
						s_rate_even = 0.0
					else:
						s_rate_even = s_even / s_odd
					
					s_rate_gap = s_rate_odd - s_rate_even
					
					s_result = {}
					s_result['svalue'] = s_rate_test
					s_result['stime'] = s_stime
					s_result['filename'] = str(filename)

					writeResult(s_result)

					# reset
					s_cnt = 0
					s_odd = 0.0
					s_even = 0.0
					s_rate_odd = 0.0
					s_rate_even = 0.0
					s_rate_gap = 0.0
					s_stime += 1

				if isCompute == False:
					break

				#if s_stime > 300:
				#	break
			
			fh.close()

	return 0

if __name__ == '__main__':
    import sys
    import os

    # set system encoding to utf-8
    reload(sys)
    sys.setdefaultencoding('utf8')
    
    # units (max 4k)
    scan_units = [4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]

    sys.exit(main(sys.argv))
