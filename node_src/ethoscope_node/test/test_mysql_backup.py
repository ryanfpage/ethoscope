from nose.tools import assert_equal
from ethoscope_node.utils.mysql_db_writer import MySQLdbCSVWriter
#from ethoscope_node.utils.mysql_backup import DBNotReadyError
import os
import logging
import traceback

def TestMySQLDump():

    try:

        mirror = MySQLdbCSVWriter("/Users/phrfp/Software/anaconda2/envs/ethoscope/home/tmp",
                        remote_db_name="test_etho_db",
                        remote_host="localhost",
                        remote_pass="",
                        remote_user="root")


        mirror.update_roi_tables()


    except Exception as e:
        print e
        logging.error(traceback.format_exc(e))
