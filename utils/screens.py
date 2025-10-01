from exports.exporter import Exporter
from prettytable import PrettyTable


export = Exporter()


def show_list_of_clubs():
    club_table = PrettyTable()
    list_of_clubs = export.export_all_clubs()

    club_table.field_names = ["ID kluba", "Naziv kluba"]
    for club in list_of_clubs:
        club_table.add_row([club["id"], club["club_name"]])

    print(club_table)


def show_list_of_employees():
    list_of_employees = export.export_all_employees()
    employee_table = PrettyTable()

    employee_table.field_names = ["ID zaposlenog", "Ime", "Prezime", "Pozicija", "Delegiran"]
    for employee in list_of_employees:
        if employee["delegated"] == 0:
            delegation = "Ne"
        elif employee["delegated"] == 1:
            delegation = "Da"

        employee_table.add_row([employee["id"], employee["first_name"], employee["last_name"],
                                  employee["role"],delegation])

    print(employee_table)


def show_schedule():
    schedule = export.export_complete_actual_schedule_data()
    schedule_table = PrettyTable()

    schedule_table.field_names = ["ID rasporeda", "Naziv kluba", "Ime", "Prezime", "Pozicija", "Delegiran od", "Delegiran do"]

    for record in schedule:
        schedule_table.add_row([record["ID rasporeda"], record["Naziv kluba"], record["Ime"], record["Prezime"],
                                record["Pozicija"], record["Delegiran od"], record["Delegiran do"]])

    print(schedule_table)

def show_selected_record(record_id):
    selected_record = export.export_schedule_record_by_id(record_id)
    selected_record_table = PrettyTable()

    selected_record_table.field_names = ["ID kluba", "ID zaposlenog", "Pocetak delegacije", "Zavrsetak delegacije"]

    for record in selected_record:
        selected_record_table.add_row([record["club_id"], record["employee_id"], record["date_in"], record["date_out"]])

    print(selected_record_table)



