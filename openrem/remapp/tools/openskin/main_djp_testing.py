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

import csv
from Tkinter import *
from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename

import calc_exp_map

root = Tk()
root.withdraw()

my_exp_map = calc_exp_map.CalcExpMap(phantom_type='3D',
                                     pat_mass=73.2, pat_height=178.6,
                                     table_thick=0.5, table_trans=0.8, table_width=40.0, table_length=150.0,
                                     matt_thick=4.0, matt_trans=0.75)

csv_file = askopenfilename(title='Choose a CSV file')

saveFolder = askdirectory(title='Choose folder to save results')

f = open(csv_file, 'rU')
csv_f = csv.reader(f)

for row in csv_f:
    refAK = float(row[11])
    if not refAK == 0:
        delta_x = float(row[34]) / 10.
        delta_y = float(row[35]) / 10.
        delta_z = float(row[36]) / 10.
        angle_x = float(row[12])
        angle_y = float(row[13])
        D_ref = float(row[33]) / 10. - 15
        area = float(row[10]) / refAK * 100. * 100.
        kV = float(row[24])

        if row[19] == "":
            filterCu = 0.0
        else:
            filterCu = float(row[19])

        typeOfRun = row[6]

        if "Rotational" in typeOfRun:
            frames = float(row[23])
            endAngle = float(row[14])
        else:
            frames = None
            endAngle = None

        my_exp_map.add_view(delta_x=delta_x, delta_y=delta_y, delta_z=delta_z,
                            angle_x=angle_x, angle_y=angle_y,
                            d_ref=D_ref, dap=float(row[10]), ref_ak=refAK,
                            kvp=kV, filter_cu=filterCu,
                            run_type=typeOfRun, frames=frames, end_angle=endAngle)

# The following line will return an array of doses that could
# then be used to construct an image on-screen. This will be
# useful when wanting to display a 2D representation of the
# dose map on screen. It will also be used to calculate the
# texture to wrap around a three.js 3D model.
skin_dose_array = my_exp_map.my_dose.totalDose

# The following three lines can be ued to obtain the dimensions
# of the 3D phantom in terms of width, height and depth. These
# will be useful when using the data to display on-screen as a
# three.js 3D model.
phantom_width = my_exp_map.phantom.phantom_width
phantom_height = my_exp_map.phantom.phantom_height
phantom_depth = my_exp_map.phantom.phantom_depth
