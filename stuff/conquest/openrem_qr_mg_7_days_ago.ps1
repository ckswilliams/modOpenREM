# Script to obtain all MG studies from PACS for the date seven days prior to
# date the script is run and import them into OpenREM. This script is designed
# to be run as a scheduled task on the OpenREM server once per day, ideally in
# the early hours of the morning.
#
# The seven day delay is to provide some time for images from mobile vans to be
# put on to PACS.
#
# Get yesterday's date
$dateString = "{0:yyyy-MM-dd}" -f (get-date).AddDays(-7)
# Run the openrem_qr.py script with yesterday's date as the to and from date
# The first "1" is OpenREM's database ID for the PACS DICOM node
# The second "1" is OpenREM's database ID for its own Store SCP node
python D:\Server_Apps\python27\Scripts\openrem_qr.py 1 1 -mg -f $dateString -t $dateString