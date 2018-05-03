import re
import path_planner as pp
import path_drawer as pd


# printing out coordinates in readable list order as coordinates to send to controller
def get_path_coordinates(path):
    coordinate_path = []
    co_path = path
    while all(co_path[-1]):
        coordinate_path.append(co_path[1])
        if (not all(co_path)):
            break
        co_path = co_path[0]
    print(coordinate_path[::-1])
    # Draw environment to see if desired, uncomment this to draw paths
    graphics = pd.Drawer(g.planes, coordinate_path[::-1])
    return (coordinate_path[::-1])


# changing format of path to use labels and not coordinates if need be
def get_path_labels(path):
    labeled_path = []
    la_path = path
    while all(la_path[-1]):
        labeled_path.append(planner.graph.get_plane_from_center(la_path[1]).label)
        if (not all(la_path)):
            break
        la_path = la_path[0]
    print(labeled_path[::-1])
    return (labeled_path[::-1])


# Read from text file
p = []
filename = "./enviro.txt"
start_node = "A"
end_node = "E"
with open(filename, 'r') as file:
    for line in file:
        raw_data = re.sub(r"[\n\t\s]*", "", line)
        data, raw_tuple = raw_data.split(',', 1)
        v1, v2, v3, empty = raw_tuple.split(')')
        list = []
        for x in [v1, v2, v3]:
            y = x.split('(')[1]
            z = y.split(',')
            list.append((float(z[0]), float(z[1])))
        p.append(pp.Plane(str(data), (list[0], list[1], list[2])),)


# Initialize all planes, graph object, and path planner object
planes = tuple(p)
g = pp.Graph(planes)
planner = pp.Path_Planner(g)


# Actual calling of path_planner.py and returning path in readable-ish order
make_path = lambda tup: (make_path(tup[1]), tup[0]) if tup else ()
out = planner.dijkstra(start_node, end_node)
path = make_path(out[1])
get_path_coordinates(path)
#get_path_labels(path)
