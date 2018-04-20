DICOM import modules
====================

RDSR module
+++++++++++

Ultimately this should be the only module required as it deals with all Radiation Dose Structured Reports. This is used
for CT, fluoroscopy, mammography and digital radiography.

.. autotask:: openrem.remapp.extractors.rdsr.rdsr

.. _mammo-module:

Mammography module
++++++++++++++++++

Mammography is interesting in that all the information required for dose
audit is contained in the image header, including patient 'size', ie thickness.
However the disadvantage over an RSDR is the requirement to process each
individual image rather than a single report for the study, which would
also capture any rejected images.

.. autotask:: openrem.remapp.extractors.mam.mam

CR and DR module
++++++++++++++++

In practice this is only useful for DR modalities, but most of them use the
CR IOD instead of the DX one, so both are catered for. This module makes use
of the image headers much like the mammography module.

.. autotask:: openrem.remapp.extractors.dx.dx

CT non-standard modules
+++++++++++++++++++++++

Philips CT dose report images are catered for. These have all the information
that could be derived from the images also held in the DICOM header
information, making harvesting relatively easy.

.. autotask:: openrem.remapp.extractors.ct_philips.ct_philips
    :members:

Older Toshiba CT systems that create dose summary images but cannot create
RDSR objects are also catered for. These have some information that can be derived
from the dose summary objects and CT image tags. This extractor requires that
the DICOM toolkit, java.exe and pixelmed.jar are available to the system.

.. automodule:: openrem.remapp.extractors.rdsr_toshiba_ct_from_dose_images
    :members:

