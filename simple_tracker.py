#! /usr/bin/env python

"""Simple tracking solution based off triad_openvr

Track the pose and velocity of devices connected to a steamVR system at some user-defined (default 250hz) frequency.
"""

import triad_openvr
from argparse import ArgumentParser
from time import sleep

to_track = ["tracker_1", "tracker_2", "tracker_3", "controller_1", "controller_2", "controller_3"]

parser = ArgumentParser(description="Application to log the position of devices tracked by the HTC Vive")
parser.add_argument("device", choices=to_track, help="device to log")
parser.add_argument("output_file", help="csv file to log the positions to")

args = parser.parse_args()

# Open the file and write the header
dump = open(args.output_file, "w+")
dump.write("#x, y, z, r_w, r_y, r_z, r_x, v_x, v_y, v_z\n")

# Connect to the VR system
v = triad_openvr.triad_openvr()

# Loop until Ctrl-C
iterations = 0
try:
    while True:
        iterations += 1

        # Loop through all devices that could be trackable
        if args.device not in v.devices:
            continue

        # Try and get the pose and velocity
        try:
            pose = v.devices[args.device].get_pose_quaternion()
            vel = v.devices[args.device].get_velocity()
        except ZeroDivisionError:
            print(f"Zero division in quaternion calculation for {args.device}.")

        # if the pose is None this means that the device cannot see enough
        # lighthouses to get a good fix. In this case just skip it
        if pose is None:
            print(f"{args.device} can not see enough lighthouses.")

        # Extract the pose into its' parts
        y, z, x, r_w, r_y, r_z, r_x = pose
        v_y, v_z, v_x = vel
        dump.write(f"{x}, {y}, {z}, {r_w}, {r_x}, {r_y}, {r_z}, {v_z}, {v_y}, {v_z}\n")

        sleep(1 / 60.)
except KeyboardInterrupt:
    print(f"Finished {iterations} iterations.")
    dump.close()