from utils.screens import show_list_of_clubs, show_list_of_employees


HOME_PROMPT_OPTIONS = ["Klubovi", "Zaposleni", "Raspored", "Izlaz"]
CLUBS_PROMPT_OPTIONS = ["Lista klubova", "Dodavanje novih klubova", "Brisanje postojecih klubova"]
EMPLOYEE_PROMPT_OPTIONS = ["Lista zaposlenih", "Dodavanjhe novih zaposlenih", "Brisanje postojecih zaposlenih", "Izmena podataka zaposlenih", "Delegiranje"]
SCHEDULE_PROMPT_OPTIONS = ["Raspored", "Brisanje delegacije", "Azuriranje rasporeda"]

def default_prompt(options):
    print("Opcije:")
    for idx, option in enumerate(options):
        print(f"{idx +1}. {option}")

    user_entry = int(input(f"Izaberite opciju({1}-{len(options)}): "))

    return user_entry


def home_prompt():
    return default_prompt(HOME_PROMPT_OPTIONS)


def clubs_prompt():
    return default_prompt(CLUBS_PROMPT_OPTIONS)


def employees_prompt():
    return default_prompt(EMPLOYEE_PROMPT_OPTIONS)


def schedule_prompt():
    return default_prompt(SCHEDULE_PROMPT_OPTIONS)

def club_addition_prompt():
    club_name = input("Unesite ime kluba: ")
    return club_name

def delete_club_selection():
    show_list_of_clubs()
    club_id = int(input("Izaberite ID kluba koji zelite da obrisete:"))
    return club_id

def employee_addition_prompt():
    first_name = input("Unesite ime zaposlenog: ")
    last_name = input("Unesite prezime zaposlenog: ")
    role = input("Unesite poziciju zaposlenog: ")
    return {"first_name": first_name, "last_name": last_name, "role": role}

def delete_employee_selection():
    show_list_of_employees()
    employee_id = int(input("Izaberite ID zaposlenog kojeg zelite da obrisete: "))
    return employee_id

def schedule_generation_prompt():
    show_list_of_clubs()
    club_id = int(input("Izaberite ID kluba: "))
    show_list_of_employees()
    employee_id = int(input("Unesite ID zaposlenog: "))
    date_in = input("Unesite pocetni datum delegacije(dd-mm-yyyy): ")
    date_out = input("Unesite zavrsni datum delegacije(dd-mm-yyyy): ")

    return {"club_id": club_id, "employee_id": employee_id, "date_in": date_in, "date_out": date_out}


def employee_data_update():
    show_list_of_employees()
    employee_id = int(input("Izaberite ID zaposlenog: "))
    column_data = {"Ime": "first_name", "Prezime": "last_name", "Pozicija": "role"}
    column_names = [key for key, value in column_data.items()]
    hint = f"{column_names[0]}/{column_names[1]}/{column_names[2]}"
    column_name_choice = input(f"Unesite podatak koji zelite izmeniti({hint}): ").capitalize()
    new_value = input("Unesite novu vrednost za izabrani podatak: ")

    return {"employee_id": employee_id, "column_name": column_data[column_name_choice], "new_value": new_value}




