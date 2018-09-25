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
..  module:: hash_id.
    :synopsis: Creates a hash of an ID field

..  moduleauthor:: Ed McDonagh

"""


def hash_id(id_string, *args, **kwargs):
    """Return a one-way hash of the provided ID value

    :param id_string:         ID to create hash from
    :type id_string:          str
    :returns:          str
    """
    import dicom
    from django.utils.encoding import smart_bytes
    import hashlib

    if id_string:
        # print("hash_id id_string before is of type {0}".format(type(id_string)))
        if isinstance(id_string, (dicom.multival.MultiValue, list, dicom.valuerep.PersonNameUnicode)):
            id_string = ''.join(id_string)
        id_string = smart_bytes(id_string, encoding='utf-8')
        return hashlib.sha256(id_string).hexdigest()
