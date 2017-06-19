__author__ = 'ryanfpage'

import MySQLdb
import os
import logging
import traceback


class MySQLdbCSVWriter(object):

    def __init__(self, dst_path,
                            remote_db_name="ethoscope_db",
                            remote_host="localhost",
                            remote_user="ethoscope",
                            remote_pass="ethoscope",
                            overwrite=True):
        """

        A class to dump the current data base into a pandas data frame. This is going to be intially desigend and
        tested so that it runs with the MySQL server running locally and not remotly.


        :param db_name: the name of the database running locally.
        :param host: the ip of the database - localhost will be fully test remote testing to follow
        :param user: the user name for the database
        :param pass: the password for the database
        :param overwrite: whether the destination file should be overwritten. If False, data are appended to it


        """
        try:
            self._remote_host = remote_host
            self._remote_user = remote_user
            self._remote_pass = remote_pass
            self._remote_db_name = remote_db_name

            self._dst_path=dst_path

            self._csv_file_name = self._dst_path+"/"+self._remote_db_name + ".csv"
            print ("Filename:", self._csv_file_name)

            # we remove file and create dir, if needed

            if overwrite:
                logging.info("Trying to remove old database")
                try:
                    os.remove(self._csv_file_name)
                    logging.info("Success")
                except OSError as e:
                    logging.warning(e)
                    pass



        except Exception as e:
            raise

    def update_roi_tables(self):
        """
        Fetch new ROI tables and new data points in the remote and use them to update local db

        :return:
        """

        src = MySQLdb.connect(host=self._remote_host, user=self._remote_user,
                                         passwd=self._remote_pass, db=self._remote_db_name)




        command = "SELECT roi_idx FROM ROI_MAP"
        cur = src.cursor()
        cur.execute(command)
        rois_in_src = set([c[0] for c in cur])
        for i in rois_in_src :
            print "ROIs: ", i
            self._update_one_roi_table("ROI_%i" % i, i, src)

    def _update_one_roi_table(self, table_name, roi_num,src):
        src_cur = src.cursor()
        src_command = "SELECT * FROM %s" % (table_name)
        src_cur.execute(src_command)

        for sc in src_cur:
            with open(self._csv_file_name,"a") as f:
                row = "\t".join(["{0}".format(val) for val in sc])
                row += "\t"+str(roi_num)
                f.write(row)
                f.write("\n")
