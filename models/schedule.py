from models.db import Db
from datetime import date
from exports.exporter import Exporter
import pymysql


class Schedule(Db):
    schedule_column_names = ["club_id", "employee_id", "date_in","date_out"]

    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.club_id = None
        self.employee_id = None
        self.start_date = None
        self.end_date = None
        self.exports = Exporter()


    def __convert_date_input_to_date(self, date_input):
        date_data_collection = [int(date_data) for date_data in date_input.split("-")]
        try:
            converted_date = date(day=date_data_collection[0],
                                  month=date_data_collection[1],
                                  year=date_data_collection[2])
        except ValueError:
            raise ValueError("Datum nije validan. Format mora biti dd-mm-yyyy.")

        return converted_date


    @property
    def id_of_club(self):
        return self.club_id

    @id_of_club.setter
    def id_of_club(self, club_id):
        if not  club_id or not club_id.strip():
            raise ValueError("ID kluba mora biti unesen.")
        self.club_id = int(club_id)

    @property
    def id_of_employee(self):
        return self.employee_id

    @id_of_employee.setter
    def id_of_employee(self, employee_id):
        if not  employee_id or not employee_id.strip():
            raise ValueError("ID zaposlenog mora biti unesen.")
        self.employee_id = int(employee_id)

    @property
    def delegation_in(self):
        return self.start_date

    @delegation_in.setter
    def delegation_in(self, start_date):
        if not  start_date or not start_date.strip():
            raise ValueError("Pocetni datum delegacije mora biti unesen.")
        self.start_date = self.__convert_date_input_to_date(start_date)

    @property
    def delegation_out(self):
        return self.end_date

    @delegation_out.setter
    def delegation_out(self, end_date):
        if not  end_date or not end_date.strip():
            raise ValueError("Zavrsni datum delegacije mora biti unesen.")
        self.end_date = self.__convert_date_input_to_date(end_date)


    def check_employee_delegation(self):
        current_delegation = self.exports.export_actual_schedule()
        if not current_delegation:
            return True
        else:
            for delegation in current_delegation:
                if delegation["employee_id"] == self.employee_id:
                    return False
            return True


    def generate_schedule(self):
        if self.check_employee_delegation():
            with self.con.cursor() as cursor:
                try:
                    query = ("INSERT INTO employee_management_system.schedule (club_id, employee_id, date_in, date_out) "
                             "VALUES (%s, %s, %s, %s)")
                    cursor.execute(query, (self.club_id, self.employee_id, self.start_date, self.end_date))
                    self.con.commit()
                except pymysql.MySQLError as e:
                    raise RuntimeError(f"Greska pri generisanju rasporeda: {e}")
        else:
            print("Zaposleni je vec delegiran.")


    def delete_schedule_record(self, record_id):
        try:
            with self.con.cursor() as cursor:
                query = "DELETE FROM employee_management_system.schedule WHERE id=%s"
                cursor.execute(query, (record_id, ))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri brisanju red iz rasporeda: {e}")


    def update_schedule_record(self, record_id, column_name, new_value):
        if column_name not in Schedule.schedule_column_names:
            raise ValueError("Izabrano polje nije validno")

        value = new_value
        if column_name == "date_in" or column_name == "date_out":
            value = self.__convert_date_input_to_date(new_value)
        try:
            with self.con.cursor() as cursor:
                query = f"UPDATE employee_management_system.schedule SET {column_name}=%s WHERE id=%s"
                cursor.execute(query, (value, record_id))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri azuriranju reda u rasporedu: {e}")


    def remove_schedules_for_deleted_employee(self, employee_id):
        try:
            with self.con.cursor() as cursor:
                query = "DELETE FROM employee_management_system.schedule WHERE employee_id=%s"
                cursor.execute(query, (employee_id,))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri brasnju rasporeda obrisanog radnika: {e}")


    def remove_schedules_for_deleted_club(self, club_id):
        try:
            with self.con.cursor() as cursor:
                query = "DELETE FROM employee_management_system.schedule WHERE club_id=%s"
                cursor.execute(query, (club_id,))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri brisanju rasporeda za obrisani klub")


    def delete_past_delegations(self):
        schedule_data = self.exports.export_complete_schedule()
        for data in schedule_data:
            if data["date_out"] < date.today():
                try:
                    with self.con.cursor() as cursor:
                        query = "DELETE FROM employee_management_system.schedule WHERE id=%s"
                        cursor.execute(query, (data["id"]))
                        self.con.commit()
                except pymysql.MySQLError as e:
                    raise RuntimeError(f"Greska pri brisanju starih rasporeda: {e}")
