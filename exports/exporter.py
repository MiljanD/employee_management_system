from models.db import Db
from datetime import date
import pymysql


class Exporter(Db):
    """
    Centralized class for exporting data from the database.

    Inherits from Db to establish a database connection.
    Provides reusable methods for retrieving clubs, employees, and schedule data.
    Used by other classes to avoid duplication of SQL logic.
    """
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()


    def _execute_query(self, query, params=None):
        """
        Executes a SQL query and returns the fetched results.
        :param query: SQL query string to be executed
        :param params: Optional tuple of parameters for parameterized queries
        :return: List of rows returned by the query
        """
        try:
            with self.con.cursor() as cursor:
                cursor.execute(query, params or ())
                self.con.commit()
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri ekstrakciji podataka: {e}")


    def export_all_clubs(self):
        """
        Retrives all club records  from the database.
        :return: List of club records
        """
        query = "SELECT * FROM employee_management_system.clubs"
        return self._execute_query(query)

    def export_all_employees(self):
        """
        Retrives all employee records from the database.
        :return: List of employee records
        """
        query = "SELECT * FROM employee_management_system.employees"
        return self._execute_query(query)

    def export_delegated_employees(self):
        """
        Retrives all employees who are currently delegated.
        :return: List of delegated employee records
        """
        query = "SELECT * FROM employee_management_system.employees WHERE delegated=%s"
        return self._execute_query(query, params=(1,))

    def export_non_delegated_employees(self):
        """
        Retrives all emoployees who are currentlly not delegated
        :return:List of non-delegated employee records
        """
        query = "SELECT * FROM employee_management_system.employees WHERE delegated=%s"
        return self._execute_query(query, params=(0,))

    def export_complete_schedule(self):
        """
        Retrives all schedule records, ordered by club ID.
        :return:List of schedule records
        """
        query = "SELECT * FROM employee_management_system.schedule ORDER BY club_id"
        return self._execute_query(query)

    def export_actual_schedule(self):
        """
        Filters and returns only active schedule records(where date_out is in the future.)
        :return:List of currently active schedule records
        """
        complete_schedule = self.export_complete_schedule()
        current_schedule = [schedule for schedule in complete_schedule if schedule["date_out"] > date.today()]
        return current_schedule

    def export_complete_actual_schedule_data(self):
        """
        Retrives enriched schedule data by joining clubs and employees.
        Incloudes club name, employee details and delegation dates.
        Only includes active delegations(date_out > today).
        :return: List of detailed schedule  records
        """
        query = ("SELECT s.id AS 'ID rasporeda', c.club_name AS 'Naziv kluba', "
                 "e.first_name AS 'Ime', e.last_name AS 'Prezime', e.role AS 'Pozicija', "
                 "s.date_in AS 'Delegiran od', s.date_out AS 'Delegiran do' "
                 "FROM employee_management_system.schedule s "
                 "JOIN employee_management_system.clubs c  ON s.club_id = c.id "
                 "JOIN employee_management_system.employees e ON s.employee_id = e.id "
                 "WHERE s.date_out > CURDATE() "
                 "ORDER BY  s.club_id ")

        return self._execute_query(query)


    def export_schedule_record_by_id(self, record_id):
        """
        Retrives a specific schedule record by its ID.
        :param record_id: Id of the schedule record
        :return: Schedule record matching the given ID
        """
        query = "SELECT * FROM employee_management_system.schedule WHERE id=%s"

        return self._execute_query(query, (record_id,))

