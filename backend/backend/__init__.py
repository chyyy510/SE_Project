import sys

if sys.platform.startswith("linux"):
    import pymysql

    pymysql.install_as_MySQLdb()
