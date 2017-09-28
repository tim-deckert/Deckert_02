 # Deckert, Timothy
# 1000-637-406
# 2017-09-17
# Assignment_01_03

import numpy as np
import math
import time

class cl_world:
    def __init__(self, objects=[], canvases=[], world=[], edges = []):
        self.objects = objects
        self.canvases = canvases
        self.world = world
        self.edges = edges

    def add_canvas(self, canvas):
        self.canvases.append(canvas)
        canvas.world = self

    def create_translate_matrix(self, matrix):

        translateMatrix = np.identity(4)    
        translateMatrix[0][3] = matrix[0]
        translateMatrix[1][3] = matrix[1]
        translateMatrix[2][3] = matrix[2]

        return translateMatrix

    def create_scale_matrix(self, matrix):

        scaleMatrix = np.diag(matrix)

        return scaleMatrix

    def create_x_axis_rotation_matrix(self, matrix):
        
        xRotateMatrix = np.identity(4)

        if math.hypot(matrix[2], matrix[1]) != 0:
        
            xRotateMatrix[1][1] = matrix[2] / math.hypot(matrix[2], matrix[1])
            xRotateMatrix[1][2] = -matrix[1] /  math.hypot(matrix[2], matrix[1])
            xRotateMatrix[2][1] = matrix[1] / math.hypot(matrix[2], matrix[1])
            xRotateMatrix[2][2] = matrix[2] / math.hypot(matrix[2], matrix[1])
            
        return xRotateMatrix
    
    def create_y_axis_rotation_matrix(self, matrix):
        
        yRotateMatrix = np.identity(4)
        
        if math.hypot(matrix[2], matrix[0]) != 0:
            
            yRotateMatrix[0][0] = matrix[2] / math.hypot(matrix[2], matrix[0])
            yRotateMatrix[2][0] = -matrix[0] /  math.hypot(matrix[2], matrix[0])
            yRotateMatrix[0][2] = matrix[0] /  math.hypot(matrix[2], matrix[0])
            yRotateMatrix[2][2] = matrix[2] / math.hypot(matrix[2], matrix[0])

        return yRotateMatrix

    def create_z_axis_rotation_matrix(self, rotation):

        rotation = math.radians(rotation)

        zRotateMatrix = np.identity(4)
        
        zRotateMatrix[0][0] = math.cos(rotation)
        zRotateMatrix[0][1] = -math.sin(rotation)
        zRotateMatrix[1][0] = math.sin(rotation)
        zRotateMatrix[1][1] = math.cos(rotation)
        
        return zRotateMatrix


    def rotate_button(self, canvas, point1, point2, rotation):
        
        point1 = point1.lstrip("[")
        point1 = point1.rstrip("]")
        point1 = point1.split(",")
        
        point2 = point2.lstrip("[")
        point2 = point2.rstrip("]")
        point2 = point2.split(",")

        point1 = np.array(point1, dtype=np.float32)
        point2 = np.array(point2, dtype=np.float32)

        rotation = float(rotation)

        point1Back = self.create_translate_matrix(point1)
        point1ToOrigin = point1Back
        point1ToOrigin[0][3] = -1 * point1ToOrigin[0][3]
        point1ToOrigin[1][3] = -1 * point1ToOrigin[1][3]
        point1ToOrigin[2][3] = -1 * point1ToOrigin[2][3]

        point2ToX = self.create_x_axis_rotation_matrix(point2)
        point2ToZ = self.create_y_axis_rotation_matrix(point2)

        xToPoint2 = np.transpose(point2ToX)
        zToPoint2 = np.transpose(point2ToZ)

        for k in range(100):

            rotationMatrix = self.create_z_axis_rotation_matrix(rotation * (1/100))

            transform = np.dot(point2ToX, point1ToOrigin)
            transform = np.dot(point2ToZ, transform)
            transform = np.dot(rotationMatrix, transform)
            transform = np.dot(zToPoint2, transform)
            transform = np.dot(xToPoint2, transform)
            transform = np.dot(point1Back, transform)

            vertices = []

            for i in range(len(self.world[0:-1])):
            
                self.world[i] = np.dot(transform, self.world[i])
                vertices.append(np.dot(self.world[-1], self.world[i]))

            edgeIter = iter(self.edges)
            points = []

            for face in self.objects:
                if len(canvas.coords(face)) != 4:
                    for fp in next(edgeIter):
                        points.append(int(vertices[int(fp)-1][0]))
                        points.append(int(vertices[int(fp)-1][1]))

                    canvas.coords(face, points)
                    points = []
                    
            canvas.update_idletasks()


    def scale_button(self, canvas, matrix, point):

        matrix = matrix.lstrip("[")
        matrix = matrix.rstrip("]")
        matrix = matrix.split(",")
        matrix.append(1.0)

        point = point.lstrip("[")
        point = point.rstrip("]")
        point = point.split(",")
        point.append(1.0)

        matrix = np.array(matrix, dtype=np.float32)
        point = np.array(point, dtype=np.float32)

        tempMat = np.zeros_like(matrix)
        tempMat[3] = 1.0
        
        translateBack = self.create_translate_matrix(point)
        translateThere = translateBack.copy()
        translateThere[0][3] = -1 * translateThere[0][3]
        translateThere[1][3] = -1 * translateThere[1][3]
        translateThere[2][3] = -1 * translateThere[2][3]

        tempMat[0] = math.pow(matrix[0], 0.01)
        tempMat[1] = math.pow(matrix[1], 0.01)
        tempMat[2] = math.pow(matrix[2], 0.01)        

        for k in range(1,101):
            
            scaleMatrix = self.create_scale_matrix(tempMat)

            transform = np.dot(translateBack, np.dot(scaleMatrix, translateThere))
            
            vertices = []

            for i in range(len(self.world[0:-1])):
            
                self.world[i] = np.dot(transform, self.world[i])
                vertices.append(np.dot(self.world[-1], self.world[i]))

            edgeIter = iter(self.edges)
            points = []

            for face in self.objects:
                if len(canvas.coords(face)) != 4:
                    for fp in next(edgeIter):
                        points.append(int(vertices[int(fp)-1][0]))
                        points.append(int(vertices[int(fp)-1][1]))

                    canvas.coords(face, points)
                    points = []

            canvas.update_idletasks()
        
    def translate_button(self, canvas, matrix):
        
        matrix = matrix.lstrip("[")
        matrix = matrix.rstrip("]")
        matrix = matrix.split(",")
        matrix.append(1.0)

        matrix = np.array(matrix, dtype=np.float32)
        tempMat = np.zeros_like(matrix)

        #translate = self.create_translate_matrix(matrix)

        
        tempMat[0] = matrix[0] * (1/100) 
        tempMat[1] = matrix[1] * (1/100)
        tempMat[2] = matrix[2] * (1/100)
        tempMat[3] = 1.0

        for k in range (100):
            
            translateMatrix = self.create_translate_matrix(tempMat)

            vertices = []

            for i in range(len(self.world[0:-1])):
            
                self.world[i] = np.dot(translateMatrix, self.world[i])
                vertices.append(np.dot(self.world[-1], self.world[i]))

            edgeIter = iter(self.edges)
            points = []

            for face in self.objects:
                if len(canvas.coords(face)) != 4:
                    for fp in next(edgeIter):
                        points.append(int(vertices[int(fp)-1][0]))
                        points.append(int(vertices[int(fp)-1][1]))

                    canvas.coords(face, points)
                    points = []

            canvas.update_idletasks()
                    
    def create_graphic_objects(self, canvas, filename):
        file = open(filename, 'r')
        data = file.read()
        file.close()
	
        rows = data.splitlines()

        vertices = []
        faces = []

        for row in rows:

            row = row.strip()

            coords = row.split(" ")

            if coords[0] == "v":
                coords.append(1.0)
                coordMat = np.array(coords[1:], dtype=np.float32)
                vertices.append(coordMat)
                self.world.append(coordMat)
            if coords[0] == "f":
                coordMat = np.array(coords[1:], dtype=np.int32)
                faces.append(coordMat)
                self.edges.append(coordMat)
            if coords[0] == "w":
                window = np.array(coords[1:], dtype=np.float32)
            if coords[0] == "s":
                viewport = np.array(coords[1:], dtype=np.float32)

        viewport[0] = int(viewport[0] * float(canvas.cget("width")))
        viewport[1] = int(viewport[1] * float(canvas.cget("height")))
        viewport[2] = int(viewport[2] * float(canvas.cget("width")))
        viewport[3] = int(viewport[3] * float(canvas.cget("height")))

        self.objects.append(canvas.create_rectangle(viewport[0], viewport[1], viewport[2], viewport[3], outline="red", width=2))

        vpx = (viewport[2] - viewport[0]) / (window[2] - window[0])
        vpy = (viewport[3] - viewport[1]) / (window[3] - window[1])

        dxy = np.array([[1,0,0,-window[0]],[0,-1,0,window[3]],[0,0,1,0],[0,0,0,1]])
        sxy = np.array([[vpx,0,0,0],[0,vpy,0,0],[0,0,1,0],[0,0,0,1]])
        dvpxy = np.array([[1,0,0,viewport[0]],[0,1,0,viewport[1]],[0,0,1,0],[0,0,0,1]])

        transform = np.dot(dvpxy, np.dot(sxy,dxy))
        #invTransform = np.linalg.inv(transform)
        self.world.append(transform)
        
        particles = []

        for vertex in vertices:
            particles.append(np.dot(transform, vertex))

        points = []

        for face in faces:
            for fp in face:
                points.append(int(particles[int(fp)-1][0]))
                points.append(int(particles[int(fp)-1][1]))
        
            self.objects.append(canvas.create_polygon(points, outline="red", fill="yellow"))
            points = []

    def redisplay(self, canvas, event, width, height):
        if self.objects:
            points = []
            
            scaleX = (float(event.width) - 4) / float(width)
            scaleY = (float(event.height) - 4) / float(height)
            
            for face in self.objects:
                canvas.scale(face, 0, 0, scaleX, scaleY)

    def clear_canvas(self, canvas):
        if self.objects:
            canvas.delete("all")
            self.objects = []
        if self.world:
            self.world = []
        if self.edges:
            self.edges = []
             
