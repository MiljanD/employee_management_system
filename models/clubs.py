import pymysql
from models.db import Db


class Club(Db):
    def __init__(self):
        super().__init__()
        self.con = self._get_connection()
        self.__club_name = None


    @property
    def club(self):
        return self.__club_name


    @club.setter
    def club(self, club_name):
        if not club_name or not club_name.strip():
            raise ValueError("Naziv kluba mora da bude unesen.")

        self.__club_name = club_name.capitalize()


    def add_club(self):
        try:
            with self.con.cursor() as cursor:
                query = "INSERT INTO employee_management_system.clubs (club_name) VALUES (%s)"
                cursor.execute(query, (self.__club_name, ))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri dodavanju kluba: {e}")

    def delete_club(self, club_id):
        try:
            with self.con.cursor() as cursor:
                query = "DELETE FROM employee_management_system.clubs WHERE id=%s"
                cursor.execute(query, (club_id,))
                self.con.commit()
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Greska pri brisanju kluba: {e}")

        return club_id
