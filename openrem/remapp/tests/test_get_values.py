# This Python file uses the following encoding: utf-8
# test_get_values.py

from __future__ import unicode_literals
from django.test import TestCase
from dicom.sequence import Sequence
from dicom.dataset import Dataset
from remapp.tools.get_values import get_seq_code_value, get_seq_code_meaning, get_value_kw


class GetCodeValueTests(TestCase):
    def test_get_code_value_value_exists(self):
        """
        get_seq_code_value should return the CodeValue when it is present
        """
        dummy_seq = Dataset()
        ds = Dataset()
        dummy_seq.CodeValue = '1234'
        ds.ViewCodeSequence = Sequence([dummy_seq])
        val = get_seq_code_value('ViewCodeSequence', ds)
        
        self.assertEqual(val, '1234')

    def test_get_code_value_attr_not_present(self):
        """
        get_seq_code_value should not return and not error when CodeValue is not present
        """
        dummy_seq = Dataset()
        ds = Dataset()
        ds.ViewCodeSequence = Sequence([dummy_seq])
        val = get_seq_code_value('ViewCodeSequence', ds)
        
        self.assertEqual(val, None)


class GetCodeMeaningTests(TestCase):
    def test_get_code_meaning_meaning_exists(self):
        """
        get_seq_code_meaning should return the CodeMeaning when it is present
        """
        dummy_seq = Dataset()
        ds = Dataset()
        dummy_seq.CodeMeaning = 'A code meaning'
        ds.ViewCodeSequence = Sequence([dummy_seq])
        val = get_seq_code_meaning('ViewCodeSequence', ds)
        
        self.assertEqual(val, 'A code meaning')

    def test_get_code_value_attr_not_present(self):
        """
        get_seq_code_value should not return and not error when CodeMeaning is not present
        """
        dummy_seq = Dataset()
        ds = Dataset()
        ds.ViewCodeSequence = Sequence([dummy_seq])
        val = get_seq_code_meaning('ViewCodeSequence', ds)
        
        self.assertEqual(val, None)


class GetValueKWTests(TestCase):
    def test_non_ascii(self):
        """
        get_value_kw should return appropriate unicode string
        """
        ds = Dataset()
        ds.ProtocolName = 'mamografíaマンモグラフィー'
        val = get_value_kw('ProtocolName', ds)
        self.assertEqual(val, 'mamografíaマンモグラフィー')