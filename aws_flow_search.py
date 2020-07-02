import argparse
import re
import string

log_line = r'^(?P<version>\d+|-) (?P<account>$account) (?P<interface>$interface) (?P<source>$source) (?P<dest>$dest) (?P<src_port>$source_port) (?P<dst_port>$destination_port) (?P<protocol>$protocol) (?P<packets>\d+|-) (?P<bytes>\d+|-) (?P<start>\d+|-) (?P<end>\d+|-) (?P<action>$action) (?P<result>\S+|-)$$'


def prepare_regex(args: argparse.Namespace) -> re.Pattern:
    template = string.Template(log_line)
    return re.compile(template.substitute(vars(args)))


def process_logs(query: re.Pattern, args: argparse.Namespace) -> None:
    with open(args.input_file_name, 'r') as f:
        with open(args.output_file_name, 'a') as o:
            for line in f:
                
                match = query.match(line)
                
                if match is None:
                    continue
                
                named_matches = match.groupdict()
                # these if statements could probably be put into a method and refactored to be better
                # but for now this is okay
                
                if named_matches['start'] != '-' and args.start is not None and \
                        int(named_matches['start']) < args.start:
                    continue
                
                if named_matches['start'] != '-' and args.end is not None and \
                        int(named_matches['start']) > args.end:
                    continue
                
                if named_matches['bytes'] != '-' and args.bytes is not None and \
                        int(named_matches['bytes']) < args.bytes:
                    continue
                
                if named_matches['packets'] != '-' and args.packets is not None and \
                        int(named_matches['packets']) < args.packets:
                    continue
              
                #  print(f"[FOUND] {line.rstrip()}")
            
                o.write(line)


def main():
    parser = argparse.ArgumentParser(description='Tool to Search AWS PVC Flow Logs')
    parser.add_argument('-a', '--account', default=r"\d+|-", help='Account ID')
    parser.add_argument('-i', '--interface', default=r'\S+|-', help='Interface ID')
    parser.add_argument('-s', '--source', default=r'\d+\.\d+\.\d+\.\d+|-', help='Source IP Address')
    parser.add_argument('-d', '--dest', default=r'\d+\.\d+\.\d+\.\d+|-', help='Destination IP Address')
    parser.add_argument('-sp', '--source-port', default=r'\d+|-', help='Source Port')
    parser.add_argument('-dp', '--destination-port', default=r'\d+|-', help='Destination Port')
    parser.add_argument('-pk', '--packets', default=None, type=int, help='Number of Packets')
    parser.add_argument('-b', '--bytes', default=None, type=int, help='Bytes')
    parser.add_argument('-st', '--start', default=None, type=int, help='Start Time')
    parser.add_argument('-et', '--end', default=None, type=int, help='End Time')
    parser.add_argument('-at', '--action', default=r'\S+|-', help='Action')
    parser.add_argument('-pr', '--protocol', default=r'\d+|-', help='Protocol')
    parser.add_argument('-if', '--input-file-name', required=True, help='Input filename')
    parser.add_argument('-of', '--output-file-name', required=True, help='Output filename')
    args = parser.parse_args()
    query = prepare_regex(args)
    process_logs(query, args)


if __name__ == '__main__':
    main()
