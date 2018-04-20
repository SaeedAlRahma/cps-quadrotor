# Worlds Directory

## Generate New Worlds
* Run the following line in this directory

`python generate_worlds.py [input-file] [output-file]`

  * [input-file] should be input_files/[filename] formatted based on the description below
  * [output-file] should be [filename].world
  
## Input File Format
* Format
  * File must contain a list of regions (circles) followed by a list of obstacles (walls) separated by an empty line
  * Region line: [name] [radius] [x] [y] [color]
  * Obstacle line: [name] [length] [x] [y] [yaw]
  * The origin of both regions (circles) and obstacles (walls) is their center
  * Use White for start region, Blue for intermediate regions, and Green for goal region
 
