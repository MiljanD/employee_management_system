import pymysql


class Db:
    """
    Base class for managing database connection.
    Provides a reusable connection handler for all database-related classes.
    """
    def __init__(self):
        self.__connection = None


    def _get_connection(self):
        """
        Establishes and returns a MySQL database connection.
        Uses pymysql with dictionary cursor for row access by column name.
        If connection already exists, returns the existing one.
        :return: Active pymysql connection object
        """
        if self.__connection is None:
            try:
                self.__connection = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="dm3004^mk2606",
                    database="employee_management_system",
                    cursorclass=pymysql.cursors.DictCursor
                )
            except pymysql.MySQLError as e:
                raise  RuntimeError(f"Neuspesna konekcija ka bazi: {e}")

        return self.__connection


    def close_connection(self):
        """
        Closes the active database connection if it exists.
        Resets the internal connection reference to None.
        """
        if self.__connection:
            self.__connection.close()
            self.__connection = None
