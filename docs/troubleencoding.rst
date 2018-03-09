***********************
Unknown encoding errors
***********************

Background
==========

OpenREM versions 0.8 and earlier rely on pydicom 0.9.9 which has recently had a new release, version 1.0. A
replacement of pynetdicom is also being worked on and will be called pynetdicom3. When pynetdicom3 is released, OpenREM
will be revised to work the two new packages, but as they are both backwards-incompatible with the old versions you must
keep using the versions specified by the installation instructions until this happens. (The correct version of pydicom
is installed automatically when you install OpenREM).

The function that deals with character set encoding in pydicom 0.9.9 has not been edited since 2013 and is missing a lot
of encodings which can cause imports and query-retrieve functions to fail if those encodings are encountered.

As an interim work-around, users that encounter this issue can take the following step to work with those files in
OpenREM 0.8.

Work-around
===========

Find and edit the pydicom file ``charset.py``. It should be at one of the following paths:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/dicom/charset.py``
* Other linux: ``/usr/lib/python2.7/site-packages/dicom/charset.py``
* Linux virtualenv: ``lib/python2.7/site-packages/dicom/charset.py``
* Windows: ``C:\Python27\Lib\site-packages\dicom\charset.py``
* Windows virtualenv: ``Lib\site-packages\dicom\charset.py``

Replace the dictionary  ``python_encoding`` that is declared at the start with the following dictionary:

.. sourcecode:: python

    # Map DICOM Specific Character Set to python equivalent
    python_encoding = {

        # default character set for DICOM
        '': 'iso8859',

        # alias for latin_1 too (iso_ir_6 exists as an alias to 'ascii')
        'ISO_IR 6': 'iso8859',
        'ISO_IR 13': 'shift_jis',

        # these also have iso_ir_1XX aliases in python 2.7
        'ISO_IR 100': 'latin_1',
        'ISO_IR 101': 'iso8859_2',
        'ISO_IR 109': 'iso8859_3',
        'ISO_IR 110': 'iso8859_4',
        'ISO_IR 126': 'iso_ir_126',  # Greek
        'ISO_IR 127': 'iso_ir_127',  # Arabic
        'ISO_IR 138': 'iso_ir_138',  # Hebrew
        'ISO_IR 144': 'iso_ir_144',  # Russian
        'ISO_IR 148': 'iso_ir_148',  # Turkish
        'ISO_IR 166': 'iso_ir_166',  # Thai
        'ISO 2022 IR 6': 'iso8859',  # alias for latin_1 too
        'ISO 2022 IR 13': 'shift_jis',
        'ISO 2022 IR 87': 'iso2022_jp',
        'ISO 2022 IR 100': 'latin_1',
        'ISO 2022 IR 101': 'iso8859_2',
        'ISO 2022 IR 109': 'iso8859_3',
        'ISO 2022 IR 110': 'iso8859_4',
        'ISO 2022 IR 126': 'iso_ir_126',
        'ISO 2022 IR 127': 'iso_ir_127',
        'ISO 2022 IR 138': 'iso_ir_138',
        'ISO 2022 IR 144': 'iso_ir_144',
        'ISO 2022 IR 148': 'iso_ir_148',
        'ISO 2022 IR 149': 'euc_kr',  # needs cleanup via clean_escseq()
        'ISO 2022 IR 159': 'iso-2022-jp',
        'ISO 2022 IR 166': 'iso_ir_166',
        'ISO 2022 IR 58': 'iso_ir_58',
        'ISO_IR 192': 'UTF8',  # from Chinese example, 2008 PS3.5 Annex J p1-4
        'GB18030': 'GB18030',
        'ISO 2022 GBK': 'GBK',  # from DICOM correction CP1234
        'ISO 2022 58': 'GB2312',  # from DICOM correction CP1234
        'GBK': 'GBK',  # from DICOM correction CP1234
    }

Leave the rest of the file as it was and save. You should now be able to work with DICOM encoded with a much wider range
of character sets.

