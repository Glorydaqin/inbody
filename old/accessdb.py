#-*-coding:utf-8-*-
import pypyodbc
import ConfigParser
import util
def conn():
    filepath = util.get_current_path() + "\license.ini"
    conf = ConfigParser.ConfigParser()
    res = conf.read(filepath)
    mdb = conf.get("config","dbpath")
    str = 'Driver={Microsoft Access Driver (*.mdb,*.accdb)};DBQ='+mdb+';'
    #str = 'Driver={Microsoft Access Driver (*.mdb,*.accdb)};DBQ=C:\Users\QN\PycharmProjects\inbody\LookinBody.mdb;'
    con = pypyodbc.win_connect_mdb(str)
    return con
def get(sql):
    con = conn()
    cur = con.cursor()
    cur.execute(sql)
    # for col in cur.description:
    #     print str(col[0]) + "\t" + str(col[1])

    # for row in cur.fetchall():
    #     print row
        # for field in row:
        #     print field,
        # print ''
    data = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return data