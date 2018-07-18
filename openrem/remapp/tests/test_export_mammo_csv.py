# This Python file uses the following encoding: utf-8
# test_export_mammo_csv.py

import hashlib
import os
from collections import Counter
from django.contrib.auth.models import User, Group
from django.test import TestCase, RequestFactory
from remapp.extractors import mam, rdsr
from remapp.exports.mg_export import exportMG2excel
from remapp.exports.mg_csv_nhsbsp import mg_csv_nhsbsp
from remapp.models import PatientIDSettings, Exports

class ExportMammoCSV(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        eg = Group(name="exportgroup")
        eg.save()
        eg.user_set.add(self.user)
        eg.save()

        PatientIDSettings.objects.create()

        dicom_file = os.path.join("test_files", "MG-Im-GE-SenDS-scaled.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        mam(dicom_path)

    def test_all_values(self):
        import pandas as pd

        filter_set = {}
        pid = False
        name = False
        patient_id = False

        exportMG2excel(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        task = Exports.objects.all()[0]
        csvdf = pd.read_csv(task.filename.path)

        cols = ['Institution', 'Manufacturer', 'Model name', 'Station name', 'Display name', 'Accession number',
                'Operator', 'Study date', 'Study time', 'Age', 'Sex', 'Test patient?', 'Study description',
                'Requested procedure', 'Study Comments', 'No. events',
                'View', 'Laterality', 'Acquisition', 'Thickness', 'Radiological thickness', 'Force', 'Mag', 'Area',
                'Mode', 'Target', 'Filter', 'Filter thickness', 'Focal spot size', 'kVp', 'mA', 'ms', 'uAs', 'ESD',
                'AGD', '% Fibroglandular tissue', 'Exposure mode description']
        exportline = ['中心医院', 'GE MEDICAL SYSTEMS', 'Senograph DS ADS_43.10.1', 'SENODS01', '中心医院 SENODS01',
                      'AAAA9876', '', '2013-04-12', '12:35:46',
                      '0.000', 'O', '', '', '', '', '1', 'cranio-caudal', 'Left', 'ROUTINE', '53.00000000',
                      '45.00000000', '50.00000000', '1.00000000', '0.04373900', 'AUTOMATIC',
                      'Rh', 'Rh', '', '0.30000000', '29.00000000',
                      '61.00000000', '834.00', '51800.00', '5.07100000', '1.37300000', '31.00000000',
                      'AOP standard RECTANGLE 1662 mm 10 mm 180 mm 240 mm EXP DOSE 87504 nGy PRE-EXP DOSE 5655 nGy '
                      'PRE-EXP THICK 45 mm PRE-EXP COMPO 29 % PRE-EXP KV 28 PRE-EXP TRACK Rh PRE-EXP FILTER Rh PADDLE '
                      '1 FLATFIELD no']
        refdf = pd.DataFrame([exportline], columns=cols, index=range(1))

        self.assertEqual(list(csvdf.columns), cols)
        for col in cols:
            if pd.isnull(csvdf[col][0]):  # deals with missing data
                self.assertEqual('', refdf[col][0])
            elif type(csvdf[col][0]) is str:  # compare all the string values
                self.assertEqual(csvdf[col][0], refdf[col][0])
            else:  # assume all other values are numbers
                self.assertAlmostEqual(csvdf[col][0], float(refdf[col][0]))

        # cleanup
        task.filename.delete()  # delete file so local testing doesn't get too messy!
        task.delete()  # not necessary, by hey, why not?

class ExportMammoCSVNHSBSP(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        eg = Group(name="exportgroup")
        eg.save()
        eg.user_set.add(self.user)
        eg.save()

        PatientIDSettings.objects.create()

        dicom_file = os.path.join("test_files", "MG-RDSR-Hologic_mix.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)

    def test_nhsbsp(self):
        import pandas as pd

        filter_set = {u'o': '-projectionxrayradiationdose__accumxraydose__accummammographyxraydose__accumulated_'
                            'average_glandular_dose'}

        mg_csv_nhsbsp(filter_set, user=self.user)

        task = Exports.objects.all()[0]
        csvdf = pd.read_csv(task.filename.path)

        # Test there are only seven data rows (and fifteen columns), ie no duplication from AGD ordering
        self.assertEqual(csvdf.shape, (7, 15))

        # Test all three filters are in the results in the right quantities
        self.assertEqual(Counter(csvdf.Filter.tolist()), Counter(['Al', 'Al', 'Al', 'Al', 'Ag', 'Rh', 'Rh']))

        # Test numbered view codes
        self.assertEqual(
            Counter(csvdf['View code'].tolist()), Counter(['RCC', 'RCC2', 'RCC3', 'RCC4', 'RCC5', 'ROB', 'LCC']))

        # Test each row
        rcc1 = csvdf[csvdf['View code'].str.contains('RCC') & (csvdf['Filter'] == 'Al') & (csvdf['Thickness'] == 19.0)]
        self.assertAlmostEquals(rcc1.mAs.values[0], 34.3)
        self.assertAlmostEquals(rcc1.kV.values[0], 26.0)

        rcc4 = csvdf[csvdf['View code'].str.contains('RCC') & (csvdf['Filter'] == 'Al') & (csvdf['Thickness'] == 20.0)]
        self.assertAlmostEquals(rcc4.mAs.values[0], 33.9)
        self.assertAlmostEquals(rcc4.kV.values[0], 26.0)

        rob1 = csvdf[csvdf['View code'].str.contains('ROB')]
        self.assertAlmostEquals(rob1.mAs.values[0], 35.6)
        self.assertAlmostEquals(rob1.kV.values[0], 26.0)
        self.assertEqual(rob1.Filter.values[0], 'Al')
        self.assertAlmostEquals(rob1.Thickness.values[0], 21.0)

        lcc1 = csvdf[csvdf['View code'].str.contains('LCC')]
        self.assertAlmostEquals(lcc1.mAs.values[0], 33.9)
        self.assertAlmostEquals(lcc1.kV.values[0], 26.0)
        self.assertEqual(lcc1.Filter.values[0], 'Al')
        self.assertAlmostEquals(lcc1.Thickness.values[0], 20.0)

        rcc2 = csvdf[csvdf['View code'].str.contains('RCC') & (csvdf['Filter'] == 'Rh') & (csvdf['Thickness'] == 23.0)]
        self.assertAlmostEquals(rcc2.mAs.values[0], 17.9)
        self.assertAlmostEquals(rcc2.kV.values[0], 20.0)

        rcc5 = csvdf[csvdf['View code'].str.contains('RCC') & (csvdf['Filter'] == 'Rh') & (csvdf['Thickness'] == 46.0)]
        self.assertAlmostEquals(rcc5.mAs.values[0], 17.8)
        self.assertAlmostEquals(rcc5.kV.values[0], 20.0)

        rcc3 = csvdf[csvdf['View code'].str.contains('RCC') & (csvdf['Filter'] == 'Ag')]
        self.assertAlmostEquals(rcc3.mAs.values[0], 17.9)
        self.assertAlmostEquals(rcc3.kV.values[0], 20.0)
        self.assertAlmostEquals(rcc3.Thickness.values[0], 128.0)


