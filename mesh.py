import pygame
import time
from vector3 import *

class Mesh:
    stat_vertex_count = 0
    stat_transform_time = 0
    stat_render_time = 0

    def __init__(self, name = "UnknownMesh"):
        self.name = name
        self.polygons = []

    def offset(self, v):
        new_polys = []
        for poly in self.polygons:
            new_poly = []
            for p in poly:
                new_poly.append(p + v)
            new_polys.append(new_poly)

        self.polygons = new_polys

    def render(self, screen, matrix, material):
        c = material.color.tuple3()        

        for poly in self.polygons:
            tpoly = []
            #Mesh.stat_vertex_count += len(poly)
            #t0 = time.time()
            for v in poly:
                vout = v.to_np4()
                vout = vout @ matrix
                
                tpoly.append( ( screen.get_width() * 0.5 + vout[0] / vout[3], screen.get_height() * 0.5 - vout[1] / vout[3]) )

            #t1 = time.time()
            
            pygame.draw.polygon(screen, c, tpoly, material.line_width)

            #t2 = time.time()
            #Mesh.stat_transform_time += (t1 - t0)
            #Mesh.stat_render_time += (t2 - t1)

    @staticmethod
    def create_cube(size, mesh = None):
        if (mesh == None):
            mesh = Mesh("UnknownCube")

        Mesh.create_quad(vector3( size[0] * 0.5, 0, 0), vector3(0, -size[1] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)
        Mesh.create_quad(vector3(-size[0] * 0.5, 0, 0), vector3(0,  size[1] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)

        Mesh.create_quad(vector3(0,  size[1] * 0.5, 0), vector3(size[0] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)
        Mesh.create_quad(vector3(0, -size[1] * 0.5, 0), vector3(-size[0] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)

        Mesh.create_quad(vector3(0, 0,  size[2] * 0.5), vector3(-size[0] * 0.5, 0), vector3(0, size[1] * 0.5, 0), mesh)
        Mesh.create_quad(vector3(0, 0, -size[2] * 0.5), vector3( size[0] * 0.5, 0), vector3(0, size[1] * 0.5, 0), mesh)

        return mesh

    @staticmethod
    def create_sphere(size, resLat, resLon, mesh = None):
        if (mesh == None):
            mesh = Mesh("UnknownSphere")

        if (isinstance(size, vector3)):
            hs = size * 0.5
        else:
            hs = vector3(size[0], size[1], size[2]) * 0.5

        bottom_vertex = vector3(0, -hs.y, 0)
        top_vertex = vector3(0, hs.y, 0)

        latInc = math.pi / resLat
        lonInc = math.pi * 2 / resLon
        # First row of triangles
        lat = -math.pi / 2
        lon = 0

        y = hs.y * math.sin(lat + latInc)
        c = math.cos(lat + latInc)
        for _ in range(0, resLon):
            p1 = vector3(c * math.cos(lon) * hs.x, y, c * math.sin(lon) * hs.z)
            p2 = vector3(c * math.cos(lon + lonInc) * hs.x, y, c * math.sin(lon + lonInc) * hs.z)

            Mesh.create_tri(bottom_vertex, p1, p2, mesh)

            lon += lonInc

        # Quads in the middle
        for _ in range(1, resLat - 1):
            lat += latInc

            y1 = hs.y * math.sin(lat)
            y2 = hs.y * math.sin(lat + latInc)
            c1 = math.cos(lat)
            c2 = math.cos(lat + latInc)

            lon = 0
            for _ in range(0, resLon):
                p1 = vector3(c1 * math.cos(lon) * hs.x, y1, c1 * math.sin(lon) * hs.z)
                p2 = vector3(c1 * math.cos(lon + lonInc) * hs.x, y1, c1 * math.sin(lon + lonInc) * hs.z)
                p3 = vector3(c2 * math.cos(lon) * hs.x, y2, c2 * math.sin(lon) * hs.z)
                p4 = vector3(c2 * math.cos(lon + lonInc) * hs.x, y2, c2 * math.sin(lon + lonInc) * hs.z)

                poly = []
                poly.append(p1)
                poly.append(p2)
                poly.append(p4)
                poly.append(p3)

                mesh.polygons.append(poly)

                lon += lonInc

        # Last row of triangles
        lat += latInc
        y = hs.y * math.sin(lat)
        c = math.cos(lat)
        for _ in range(0, resLon):
            p1 = vector3(c * math.cos(lon) * hs.x, y, c * math.sin(lon) * hs.z)
            p2 = vector3(c * math.cos(lon + lonInc) * hs.x, y, c * math.sin(lon + lonInc) * hs.z)

            Mesh.create_tri(top_vertex, p1, p2, mesh)

            lon += lonInc
        
        return mesh


    @staticmethod
    def create_quad(origin, axis0, axis1, mesh):
        if (mesh == None):
            mesh = Mesh("UnknownQuad")

        poly = []
        poly.append(origin + axis0 + axis1)
        poly.append(origin + axis0 - axis1)
        poly.append(origin - axis0 - axis1)
        poly.append(origin - axis0 + axis1)

        mesh.polygons.append(poly)

        return mesh
    
    @staticmethod
    def create_tri(p1, p2, p3, mesh):
        if (mesh == None):
            mesh = Mesh("UnknownQuad")

        poly = []
        poly.append(p1)
        poly.append(p2)
        poly.append(p3)

        mesh.polygons.append(poly)

        return mesh
    
