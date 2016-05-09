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
from geomclass import *


def intersect(aRay, aTriangle):
    """ Derived from example code at http://geomalgorithms.com/a06-_intersect-2.html
    provided under the following license:

    Copyright 2001 softSurfer, 2012 Dan Sunday
    This code may be freely used and modified for any purpose
    providing that this copyright notice is included with it.
    SoftSurfer makes no warranty for this code, and cannot be held
    liable for any real or imagined damage resulting from its use.
    Users of this code must verify correctness for their application.

    This function checks if a ray intersects a triangle

    Args:
        aRay: the ray (Segment_3) being projected
        aTriangle: the triangle (Trianlge_3) to hit

    Returns:
        A string describing the status of the hit.
    """

    n = np.cross(aTriangle.u, aTriangle.v)
    if n is [0, 0, 0]:
        output = "degenerate"
    w0 = aRay.source - aTriangle.a;
    a = -np.dot(n, w0);
    b = np.dot(n, aRay.vector);

    if (abs(b) < 0.00000001):
        output = "same plane"
        return output

    r = a / b
    if (r < 0.0):
        output = "away from triangle"
        return output

    I = aRay.source + r * aRay.vector

    uu = np.dot(aTriangle.u, aTriangle.u);
    uv = np.dot(aTriangle.u, aTriangle.v);
    vv = np.dot(aTriangle.v, aTriangle.v);
    w = I - aTriangle.a;
    wu = np.dot(w, aTriangle.u);
    wv = np.dot(w, aTriangle.v);
    D = uv * uv - uu * vv;

    s = (uv * wv - vv * wu) / D;
    t = (uv * wu - uu * wv) / D;

    # Hit some precision problems so either use this fix or use an exact maths library. This seems easier for now.

    if (s < 0.0 or s > 1.000000000001):  # Technically >1 but for the rounding errors.
        output = "outside test 1"
    else:
        if (t < 0.0 or (s + t) > 1.000000000001):
            output = "outside test 2" + "S:" + str(s) + " t:" + str(t)

        else:
            output = "hit"
    return output


def collimate(aRay, area, Dref):
    """ This function produces a pair of triangles representing a square field
    of a collimated x-ray beam. These are then used for intersection checks to
    see if the phantom cell sees radiation.

    Args:
        aRay: the x-ray beam from focus to isoncentre as a Segment_3
        area: an area of the beam in square centimetres at any arbitrary distance
        Dref: the reference distance the area is defined at

    Returns:
        A tuple of two touching triangles making a square field oriented
        perpendicular to the beam direction.
    """
    sideLength = math.sqrt(area) * 10 / Dref  # Side at 10 cm

    centrePoint = aRay.source + aRay.vector / aRay.length * 10  # point at 10 cm up on the midline of the ray

    xvector = np.array([np.sin(aRay.xangle), 0, -np.cos(aRay.xangle)])
    yvector = np.array([0, np.sin(aRay.yangle), np.cos(aRay.yangle)])
    pointA = centrePoint + ((sideLength / 2) * xvector) + ((sideLength / 2) * yvector)
    pointB = centrePoint + ((sideLength / 2) * xvector) - ((sideLength / 2) * yvector)
    pointC = centrePoint - ((sideLength / 2) * xvector) + ((sideLength / 2) * yvector)
    pointD = centrePoint - ((sideLength / 2) * xvector) - ((sideLength / 2) * yvector)

    triangle_1 = Triangle_3(pointD, pointB, pointC)
    triangle_2 = Triangle_3(pointA, pointB, pointC)
    return (triangle_1, triangle_2)


def buildRay(tableLongitudinal, tableLateral, tableHeight, LRangle, CCangle, Dref):
    """ This function takes RDSR geometry information and uses it to build
    an x-ray (Segment_3) taking into account translation and rotation.

    Args:
        tableLongitudinal: the table longitudinal offset as defined in the DICOM statement
        tableLateral: the table lateral offset as defined in the DICOM statement
        tableHeight: the table height offset as defined in the DICOM statement
        LRangle: the left-right angle. +90 is detector to the patient's left
        CCangle: the cranial-caudal angle in degrees. +90 is detector to the head
        Dref: the reference distance to the isocentre

    Returns:
        A ray (Segment_3) representing the x-ray beam.
    """
    x = 0
    y = 0
    z = -Dref

    LRrads = (LRangle / 360.) * 2. * math.pi
    CCrads = (CCangle / 360.) * 2. * math.pi

    sinLR = math.sin(LRrads)
    cosLR = math.cos(LRrads)
    sinCC = math.sin(CCrads)
    cosCC = math.cos(CCrads)

    # Full maths: xNew = z*sinLR + x*cosLR
    xNew = z * sinLR

    # Full maths: zStep = z*cosLR - x*sinLR
    zStep = z * cosLR

    # Full maths: yNew = y*cosCC - zStep*sinCC
    yNew = -zStep * sinCC

    # Full maths: zNew = y*sinCC + zStep*cosCC
    zNew = zStep * cosCC

    zTranslated = zNew + tableHeight

    xTranslated = xNew - tableLongitudinal

    yTranslated = yNew + tableLateral

    focus = np.array([xTranslated, yTranslated, zTranslated])
    isocentre = np.array([x - tableLongitudinal, y + tableLateral, 0 + tableHeight])

    myRay = Segment_3(focus, isocentre)

    return myRay


def checkOrthogonal(segment1, segment2):
    """ This function checks whether two segments are within 90 degrees

    Args:
        segment1: A Segment_3 line segment
        segment2: Another Segment_3 line segment

    Returns:
        A boolean: true if the segments are within 90 degrees,
        false if outside.
    """
    if (np.dot(segment1.vector, segment2.vector) >= 0):
        return True
    else:
        return False


def checkMiss(source, centre, target1, target2):
    """ This function compares two angles between a source and two targets.
    If the second target is at a steeper angle than the first, it misses.

    Args:
        source: the shared start point
        centre: the reference point to angle against
        target1: the triangle corner
        target2: the ray cell target

    Returns:
        A boolean: true if the second target misses.
    """

    mainLine = centre - source
    mainLength = np.linalg.norm(mainLine)
    target1Vec = target1 - source
    # target1Length = np.linalg.norm(target1Vec)
    target1Length = math.sqrt(math.pow(target1Vec[0], 2) + math.pow(target1Vec[1], 2) + math.pow(target1Vec[2], 2))
    target2Vec = target2 - source
    # target2Length = np.linalg.norm(target2Vec)
    target2Length = math.sqrt(math.pow(target2Vec[0], 2) + math.pow(target2Vec[1], 2) + math.pow(target2Vec[2], 2))

    angle1 = np.arccos(np.dot(mainLine, target1Vec) / (mainLength * target1Length))
    angle2 = np.arccos(np.dot(mainLine, target2Vec) / (mainLength * target2Length))

    if abs(angle2) > abs(angle1):
        return True  # miss
    else:
        return False


def find_nearest(array, value):
    """ This function finds the closest match to a value from an array.

    Args:
        The array to search and the value to compare.

    Returns:
        The index of the matching value.
    """
    index = (np.abs(array - value)).argmin()
    return index


def getBSF(kV, Cu, size):
    """ This function gives a BSF and f-factor combined. Data from:
    Backscatter factors and mass energy-absorption coefficient ratios for diagnostic radiology dosimetry
    Hamza Benmakhlouf et al 2011 Phys. Med. Biol. 56 7179 doi:10.1088/0031-9155/56/22/012

    Args:
        kV: The peak kilovoltage
        Cu: the added copper filtration. In addition, 3.1 mm Al is assumed by default
        size: The side of the square field incident on the patient

    Returns:
        A combined backscatter factor and f-factor.
    """
    kVTable = np.array([50, 80, 110, 150])
    CuTable = np.array([0, 0.1, 0.2, 0.3, 0.6, 0.9])
    sizeTable = np.array([5, 10, 20, 35])

    lookup_kV = find_nearest(kVTable, kV)
    lookup_Cu = find_nearest(CuTable, Cu)
    lookup_Size = find_nearest(sizeTable, size)

    lookupArray = np.array([
        [[1.2, 1.3, 1.3, 1.3], [1.3, 1.3, 1.4, 1.4], [1.3, 1.4, 1.4, 1.4], [1.3, 1.4, 1.4, 1.5], [1.3, 1.4, 1.5, 1.5],
         [1.3, 1.5, 1.5, 1.6]],
        [[1.3, 1.4, 1.4, 1.5], [1.3, 1.4, 1.5, 1.5], [1.3, 1.5, 1.6, 1.6], [1.4, 1.5, 1.6, 1.7], [1.4, 1.5, 1.7, 1.7],
         [1.4, 1.5, 1.7, 1.7]],
        [[1.3, 1.4, 1.5, 1.5], [1.3, 1.5, 1.6, 1.6], [1.3, 1.5, 1.6, 1.7], [1.4, 1.5, 1.6, 1.7], [1.4, 1.5, 1.7, 1.7],
         [1.3, 1.5, 1.7, 1.7]],
        [[1.3, 1.5, 1.5, 1.6], [1.3, 1.5, 1.6, 1.6], [1.3, 1.5, 1.6, 1.7], [1.3, 1.5, 1.6, 1.7], [1.3, 1.5, 1.6, 1.7],
         [1.3, 1.5, 1.6, 1.7]]
    ])

    return lookupArray[lookup_kV, lookup_Cu, lookup_Size]


def rotateRayY(segment1, angle):
    """ This function rotates a ray around the end point of the ray by angle degrees.

    Args:
        segment1: the ray to rotateRayY
        angle: rotation angle in degrees

    Returns:
        A new ray with the same end point but the start point rotated.
    """
    isocentre = segment1.target
    translateSource = segment1.source - isocentre
    angleRads = angle / 360 * 2. * math.pi
    myY = translateSource[1]
    myX = translateSource[2] * math.sin(angleRads) + translateSource[0] * math.cos(angleRads)
    myZ = translateSource[2] * math.cos(angleRads) - translateSource[0] * math.sin(angleRads)
    newSource = np.array([myX, myY, myZ])
    newRay = Segment_3(newSource + isocentre, isocentre)
    return newRay
    
    
def getTableTrans(kV, Cu):
    """ This function gives just the table transmission factor based
    on measurements made at the Royal Free Hospital on a Siemens Artis Zeego
    in early 2016.

    Args:
        kV: The peak kilovoltage
        Cu: the added copper filtration. In addition, 3.1 mm Al is assumed by default

    Returns:
        A transmission factor for the table without a mattress.
    """
    kVTable = np.array([60, 80, 110, 125])
    CuTable = np.array([0, 0.1, 0.2, 0.3, 0.6, 0.9])

    lookup_kV = find_nearest(kVTable, kV)
    lookup_Cu = find_nearest(CuTable, Cu)

    lookupArray = np.array([
        [0.80, 0.82, 0.82, 0.82],
        [0.84, 0.84, 0.86, 0.87],
        [0.86, 0.86, 0.88, 0.88],
        [0.84, 0.86, 0.88, 0.89],
        [0.86, 0.87, 0.88, 0.90],
        [0.86, 0.87, 0.89, 0.90]   
    ])

    return lookupArray[lookup_Cu, lookup_kV]

def getTableMattressTrans(kV, Cu):
    """ This function gives a table and mattress transmission factor based
    on measurements made at the Royal Free Hospital on a Siemens Artis Zeego
    in early 2016.

    Args:
        kV: The peak kilovoltage
        Cu: the added copper filtration. In addition, 3.1 mm Al is assumed by default

    Returns:
        A combined transmission factor for table and mattress.
    """
    kVTable = np.array([60, 80, 110, 125])
    CuTable = np.array([0, 0.1, 0.2, 0.3, 0.6, 0.9])

    lookup_kV = find_nearest(kVTable, kV)
    lookup_Cu = find_nearest(CuTable, Cu)

    lookupArray = np.array([
        [0.66, 0.68, 0.71, 0.72],
        [0.73, 0.75, 0.78, 0.78],
        [0.75, 0.78, 0.81, 0.81],
        [0.76, 0.79, 0.83, 0.83],
        [0.79, 0.81, 0.85, 0.85],
        [0.80, 0.82, 0.85, 0.86]   
    ])

    return lookupArray[lookup_Cu, lookup_kV]

