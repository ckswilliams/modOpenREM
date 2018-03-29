#############################
Daemonising Celery on Windows
#############################

To ensure that the Celery task queue is started at system start-up it is
advisable to launch Celery using a batch file. Windows Task Scheduler can then
be used to start Celery at system start-up.

Celery will sometimes fall over during the execution of a long task. In this
situation it will not restart on its own. Windows Task Scheduler can be used to
restart Celery on a regular basis, or can be used to restart celery a few
minutes before OpenREM is due to carry out a long task, such as making a PACS query. 

A suitable batch file may be similar to the code below:

.. sourcecode:: bat
   :linenos:

    TASKKILL /IM /F celery.exe
    DEL /F E:\media_root\celery\default.pid
    D:
    CD D:\Server_Apps\python27\Lib\site-packages\openrem
    celery worker -n default -P solo -Ofair -A openremproject -c 4 -Q default --pidfile=e:\media_root\celery\default.pid --logfile=e:\media_root\celery\default.log

Line 1 kills any celery.exe processes that are currently running. Line 2 deletes
any process ID file that exists in the celery log file location. Lines 3 and 4
navigate to the OpenREM drive and folder. Finally, line 5 runs celery.


.. figure:: img/010_taskOverview.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/010_taskOverview.png

   Figure 1: An overview of Windows Task Scheduler

   
.. figure:: img/020_taskPropertiesGeneral.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/020_taskPropertiesGeneral.png

   Figure 2: General properties

   
.. figure:: img/030_taskPropertiesTriggers.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/030_taskPropertiesTriggers.png

   Figure 3: Trigger properties


.. figure:: img/040_taskPropertiesActions.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/040_taskPropertiesActions.png

   Figure 4: Action properties


.. figure:: img/050_taskPropertiesConditions.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/050_taskPropertiesConditions.png

   Figure 5: Condition properties


.. figure:: img/060_taskOverviewSettings.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/060_taskOverviewSettings.png

   Figure 6: Task settings
