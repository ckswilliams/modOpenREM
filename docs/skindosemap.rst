########################################
Calulation and display of skin dose maps
########################################

***********************
Functionality available
***********************

* Skin dose map data calculated using in-built openSkin routines
* Data can be calculated on import to OpenREM, or on demand when a study is
  viewed
* Skin dose map data shown graphically as a 2D image and a 3D model
* Sliders are available to change the maximum and minimum displayed dose;
  alternatively, window level and width sliders can be used
* A colour dose scale is shown, with an option to change the colour scheme
* The skin dose map section can be displayed full-screen

The calculated peak skin dose, phantom dimensions and patient height and mass
used for the calculations are shown in the top left hand corner of the skin
dose map.

The skin dose is calculated to the surface of a simple geometric phantom with
dimensions that are calculated from the height and mass of the patient. The
phantom consists of a cuboid with one semi-cylinder on each side (see
`Phantom design`_ for details). A default height of 1.786 m and mass of
73.2 kg are used if patient-specific data is unavailable.

================
2d visualisation
================

The 2d skin dose map section displays:
* The skin dose at the mouse pointer when moved over the map
* Moving the mouse whilst holding down the left-hand mouse button changes the
  window level and width of the displayed skin dose map
* An overlay indicating the phantom regions and orientation: anterior, left,
  posterior, right, superior and inferior
* A save button, which enables the current view to be saved as a png file

================
3d visualisation
================

The 3d skin dose map section displays:
* The skin dose map wrapped around a 3d model of the same dimensions as the
  phantom used to calculate the map
* Moving the mouse whilst holding down the left-hand mouse button rotates the
  3d model
* Turning the mouse wheel zooms in and out
* A simple 3d model of a person is displayed in the bottom left corner. This is
  to enable the viewer to orientate themselves when viewing the 3d skin dose
  map
* A save button, which enables the current view to be saved as a png file

**********************
Skin dose map settings
**********************

There are two skin dose map options that can be set by an OpenREM
administrator:

* Enable skin dose maps
* Calculate skin dose maps on import

The first of these sets whether skin dose map data is calculated, and also
switches the display of skin dose maps on or off.

The second option controls whether the skin dose map data is calculated at the
point when a new study is imported into OpenREM.

When skin dose maps are enabled:

* OpenREM attempts to calculate skin dose map data when a user views the
  details of a fluoroscopy study. These calculations can take some time
* The calculations are carried out in the background: an animated graphic is
  shown whilst the calculations are carried out
* On successful calculation of the data the skin dose map is displayed
* The calculated skin dose map data is saved as a pickle file on the OpenREM
  server in a `skin_maps` subfolder of `MEDIA_ROOT`
* For subsequent views of the same study the data in the pickle file is loaded,
  rather than re-calculating the data, making the display of the skin dose map
  much quicker

When calculation on import is enabled:

* OpenREM calculates the skin dose map data as soon as it arrives in the system
* A pickle file containing the data is saved
* Users viewing the details of a study won't have to wait for the skin dose map
  data to be calculated

***********
Limitations
***********

openSkin is yet to be validated independently - if this is something you want
to do, please do go ahead and feed back your findings to Jonathan Cole at
`jacole`_.


.. _`Phantom design`: http://bitbucket.org/jacole/openskin/wiki/Phantom%20design
.. _`openSkin`: http://bitbucket.org/openskin/openskin
.. _`jacole`: http://bitbucket.org/jacole/
