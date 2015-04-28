#############################
Exporting studies to OpenSkin
#############################

***********************
Functionality available
***********************

This is a temporary solution for 0.6.0; future versions will have OpenSkin built-in.

* Fluoroscopy study export in a format suitable for OpenSkin
* Currently OpenSkin must be downloaded and run independently

************************
Instructions for OpenREM
************************

Select the fluoroscopy study you wish to create the exposure incidence map for and go to the detail view. Then click on
link to create the OpenSkin export.

*************************
Instructions for OpenSkin
*************************

Download the latest version as a zip file from https://bitbucket.org/jacole/openskin/downloads. At the time of release
for OpenREM 0.6.0, the current OpenSkin release was 0.4, 26th March 2015. The application referred to here will only
work on Windows. When OpenSkin is built into OpenREM, it will work on both Linux and Windows servers.

* Extract the contents of the zip file into a folder on your computer and run the openSkin.exe executable
* Choose a phantom type: 3D or flat. See `Phantom design`_ for details, but in summary:
    * Flat represents the exposure incidence if the X-rays had been delivered to a film placed flat on the couch
    * 3D represents the exposure incidence if the X-rays had been delivered to a phantom consisting of a cuboid with
      one semi-cylinder on each side
* Select the source csv file - this should be the one exported from OpenREM
* Select the output folder - this should already exist as it can't be created in the dialogue
* Wait! Depending on the number of events in the export and the power of your machine, this can take a few minutes

Two files will be produced:

* Text file called ``skin_dose_results.txt``::

    File created    : 04/21/15 17:42:45
    Data file       : C:/Users/[...]/exports-2015-04-21-OpenSkinExport20150421-162805246134.csv
    Phantom         : 90.0x70.0 3d phantom
    Peak dose (Gy)  :                  0.50844405521
    Cells > 3 Gy    :                              0
    Cells > 5 Gy    :                              0
    Cells > 10 Gy   :                              0

* A small 70 px by 90 px image called ``skin_dose_map.png``







.. _`Phantom design`: https://bitbucket.org/jacole/openskin/wiki/Phantom%20design