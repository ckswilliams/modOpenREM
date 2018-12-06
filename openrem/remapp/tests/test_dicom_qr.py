# This Python file uses the following encoding: utf-8
# test_dicom_qr.py

import collections
import os
import uuid

from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
from dicom.dataset import Dataset
from django.test import TestCase
from mock import patch
from netdicom.SOPclass import StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass
from netdicom.applicationentity import AE
from testfixtures import LogCapture

from remapp.extractors import rdsr
from remapp.models import DicomQuery, DicomQRRspStudy, DicomQRRspSeries, DicomQRRspImage, DicomRemoteQR, \
    DicomStoreSCP, GeneralStudyModuleAttr, PatientIDSettings
from remapp.netdicom import qrscu


def _fake_check_sr_type_in_study_with_rdsr(assoc, study, query_id):
    return 'RDSR'


fake_responses = [
    [[u'MG', u'SR'], [u'MG'], [u'OT', u'MG'], [u'PR', u'MG']],
    [[u'CT'], [u'OT', u'CT', u'SR'], [u'SR', u'CT']],
    ]


def _fake_two_modalities(assoc, d, query, query_id, *args, **kwargs):
    """
    Mock routine that returns a set of four MG studies the first time it is called, and a set of three CT studies the
    second time  it is called.

    Used by test_modality_matching

    :param my_ae:       Not used in mock
    :param remote_ae:   Not used in mock
    :param d:           Not used in mock
    :param query:       Database foreign key to create DicomQRRspStudy objects
    :param query_id:    Query ID to tie DicomQRRspStudy from this query together
    :param args:        Not used in mock
    :param kwargs:      Not used in mock
    :return:            Seven MG and CT DicomQRRspStudy objects in the database
    """
    mods = fake_responses.pop()
    for mod_list in mods:
        rsp = DicomQRRspStudy.objects.create(dicom_query=query)
        rsp.query_id = query_id
        rsp.set_modalities_in_study(mod_list)
        rsp.save()


def _fake_all_modalities(assoc, d, query, query_id, *args, **kwargs):
    """
    Mock routine to return a modality response that includes a study with a 'modalities in study' that does not have
    the requested modality in.

    Used by test_non_modality_matching

    :param my_ae:       Not used in mock
    :param remote_ae:   Not used in mock
    :param d:           Not used in mock
    :param query:       Database foreign key to create DicomQRRspStudy objects
    :param query_id:    Query ID to tie DicomQRRspStudy from this query together
    :param args:        Not used in mock
    :param kwargs:      Not used in mock
    :return:            Two DicomQRRspStudy objects in the database
    """
    mods = [[u'MG', u'SR'], [u'US', u'SR']]
    for mod_list in mods:
        rsp = DicomQRRspStudy.objects.create(dicom_query=query)
        rsp.query_id = query_id
        rsp.set_modalities_in_study(mod_list)
        rsp.save()


class StudyQueryLogic(TestCase):
    def setUp(self):
        # Remote find/move node details
        qr_scp = DicomRemoteQR.objects.create()
        qr_scp.hostname = "qrserver"
        qr_scp.port = 104
        qr_scp.aetitle = "qrserver"
        qr_scp.callingaet = "openrem"
        qr_scp.save()
        # Local store node details
        store_scp = DicomStoreSCP.objects.create()
        store_scp.aetitle = "openremstore"
        store_scp.port = 104
        store_scp.save()
        # Query db object
        query_id = uuid.uuid4()
        query = DicomQuery.objects.create()
        query.query_id = query_id
        query.complete = False
        query.store_scp_fk = store_scp
        query.qr_scp_fk = qr_scp
        query.save()

    @patch("remapp.netdicom.qrscu._query_study", side_effect=_fake_all_modalities)
    def test_non_modality_matching(self, study_query_mock):
        """
        Tests the study level query for each modality. Fake responses include a study with just US in, indicating the
        study filter doesn't work and there is no point querying for any further modalities as we'll already have the
        responses.
        :param study_query_mock: Mocked study level response routine
        :return: Nothing
        """
        from remapp.netdicom.qrscu import _query_for_each_modality

        all_mods = {'CT': {'inc': True, 'mods': ['CT']},
                    'MG': {'inc': True, 'mods': ['MG']},
                    'FL': {'inc': False, 'mods': ['RF', 'XA']},
                    'DX': {'inc': False, 'mods': ['DX', 'CR']}
                    }
        query = DicomQuery.objects.get()

        d = Dataset()
        assoc = None
        modalities_returned, modality_matching = _query_for_each_modality(all_mods, query, d, assoc)

        self.assertEqual(DicomQRRspStudy.objects.count(), 2)
        self.assertEqual(study_query_mock.call_count, 1)
        self.assertEqual(modality_matching, False)
        self.assertEqual(modalities_returned, True)

    @patch("remapp.netdicom.qrscu._query_study", side_effect=_fake_two_modalities)
    def test_modality_matching(self, study_query_mock):
        """
        Tests the study level query for each modality. Fake responses only include appropriate modalities, so
        _query_for_each_modality should return modality_matching as True
        :param study_query_mock: Mocked study level response routine
        :return:  Nothing
        """
        from remapp.netdicom.qrscu import _query_for_each_modality

        all_mods = collections.OrderedDict()
        all_mods['CT'] = {'inc': True, 'mods': ['CT']}
        all_mods['MG'] = {'inc': True, 'mods': ['MG']}
        all_mods['FL'] = {'inc': False, 'mods': ['RF', 'XA']}
        all_mods['DX'] = {'inc': False, 'mods': ['DX', 'CR']}

        query = DicomQuery.objects.get()
        qr_scp = DicomRemoteQR.objects.get()

        # Create my_ae and remote_ae
        aec = qr_scp.aetitle
        aet = qr_scp.callingaet
        ts = [
            ExplicitVRLittleEndian,
            ImplicitVRLittleEndian,
            ExplicitVRBigEndian
        ]
        my_ae = AE(aet.encode('ascii', 'ignore'), 0, [StudyRootFindSOPClass, StudyRootMoveSOPClass,
                                                      VerificationSOPClass], [], ts)
        remote_ae = dict(Address=qr_scp.hostname, Port=qr_scp.port, AET=aec.encode('ascii', 'ignore'))

        d = Dataset()
        assoc = None
        modalities_returned, modality_matching = _query_for_each_modality(all_mods, query, d, assoc)

        self.assertEqual(DicomQRRspStudy.objects.count(), 7)
        self.assertEqual(study_query_mock.call_count, 2)
        self.assertEqual(modality_matching, True)


class QRPhilipsCT(TestCase):
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
        filters = {
            'stationname_inc': None,
            'stationname_exc': None,
            'study_desc_inc': None,
            'study_desc_exc': None,
        }

        query = DicomQuery.objects.get()
        rst1 = query.dicomqrrspstudy_set.all()[0]

        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 3)

        assoc = None
        qrscu._prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)

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
        filters = {
            'stationname_inc': None,
            'stationname_exc': None,
            'study_desc_inc': None,
            'study_desc_exc': None,
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

        assoc = None
        qrscu._prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)

        # After pruning, two series
        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 1)
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 2)

    def test_response_sorting_ct_philips_with_desc_no_dose_info(self):
        """
        Study response doesn't contain a Philips style 'dose info' series or an SR series, and study descriptions
        are returned. Expect no series to be left after pruning, and the study response record deleted.
        """
        all_mods = {'CT': {'inc': True, 'mods': ['CT']},
                    'MG': {'inc': False, 'mods': ['MG']},
                    'FL': {'inc': False, 'mods': ['RF', 'XA']},
                    'DX': {'inc': False, 'mods': ['DX', 'CR']}
                    }
        filters = {
            'stationname_inc': None,
            'stationname_exc': None,
            'study_desc_inc': None,
            'study_desc_exc': None,
        }

        query = DicomQuery.objects.get()
        rst1 = query.dicomqrrspstudy_set.all()[0]
        rst1_series_rsp = rst1.dicomqrrspseries_set.order_by('id')
        rst1s3 = rst1_series_rsp[2]

        # Remove the third series with the 'dose info' description
        rst1s3.delete()

        # Before the pruning, two series
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 2)

        assoc = None
        qrscu._prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)

        # After pruning, there should be no studies left
        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 0)

    @patch("remapp.netdicom.qrscu._check_sr_type_in_study", _fake_check_sr_type_in_study_with_rdsr)
    def test_response_pruning_ct_philips_with_desc_and_sr(self):
        """
        Study response contains a Philips style 'dose info' series, with study descriptions available, and a structured
        report series. Expect a single SR series to be left after pruning.
        """
        all_mods = {'CT': {'inc': True, 'mods': ['CT']},
                    'MG': {'inc': False, 'mods': ['MG']},
                    'FL': {'inc': False, 'mods': ['RF', 'XA']},
                    'DX': {'inc': False, 'mods': ['DX', 'CR']}
                    }
        filters = {
            'stationname_inc': None,
            'stationname_exc': None,
            'study_desc_inc': None,
            'study_desc_exc': None,
        }

        query = DicomQuery.objects.get()
        rst1 = query.dicomqrrspstudy_set.all()[0]

        # Add in a fourth series with modality SR
        rst1s4 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=rst1)
        rst1s4.query_id = query.query_id
        rst1s4.series_instance_uid = uuid.uuid4()
        rst1s4.modality = u"SR"
        rst1s4.series_number = 999
        rst1s4.series_description = u"radiation dose report"
        rst1s4.number_of_series_related_instances = 1
        rst1s4.save()

        # Re-generate the modality list
        rst1_series_rsp = rst1.dicomqrrspseries_set.all()
        rst1.set_modalities_in_study(
            list(
                set(
                    val for dic in rst1_series_rsp.values('modality') for val in dic.values()
                )
            ))
        rst1.save()

        # Now starting with four series
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 4)

        assoc = None
        qrscu._prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)

        # Should now have one SR series left, identified by the series description for the purposes of this test
        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 1)
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 1)
        self.assertEqual(rst1.dicomqrrspseries_set.all()[0].series_description, u"radiation dose report")

    def test_modalities_in_study_generation(self):
        """
        Testing that ModalitiesInStudy is generated if not returned by remote C-Find SCP
        """
        from collections import Counter
        from remapp.netdicom.qrscu import _generate_modalities_in_study

        query = DicomQuery.objects.get()
        rst1 = query.dicomqrrspstudy_set.all()[0]

        # Add in a fourth series with modality SR
        rst1s4 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=rst1)
        rst1s4.query_id = query.query_id
        rst1s4.series_instance_uid = uuid.uuid4()
        rst1s4.modality = u"SR"
        rst1s4.series_number = 999
        rst1s4.series_description = u"radiation dose report"
        rst1s4.number_of_series_related_instances = 1
        rst1s4.save()

        # Delete the modalities in study data
        rst1.set_modalities_in_study(None)
        rst1.save()

        _generate_modalities_in_study(rst1, query.query_id)

        # reload study, else _generate_modalities_in_study appears to work without save. See #627
        rst2 = query.dicomqrrspstudy_set.all()[0]

        # Modalities in study should now be available again
        self.assertEqual(Counter(rst2.get_modalities_in_study()), Counter([u'CT', u'SC', u'SR']))


class ResponseFiltering(TestCase):
    """
    Test case for the study or series level filtering for desired or otherwise station names, study descriptions etc
    Function tested is qrscu._filter
    """
    def setUp(self):
        """
        """

        query = DicomQuery.objects.create()
        query.query_id = uuid.uuid4()
        query.save()

        rst1 = DicomQRRspStudy.objects.create(dicom_query=query)
        rst1.query_id = query.query_id
        rst1.study_instance_uid = uuid.uuid4()
        rst1.study_description = u"Imported  CT studies"
        rst1.station_name = u"badstation"
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
        rst1.set_modalities_in_study(
            list(
                set(
                    val for dic in rst1_series_rsp.values('modality') for val in dic.values()
                )
            ))
        rst1.save()

        rst2 = DicomQRRspStudy.objects.create(dicom_query=query)
        rst2.query_id = query.query_id
        rst2.study_instance_uid = uuid.uuid4()
        rst2.study_description = u"Test Response 2"
        rst2.station_name = u"goodstation"
        rst2.save()

        rst3 = DicomQRRspStudy.objects.create(dicom_query=query)
        rst3.query_id = query.query_id
        rst3.study_instance_uid = uuid.uuid4()
        rst3.study_description = u"test response 3"
        rst3.station_name = u"goodstation2"
        rst3.save()

    def test_filter_include_station_name(self):
        """
        Testing _filter with include station name of 'goodstation'. Expect two responses goodstation and goodstation2
        :return: None
        """
        from remapp.netdicom.qrscu import _filter

        query = DicomQuery.objects.get()
        _filter(query, u"study", u"station_name", [u"goodstation"], u"include")

        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 2)
        studies = query.dicomqrrspstudy_set.all()
        for study in studies:
            self.assertTrue(u"goodstation" in study.station_name)

    def test_filter_exclude_station_name(self):
        """
        Testing _filter with exclude station name of 'badstation'. Expect two responses goodstation and goodstation2
        :return: None
        """
        from remapp.netdicom.qrscu import _filter

        query = DicomQuery.objects.get()
        _filter(query, u"study", u"station_name", [u"badstation"], u"exclude")

        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 2)
        studies = query.dicomqrrspstudy_set.all()
        for study in studies:
            self.assertFalse(u"badstation" in study.station_name)

    def test_filter_exclude_study_description(self):
        """
        Testing _filter with exclude two study descriptions. Expect one response of goodstation
        :return: None
        """
        from remapp.netdicom.qrscu import _filter

        query = DicomQuery.objects.get()
        _filter(query, u"study", u"study_description", [u"import", u"test response 3"], u"exclude")

        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 1)
        study = query.dicomqrrspstudy_set.get()
        self.assertTrue(study.station_name == u"goodstation")

    def test_filter_include_study_description(self):
        """
        Testing _filter with include study description 'test'. Expect two responses of goodstation and goodstation2
        :return: None
        """
        from remapp.netdicom.qrscu import _filter

        query = DicomQuery.objects.get()
        _filter(query, u"study", u"study_description", [u"test", ], u"include")

        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 2)
        studies = query.dicomqrrspstudy_set.all()
        for study in studies:
            self.assertTrue(u"goodstation" in study.station_name)


def _fake_image_query(assoc, sr, query_id):
    return


class PruneSeriesResponses(TestCase):
    """
    Test case for the study or series level filtering for desired or otherwise station names, study descriptions etc
    Function tested is qrscu._filter
    """
    def setUp(self):
        """
        """

        self.all_mods = {'CT': {'inc': True, 'mods': ['CT']},
                    'MG': {'inc': True, 'mods': ['MG']},
                    'FL': {'inc': True, 'mods': ['RF', 'XA']},
                    'DX': {'inc': True, 'mods': ['DX', 'CR']}
                    }
        self.filters = {
            'stationname_inc': None,
            'stationname_exc': None,
            'study_desc_inc': None,
            'study_desc_exc': None,
        }

    def test_prune_ser_resp_mg_no_sr(self):
        """
        Test _prune_series_responses with mammo exam with no SR.
        :return: No change to response
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.create()
        query.query_id = "MammoNoSR"
        query.save()

        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = uuid.uuid4()
        st1.study_description = u"MG study no SR"
        st1.set_modalities_in_study(['MG'])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = uuid.uuid4()
        st1_se1.modality = u"MG"
        st1_se1.series_number = 1
        st1_se1.number_of_series_related_instances = 1
        st1_se1.save()

        query = DicomQuery.objects.get(query_id__exact="MammoNoSR")
        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 1)
        series = studies[0].dicomqrrspseries_set.all()
        self.assertEqual(series.count(), 1)

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_prune_ser_resp_mg_with_sr(self):
        """
        Test _prune_series_responses with mammo exam with two SRs, one RDSR and one Basic SR.
        :return: MG series and basic SR series should be deleted.
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.create()
        query.query_id = "MammoWithSR"
        query.save()

        st2 = DicomQRRspStudy.objects.create(dicom_query=query)
        st2.query_id = query.query_id
        st2.study_instance_uid = uuid.uuid4()
        st2.study_description = u"MG study with SR"
        st2.set_modalities_in_study(['MG', 'SR'])
        st2.save()

        st2_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st2)
        st2_se1.query_id = query.query_id
        st2_se1.series_instance_uid = uuid.uuid4()
        st2_se1.modality = u"MG"
        st2_se1.series_number = 1
        st2_se1.number_of_series_related_instances = 1
        st2_se1.save()

        st2_se2 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st2)
        st2_se2.query_id = query.query_id
        st2_se2.series_instance_uid = uuid.uuid4()
        st2_se2.modality = u"SR"
        st2_se2.series_number = 2
        st2_se2.number_of_series_related_instances = 1
        st2_se2.save()

        st2_se2_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st2_se2)
        st2_se2_im1.query_id = query.query_id
        st2_se2_im1.sop_instance_uid = uuid.uuid4()
        st2_se2_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.67'
        st2_se2_im1.save()

        st2_se3 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st2)
        st2_se3.query_id = query.query_id
        st2_se3.series_instance_uid = uuid.uuid4()
        st2_se3.modality = u"SR"
        st2_se3.series_number = 3
        st2_se3.number_of_series_related_instances = 1
        st2_se3.save()

        st2_se3_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st2_se3)
        st2_se3_im1.query_id = query.query_id
        st2_se3_im1.sop_instance_uid = uuid.uuid4()
        st2_se3_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.11'
        st2_se3_im1.save()

        query = DicomQuery.objects.get(query_id__exact="MammoWithSR")
        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 1)
        series = studies[0].dicomqrrspseries_set.all()
        self.assertEqual(series.count(), 1)
        sr_instance = series[0].dicomqrrspimage_set.get()
        self.assertEqual(sr_instance.sop_class_uid, u'1.2.840.10008.5.1.4.1.1.88.67')

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_prune_ser_resp_cr_no_rdsr(self):
        """
        Test _prune_series_responses with CR exam with no RDSR but with Basic SR.
        :return: Basic SR deleted, study.modality set to "DX"
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.create()
        query.query_id = "CRNoRDSR"
        query.save()

        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = uuid.uuid4()
        st1.study_description = u"CR study no SR"
        st1.set_modalities_in_study(['CR', 'SR'])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = uuid.uuid4()
        st1_se1.modality = u"CR"
        st1_se1.series_number = 1
        st1_se1.number_of_series_related_instances = 1
        st1_se1.save()

        st1_se2 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se2.query_id = query.query_id
        st1_se2.series_instance_uid = uuid.uuid4()
        st1_se2.modality = u"SR"
        st1_se2.series_number = 2
        st1_se2.number_of_series_related_instances = 1
        st1_se2.save()

        st1_se2_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se2)
        st1_se2_im1.query_id = query.query_id
        st1_se2_im1.sop_instance_uid = uuid.uuid4()
        st1_se2_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.11'
        st1_se2_im1.save()

        query = DicomQuery.objects.get(query_id__exact="CRNoRDSR")
        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 1)
        series = studies[0].dicomqrrspseries_set.all()
        self.assertEqual(series.count(), 1)
        self.assertEqual(series[0].modality, u"CR")
        self.assertEqual(studies[0].modality, u"DX")

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_prune_ser_resp_dx_with_sr(self):
        """
        Test _prune_series_responses with DX exam with three SRs, one RDSR, one ESR and one Basic SR.
        :return: DX series, ESR and basic SR series should be deleted.
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.create()
        query.query_id = "DXWithSR"
        query.save()

        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = uuid.uuid4()
        st1.study_description = u"DX study with RDSR"
        st1.set_modalities_in_study(['DX', 'SR'])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = uuid.uuid4()
        st1_se1.modality = u"DX"
        st1_se1.series_number = 1
        st1_se1.number_of_series_related_instances = 1
        st1_se1.save()

        st1_se2 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se2.query_id = query.query_id
        st1_se2.series_instance_uid = uuid.uuid4()
        st1_se2.modality = u"SR"
        st1_se2.series_number = 2
        st1_se2.number_of_series_related_instances = 1
        st1_se2.save()

        st1_se2_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se2)
        st1_se2_im1.query_id = query.query_id
        st1_se2_im1.sop_instance_uid = uuid.uuid4()
        st1_se2_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.67'
        st1_se2_im1.save()

        st1_se3 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se3.query_id = query.query_id
        st1_se3.series_instance_uid = uuid.uuid4()
        st1_se3.modality = u"SR"
        st1_se3.series_number = 3
        st1_se3.number_of_series_related_instances = 1
        st1_se3.save()

        st1_se3_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se3)
        st1_se3_im1.query_id = query.query_id
        st1_se3_im1.sop_instance_uid = uuid.uuid4()
        st1_se3_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.11'
        st1_se3_im1.save()

        st1_se4 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se4.query_id = query.query_id
        st1_se4.series_instance_uid = uuid.uuid4()
        st1_se4.modality = u"SR"
        st1_se4.series_number = 4
        st1_se4.number_of_series_related_instances = 1
        st1_se4.save()

        st1_se4_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se4)
        st1_se4_im1.query_id = query.query_id
        st1_se4_im1.sop_instance_uid = uuid.uuid4()
        st1_se4_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.22'
        st1_se4_im1.save()

        query = DicomQuery.objects.get(query_id__exact="DXWithSR")
        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 1)
        series = studies[0].dicomqrrspseries_set.all()
        self.assertEqual(series.count(), 1)
        sr_instance = series[0].dicomqrrspimage_set.get()
        self.assertEqual(sr_instance.sop_class_uid, u'1.2.840.10008.5.1.4.1.1.88.67')

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_prune_ser_resp_rf_no_sr(self):
        """
        Test _prune_series_responses with fluoro exam with no ESR or RDSR.
        :return: Whole study response deleted
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.create()
        query.query_id = "RFNoSR"
        query.save()

        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = uuid.uuid4()
        st1.study_description = u"RF study no SR"
        st1.set_modalities_in_study(['RF', 'SR'])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = uuid.uuid4()
        st1_se1.modality = u"RF"
        st1_se1.series_number = 1
        st1_se1.number_of_series_related_instances = 1
        st1_se1.save()

        st1_se2 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se2.query_id = query.query_id
        st1_se2.series_instance_uid = uuid.uuid4()
        st1_se2.modality = u"SR"
        st1_se2.series_number = 2
        st1_se2.number_of_series_related_instances = 1
        st1_se2.save()

        st1_se2_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se2)
        st1_se2_im1.query_id = query.query_id
        st1_se2_im1.sop_instance_uid = uuid.uuid4()
        st1_se2_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.11'
        st1_se2_im1.save()

        query = DicomQuery.objects.get(query_id__exact="RFNoSR")
        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 0)

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_prune_ser_resp_xa_with_esr(self):
        """
        Test _prune_series_responses with XA exam with an ESR, and one Basic SR.
        :return: XA series and basic SR series should be deleted.
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.create()
        query.query_id = "XAWithESRBSR"
        query.save()

        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = uuid.uuid4()
        st1.study_description = u"XA study with ESR and Basic SR"
        st1.set_modalities_in_study(['XA', 'SR'])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = uuid.uuid4()
        st1_se1.modality = u"XA"
        st1_se1.series_number = 1
        st1_se1.number_of_series_related_instances = 1
        st1_se1.save()

        st1_se2 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se2.query_id = query.query_id
        st1_se2.series_instance_uid = uuid.uuid4()
        st1_se2.modality = u"SR"
        st1_se2.series_number = 2
        st1_se2.number_of_series_related_instances = 1
        st1_se2.save()

        st1_se2_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se2)
        st1_se2_im1.query_id = query.query_id
        st1_se2_im1.sop_instance_uid = uuid.uuid4()
        st1_se2_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.22'
        st1_se2_im1.save()

        st1_se3 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se3.query_id = query.query_id
        st1_se3.series_instance_uid = uuid.uuid4()
        st1_se3.modality = u"SR"
        st1_se3.series_number = 3
        st1_se3.number_of_series_related_instances = 1
        st1_se3.save()

        st1_se3_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se3)
        st1_se3_im1.query_id = query.query_id
        st1_se3_im1.sop_instance_uid = uuid.uuid4()
        st1_se3_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.11'
        st1_se3_im1.save()

        query = DicomQuery.objects.get(query_id__exact="XAWithESRBSR")
        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 1)
        series = studies[0].dicomqrrspseries_set.all()
        self.assertEqual(series.count(), 1)
        sr_instance = series[0].dicomqrrspimage_set.get()
        self.assertEqual(sr_instance.sop_class_uid, u'1.2.840.10008.5.1.4.1.1.88.22')


class PruneSeriesResponsesCT(TestCase):
    """
    Test case for the study or series level filtering for desired or otherwise station names, study descriptions etc
    Function tested is qrscu._filter
    """
    def setUp(self):
        """
        """

        self.all_mods = {'CT': {'inc': True, 'mods': ['CT']},
                         'MG': {'inc': True, 'mods': ['MG']},
                         'FL': {'inc': True, 'mods': ['RF', 'XA']},
                         'DX': {'inc': True, 'mods': ['DX', 'CR']}
                         }
        self.filters = {
            'stationname_inc': None,
            'stationname_exc': None,
            'study_desc_inc': None,
            'study_desc_exc': None,
        }

        query = DicomQuery.objects.create()
        query.query_id = "CT"
        query.save()

        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = uuid.uuid4()
        st1.study_description = u"CT study"
        st1.set_modalities_in_study(['CT', 'SR'])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = uuid.uuid4()
        st1_se1.modality = u"CT"
        st1_se1.series_number = 1
        st1_se1.number_of_series_related_instances = 15
        st1_se1.series_description = u"TAP"
        st1_se1.save()

        st1_se2 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se2.query_id = query.query_id
        st1_se2.series_instance_uid = uuid.uuid4()
        st1_se2.modality = u"SR"
        st1_se2.series_number = 2
        st1_se2.number_of_series_related_instances = 1
        st1_se2.save()

        st1_se2_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se2)
        st1_se2_im1.query_id = query.query_id
        st1_se2_im1.sop_instance_uid = uuid.uuid4()
        st1_se2_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.22'
        st1_se2_im1.save()

        st1_se3 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se3.query_id = query.query_id
        st1_se3.series_instance_uid = uuid.uuid4()
        st1_se3.modality = u"SR"
        st1_se3.series_number = 3
        st1_se3.number_of_series_related_instances = 1
        st1_se3.save()

        st1_se3_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se3)
        st1_se3_im1.query_id = query.query_id
        st1_se3_im1.sop_instance_uid = uuid.uuid4()
        st1_se3_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.11'
        st1_se3_im1.save()

        st1_se4 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se4.query_id = query.query_id
        st1_se4.series_instance_uid = uuid.uuid4()
        st1_se4.modality = u"CT"
        st1_se4.series_number = 4
        st1_se4.number_of_series_related_instances = 1
        st1_se4.series_description = u"Dose Info"
        st1_se4.save()

        st1_se5 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se5.query_id = query.query_id
        st1_se5.series_instance_uid = uuid.uuid4()
        st1_se5.modality = u"SR"
        st1_se5.series_number = 5
        st1_se5.number_of_series_related_instances = 1
        st1_se5.save()

        st1_se5_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se5)
        st1_se5_im1.query_id = query.query_id
        st1_se5_im1.sop_instance_uid = uuid.uuid4()
        st1_se5_im1.sop_class_uid = u'1.2.840.10008.5.1.4.1.1.88.67'
        st1_se5_im1.save()

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_prune_ser_resp_ct_with_rdsr(self):
        """
        Test _prune_series_responses with CT exam with a RDSR, ESR, Basic SR, Dose info and an axial series.
        :return: RDSR series.
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.get(query_id__exact="CT")
        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 1)
        series = studies[0].dicomqrrspseries_set.all()
        self.assertEqual(series.count(), 1)
        sr_instance = series[0].dicomqrrspimage_set.get()
        self.assertEqual(sr_instance.sop_class_uid, u'1.2.840.10008.5.1.4.1.1.88.67')

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_prune_ser_resp_ct_with_esr(self):
        """
        Test _prune_series_responses with CT exam with a ESR, Basic SR, Dose info and an axial series.
        :return: ESR series.
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.get(query_id__exact="CT")

        study = query.dicomqrrspstudy_set.get()
        rdsr_series = study.dicomqrrspseries_set.filter(series_number__exact=5)
        rdsr_series.delete()

        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 1)
        series = studies[0].dicomqrrspseries_set.all()
        self.assertEqual(series.count(), 1)
        sr_instance = series[0].dicomqrrspimage_set.get()
        self.assertEqual(sr_instance.sop_class_uid, u'1.2.840.10008.5.1.4.1.1.88.22')

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_prune_ser_resp_ct_with_dose_info(self):
        """
        Test _prune_series_responses with CT exam with a Basic SR, Dose info and an axial series.
        :return: Dose info series.
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.get(query_id__exact="CT")

        study = query.dicomqrrspstudy_set.get()
        rdsr_series = study.dicomqrrspseries_set.filter(series_number__exact=5)
        rdsr_series.delete()
        esr_series = study.dicomqrrspseries_set.filter(series_number__exact=2)
        esr_series.delete()

        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 1)
        series = studies[0].dicomqrrspseries_set.all()
        self.assertEqual(series.count(), 1)
        self.assertEqual(series[0].series_number, 4)

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_prune_ser_resp_ct_with_dose_info_no_desc(self):
        """
        Test _prune_series_responses with CT exam with a Basic SR, Dose info and an axial series, but no series desc.
        :return: Dose info series.
        """
        from remapp.netdicom.qrscu import _prune_series_responses

        query = DicomQuery.objects.get(query_id__exact="CT")

        study = query.dicomqrrspstudy_set.get()
        rdsr_series = study.dicomqrrspseries_set.filter(series_number__exact=5)
        rdsr_series.delete()
        esr_series = study.dicomqrrspseries_set.filter(series_number__exact=2)
        esr_series.delete()
        dose_info_series = study.dicomqrrspseries_set.filter(series_number__exact=4)
        dose_info_series[0].series_description = ""

        all_mods = self.all_mods
        filters = self.filters
        assoc = None
        _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images=False)
        studies = query.dicomqrrspstudy_set.all()
        self.assertEqual(studies.count(), 1)
        series = studies[0].dicomqrrspseries_set.all()
        self.assertEqual(series.count(), 1)
        self.assertEqual(series[0].series_number, 4)


def _fake_qrscu(qr_scp_pk=None, store_scp_pk=None,
        implicit=False, explicit=False, move=False, query_id=None,
        date_from=None, date_until=None, modalities=None, inc_sr=False, remove_duplicates=True, filters=None):
    """
    Check that the parsing has worked
    """
    pass


def _fake_echo_success(scp_pk=None, store_scp=False, qr_scp=False):
    """
    Fake success return for echoscu
    :param scp_pk:
    :param store_scp:
    :param qr_scp:
    :return: str "Success"
    """
    return "Success"


class QRSCUScriptArgParsing(TestCase):
    """
    Test the args passed on the command line are parsed properly
    """

    @patch("remapp.netdicom.tools.echoscu", _fake_echo_success)
    def test_ct_mg(self):
        """
        Test the arg parser with modalities CT and MG
        :return:
        """

        from remapp.netdicom.qrscu import _create_parser, _process_args

        parser = _create_parser()
        parsed_args = _process_args(parser.parse_args(['1', '2', '-ct', '-mg']), parser)

        self.assertEqual(parsed_args['qr_id'], 1)
        self.assertEqual(parsed_args['store_id'], 2)
        self.assertEqual(parsed_args['modalities'].sort(), ['MG', 'CT'].sort())
        filters = {'study_desc_exc': None, 'stationname_exc': None, 'study_desc_inc': None, 'stationname_inc': None}
        self.assertEqual(parsed_args['filters'], filters)

    @patch("remapp.netdicom.tools.echoscu", _fake_echo_success)
    def test_ct_std_exc(self):
        """
        Test the arg parser with modalities CT and MG
        :return:
        """

        from remapp.netdicom.qrscu import _create_parser, _process_args

        parser = _create_parser()
        parsed_args = _process_args(parser.parse_args(['1', '2', '-ct', '-e Thorax, Neck ']), parser)

        self.assertEqual(parsed_args['qr_id'], 1)
        self.assertEqual(parsed_args['store_id'], 2)
        self.assertEqual(parsed_args['modalities'].sort(), ['MG', 'CT'].sort())
        filters = {'study_desc_exc': [u'thorax', u'neck'],
                   'study_desc_inc': None,
                   'stationname_exc': None,
                   'stationname_inc': None}
        self.assertEqual(parsed_args['filters'], filters)

    @patch("remapp.netdicom.tools.echoscu", _fake_echo_success)
    def test_ct_std_exc_stn_inc(self):
        """
        Test the arg parser with modalities CT and MG
        :return:
        """

        from remapp.netdicom.qrscu import _create_parser, _process_args

        parser = _create_parser()
        parsed_args = _process_args(parser.parse_args(
            ['1', '2', '-ct', '--desc_exclude', 'Thorax, Neck ', '-sni', 'MyStn']),
            parser)

        self.assertEqual(parsed_args['qr_id'], 1)
        self.assertEqual(parsed_args['store_id'], 2)
        self.assertEqual(parsed_args['modalities'].sort(), ['MG', 'CT'].sort())
        filters = {'study_desc_exc': [u'thorax', u'neck'],
                   'study_desc_inc': None,
                   'stationname_exc': None,
                   'stationname_inc': [u'mystn']}
        self.assertEqual(parsed_args['filters'], filters)

class RemoveDuplicates(TestCase):
    """
    Test the routine to remove any responses that correspond to information already in the database
    """

    def test_rdsr_new(self):
        """Inital test that _remove_duplicates doesn't remove new RDSR

        """

        from remapp.netdicom.qrscu import _remove_duplicates

        PatientIDSettings.objects.create()

        # Nothing imported into the database

        query = DicomQuery.objects.create()
        query.query_id = "CT"
        query.save()

        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = "1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.3.0"
        st1.study_description = u"CT study"
        st1.set_modalities_in_study(['CT', 'SR'])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = "1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.12.0"
        st1_se1.modality = u"SR"
        st1_se1.series_number = 502
        st1_se1.number_of_series_related_instances = 1
        st1_se1.save()

        st1_se1_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se1)
        st1_se1_im1.query_id = query.query_id
        st1_se1_im1.sop_instance_uid = u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.11.0'
        st1_se1_im1.save()

        study_responses_pre = DicomQRRspStudy.objects.all()
        self.assertEqual(study_responses_pre.count(), 1)
        self.assertEqual(study_responses_pre[0].dicomqrrspseries_set.count(), 1)

        study_rsp = query.dicomqrrspstudy_set.all()
        assoc = None
        query_id = None
        _remove_duplicates(query, study_rsp, assoc, query_id)

        study_responses_post = DicomQRRspStudy.objects.all()
        self.assertEqual(study_responses_post.count(), 1)
        self.assertEqual(study_responses_post[0].dicomqrrspseries_set.count(), 1)


    def test_rdsr_same(self):
        """Now testing _remove_duplicates will remove an identical RDSR, but retain a new one.
        """

        from remapp.netdicom.qrscu import _remove_duplicates

        PatientIDSettings.objects.create()

        dicom_file_1 = "test_files/CT-RDSR-Siemens-Multi-1.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path_1 = os.path.join(root_tests, dicom_file_1)
        rdsr(dicom_path_1)

        query = DicomQuery.objects.create()
        query.query_id = "CT"
        query.save()

        # Same RDSR - expect study response to be deleted (post count = 0)
        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = "1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.3.0"
        st1.study_description = u"CT study"
        st1.set_modalities_in_study(['CT', 'SR'])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = "1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.12.0"
        st1_se1.modality = u"SR"
        st1_se1.series_number = 501
        st1_se1.number_of_series_related_instances = 1
        st1_se1.save()

        st1_se1_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se1)
        st1_se1_im1.query_id = query.query_id
        st1_se1_im1.sop_instance_uid = u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.11.0'
        st1_se1_im1.save()

        st1_se2 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se2.query_id = query.query_id
        st1_se2.series_instance_uid = "1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.7.0"
        st1_se2.modality = u"SR"
        st1_se2.series_number = 501
        st1_se2.number_of_series_related_instances = 1
        st1_se2.save()

        st1_se2_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se2)
        st1_se2_im1.query_id = query.query_id
        st1_se2_im1.sop_instance_uid = u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.6.0'
        st1_se2_im1.save()

        study_responses_pre = DicomQRRspStudy.objects.all()
        self.assertEqual(study_responses_pre.count(), 1)
        self.assertEqual(study_responses_pre[0].dicomqrrspseries_set.count(), 2)

        study_rsp = query.dicomqrrspstudy_set.all()
        assoc = None
        query_id = None
        _remove_duplicates(query, study_rsp, assoc, query_id)

        study_responses_post = DicomQRRspStudy.objects.all()
        self.assertEqual(study_responses_post.count(), 1)
        self.assertEqual(study_responses_post[0].dicomqrrspseries_set.count(), 1)
        self.assertEqual(study_responses_post[0].dicomqrrspseries_set.all()[0].series_instance_uid,
                         u"1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.7.0")

    def test_rdsr_no_objectuids(self):
        """
        Test importing RDSR where
        * same study, ObjectUIDsProcessed not populated
        :return:
        """

        from remapp.netdicom.qrscu import _remove_duplicates

        PatientIDSettings.objects.create()

        dicom_file_1 = "test_files/CT-RDSR-Siemens-Multi-2.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path_1 = os.path.join(root_tests, dicom_file_1)
        rdsr(dicom_path_1)
        imported_study = GeneralStudyModuleAttr.objects.order_by('pk')[0]
        imported_study.objectuidsprocessed_set.all().delete()
        imported_study.save()

        query = DicomQuery.objects.create()
        query.query_id = "CT"
        query.save()

        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = "1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.3.0"
        st1.study_description = u"CT study"
        st1.set_modalities_in_study(['CT', 'SR'])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = "1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.7.0"
        st1_se1.modality = u"SR"
        st1_se1.series_number = 501
        st1_se1.number_of_series_related_instances = 1
        st1_se1.save()

        st1_se1_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se1)
        st1_se1_im1.query_id = query.query_id
        st1_se1_im1.sop_instance_uid = u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.6.0'
        st1_se1_im1.save()

        study_responses_pre = DicomQRRspStudy.objects.all()
        self.assertEqual(study_responses_pre.count(), 1)
        self.assertEqual(study_responses_pre[0].dicomqrrspseries_set.count(), 1)

        study_rsp = query.dicomqrrspstudy_set.all()
        assoc = None
        query_id = None
        _remove_duplicates(query, study_rsp, assoc, query_id)

        study_responses_post = DicomQRRspStudy.objects.all()
        self.assertEqual(study_responses_post.count(), 1)
        self.assertEqual(study_responses_post[0].dicomqrrspseries_set.count(), 1)

    @patch("remapp.netdicom.qrscu._query_images", _fake_image_query)
    def test_dx(self):
        """
        Test remove duplicates with DX images
        :return:
        """

        from remapp.extractors import dx
        from remapp.netdicom.qrscu import _remove_duplicates

        PatientIDSettings.objects.create()

        dx_ge_xr220_1 = os.path.join("test_files", "DX-Im-GE_XR220-1.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dx(os.path.join(root_tests, dx_ge_xr220_1))

        query = DicomQuery.objects.create()
        query.query_id = "DX"
        query.save()

        st1 = DicomQRRspStudy.objects.create(dicom_query=query)
        st1.query_id = query.query_id
        st1.study_instance_uid = "1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.24.0"
        st1.study_description = u"DX study"
        st1.set_modalities_in_study(['DX', ])
        st1.save()

        st1_se1 = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=st1)
        st1_se1.query_id = query.query_id
        st1_se1.series_instance_uid = "1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.25.0"
        st1_se1.modality = u"DX"
        st1_se1.series_number = 1
        st1_se1.number_of_series_related_instances = 1
        st1_se1.save()

        # Image responses won't be there yet, but image level query is faked
        st1_se5_im1 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se1)
        st1_se5_im1.query_id = query.query_id
        st1_se5_im1.sop_instance_uid = "1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.20.0"
        st1_se5_im1.save()

        st1_se5_im2 = DicomQRRspImage.objects.create(dicom_qr_rsp_series=st1_se1)
        st1_se5_im2.query_id = query.query_id
        st1_se5_im2.sop_instance_uid = "1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.26.0"
        st1_se5_im2.save()

        study_responses_pre = DicomQRRspStudy.objects.all()
        self.assertEqual(study_responses_pre.count(), 1)
        self.assertEqual(study_responses_pre[0].dicomqrrspseries_set.count(), 1)
        self.assertEqual(study_responses_pre[0].dicomqrrspseries_set.get().dicomqrrspimage_set.count(), 2)

        study_rsp = query.dicomqrrspstudy_set.all()
        assoc = None
        query_id = None
        _remove_duplicates(query, study_rsp, assoc, query_id)

        # One image response should have been deleted, one remain
        study_responses_post = DicomQRRspStudy.objects.all()
        self.assertEqual(study_responses_post.count(), 1)
        self.assertEqual(study_responses_post[0].dicomqrrspseries_set.count(), 1)
        self.assertEqual(study_responses_pre[0].dicomqrrspseries_set.get().dicomqrrspimage_set.count(), 1)
        remaining_image_rsp = study_responses_pre[0].dicomqrrspseries_set.get().dicomqrrspimage_set.get()
        self.assertEqual(
            remaining_image_rsp.sop_instance_uid, "1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.26.0")


class InvalidMove(TestCase):
    """Small test class to check passing an invalid query ID to movescu fails gracefully

    """

    def test_invalid_query_id(self):
        """Pass invalid query_id to movescu, expect log update and return False/0

        """
        from remapp.netdicom.qrscu import movescu

        PatientIDSettings.objects.create()

        with LogCapture('remapp.netdicom.qrscu') as log:
            movestatus = movescu('not_a_query_ID')
            self.assertEqual(movestatus, False)

            log.check_present(('remapp.netdicom.qrscu', 'WARNING',
                               u"Move called with invalid query_id not_a_query_ID. Move abandoned."))



