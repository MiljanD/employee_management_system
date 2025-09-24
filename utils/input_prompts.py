

def generate_schedule_input_prompt():
    club_id = input("ID kluba: ")
    employee_id = input("ID zaposlenog: ")
    delegation_in = input("Pocetni datum delegacije: ")
    delegation_out = input("Zavrsni datum delegacije: ")

    return {"club_id": club_id, "employee_id": employee_id,
            "delegation_in": delegation_in, "delegation_out": delegation_out}

