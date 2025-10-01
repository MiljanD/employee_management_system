from utils.screens import Screens


class InputPrompts:
    def __init__(self):
        self.home_prompt_options = ["Klubovi", "Zaposleni", "Raspored", "Izlaz"]
        self.club_prompt_options = ["Lista klubova", "Dodavanje novih klubova", "Brisanje postojecih klubova"]
        self.employee_prompt_options = ["Lista zaposlenih", "Dodavanjhe novih zaposlenih", "Brisanje postojecih zaposlenih", "Izmena podataka zaposlenih", "Delegiranje"]
        self.schedule_option_prompt = ["Raspored", "Brisanje delegacije", "Azuriranje rasporeda"]
        self.screens = Screens()


    def __default_prompt(self, options):
        print("Opcije:")
        for idx, option in enumerate(options):
            print(f"{idx +1}. {option}")

        user_entry = int(input(f"Izaberite opciju({1}-{len(options)}): "))

        return user_entry


    def home_prompt(self):
        return self.__default_prompt(self.home_prompt_options)


    def clubs_prompt(self):
        return self.__default_prompt(self.club_prompt_options)


    def employees_prompt(self):
        return self.__default_prompt(self.employee_prompt_options)


    def schedule_prompt(self):
        return self.__default_prompt(self.schedule_option_prompt)


    def club_addition_prompt(self):
        club_name = input("Unesite ime kluba: ").capitalize()
        return club_name


    def delete_club_selection(self):
        self.screens.show_list_of_clubs()
        club_id = int(input("Izaberite ID kluba koji zelite da obrisete:"))
        return club_id


    def employee_addition_prompt(self):
        first_name = input("Unesite ime zaposlenog: ").capitalize()
        last_name = input("Unesite prezime zaposlenog: ").capitalize()
        role = input("Unesite poziciju zaposlenog: ").capitalize()
        return {"first_name": first_name, "last_name": last_name, "role": role}


    def delete_employee_selection(self):
        self.screens.show_list_of_employees()
        employee_id = int(input("Izaberite ID zaposlenog kojeg zelite da obrisete: "))
        return employee_id


    def schedule_generation_prompt(self):
        self.screens.show_list_of_clubs()
        club_id = int(input("Izaberite ID kluba: "))
        self.screens.show_list_of_employees()
        employee_id = int(input("Unesite ID zaposlenog: "))
        date_in = input("Unesite pocetni datum delegacije(dd-mm-yyyy): ")
        date_out = input("Unesite zavrsni datum delegacije(dd-mm-yyyy): ")

        return {"club_id": club_id, "employee_id": employee_id, "date_in": date_in, "date_out": date_out}


    def employee_data_update(self):
        self.screens.show_list_of_employees()
        employee_id = int(input("Izaberite ID zaposlenog: "))
        column_data = {"Ime": "first_name", "Prezime": "last_name", "Pozicija": "role"}
        column_names = [key for key, value in column_data.items()]
        hint = f"{column_names[0]}/{column_names[1]}/{column_names[2]}"
        column_name_choice = input(f"Unesite podatak koji zelite izmeniti({hint}): ").capitalize()
        new_value = input("Unesite novu vrednost za izabrani podatak: ").capitalize()

        return {"employee_id": employee_id, "column_name": column_data[column_name_choice], "new_value": new_value}


    def schedule_data_update(self):
        column_data = {"Id kluba": "club_id", "Id zaposlenog": "employee_id", "Pocetak delegacije": "date_in",
                        "Zavrsetak delegacije": "date_out"}

        column_names = [key for key, value in column_data.items()]
        hint = f"{column_names[0]}/{column_names[1]}/{column_names[2]}/{column_names[3]}"

        new_value = None
        column_name_choice = input(f"Unesite podatak koji zelite izmeniti({hint}): ").capitalize()
        if column_name_choice == "Id kluba" or column_name_choice == "Id zaposlenog":
            new_value = int(input("Unesite novu vrednost za izabrani podatak: "))
        elif column_name_choice == "Pocetak delegacije" or column_name_choice == "Zavrsetak delegacije":
            new_value = input("Unesite novu vrednost za izabrani podatak(dd-mm-yyyy):")

        return {"column_name": column_data[column_name_choice], "new_value": new_value}
