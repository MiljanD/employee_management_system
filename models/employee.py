from models.db import Db


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
                     "(first_name, last_name, role) "
                     "VALUES (%s, %s, %s)")
            cursor.execute(query, (self.__first_name, self.__last_name, self.__role))
            self.con.commit()



if __name__ == "__main__":
    employee = Employee()
    employee.first_name = "Miljan"
    employee.last_name = "Duvnjak"
    employee.role = "Student"
    employee.add_employee()


