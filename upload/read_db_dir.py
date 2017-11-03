import ConfigParser
import os.path as op


def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = op.split(op.realpath(__file__))[0] + '/db.conf'
    config.read(path)
    return config.get(section, key)


dbhost = getConfig("database", "dbhost")
dbport = getConfig("database", "dbport")
dbuser = getConfig("database", "dbuser")
dbpassword = getConfig("database", "dbpassword")
dbname = getConfig("database", "dbname")


def sql_dir():
    a = "mysql+pymysql://" + \
        dbuser + ":" + \
        dbpassword + "@" + \
        dbhost + ":" +\
        dbport + "/" + \
        dbname
    # print a
    return a
# sql_dir()


def get_upload_dir():
    a = getConfig("upload_dir2", "dir")
    print a
    return a

# get_upload_dir()
