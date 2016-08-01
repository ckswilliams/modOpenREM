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
..  module:: get_values.
    :synopsis: Module to return values from DICOM elements using pydicom.

..  moduleauthor:: Ed McDonagh

"""
from dicom.valuerep import PersonName
import logging
logger = logging.getLogger(__name__)


def get_value_kw(tag,dataset):
    """Get DICOM value by keyword reference.

    :param keyword:     DICOM keyword, no spaces or plural as per dictionary.
    :type keyword:      str.
    :param dataset:     The DICOM dataset containing the tag.
    :type dataset:      dataset
    :returns:           str. -- value
    """
    if (tag in dataset):
        val = getattr(dataset,tag)
        if val != '':
            if type(val) is str or type(val) is PersonName:
                val = val.decode('latin-1', 'replace')
            return val

def get_value_num(tag,dataset):
    """Get DICOM value by tag group and element number.
    
    Always use get_value_kw by preference for readability. This module can
    be required when reading private elements.

    :param tag:     DICOM group and element number as a single hexadecimal number (prefix 0x).
    :type tag:          hex
    :param dataset:     The DICOM dataset containing the tag.
    :type dataset:      dataset
    :returns:           str. -- value
    """
    if (tag in dataset):
        val = dataset[tag].value
        if val != '':
            if type(val) is str or type(val) is PersonName:
                val = val.decode('latin-1', 'replace')
            return val

def get_seq_code_value(sequence,dataset):
    """From a DICOM sequence, get the code value.

    :param sequence:    DICOM sequence name.
    :type sequence:     DICOM keyword, no spaces or plural as per dictionary.
    :param dataset:     The DICOM dataset containing the sequence.
    :type dataset:      DICOM dataset
    :returns:           int. -- code value
    """
    if (sequence in dataset):
        seq = getattr(dataset,sequence)
        if seq and hasattr(seq[0],'CodeValue'):
            return seq[0].CodeValue


def get_seq_code_meaning(sequence,dataset):
    """From a DICOM sequence, get the code meaning.

    :param sequence:    DICOM sequence name.
    :type sequence:     DICOM keyword, no spaces or plural as per dictionary.
    :param dataset:     The DICOM dataset containing the sequence.
    :type dataset:      DICOM dataset
    :returns:           str. -- code meaning
    """
    if (sequence in dataset):
        seq = getattr(dataset,sequence)
        if seq and hasattr(seq[0],'CodeMeaning'):
            meaning = seq[0].CodeMeaning
            if meaning != '':
                if type(meaning) is str or type(meaning) is PersonName:
                    meaning = meaning.decode('latin-1', 'replace')
            return meaning

def get_or_create_cid(codevalue, codemeaning):
    """Create a code_value code_meaning pair entry in the ContextID
    table if it doesn't already exist. 

    :param codevalue:   Code value as defined in the DICOM standard part 16
    :type codevalue:    int.
    :param codemeaning: Code meaning as defined in the DICOM standard part 16
    :type codevalue:    int.
    :returns:           ContextID entry for code value passed
    """
    from remapp.models import ContextID
    if codevalue:
        if not ContextID.objects.all().filter(code_value=codevalue).exists():
            cid = ContextID(
                code_value = codevalue,
                code_meaning = codemeaning,
                )
            cid.save()
        code = ContextID.objects.filter(code_value__exact = codevalue)
        if code.count() > 1:
            logger.warning("Duplicate entry in the ContextID table: %s/%s, import continuing",
                            codevalue, codemeaning)
        return code[0]

def return_for_export(model, field):
    """
    Prevent errors due to missing data in models
    :param val: database field
    :return: value or None
    """
    import datetime
    from django.core.exceptions import ObjectDoesNotExist
    try:
        val = getattr(model, field)
        if val:
            if isinstance(val, datetime.date):
                return val
            val = unicode(val)
        return val
    except ObjectDoesNotExist:
        return None


def safe_strings(str):
    try:
        return str.decode('latin-1', 'replace')
    except AttributeError:
        return None


def replace_comma(comma_string):
    if comma_string:
        no_comma_string = comma_string.replace(","," ").replace(";"," ")
        return no_comma_string
    return comma_string


def export_safe(ascii_string):
    if ascii_string:
        utf8_string = ascii_string.encode("utf-8")
        safe_string = replace_comma(utf8_string)
        return safe_string
