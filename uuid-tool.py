#! /usr/bin/env python3

import uuid
import datetime
import sys
import argparse


def UUIDTime(u):
    dt_zero = datetime.datetime(1582, 10, 15)
    return dt_zero + datetime.timedelta(microseconds=u.time//10)

def UUIDMac(u):
    # https://www.geeksforgeeks.org/extracting-mac-address-using-python/
    return ":".join(['{:02x}'.format((u.node >> ele) & 0xff) for ele in range (0, 8*6,8)][::-1])

# Taken from Python's UUID library
def uuid1(node, clock_seq, timestamp):
    """Generate a UUID from a host ID, sequence number, and the current time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen."""

    time_low = timestamp & 0xffffffff
    time_mid = (timestamp >> 32) & 0xffff
    time_hi_version = (timestamp >> 48) & 0x0fff
    clock_seq_low = clock_seq & 0xff
    clock_seq_hi_variant = (clock_seq >> 8) & 0x3f
    return uuid.UUID(fields=(time_low, time_mid, time_hi_version,
			     clock_seq_hi_variant, clock_seq_low, node), version=1)

def printUUIDInfo(u):
    try:
        u = uuid.UUID(sys.argv[1])
    except ValueError:
        print("Invalid UUID")
        sys.exit(2)

    print ("UUID version: {}".format(u.version))

    if u.version == 1:
        t = UUIDTime(u)
        print("UUID time: {}".format(t))
        print("UUID timestamp: {}".format(u.time))
        print("UUID node: {}".format(u.node))
        m = UUIDMac(u)
        print("UUID MAC address: {}".format(m))
        print("UUID clock sequence: {}".format(u.clock_seq))

def genUUIDs(sample_uuid, precision, seconds, base_time):
    if u.version != 1:
        print("Only v1 GUIDs supported")
        sys.exit(2)

    # Get timestamp of starting GUID
    dt_zero = datetime.datetime(1582, 10, 15)
    base_guid_time = base_time - dt_zero
    base_timestamp = int(base_guid_time.total_seconds() * 1e7)

    # 1 second = 1e7 100-nanosecond intervals
    start =  int(base_timestamp - (1e7)*seconds)
    end =  int(base_timestamp + (1e7)*seconds)
    for t in range(start, end, precision):
        yield uuid1(u.node, u.clock_seq, t)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--info", help="Print UUID info an exit", action="store_true")

    parser.add_argument("-p", "--precision", type=int, default=10000, help="The number of 100-nanosecond intervals between each UUID")
    parser.add_argument("-r", "--range", type=int, default=1, help="The number of seconds each side of the timestamp to generate UUIDs for")
    parser.add_argument("-t", "--base-time",
                        help="The estimated time at which the UUID was generated in '%Y-%m-%d %H:%M:%S' format, e.g. '2021-03-17 16:42:11'",
                        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S"))

    parser.add_argument("uuid", help="The UUID to inspect")
    args = parser.parse_args()

    # Validate GUID
    try:
        u = uuid.UUID(args.uuid)
    except:
        print("Invalid UUID")
        sys.exit(1)

    # Handle info printing
    if args.info:
        printUUIDInfo(args.uuid)
        sys.exit(0)


    # Handle generation. Some optional arguments are required in this case
    if args.base_time is None:
        print("Base time required - specify with '-t' or '--base-time'")
        sys.exit(1)

    for u in genUUIDs(args.uuid, args.precision, args.range, args.base_time):
        print(u)
