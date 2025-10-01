from models.db import Db
from exports.exporter import Exporter


class Employee(Db):
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.__first_name = None
        self.__last_name = None
        self.__role = None


    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        self.__first_name = first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role


    def add_employee(self):
        with self.con.cursor() as cursor:
            query = ("INSERT INTO employee_management_system.employees "
                     "(first_name, last_name, role, delegated) "
                     "VALUES (%s, %s, %s, %s)")
            cursor.execute(query, (self.__first_name, self.__last_name, self.__role, False))
            self.con.commit()


    def delete_employee(self, employee_id):
        with self.con.cursor() as cursor:
            query = "DELETE FROM employee_management_system.employees WHERE id=%s"
            cursor.execute(query, (employee_id,))
            self.con.commit()
        return employee_id


    def add_delegation_to_employee(self, employee_id):
            with self.con.cursor() as cursor:
                query = "UPDATE employee_management_system.employees SET delegated=%s WHERE id=%s"
                cursor.execute(query, (1, employee_id))
                self.con.commit()


    def remove_employee_delegation(self):
        exports = Exporter()
        current_delegations = exports.export_actual_schedule()
        employee_list = exports.export_all_employees()
        delegated_employee_ids = [delegation["employee_id"] for delegation in current_delegations]

        for employee in employee_list:
            if employee["id"] not in delegated_employee_ids:
                with self.con.cursor() as cursor:
                    query = "UPDATE employee_management_system.employees SET delegated=%s WHERE id=%s"
                    cursor.execute(query, (0, employee["id"]))
                    self.con.commit()

    def update_employee_data(self, employee_id, table_header, new_value):
        with self.con.cursor() as cursor:
            query = f"UPDATE employee_management_system.employees SET {table_header}=%s WHERE id=%s"
            cursor.execute(query, (new_value, employee_id))
            self.con.commit()
