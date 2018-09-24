# This Python file uses the following encoding: utf-8
#    OpenREM - Radiation Exposure Monitoring tools for the physicist
#    Copyright (C) 2012,2013  The Royal Marsden NHS Foundation Trust
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    Additional permission under section 7 of GPLv3:
#    You shall not make any use of the name of The Royal Marsden NHS
#    Foundation trust in connection with this Program in any press or
#    other public announcement without the prior written consent of
#    The Royal Marsden NHS Foundation Trust.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
..  module:: make_skin_map.
    :synopsis: Module to calculate skin dose map from study data.

..  moduleauthor:: Ed McDonagh, David Platten

"""

import os
import sys
import logging
import django

# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1,projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

from celery import shared_task

logger = logging.getLogger('remapp.tools.make_skin_map')  # Explicitly named so that it is still handled when using __main__


@shared_task(name='remapp.tools.make_skin_map', ignore_result=True)
def make_skin_map(study_pk=None):
    import remapp.tools.openskin.calc_exp_map as calc_exp_map
    from remapp.models import GeneralStudyModuleAttr
    from openremproject.settings import MEDIA_ROOT
    import cPickle as pickle
    import gzip
    from remapp.version import __skin_map_version__
    from django.core.exceptions import ObjectDoesNotExist
    import numpy as np

    if study_pk:
        study = GeneralStudyModuleAttr.objects.get(pk=study_pk)

        pat_mass_source = u'assumed'
        try:
            pat_mass = float(study.patientstudymoduleattr_set.get().patient_weight)
            pat_mass_source = u'extracted'
        except (ValueError, TypeError):
            pat_mass = 73.2

        if pat_mass == 0.0:
            pat_mass = 73.2
            pat_mass_source = u'assumed'

        pat_height_source = u'assumed'
        try:
            pat_height = float(study.patientstudymoduleattr_set.get().patient_size) * 100
            pat_height_source = u'extracted'
        except (ValueError, TypeError):
            pat_height = 178.6

        if pat_height == 0.0:
            pat_height = 178.6
            pat_height_source = u'assumed'

        ptr = None
        orientation_modifier = None
        try:
            ptr_meaning = study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[
                0].patient_table_relationship_cid.code_meaning.lower()
            if ptr_meaning in u"headfirst":
                ptr = u"H"
            elif ptr_meaning in u"feet-first":
                ptr = u"F"
            else:
                logger.info(u"Study PK {0}: Patient table relationship not recognised ({1}). "
                            u"Assuming head first.".format(study_pk, ptr_meaning))
        except AttributeError:
            logger.info(u"Study PK {0}: Patient table relationship not found. Assuming head first.".format(study_pk))
        except IndexError:
            logger.info(u"Study PK {0}: No irradiation event x-ray data found. Assuming head first.".format(study_pk))
        try:
            orientation_modifier_meaning = study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[
                0].patient_orientation_modifier_cid.code_meaning.lower()
            if orientation_modifier_meaning in u"supine":
                orientation_modifier = u"S"
            elif orientation_modifier_meaning in u"prone":
                orientation_modifier = u"P"
            else:
                logger.info(u"Study PK {0}: Orientation modifier not recognised ({1}). "
                            u"Assuming supine.".format(study_pk, orientation_modifier_meaning))
        except AttributeError:
            logger.info(u"Study PK {0}: Orientation modifier not found. Assuming supine.".format(study_pk))
        except IndexError:
            logger.info(u"Study PK {0}: No irradiation event x-ray data found. Assuming supine.".format(study_pk))
        if ptr and orientation_modifier:
            pat_pos_source = u"extracted"
            patPos = ptr + u"F" + orientation_modifier
        elif ptr:
            pat_pos_source = u"supine assumed"
            patPos = ptr + u"FS"
        elif orientation_modifier:
            pat_pos_source = u"head first assumed"
            patPos = u"HF" + orientation_modifier
        else:
            pat_pos_source = u"assumed"
            patPos = u"HFS"
        logger.debug(u"patPos is {0} and source is {1}".format(patPos, pat_pos_source))

        my_exp_map = calc_exp_map.CalcExpMap(phantom_type='3D', patPos=patPos,
                                             pat_mass=pat_mass, pat_height=pat_height,
                                             table_thick=0.5, table_width=40.0, table_length=150.0,
                                             matt_thick=4.0)

        for irrad in study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all():
            try:
                delta_x = float(irrad.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(
                                                                                ).table_longitudinal_position) / 10.0
            except (ObjectDoesNotExist, TypeError):
                delta_x = 0.0
            try:
                delta_y = float(irrad.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(
                                                                                        ).table_lateral_position) / 10.0
            except (ObjectDoesNotExist, TypeError):
                delta_y = 0.0
            try:
                delta_z = float(irrad.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(
                                                                                        ).table_height_position) / 10.0
            except (ObjectDoesNotExist, TypeError):
                delta_z = 0.0
            if irrad.irradeventxraymechanicaldata_set.get().positioner_primary_angle:
                angle_x = float(irrad.irradeventxraymechanicaldata_set.get().positioner_primary_angle)
            else:
                angle_x = 0.0
            try:
                angle_y = float(irrad.irradeventxraymechanicaldata_set.get().positioner_secondary_angle)
            except (ObjectDoesNotExist, TypeError):
                angle_y = 0.0
            try:
                d_ref = float(irrad.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(
                                                                        ).distance_source_to_isocenter) / 10.0 - 15.0
            except (ObjectDoesNotExist, TypeError):
                # This will result in failure to calculate skin dose map. Need a sensible default, or a lookup to a
                # user-entered value
                d_ref = None
            try:
                dap = float(irrad.dose_area_product)
            except (ObjectDoesNotExist, TypeError):
                dap = None
            try:
                ref_ak = float(irrad.irradeventxraysourcedata_set.get().dose_rp)
            except (ObjectDoesNotExist, TypeError):
                ref_ak = None
            try:
                kvp = np.mean(irrad.irradeventxraysourcedata_set.get().kvp_set.all().exclude(kvp__isnull=True).exclude(kvp__exact=0).values_list('kvp', flat=True))
                kvp = float(kvp)
                if np.isnan(kvp):
                    kvp = None
            except (ObjectDoesNotExist, TypeError):
                kvp = None

            filter_cu = 0.0
            if irrad.irradeventxraysourcedata_set.get().xrayfilters_set.all():
                for xray_filter in irrad.irradeventxraysourcedata_set.get().xrayfilters_set.all():
                    try:
                        if xray_filter.xray_filter_material.code_value == 'C-127F9':
                            filter_cu += float(xray_filter.xray_filter_thickness_minimum)
                    except AttributeError:
                        pass

            if irrad.irradiation_event_type:
                run_type = str(irrad.irradiation_event_type)
            else:
                run_type = None
            try:
                frames = float(irrad.irradeventxraysourcedata_set.get().number_of_pulses)
            except (ObjectDoesNotExist, TypeError):
                frames = None
            try:
                end_angle = float(irrad.irradeventxraymechanicaldata_set.get().positioner_primary_end_angle)
            except (ObjectDoesNotExist, TypeError):
                end_angle = None
            if ref_ak and d_ref:
                my_exp_map.add_view(delta_x=delta_x, delta_y=delta_y, delta_z=delta_z,
                                    angle_x=angle_x, angle_y=angle_y,
                                    d_ref=d_ref, dap=dap, ref_ak=ref_ak,
                                    kvp=kvp, filter_cu=filter_cu,
                                    run_type=run_type, frames=frames, end_angle=end_angle, patPos=patPos)

        # Flip the skin dose map left-right so the view is from the front
        # my_exp_map.my_dose.fliplr()
        my_exp_map.my_dose.totalDose = np.roll(my_exp_map.my_dose.totalDose,
                                               int(my_exp_map.phantom.phantom_flat_dist / 2),
                                               axis=0)
        try:
            my_exp_map.my_dose.totalDose = np.rot90(my_exp_map.my_dose.totalDose)
        except ValueError:
            pass

        return_structure = {
            'skin_map': my_exp_map.my_dose.totalDose.flatten().tolist(),
            'width': my_exp_map.phantom.width,
            'height': my_exp_map.phantom.height,
            'phantom_width': my_exp_map.phantom.phantom_width,
            'phantom_height': my_exp_map.phantom.phantom_height,
            'phantom_depth': my_exp_map.phantom.phantom_depth,
            'phantom_flat_dist': my_exp_map.phantom.phantom_flat_dist,
            'phantom_curved_dist': my_exp_map.phantom.phantom_curved_dist,
            'patient_height': pat_height,
            'patient_mass': pat_mass,
            'patient_orientation': patPos,
            'patient_height_source': pat_height_source,
            'patient_mass_source': pat_mass_source,
            'patient_orientation_source': pat_pos_source,
            'skin_map_version': __skin_map_version__
        }

        # Save the return_structure as a pickle in a skin_maps sub-folder of the MEDIA_ROOT folder
        try:
            study_date = study.study_date
            if study_date:
                skin_map_path = os.path.join(MEDIA_ROOT, 'skin_maps', "{0:0>4}".format(study_date.year),
                                             "{0:0>2}".format(study_date.month), "{0:0>2}".format(study_date.day))
            else:
                skin_map_path = os.path.join(MEDIA_ROOT, 'skin_maps')
        except:
            skin_map_path = os.path.join(MEDIA_ROOT, 'skin_maps')

        if not os.path.exists(skin_map_path):
            os.makedirs(skin_map_path)

        with gzip.open(os.path.join(skin_map_path, 'skin_map_' + str(study_pk) + '.p'), 'wb') as f:
            pickle.dump(return_structure, f)
