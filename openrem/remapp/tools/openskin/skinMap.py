""" 
    Copyright 2015 Jonathan Cole

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

from geomfunc import *
import time


def skinMap(xRay, phantom, area, refAK, kV, filterCu, Dref, tableLength, tableWidth, transmission,
            tableMattressThickness):
    """ This function calculates a skin dose map.

    Args:
        xRay: the x-ray beam as a Segment_3
        phantom: the phantom object representing the surface to map on
        area: the area of the beam at the reference point in square cm
        refAK: the air kerma at the reference point
        kV: the peak kilovoltage
        filterCu: the copper filter thickness in mm
        Dref: the distance to the interventional reference point in cm
        tableLength: the length of the table in cm from head to foot
        tableWidth: the width of the table in cm
        transmission: the table and/or mattress transmission as a decimal (0 to 1.0)
        tableMattressThickness: the table and/or mattress thickess in cm

    Returns:
        An array containing doses for each cell in the phantom.
    """
    refLength_squared = math.pow(Dref, 2)

    skinMap = np.zeros((phantom.width, phantom.height))
    focus = xRay.source
    table1 = Triangle_3(np.array([-tableWidth / 2, 0, 0]), np.array([tableWidth / 2, 0, 0]),
                        np.array([-tableWidth / 2, tableLength, 0]))
    table2 = Triangle_3(np.array([-tableWidth / 2, tableLength, 0]), np.array([tableWidth / 2, tableLength, 0]),
                        np.array([tableWidth / 2, 0, 0]))

    it = np.nditer(skinMap, op_flags=['readwrite'], flags=['multi_index'])

    (myTriangle1, myTriangle2) = collimate(xRay, area, Dref)

    while not it.finished:

        lookup_row = it.multi_index[0]
        lookup_col = it.multi_index[1]
        myX = phantom.phantomMap[lookup_row, lookup_col][0]
        myY = phantom.phantomMap[lookup_row, lookup_col][1]
        myZ = phantom.phantomMap[lookup_row, lookup_col][2]
        myRay = Segment_3(focus, np.array([myX, myY, myZ]))
        reverseNormal = phantom.normalMap[lookup_row, lookup_col]

        if checkOrthogonal(reverseNormal, myRay):
            # Check to see if the beam hits the patient
            hit1 = intersect(myRay, myTriangle1)
            hit2 = intersect(myRay, myTriangle2)
            if hit1 is "hit" or hit2 is "hit":

                # Check to see if the beam passes through the table
                tableNormal = Segment_3(np.array([0, 0, 0]), np.array([0, 0, 1]))
                hitTable1 = intersect(myRay, table1)
                hitTable2 = intersect(myRay, table2)
                # If the beam passes the table and does so on the way in to the patient, correct the AK
                if hitTable1 is "hit" or hitTable2 is "hit":
                    if checkOrthogonal(tableNormal, myRay):
                        sinAlpha = xRay.vector[2] / xRay.length
                        pathLength = tableMattressThickness / sinAlpha
                        mu = np.log(transmission) / (-tableMattressThickness)
                        tableCor = np.exp(-mu * pathLength)
                        refAKcor = refAK * tableCor
                    # If the beam is more than 90 degrees (ie above the table) leave the AK alone
                    else:
                        refAKcor = refAK
                # If the beam doesn't pass through the table, leave the AK alone
                else:
                    refAKcor = refAK

                # Calculate the dose at the skin point by correcting for distance and BSF
                mylengthSquared = pow(myRay.length, 2)
                it[0] = refLength_squared / mylengthSquared * refAKcor * getBSF(kV, filterCu, math.sqrt(
                    mylengthSquared / refLength_squared))

        it.iternext()

    return skinMap


def rotational(xRay, startAngle, endAngle, frames, phantom, area, refAK, kV, filterCu, Dref, tableLength, tableWidth,
               transmission, tableMattressThickness):
    """ This function computes the dose from a rotational exposure.

    Args:
        xRay: the initial ray
        startAngle: the initial angle in degrees
        endAngle: the stop angle in degrees
        frames: the number of frames in the rotation
        phantom: the geomclass.phantom class being exposed
        area: the area of the beam
        refAK: the air kerma at the reference point
        kV: the kV used for the exposure
        filterCu: the copper filter used, if any
        Dref: the reference distance
        tableLength: the length of the table in cm from head to foot
        tableWidth: the width of the table in cm
        transmission: the table and/or mattress transmission as a decimal (0 to 1.0)
        tableMattressThickness: the table and/or mattress thickess in cm

    Returns:
        A skin dose map.

    """
    rotationAngle = (endAngle - startAngle) / frames
    myDose = skinMap(xRay, phantom, area, refAK / frames, kV, filterCu, Dref, tableLength, tableWidth, transmission,
                     tableMattressThickness)
    for i in range(1, frames - 1):
        xRay = rotateRayY(xRay, rotationAngle)
        myDose = myDose + skinMap(xRay, phantom, area, refAK / frames, kV, filterCu, Dref, tableLength, tableWidth,
                                  transmission, tableMattressThickness)
    return myDose


def skinMapToPng(colour, totalDose, filename, testPhantom, encode_16_bit_colour=None):
    """ Writes a dose map to a PNG file.

    Args:
        colour: a boolean choice of colour or black and white
        filename: the file name to write the PNG to
        testPhantom: the phantom used for calculations
        totalDose: the dose map to write

    Returns:
        Nothing.

    """

    import png

    if colour:
        threshDose = 5.

        blue = np.zeros((testPhantom.width, testPhantom.height))

        red = totalDose * (255. / threshDose)
        red[totalDose[:, :] > threshDose] = 255

        green = (totalDose - threshDose) * (-255. / threshDose) + 255.
        green[green[:, :] > 255] = 255
        green[totalDose[:, :] == 0] = 0

        image_3d = np.dstack((red, green, blue))
        image_3d = np.reshape(image_3d, (-1, testPhantom.height * 3))

        f = open(filename, 'wb')

        w = png.Writer(testPhantom.height, testPhantom.width, greyscale=False, bitdepth=8)
        w.write(f, image_3d)
        f.close()

    elif encode_16_bit_colour:
        # White at 10 Gy
        threshDose = 10.
        totalDose = totalDose / threshDose * 65535.

        r, g = divmod(totalDose, 255)
        # r is the number of times 255 goes into totalDose; g is the remainder

        b = np.empty([testPhantom.width, testPhantom.height])
        b.fill(255)

        # To reconstruct the 16-bit value, do (r * b) + g

        image_3d = np.dstack((r, g, b))
        image_3d = np.reshape(image_3d, (-1, testPhantom.height * 3))

        f = open(filename, 'wb')

        w = png.Writer(testPhantom.height, testPhantom.width, greyscale=False, bitdepth=8)
        w.write(f, image_3d)
        f.close()

    else:
        # White at 10 Gy
        threshDose = 10.
        totalDose = totalDose / threshDose * 65535.

        f = open(filename, 'wb')

        w = png.Writer(testPhantom.height, testPhantom.width, greyscale=True, bitdepth=16)
        w.write(f, totalDose)
        f.close()


def writeResultsToTxt(txtfile, csvfile, testPhantom, myDose):
    """ This function writes useful skin dose results to a text file.

    Args:
        txtfile: the destination filename with path
        csvfile: the original data file name
        testPhantom: the phantom used for calculations
        myDose: the skinDose object holding the results

    Returns:
        Nothing.

    """
    totalDose = myDose.totalDose
    phantomTxt = str(testPhantom.width) + 'x' + str(testPhantom.height) + ' ' + testPhantom.phantomType + ' phantom'
    f = open(txtfile, 'w')
    f.write('{0:15} : {1:30}\n'.format('File created', time.strftime("%c")))
    f.write('{0:15} : {1:30}\n'.format('Data file', csvfile))
    f.write('{0:15} : {1:30}\n'.format('Phantom', phantomTxt))
    f.write('{0:15} : {1:30}\n'.format('Peak dose (Gy)', np.amax(totalDose)))
    f.write('{0:15} : {1:30}\n'.format('Cells > 3 Gy', np.sum(totalDose >= 3)))
    f.write('{0:15} : {1:30}\n'.format('Cells > 5 Gy', np.sum(totalDose >= 5)))
    f.write('{0:15} : {1:30}\n'.format('Cells > 10 Gy', np.sum(totalDose >= 10)))
    f.close()
