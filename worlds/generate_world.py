#!/usr/bin/env python
import sys

if len(sys.argv) != 3:
    print 'Wrong arguments! This script takes exactly 2 arguments'
    print 'python generate_world.py [input-file] [output-file]'
    exit(0)

IN_FILE = sys.argv[1]
OUT_FILE = sys.argv[2]

PREFIX = \
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
    <!-- Camera position -->
    <gui>
      <camera name="user_camera">
        <pose>8.5 11.0 18.0 0.0 1.42 3.14</pose>
      </camera>
    </gui>
    <!-- Ground regions -->"""
SUFFIX = """
  </world>
</sdf>
"""
NAME = 0
RADIUS = 1
LENGTH = 1
X = 2
Y = 3
COLOR = 4
YAW = 4


def getRegion(data):
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
    return region


def getObstacle(data):
    obstacle = """
    <model name='wall_%s'>
    <pose frame=''>%s %s 1.0 0 0 %s</pose>
    <link name='link'>
    <collision name='collision'>
      <geometry>
        <box>
          <size>0.05 %s 2</size>
        </box>
      </geometry>
    </collision>
    <visual name='visual'>
      <geometry>
        <box>
          <size>0.05 %s 2</size>
        </box>
      </geometry>
      <material>
        <script>
          <name>Gazebo/Red</name>
          <uri>file://media/materials/scripts/gazebo.material</uri>
        </script>
      </material>
    </visual>
    </link>
    </model>""" \
    %(data[NAME], data[X], data[Y], data[YAW], data[LENGTH], data[LENGTH])
    return obstacle


infile = open(IN_FILE, 'r')
if infile.mode != 'r':
    print 'File does not exists. Make sure you are in the correct directory'
    exit(0)
outfile = open(OUT_FILE,"w+")

isObstacle = False

outfile.write(PREFIX)
for line in infile.readlines():
    data = line.split()
    if data == None or len(data)== 0:
        isObstacle = True
        continue

    if not isObstacle:
        object = getRegion(data)
    else:
        object = getObstacle(data)
    outfile.write(object)

outfile.write(SUFFIX)
outfile.close()
