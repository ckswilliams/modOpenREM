########################################
Daemonising Celery and Flower on Windows
########################################

To ensure that the Celery task queue and Flower are started at system start-up
it is advisable to launch them using batch files and configure Windows Task
Scheduler to run each of these at system start-up.

Celery will sometimes fall over during the execution of a long task. In this
situation it will not restart on its own. Windows Task Scheduler can be used to
restart Celery on a regular basis. In addition it can be used to ensure celery
is running a few minutes prior to a scheduled PACS query.

An example batch file is shown below for running and restarting Celery. This
calls separate batch files to shutdown and start Celery, and start Flower if
needed.

Celery control batch file
=========================

`celery_task.bat`, to be run as a scheduled task.

.. sourcecode:: bat

    :: Create variables containing the name and path of the Celery pid file and the
    :: names and paths to the batch files used to shutdown and run Celery and run
    :: Flower.
    SET celeryPidFile=E:\media_root\celery\default.pid
    SET celeryShutdownFile=D:\Server_Apps\celery\celery_shutdown.bat
    SET celeryStartFile=D:\Server_Apps\celery\celery_start.bat
    SET flowerStartFile=D:\Server_Apps\flower\flower_start.bat

    :: Attempt to shutdown Celery gracefully.
    START /B CMD /C CALL "%celeryShutdownFile%"

    :: Pause this file for 60 s to ensure that the above has time to work (you may
    :: need to check that the 'timeout' command is available on your Windows
    :: system. Some systems may have 'sleep' instead, in which case replace the
    :: line below with:
    :: SLEEP 60
    TIMEOUT /T 60

    :: Kill any remaining Celery instances (ungraceful) and delete the pid file in
    :: case the above graceful shutdown did not work. If the default.pid file
    :: exists then the graceful shutdown didn't work.
    IF EXIST "%celeryPidFile%" (
        :: Kill all processes with the name celery.exe and any associated
        :: python.exe processes. This will also kill Flower.
        TASKKILL /IM celery.exe /T /F

        :: Force the deletion of the pid file.
        DEL /F "%celeryPidFile%"
        
        :: Start Flower.
        START /B CMD /C CALL "%flowerStartFile%"
    )

    :: Start Celery.
    START /B CMD /C CALL "%celeryStartFile%"


Celery shutdown batch file
==========================

`celery_shutdown.bat`, called by `celery_task.bat`.

.. sourcecode:: bat

    :: Create variable containing the drive and path to OpenREM.
    SET openremDrive=D:
    SET openremPath=D:\Server_Apps\python27\Lib\site-packages\openrem

    :: Change to the drive on which OpenREM is installed and navigate to the
    :: OpenREM folder.
    %openremDrive%
    CD "%openremPath%"

    :: Attempt to shutdown Celery gracefully.
    celery -A openremproject control shutdown --timeout=30



Celery start batch file
=======================

`celery_start.bat`, called by `celery_task.bat`.

.. sourcecode:: bat
   :linenos:

    :: Create variables containing the drive and path to OpenREM and the name and
    :: path of the Celery pid and log files.
    SET openremDrive=D:
    SET openremPath=D:\Server_Apps\python27\Lib\site-packages\openrem
    SET celeryPidFile=E:\media_root\celery\default.pid
    SET celeryLogFile=E:\media_root\celery\default.log

    :: Change to the drive on which OpenREM is installed and navigate to the
    :: OpenREM folder.
    %openremDrive%
    CD "%openremPath%"

    :: Start Celery.
    celery worker -n default -P solo -Ofair -A openremproject -c 1 -Q default --pidfile=%celeryPidFile% --logfile=%celeryLogFile%


Flower start batch file
=======================

`flower_start.bat`, called by `celery_task.bat` and also used to start Flower at system start-up.

.. sourcecode:: bat

    :: Create variables containing the drive and path to OpenREM and the name and
    :: path of the Flower log file and the Flower port.
    SET openremDrive=D:
    SET openremPath=D:\Server_Apps\python27\Lib\site-packages\openrem
    SET flowerLogFile=E:\media_root\celery\flower.log
    SET flowerPort=5555

    :: Change to the drive on which OpenREM is installed and navigate to the
    :: OpenREM folder.
    %openremDrive%
    CD "%openremPath%"

    :: Start Flower using Celery.
    celery -A openremproject flower --port="%flowerPort%" --loglevel=info --log-file-prefix="%flowerLogFile%"


Setting up a scheduled task
===========================

For Celery
++++++++++

Open ``Task Scheduler`` on the OpenREM server and then click on the ``Task Scheduler Library``
item in the left-hand pane. This should look something like figure 1 below, but without the
OpenREM tasks present.

.. figure:: img/010_taskOverview.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/010_taskOverview.png

   Figure 1: An overview of Windows Task Scheduler

To create a new task for celery click on ``Create Task...`` in the ``Actions`` menu in the
right-hand pane. Give the task a name and description. Next, click on the
``Change User or Group`` button and type ``system`` in to the box, then click
``Check Names``, then click ``OK``. This sets the server's ``SYSTEM`` user to run the
task. Also check the ``Run with highest prilileges`` box. Your task should now look similar
to figure 2.

.. figure:: img/020_taskPropertiesGeneral.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/020_taskPropertiesGeneral.png

   Figure 2: General properties

Next, click on the ``Triggers`` tab so that you can set when the task will be run. As a
minimum you should add an ``At startup`` trigger. To do this, click ``New...``. In the
dialogue box that appears select ``At startup`` from the ``Begin the task`` options and ensure
that the ``Enabled`` checkbox is selected. Then click ``OK``. You may wish to add other
triggers that take place at specific times during the day, as shown in figure 3.

In the example shown in figure 3 celery is started at system start up, and restarted multiple
times each day to ensure that it is running before any PACS queries. Your requirements may
be more straightforward than this example.

.. figure:: img/030_taskPropertiesTriggers.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/030_taskPropertiesTriggers.png

   Figure 3: Trigger properties

Now click on the ``Actions`` tab so that you can add the action that is taken when
the task is run. Click on ``New...``, and in the dialogue box that appears select
``Start a program`` as the ``Action``. Click on ``Browse`` and select the celery
batch file that you created earlier. Click ``OK`` to close the ``New Action``
dialogue box. Figure 4 shows an example of the the ``Actions`` tab.

.. figure:: img/040_taskPropertiesActions.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/040_taskPropertiesActions.png

   Figure 4: Action properties


There are no particular conditions set for the task, as shown in figure 5.

.. figure:: img/050_taskPropertiesConditions.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/050_taskPropertiesConditions.png

   Figure 5: Condition properties


Finally, click on the ``Settings`` tab (figure 6). Check the ``Allow task to be run on demand``
box, and also the ``If the running task does not end when requested, force it to stop`` box.
Choose ``Stop the existing instance`` from the ``If the task is already running, then the following rule applies:``
list. Then click the ``OK`` button to add the task to the scheduler library.

.. figure:: img/060_taskPropertiesSettings.png
   :figwidth: 100%
   :align: center
   :alt: Task scheduler overview
   :target: _images/060_taskPropertiesSettings.png

   Figure 6: Task settings


For Flower
++++++++++

Repeat the above steps for the Flower batch file, but only configure the Flower
task to trigger on system start-up: there should be no need to schedule
re-starts of Flower.
