"""
    Copyright 2016 Jonathan Cole

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import math


class Triangle_3:
    """This is a class to construct triangles in 3 dimensional Cartesian coordinate space.

    These triangles are used to construct target objects for intersection

    Constructor Args:
        Three (3x1) numpy arrays representing the coordinates of the vertices.

    Properties:
        a: The first vertex
        b: The second vertex
        c: The third vertex
        u: First of two vectors defining the triangle by making a v shape. Used for intersection calculations.
        v: Second of two vectors defining the triangle by making a v shape. Used for intersection calculations.
    """

    def __init__(self, Point_3a, Point_3b, Point_3c):
        self.a = Point_3a
        self.b = Point_3b
        self.c = Point_3c
        self.u = Point_3b - Point_3a
        self.v = Point_3c - Point_3a


class Segment_3:
    """ This is a class to construct line segments in 3 dimensional Cartesian coordinate space.

    These segments are used to represent rays from the focus to isocentre or from the focus to the skin cell
    under evaluation.

    Constructor Args:
        Two (3x1) numpy arrays representing the coordinates of the start and end of the segment.

    Properties:
        source: the start point
        target: the end point
        vector: the vector from start to end
        length: the magnitude of the segment
        xangle: the angle between the segment and the x-axis
        yangle: the angle between the segment and the y-axis
    """

    def __init__(self, Point_3a, Point_3b):
        self.source = Point_3a
        self.target = Point_3b
        self.vector = Point_3b - Point_3a
        self.length = np.linalg.norm(self.vector)
        denom0 = self.vector[0]
        if abs(denom0) < 0.00000001:
            denom0 = 0.00000001
        denom1 = self.vector[1]
        if abs(denom1) < 0.00000001:
            denom1 = 0.00000001
        self.xangle = np.arctan(self.vector[2] / denom0)
        self.yangle = np.arctan(self.vector[2] / denom1)


class Phantom:
    """ This class defines a surface to which dose will be delivered.

    Constructor Args:
        phantomType: the type of phantom being assembled
        origin: the coordinate system for the phantom. For example, some systems
            use the head end, table plane in the patient mid-line. So the origin
            would be [25,0,0] on a 50 cm wide phantom.
        width: the number of cells the phantom is wide
        height: the number of cells the phantom is long
        depth: the number of cells the phantom is deep. Ignored for flat phantom.
        scale: the steps (in cm) to make between cells

    Properties:
        width: the width of the phantom in cells
        height: the height of the phantom in cells
        phantomMap: an array containing a list of points which represent each cell in the phantom surface to be evaluated
        normalMap: an array containing line segments (Segment_3) indicating the outward facing surface of the cell
    """

    def __init__(self, phantomType, origin, width, height, depth, scale):
        self.phantomType = phantomType
        self.width = width
        self.height = height
        if phantomType is "flat":
            zOffset = -origin[2]
            self.phantomMap = np.empty((width, height), dtype=object)
            self.normalMap = np.empty((width, height), dtype=object)
            it = np.nditer(self.phantomMap, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
            while not it.finished:
                myX = it.multi_index[0] * scale - origin[0]
                myY = it.multi_index[1] * scale - origin[1]
                self.phantomMap[it.multi_index[0], it.multi_index[1]] = np.array([myX, myY, zOffset])  # As above

                planePoint = np.array([myX, myY, zOffset])
                outsidePoint = np.array([myX, myY, zOffset - 1])
                # The normal is defined going back in to the plane, to make checking alignment easier
                normal = Segment_3(outsidePoint, planePoint)
                self.normalMap[it.multi_index[0], it.multi_index[1]] = normal
                it.iternext()


class Phantom_3:
    """ This class defines a surface in 3d to project dose onto.
    It is formed of a central cuboid with two semi cylinders on the sides.

    Constructor Args:
        origin: the coordinate system for the phantom. For example, some systems
            use the head end, table plane in the patient mid-line. This phantom
            assumes the origin is at the head, on the mid-line and on the table
            for [0,0,0].
        width: the number of cells the phantom is wide. Includes the wrap around
        height: the number of cells the phantom is long
        scale: the steps (in cm) to make between cells

    Properties:
        width: the total distance around the phantom (distance around both curved edges,
            plus the distance across the flat front and back - not really the width...)
        height: the height of the phantom in cells
        phantom_width: the horizontal distance across the 3D phantom
        phantom_height: the height of the 3D phantom
        phantom_depth: the depth of the 3D phantom
        phantom_flat_dist: the width of the flat part of the phantom (same for front and back)
        phantom_curved_dist: the distance around one curved side of the phantom (same for left and right sides)
        phantomMap: an array containing a list of points which represent each cell in the phantom surface to be evaluated
        normalMap: an array containing line segments (Segment_3) indicating the outward facing surface of the cell
        phantomType: set to "3d"
    """

    def __init__(self, origin, scale=1, mass=73.2, height=178.6, patPos="HFS"):

        refHeight = 178.6
        refMass = 73.2
        refTorso = 70.
        refRadius = 10.
        refWidth = 14.4
        torso = refTorso * height / refHeight
        radius = refRadius / math.sqrt(height / refHeight) * math.sqrt(mass / refMass)
        
        if patPos == "HFS":
            prone = False
            patPosZ = 1.
            patPosY = 1.
            origin[1] = origin[1] - 24 * height/refHeight
        elif patPos == "FFS":
            prone = False
            patPosZ = 1.
            patPosY = -1.
            origin[1] = origin[1] - 174 * height/refHeight
        elif patPos == "HFP":
            prone = True		
            patPosZ = -1.
            patPosY = 1.
            origin[1] = origin[1] - 24 * height/refHeight
        elif patPos == "FFP":
            prone = True
            patPosZ = -1.
            patPosY = -1.
            origin[1] = origin[1] - 174 * height/refHeight
        
            

        partCircumference = math.pi * radius
        roundCircumference = round(partCircumference, 0)
        flatWidth = refWidth / refRadius * radius
        roundFlat = round(flatWidth, 0)
        flatSpacing = flatWidth / roundFlat

        # The three properties were added by DJP to describe
        # the dimensions of the 3D phantom.
        self.phantom_width = int(round(flatWidth + 2 * radius, 0))
        self.phantom_height = int(round(torso, 0))
        self.phantom_depth = round(radius * 2, 0)
        self.phantom_flat_dist = roundFlat
        self.phantom_curved_dist = roundCircumference

        self.width = int(2 * roundCircumference + 2 * roundFlat)
        self.height = int(round(torso, 0))
        self.phantomType = "3d"
        self.phantomMap = np.empty((self.width, self.height), dtype=object)
        self.normalMap = np.empty((self.width, self.height), dtype=object)
        transition1 = (roundFlat / 2.) + 0.5  # Centre line flat to start of curve.
        transition2 = transition1 + roundCircumference  # End of first curve to table flat
        transition3 = transition2 + roundFlat  # End of table flat to second curve
        transition4 = transition3 + roundCircumference  # End of second curve to flat back to centre line
        it = np.nditer(self.phantomMap, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            # Start top, centre line.
            row_index = it.multi_index[0] - origin[0]
            col_index = it.multi_index[1] - origin[1]
            angleStep = math.pi / roundCircumference
            zOffset = -origin[2]

            if row_index < transition1:
                myZ = (2. * radius + zOffset) * patPosZ
                myX = row_index * flatSpacing - (roundFlat / 2.) + round(roundFlat / 2., 0)
                myY = (col_index) * patPosY
                normal = Segment_3(np.array([myX, myY, myZ + patPosZ]), np.array([myX, myY, myZ]))
            elif row_index >= transition1 and row_index < transition2:
                myY = (col_index)*patPosY
                myX = flatSpacing * round(transition1, 0) - 1 + radius * math.sin(
                    angleStep * (row_index - round(transition1, 0) + 1)) - (roundFlat / 2.) + round(roundFlat / 2., 0)
                myZ = (2. * radius + zOffset + radius * math.cos(
                    angleStep * (row_index - round(transition1, 0) + 1)) - radius) * patPosZ
                normalX = myX + math.sin(angleStep * (row_index - round(transition1, 0) + 1))
                normalZ = myZ + patPosZ * math.cos(angleStep * (row_index - round(transition1, 0) + 1))
                normal = Segment_3(np.array([normalX, myY, normalZ]), np.array([myX, myY, myZ]))
            elif row_index >= transition2 and row_index < transition3:
                myZ = zOffset * patPosZ
                myX = flatWidth - (row_index - roundCircumference) * flatSpacing + ((roundFlat / 2.) - round(
                    roundFlat / 2., 0)) * (row_index - roundCircumference) / abs(row_index - roundCircumference)
                myY = col_index * patPosY
                normal = Segment_3(np.array([myX, myY, myZ - patPosZ]), np.array([myX, myY, myZ]))
            elif row_index >= transition3 and row_index < transition4:
                myY = col_index * patPosY
                myX = -flatSpacing * round(roundFlat / 2, 0) - radius * math.sin(
                    angleStep * (row_index - round(transition3, 0) + 1)) - (roundFlat / 2.) + round(roundFlat / 2., 0)
                myZ = (zOffset - radius * math.cos(angleStep * (row_index - round(transition3, 0) + 1)) + radius) * patPosZ
                normalX = myX - math.sin(angleStep * (row_index - round(transition3, 0) + 1))
                normalZ = myZ - patPosZ * math.cos(angleStep * (row_index - round(transition3, 0) + 1))
                normal = Segment_3(np.array([normalX, myY, normalZ]), np.array([myX, myY, myZ]))
            else:
                myZ = (2. * radius + zOffset) * patPosZ
                myX = (row_index - self.width) * flatSpacing - (roundFlat / 2.) + round(roundFlat / 2., 0)
                myY = col_index * patPosY
                normal = Segment_3(np.array([myX, myY, myZ + patPosZ]), np.array([myX, myY, myZ]))
            self.phantomMap[it.multi_index[0], it.multi_index[1]] = np.array([myX, myY, myZ])
            self.normalMap[it.multi_index[0], it.multi_index[1]] = normal
            it.iternext()
        #Flip to correct left and right so it becomes a view of the back.
        #self.phantomMap = np.flipud(self.phantomMap)
        #self.normalMap = np.flipud(self.normalMap)
        self.phantomMap = np.fliplr(self.phantomMap)
        self.normalMap = np.fliplr(self.normalMap)
        if prone:
            self.normalMap = np.roll(self.normalMap, int(self.phantom_flat_dist + self.phantom_curved_dist),axis=0)
            self.phantomMap = np.roll(self.phantomMap, int(self.phantom_flat_dist + self.phantom_curved_dist),axis=0)
            self.phantomMap = np.flipud(self.phantomMap)
            self.normalMap = np.flipud(self.normalMap)
           


class SkinDose:
    """ This class holds dose maps for a defined phantom. It is intended
    to simplify combining multiple views.

    Constructor Args:
        phantom: the phantom being irradiated.

    Properties:
        phantom: the phantom being irradiated
        views: a list of the irradiations included
        doseArray: an array of doses delivered to the phantom
        totalDose: a summed array of doses
        fliplr: flip the left and right of the dose map to provide a view from
        behind the patient
    """

    def __init__(self, phantom):
        self.phantom = phantom
        self.views = []
        self.doseArray = []
        self.totalDose = []

    def addView(self, viewStr):
        if len(self.views) == 0:
            self.views = viewStr
        else:
            self.views = np.vstack((self.views, viewStr))

    def addDose(self, skinMap):
        if len(self.doseArray) == 0:
            self.doseArray = skinMap
            self.totalDose = skinMap
        else:
            self.doseArray = np.dstack((self.doseArray, skinMap))
            self.totalDose = self.totalDose + skinMap		