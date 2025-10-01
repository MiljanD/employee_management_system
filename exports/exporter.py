from models.db import Db
from datetime import date


class Exporter(Db):
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()


    def _execute_query(self, query, params=None):
        with self.con.cursor() as cursor:
            cursor.execute(query, params or ())
            self.con.commit()
            return cursor.fetchall()


    def export_all_clubs(self):
        query = "SELECT * FROM employee_management_system.clubs"
        return self._execute_query(query)

    def export_all_employees(self):
        query = "SELECT * FROM employee_management_system.employees"
        return self._execute_query(query)

    def export_delegated_employees(self):
        query = "SELECT * FROM employee_management_system.employees WHERE delegated=%s"
        return self._execute_query(query, params=(1,))

    def export_non_delegated_employees(self):
        query = "SELECT * FROM employee_management_system.employees WHERE delegated=%s"
        return self._execute_query(query, params=(0,))

    def export_complete_schedule(self):
        query = "SELECT * FROM employee_management_system.schedule ORDER BY club_id"
        return self._execute_query(query)

    def export_actual_schedule(self):
        complete_schedule = self.export_complete_schedule()
        current_schedule = [schedule for schedule in complete_schedule if schedule["date_out"] > date.today()]
        return current_schedule

    def export_complete_actual_schedule_data(self):
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
        query = "SELECT * FROM employee_management_system.schedule WHERE id=%s"

        return self._execute_query(query, (record_id))

