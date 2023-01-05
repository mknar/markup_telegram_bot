from time import sleep

import MySQLdb


def check_mysql_conaction():
    try:
        MySQLdb.connect(host='localhost', user='root', passwd='', db='markup_tool_db')
    except MySQLdb.OperationalError:
        print('MySQL not ready yet, please wait ...')
        sleep(4)
        check_mysql_conaction()


check_mysql_conaction()
print('MySQL is ready')
