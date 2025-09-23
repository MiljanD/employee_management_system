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
        self.__club_name = club_name.capitalize()


    def add_club(self):
        with self.con.cursor() as cursor:
            query = "INSERT INTO employee_management_system.clubs (club_name) VALUES (%s)"
            cursor.execute(query, (self.__club_name, ))
            self.con.commit()



if __name__ == "__main__":
    club = Club()
    club.club = "moj klub"
    print(club.club)
    club.add_club()

