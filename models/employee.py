from models.db import Db
from exports.exporter import Exporter
import pymysql


class Employee(Db):
    """
    Class for managing work with employees
    Inherits from Db for database access.
    Enables addition, removal, update and display of employees.
    """
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.__first_name = None
        self.__last_name = None
        self.__role = None
        self.exports = Exporter()


    @property
    def first_name(self):
        """
        Returns first name of employee
        :return: employee first name
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        """
        Sets employee first name
        :param first_name: parameter provided from user input
        """
        if not first_name or not first_name.strip():
            raise ValueError("Ime mora biti uneto")
        self.__first_name = first_name

    @property
    def last_name(self):
        """
        Returns last name of employee
        :return: employee last name
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        """
        Sets employee last name
        :param last_name: parameter provided from user input
        """
        if not last_name or not last_name.strip():
            raise ValueError("Prezime mora biti uneto")
        self.__last_name = last_name

    @property
    def role(self):
        """
        Returns role of the employee
        :return: employee role
        """
        return self.__role

    @role.setter
    def role(self, role):
        """
        Sets role of employee
        :param role: parameter provided from user input
        """
        if not role or not role.strip():
            raise ValueError("Pozicija mora biti uneta")
        self.__role = role


    def add_employee(self):
        """
        Inserts a new employee record into the database using previously set values.
        Sets delegated status to False by default.
        """
        try:
            with self.con.cursor() as cursor:
                query = ("INSERT INTO employee_management_system.employees "
                         "(first_name, last_name, role, delegated) "
                         "VALUES (%s, %s, %s, %s)")
                cursor.execute(query, (self.__first_name, self.__last_name, self.__role, False))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri upisu zaposlenog: {e}")


    def delete_employee(self, employee_id):
        """
        Removal of selected employee
        :param employee_id: id of selected employee
        """
        try:
            with self.con.cursor() as cursor:
                query = "DELETE FROM employee_management_system.employees WHERE id=%s"
                cursor.execute(query, (employee_id,))
                self.con.commit()
            return employee_id
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri brisanju zaposlenog: {e}")


    def add_delegation_to_employee(self, employee_id):
        """
        Addition of delegation to selected employee
        :param employee_id: id of selected employee
        """
        try:
            with self.con.cursor() as cursor:
                query = "UPDATE employee_management_system.employees SET delegated=%s WHERE id=%s"
                cursor.execute(query, (True, employee_id))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri promeni delegacije zaposlenog: {e}")


    def remove_employee_delegation(self):
        """
        Removes delegation flag from employees whose assignments have expired
        """
        current_delegations = self.exports.export_actual_schedule()
        employee_list = self.exports.export_all_employees()
        delegated_employee_ids = [delegation["employee_id"] for delegation in current_delegations]

        for employee in employee_list:
            if employee["id"] not in delegated_employee_ids:
                try:
                    with self.con.cursor() as cursor:
                        query = "UPDATE employee_management_system.employees SET delegated=%s WHERE id=%s"
                        cursor.execute(query, (False, employee["id"]))
                        self.con.commit()
                except pymysql.MySQLError as e:
                    raise RuntimeError(f"Greska pri izmeni delegacije zaposlenog: {e}")


    def update_employee_data(self, employee_id, table_header, new_value):
        """
        Updates employee information in the database.
        :param employee_id: id of selected employee
        :param table_header: name of column which will be updated
        :param new_value: value that will replace old value
        """
        allowed_fields = {"first_name", "last_name", "role"}

        if table_header not in allowed_fields:
            raise ValueError("Izabrano polje nije validno")

        try:
            with self.con.cursor() as cursor:
                query = f"UPDATE employee_management_system.employees SET {table_header}=%s WHERE id=%s"
                cursor.execute(query, (new_value, employee_id))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri azuriranju podataka zaposlenog: {e}")
