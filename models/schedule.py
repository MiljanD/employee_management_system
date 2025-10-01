from models.db import Db
from datetime import date
from exports.exporter import Exporter


class Schedule(Db):
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.club_id = None
        self.employee_id = None
        self.start_date = None
        self.end_date = None


    def __convert_date_input_to_date(self, date_input):
        date_data_collection = [int(date_data) for date_data in date_input.split("-")]
        converted_date = date(day=date_data_collection[0],
                              month=date_data_collection[1],
                              year=date_data_collection[2])
        return converted_date


    @property
    def id_of_club(self):
        return self.club_id

    @id_of_club.setter
    def id_of_club(self, club_id):
        self.club_id = int(club_id)

    @property
    def id_of_employee(self):
        return self.employee_id

    @id_of_employee.setter
    def id_of_employee(self, employee_id):
        self.employee_id = int(employee_id)

    @property
    def delegation_in(self):
        return self.start_date

    @delegation_in.setter
    def delegation_in(self, start_date):
        self.start_date = self.__convert_date_input_to_date(start_date)

    @property
    def delegation_out(self):
        return self.end_date

    @delegation_out.setter
    def delegation_out(self, end_date):
        self.end_date = self.__convert_date_input_to_date(end_date)


    def check_employee_delegation(self):
        exports = Exporter()
        current_delegation = exports.export_actual_schedule()
        if not current_delegation:
            not_delegated = True
        else:
            for delegation in current_delegation:
                if delegation["employee_id"] == self.employee_id:
                    not_delegated = False
                else:
                    not_delegated = True

        return not_delegated

    def generate_schedule(self):
        if self.check_employee_delegation():
            with self.con.cursor() as cursor:
                query = ("INSERT INTO employee_management_system.schedule (club_id, employee_id, date_in, date_out) "
                         "VALUES (%s, %s, %s, %s)")
                cursor.execute(query, (self.club_id, self.employee_id, self.start_date, self.end_date))
                self.con.commit()
        else:
            print("Zaposleni je vec delegiran.")


    def delete_schedule_record(self, record_id):
        with self.con.cursor() as cursor:
            query = "DELETE FROM employee_management_system.schedule WHERE id=%s"
            cursor.execute(query, (record_id, ))
            self.con.commit()


    def update_schedule_record(self, record_id, clolumn_name, new_value):
        value = new_value
        if clolumn_name == "date_in" or clolumn_name == "date_out":
            value = self.__convert_date_input_to_date(new_value)

        with self.con.cursor() as cursor:
            query = f"UPDATE employee_management_system.schedule SET {clolumn_name}=%s WHERE id=%s"
            cursor.execute(query, (value, record_id))
            self.con.commit()


    def remove_schedules_for_deleted_employee(self, employee_id):
        with self.con.cursor() as cursor:
            query = "DELETE FROM employee_management_system.schedule WHERE employee_id=%s"
            cursor.execute(query, (employee_id,))
            self.con.commit()


    def remove_schedules_for_deleted_club(self, club_id):
        with self.con.cursor() as cursor:
            query = "DELETE FROM employee_management_system.schedule WHERE club_id=%s"
            cursor.execute(query, (club_id,))
            self.con.commit()


    def delete_past_delegations(self):
        current_schedule = Exporter()
        schedule_data = current_schedule.export_complete_schedule()
        for data in schedule_data:
            if data["date_out"] < date.today():
                with self.con.cursor() as cursor:
                    query = "DELETE FROM employee_management_system.schedule WHERE id=%s"
                    cursor.execute(query, (data["id"]))
                    self.con.commit()
