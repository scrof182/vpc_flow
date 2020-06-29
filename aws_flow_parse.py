## allows quick searching of AWS VPC flow logs 
## AWS docs
## https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
## Sample logs:
## 2 123456789010 eni-1235b8ca123456789 172.31.9.69 172.31.9.12 49761 3389 6 20 4249 1418530010 1418530070 REJECT OK
## 2 123456789010 eni-1235b8ca123456789 172.31.16.139 172.31.16.21 20641 22 6 20 4249 1418530010 1418530070 ACCEPT OK
## Regex to parse: 
## ^(\d+) (\d+) (\S+) (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\S+) (\S+)$
## Fields, in order:
## version, account_id, interface_id, source_address, destination_address, source_port, destination_port, protocol, packets, bytes, start, end, action, log_status

import argparse
import re

parser = argparse.ArgumentParser(description='Tool to Search AWS PVC Flow Logs')
parser.add_argument('-a', '--account', help='Account ID')
parser.add_argument('-i', '--interface', help='Interface ID')
parser.add_argument('-s', '--source', help='Source IP Address')
parser.add_argument('-d', '--dest', help='Destination IP Address')
parser.add_argument('-sp', '--source_port', help='Source Port')
parser.add_argument('-dp', '--destination_port', help='Destination Port')
parser.add_argument('-pk', '--packets', help='Number of Packets')
parser.add_argument('-b', '--bytes', help='Bytes')
parser.add_argument('-st', '--start', help='Start Time')
parser.add_argument('-et', '--end', help='End Time')
parser.add_argument('-at', '--action', help='Action')
parser.add_argument('-pr', '--protocol', help='Protocol')
parser.add_argument('-if', '--input_file_name', help='File Name')
parser.add_argument('-of', '--output_file_name', help='File Name')
args = parser.parse_args()

## Good logs
test_log = "2 123456789010 eni-1235b8ca123456789 172.31.16.139 172.31.16.21 20641 22 6 20 4249 1418530010 1418530070 ACCEPT OK"
regex = "^(\d+) (\d+) (\S+) (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\S+) (\S+)$"
reg_parser = re.compile(regex)

## Bad Logs
bad_log = "2 123456789010 eni-1235b8ca123456789 - - - - - - - 1418530010 1418530070  - NODATA"
bad_regex = "^(\d) (\d+) (\S+) (-) (-) (-) (-) (-) (-) (-) (\d+) (\d+) (-) ((SKIPDATA)|(NODATA))$"
bad_reg_parser = re.compile(bad_regex)
bad_line_count = 0

with open(args.input_file_name, 'r') as f:
	for test_log in f:

		line_tester = reg_parser.match(test_log)
		bad_line_tester = bad_reg_parser.match(test_log)

		if line_tester is not None:
			version = line_tester.group(1)
			account_id = line_tester.group(2)
			interface_id= line_tester.group(3)
			source_address = line_tester.group(4)
			destination_address = line_tester.group(5)
			source_port = line_tester.group(6)
			destination_port = line_tester.group(7)
			protocol = line_tester.group(8)
			packets = line_tester.group(9)
			bits = line_tester.group(10)
			start = line_tester.group(11)
			end = line_tester.group(12)
			action = line_tester.group(13)
			log_status = line_tester.group(14)


			## account testing
			if args.account is not None and account_id != args.account:
				test_log = ""

			## interface testing
			if args.interface is not None and interface_id != args.interface:
				test_log = ""

			## Source IP Testing
			if args.source is not None and source_address != args.source:
				test_log = ""

			## Dest IP Testing
			if args.dest is not None and destination_address != args.dest:
				test_log = ""
			
			## Source Port Testing
			if args.source_port is not None and source_port != args.source_port:
				test_log = ""

			## Dest port Testing
			if args.destination_port is not None and destination_port != args.destination_port:
				test_log = ""

			## protocol
			if args.protocol is not None and protocol != args.protocol:
				test_log = ""

			## packets
			if args.packets is not None and packets != args.packets:
				test_log = ""

			## bytes
			if args.bytes is not None and bits != args.bytes:
				test_log = ""

			## action
			if args.action is not None and action != args.action:
				test_log = ""

			## start time range
			if args.start is not None and int(args.start) > int(start):
				test_log = ""

			## end time range
			if args.end is not None and int(args.end) < int(start):
				test_log = ""

			#write log line if everything passes	
			if len(test_log) >= 0:
				with open(args.output_file_name, 'a') as o:
					o.write(test_log)

		elif bad_line_tester is not None: 
			bad_line_count += 1

		else:
			print("This Line Did Not Parse Correctly: " + test_log)

print("Bad Line Count: " + str(bad_line_count))
