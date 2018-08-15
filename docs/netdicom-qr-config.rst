*****************************************
Configuration required for query-retrieve
*****************************************

You need a DICOM store service set up - see :doc:`import` for details.

If you are using a third party DICOM Store server, then you will need to add the details as per :doc:`netdicom-nodes`
but do not use the 'advaanced' section.

To configure a remote query retrieve SCP, on the ``Config`` menu select ``DICOM networking``, then click
``Add new QR Node`` and fill in the details:

* Name of QR node: This is the *friendly name*, such as ``PACS QR``
* AE Title of the remote node: This is the DICOM name of the remote node, 16 or fewer letters and numbers, no spaces
* AE Title this server: This is the DICOM name that the query (DICOM C-Find) will come from. This may be important if
  the remote node filters access based on *calling aet*. Normal rules of 16 or fewer letters and numbers, no spaces
* Remote port: Enter the port the remote node is using (eg 104)
* Remote IP address: The IP address of the remote node, for example ``192.168.1.100``
* Remote hostname: Alternatively, if your network has a DNS server that can resolve the hostnames, you can enter the
  hostname instead. If the hostname is entered, it will be used in preference to the IP address, so only enter it if
  you know it will be resolved.
* Use Modality in Study Query: Some PACS systems (like Impax 6.6) need modality at study level for correct filtering.
  if this option is checked, the modality tag is inserted in the study level request.

  .. warning::

    Modality is not a valid tag in a study level request (Modalities In Study is available instead). However, some PACS
    systems require it for proper function, others will ignore it, and some will return zero results if the tag is
    present.
