from models.employee import Employee
from models.clubs import Club
from models.schedule import Schedule
from utils.input_prompts import (home_prompt, clubs_prompt, employees_prompt,
                                 schedule_prompt, club_addition_prompt, delete_club_selection,
                                 employee_addition_prompt, delete_employee_selection,
                                 schedule_generation_prompt, employee_data_update)
from utils.screens import show_list_of_clubs, show_list_of_employees, show_schedule


is_running = True

while is_running:
    user_choice = home_prompt()

    schedule = Schedule()

    if user_choice == 1:
        club = Club()

        club_option_choice = clubs_prompt()
        if club_option_choice == 1:
            show_list_of_clubs()

        elif club_option_choice == 2:
            club_name = club_addition_prompt()
            club.club = club_name
            club.add_club()

        elif club_option_choice == 3:
            club_id = delete_club_selection()
            schedule.remove_schedules_for_deleted_club(club_id)
            club.delete_club(club_id)

    elif user_choice == 2:
        employee = Employee()
        employee.remove_employee_delegation()

        employee_option_choice = employees_prompt()

        if employee_option_choice == 1:
            show_list_of_employees()

        elif employee_option_choice == 2:
            employee_data = employee_addition_prompt()
            employee.first_name = employee_data["first_name"]
            employee.last_name = employee_data["last_name"]
            employee.role = employee_data["role"]
            employee.add_employee()

        elif employee_option_choice == 3:
            employee_id = delete_employee_selection()
            schedule.remove_schedules_for_deleted_employee(employee_id)
            employee.delete_employee(employee_id)

        elif employee_option_choice == 4:
            update_data = employee_data_update()
            employee.update_employee_data(update_data["employee_id"], update_data["column_name"], update_data["new_value"])

        elif employee_option_choice == 5:
            schedule_data = schedule_generation_prompt()
            schedule.id_of_club = schedule_data["club_id"]
            schedule.id_of_employee = schedule_data["employee_id"]
            schedule.delegation_in = schedule_data["date_in"]
            schedule.delegation_out = schedule_data["date_out"]
            schedule.generate_schedule()
            employee.add_delegation_to_employee(schedule_data["employee_id"])

    elif user_choice == 3:
        schedule_option_choice = schedule_prompt()
        if schedule_option_choice == 1:
            show_schedule()

    elif user_choice == 4:
        print("Gasenje programa...")
        is_running = False


