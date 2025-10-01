from models.db import Db
from exports.exporter import Exporter
import pymysql


class Employee(Db):
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.__first_name = None
        self.__last_name = None
        self.__role = None
        self.exports = Exporter()


    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        if not first_name or not first_name.strip():
            raise ValueError("Ime mora biti uneto")
        self.__first_name = first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        if not last_name or not last_name.strip():
            raise ValueError("Prezime mora biti uneto")
        self.__last_name = last_name

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        if not role or not role.strip():
            raise ValueError("Pozicija mora biti uneta")
        self.__role = role


    def add_employee(self):
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
        try:
            with self.con.cursor() as cursor:
                query = "DELETE FROM employee_management_system.employees WHERE id=%s"
                cursor.execute(query, (employee_id,))
                self.con.commit()
            return employee_id
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri brisanju zaposlenog: {e}")


    def add_delegation_to_employee(self, employee_id):
        try:
            with self.con.cursor() as cursor:
                query = "UPDATE employee_management_system.employees SET delegated=%s WHERE id=%s"
                cursor.execute(query, (True, employee_id))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri promeni delegacije zaposlenog: {e}")


    def remove_employee_delegation(self):
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
