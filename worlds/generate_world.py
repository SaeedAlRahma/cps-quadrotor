#!/usr/bin/env python
import sys

if len(sys.argv) != 3:
    print 'Wrong arguments! This script takes exactly 2 arguments'
    print 'python generate_world.py [input-file] [output-file]'
    exit(0)

IN_FILE = sys.argv[1]
OUT_FILE = sys.argv[2]

infile = open(IN_FILE, 'r')
if infile.mode != 'r':
    print 'File does not exists. Make sure you are in the correct directory'
    exit(0)
outfile = open(OUT_FILE,"w+")

prefix = \
"""<?xml version="1.0" ?>
<sdf version="1.5">
  <world name="default">
    <!-- A global light source -->
    <include>
      <uri>model://sun</uri>
    </include>
    <!-- A ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <!-- Ground regions -->"""
suffix = """
  </world>
</sdf>
"""
NAME = 0
X = 1
Y = 2
RADIUS = 3
COLOR = 4

outfile.write(prefix)
for line in infile.readlines():
    data = line.split()
    region = """
    <model name='region_%s'>
      <pose frame=''>%s %s 0.1 0 0 0</pose>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <cylinder>
              <radius>%s</radius>
              <length>0.2</length>
            </cylinder>
          </geometry>
        </collision>
        <visual name='visual'>
          <geometry>
            <cylinder>
              <radius>%s</radius>
              <length>0.2</length>
            </cylinder>
          </geometry>
          <material>
            <script>
              <name>Gazebo/%s</name>
              <uri>file://media/materials/scripts/gazebo.material</uri>
            </script>
          </material>
        </visual>
      </link>
    </model>""" \
        %(data[NAME], data[X], data[Y], data[RADIUS], data[RADIUS], data[COLOR])
    outfile.write(region)
outfile.write(suffix)
outfile.close()
