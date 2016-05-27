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


def hash_id(id, *args, **kwargs):
    """Return a one-way hash of the provided ID value

    :param id:         ID to create hash from
    :type id:          str
    :returns:          str
    """
    import dicom
    import hashlib

    if id:
        if isinstance(id, dicom.multival.MultiValue):
            id = ''.join(id)
        return hashlib.sha256(id.encode('utf-8')).hexdigest()
