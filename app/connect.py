from flaskext.mysql import MySQL

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "123456seven",
                           db = "Tuklab")
    c = conn.cursor()

    return c, conn