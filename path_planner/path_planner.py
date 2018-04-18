import itertools
import sys
from multiprocessing import Queue
import math as np
from collections import defaultdict
from heapq import *


class Plane():
    def __init__(self, label, vertices):
        self.label = label
        self.center = self.get_centroid(vertices)
        self.vertices = vertices
        self.edges = list(itertools.combinations(vertices, 2))


    def get_centroid(self, vertices):
        return ((vertices[0][0] + vertices[1][0] + vertices[2][0])/3, (vertices[0][1] + vertices[1][1] + vertices[2][1])/3) #can extend to z coords if necessary


class Graph():
    def __init__(self, planes):
        self.planes = planes
        self.edge_center_map = {}
        self.edge_weights = {}
        for plane in self.planes:
            self.get_adjacent(plane)
        for edge in self.edge_center_map.keys():
            self.edge_weights[edge] = self.get_dist(self.edge_center_map[edge][0], self.edge_center_map[edge][1])


    def get_dist(self, source, target):
        return np.sqrt((source[0] - target[0])**2 + (source[1] - target[1])**2)


    def get_adjacent(self, plane):
        for temp in self.planes:
            if (temp != plane):
                for e1, e2 in itertools.product(temp.edges, plane.edges):
                    if ((e1[0] == e2[0] and e1[1] == e2[1]) or (e1[0] == e2[1] and e1[1] == e2[0])):
                        if (e1 not in self.edge_center_map.keys()):
                            self.edge_center_map[e1] = (temp.center, plane.center)
        return


    def get_plane_from_label(self, label):
        return next(obj for obj in self.planes if obj.label==label)


    def get_plane_from_center(self, center):
        return next(obj for obj in self.planes if obj.center==center)


class Path_Planner():
    def __init__(self, graph):
        self.graph = graph


    def dijkstra(self, start_label, goal_label):
        # Take out these two lines to search by raw coordinates instead of by plane labels
        start = self.graph.get_plane_from_label(start_label).center
        goal = self.graph.get_plane_from_label(goal_label).center
        g = defaultdict(list)
        edges = []
        for edge in self.graph.edge_center_map.keys():
            planes = self.graph.edge_center_map[edge]
            edges.append((planes[0], planes[1], self.graph.edge_weights[edge]))
        for l,r,c in edges:
            g[l].append((c,r))
            g[r].append((c,l))

        q, seen = [(0, start, ())], set()
        while q:
            (cost, v1, path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                if v1 == goal:
                    return (cost, path)

                for c, v2 in g.get(v1, ()):
                    if v2 not in seen:
                        heappush(q, (cost+c, v2, path))
        return float("inf")
