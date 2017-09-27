 # Deckert, Timothy
# 1000-637-406
# 2017-09-17
# Assignment_01_03

import numpy as np
import math

class cl_world:
    def __init__(self, objects=[], canvases=[], world=[], edges = []):
        self.objects = objects
        self.canvases = canvases
        self.world = world
        self.edges = edges
        # self.display

    def add_canvas(self, canvas):
        self.canvases.append(canvas)
        canvas.world = self

    def create_translate_matrix(self, matrix):
        
        matrix = np.array(matrix, dtype=np.float32)

        translateMatrix = np.identity(4)    
        translateMatrix[0][3] = matrix[0]
        translateMatrix[1][3] = matrix[1]
        translateMatrix[2][3] = matrix[2]

        return translateMatrix

    def create_scale_matrix(self, matrix):
        
        scaleMatrix = np.array(matrix, dtype=np.float32)
        scaleMatrix = np.diag(scaleMatrix)

        return scaleMatrix

    def create_x_axis_rotation_matrix(self, matrix):

        matrix = np.array(matrix, dtype=np.float32)
        
        xRotateMatrix = np.identity(4)
        xRotateMatrix[1][1] = matrix[2] / math.hypot(matrix[2], matrix[1])
        xRotateMatrix[1][2] = -matrix[1] /  math.hypot(matrix[2], matrix[1])
        xRotateMatrix[2][1] = matrix[1] / math.hypot(matrix[2], matrix[1])
        xRotateMatrix[2][2] = matrix[2] / math.hypot(matrix[2], matrix[1])
        return xRotateMatrix
    
    def create_y_axis_rotation_matrix(self, matrix):
        
        matrix = np.array(matrix, dtype=np.float32)
        
        yRotateMatrix = np.identity(4)
        yRotateMatrix[0][0] = matrix[2] / math.hypot(matrix[2], matrix[0])
        yRotateMatrix[2][0] = -matrix[0] /  math.hypot(matrix[2], matrix[0])
        yRotateMatrix[0][2] = matrix[0] /  math.hypot(matrix[2], matrix[0])
        yRotateMatrix[2][2] = matrix[2] / math.hypot(matrix[2], matrix[0])

        return yRotateMatrix

    def create_z_axis_rotation_matrix(self, matrix):

        matrix = np.array(matrix, dtype=np.float32)
        
        zRotateMatrix = np.identity(4)
        zRotateMatrix[1][1] = math.cos(rotation) # / math.sqrt((math.pow(matrix[0],2) + math.pow(matrix[1],2)))
        zRotateMatrix[1][2] = -math.sin(rotation) # / math.sqrt((math.pow(matrix[0],2) + math.pow(matrix[1],2)))
        zRotateMatrix[2][1] = math.sin(rotation) # / math.sqrt((math.pow(matrix[0],2) + math.pow(matrix[1],2)))
        zRotateMatrix[2][2] = math.cos(rotation) # / math.sqrt((math.pow(matrix[0],2) + math.pow(matrix[1],2)))
        
        return zRotateMatrix


    def rotate_button(self, canvas, point1, point2, rotation):
        
        point1 = point1.lstrip("[")
        point1 = point1.rstrip("]")
        point1 = point1.split(",")
        
        point2 = point2.lstrip("[")
        point2 = point2.rstrip("]")
        point2 = point2.split(",")

        rotation = float(rotation)

        point1ToOrigin = self.create_translate_matrix(point1)
        point1ToOrigin[0][3] = -1 * point1ToOrigin[0][3]
        point1ToOrigin[1][3] = -1 * point1ToOrigin[1][3]
        point1ToOrigin[2][3] = -1 * point1ToOrigin[2][3]

        point2ToX = self.create_x_axis_rotation_matrix(point2)
        point2ToZ = self.create_y_axis_rotation_matrix(point2)

        rotationMatrix = self.create_z_axis_rotation_matrix(math.degrees(rotation))

        transform = np.dot(rotation, np.dot(point2ToZ, point2ToX))

        for face in self.objects:

            if len(canvas.coords(face)) == 4:
                continue
            
            pointIter = iter(canvas.coords(face))
            xAndY = []
            
            for points in pointIter:
                pointToTranslate = [points, next(pointIter), 0, 1]
                translatePoint = np.dot(transform, pointToTranslate)
                xAndY.extend((translatePoint[0], translatePoint[1]))
                                
            canvas.coords(face, xAndY)
            xAndY = []

    def scale_button(self, canvas, matrix, point):

        matrix = matrix.lstrip("[")
        matrix = matrix.rstrip("]")
        matrix = matrix.split(",")
        matrix.append(1.0)

        point = point.lstrip("[")
        point = point.rstrip("]")
        point = point.split(",")
        point.append(1.0)


        scaleMatrix = self.create_scale_matrix(matrix)
        translateBack = self.create_translate_matrix(point)
        translateThere = translateBack.copy()
        translateThere[0][3] = -1 * translateThere[0][3]
        translateThere[1][3] = -1 * translateThere[1][3]
        translateThere[2][3] = -1 * translateThere[2][3]

        transform = np.dot(translateBack, np.dot(scaleMatrix, translateThere))

        for face in self.objects:

            if len(canvas.coords(face)) == 4:
                continue
            
            pointIter = iter(canvas.coords(face))
            xAndY = []
            
            for points in pointIter:
                pointToTranslate = [points, next(pointIter), 0, 1]
                translatePoint = np.dot(transform, pointToTranslate)
                xAndY.extend((translatePoint[0], translatePoint[1]))
                                
            canvas.coords(face, xAndY)
            xAndY = []
        
    def translate_button(self, canvas, matrix):

        matrix = matrix.lstrip("[")
        matrix = matrix.rstrip("]")
        matrix = matrix.split(",")
        matrix.append(1.0)

        translateMatrix = self.create_translate_matrix(matrix)

        vertices = []

        for i in range(len(self.world[0:-1])):
            
            self.world[i] = np.dot(translateMatrix, self.world[i])
            vertices.append(np.dot(self.world[-1], self.world[i]))

##        objIter = iter(self.objects)
##        points = []

##        for face in self.edges:
##            if len(self.objects[objIter]) == 4 :
##                next(objIter)
##                
##            for fp in face:
##                points.append(int(particles[int(fp)-1][0]))
##                points.append(int(particles[int(fp)-1][1]))
##
##            canvas.coords(next(objIter), points)
##            points = []
##
        edgeIter = iter(self.edges)
        points = []

        for face in self.objects:
            if len(canvas.coords(face)) != 4:
                for fp in next(edgeIter, self.edges[0]):
                    points.append(int(vertices[int(fp)-1][0]))
                    points.append(int(vertices[int(fp)-1][1]))

                canvas.coords(face, points)
                points = []

##        for face in self.objects:
##
##            if len(canvas.coords(face)) == 4:
##                continue
##            
##            pointIter = iter(canvas.coords(face))
##            xAndY = []
##            
##            for points in pointIter:
##                pointToTranslate = [points, next(pointIter), 0, 1]
##                translatePoint = np.dot(translateMatrix, pointToTranslate)
##                xAndY.extend((translatePoint[0], translatePoint[1]))
##                                
##            canvas.coords(face, xAndY)
##            xAndY = []

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

        print(len(self.objects))

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
             
