# This Python file uses the following encoding: utf-8
# test_dicom_qr.py

import os
from django.test import TestCase
import uuid
from remapp.netdicom import qrscu
from remapp.models import DicomQuery, DicomQRRspStudy, DicomQRRspSeries


class DicomQR(TestCase):
    def setUp(self):
        """
        """

        query = DicomQuery.objects.create()
        query.query_id = uuid.uuid4()
        query.save()

        rst1 = DicomQRRspStudy.objects.create(dicom_query=query)
        rst1.query_id = query.query_id
        rst1.study_instance_uid = uuid.uuid4()
        rst1.study_description = u"test response 1"
        rst1.station_name = u""
        rst1.save()

        rst1s1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=rst1)
        rst1s1.query_id = query.query_id
        rst1s1.series_instance_uid = uuid.uuid4()
        rst1s1.modality = u"CT"
        rst1s1.series_number = 1
        rst1s1.series_description = u"scan projection radiograph"
        rst1s1.number_of_series_related_instances = 1
        rst1s1.save()

        rst1s2 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=rst1)
        rst1s2.query_id = query.query_id
        rst1s2.series_instance_uid = uuid.uuid4()
        rst1s2.modality = u"CT"
        rst1s2.series_number = 3
        rst1s2.series_description = u"thorax and abdomen"
        rst1s2.number_of_series_related_instances = 300
        rst1s2.save()

        rst1s3 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=rst1)
        rst1s3.query_id = query.query_id
        rst1s3.series_instance_uid = uuid.uuid4()
        rst1s3.modality = u"SC"
        rst1s3.series_number = 2394
        rst1s3.series_description = u"dose info"
        rst1s3.number_of_series_related_instances = 1
        rst1s3.save()

        rst1_series_rsp = rst1.dicomqrrspseries_set.all()
        rst1.set_modalities_in_study(list(set(val for dic in rst1_series_rsp.values('modality') for val in dic.values())))
        rst1.save()

    def test_response_sorting_ct_philips_with_desc(self):
        """
        Study response contains a Philips style 'dose info' series, with study descriptions available, and no structured
        report series. Expect a single series to be left after pruning.
        """
        all_mods = {'CT': {'inc': True, 'mods': ['CT']},
                    'MG': {'inc': False, 'mods': ['MG']},
                    'FL': {'inc': False, 'mods': ['RF', 'XA']},
                    'DX': {'inc': False, 'mods': ['DX', 'CR']}
                    }

        query = DicomQuery.objects.get()
        rst1 = query.dicomqrrspstudy_set.all()[0]

        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 3)

        qrscu._prune_series_responses(query, all_mods)

        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 1)
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 1)
        self.assertEqual(rst1.dicomqrrspseries_set.all()[0].series_description, u"dose info")

    def test_response_sorting_ct_philips_no_desc(self):
        """
        Study response contains a Philips style 'dose info' series, but without study descriptions available, and no
        structured report series. Expect two series to be left after pruning, with the main series removed.
        """
        all_mods = {'CT': {'inc': True, 'mods': ['CT']},
                    'MG': {'inc': False, 'mods': ['MG']},
                    'FL': {'inc': False, 'mods': ['RF', 'XA']},
                    'DX': {'inc': False, 'mods': ['DX', 'CR']}
                    }

        query = DicomQuery.objects.get()
        rst1 = query.dicomqrrspstudy_set.all()[0]

        rst1_series_rsp = rst1.dicomqrrspseries_set.all()
        rst1s1 = rst1_series_rsp[0]
        rst1s2 = rst1_series_rsp[1]
        rst1s3 = rst1_series_rsp[2]
        rst1s1.series_description = None
        rst1s2.series_description = None
        rst1s3.series_description = None
        rst1s1.save()
        rst1s2.save()
        rst1s3.save()

        # Before pruning, three series
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 3)

        qrscu._prune_series_responses(query, all_mods)

        # After pruning, two series
        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 1)
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 2)
