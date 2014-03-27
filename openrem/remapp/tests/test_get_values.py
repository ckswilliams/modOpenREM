# test_get_values.py

from django.test import TestCase
from dicom.sequence import Sequence
from dicom.dataset import Dataset

class GetValuesTests(TestCase):
    def test_get_code_value_value_exists(self):
        from remapp.tools.get_values import get_seq_code_value
        inputs = {'CodeValue': '1234',
                  'CodeMeaning': 'A code meaning'}
        hasValuesSeq = Dataset()
        hasValuesSeq.update(inputs)
        ds = Dataset()
        ds.ViewCodeSequence = Sequence([hasValuesSeq])
        val = get_seq_code_value('ViewCodeSequence',ds)
        
        self.assertEqual(val, '1234')

    def test_get_code_value_attr_not_present(self):
        from remapp.tools.get_values import get_seq_code_value
        inputs = {'CodeVal': '1234',
                  'CodeMeaning': 'A code meaning'}
        hasValuesSeq = Dataset()
        hasValuesSeq.update(inputs)
        ds = Dataset()
        ds.ViewCodeSequence = Sequence([hasValuesSeq])
        val = get_seq_code_value('ViewCodeSequence',ds)
        
        self.assertEqual(val, None)
