from models.db import Db
from datetime import date
from exports.exporter import Exporter
import pymysql


class Schedule(Db):
    """
    Class for managing of delegation schedule of employees in the clubs.

    Inherits from Db for database access.
    Enables addition, removal, update and display of delegations.
    """
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
        """
        Converts user input in date object
        :param date_input: provided from user input in dd-mm-yyyy format
        :return: datetime.date object to be stored in the database
        """
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
        """
        Returns club id which is currently delegated to schedule
        :return: ID of the club
        """
        return self.club_id

    @id_of_club.setter
    def id_of_club(self, club_id):
        """
        Sets the value of  club id which is currently delegated to schedule
        :param club_id: parameter provided from user input
        """
        if not  club_id or not club_id.strip():
            raise ValueError("ID kluba mora biti unesen.")
        self.club_id = int(club_id)

    @property
    def id_of_employee(self):
        """
        Returns employee id which is currently delegated to schedule
        :return: ID of the employee
        """
        return self.employee_id

    @id_of_employee.setter
    def id_of_employee(self, employee_id):
        """
        Sets the value of  employee id which is currently delegated to schedule
        :param employee_id: parameter provided from user input
        """
        if not  employee_id or not employee_id.strip():
            raise ValueError("ID zaposlenog mora biti unesen.")
        self.employee_id = int(employee_id)

    @property
    def delegation_in(self):
        """
        Returns start date of current delegation to schedule
        :return: delegation start date
        """
        return self.start_date

    @delegation_in.setter
    def delegation_in(self, start_date):
        """
        Sets start date of current delegation to schedule
        :param start_date: parameter provided from user input
        """
        if not  start_date or not start_date.strip():
            raise ValueError("Pocetni datum delegacije mora biti unesen.")
        self.start_date = self.__convert_date_input_to_date(start_date)

    @property
    def delegation_out(self):
        """
        Returns start date of current delegation to schedule
        :return: delegation end date
        """
        return self.end_date

    @delegation_out.setter
    def delegation_out(self, end_date):
        """
        Sets end date of current delegation to schedule
        :param end_date: parameter provided from user input
        """
        if not  end_date or not end_date.strip():
            raise ValueError("Zavrsni datum delegacije mora biti unesen.")
        self.end_date = self.__convert_date_input_to_date(end_date)


    def check_employee_delegation(self):
        """
        Checks is selected employee already delegated
        :return: True if employee is not currently delegated, False otherwise
        """
        current_delegation = self.exports.export_actual_schedule()
        if not current_delegation:
            return True
        else:
            for delegation in current_delegation:
                if delegation["employee_id"] == self.employee_id:
                    return False
            return True


    def generate_schedule(self):
        """
        Generates delegation schedule with previously entered values
        """
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
        """
        Removal of selected record from active schedule
        :param record_id: id of selected record
        """
        try:
            with self.con.cursor() as cursor:
                query = "DELETE FROM employee_management_system.schedule WHERE id=%s"
                cursor.execute(query, (record_id, ))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri brisanju reda u rasporeda: {e}")


    def update_schedule_record(self, record_id, column_name, new_value):
        """
        Update information from selected record from active schedule
        :param record_id: id of selected record
        :param column_name: name of column which will be updated
        :param new_value: value that will replace perviosly inserted value
        """
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
        """
        Removal of delegations associated to removed employee.
        :param employee_id: id of removed employee
        """
        try:
            with self.con.cursor() as cursor:
                query = "DELETE FROM employee_management_system.schedule WHERE employee_id=%s"
                cursor.execute(query, (employee_id,))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri brisnju rasporeda obrisanog radnika: {e}")


    def remove_schedules_for_deleted_club(self, club_id):
        """
        Removal of delegations associated to removed club.
        :param club_id: id of removed club
        """
        try:
            with self.con.cursor() as cursor:
                query = "DELETE FROM employee_management_system.schedule WHERE club_id=%s"
                cursor.execute(query, (club_id,))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri brisanju rasporeda za obrisani klub")


    def delete_past_delegations(self):
        """
        Deletes all schedule records whose end date is earlier than today.
        Used for maintaining a clean and up-to-date schedule table.
        """
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
