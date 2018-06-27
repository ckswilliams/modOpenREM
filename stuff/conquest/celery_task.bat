REM Windows batch file to run a celery worker as part of OpenREM.
REM
REM This file is run on system start up via task scheduler.
REM
REM Each time this file is run it:
REM     Kills all tasks with the  name "celery.exe"
REM     Deletes the previous celery PID file (make sure this is pointing to the correct place)
REM     Navigates to the OpenREM folder (D:\Server_Apps\python27\Lib\site-packages\openrem in this case. Again - make sure this is the correct place)
REM     Executes a new celery worker (make sure the pidfile and logfile locations are correct for your installation)
REM
REM I find that celery fails after running a very long task, so task scheduler is also
REM configured to run this task several times a day to ensure that it is running when
REM my scheduled queries of PACS are carried out.

taskkill /im /f celery.exe
del /F E:\media_root\celery\default.pid
d:
cd D:\Server_Apps\python27\Lib\site-packages\openrem
celery worker -n default -P solo -Ofair -A openremproject -E -c 1 -Q default --pidfile=e:\media_root\celery\default.pid --logfile=e:\media_root\celery\default.log
