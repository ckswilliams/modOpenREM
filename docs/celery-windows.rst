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

An example batch file is shown below for running and restarting Celery:

.. sourcecode:: bat
   :linenos:

    :: Create variables containing the path to OpenREM and the name and path of the
    :: celery pid  and log files
    SET openremPath=D:\Server_Apps\python27\Lib\site-packages\openrem
    SET celeryPidFile=E:\media_root\celery\default.pid
    SET celeryLogFile=E:\media_root\celery\default.log

    :: Change to the drive on which OpenREM is installed and navigate to the
    :: OpenREM folder
    D:
    CD %openremPath%

    :: Attempt to shutdown celery gracefully
    celery -A openremproject control shutdown --timeout=10

    :: Pause this file for 10 s to ensure that the above has time to work (you may
    :: need to check that the 'timeout' command is available on your Windows
    :: system. Some systems may have 'sleep' instead, in which case replace the
    :: line below with:
    :: SLEEP 10
    TIMEOUT /T 10

    :: Kill any remaining celery tasks (ungraceful) and delete the pid file in case
    :: the above graceful shutdown did not work.
    IF EXIST %celeryPidFile% (
        :: Read the pid values in from the file
        SET /P celeryPid=<%celeryPidFile%

        :: Kill the process with that pid value
        TASKKILL /F /PID %celeryPid%

        :: Force the deletion of the pid file
        DEL /F %celeryPidFile%
    )

    :: Restart a new instance of celery 
    celery worker -n default -P solo -Ofair -A openremproject -c 4 -Q default --pidfile=%celeryPidFile% --logfile=%celeryLogFile%


Lines 3 to 5 set variables with the locations of your OpenREM installation and
Celery log and pid file locations. Make sure these are changed to match your
own OpenREM installation. Lines 9 and 10 navigate to the OpenREM drive and
folder. Ensure that the drive (``D:`` on line 9 in the above example) matches
the drive that contains your OpenREM installation. Line 13 attempts to
gracefully shutdown celery. If the graceful shutdown doesn't work line 29 kills
the celery.exe process that has a pid matching that contained in the
``default.pid`` file (we don't want to kill all Celery processes as this would
also kill the Celery process that is running Flower). Line 32 deletes the
``default.pid`` process ID file: Celery won't restart if this pid file exists.
Finally, line 36 runs a new instance of Celery.


An example batch file is shown below for running Flower:

.. sourcecode:: bat
   :linenos:

    :: Create variables containing the path to OpenREM and the name and path of the
    :: celery pid  and log files
    SET openremPath=D:\Server_Apps\python27\Lib\site-packages\openrem
    SET flowerLogFile=E:\media_root\celery\flower.log
    SET flowerPort=5555

    :: Change to the drive on which OpenREM is installed and navigate to the
    :: OpenREM folder
    D:
    CD %openremPath%

    :: Run flower
    celery -A openremproject flower --port=%flowerPort% --loglevel=info --log-file-prefix=%flowerLogFile%


Lines 3 and 4 set variables with the locations of your OpenREM installation and the
Flower log files. Make sure these are changed to match your own
OpenREM installation. Line 5 sets the port number Flower will use. If you change the default port from 5555 then you
need to make the same change in
``openremproject\local_settings.py`` to add/modify the line ``FLOWER_PORT = 5555``.
Lines 9 and 10 navigate to the OpenREM drive and folder.
Finally, line 13 starts Flower using the parameters that are supplied at the
top of the batch file.


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
