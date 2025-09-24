from models.db import Db
from datetime import date
from utils.input_prompts import generate_schedule_input_prompt


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


    def generate_schedule(self):
        with self.con.cursor() as cursor:
            query = ("INSERT INTO employee_management_system.schedule (club_id, employee_id, date_in, date_out) "
                     "VALUES (%s, %s, %s, %s)")
            cursor.execute(query, (self.club_id, self.employee_id, self.start_date, self.end_date))
            self.con.commit()



if __name__ == "__main__":
    schedule = Schedule()
    schedule_data = generate_schedule_input_prompt()
    print(schedule_data)
    schedule.generate_schedule()



