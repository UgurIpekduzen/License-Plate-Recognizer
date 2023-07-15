import mysql.connector
from collections import OrderedDict

class DBConnection(object):
    __host       = None
    __user       = None
    __port       = None
    __password   = None
    __database   = None
    __session    = None
    __connection = None

    def __init__(self, host='', user='', password='', database='', port=''):
        self.__host     = host
        self.__user     = user
        self.__port     = port
        self.__password = password
        self.__database = database
        if not self.__check('Vehicle'):
            self.__create('Vehicle', 'licensePlate VARCHAR(50) NOT NULL', 'isRegistered TINYINT(1) DEFAULT 0', 'isBlacklisted TINYINT(1) DEFAULT 0')
    ## End def __init__

    def __open(self):
        try:
            cnx = mysql.connector.connect(host=self.__host, user=self.__user, passwd=self.__password, database=self.__database, port=self.__port)
            self.__connection = cnx
            self.__session    = cnx.cursor()
            print(cnx)
        except mysql.connector.Error as e:
            print ("Error %d: %s" % (e.args[0],e.args[1]))
            self.__connection = None
    ## End def __open

    def __close(self):
        self.__session.close()
        self.__connection.close()
    ## End def __close

    def __create(self, table, *args):
        query = "CREATE TABLE %s (%s)" % (table, ', '.join(args))
        self.__open()
        self.__session.execute(query)
        self.__connection.commit()
        self.__close()
    ## End create

    def __check(self, table):
        query = """SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '%s' """ % table
        self.__open()
        self.__session.execute(query) 
        if self.__session.fetchone()[0] == 1:
            self.__session.close()
            return True

        self.__session.close()
        print("%s adında bir tablo bulunmamaktadır!" % table)
        return False
    ## End def check

    def select(self, table, where=None, *args, **kwargs):
        if self.__check(table):
            result = None
            query = 'SELECT * FROM %s' % table

            if where:
                query += " WHERE %s" % where

            self.__open()
            self.__session.execute(query, tuple(kwargs.values()))
            number_rows = self.__session.rowcount
            number_columns = len(self.__session.description)

            if number_columns > 1:
                result = [item for item in self.__session.fetchall()]
            else:
                result = [item[0] for item in self.__session.fetchall()]
            self.__close()

            return result
    ## End def select

    def update(self, table, where=None, *args, **kwargs):
        if self.__check(table):
            query  = "UPDATE %s SET " % table
            keys   = kwargs.keys()
            values = tuple(kwargs.values()) + tuple(args)
            l = len(keys) - 1
            for i, key in enumerate(keys):
                query += "`"+key+"` = %s"
                if i < l:
                    query += ","
                ## End if i less than 1
            ## End for keys
            query += " WHERE %s" % where

            self.__open()
            self.__session.execute(query, values)
            self.__connection.commit()

            # Obtain rows affected
            update_rows = self.__session.rowcount
            self.__close()

            return update_rows
    ## End function update

    def insert(self, table, *args, **kwargs):
        if self.__check(table):
            values = None
            query = "INSERT INTO %s " % table
            if kwargs:
                keys = kwargs.keys()
                values = tuple(kwargs.values())
                query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"] * len(values)) + ")"
            elif args:
                values = args
                query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

            self.__open()
            self.__session.execute(query, values)
            self.__connection.commit()
            self.__close()
            return self.__session.lastrowid
    ## End def insert

    def delete(self, table, where=None, *args):
        if self.__check(table):
            query = "DELETE FROM %s" % table
            if where:
                query += ' WHERE %s' % where

            values = tuple(args)

            self.__open()
            self.__session.execute(query, values)
            self.__connection.commit()

            # Obtain rows affected
            delete_rows = self.__session.rowcount
            self.__close()

            return delete_rows
    ## End def delete
## End class
