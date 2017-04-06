# This Python file uses the following encoding: utf-8
# test_dicom_qr.py

import os
from dicom.dataset import Dataset, FileDataset
from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
from django.test import TestCase
from mock import patch
from netdicom.applicationentity import AE
from netdicom.SOPclass import StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass
from testfixtures import LogCapture
import uuid
from remapp.netdicom import qrscu
from remapp.models import DicomQuery, DicomQRRspStudy, DicomQRRspSeries, DicomRemoteQR, DicomStoreSCP


def _fake_check_sr_type_in_study_with_rdsr(MyAE, RemoteAE, study):
    return 'RDSR'


#############################
# Beginnings of test of whole function - will not proceed with this further at this stage. Will test components instead.
#############################
#
# def _fake_ae_association_success(my_ae, remote_ae):
#     from netdicom.applicationentity import Association
#     assoc = Association(my_ae, RemoteAE=remote_ae, )
#     assoc.AssociationEstablished = True
#     return assoc
#
#
# def _fake_echo(assoc):
#     pass
#
#
# class QRWholeFunction(TestCase):
#
#     @patch("remapp.netdicom.qrscu._echo", _fake_echo)
#     @patch("remapp.netdicom.qrscu._create_association", _fake_ae_association_success)
#     def test_faking(self):
#         qr_scp = DicomRemoteQR.objects.create()
#         qr_scp.hostname = "qrserver"
#         qr_scp.port = 104
#         qr_scp.aetitle = "qrserver"
#         qr_scp.save()
#         store_scp = DicomStoreSCP.objects.create()
#         store_scp.aetitle = "openremstore"
#         store_scp.port = 104
#         store_scp.save()
#
#         qrscu.qrscu(qr_scp_pk=1, store_scp_pk=1, modalities=["CT",])
#
#############################

fake_responses = [
    [[u'CT'], [u'OT', u'CT', u'SR'], [u'SR', u'CT']],
    [[u'MG', u'SR'], [u'MG'], [u'OT', u'MG'], [u'PR', u'MG']]
    ]


def _fake_two_modalities(my_ae, remote_ae, d, query, query_id, *args, **kwargs):
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
        print("mod_list is {0}".format(mod_list))


def _fake_all_modalities(my_ae, remote_ae, d, query, query_id, *args, **kwargs):
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
        modality_matching = _query_for_each_modality(all_mods, query, d, my_ae, remote_ae)

        self.assertEqual(DicomQRRspStudy.objects.count(), 2)
        self.assertEqual(study_query_mock.call_count, 1)
        self.assertEqual(modality_matching, False)

    @patch("remapp.netdicom.qrscu._query_study", side_effect=_fake_two_modalities)
    def test_modality_matching(self, study_query_mock):
        """
        Tests the study level query for each modality. Fake responses only include appropriate modalities, so
        _query_for_each_modality should return modality_matching as True
        :param study_query_mock: Mocked study level response routine
        :return:  Nothing
        """
        from remapp.netdicom.qrscu import _query_for_each_modality

        all_mods = {'CT': {'inc': True, 'mods': ['CT']},
                    'MG': {'inc': True, 'mods': ['MG']},
                    'FL': {'inc': False, 'mods': ['RF', 'XA']},
                    'DX': {'inc': False, 'mods': ['DX', 'CR']}
                    }
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
        modality_matching = _query_for_each_modality(all_mods, query, d, my_ae, remote_ae)

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

        qrscu._prune_series_responses("MyAE", "RemoteAE", query, all_mods, filters)

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

        qrscu._prune_series_responses("MyAE", "RemoteAE", query, all_mods, filters)

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
        rst1_series_rsp = rst1.dicomqrrspseries_set.all()
        rst1s3 = rst1_series_rsp[2]

        # Remove the third series with the 'dose info' description
        rst1s3.delete()

        # Before the pruning, two series
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 2)

        qrscu._prune_series_responses("MyAE", "RemoteAE", query, all_mods, filters)

        # After pruning, there should be no studies left
        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 0)

    @patch("remapp.netdicom.qrscu.check_sr_type_in_study", _fake_check_sr_type_in_study_with_rdsr)
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
        rst1.set_modalities_in_study(list(set(val for dic in rst1_series_rsp.values('modality') for val in dic.values())))
        rst1.save()

        # Now starting with four series
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 4)

        qrscu._prune_series_responses("MyAE", "RemoteAE", query, all_mods, filters)

        # Should now have one SR series left, identified by the series description for the purposes of this test
        self.assertEqual(query.dicomqrrspstudy_set.all().count(), 1)
        self.assertEqual(rst1.dicomqrrspseries_set.all().count(), 1)
        self.assertEqual(rst1.dicomqrrspseries_set.all()[0].series_description, u"radiation dose report")