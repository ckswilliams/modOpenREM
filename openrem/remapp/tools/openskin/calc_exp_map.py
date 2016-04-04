import geomclass
import geomfunc
import skinMap


class CalcExpMap(object):

    def __init__(self, phantom_type=None,
                 pat_mass=73.2, pat_height=178.6,
                 table_thick=0.5, table_trans=0.8, table_width=40.0, table_length=150.0,
                 matt_thick=4.0, matt_trans=0.75):

        self.phantom_type = phantom_type
        self.pat_mass = pat_mass
        self.pat_height = pat_height
        self.table_thick = table_thick
        self.table_trans = table_trans
        self.table_width = table_width
        self.table_length = table_length
        self.matt_thick = matt_thick
        self.matt_trans = matt_trans

        if self.phantom_type == 'flat':
            # I think that the values passed to geomclass.Phantom below should be parameters
            # rather than hard-written values. Is that correct?
            # def __init__(self, phantomType, origin, width, height, depth, scale):
            # self.phantom = geomclass.Phantom("flat", [025, 0, 0], 50, 150, 10, 1)
            # Where does the 025 come from?
            # The 10 refers to the phantom depth, but isn't used by geomclass.Phantom...
            # The 1 is the scale
            self.phantom = geomclass.Phantom("flat", [025, 0, 0], self.table_width, self.table_length, 10, 1)

            self.matt_trans = 1.0
            self.matt_thick = 0.0

        elif self.phantom_type == "3D":
            self.phantom = geomclass.Phantom_3([0, -25, -self.matt_thick], mass=self.pat_mass, height=self.pat_height)

        self.my_dose = geomclass.SkinDose(self.phantom)
        self.num_views = 0

    def add_view(self,
                 delta_x=None, delta_y=None, delta_z=None,
                 angle_x=None, angle_y=None,
                 d_ref=None, dap=None, ref_ak=None,
                 kvp=None, filter_cu=None,
                 run_type=None, frames=None, end_angle=None):

        self.my_dose.addView(str(self.num_views))
        self.num_views += 1

        area = dap / ref_ak * 100. * 100.

        x_ray = geomfunc.buildRay(delta_x, delta_y, delta_z, angle_x, angle_y, d_ref + 15)

        if 'Rotational' in run_type:
            self.my_dose.addDose(skinMap.rotational(x_ray, angle_x, end_angle, int(frames), self.phantom, area, ref_ak,
                                                    kvp, filter_cu, d_ref,
                                                    self.table_length, self.table_width,
                                                    self.matt_trans * self.table_trans,
                                                    self.table_thick + self.matt_thick))
        else:
            self.my_dose.addDose(skinMap.skinMap(x_ray, self.phantom, area, ref_ak, kvp, filter_cu, d_ref,
                                                 self.table_length, self.table_width,
                                                 self.matt_trans * self.table_trans,
                                                 self.table_thick + self.matt_thick))
