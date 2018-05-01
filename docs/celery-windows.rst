#############################
Daemonising Celery on Windows
#############################

To ensure that the Celery task queue is started at system start-up it is
advisable to launch Celery using a batch file and configure Windows Task
Scheduler to run this at system start-up.

Celery will sometimes fall over during the execution of a long task. In this
situation it will not restart on its own. Windows Task Scheduler can be used to
restart Celery on a regular basis. In addition it can be used to ensure celery
is running a few minutes prior to a scheduled PACS query.

An example batch file is shown below:

.. sourcecode:: bat
   :linenos:

    :: Change to the drive on which OpenREM is installed and navigate to the
    :: OpenREM folder
    D:
    CD D:\Server_Apps\python27\Lib\site-packages\openrem
    
    :: Attempt to shutdown celery gracefully
    celery -A openremproject control shutdown --timeout=10
    
    :: Pause this file for 10 s to ensure that the above has time to work (you may
    :: need to check that the 'timeout' command is available on your Windows
    :: system. Some systems may have 'sleep' instead, in which case replace the
    :: line below with:
    :: SLEEP 10
    TIMEOUT /T 10
    
    :: Kill any remaining celery tasks (ungraceful) and delete the pid file in case
    :: the above graceful shutdown did not work
    TASKKILL /IM /F celery.exe
    DEL /F E:\media_root\celery\default.pid
    
    :: Restart a new instance of celery 
    celery worker -n default -P solo -Ofair -A openremproject -c 4 -Q default --pidfile=e:\media_root\celery\default.pid --logfile=e:\media_root\celery\default.log


Lines 3 and 4 navigate to the OpenREM drive and folder. Line 7 attempts to
gracefully shutdown celery. Line 18 kills any celery.exe processes that are
currently running in case the graceful shutdown didn't work. Line 19 deletes
the ``default.pid`` process ID file that exists in the celery log file
location. Celery won't restart if this pid file exists. Finally, line 22 runs
a new instance of celery. If you wish to use this example you will have to
ensure that the drive letters and paths are changed to match your own OpenREM
system installation.

Figure 1 shows the ``OpenREM - start celery`` task in the task list.

.. figure:: img/010_taskOverview.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/010_taskOverview.png

   Figure 1: An overview of Windows Task Scheduler


Figure 2 shows the general task settings. The task has been set to run using
the Windows ``SYSTEM`` user, whether the user is logged in or not, and with
the highest privileges.

.. figure:: img/020_taskPropertiesGeneral.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/020_taskPropertiesGeneral.png

   Figure 2: General properties


Figure 3 shows the times when the task will be triggered. In the example
celery is started at system start up, and restarted multiple times each day
to ensure that it is running before any PACS queries. Your requirements may
be more straightforward than this example.

.. figure:: img/030_taskPropertiesTriggers.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/030_taskPropertiesTriggers.png

   Figure 3: Trigger properties


Figure 4 shows the action that is taken when the task is executed: it is set to
run the batch file that is described at the top of this document.

.. figure:: img/040_taskPropertiesActions.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/040_taskPropertiesActions.png

   Figure 4: Action properties


Figure 5 shows that there are no particular conditions set for the task.

.. figure:: img/050_taskPropertiesConditions.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/050_taskPropertiesConditions.png

   Figure 5: Condition properties


Finally, figure 6 shows the task settings. The task is set so that it can be
run on demand if required. It is also set so that it is forced to stop when
requested to do so.

.. figure:: img/060_taskPropertiesSettings.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/060_taskPropertiesSettings.png

   Figure 6: Task settings
