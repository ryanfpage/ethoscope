"""
This carries out mysql back up using what ever converter is passed. It will pause for ptime minutes before doing
an update. On the first update call the tables are setup as well as copying the data in. After that it will only
do an update.
"""
__author__ = 'ryanfpage'
import threading
import time
import os
class MySQLdbBackupRunner(object):
    """
    Runner for the MySQL db back up. Runs the update in a seperate thread.
    params: ptime the time in minutes before the db is backed up
    params: dbconv the data base converter used to copy info out of the MySQL db
    """
    def __init__(self, ptime=60, dbconv=None):
        self.ptime = ptime
        self.table_setup = False
        self.dbname_backup = None
        self.condition = None
        self.running = False
        if dbconv != None:
            self.dbconv = dbconv

    def filename(self):
        return self.dbname_backup

    def dbconverter(self, dbconv, skip_tables=None, dbname_backup=None):
        """
        Set the db converter.
        params: dbconv the data base converter to be used
        params: skip_tables tables to ignore during copy
        params: the file name of the copied db
        """
        self.dbconv = dbconv
        self.skip_tables = skip_tables
        directory = os.path.dirname(dbname_backup)
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.dbname_backup = dbname_backup

    def quickupdatedb(self):
        """
        Run a quick update without any pause.
        """
        self.dbconv.update_database()

    def _updatedb(self, condition):
        """
        Carry out the update after waiting for ptime minutes. If this is the first time it is run
        it will copy the tables and then after just append the data
        """
        condition.acquire()
        while(True):

            condition.wait(float(self.ptime)*60.0)

            if self.running == False:
                break
            if self.table_setup == False:
                self.dbconv.copy_database("sqlite:////"+self.dbname_backup, skip_tables=self.skip_tables)
                self.table_setup = True
            else:
                self.dbconv.update_database()
        condition.release()

    def runbackup(self, resume_run=False):
        """
        Start the thread running the updater. Remove existing backup first and reset the table setup flag
        """
        if not resume_run:
            if self.running:
                self.stopbackup()
            self.table_setup = False
            if self.dbname_backup == None:
                raise Exception("Error no backup file name has been specified")
            if os.path.isfile(self.dbname_backup):
                os.remove(self.dbname_backup)
            self.condition = threading.Condition()
            self.db_thread = threading.Thread(target=self._updatedb, args=(self.condition, ))
            self.running = True

            self.db_thread.start()
        else:
            self.condition = threading.Condition()
            self.db_thread = threading.Thread(target=self.updatedb, args=(self.condition, ))
            self.running = True
            self.db_thread.start()



    def stopbackup(self):
        """
        Stop thread - TODO check that this will join once the function has finished executing
        """
        self.running = False
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()
        