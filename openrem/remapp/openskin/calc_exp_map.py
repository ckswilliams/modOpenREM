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
        pass

    def get_map(self):
        # not sure about how this works
        # DJP: I'm not sure that this is needed, as the dose map is
        # stored at self.my_dose.totalDose already.
        pass

    def get_results(self):
        # not sure about this either
        # DJP: I'm not interested in this at the moment, as I can
        # obtain the info that I need from the self.my_dose.totalDose
        # array.
        pass


# From Ed (https://bitbucket.org/openrem/openskin/issues/1/check-if-cleaned-up-code-still-works):
# In OpenREM we'll need something like:
#
# from openskin import CalcExpMap
# from remapp.models import GeneralStudyModuleAttr
#
# study = GeneralStudyModuleAttr.objects.get(pk=studyid)
# pat_mass = study.patientstudymoduleattr_set.get().patient_weight # plus test to see if present
# pat_height = study.patientstudymoduleattr_set.get().patient_size # plus test to see if present
#
# map = CalcExpMap(phantom='3D', pat_mass=pat_mass, pat_height=pat_height)
#
# for irrad in study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all():
#     map.add_view(
#         deltax = irrad.irradeventxraymechanicaldata_set.get().
#             doserelateddistancemeasurements_set.get().table_longitudinal_position,
#         deltay = irrad.irradeventxraymechanicaldata_set.get().
#             doserelateddistancemeasurements_set.get().table_lateral_position,
#         # etc
#     )
#
# django_store_image_thingy = map.get_map()
# data = map.get_results()


# From Jon (https://bitbucket.org/openrem/openskin/issues/1/check-if-cleaned-up-code-still-works):
# ** Inputs **
#
# The skin dose map requires the following per run:
#
#     testPhantom # An openSkin phantom instance
#     tableTrans  # The table transmission (not yet implemented)
#
#     typeOfRun   # Acquisition, Fluoroscopy, Rotational etc. Needed to separate spins from normal use
#     deltax      # Table longitudinal position in cm. Isocentre to the patient's right is positive
#     deltay      # Table lateral position in cm. Isocentre towards the patient's feet is positive
#     deltaz      # Table height position in cm. Table below the isocentre is positive
#     anglex     # Positioner primary angle in degrees. +90 is detector to the patient's left, 180 is tube above patient
#     angley      # Positioner secondary angle in degrees. +90 is detector to the head, -90 is detector to the feet
#     Dref        # Distance from the focus to the interventional reference point
#     * One of *
#         dap     # Used to calculate the area of the beam in Gy.m^2
#         area    # Area of the beam in cm^2
#     refAK       # Air kerma at the interventional reference point in Gy
#     kV          # kV reported for the run
#     filterCu    # Copper filter thickness reported for the run in mm
#     endAngle    # *Rotational only* Angle where the spin stops in degrees
#     frames      # *Rotational only* Number of frames in the rotational acquisition
#
#
# A 3D testPhantom can be generated using:
#
#     mass        # The patient mass in kg
#     height      # The patient height in cm
# We also need to decide a few things about outputs. OpenSkin currently prints
# peak dose (in Gy) and the number of cm^2 over 3, 5 and 10 Gy to a file. It
# also generates a 16 bit greyscale PNG scaled so that white is 10 Gy. However,
# it is fairly simple to change those outputs to whatever is desired (colour or
# greyscale, different scaling, per run images or data, acquisition versus fluoro
# etc). It depends what is sensible to give OpenREM.
#
# 2015-06-26
# Jonathan Cole
# I've added table and mattress transmission correction, so the thickness and
# attenuation will need to be included somewhere in the call to openskin or a
# config file too.
