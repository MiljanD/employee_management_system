from exports.exporter import Exporter
from prettytable import PrettyTable


class Screens(Exporter):
    def __init__(self):
        super().__init__()


    def show_list_of_clubs(self):
        club_table = PrettyTable()
        list_of_clubs = self.export_all_clubs()

        club_table.field_names = ["ID kluba", "Naziv kluba"]
        for club in list_of_clubs:
            club_table.add_row([club["id"], club["club_name"]])

        print(club_table)


    def show_list_of_employees(self):
        list_of_employees = self.export_all_employees()
        employee_table = PrettyTable()

        employee_table.field_names = ["ID zaposlenog", "Ime", "Prezime", "Pozicija", "Delegiran"]
        for employee in list_of_employees:
            if employee["delegated"] == 0:
                delegation = "Ne"
            elif employee["delegated"] == 1:
                delegation = "Da"
            else:
                delegation = "Ne"

            employee_table.add_row([employee["id"], employee["first_name"], employee["last_name"],
                                      employee["role"],delegation])

        print(employee_table)


    def show_schedule(self):
        schedule = self.export_complete_actual_schedule_data()
        schedule_table = PrettyTable()

        schedule_table.field_names = ["ID rasporeda", "Naziv kluba", "Ime", "Prezime", "Pozicija", "Delegiran od", "Delegiran do"]

        for record in schedule:
            schedule_table.add_row([record["ID rasporeda"], record["Naziv kluba"], record["Ime"], record["Prezime"],
                                    record["Pozicija"], record["Delegiran od"], record["Delegiran do"]])

        print(schedule_table)

    def show_selected_record(self, record_id):
        selected_record = self.export_schedule_record_by_id(record_id)
        selected_record_table = PrettyTable()

        selected_record_table.field_names = ["ID kluba", "ID zaposlenog", "Pocetak delegacije", "Zavrsetak delegacije"]

        for record in selected_record:
            selected_record_table.add_row([record["club_id"], record["employee_id"], record["date_in"], record["date_out"]])

        print(selected_record_table)
