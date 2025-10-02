from models.employee import Employee
from models.clubs import Club
from models.schedule import Schedule
from utils.input_prompts import InputPrompts
from utils.screens import Screens

# Main loop of application - initiate interactive CLI system

is_running = True

while is_running:
    # Initialization of interface and displays

    prompts = InputPrompts()
    screens = Screens()
    schedule = Schedule()

    # Display of home screen and user choice

    user_choice = prompts.home_prompt()

    if user_choice == 1:
        # Work with clubs

        club = Club()
        club_option_choice = prompts.clubs_prompt()

        if club_option_choice == 1:
            # Display of all clubs

            screens.show_list_of_clubs()

        elif club_option_choice == 2:
            # Addition of new club

            club_name = prompts.club_addition_prompt()
            club.club = club_name
            club.add_club()

        elif club_option_choice == 3:
            # Removal of club and all associated delegations

            club_id = prompts.delete_club_selection()
            schedule.remove_schedules_for_deleted_club(club_id)
            club.delete_club(club_id)

    elif user_choice == 2:
        # Work with employees

        employee = Employee()
        # Removal of past delegations from active ones

        employee.remove_employee_delegation()

        employee_option_choice = prompts.employees_prompt()

        if employee_option_choice == 1:
            # Display of all employees

            screens.show_list_of_employees()

        elif employee_option_choice == 2:
            # Addition of new employee

            employee_data = prompts.employee_addition_prompt()
            employee.first_name = employee_data["first_name"]
            employee.last_name = employee_data["last_name"]
            employee.role = employee_data["role"]
            employee.add_employee()

        elif employee_option_choice == 3:
            # Removal of employee and all associated delegations

            employee_id = prompts.delete_employee_selection()
            schedule.remove_schedules_for_deleted_employee(employee_id)
            employee.delete_employee(employee_id)

        elif employee_option_choice == 4:
            # Update of employees information

            update_data = prompts.employee_data_update()
            employee.update_employee_data(update_data["employee_id"], update_data["column_name"], update_data["new_value"])

        elif employee_option_choice == 5:
            # Delegation of employee to club on certain dates

            schedule_data = prompts.schedule_generation_prompt()
            schedule.id_of_club = schedule_data["club_id"]
            schedule.id_of_employee = schedule_data["employee_id"]
            schedule.delegation_in = schedule_data["date_in"]
            schedule.delegation_out = schedule_data["date_out"]
            schedule.generate_schedule()
            employee.add_delegation_to_employee(schedule_data["employee_id"])

    elif user_choice == 3:
        # Work with schedule

        schedule_option_choice = prompts.schedule_prompt()

        if schedule_option_choice == 1:
            # Display of active schedule

            screens.show_schedule()

        elif schedule_option_choice == 2:
            # Removal of certain delegation

            screens.show_schedule()
            try:
                schedule_record_id = int(input("Unesite ID rasporeda koji zelite da obrisete: "))
            except ValueError:
                print("Unos mora biti broj.")
                continue
            schedule.delete_schedule_record(schedule_record_id)

        elif schedule_option_choice == 3:
            # Update of certain delegation

            screens.show_schedule()
            try:
                schedule_record_id = int(input("Unesite ID rasporeda koji zelite da azuririrate: "))
            except ValueError:
                print("Unos mora biti broj.")
                continue
            screens.show_selected_record(schedule_record_id)
            data_for_record_update = prompts.schedule_data_update()
            schedule.update_schedule_record(schedule_record_id, data_for_record_update["column_name"], data_for_record_update["new_value"])

    elif user_choice == 4:
        # Exit from program

        print("Gasenje programa...")
        is_running = False


