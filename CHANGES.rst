=======================
OpenREM version history
=======================

0.9.1 (2019-05-16)
------------------
* `#755`_  Interface: fix more static URLs to allow virtual directory web server configurations
* `#754`_  Documentation and install: updated docs and minimum version for collectstatic_js_reverse
* `#753`_  Query-retrieve: removed patient age fields from study level C-FIND that were not used
* `#752`_  Exports: fixed missing weight field in PHE CT 2019 export
* `#749`_  Documentation: updated the Linux quick install docs
* `#748`_  Charts: fixed error that caused blank charts if series per system was selected
* `#747`_  Installation: changed minimum Python version for current version of Flower
* `#743`_  Testing: added configuration to enable testing with default logging
* `#742`_  Interface: sorting of task tables now works in Internet Explorer 11
* `#740`_  Installation: fixed Celery version to avoid dependency on Django 1.11
* `#739`_  Imports: fixed import errors for GE surgical fluoroscopy
* `#738`_  Logging: added single_date query date to log, added tasks aborts to logs
* `#737`_  Interface and exports: specify number of events and export to PHE 2019 CT survey specification
* `#736`_  Query-retrieve: duplicate study level responses now removed from query
* `#735`_  Imports: switched to more secure defusedxml for parsing XML in comments
* `#734`_  Query-retrieve: handle illegal image level response with no instance number
* `#732`_  Query-retrieve: added advanced option to workaround empty series issue
* `#710`_  Interface: time-based columns in Celery and RabbitMQ tables now sorted correctly
* `#404`_  Code quality: changes to lead toward Python 3 compliance

0.9.0 (2019-03-06)
------------------
* `#733`_  Documentation: post-release fixes for 0.9.0 docs
* `#731`_  Imports: fixed another issue with display names on upgrade to 0.9
* `#729`_  Interface: replaced hard coded URLs in displaynameview.html and review_failed_imports.html with url names
* `#727`_  Imports: fixed issue with display names on upgrade to 0.9
* `#726`_  Documentation: updated to include the new task management function
* `#725`_  Charts: added fluoroscopy charts of DAP and frequency per requested procedure
* `#723`_  Task management: fixed issue with latest version of kombu and amqp on Windows
* `#722`_  Interface: dual-plane DX studies are now displayed without error in filtered list and study detail page
* `#721`_  Documentation: removed Django Debug Toolbar from default install and documented how to install and use it
* `#720`_  Interface: fixed small overlap between skin dose map and irradiation type table
* `#719`_  Interface: fixed hardcoded link in template rffiltered.html
* `#717`_  Query-retrieve: fixed problem where an error was thrown if association is None
* `#716`_  Task manager: removed assumption of queue name from RabbitMQ management interface
* `#714`_  Documentation: add missing documentation about changing STATIC_URL if serving OpenREM in a virtual directory
* `#711`_  Query-retrieve: fixed problem for zero image series when using -toshiba flag
* `#710`_  Interface: Celery and RabbitMQ tables can now be sorted by clicking on column headings
* `#709`_  Query-retrieve: corrected query logic for multiple modalities using `#627`_ Modality tag at study level fix
* `#708`_  Query-retrieve: fixed problem for empty Series Number
* `#707`_  Interface: fixed issue where sigdig returned an error if it was passed an empty string
* `#706`_  Exports: fixed problem where filters were not respected for radiographic exports
* `#705`_  Task manager: added Flower to install and integrated to interface
* `#704`_  Imports: caters for illegal use of dGy.cm2 units in RDSR for DAP values
* `#703`_  Interface: fixed URL lookup error for failed imports on homepage
* `#702`_  Query-retrieve: fixed URLs in DICOM javascript files to allow virtual-directories
* `#701`_  Interface: made the fluoroscopy exposure detail table sortable by clicking on headers
* `#698`_  Imports: allow for incorrect case in Procedure reported tag in RDSR
* `#697`_  Testing: added tests for fluoroscopy high dose alerts (single-plane systems)
* `#696`_  Interface: fixed broken Delete Studies and Entry button
* `#695`_  Imports: added missing name attribute for size_abort url
* `#694`_  Query-retrieve: added extensive logging and summary to interface
* `#693`_  Interface: fixed display of numbers with significant places settings and comma localisation
* `#691`_  Interface: fixed URL lookup error for Display Names page
* `#690`_  Interface: added workload stats user option entry back into config menu
* `#689`_  Interface: fixed URL lookup error for DICOM summary page
* `#688`_  Interface: Add possibility to apply known display name based on Device Observer UID (default: disabled)
* `#685`_  Charts: fixed link code that would otherwise cause DLP per acquisition protocol chart histogram links to fail
* `#683`_  Installation: added VIRTUAL_DIRECTORY to the settings file to avoid updating local_settings file on upgrade
* `#682`_  Charts: fixed problem where links from histogram bars didn't filter correctly when case-insensitive categories selected
* `#681`_  Imports: modified RDSR import to work with Varian RDSRs
* `#679`_  Interface: added ability to filter CT studies on acquisition type
* `#677`_  Interface: added additional filter materials to convert to abbreviations
* `#676`_  Imports: improved error handling on patient size imports
* `#675`_  Exports: improved resilience when export includes malformed studies
* `#674`_  Documentation: amended zip command in example Orthanc configuration to work with Linux and Windows
* `#673`_  Imports: handle empty NumericValues and workaround for incorrect Philips Azurion AcquisitionDeviceType
* `#672`_  Documentation: improve and extend linux one-page install
* `#670`_  Imports: handle illegal multi-value number in Toshiba RDSR with vHP
* `#668`_  Code quality: library import and blank space cleanup
* `#667`_  Web server: enable OpenREM to be hosted from a non-root folder/virtual-directory
* `#666`_  Query-retrieve: handle non-return of ModalitiesInStudy correctly
* `#665`_  Interface: added fluoroscopy high dose highlighting and e-mail alerts
* `#662`_  Administration: added facility to list and purge RabbitMQ queues
* `#659`_  Interface: made the latest study field in summary tables on the home page sort correctly
* `#658`_  Interface: added display of workload stats in home page modality tables
* `#637`_  Administration: added facility to list and purge RabbitMQ queues
* `#554`_  Query-retrieve: added time as matching argument for command line use
* `#461`_  Web server: enable OpenREM to be hosted from a non-root folder/virtual-directory (via `#667`_)
* `#479`_  Administration: added facility to list and delete failed import studies
* `#349`_  Task management: fixed issue with Windows tasks not being killed on request

0.8.1 (2018-09-16)
------------------
* `#663`_  Interface: updated column headings on home page
* `#660`_  Documentation: corrected and improved Linux one-page install
* `#659`_  Interface: made the summary tables on the home page sortable by clicking on headers
* `#656`_  Install: pegged django-debug-toolbar to 1.9.1 until Django is upgraded
* `#654`_  Documentation: supplemented the Orthanc Lua file config option docs
* `#653`_  Docs: clarified notes to get link to Orthanc lua file correct on release
* `#652`_  Documentation: added docs showing Celery daemonisation in Linux
* `#651`_  Documentation: added one-page full setup Ubuntu 18.04 install instructions
* `#650`_  Documentation: modified quick install virtualenv docs
* `#649`_  Documentation: instructions for updating hosts file for Ubuntu and RabbitMQ
* `#648`_  Documentation: clarified Toshiba options when not required
* `#647`_  Documentation: updated link to pixelmed
* `#646`_  Modified Celery import to avoid name clash in some circumstances
* `#645`_  Imports: prevent import failure when text is used in filter thickness field in DX image
* `#644`_  Exports: fixed error in exporting non-ASCII CT protocol acquisition names
* `#643`_  Installation: updated docs to make use of pip binaries for Postgres connector and numpy, Windows and Linux
* `#642`_  Skin dose maps: added catch for error when there are no events in the study
* `#641`_  Exports: mammography exports from filtered pages sorted by AGD no longer result in duplicate studies
* `#640`_  Exports: error in filter listing for NHSBSP csv exports corrected
* `#639`_  Charts: fixed problem where a blank category name may not be displayed correctly
* `#638`_  Skin dose maps: added a link to download data for stand-alone openSkin even when map displayed
* `#627`_  DICOM Networking: implemented workaround for query "bug" in Impax 6.6
* `#606`_  Interface: Made it possible for the user to change his/her password

0.8.0 (2018-06-11)
------------------
* `#635`_  Documentation: added Orthanc as preferred third party DICOM Store service
* `#634`_  Documentation: updated docs for import and query-retrieve duplicates processing
* `#633`_  Charts: fixed issue where charts failed if bar chart series name was null
* `#632`_  DICOM: move requests for queries that don't exist now fail gracefully
* `#631`_  Skin dose maps: bug fixed that prevented message from displaying on screen when skin dose map cannot be calculated
* `#630`_  Documentation: improved installation instructions
* `#628`_  Imports: fixed code for importing when there are duplicate DX or MG studies in the database
* `#626`_  DICOM: isolated the generate modalities in study function and added testing
* `#625`_  Imports: now using event level UIDs to process continued, cumulative and duplicate RDSRs
* `#624`_  Charts: removed filter link on number of events histogram as it was not functioning correctly
* `#623`_  Imports: changed name of Toshiba image based extractor routine
* `#621`_  Documentation: reversed install order of openrem and pynetdicom due to new pydicom release
* `#619`_  Documentation: added workaround for outdated dictionary issues
* `#618`_  DICOM: fixed image level query that prevented RDSRs from being found
* `#617`_  Imports: fixed issue with multi study exams crashing the Toshiba extractor
* `#616`_  Documentation: added information for pip download -d
* `#615`_  Exports: added Target Exposure Index and Deviation Index to radiographic exports
* `#614`_  Exports: handle error when study is deleted during sheet creation for exports
* `#613`_  Imports: fixed dual modality type imports after 'dual' designation from ref `#580`_
* `#612`_  Imports: prevented crash when RDSR was imported with AcquisitionProtocol sequence with no TextValue
* `#610`_  DICOM: query-retrieve changed to work for duplicate RDSRs, ref `#114`_
* `#609`_  Interface: fixed the feature that toggles the selection when clicking anywhere on a display name table row
* `#608`_  Interface: fixed the broken sorting of display name table
* `#603`_  Interface: fixed JavaScript error if there are any None values in fluoro detail irradiation type table
* `#602`_  Skin dose maps: fixed error when there are multiple kVp values for a single irradiation event
* `#599`_  Installation: postgres instructions now include note about differing security choices
* `#597`_  Skin dose maps: documented that using a production webserver the default timeout value must be increased
* `#596`_  Documentation: added docs for using Gunicorn and NGINX on linux
* `#594`_  Display: corrected display of dual-plane DAP and RP dose in RF filtered view
* `#593`_  Imports: properly handles MultiValue filter material tags and permits aluminium spelling
* `#592`_  Documentation: added docs for using IIS on Windows
* `#589`_  Exports: now handles zero studies and studies deleted during exports sensibly
* `#587`_  Documentation: added instructions for Linux users to rotate logs
* `#586`_  Documentation: updated exports and detailed how pulse level data is exported
* `#585`_  Documentation: added information about multiple cumulative RDSRs
* `#584`_  Import, Interface, Export: RDSR with pulse level data now function
* `#583`_  Documentation: added information about dual mode modalities and deleting all from an X-ray unit
* `#582`_  Celery: updated results backend as amqp deprecated and slow
* `#581`_  Import scripts: interpreter line now always first, functions imported specifically
* `#580`_  Imports and Interface: one modality creating both DX and RF can now be handled appropriately
* `#579`_  Imports: dummy values for Toshiba CT import function now in settings.py, log file config in docs
* `#578`_  Exports: fixed NHSBSP export that was excluding RDSR imported Hologic studies
* `#575`_  Exports: export page now updates using AJAX and has a select all button
* `#573`_  Exports: corrected and clarified exposure time and duration units, added number of pulses
* `#572`_  Interface: homepage now populates as AJAX to increase responsiveness
* `#570`_  Charts: simplified chart function code
* `#569`_  Charts: fixed frequency issue with mean averages selected
* `#568`_  Imports: missing DICOM date-time no longer causes an error
* `#567`_  Celery: fixed dual-namespace imports of tasks
* `#566`_  Interface: correctly show "assumed patient mass" in case of set value of zero
* `#565`_  Interface: correctly handle dose area product with zero value
* `#564`_  Skin dose maps: text information on skin dose maps now embedded when saving the 2d or 3d map as a graphic
* `#562`_  Skin dose maps: error message on calculation failure now more explicit
* `#561`_  Imports: patient orientation modifier now correctly extracted from RDSR
* `#560`_  Exports: added study level comments
* `#559`_  Interface: date pickers inconsistent start day fixed
* `#558`_  Skin dose maps: set defaults instead of crashing if kV, dose, table or tube/detector position are missing
* `#557`_  Skin dose maps: improved construction of patient orientation code
* `#556`_  Exports: DX exports where TotalNumberOfRadiographicFrames is not populated now export
* `#552`_  Documentation: documented extractor for older Toshiba CT scanners
* `#551`_  Documentation: added procedure for opening csv files in Excel with non-ASCII characters
* `#550`_  Documentation: added a note to describe exposure time and duration for fluoroscopy studies
* `#549`_  Documentation: added procedure for fixing laterality on Hologic studies, ref `#411`_
* `#547`_  Interface: improved handling of available time information for fluoro studies
* `#546`_  Query Retrieve: added flag and functionality to query for Toshiba images
* `#544`_  Interface: added procedure, requested procedure to summary listings and details and filtering
* `#543`_  Interface: added drop-down box to choose how many studies are displayed on filtered pages
* `#542`_  Interface: added display name to all detailed html pages
* `#541`_  Documentation: updated for celery on Windows
* `#540`_  Documentation: updated for current skinDose functionality
* `#539`_  Documentation: updated chart document to include series toggle buttons
* `#537`_  Charts: hide series function added
* `#536`_  Code quality: reduced javascript duplication and collected file groups into subfolders
* `#535`_  Interface: fixed problem where category names that included a plus symbol caused filtering and chart issues
* `#534`_  Interface: chart drilldown reported as not working - was actually due to a user's database migrations
* `#533`_  Query Retrieve: Reduced number of simultaneous associations to one, reused for everything
* `#532`_  DICOM: documented how to work-around missing encoding charsets due to old pydicom
* `#529`_  Charts: added CT charts of number of irradiation events per study description and requested procedure
* `#528`_  Query Retrieve: reduced number of simultaneous associations to one, reused for everything
* `#526`_  Code quality: addressed some of the code quality/style issues raised by `Codacy`_
* `#525`_  Importing: improved mammo import by checking compression force before converting to float
* `#524`_  Importing: improved mammo import by checking anode exists before converting to DICOM terms
* `#523`_  Importing: changed mammo import to use del_no_match instead of del_mg_im if not mammo
* `#522`_  Documentation: made it clearer on offline-install docs that version numbers will change
* `#521`_  Testing: added tests for dual source CT imports
* `#520`_  Imports: removed XML styling from Philips legacy CT comment creation
* `#519`_  Skin dose maps: fixed black on black text issue
* `#518`_  Importing: fixed imports where CT Target Region isn't specified
* `#517`_  Interface: operator name is now displayed on the detail page for each modality, along with physician for CT and fluoro
* `#516`_  Imports: MultiValue person names are now stored as a decoded string, not a list
* `#511`_  Testing: develop and other branches can now be deployed to dev.openrem.org and testing.openrem.org automatically
* `#510`_  Imports: 'not-patient-indicators' can now be configured in the interface
* `#509`_  Skin dose maps: now recalculated on view if recorded height or weight has changed since last calculation
* `#508`_  Testing: DX sample files are now tested
* `#507`_  Interface: Mammo now filterable by study description, procedure, requested procedure and acquisition protocol
* `#506`_  Documentation: updated query-retrieve docs
* `#505`_  Charts: n is now displayed on charts
* `#504`_  Charts: Fixed issue with null values
* `#503`_  Internationalisation: more robust decoding and use of unicode throughout
* `#502`_  Testing: tests now work with SQLite3 and PostgreSQL databases
* `#501`_  Imports: Changed field type for CodeValue  from 16 chars to text, allows for illegal long values
* `#500`_  Imports: Philips SC Dose Info with missing time stamps now import
* `#499`_  Imports: Now aborts gracefully with error log if no template in RDSR
* `#498`_  Exports: Missing units added to header fields
* `#497`_  Interface: Detailed fluoro study view: added irradiation type, pulse rate, dose to ref. point, secondary angle, total DAP and ref. point dose from each irradition type
* `#495`_  Charts: Reduced time taken to render scatter plots with multiple series
* `#494`_  Charts: Charts now ignore blank and zero-value data when calculating mean, median and number of events
* `#493`_  Charts: Added user option to made chart categories all lower case
* `#492`_  Exports: Each view is now unique for NHSBSP mammo exports as required by the NCCPM database
* `#491`_  Imports, Interface and Exports: CT Dose Check alerts and notifications are now extracted, displayed and exported
* `#490`_  Exports: Response object included for messages - removed as now asynchronous
* `#489`_  Exports: NHSBSP mammo exports deals with all views, excludes biopsies and specimens
* `#488`_  Exports: All exports now include study time
* `#487`_  Imports: CT RDSR now imports 'procedure context' correctly
* `#486`_  Imports: CT RDSR now imports 'NameOfPhysiciansReadingStudy' correctly
* `#485`_  Imports: CT RDSR now imports 'target region' correctly
* `#484`_  Exports and Interface: Exports and interface page views are now more efficient and (much) faster
* `#482`_  Imports: DX extractor now extracts acquisition protocol, requested procedure name and study name for Fuji Go mobile; extracts acquisition protocol for Toshiba Radrex equipment; extracts requested procedure name from Carestream DRX-Revolution mobiles
* `#480`_  Imports: Code and instructions to create and import an RDSR from Toshiba CT dose summary images and studies
* `#476`_  Imports: Mixed latin-1 and UTF8 characters now imported, but need to be handled better if possible
* `#475`_  Query Retrieve: Made -sr a stand-alone option - it has a very niche use-case!
* `#474`_  Logging: Changing to DEBUG logging level in ``local_settings.py`` will now be respected
* `#473`_  Query Retrieve: Added tests
* `#472`_  Query Retrieve: Overhauled the query retrieve routines
* `#471`_  Internationalisation: added configuration and docs to set the timezone
* `#470`_  Query Retrieve: Optimised CT filtering
* `#468`_  Query Retrieve: Station names can now be used for filtering if returned
* `#467`_  Testing: Added tests for mammography RDSR imports
* `#466`_  Query Retrieve: RDSR now retrieved in preference to images for MG and DX/CR
* `#465`_  Added newer SSDE and water equivalent diameter fields to database
* `#464`_  Imports: DX RDSR now imported properly
* `#463`_  Imports: Properly checks that Enhanced SR are GE dose reports before importing
* `#460`_  Interface: Display names table now sortable
* `#458`_  Exports: Filter thicknesses are rounded to max 4 significant figures on export
* `#454`_  Exports: Mean filter thickness now reported in exports
* `#453`_  Imports: DX with min filter thickness greater than max have values switched on import
* `#452`_  Exports: Added CTDIw phantom size to CT exports
* `#451`_  Skin dose maps: fixed issue with filters being referenced before being defined
* `#450`_  Imports: DX imports with filter thickness of 0.00 are now recorded as such
* `#449`_  Exports: Fixed a bug that prevented fluoro exports if protocol names had non-ASCII characters
* `#448`_  Documentation: Added a diagram showing the relationship between the OpenREM system components
* `#447`_  Imports: Modified rdsr and ctdetail template to import and display data from Pixelmed generated Toshiba RDSR
* `#446`_  Import: Extract additional Philips private information for Allura Xper systems, create workaround for missing end angles for rotational acquisitions
* `#445`_  Interface: Added function for user to determine between DX and fluoro for ambiguous modalities
* `#444`_  Imports: DX systems that submit RDSRs that look like fluoro can now be reclassified using `#445`_
* `#443`_  Exports: Accession number and ID are now exported to XLSX as text. Thanks to `@LuukO`_
* `#442`_  Exports: Fixed RF exports with multiple filters, added tests. Thanks to `@LuukO`_
* `#441`_  Charts: Fixed a bug that broke chart links containing non-ASCII characters
* `#440`_  Charts: Fixed a bug in sorting.js so that undefined strings are handled correctly
* `#439`_  Charts: Added controls for plotting a series per system and calculation histogram data to each filtered view
* `#438`_  Skin dose maps: skin dose maps successfully calculated from existing studies; indication of assumed or extracted data shown
* `#434`_  Internationalisation: added passing char_set throughout the extractor functions (since largely made redundant again!)
* `#432`_  Imports: RDSR import function now looks in comment field for `patient_table_relationship` data
* `#431`_  Imports: fixed DX imports with MultiValue filter values (Cu+Al) again!
* `#430`_  Exports: fixed DX exports with multiple filters again, added tests
* `#429`_  Charts: added new mammo scatter plots. Thanks to `@rijkhorst`_
* `#427`_  Testing: added a large number of tests that are automatically run on commit to bitbucket
* `#414`_  Reduced use of JavaScript global variables and improved JavaScript objects
* `#411`_  Imports: fixed laterality and accumulated AGD failure for Hologic DBT proprietary projection images
* `#323`_  Documentation: code autodocumentation largely now working again
* `#318`_  Database management: Display names view can be used to review and delete all studies from one source
* `#114`_  Imports: Subsequent RDSRs of the same study will now replace existing study in database
* `#61`_  Skin dose maps: These have been re-enabled, and currently work for Siemens systems

0.7.4 (2016-10-17)
------------------

* `#436`_  Install: temporary fix blocking django-filter latest version that breaks OpenREM
* `#431`_  Imports: fixed DX imports with MultiValue filter values (Cu+Al)
* `#430`_  Exports: fixed DX exports with multiple filters (Cu + Al)


0.7.3 (2016-08-30)
------------------

* `#426`_  Charts: added css so that wide chart data tables are displayed above the filter form div
* `#425`_  Exports: fixed error with non-ASCII characters being exported to csv
* `#424`_  Charts: fixed error where png or svg export of chart would show incorrect x-axis labels
* `#423`_  Charts: fixed error where some chart plotting options were not updated after being changed by the user
* `#422`_  Charts: added a button below each chart to toggle the display of the data table
* `#421`_  Charts: fixed error where only some scatter plot data was being exported to csv or xls files
* `#420`_  Charts: fixed error where frequency pie charts were only showing data from the first system
* `#419`_  Interface: fixed error where "Cancel" was ignored when deleting study in Firefox browser
* `#418`_  Exports: fixed error when exporting fluoroscopy study with missing xray_filter_material
* `#416`_  Charts: improved efficiency of JavaScript
* `#415`_  Database: migration for 0.6 upgraded installs to fix acquisition_device_type failures
* `#413`_  Documentation: removed erroneous reference to store queue in stop celery command
* `#410`_  Charts: fixed display of bar charts containing only one data point
* `#408`_  Charts: Increased number of items that can be shown on some Highcharts plots
* `#407`_  Fixed issue where skin dose map data was not being calculated on import
* `#406`_  Replaced Math.log10 JavaScript function with alternative function to fix IE11 skin dose map error
* `#405`_  Altered multi-line cell links in filtered pages so they work with IE8

0.7.1 (2016-06-10)
------------------

* `#403`_  Now deals with PersonName fields with latin-1 extended characters correctly
* `#402`_  Skin dose map data pickle files saved using gzip compression to save space
* `#401`_  Updated skin dose map documentation to say it won't be in this release
* `#400`_  Strings are encoded as UTF-8 before being hashed to prevent errors with non-ASCII characters
* `#399`_  Migration file brought up to date for 0.6 to 0.7 upgrades
* `#398`_  Skin exposure maps are now stored in folders (feature postponed for future release)
* `#397`_  Skin exposure maps no longer available until orientation errors are fixed
* `#396`_  Charts: zooming on bar charts of average value vs. category now works
* `#395`_  Docs: offline Windows install instructions created, plus offline upgrade instructions
* `#394`_  Charts: made charts resize to fit containing div when browser is resized
* `#392`_  Charts: normalised histogram tooltip now correctly reports frequency
* `#391`_  Basic troubleshooting is now documented
* `#390`_  Charts: mammography and fluoroscopy charts added
* `#389`_  Charts: series without a name are now plotted under the name of `Blank` rather than not being plotted at all
* `#387`_  Added laterality to mammography exports
* `#385`_  Fixed issue with non-ASCII letters in RDSR sequence TextValue fields
* `#384`_  Fluoro exports for OpenSkin only consider copper filters now
* `#383`_  Refreshed settings.py to django 1.8 including updating template settings and TEMPLATE_CONTEXT_PROCESSORS
* `#380`_  Tube current now extracted from Siemens Intevo RDSR despite non-conformance
* `#379`_  Exposure time now populated for fluoro if not supplied by RDSR
* `#378`_  The display name of multiple systems can now be updated together using a single new name
* `#376`_  Corrected an ill-advised model change
* `#374`_  CTDIw phantom size now displayed in CT detail view
* `#373`_  Charts in some releases used GT rather than greater than or equal to for start date, now fixed
* `#372`_  Mammography studies now record an accumulated AGD per breast. Existing joint accumulated AGD values won't be
  changed. Ordering by Accumulated AGD now creates an entry per accumulated AGD, one per breast
* `#371`_  Mammo RDSR generates average mA where not recorded, mammo image populates mA
* `#370`_  Added study description to mammography export
* `#369`_  Bi-plane fluoroscopy studies now export correctly
* `#368`_  Mammo RDSR now imports correctly
* `#365`_  Tube filtration is now displayed in the RF detail view
* `#364`_  Philips Allura fluorscopy RDSRs now import correctly
* `#362`_  Display of RF where bi-plane RDSRs have been imported no longer crash the interface
* `#360`_  Charts: saving data from average data charts as csv or xls now includes frequency values
* `#359`_  Added missing 'y' to query retrieve command line help
* `#358`_  Charts: chart sorting links and instructions now hidden when viewing histograms
* `#357`_  Charts: button to return from histogram now displays the name of the main chart
* `#356`_  Charts: histogram normalise button appears for all appropriate charts
* `#355`_  Charts: sorting now works as expected for plots with a series per system
* `#352`_  Fixed CT xlsx exports that had complete study data in each series protocol sheet (from earlier beta)
* `#351`_  Charts: simplified chart JavaScript and Python code
* `#350`_  DICOM networking documented for use with 3rd party store and advanced use with native
* `#348`_  Study delete confirmation page now displays total DAP for DX or CR radiographic studies
* `#346`_  Charts: exporting a chart as an image no longer requires an internet connection
* `#345`_  CSV size imports in cm are now stored as m in the database. Interface display of size corrected.
* `#343`_  Charts: user can now specify number of histogram bins in the range of 2 to 40
* `#342`_  Charts: improved the colours used for plotting chart data
* `#340`_  Fixed store failure to save due to illegal values in Philips private tags, improved exception code
* `#339`_  Improved extraction of requested procedure information for radiographic studies
* `#338`_  Fix Kodak illegally using comma in filter thickness values
* `#335`_  DICOM Store keep_alive and echo_scu functions now log correctly
* `#334`_  Fixed issue with tasks needing to be explicitly named
* `#333`_  Fixed StoreSCP not starting in beta 11 error
* `#332`_  Charts: some charts can now be plotted with a series per x-ray system
* `#331`_  Keep_alive tasks are now discarded if not executed, so don't pile up
* `#329`_  All existing logging is now done via the same log files
* `#328`_  Store SCP no longer uses Celery tasks
* `#327`_  Celery workers now only take one task at a time
* `#325`_  Charts: switching charts off now leaves the user on the same page, rather than going to the home page
* `#324`_  Charts: forced chart tooltip background to be opaque to make reading the text easier
* `#320`_  The week now begins on Monday rather than Sunday on date form fields
* `#316`_  Query retrieve function can now exclude and include based on strings entered
* `#315`_  Charts: made size of exported chart graphics follow the browser window size
* `#314`_  One version number declaration now used for distribute, docs and interface
* `#313`_  Replaced non-working function with code to extract SeriesDescription etc in query response message
* `#312`_  Display names are now grouped by modality
* `#311`_  Queries are deleted from database after a successful C-Move
* `#310`_  Series level QR feedback now presented. Any further would require improvements in pynetdicom
* `#309`_  StoreSCP now deals safely with incoming files with additional transfer syntax tag
* `#308`_  Secondary capture images that don't have the manufacturer field no longer crash the StoreSCP function
* `#306`_  Charts: added a button to each chart to toggle full-screen display
* `#305`_  Added links to documentation throughout the web interface
* `#304`_  Date of birth is now included in all exports that have either patient name or ID included
* `#303`_  Fixed a typo in 0.6.0 documents relating to the storescp command
* `#302`_  Improved handling of Philips Dose Info objects when series information sequence has UN value representation
* `#301`_  Charts: fixed bug that could stop average kVp and mAs radiographic plots from working
* `#300`_  Calling AE Title for Query Retrieve SCU is now configured not hardcoded
* `#299`_  Hash of MultiValued DICOM elements now works
* `#298`_  Added ordering by accumulated AGD for mammographic studies
* `#297`_  Fixed ordering by Total DAP for radiographic studies
* `#296`_  StoreSCP now logs an error message and continues if incoming file has problems
* `#295`_  Charts: fixed bug that arose on non-PostgreSQL databases
* `#294`_  Harmonised time display between filter list and detail view, both to HH:mm
* `#292`_  Added keep-alive and auto-start to DICOM stores
* `#291`_  Charts: fixed issue with CTDI and DLP not showing correct drilldown data
* `#290`_  Added new tables and fields to migration file, uses `#288`_ and median code from `#241`_
* `#289`_  Crispy forms added into the requires file
* `#288`_  Added device name hashes to migration file
* `#286`_  Increased granularity of permission groups
* `#285`_  Tidied up Options and Admin menus
* `#284`_  Fixed DICOM Query that looped if SCP respected ModalitiesInStudy
* `#282`_  Missing javascript file required for IE8 and below added
* `#281`_  Added check to import function to prevent extract failure
* `#280`_  Fixed typo in mammography export
* `#279`_  Charts: Fixed issue with median CTDI series from appearing
* `#278`_  Charts: Fixed javascript namespace pollution that caused links to fail
* `#277`_  Overhaul of acquisition level filters to get tooltip generated filters to follow through to export
* `#276`_  Unique fields cannot have unlimited length in MySQL - replaced with hash
* `#274`_  Charts: Fixed legend display issue
* `#273`_  Charts: Added plots of average kVp and mAs over time for DX
* `#272`_  Tweak to display of exam description for DX
* `#271`_  Fixed DX import failure where ``AcquisitionDate`` or ``AcquisitionTime`` are ``None``
* `#270`_  Django 1.8 Admin site has a 'view site' link. Pointed it back to OpenREM
* `#268`_  Improved population of procedure_code_meaning for DX imports
* `#266`_  DICOM C-Store script added back in - largely redundant with web interface
* `#265`_  DICOM Store and Query Retrieve services documented
* `#263`_  Settings for keeping or deleting files once processed moved to database and web interface
* `#262`_  Dealt with issue where two exposures from the same study would race on import
* `#260`_  Fixed issue where import and export jobs would get stuck behind StoreSCP task in queue
* `#259`_  Link to manage users added to Admin menu
* `#258`_  Fixed DX import error where manufacturer or model name was not provided
* `#257`_  Documentation update
* `#256`_  Fixed errors with non-ASCII characters in imports and query-retrieve
* `#255`_  Charts: Small y-axis values on histograms are more visible when viewing full-screen
* `#254`_  Charts: Simplified chart data processing in the templates
* `#253`_  Charts: AJAX used to make pages responsive with large datasets when charts enabled
* `#252`_  Fixed duplicate entries in DX filtered data for studies with multiple exposures
* `#248`_  Charts: can now be ordered by frequency or alphabetically
* `#247`_  Fixed incorrect reference to manufacturer_model_name
* `#246`_  Charts: Added median data for PostgreSQL users
* `#245`_  Fixed error in csv DX export
* `#244`_  Fixed issue where scripts wouldn't function after upgrade to Django 1.8
* `#243`_  Added distance related data to DX exports
* `#242`_  Distance source to patient now extracted from DX images
* `#241`_  Charts: Median values can be plotted for PostgreSQL users
* `#240`_  Charts: Improved DAP over time calculations
* `#239`_  Configurable equipment names to fix multiple sources with the same station name
* `#237`_  Charts: Tidied up plot data calculations in ``views.py``
* `#235`_  Added patient sex to each of the exports
* `#234`_  Charts: Fixed error with datetime combine
* `#232`_  Charts: on or off displayed on the home page
* `#231`_  Charts: made links from requested procedure frequency plot respect the other filters
* `#230`_  Fixed error in OperatorsName field in DICOM extraction
* `#229`_  Charts: Added chart of DLP per requested procedure
* `#223`_  Charts: speed improvement for weekday charts
* `#217`_  Charts: Further code optimisation to speed up calculation time
* `#207`_  DICOM QR SCU now available from web interface
* `#206`_  DICOM Store SCP configuration now available from web interface
* `#183`_  Added options to store patient name and ID, and options to hash name, ID and accession number
* `#171`_  Root URL now resolves so ``/openrem`` is not necessary
* `#151`_  Suspected non-patient studies can now be filtered out
* `#135`_  GE Senographe DS now correctly records compression force in Newtons for new imports
* `#120`_  Improved testing of data existing for exports
* `#118`_  Upgraded to Django 1.8
* `#70`_   User is returned to the filtered view after deleting a study
* `#61`_   Skin dose maps for fluoroscopy systems can now be calculated and displayed

0.6.2 (2016-01-27)
------------------
* `#347`_  Django-filter v0.12 has minimum Django version of 1.8, fixed OpenREM 0.6.2 to max django-filter 0.11
* `#341`_  Changed references to the OpenSkin repository for 0.6 series.

0.6.1 (2015-10-30)
------------------
* `#303`_  Corrected name of Store SCP command in docs

0.6.0 (2015-05-14)
------------------

* `#227`_  Fixed import of RDSRs from Toshiba Cath Labs
* `#226`_  Charts: Updated Highcharts code and partially fixed issues with CTDIvol and DLP combined chart
* `#225`_  Charts: Added link from mAs and kVp histograms to associated data
* `#224`_  Charts: Added link from CTDIvol histograms to associated data
* `#221`_  Charts: Fixed issue where filters at acquisition event level were not adequately restricting the chart data
* `#219`_  Charts: Fixed issue where some charts showed data beyond the current filter
* `#217`_  Charts: Code optimised to speed up calculation time
* `#216`_  Fixed typo that prevented import of RSDR when DICOM store settings not present
* `#215`_  Charts: Fixed x-axis labels for mean dose over time charts
* `#214`_  Charts: Improved consistency of axis labels
* `#213`_  Fixed admin menu not working
* `#212`_  Charts: Created off-switch for charts
* `#210`_  OpenSkin exports documented
* `#209`_  Charts: Fixed server error when CT plots switched off and filter form submitted
* `#208`_  Charts: Fixed blank chart plotting options when clicking on histogram tooltip link
* `#205`_  Charts: Fixed issue of histogram tooltip links to data not working
* `#204`_  Charts: Fixed issue of not being able to export with the charts features added
* `#203`_  Charts: Fixed display of HTML in plots issue
* `#202`_  Charts: Added mean CTDIvol to charts
* `#200`_  Charts: Now exclude Philips Ingenuity SPRs from plots
* `#196`_  Added comments and entrance exposure data to DX export
* `#195`_  Fixed error with no users on fresh install
* `#194`_  Added more robust extraction of series description from DX
* `#193`_  Charts: Fixed reset of filters when moving between pages
* `#192`_  Created RF export for OpenSkin
* `#191`_  Charts: Factored out the javascript from the filtered.html files
* `#190`_  Charts: Added time period configuration to dose over time plots
* `#189`_  Charts: Fixed plotting of mean doses over time when frequency not plotted
* `#187`_  Charts: Merged the charts work into the main develop branch
* `#186`_  Fixed duplicate data in DX exports
* `#179`_  Charts: Added kVp and mAs plots for DX
* `#177`_  Charts: Fixed issue with date ranges for DX mean dose over time charts
* `#176`_  Charts: Added link to filtered dataset from mean dose over time charts
* `#175`_  Charts: Allowed configuration of the time period for mean dose trend charts to improve performance
* `#174`_  Charts: Fixed number of decimal places for mean DLP values
* `#173`_  Charts: Fixed plot of mean DLP over time y-axis issue
* `#170`_  Charts: Added plot of mean dose over time
* `#169`_  Charts: Improved chart colours
* `#157`_  Charts: Added chart showing number of studies per day of the week, then hour in the day
* `#156`_  Charts: Fixed issue with some protocols not being displayed
* `#155`_  Charts: Added chart showing relative frequency of protocols and study types
* `#140`_  Charts: Added configuration options
* `#139`_  Charts: Link to filtered dataset from histogram chart
* `#138`_  Charts: Number of datapoints displayed on tooltip
* `#135`_  Mammography compression force now only divides by 10 if model contains *senograph ds* **Change in behaviour**
* `#133`_  Documented installation of NumPy, initially for charts
* `#41`_   Preview of DICOM Store SCP now available
* `#20`_   Modality sections are now suppressed until populated


0.5.1 (2015-03-12)
------------------

* `#184`_  Documentation for 0.5.1
* `#180`_  Rename all reverse lookups as a result of `#62`_
* `#178`_  Added documentation regarding backing up and restoring PostgreSQL OpenREM databases
* `#172`_  Revert all changes made to database so `#62`_ could take place first
* `#165`_  Extract height and weight from DX, height from RDSR, all if available
* `#161`_  Views and exports now look for accumulated data in the right table after changes in `#159`_ and `#160`_
* `#160`_  Created the data migration to move all the DX accumulated data from TID 10004 to TID 10007
* `#159`_  Modified the DX import to populate TID 10007 rather than TID 10004. RDSR RF already populates both
* `#158`_  Demo website created by DJ Platten: http://demo.openrem.org/openrem
* `#154`_  Various decimal fields are defined with too few decimal places - all have now been extended.
* `#153`_  Changed home page and modality pages to have whole row clickable and highlighted
* `#150`_  DJ Platten has added Conquest configuration information
* `#137`_  Carestream DX multiple filter thickness values in a DS VR now extracted correctly
* `#113`_  Fixed and improved recording of grid information for mammo and DX and RDSR import routines
* `#62`_   Refactored all model names to be less than 39 characters and be in CamelCase to allow database migrations and
  to come into line with PEP 8 naming conventions for classes.


0.5.0 (2014-11-19)
------------------

* Pull request from DJ Platten: Improved display of DX data and improved export of DX data
* `#132`_  Fixed mammo export error that slipped in before the first beta
* `#130`_  Only creates ExposureInuAs from Exposure if Exposure exists now
* `#128`_  Updated some non-core documentation that didn't have the new local_settings.py reference or the new
  openremproject folder name
* `#127`_  DX IOD studies with image view populated failed to export due to lack of conversion to string
* `#126`_  Documentation created for the radiographic functionality
* `#125`_  Fixes issue where Hologic tomo projection objects were dropped as they have the same event time as the 2D element
* `#123`_  Fixed issue where filters came through on export as lists rather than strings on some installs
* `#122`_  Exports of RF data should now be more useful when exporting to xlsx. Will need refinement in the future
* `#26`_   Extractors created for radiographic DICOM images. Contributed by DJ Platten
* `#25`_   Views and templates added for radiographic exposures - either from RDSRs or from images - see `#26`_.
  Contributed by DJ Platten
* `#9`_    Import of \*.dcm should now be available from Windows and Linux alike


0.4.3 (2014-10-01)
------------------

* `#119`_  Fixed issue where Celery didn't work on Windows. Django project folder is now called openremproject instead of openrem
* `#117`_  Added Windows line endings to patient size import logs
* `#113`_  Fixed units spelling error in patient size import logs
* `#112`_  File system errors during imports and exports are now handled properly with tasks listed in error states on the summary pages
* `#111`_  Added abort function to patient size imports and study exports
* `#110`_  Converted exports to use the FileField handling for storage and access, plus modified folder structure.
* `#109`_  Added example ``MEDIA_ROOT`` path for Windows to the install docs
* `#108`_  Documented ownership issues between the webserver and Celery
* `#107`_  Documented process for upgrading to 0.4.2 before 0.4.3 for versions 0.3.9 or earlier
* `#106`_  Added the duration of export time to the exports table. Also added template formatting tag to convert seconds to natural time
* `#105`_  Fixed bug in Philips CT import where :py:class:`decimal.Decimal` was not imported before being used in the age calculation
* `#104`_  Added documentation for the additional study export functions as a result of using Celery tasks in task `#19`_ as well as documentation for the code
* `#103`_  Added documentation for using the web import of patient size information as well as the new code
* `#102`_  Improved handling of attempts to process patient size files that have been deleted for when users go back in the browser after the process is finished
* `#101`_  Set the security of the new patient size imports to prevent users below admin level from using it
* `#100`_  Logging information for patient size imports was being written to the database - changed to write to file
* `#99`_   Method for importing remapp from scripts and for setting the `DJANGO_SETTINGS_MODULE` made more robust so that it should work out of the box on Windows, debian derivatives and virtualenvs
* `#98`_   Versions 0.4.0 to 0.4.2 had a settings.py.new file to avoid overwriting settings files on upgrades; renaming this file was missing from the installation documentation for new installs
* `#97`_   Changed the name of the export views file from ajaxviews as ajax wasn't used in the end
* `#96`_   Changed mammo and fluoro filters to use named fields to avoid needing to use the full database path
* `#93`_   Set the security of the new exports to prevent users below export level from creating or downloading exports
* `#92`_   Add `NHSBSP specific mammography csv export`_ from Jonathan Cole - with Celery
* `#91`_   Added documentation for Celery and RabbitMQ
* `#90`_   Added delete function for exports
* `#89`_   Added the Exports navigation item to all templates, limited to export or admin users
* `#88`_   Converted fluoroscopy objects to using the Celery task manager after starting with CT for `#19`_
* `#87`_   Converted mammography objects to using the Celery task manager after starting with CT for `#19`_
* `#86`_   Digital Breast Tomosynthesis systems have a projections object that for Hologic contains required dosimetry information
* `#85`_   Fix for bug introduced in `#75`_ where adaption of ptsize import for procedure import broke ptsize imports
* `#74`_   'Time since last study' is now correct when daylight saving time kicks in
* `#39`_   Debug mode now defaults to False
* `#21`_   Height and weight data can now be imported through forms in the web interface
* `#19`_   Exports are now sent to a task manager instead of locking up the web interface

Reopened issue
``````````````

* `#9`_    Issue tracking import using \*.dcm style wildcards reopened as Windows ``cmd.exe`` shell doesn't do wildcard expansion, so this will need to be handled by OpenREM in a future version

0.4.2 (2014-04-15)
------------------

* `#83`_   Fix for bug introduced in `#73`_ that prevents the import scripts from working.

0.4.1 (2014-04-15)
------------------

* `#82`_   Added instructions for adding users to the release notes

0.4.0 (2014-04-15)
------------------

..  note::

    * `#64`_ includes **changes to the database schema and needs a user response** - see `version 0.4.0 release notes <https://docs.openrem.org/page/release-0.4.0.html>`_
    * `#65`_ includes changes to the settings file which **require settings information to be copied** and files moved/renamed - see `version 0.4.0 release notes <https://docs.openrem.org/page/release-0.4.0.html>`_


* `#80`_   Added docs for installing Apache with auto-start on Windows Server 2012. Contributed by JA Cole
* `#79`_   Updated README.rst instructions
* `#78`_   Moved upgrade documentation into the release notes page
* `#77`_   Removed docs builds from repository
* `#76`_   Fixed crash if exporting from development environment
* `#75`_   Fixed bug where requested procedure wasn't being captured on one modality
* `#73`_   Made launch scripts and ptsizecsv2db more robust
* `#72`_   Moved the secret key into the local documentation and added instructions to change it to release notes and install instructions
* `#71`_   Added information about configuring users to the install documentation
* `#69`_   Added documentation about the new delete study function
* `#68`_   Now checks sequence code meaning and value exists before assigning them. Thanks to JA Cole
* `#67`_   Added 'Contributing authors' section of documentation
* `#66`_   Added 'Release notes' section of documentation, incuding this file
* `#65`_   Added new ``local_settings.py`` file for database settings and other local settings
* `#64`_   Fixed imports failing due to non-conforming strings that were too long
* `#63`_   The mammography import code stored the date of birth unnecessarily. Also now gets decimal_age from age field if necessary
* `#60`_   Removed extraneous colon from interface data field
* `#18`_   Studies can now be deleted from the web interface with the correct login
* `#16`_   Added user authentication with different levels of access
* `#9`_    Enable import of ``*.dcm``


0.3.9 (2014-03-08)
------------------
..  note:: `#51`_ includes changes to the database schema -- make sure South is in use before upgrading. See https://docs.openrem.org/page/upgrade.html

* `#59`_   CSS stylesheet referenced particular fonts that are not in the distribution -- references removed
* `#58`_   Export to xlsx more robust - limitation of 31 characters for sheet names now enforced
* `#57`_   Modified the docs slightly to include notice to convert to South before upgrading
* `#56`_   Corrected the mammography target and filter options added for issue `#44`_
* `#53`_   Dates can now be selected from a date picker widget for filtering studies
* `#52`_   Split the date field into two so either, both or neither can be specified
* `#51`_   Remove import modifications from issue `#28`_ and `#43`_ now that exports are filtered in a better way after `#48`_ and `#49`_ changes.
* `#50`_   No longer necessary to apply a filter before exporting -- docs changed to reflect this
* `#49`_   CSV exports changed to use the same filtering routine introduced for `#48`_ to better handle missing attributes
* `#48`_   New feature -- can now filter by patient age. Improved export to xlsx to better handle missing attributes
* `#47`_   Install was failing on pydicom -- fixed upstream

0.3.8 (2014-03-05)
------------------

* --    File layout modified to conform to norms
* `#46`_   Updated documentation to reflect limited testing of mammo import on additional modalities
* `#45`_   mam.py was missing the licence header - fixed
* `#44`_   Added Tungsten, Silver and Aluminum to mammo target/filter strings to match -- thanks to DJ Platten for strings
* `#43`_   Mammography and Philips CT import and export now more robust for images with missing information such as accession number and collimated field size
* `#42`_   Documentation updated to reflect `#37`_
* `#37`_   Studies now sort by time and date


0.3.7 (2014-02-25)
------------------

* `#40`_   Restyled the filter section in the web interface and added a title to that section
* `#38`_   Column titles tidied up in Excel exports
* `#36`_   openrem_ptsizecsv output of log now depends on verbose flag
* `#35`_   Numbers no longer stored as text in Excel exports

0.3.6 (2014-02-24)
------------------

* `#34`_   Localised scripts that were on remote web servers in default Bootstrap code
* `#33`_   Documentation now exists for adding data via csv file
* `#24`_   Web interface has been upgraded to Bootstrap v3
* `#5`_    Web interface and export function now have some documentation with screenshots


0.3.5-rc2 (2014-02-17)
----------------------

* `#32`_   Missing sys import bug prevented new patient size import from working

0.3.5 (2014-02-17)
------------------

* --    Prettified this document!
* `#31`_   Promoted patient size import from csv function to the scripts folder so it will install and can be called from the path
* `#30`_   Improved patient size import from csv to allow for arbitary column titles and study instance UID in addition to accession number.
* `#29`_   Corrected the docs URL in the readme

0.3.4-rc2 (2014-02-14)
----------------------

* `#28`_   XLSX export crashed if any of the filter fields were missing. Now fills on import with 'None'
* `#27`_   Use requested procedure description if requested procedure code description is missing


0.3.4 (2014-02-14)
------------------

* --    General improvements and addition of logo to docs
* `#23`_   Added Windows XP MySQL backup guide to docs
* `#22`_   Added running Conquest as a Windows XP service to docs
* `#15`_   Added version number and copyright information to xlsx exports
* `#14`_   Added version number to the web interface
* `#13`_   Improve the docs with respect to South database migrations


0.3.3-r2 (2014-02-04)
---------------------

* `#12`_   Added this version history
* `#11`_   Documentation is no longer included in the tar.gz install file -- see http://openrem.trfd.org instead

0.3.3 (2014-02-01)
------------------

..      Note::

        Installs of OpenREM earlier than 0.3.3 will break on upgrade if the scripts are called from other programs.
        For example openrem_rdsr is now called openrem_rdsr.py

* --    Added warning of upgrade breaking existing installs to docs
* `#10`_   Added .py suffix to the scripts to allow them to be executed on Windows (thanks to DJ Platten)
* `#8`_    Removed superfluous '/' in base html file, harmless on linux, prevented Windows loading stylesheets (thanks to DJ Platten)
* `#7`_    Added windows and linux path examples for test SQLite database creation
* `#6`_    Corrected renaming of example files installation instruction (thanks to DJ Platten)
* `#4`_    Added some text to the documentation relating to importing files to OpenREM
* `#3`_    Corrected copyright notice in documentation


0.3.2 (2014-01-29)
------------------

*       Initial version uploaded to bitbucket.org

..  _`#800`: https://bitbucket.org/openrem/openrem/issue/800/
..  _`#799`: https://bitbucket.org/openrem/openrem/issue/799/
..  _`#798`: https://bitbucket.org/openrem/openrem/issue/798/
..  _`#797`: https://bitbucket.org/openrem/openrem/issue/797/
..  _`#796`: https://bitbucket.org/openrem/openrem/issue/796/
..  _`#795`: https://bitbucket.org/openrem/openrem/issue/795/
..  _`#794`: https://bitbucket.org/openrem/openrem/issue/794/
..  _`#793`: https://bitbucket.org/openrem/openrem/issue/793/
..  _`#792`: https://bitbucket.org/openrem/openrem/issue/792/
..  _`#791`: https://bitbucket.org/openrem/openrem/issue/791/
..  _`#790`: https://bitbucket.org/openrem/openrem/issue/790/
..  _`#789`: https://bitbucket.org/openrem/openrem/issue/789/
..  _`#788`: https://bitbucket.org/openrem/openrem/issue/788/
..  _`#787`: https://bitbucket.org/openrem/openrem/issue/787/
..  _`#786`: https://bitbucket.org/openrem/openrem/issue/786/
..  _`#785`: https://bitbucket.org/openrem/openrem/issue/785/
..  _`#784`: https://bitbucket.org/openrem/openrem/issue/784/
..  _`#783`: https://bitbucket.org/openrem/openrem/issue/783/
..  _`#782`: https://bitbucket.org/openrem/openrem/issue/782/
..  _`#781`: https://bitbucket.org/openrem/openrem/issue/781/
..  _`#780`: https://bitbucket.org/openrem/openrem/issue/780/
..  _`#779`: https://bitbucket.org/openrem/openrem/issue/779/
..  _`#778`: https://bitbucket.org/openrem/openrem/issue/778/
..  _`#777`: https://bitbucket.org/openrem/openrem/issue/777/
..  _`#776`: https://bitbucket.org/openrem/openrem/issue/776/
..  _`#775`: https://bitbucket.org/openrem/openrem/issue/775/
..  _`#774`: https://bitbucket.org/openrem/openrem/issue/774/
..  _`#773`: https://bitbucket.org/openrem/openrem/issue/773/
..  _`#772`: https://bitbucket.org/openrem/openrem/issue/772/
..  _`#771`: https://bitbucket.org/openrem/openrem/issue/771/
..  _`#770`: https://bitbucket.org/openrem/openrem/issue/770/
..  _`#769`: https://bitbucket.org/openrem/openrem/issue/769/
..  _`#768`: https://bitbucket.org/openrem/openrem/issue/768/
..  _`#767`: https://bitbucket.org/openrem/openrem/issue/767/
..  _`#766`: https://bitbucket.org/openrem/openrem/issue/766/
..  _`#765`: https://bitbucket.org/openrem/openrem/issue/765/
..  _`#764`: https://bitbucket.org/openrem/openrem/issue/764/
..  _`#763`: https://bitbucket.org/openrem/openrem/issue/763/
..  _`#762`: https://bitbucket.org/openrem/openrem/issue/762/
..  _`#761`: https://bitbucket.org/openrem/openrem/issue/761/
..  _`#760`: https://bitbucket.org/openrem/openrem/issue/760/
..  _`#759`: https://bitbucket.org/openrem/openrem/issue/759/
..  _`#758`: https://bitbucket.org/openrem/openrem/issue/758/
..  _`#757`: https://bitbucket.org/openrem/openrem/issue/757/
..  _`#756`: https://bitbucket.org/openrem/openrem/issue/756/
..  _`#755`: https://bitbucket.org/openrem/openrem/issue/755/
..  _`#754`: https://bitbucket.org/openrem/openrem/issue/754/
..  _`#753`: https://bitbucket.org/openrem/openrem/issue/753/
..  _`#752`: https://bitbucket.org/openrem/openrem/issue/752/
..  _`#751`: https://bitbucket.org/openrem/openrem/issue/751/
..  _`#750`: https://bitbucket.org/openrem/openrem/issue/750/
..  _`#749`: https://bitbucket.org/openrem/openrem/issue/749/
..  _`#748`: https://bitbucket.org/openrem/openrem/issue/748/
..  _`#747`: https://bitbucket.org/openrem/openrem/issue/747/
..  _`#746`: https://bitbucket.org/openrem/openrem/issue/746/
..  _`#745`: https://bitbucket.org/openrem/openrem/issue/745/
..  _`#744`: https://bitbucket.org/openrem/openrem/issue/744/
..  _`#743`: https://bitbucket.org/openrem/openrem/issue/743/
..  _`#742`: https://bitbucket.org/openrem/openrem/issue/742/
..  _`#741`: https://bitbucket.org/openrem/openrem/issue/741/
..  _`#740`: https://bitbucket.org/openrem/openrem/issue/740/
..  _`#739`: https://bitbucket.org/openrem/openrem/issue/739/
..  _`#738`: https://bitbucket.org/openrem/openrem/issue/738/
..  _`#737`: https://bitbucket.org/openrem/openrem/issue/737/
..  _`#736`: https://bitbucket.org/openrem/openrem/issue/736/
..  _`#735`: https://bitbucket.org/openrem/openrem/issue/735/
..  _`#734`: https://bitbucket.org/openrem/openrem/issue/734/
..  _`#733`: https://bitbucket.org/openrem/openrem/issue/733/
..  _`#732`: https://bitbucket.org/openrem/openrem/issue/732/
..  _`#731`: https://bitbucket.org/openrem/openrem/issue/731/
..  _`#730`: https://bitbucket.org/openrem/openrem/issue/730/
..  _`#729`: https://bitbucket.org/openrem/openrem/issue/729/
..  _`#728`: https://bitbucket.org/openrem/openrem/issue/728/
..  _`#727`: https://bitbucket.org/openrem/openrem/issue/727/
..  _`#726`: https://bitbucket.org/openrem/openrem/issue/726/
..  _`#725`: https://bitbucket.org/openrem/openrem/issue/725/
..  _`#724`: https://bitbucket.org/openrem/openrem/issue/724/
..  _`#723`: https://bitbucket.org/openrem/openrem/issue/723/
..  _`#722`: https://bitbucket.org/openrem/openrem/issue/722/
..  _`#721`: https://bitbucket.org/openrem/openrem/issue/721/
..  _`#720`: https://bitbucket.org/openrem/openrem/issue/720/
..  _`#719`: https://bitbucket.org/openrem/openrem/issue/719/
..  _`#718`: https://bitbucket.org/openrem/openrem/issue/718/
..  _`#717`: https://bitbucket.org/openrem/openrem/issue/717/
..  _`#716`: https://bitbucket.org/openrem/openrem/issue/716/
..  _`#715`: https://bitbucket.org/openrem/openrem/issue/715/
..  _`#714`: https://bitbucket.org/openrem/openrem/issue/714/
..  _`#713`: https://bitbucket.org/openrem/openrem/issue/713/
..  _`#712`: https://bitbucket.org/openrem/openrem/issue/712/
..  _`#711`: https://bitbucket.org/openrem/openrem/issue/711/
..  _`#710`: https://bitbucket.org/openrem/openrem/issue/710/
..  _`#709`: https://bitbucket.org/openrem/openrem/issue/709/
..  _`#708`: https://bitbucket.org/openrem/openrem/issue/708/
..  _`#707`: https://bitbucket.org/openrem/openrem/issue/707/
..  _`#706`: https://bitbucket.org/openrem/openrem/issue/706/
..  _`#705`: https://bitbucket.org/openrem/openrem/issue/705/
..  _`#704`: https://bitbucket.org/openrem/openrem/issue/704/
..  _`#703`: https://bitbucket.org/openrem/openrem/issue/703/
..  _`#702`: https://bitbucket.org/openrem/openrem/issue/702/
..  _`#701`: https://bitbucket.org/openrem/openrem/issue/701/
..  _`#700`: https://bitbucket.org/openrem/openrem/issue/700/
..  _`#699`: https://bitbucket.org/openrem/openrem/issue/699/
..  _`#698`: https://bitbucket.org/openrem/openrem/issue/698/
..  _`#697`: https://bitbucket.org/openrem/openrem/issue/697/
..  _`#696`: https://bitbucket.org/openrem/openrem/issue/696/
..  _`#695`: https://bitbucket.org/openrem/openrem/issue/695/
..  _`#694`: https://bitbucket.org/openrem/openrem/issue/694/
..  _`#693`: https://bitbucket.org/openrem/openrem/issue/693/
..  _`#692`: https://bitbucket.org/openrem/openrem/issue/692/
..  _`#691`: https://bitbucket.org/openrem/openrem/issue/691/
..  _`#690`: https://bitbucket.org/openrem/openrem/issue/690/
..  _`#689`: https://bitbucket.org/openrem/openrem/issue/689/
..  _`#688`: https://bitbucket.org/openrem/openrem/issue/688/
..  _`#687`: https://bitbucket.org/openrem/openrem/issue/687/
..  _`#686`: https://bitbucket.org/openrem/openrem/issue/686/
..  _`#685`: https://bitbucket.org/openrem/openrem/issue/685/
..  _`#684`: https://bitbucket.org/openrem/openrem/issue/684/
..  _`#683`: https://bitbucket.org/openrem/openrem/issue/683/
..  _`#682`: https://bitbucket.org/openrem/openrem/issue/682/
..  _`#681`: https://bitbucket.org/openrem/openrem/issue/681/
..  _`#680`: https://bitbucket.org/openrem/openrem/issue/680/
..  _`#679`: https://bitbucket.org/openrem/openrem/issue/679/
..  _`#678`: https://bitbucket.org/openrem/openrem/issue/678/
..  _`#677`: https://bitbucket.org/openrem/openrem/issue/677/
..  _`#676`: https://bitbucket.org/openrem/openrem/issue/676/
..  _`#675`: https://bitbucket.org/openrem/openrem/issue/675/
..  _`#674`: https://bitbucket.org/openrem/openrem/issue/674/
..  _`#673`: https://bitbucket.org/openrem/openrem/issue/673/
..  _`#672`: https://bitbucket.org/openrem/openrem/issue/672/
..  _`#671`: https://bitbucket.org/openrem/openrem/issue/671/
..  _`#670`: https://bitbucket.org/openrem/openrem/issue/670/
..  _`#669`: https://bitbucket.org/openrem/openrem/issue/669/
..  _`#668`: https://bitbucket.org/openrem/openrem/issue/668/
..  _`#667`: https://bitbucket.org/openrem/openrem/issue/667/
..  _`#666`: https://bitbucket.org/openrem/openrem/issue/666/
..  _`#665`: https://bitbucket.org/openrem/openrem/issue/665/
..  _`#664`: https://bitbucket.org/openrem/openrem/issue/664/
..  _`#663`: https://bitbucket.org/openrem/openrem/issue/663/
..  _`#662`: https://bitbucket.org/openrem/openrem/issue/662/
..  _`#661`: https://bitbucket.org/openrem/openrem/issue/661/
..  _`#660`: https://bitbucket.org/openrem/openrem/issue/660/
..  _`#659`: https://bitbucket.org/openrem/openrem/issue/659/
..  _`#658`: https://bitbucket.org/openrem/openrem/issue/658/
..  _`#657`: https://bitbucket.org/openrem/openrem/issue/657/
..  _`#656`: https://bitbucket.org/openrem/openrem/issue/656/
..  _`#655`: https://bitbucket.org/openrem/openrem/issue/655/
..  _`#654`: https://bitbucket.org/openrem/openrem/issue/654/
..  _`#653`: https://bitbucket.org/openrem/openrem/issue/653/
..  _`#652`: https://bitbucket.org/openrem/openrem/issue/652/
..  _`#651`: https://bitbucket.org/openrem/openrem/issue/651/
..  _`#650`: https://bitbucket.org/openrem/openrem/issue/650/
..  _`#649`: https://bitbucket.org/openrem/openrem/issue/649/
..  _`#648`: https://bitbucket.org/openrem/openrem/issue/648/
..  _`#647`: https://bitbucket.org/openrem/openrem/issue/647/
..  _`#646`: https://bitbucket.org/openrem/openrem/issue/646/
..  _`#645`: https://bitbucket.org/openrem/openrem/issue/645/
..  _`#644`: https://bitbucket.org/openrem/openrem/issue/644/
..  _`#643`: https://bitbucket.org/openrem/openrem/issue/643/
..  _`#642`: https://bitbucket.org/openrem/openrem/issue/642/
..  _`#641`: https://bitbucket.org/openrem/openrem/issue/641/
..  _`#640`: https://bitbucket.org/openrem/openrem/issue/640/
..  _`#639`: https://bitbucket.org/openrem/openrem/issue/639/
..  _`#638`: https://bitbucket.org/openrem/openrem/issue/638/
..  _`#637`: https://bitbucket.org/openrem/openrem/issue/637/
..  _`#636`: https://bitbucket.org/openrem/openrem/issue/636/
..  _`#635`: https://bitbucket.org/openrem/openrem/issue/635/
..  _`#634`: https://bitbucket.org/openrem/openrem/issue/634/
..  _`#633`: https://bitbucket.org/openrem/openrem/issue/633/
..  _`#632`: https://bitbucket.org/openrem/openrem/issue/632/
..  _`#631`: https://bitbucket.org/openrem/openrem/issue/631/
..  _`#630`: https://bitbucket.org/openrem/openrem/issue/630/
..  _`#629`: https://bitbucket.org/openrem/openrem/issue/629/
..  _`#628`: https://bitbucket.org/openrem/openrem/issue/628/
..  _`#627`: https://bitbucket.org/openrem/openrem/issue/627/
..  _`#626`: https://bitbucket.org/openrem/openrem/issue/626/
..  _`#625`: https://bitbucket.org/openrem/openrem/issue/625/
..  _`#624`: https://bitbucket.org/openrem/openrem/issue/624/
..  _`#623`: https://bitbucket.org/openrem/openrem/issue/623/
..  _`#622`: https://bitbucket.org/openrem/openrem/issue/622/
..  _`#621`: https://bitbucket.org/openrem/openrem/issue/621/
..  _`#620`: https://bitbucket.org/openrem/openrem/issue/620/
..  _`#619`: https://bitbucket.org/openrem/openrem/issue/619/
..  _`#618`: https://bitbucket.org/openrem/openrem/issue/618/
..  _`#617`: https://bitbucket.org/openrem/openrem/issue/617/
..  _`#616`: https://bitbucket.org/openrem/openrem/issue/616/
..  _`#615`: https://bitbucket.org/openrem/openrem/issue/615/
..  _`#614`: https://bitbucket.org/openrem/openrem/issue/614/
..  _`#613`: https://bitbucket.org/openrem/openrem/issue/613/
..  _`#612`: https://bitbucket.org/openrem/openrem/issue/612/
..  _`#611`: https://bitbucket.org/openrem/openrem/issue/611/
..  _`#610`: https://bitbucket.org/openrem/openrem/issue/610/
..  _`#609`: https://bitbucket.org/openrem/openrem/issue/609/
..  _`#608`: https://bitbucket.org/openrem/openrem/issue/608/
..  _`#607`: https://bitbucket.org/openrem/openrem/issue/607/
..  _`#606`: https://bitbucket.org/openrem/openrem/issue/606/
..  _`#605`: https://bitbucket.org/openrem/openrem/issue/605/
..  _`#604`: https://bitbucket.org/openrem/openrem/issue/604/
..  _`#603`: https://bitbucket.org/openrem/openrem/issue/603/
..  _`#602`: https://bitbucket.org/openrem/openrem/issue/602/
..  _`#601`: https://bitbucket.org/openrem/openrem/issue/601/
..  _`#600`: https://bitbucket.org/openrem/openrem/issue/600/
..  _`#599`: https://bitbucket.org/openrem/openrem/issue/599/
..  _`#598`: https://bitbucket.org/openrem/openrem/issue/598/
..  _`#597`: https://bitbucket.org/openrem/openrem/issue/597/
..  _`#596`: https://bitbucket.org/openrem/openrem/issue/596/
..  _`#595`: https://bitbucket.org/openrem/openrem/issue/595/
..  _`#594`: https://bitbucket.org/openrem/openrem/issue/594/
..  _`#593`: https://bitbucket.org/openrem/openrem/issue/593/
..  _`#592`: https://bitbucket.org/openrem/openrem/issue/592/
..  _`#591`: https://bitbucket.org/openrem/openrem/issue/591/
..  _`#590`: https://bitbucket.org/openrem/openrem/issue/590/
..  _`#589`: https://bitbucket.org/openrem/openrem/issue/589/
..  _`#588`: https://bitbucket.org/openrem/openrem/issue/588/
..  _`#587`: https://bitbucket.org/openrem/openrem/issue/587/
..  _`#586`: https://bitbucket.org/openrem/openrem/issue/586/
..  _`#585`: https://bitbucket.org/openrem/openrem/issue/585/
..  _`#584`: https://bitbucket.org/openrem/openrem/issue/584/
..  _`#583`: https://bitbucket.org/openrem/openrem/issue/583/
..  _`#582`: https://bitbucket.org/openrem/openrem/issue/582/
..  _`#581`: https://bitbucket.org/openrem/openrem/issue/581/
..  _`#580`: https://bitbucket.org/openrem/openrem/issue/580/
..  _`#579`: https://bitbucket.org/openrem/openrem/issue/579/
..  _`#578`: https://bitbucket.org/openrem/openrem/issue/578/
..  _`#577`: https://bitbucket.org/openrem/openrem/issue/577/
..  _`#576`: https://bitbucket.org/openrem/openrem/issue/576/
..  _`#575`: https://bitbucket.org/openrem/openrem/issue/575/
..  _`#574`: https://bitbucket.org/openrem/openrem/issue/574/
..  _`#573`: https://bitbucket.org/openrem/openrem/issue/573/
..  _`#572`: https://bitbucket.org/openrem/openrem/issue/572/
..  _`#571`: https://bitbucket.org/openrem/openrem/issue/571/
..  _`#570`: https://bitbucket.org/openrem/openrem/issue/570/
..  _`#569`: https://bitbucket.org/openrem/openrem/issue/569/
..  _`#568`: https://bitbucket.org/openrem/openrem/issue/568/
..  _`#567`: https://bitbucket.org/openrem/openrem/issue/567/
..  _`#566`: https://bitbucket.org/openrem/openrem/issue/566/
..  _`#565`: https://bitbucket.org/openrem/openrem/issue/565/
..  _`#564`: https://bitbucket.org/openrem/openrem/issue/564/
..  _`#563`: https://bitbucket.org/openrem/openrem/issue/563/
..  _`#562`: https://bitbucket.org/openrem/openrem/issue/562/
..  _`#561`: https://bitbucket.org/openrem/openrem/issue/561/
..  _`#560`: https://bitbucket.org/openrem/openrem/issue/560/
..  _`#559`: https://bitbucket.org/openrem/openrem/issue/559/
..  _`#558`: https://bitbucket.org/openrem/openrem/issue/558/
..  _`#557`: https://bitbucket.org/openrem/openrem/issue/557/
..  _`#556`: https://bitbucket.org/openrem/openrem/issue/556/
..  _`#555`: https://bitbucket.org/openrem/openrem/issue/555/
..  _`#554`: https://bitbucket.org/openrem/openrem/issue/554/
..  _`#553`: https://bitbucket.org/openrem/openrem/issue/553/
..  _`#552`: https://bitbucket.org/openrem/openrem/issue/552/
..  _`#551`: https://bitbucket.org/openrem/openrem/issue/551/
..  _`#550`: https://bitbucket.org/openrem/openrem/issue/550/
..  _`#549`: https://bitbucket.org/openrem/openrem/issue/549/
..  _`#548`: https://bitbucket.org/openrem/openrem/issue/548/
..  _`#547`: https://bitbucket.org/openrem/openrem/issue/547/
..  _`#546`: https://bitbucket.org/openrem/openrem/issue/546/
..  _`#545`: https://bitbucket.org/openrem/openrem/issue/545/
..  _`#544`: https://bitbucket.org/openrem/openrem/issue/544/
..  _`#543`: https://bitbucket.org/openrem/openrem/issue/543/
..  _`#542`: https://bitbucket.org/openrem/openrem/issue/542/
..  _`#541`: https://bitbucket.org/openrem/openrem/issue/541/
..  _`#540`: https://bitbucket.org/openrem/openrem/issue/540/
..  _`#539`: https://bitbucket.org/openrem/openrem/issue/539/
..  _`#538`: https://bitbucket.org/openrem/openrem/issue/538/
..  _`#537`: https://bitbucket.org/openrem/openrem/issue/537/
..  _`#536`: https://bitbucket.org/openrem/openrem/issue/536/
..  _`#535`: https://bitbucket.org/openrem/openrem/issue/535/
..  _`#534`: https://bitbucket.org/openrem/openrem/issue/534/
..  _`#533`: https://bitbucket.org/openrem/openrem/issue/533/
..  _`#532`: https://bitbucket.org/openrem/openrem/issue/532/
..  _`#531`: https://bitbucket.org/openrem/openrem/issue/531/
..  _`#530`: https://bitbucket.org/openrem/openrem/issue/530/
..  _`#529`: https://bitbucket.org/openrem/openrem/issue/529/
..  _`#528`: https://bitbucket.org/openrem/openrem/issue/528/
..  _`#527`: https://bitbucket.org/openrem/openrem/issue/527/
..  _`#526`: https://bitbucket.org/openrem/openrem/issue/526/
..  _`#525`: https://bitbucket.org/openrem/openrem/issue/525/
..  _`#524`: https://bitbucket.org/openrem/openrem/issue/524/
..  _`#523`: https://bitbucket.org/openrem/openrem/issue/523/
..  _`#522`: https://bitbucket.org/openrem/openrem/issue/522/
..  _`#521`: https://bitbucket.org/openrem/openrem/issue/521/
..  _`#520`: https://bitbucket.org/openrem/openrem/issue/520/
..  _`#519`: https://bitbucket.org/openrem/openrem/issue/519/
..  _`#518`: https://bitbucket.org/openrem/openrem/issue/518/
..  _`#517`: https://bitbucket.org/openrem/openrem/issue/517/
..  _`#516`: https://bitbucket.org/openrem/openrem/issue/516/
..  _`#515`: https://bitbucket.org/openrem/openrem/issue/515/
..  _`#514`: https://bitbucket.org/openrem/openrem/issue/514/
..  _`#513`: https://bitbucket.org/openrem/openrem/issue/513/
..  _`#512`: https://bitbucket.org/openrem/openrem/issue/512/
..  _`#511`: https://bitbucket.org/openrem/openrem/issue/511/
..  _`#510`: https://bitbucket.org/openrem/openrem/issue/510/
..  _`#509`: https://bitbucket.org/openrem/openrem/issue/509/
..  _`#508`: https://bitbucket.org/openrem/openrem/issue/508/
..  _`#507`: https://bitbucket.org/openrem/openrem/issue/507/
..  _`#506`: https://bitbucket.org/openrem/openrem/issue/506/
..  _`#505`: https://bitbucket.org/openrem/openrem/issue/505/
..  _`#504`: https://bitbucket.org/openrem/openrem/issue/504/
..  _`#503`: https://bitbucket.org/openrem/openrem/issue/503/
..  _`#502`: https://bitbucket.org/openrem/openrem/issue/502/
..  _`#501`: https://bitbucket.org/openrem/openrem/issue/501/
..  _`#500`: https://bitbucket.org/openrem/openrem/issue/500/
..  _`#499`: https://bitbucket.org/openrem/openrem/issue/499/
..  _`#498`: https://bitbucket.org/openrem/openrem/issue/498/
..  _`#497`: https://bitbucket.org/openrem/openrem/issue/497/
..  _`#496`: https://bitbucket.org/openrem/openrem/issue/496/
..  _`#495`: https://bitbucket.org/openrem/openrem/issue/495/
..  _`#494`: https://bitbucket.org/openrem/openrem/issue/494/
..  _`#493`: https://bitbucket.org/openrem/openrem/issue/493/
..  _`#492`: https://bitbucket.org/openrem/openrem/issue/492/
..  _`#491`: https://bitbucket.org/openrem/openrem/issue/491/
..  _`#490`: https://bitbucket.org/openrem/openrem/issue/490/
..  _`#489`: https://bitbucket.org/openrem/openrem/issue/489/
..  _`#488`: https://bitbucket.org/openrem/openrem/issue/488/
..  _`#487`: https://bitbucket.org/openrem/openrem/issue/487/
..  _`#486`: https://bitbucket.org/openrem/openrem/issue/486/
..  _`#485`: https://bitbucket.org/openrem/openrem/issue/485/
..  _`#484`: https://bitbucket.org/openrem/openrem/issue/484/
..  _`#483`: https://bitbucket.org/openrem/openrem/issue/483/
..  _`#482`: https://bitbucket.org/openrem/openrem/issue/482/
..  _`#481`: https://bitbucket.org/openrem/openrem/issue/481/
..  _`#480`: https://bitbucket.org/openrem/openrem/issue/480/
..  _`#479`: https://bitbucket.org/openrem/openrem/issue/479/
..  _`#478`: https://bitbucket.org/openrem/openrem/issue/478/
..  _`#477`: https://bitbucket.org/openrem/openrem/issue/477/
..  _`#476`: https://bitbucket.org/openrem/openrem/issue/476/
..  _`#475`: https://bitbucket.org/openrem/openrem/issue/475/
..  _`#474`: https://bitbucket.org/openrem/openrem/issue/474/
..  _`#473`: https://bitbucket.org/openrem/openrem/issue/473/
..  _`#472`: https://bitbucket.org/openrem/openrem/issue/472/
..  _`#471`: https://bitbucket.org/openrem/openrem/issue/471/
..  _`#470`: https://bitbucket.org/openrem/openrem/issue/470/
..  _`#469`: https://bitbucket.org/openrem/openrem/issue/469/
..  _`#468`: https://bitbucket.org/openrem/openrem/issue/468/
..  _`#467`: https://bitbucket.org/openrem/openrem/issue/467/
..  _`#466`: https://bitbucket.org/openrem/openrem/issue/466/
..  _`#465`: https://bitbucket.org/openrem/openrem/issue/465/
..  _`#464`: https://bitbucket.org/openrem/openrem/issue/464/
..  _`#463`: https://bitbucket.org/openrem/openrem/issue/463/
..  _`#462`: https://bitbucket.org/openrem/openrem/issue/462/
..  _`#461`: https://bitbucket.org/openrem/openrem/issue/461/
..  _`#460`: https://bitbucket.org/openrem/openrem/issue/460/
..  _`#459`: https://bitbucket.org/openrem/openrem/issue/459/
..  _`#458`: https://bitbucket.org/openrem/openrem/issue/458/
..  _`#457`: https://bitbucket.org/openrem/openrem/issue/457/
..  _`#456`: https://bitbucket.org/openrem/openrem/issue/456/
..  _`#455`: https://bitbucket.org/openrem/openrem/issue/455/
..  _`#454`: https://bitbucket.org/openrem/openrem/issue/454/
..  _`#453`: https://bitbucket.org/openrem/openrem/issue/453/
..  _`#452`: https://bitbucket.org/openrem/openrem/issue/452/
..  _`#451`: https://bitbucket.org/openrem/openrem/issue/451/
..  _`#450`: https://bitbucket.org/openrem/openrem/issue/450/
..  _`#449`: https://bitbucket.org/openrem/openrem/issue/449/
..  _`#448`: https://bitbucket.org/openrem/openrem/issue/448/
..  _`#447`: https://bitbucket.org/openrem/openrem/issue/447/
..  _`#446`: https://bitbucket.org/openrem/openrem/issue/446/
..  _`#445`: https://bitbucket.org/openrem/openrem/issue/445/
..  _`#444`: https://bitbucket.org/openrem/openrem/issue/444/
..  _`#443`: https://bitbucket.org/openrem/openrem/issue/443/
..  _`#442`: https://bitbucket.org/openrem/openrem/issue/442/
..  _`#441`: https://bitbucket.org/openrem/openrem/issue/441/
..  _`#440`: https://bitbucket.org/openrem/openrem/issue/440/
..  _`#439`: https://bitbucket.org/openrem/openrem/issue/439/
..  _`#438`: https://bitbucket.org/openrem/openrem/issue/438/
..  _`#437`: https://bitbucket.org/openrem/openrem/issue/437/
..  _`#436`: https://bitbucket.org/openrem/openrem/issue/436/
..  _`#435`: https://bitbucket.org/openrem/openrem/issue/435/
..  _`#434`: https://bitbucket.org/openrem/openrem/issue/434/
..  _`#433`: https://bitbucket.org/openrem/openrem/issue/433/
..  _`#432`: https://bitbucket.org/openrem/openrem/issue/432/
..  _`#431`: https://bitbucket.org/openrem/openrem/issue/431/
..  _`#430`: https://bitbucket.org/openrem/openrem/issue/430/
..  _`#429`: https://bitbucket.org/openrem/openrem/issue/429/
..  _`#428`: https://bitbucket.org/openrem/openrem/issue/428/
..  _`#427`: https://bitbucket.org/openrem/openrem/issue/427/
..  _`#426`: https://bitbucket.org/openrem/openrem/issue/426/
..  _`#425`: https://bitbucket.org/openrem/openrem/issue/425/
..  _`#424`: https://bitbucket.org/openrem/openrem/issue/424/
..  _`#423`: https://bitbucket.org/openrem/openrem/issue/423/
..  _`#422`: https://bitbucket.org/openrem/openrem/issue/422/
..  _`#421`: https://bitbucket.org/openrem/openrem/issue/421/
..  _`#420`: https://bitbucket.org/openrem/openrem/issue/420/
..  _`#419`: https://bitbucket.org/openrem/openrem/issue/419/
..  _`#418`: https://bitbucket.org/openrem/openrem/issue/418/
..  _`#417`: https://bitbucket.org/openrem/openrem/issue/417/
..  _`#416`: https://bitbucket.org/openrem/openrem/issue/416/
..  _`#415`: https://bitbucket.org/openrem/openrem/issue/415/
..  _`#414`: https://bitbucket.org/openrem/openrem/issue/414/
..  _`#413`: https://bitbucket.org/openrem/openrem/issue/413/
..  _`#412`: https://bitbucket.org/openrem/openrem/issue/412/
..  _`#411`: https://bitbucket.org/openrem/openrem/issue/411/
..  _`#410`: https://bitbucket.org/openrem/openrem/issue/410/
..  _`#409`: https://bitbucket.org/openrem/openrem/issue/409/
..  _`#408`: https://bitbucket.org/openrem/openrem/issue/408/
..  _`#407`: https://bitbucket.org/openrem/openrem/issue/407/
..  _`#406`: https://bitbucket.org/openrem/openrem/issue/406/
..  _`#405`: https://bitbucket.org/openrem/openrem/issue/405/
..  _`#404`: https://bitbucket.org/openrem/openrem/issue/404/
..  _`#403`: https://bitbucket.org/openrem/openrem/issue/403/
..  _`#402`: https://bitbucket.org/openrem/openrem/issue/402/
..  _`#401`: https://bitbucket.org/openrem/openrem/issue/401/
..  _`#400`: https://bitbucket.org/openrem/openrem/issue/400/
..  _`#399`: https://bitbucket.org/openrem/openrem/issue/399/
..  _`#398`: https://bitbucket.org/openrem/openrem/issue/398/
..  _`#397`: https://bitbucket.org/openrem/openrem/issue/397/
..  _`#396`: https://bitbucket.org/openrem/openrem/issue/396/
..  _`#395`: https://bitbucket.org/openrem/openrem/issue/395/
..  _`#394`: https://bitbucket.org/openrem/openrem/issue/394/
..  _`#393`: https://bitbucket.org/openrem/openrem/issue/393/
..  _`#392`: https://bitbucket.org/openrem/openrem/issue/392/
..  _`#391`: https://bitbucket.org/openrem/openrem/issue/391/
..  _`#390`: https://bitbucket.org/openrem/openrem/issue/390/
..  _`#389`: https://bitbucket.org/openrem/openrem/issue/389/
..  _`#388`: https://bitbucket.org/openrem/openrem/issue/388/
..  _`#387`: https://bitbucket.org/openrem/openrem/issue/387/
..  _`#386`: https://bitbucket.org/openrem/openrem/issue/386/
..  _`#385`: https://bitbucket.org/openrem/openrem/issue/385/
..  _`#384`: https://bitbucket.org/openrem/openrem/issue/384/
..  _`#383`: https://bitbucket.org/openrem/openrem/issue/383/
..  _`#382`: https://bitbucket.org/openrem/openrem/issue/382/
..  _`#381`: https://bitbucket.org/openrem/openrem/issue/381/
..  _`#380`: https://bitbucket.org/openrem/openrem/issue/380/
..  _`#379`: https://bitbucket.org/openrem/openrem/issue/379/
..  _`#378`: https://bitbucket.org/openrem/openrem/issue/378/
..  _`#377`: https://bitbucket.org/openrem/openrem/issue/377/
..  _`#376`: https://bitbucket.org/openrem/openrem/issue/376/
..  _`#375`: https://bitbucket.org/openrem/openrem/issue/375/
..  _`#374`: https://bitbucket.org/openrem/openrem/issue/374/
..  _`#373`: https://bitbucket.org/openrem/openrem/issue/373/
..  _`#372`: https://bitbucket.org/openrem/openrem/issue/372/
..  _`#371`: https://bitbucket.org/openrem/openrem/issue/371/
..  _`#370`: https://bitbucket.org/openrem/openrem/issue/370/
..  _`#369`: https://bitbucket.org/openrem/openrem/issue/369/
..  _`#368`: https://bitbucket.org/openrem/openrem/issue/368/
..  _`#367`: https://bitbucket.org/openrem/openrem/issue/367/
..  _`#366`: https://bitbucket.org/openrem/openrem/issue/366/
..  _`#365`: https://bitbucket.org/openrem/openrem/issue/365/
..  _`#364`: https://bitbucket.org/openrem/openrem/issue/364/
..  _`#363`: https://bitbucket.org/openrem/openrem/issue/363/
..  _`#362`: https://bitbucket.org/openrem/openrem/issue/362/
..  _`#361`: https://bitbucket.org/openrem/openrem/issue/361/
..  _`#360`: https://bitbucket.org/openrem/openrem/issue/360/
..  _`#359`: https://bitbucket.org/openrem/openrem/issue/359/
..  _`#358`: https://bitbucket.org/openrem/openrem/issue/358/
..  _`#357`: https://bitbucket.org/openrem/openrem/issue/357/
..  _`#356`: https://bitbucket.org/openrem/openrem/issue/356/
..  _`#355`: https://bitbucket.org/openrem/openrem/issue/355/
..  _`#354`: https://bitbucket.org/openrem/openrem/issue/354/
..  _`#353`: https://bitbucket.org/openrem/openrem/issue/353/
..  _`#352`: https://bitbucket.org/openrem/openrem/issue/352/
..  _`#351`: https://bitbucket.org/openrem/openrem/issue/351/
..  _`#350`: https://bitbucket.org/openrem/openrem/issue/350/
..  _`#349`: https://bitbucket.org/openrem/openrem/issue/349/
..  _`#348`: https://bitbucket.org/openrem/openrem/issue/348/
..  _`#347`: https://bitbucket.org/openrem/openrem/issue/347/
..  _`#346`: https://bitbucket.org/openrem/openrem/issue/346/
..  _`#345`: https://bitbucket.org/openrem/openrem/issue/345/
..  _`#344`: https://bitbucket.org/openrem/openrem/issue/344/
..  _`#343`: https://bitbucket.org/openrem/openrem/issue/343/
..  _`#342`: https://bitbucket.org/openrem/openrem/issue/342/
..  _`#341`: https://bitbucket.org/openrem/openrem/issue/341/
..  _`#340`: https://bitbucket.org/openrem/openrem/issue/340/
..  _`#339`: https://bitbucket.org/openrem/openrem/issue/339/
..  _`#338`: https://bitbucket.org/openrem/openrem/issue/338/
..  _`#337`: https://bitbucket.org/openrem/openrem/issue/337/
..  _`#336`: https://bitbucket.org/openrem/openrem/issue/336/
..  _`#335`: https://bitbucket.org/openrem/openrem/issue/335/
..  _`#334`: https://bitbucket.org/openrem/openrem/issue/334/
..  _`#333`: https://bitbucket.org/openrem/openrem/issue/333/
..  _`#332`: https://bitbucket.org/openrem/openrem/issue/332/
..  _`#331`: https://bitbucket.org/openrem/openrem/issue/331/
..  _`#330`: https://bitbucket.org/openrem/openrem/issue/330/
..  _`#329`: https://bitbucket.org/openrem/openrem/issue/329/
..  _`#328`: https://bitbucket.org/openrem/openrem/issue/328/
..  _`#327`: https://bitbucket.org/openrem/openrem/issue/327/
..  _`#326`: https://bitbucket.org/openrem/openrem/issue/326/
..  _`#325`: https://bitbucket.org/openrem/openrem/issue/325/
..  _`#324`: https://bitbucket.org/openrem/openrem/issue/324/
..  _`#323`: https://bitbucket.org/openrem/openrem/issue/323/
..  _`#322`: https://bitbucket.org/openrem/openrem/issue/322/
..  _`#321`: https://bitbucket.org/openrem/openrem/issue/321/
..  _`#320`: https://bitbucket.org/openrem/openrem/issue/320/
..  _`#319`: https://bitbucket.org/openrem/openrem/issue/319/
..  _`#318`: https://bitbucket.org/openrem/openrem/issue/318/
..  _`#317`: https://bitbucket.org/openrem/openrem/issue/317/
..  _`#316`: https://bitbucket.org/openrem/openrem/issue/316/
..  _`#315`: https://bitbucket.org/openrem/openrem/issue/315/
..  _`#314`: https://bitbucket.org/openrem/openrem/issue/314/
..  _`#313`: https://bitbucket.org/openrem/openrem/issue/313/
..  _`#312`: https://bitbucket.org/openrem/openrem/issue/312/
..  _`#311`: https://bitbucket.org/openrem/openrem/issue/311/
..  _`#310`: https://bitbucket.org/openrem/openrem/issue/310/
..  _`#309`: https://bitbucket.org/openrem/openrem/issue/309/
..  _`#308`: https://bitbucket.org/openrem/openrem/issue/308/
..  _`#307`: https://bitbucket.org/openrem/openrem/issue/307/
..  _`#306`: https://bitbucket.org/openrem/openrem/issue/306/
..  _`#305`: https://bitbucket.org/openrem/openrem/issue/305/
..  _`#304`: https://bitbucket.org/openrem/openrem/issue/304/
..  _`#303`: https://bitbucket.org/openrem/openrem/issue/303/
..  _`#302`: https://bitbucket.org/openrem/openrem/issue/302/
..  _`#301`: https://bitbucket.org/openrem/openrem/issue/301/
..  _`#300`: https://bitbucket.org/openrem/openrem/issue/300/
..  _`#299`: https://bitbucket.org/openrem/openrem/issue/299/
..  _`#298`: https://bitbucket.org/openrem/openrem/issue/298/
..  _`#297`: https://bitbucket.org/openrem/openrem/issue/297/
..  _`#296`: https://bitbucket.org/openrem/openrem/issue/296/
..  _`#295`: https://bitbucket.org/openrem/openrem/issue/295/
..  _`#294`: https://bitbucket.org/openrem/openrem/issue/294/
..  _`#293`: https://bitbucket.org/openrem/openrem/issue/293/
..  _`#292`: https://bitbucket.org/openrem/openrem/issue/292/
..  _`#291`: https://bitbucket.org/openrem/openrem/issue/291/
..  _`#290`: https://bitbucket.org/openrem/openrem/issue/290/
..  _`#289`: https://bitbucket.org/openrem/openrem/issue/289/
..  _`#288`: https://bitbucket.org/openrem/openrem/issue/288/
..  _`#287`: https://bitbucket.org/openrem/openrem/issue/287/
..  _`#286`: https://bitbucket.org/openrem/openrem/issue/286/
..  _`#285`: https://bitbucket.org/openrem/openrem/issue/285/
..  _`#284`: https://bitbucket.org/openrem/openrem/issue/284/
..  _`#283`: https://bitbucket.org/openrem/openrem/issue/283/
..  _`#282`: https://bitbucket.org/openrem/openrem/issue/282/
..  _`#281`: https://bitbucket.org/openrem/openrem/issue/281/
..  _`#280`: https://bitbucket.org/openrem/openrem/issue/280/
..  _`#279`: https://bitbucket.org/openrem/openrem/issue/279/
..  _`#278`: https://bitbucket.org/openrem/openrem/issue/278/
..  _`#277`: https://bitbucket.org/openrem/openrem/issue/277/
..  _`#276`: https://bitbucket.org/openrem/openrem/issue/276/
..  _`#275`: https://bitbucket.org/openrem/openrem/issue/275/
..  _`#274`: https://bitbucket.org/openrem/openrem/issue/274/
..  _`#273`: https://bitbucket.org/openrem/openrem/issue/273/
..  _`#272`: https://bitbucket.org/openrem/openrem/issue/272/
..  _`#271`: https://bitbucket.org/openrem/openrem/issue/271/
..  _`#270`: https://bitbucket.org/openrem/openrem/issue/270/
..  _`#269`: https://bitbucket.org/openrem/openrem/issue/269/
..  _`#268`: https://bitbucket.org/openrem/openrem/issue/268/
..  _`#267`: https://bitbucket.org/openrem/openrem/issue/267/
..  _`#266`: https://bitbucket.org/openrem/openrem/issue/266/
..  _`#265`: https://bitbucket.org/openrem/openrem/issue/265/
..  _`#264`: https://bitbucket.org/openrem/openrem/issue/264/
..  _`#263`: https://bitbucket.org/openrem/openrem/issue/263/
..  _`#262`: https://bitbucket.org/openrem/openrem/issue/262/
..  _`#261`: https://bitbucket.org/openrem/openrem/issue/261/
..  _`#260`: https://bitbucket.org/openrem/openrem/issue/260/
..  _`#259`: https://bitbucket.org/openrem/openrem/issue/259/
..  _`#258`: https://bitbucket.org/openrem/openrem/issue/258/
..  _`#257`: https://bitbucket.org/openrem/openrem/issue/257/
..  _`#256`: https://bitbucket.org/openrem/openrem/issue/256/
..  _`#255`: https://bitbucket.org/openrem/openrem/issue/255/
..  _`#254`: https://bitbucket.org/openrem/openrem/issue/254/
..  _`#253`: https://bitbucket.org/openrem/openrem/issue/253/
..  _`#252`: https://bitbucket.org/openrem/openrem/issue/252/
..  _`#251`: https://bitbucket.org/openrem/openrem/issue/251/
..  _`#250`: https://bitbucket.org/openrem/openrem/issue/250/
..  _`#249`: https://bitbucket.org/openrem/openrem/issue/249/
..  _`#248`: https://bitbucket.org/openrem/openrem/issue/248/
..  _`#247`: https://bitbucket.org/openrem/openrem/issue/247/
..  _`#246`: https://bitbucket.org/openrem/openrem/issue/246/
..  _`#245`: https://bitbucket.org/openrem/openrem/issue/245/
..  _`#244`: https://bitbucket.org/openrem/openrem/issue/244/
..  _`#243`: https://bitbucket.org/openrem/openrem/issue/243/
..  _`#242`: https://bitbucket.org/openrem/openrem/issue/242/
..  _`#241`: https://bitbucket.org/openrem/openrem/issue/241/
..  _`#240`: https://bitbucket.org/openrem/openrem/issue/240/
..  _`#239`: https://bitbucket.org/openrem/openrem/issue/239/
..  _`#238`: https://bitbucket.org/openrem/openrem/issue/238/
..  _`#237`: https://bitbucket.org/openrem/openrem/issue/237/
..  _`#236`: https://bitbucket.org/openrem/openrem/issue/236/
..  _`#235`: https://bitbucket.org/openrem/openrem/issue/235/
..  _`#234`: https://bitbucket.org/openrem/openrem/issue/234/
..  _`#233`: https://bitbucket.org/openrem/openrem/issue/233/
..  _`#232`: https://bitbucket.org/openrem/openrem/issue/232/
..  _`#231`: https://bitbucket.org/openrem/openrem/issue/231/
..  _`#230`: https://bitbucket.org/openrem/openrem/issue/230/
..  _`#229`: https://bitbucket.org/openrem/openrem/issue/229/
..  _`#228`: https://bitbucket.org/openrem/openrem/issue/228/
..  _`#227`: https://bitbucket.org/openrem/openrem/issue/227/
..  _`#226`: https://bitbucket.org/openrem/openrem/issue/226/
..  _`#225`: https://bitbucket.org/openrem/openrem/issue/225/
..  _`#224`: https://bitbucket.org/openrem/openrem/issue/224/
..  _`#223`: https://bitbucket.org/openrem/openrem/issue/223/
..  _`#222`: https://bitbucket.org/openrem/openrem/issue/222/
..  _`#221`: https://bitbucket.org/openrem/openrem/issue/221/
..  _`#220`: https://bitbucket.org/openrem/openrem/issue/220/
..  _`#219`: https://bitbucket.org/openrem/openrem/issue/219/
..  _`#218`: https://bitbucket.org/openrem/openrem/issue/218/
..  _`#217`: https://bitbucket.org/openrem/openrem/issue/217/
..  _`#216`: https://bitbucket.org/openrem/openrem/issue/216/
..  _`#215`: https://bitbucket.org/openrem/openrem/issue/215/
..  _`#214`: https://bitbucket.org/openrem/openrem/issue/214/
..  _`#213`: https://bitbucket.org/openrem/openrem/issue/213/
..  _`#212`: https://bitbucket.org/openrem/openrem/issue/212/
..  _`#211`: https://bitbucket.org/openrem/openrem/issue/211/
..  _`#210`: https://bitbucket.org/openrem/openrem/issue/210/
..  _`#209`: https://bitbucket.org/openrem/openrem/issue/209/
..  _`#208`: https://bitbucket.org/openrem/openrem/issue/208/
..  _`#207`: https://bitbucket.org/openrem/openrem/issue/207/
..  _`#206`: https://bitbucket.org/openrem/openrem/issue/206/
..  _`#205`: https://bitbucket.org/openrem/openrem/issue/205/
..  _`#204`: https://bitbucket.org/openrem/openrem/issue/204/
..  _`#203`: https://bitbucket.org/openrem/openrem/issue/203/
..  _`#202`: https://bitbucket.org/openrem/openrem/issue/202/
..  _`#201`: https://bitbucket.org/openrem/openrem/issue/201/
..  _`#200`: https://bitbucket.org/openrem/openrem/issue/200/
..  _`#199`: https://bitbucket.org/openrem/openrem/issue/199/
..  _`#198`: https://bitbucket.org/openrem/openrem/issue/198/
..  _`#197`: https://bitbucket.org/openrem/openrem/issue/197/
..  _`#196`: https://bitbucket.org/openrem/openrem/issue/196/
..  _`#195`: https://bitbucket.org/openrem/openrem/issue/195/
..  _`#194`: https://bitbucket.org/openrem/openrem/issue/194/
..  _`#193`: https://bitbucket.org/openrem/openrem/issue/193/
..  _`#192`: https://bitbucket.org/openrem/openrem/issue/192/
..  _`#191`: https://bitbucket.org/openrem/openrem/issue/191/
..  _`#190`: https://bitbucket.org/openrem/openrem/issue/190/
..  _`#189`: https://bitbucket.org/openrem/openrem/issue/189/
..  _`#188`: https://bitbucket.org/openrem/openrem/issue/188/
..  _`#187`: https://bitbucket.org/openrem/openrem/issue/187/
..  _`#186`: https://bitbucket.org/openrem/openrem/issue/186/
..  _`#185`: https://bitbucket.org/openrem/openrem/issue/185/
..  _`#184`: https://bitbucket.org/openrem/openrem/issue/184/
..  _`#183`: https://bitbucket.org/openrem/openrem/issue/183/
..  _`#182`: https://bitbucket.org/openrem/openrem/issue/182/
..  _`#181`: https://bitbucket.org/openrem/openrem/issue/181/
..  _`#180`: https://bitbucket.org/openrem/openrem/issue/180/
..  _`#179`: https://bitbucket.org/openrem/openrem/issue/179/
..  _`#178`: https://bitbucket.org/openrem/openrem/issue/178/
..  _`#177`: https://bitbucket.org/openrem/openrem/issue/177/
..  _`#176`: https://bitbucket.org/openrem/openrem/issue/176/
..  _`#175`: https://bitbucket.org/openrem/openrem/issue/175/
..  _`#174`: https://bitbucket.org/openrem/openrem/issue/174/
..  _`#173`: https://bitbucket.org/openrem/openrem/issue/173/
..  _`#172`: https://bitbucket.org/openrem/openrem/issue/172/
..  _`#171`: https://bitbucket.org/openrem/openrem/issue/171/
..  _`#170`: https://bitbucket.org/openrem/openrem/issue/170/
..  _`#169`: https://bitbucket.org/openrem/openrem/issue/169/
..  _`#168`: https://bitbucket.org/openrem/openrem/issue/168/
..  _`#167`: https://bitbucket.org/openrem/openrem/issue/167/
..  _`#166`: https://bitbucket.org/openrem/openrem/issue/166/
..  _`#165`: https://bitbucket.org/openrem/openrem/issue/165/
..  _`#164`: https://bitbucket.org/openrem/openrem/issue/164/
..  _`#163`: https://bitbucket.org/openrem/openrem/issue/163/
..  _`#162`: https://bitbucket.org/openrem/openrem/issue/162/
..  _`#161`: https://bitbucket.org/openrem/openrem/issue/161/
..  _`#160`: https://bitbucket.org/openrem/openrem/issue/160/
..  _`#159`: https://bitbucket.org/openrem/openrem/issue/159/
..  _`#158`: https://bitbucket.org/openrem/openrem/issue/158/
..  _`#157`: https://bitbucket.org/openrem/openrem/issue/157/
..  _`#156`: https://bitbucket.org/openrem/openrem/issue/156/
..  _`#155`: https://bitbucket.org/openrem/openrem/issue/155/
..  _`#154`: https://bitbucket.org/openrem/openrem/issue/154/
..  _`#153`: https://bitbucket.org/openrem/openrem/issue/153/
..  _`#152`: https://bitbucket.org/openrem/openrem/issue/152/
..  _`#151`: https://bitbucket.org/openrem/openrem/issue/151/
..  _`#150`: https://bitbucket.org/openrem/openrem/issue/150/
..  _`#149`: https://bitbucket.org/openrem/openrem/issue/149/
..  _`#148`: https://bitbucket.org/openrem/openrem/issue/148/
..  _`#147`: https://bitbucket.org/openrem/openrem/issue/147/
..  _`#146`: https://bitbucket.org/openrem/openrem/issue/146/
..  _`#145`: https://bitbucket.org/openrem/openrem/issue/145/
..  _`#144`: https://bitbucket.org/openrem/openrem/issue/144/
..  _`#143`: https://bitbucket.org/openrem/openrem/issue/143/
..  _`#142`: https://bitbucket.org/openrem/openrem/issue/142/
..  _`#141`: https://bitbucket.org/openrem/openrem/issue/141/
..  _`#140`: https://bitbucket.org/openrem/openrem/issue/140/
..  _`#139`: https://bitbucket.org/openrem/openrem/issue/139/
..  _`#138`: https://bitbucket.org/openrem/openrem/issue/138/
..  _`#137`: https://bitbucket.org/openrem/openrem/issue/137/
..  _`#136`: https://bitbucket.org/openrem/openrem/issue/136/
..  _`#135`: https://bitbucket.org/openrem/openrem/issue/135/
..  _`#134`: https://bitbucket.org/openrem/openrem/issue/134/
..  _`#133`: https://bitbucket.org/openrem/openrem/issue/133/
..  _`#132`: https://bitbucket.org/openrem/openrem/issue/132/
..  _`#131`: https://bitbucket.org/openrem/openrem/issue/131/
..  _`#130`: https://bitbucket.org/openrem/openrem/issue/130/
..  _`#129`: https://bitbucket.org/openrem/openrem/issue/129/
..  _`#128`: https://bitbucket.org/openrem/openrem/issue/128/
..  _`#127`: https://bitbucket.org/openrem/openrem/issue/127/
..  _`#126`: https://bitbucket.org/openrem/openrem/issue/126/
..  _`#125`: https://bitbucket.org/openrem/openrem/issue/125/
..  _`#124`: https://bitbucket.org/openrem/openrem/issue/124/
..  _`#123`: https://bitbucket.org/openrem/openrem/issue/123/
..  _`#122`: https://bitbucket.org/openrem/openrem/issue/122/
..  _`#121`: https://bitbucket.org/openrem/openrem/issue/121/
..  _`#120`: https://bitbucket.org/openrem/openrem/issue/120/
..  _`#119`: https://bitbucket.org/openrem/openrem/issue/119/
..  _`#118`: https://bitbucket.org/openrem/openrem/issue/118/
..  _`#117`: https://bitbucket.org/openrem/openrem/issue/117/
..  _`#116`: https://bitbucket.org/openrem/openrem/issue/116/
..  _`#115`: https://bitbucket.org/openrem/openrem/issue/115/
..  _`#114`: https://bitbucket.org/openrem/openrem/issue/114/
..  _`#113`: https://bitbucket.org/openrem/openrem/issue/113/
..  _`#112`: https://bitbucket.org/openrem/openrem/issue/112/
..  _`#111`: https://bitbucket.org/openrem/openrem/issue/111/
..  _`#110`: https://bitbucket.org/openrem/openrem/issue/110/
..  _`#109`: https://bitbucket.org/openrem/openrem/issue/109/
..  _`#108`: https://bitbucket.org/openrem/openrem/issue/108/
..  _`#107`: https://bitbucket.org/openrem/openrem/issue/107/
..  _`#106`: https://bitbucket.org/openrem/openrem/issue/106/
..  _`#105`: https://bitbucket.org/openrem/openrem/issue/105/
..  _`#104`: https://bitbucket.org/openrem/openrem/issue/104/
..  _`#103`: https://bitbucket.org/openrem/openrem/issue/103/
..  _`#102`: https://bitbucket.org/openrem/openrem/issue/102/
..  _`#101`: https://bitbucket.org/openrem/openrem/issue/101/
..  _`#100`: https://bitbucket.org/openrem/openrem/issue/100/
..  _`#99`: https://bitbucket.org/openrem/openrem/issue/99/
..  _`#98`: https://bitbucket.org/openrem/openrem/issue/98/
..  _`#97`: https://bitbucket.org/openrem/openrem/issue/97/
..  _`#96`: https://bitbucket.org/openrem/openrem/issue/96/
..  _`#95`: https://bitbucket.org/openrem/openrem/issue/95/
..  _`#94`: https://bitbucket.org/openrem/openrem/issue/94/
..  _`#93`: https://bitbucket.org/openrem/openrem/issue/93/
..  _`#92`: https://bitbucket.org/openrem/openrem/issue/92/
..  _`#91`: https://bitbucket.org/openrem/openrem/issue/91/
..  _`#90`: https://bitbucket.org/openrem/openrem/issue/90/
..  _`#89`: https://bitbucket.org/openrem/openrem/issue/89/
..  _`#88`: https://bitbucket.org/openrem/openrem/issue/88/
..  _`#87`: https://bitbucket.org/openrem/openrem/issue/87/
..  _`#86`: https://bitbucket.org/openrem/openrem/issue/86/
..  _`#85`: https://bitbucket.org/openrem/openrem/issue/85/
..  _`#84`: https://bitbucket.org/openrem/openrem/issue/84/
..  _`#83`: https://bitbucket.org/openrem/openrem/issue/83/
..  _`#82`: https://bitbucket.org/openrem/openrem/issue/82/
..  _`#81`: https://bitbucket.org/openrem/openrem/issue/81/
..  _`#80`: https://bitbucket.org/openrem/openrem/issue/80/
..  _`#79`: https://bitbucket.org/openrem/openrem/issue/79/
..  _`#78`: https://bitbucket.org/openrem/openrem/issue/78/
..  _`#77`: https://bitbucket.org/openrem/openrem/issue/77/
..  _`#76`: https://bitbucket.org/openrem/openrem/issue/76/
..  _`#75`: https://bitbucket.org/openrem/openrem/issue/75/
..  _`#74`: https://bitbucket.org/openrem/openrem/issue/74/
..  _`#73`: https://bitbucket.org/openrem/openrem/issue/73/
..  _`#72`: https://bitbucket.org/openrem/openrem/issue/72/
..  _`#71`: https://bitbucket.org/openrem/openrem/issue/71/
..  _`#70`: https://bitbucket.org/openrem/openrem/issue/70/
..  _`#69`: https://bitbucket.org/openrem/openrem/issue/69/
..  _`#68`: https://bitbucket.org/openrem/openrem/issue/68/
..  _`#67`: https://bitbucket.org/openrem/openrem/issue/67/
..  _`#66`: https://bitbucket.org/openrem/openrem/issue/66/
..  _`#65`: https://bitbucket.org/openrem/openrem/issue/65/
..  _`#64`: https://bitbucket.org/openrem/openrem/issue/64/
..  _`#63`: https://bitbucket.org/openrem/openrem/issue/63/
..  _`#62`: https://bitbucket.org/openrem/openrem/issue/62/
..  _`#61`: https://bitbucket.org/openrem/openrem/issue/61/
..  _`#60`: https://bitbucket.org/openrem/openrem/issue/60/
..  _`#59`: https://bitbucket.org/openrem/openrem/issue/59/
..  _`#58`: https://bitbucket.org/openrem/openrem/issue/58/
..  _`#57`: https://bitbucket.org/openrem/openrem/issue/57/
..  _`#56`: https://bitbucket.org/openrem/openrem/issue/56/
..  _`#55`: https://bitbucket.org/openrem/openrem/issue/55/
..  _`#54`: https://bitbucket.org/openrem/openrem/issue/54/
..  _`#53`: https://bitbucket.org/openrem/openrem/issue/53/
..  _`#52`: https://bitbucket.org/openrem/openrem/issue/52/
..  _`#51`: https://bitbucket.org/openrem/openrem/issue/51/
..  _`#50`: https://bitbucket.org/openrem/openrem/issue/50/
..  _`#49`: https://bitbucket.org/openrem/openrem/issue/49/
..  _`#48`: https://bitbucket.org/openrem/openrem/issue/48/
..  _`#47`: https://bitbucket.org/openrem/openrem/issue/47/
..  _`#46`: https://bitbucket.org/openrem/openrem/issue/46/
..  _`#45`: https://bitbucket.org/openrem/openrem/issue/45/
..  _`#44`: https://bitbucket.org/openrem/openrem/issue/44/
..  _`#43`: https://bitbucket.org/openrem/openrem/issue/43/
..  _`#42`: https://bitbucket.org/openrem/openrem/issue/42/
..  _`#41`: https://bitbucket.org/openrem/openrem/issue/41/
..  _`#40`: https://bitbucket.org/openrem/openrem/issue/40/
..  _`#39`: https://bitbucket.org/openrem/openrem/issue/39/
..  _`#38`: https://bitbucket.org/openrem/openrem/issue/38/
..  _`#37`: https://bitbucket.org/openrem/openrem/issue/37/
..  _`#36`: https://bitbucket.org/openrem/openrem/issue/36/
..  _`#35`: https://bitbucket.org/openrem/openrem/issue/35/
..  _`#34`: https://bitbucket.org/openrem/openrem/issue/34/
..  _`#33`: https://bitbucket.org/openrem/openrem/issue/33/
..  _`#32`: https://bitbucket.org/openrem/openrem/issue/32/
..  _`#31`: https://bitbucket.org/openrem/openrem/issue/31/
..  _`#30`: https://bitbucket.org/openrem/openrem/issue/30/
..  _`#29`: https://bitbucket.org/openrem/openrem/issue/29/
..  _`#28`: https://bitbucket.org/openrem/openrem/issue/28/
..  _`#27`: https://bitbucket.org/openrem/openrem/issue/27/
..  _`#26`: https://bitbucket.org/openrem/openrem/issue/26/
..  _`#25`: https://bitbucket.org/openrem/openrem/issue/25/
..  _`#24`: https://bitbucket.org/openrem/openrem/issue/24/
..  _`#23`: https://bitbucket.org/openrem/openrem/issue/23/
..  _`#22`: https://bitbucket.org/openrem/openrem/issue/22/
..  _`#21`: https://bitbucket.org/openrem/openrem/issue/21/
..  _`#20`: https://bitbucket.org/openrem/openrem/issue/20/
..  _`#19`: https://bitbucket.org/openrem/openrem/issue/19/
..  _`#18`: https://bitbucket.org/openrem/openrem/issue/18/
..  _`#17`: https://bitbucket.org/openrem/openrem/issue/17/
..  _`#16`: https://bitbucket.org/openrem/openrem/issue/16/
..  _`#15`: https://bitbucket.org/openrem/openrem/issue/15/
..  _`#14`: https://bitbucket.org/openrem/openrem/issue/14/
..  _`#13`: https://bitbucket.org/openrem/openrem/issue/13/
..  _`#12`: https://bitbucket.org/openrem/openrem/issue/12/
..  _`#11`: https://bitbucket.org/openrem/openrem/issue/11/
..  _`#10`: https://bitbucket.org/openrem/openrem/issue/10/
..  _`#9`: https://bitbucket.org/openrem/openrem/issue/9/
..  _`#8`: https://bitbucket.org/openrem/openrem/issue/8/
..  _`#7`: https://bitbucket.org/openrem/openrem/issue/7/
..  _`#6`: https://bitbucket.org/openrem/openrem/issue/6/
..  _`#5`: https://bitbucket.org/openrem/openrem/issue/5/
..  _`#4`: https://bitbucket.org/openrem/openrem/issue/4/
..  _`#3`: https://bitbucket.org/openrem/openrem/issue/3/
..  _`#2`: https://bitbucket.org/openrem/openrem/issue/2/
..  _`#1`: https://bitbucket.org/openrem/openrem/issue/1/


..  _`NHSBSP specific mammography csv export`: https://bitbucket.org/jacole/openrem-visualisation/commits/0ee416511c847960523a6475ef33ac72#comment-1003330
..  _@rijkhorst: https://bitbucket.org/rijkhorst/
..  _@LuukO: https://bitbucket.org/LuukO/
..  _Codacy: https://www.codacy.com/app/OpenREM/openrem
