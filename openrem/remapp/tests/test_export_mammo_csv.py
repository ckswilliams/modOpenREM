# test_get_values.py

import os
from decimal import Decimal
from django.test import TestCase
from remapp.exports.exportcsv import exportMG2excel
from remapp.models import GeneralStudyModuleAttr, UniqueEquipmentNames
from remapp.tools.hash_id import hash_id

class ExportMammoCSV(TestCase):
    def test_export_no_ascii(self):
        """

        """
        study = GeneralStudyModuleAttr.objects.create()
        study.save()
        equip = study.generalequipmentmoduleattr_set.create()
        equip.institution_name = "Institution"
        equip.institutional_department_name = "Department"
        equip.manufacturer = "Manufacturer"
        equip.manufacturer_model_name = "Model name"
        equip.station_name = "stationname"
        equip.device_serial_number = "123abc"
        equip.software_versions = "version 123.456"
        equip.gantry_id = "gantry123abc"
        equip.save()

        equip_display_name, created = UniqueEquipmentNames.objects.get_or_create(manufacturer=equip.manufacturer,
                                                                                 manufacturer_hash=hash_id(equip.manufacturer),
                                                                                 institution_name=equip.institution_name,
                                                                                 institution_name_hash=hash_id(
                                                                                     equip.institution_name),
                                                                                 station_name=equip.station_name,
                                                                                 station_name_hash=hash_id(equip.station_name),
                                                                                 institutional_department_name=equip.institutional_department_name,
                                                                                 institutional_department_name_hash=hash_id(
                                                                                     equip.institutional_department_name),
                                                                                 manufacturer_model_name=equip.manufacturer_model_name,
                                                                                 manufacturer_model_name_hash=hash_id(
                                                                                     equip.manufacturer_model_name),
                                                                                 device_serial_number=equip.device_serial_number,
                                                                                 device_serial_number_hash=hash_id(
                                                                                     equip.device_serial_number),
                                                                                 software_versions=equip.software_versions,
                                                                                 software_versions_hash=hash_id(
                                                                                     equip.software_versions),
                                                                                 gantry_id=equip.gantry_id,
                                                                                 gantry_id_hash=hash_id(equip.gantry_id),
                                                                                 hash_generated=True
                                                                                 )
        if created:
            if equip.institution_name and equip.station_name:
                equip_display_name.display_name = equip.institution_name + ' ' + equip.station_name
            elif equip.institution_name:
                equip_display_name.display_name = equip.institution_name
            elif equip.station_name:
                equip_display_name.display_name = equip.station_name
            else:
                equip_display_name.display_name = 'Blank'
            equip_display_name.save()

        equip.unique_equipment_name = UniqueEquipmentNames(pk=equip_display_name.pk)
        equip.save()


