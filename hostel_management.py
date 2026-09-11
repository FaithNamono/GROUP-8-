# NAMONO FAITH  VU-BBC-2603-2819-DAY

# ============================================================
# HOSTEL ROOM BOOKING AND FEES MANAGEMENT SYSTEM
# ============================================================
#
# This Python program is designed to help a hostel warden
# manage student registration, room allocation, hostel fees,
# payments, occupancy and student records.
#
# The system provides a simple menu-driven interface and
# allows records to be saved and loaded using a JSON file.
#
# ============================================================

import json
import os
from datetime import datetime


DATA_FILE = "hostel_data.json"


HOSTEL_FEE = 800000

# ============================================================
# 1. HOSTEL AND ROOM DATA
# ============================================================

def create_hostel_data():
    """
    Creates the initial hostel structure.
    Each room has a fixed capacity and a list of students.
    """

    hostels = {
        "Block A": {},
        "Block B": {},
        "Block C": {}
    }

    # Block A - 5 rooms, capacity 4
    for number in range(101, 106):
        room_number = f"A{number}"
        hostels["Block A"][room_number] = {
            "capacity": 4,
            "students": []
        }

    # Block B - 5 rooms, capacity 4
    for number in range(101, 106):
        room_number = f"B{number}"
        hostels["Block B"][room_number] = {
            "capacity": 4,
            "students": []
        }

    # Block C - 5 rooms, capacity 3
    for number in range(101, 106):
        room_number = f"C{number}"
        hostels["Block C"][room_number] = {
            "capacity": 3,
            "students": []
        }

    return hostels


# ============================================================
# 2. DISPLAY OCCUPANCY OVERVIEW
# ============================================================

def display_startup_occupancy(hostels):
    """
    Displays a brief occupancy overview when the program starts.
    """

    print("\n" + "=" * 60)
    print("              HOSTEL OCCUPANCY OVERVIEW")
    print("=" * 60)

    for block, rooms in hostels.items():

        total_capacity = 0
        total_occupied = 0

        for room, details in rooms.items():
            total_capacity += details["capacity"]
            total_occupied += len(details["students"])

        print(
            f"{block}: {total_occupied}/{total_capacity} "
            f"students | {len(rooms)} rooms"
        )

    print("=" * 60)


# ============================================================
# 3. SAVE DATA
# ============================================================

def save_data(hostels, students, payments):
    """
    Saves hostel, student and payment records to a JSON file.
    """

    data = {
        "hostels": hostels,
        "students": students,
        "payments": payments
    }

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

        print("\nData saved successfully.")

    except OSError as error:
        print(f"\nError saving data: {error}")


# ============================================================
# 4. LOAD DATA
# ============================================================

def load_data():
    """
    Loads saved data from the JSON file.
    If the file does not exist or is damaged,
    a fresh system is created instead.
    """

    if not os.path.exists(DATA_FILE):
        print("\nNo previous data found.")
        print("Starting a new hostel system.")

        return create_hostel_data(), {}, {}

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        print("\nPrevious hostel data loaded successfully.")

        return (
            data["hostels"],
            data["students"],
            data["payments"]
        )

    except (json.JSONDecodeError, KeyError, OSError) as error:

        print("\nWarning: The saved data file is missing or damaged.")
        print("Starting with a new hostel system.")
        print(f"Details: {error}")

        return create_hostel_data(), {}, {}


# ============================================================
# 5. VALIDATE STUDENT NAME
# ============================================================

def get_student_name():
    """
    Gets and validates a student's name.
    """

    while True:

        name = input("Enter student's full name: ").strip()

        if name == "":
            print("Name cannot be empty.")

        elif len(name) < 2:
            print("Please enter a valid name.")

        elif any(char.isdigit() for char in name):
            print("Name should not contain numbers.")

        else:
            return name.title()


# ============================================================
# 6. VALIDATE REGISTRATION NUMBER
# ============================================================

def get_new_reg_number(students):
    """
    Gets and validates a NEW student registration number:
    non-empty, alphanumeric (dashes/slashes allowed), a
    sensible length, and not already in use. Typing "0"
    cancels registration entirely.
    """

    while True:

        reg_number = input(
            "Enter student registration number "
            "(or 0 to cancel): "
        ).strip().upper()

        if reg_number == "0":
            return None

        if reg_number == "":
            print("Registration number cannot be empty.")
            continue

        if len(reg_number) < 4 or len(reg_number) > 25:
            print(
                "Registration number should be between "
                "4 and 25 characters long."
            )
            continue

        cleaned = reg_number.replace("-", "").replace("/", "")

        if not cleaned.isalnum():
            print(
                "Registration number should only contain "
                "letters, numbers, '-' or '/'."
            )
            continue

        if reg_number in students:
            print(
                "A student with that registration number "
                "already exists."
            )
            continue

        return reg_number


# ============================================================
# 7. REGISTER STUDENT AND ALLOCATE ROOM
# ============================================================

def register_student(hostels, students, payments):
    """
    Registers a new student and allocates them to a specified room.
    Can be cancelled at any prompt by entering "0".
    """

    print("\n" + "=" * 60)
    print("          STUDENT REGISTRATION AND ALLOCATION")
    print("=" * 60)

    reg_number = get_new_reg_number(students)

    if reg_number is None:
        print("\nRegistration cancelled.")
        return

    name = get_student_name()

    print("\nAvailable Rooms:")

    for block, rooms in hostels.items():

        print(f"\n{block}")

        for room, details in rooms.items():

            capacity = details["capacity"]
            occupied = len(details["students"])
            available = capacity - occupied

            print(
                f"{room} - Capacity: {capacity} | "
                f"Occupied: {occupied} | "
                f"Available: {available}"
            )

    while True:

        room_number = input(
            "\nEnter room number for allocation "
            "(or 0 to cancel): "
        ).strip().upper()

        if room_number == "0":
            print("\nRegistration cancelled.")
            return

        room_found = False

        for block, rooms in hostels.items():

            if room_number in rooms:

                room_found = True

                room = rooms[room_number]

                if len(room["students"]) >= room["capacity"]:

                    print(
                        f"\nRoom {room_number} is FULL."
                    )
                    print(
                        "Please choose another room."
                    )

                else:

                    room["students"].append(reg_number)

                    students[reg_number] = {
                        "name": name,
                        "room": room_number,
                        "block": block,
                        "total_fee": HOSTEL_FEE,
                        "amount_paid": 0,
                        "balance": HOSTEL_FEE
                    }

                    payments[reg_number] = []

                    print("\nStudent registered successfully!")
                    print(f"Name: {name}")
                    print(f"Registration Number: {reg_number}")
                    print(f"Hostel: {block}")
                    print(f"Room: {room_number}")
                    print(f"Hostel Fee: UGX {HOSTEL_FEE:,}")
                    print("Amount Paid: UGX 0")
                    print(f"Outstanding Balance: UGX {HOSTEL_FEE:,}")

                    save_data(hostels, students, payments)

                    return

        if not room_found:
            print(
                "Invalid room number. Please enter a valid room."
            )


# ============================================================
# 8. DE-REGISTER STUDENT / VACATE ROOM
# ============================================================

def deregister_student(hostels, students, payments):
    """
    Removes a student from the system entirely: frees up their
    room slot and deletes their student and payment records.
    Asks for confirmation before making any change, since this
    cannot be undone.
    """

    print("\n" + "=" * 60)
    print("            DE-REGISTER STUDENT / VACATE ROOM")
    print("=" * 60)

    if not students:
        print("No students are registered.")
        return

    reg_number = input(
        "Enter student registration number "
        "(or 0 to cancel): "
    ).strip().upper()

    if reg_number == "0":
        print("\nCancelled.")
        return

    if reg_number not in students:
        print("Student not found.")
        return

    student = students[reg_number]

    print(f"\nName: {student['name']}")
    print(f"Block: {student['block']}")
    print(f"Room: {student['room']}")
    print(f"Outstanding Balance: UGX {student['balance']:,}")

    confirm = input(
        "\nThis will permanently remove this student and their "
        "payment history. Type YES to confirm: "
    ).strip().upper()

    if confirm != "YES":
        print("\nCancelled. No changes were made.")
        return

    # Free up the room slot
    block = student["block"]
    room_number = student["room"]

    if reg_number in hostels[block][room_number]["students"]:
        hostels[block][room_number]["students"].remove(reg_number)

    # Remove student and payment records
    del students[reg_number]
    payments.pop(reg_number, None)

    print(f"\n{reg_number} has been de-registered and room "
          f"{room_number} has been vacated.")

    save_data(hostels, students, payments)


# ============================================================
# 9. RECORD FEE PAYMENT
# ============================================================

def record_payment(hostels, students, payments):
    """
    Records a full or partial payment.
    Multiple payments can be made for the same student.
    """

    print("\n" + "=" * 60)
    print("                RECORD FEE PAYMENT")
    print("=" * 60)

    if not students:
        print("No students are registered yet.")
        return

    reg_number = input(
        "Enter student registration number: "
    ).strip().upper()

    if reg_number not in students:
        print("Student not found.")
        return

    student = students[reg_number]

    print(f"\nStudent Name: {student['name']}")
    print(f"Registration Number: {reg_number}")
    print(f"Total Fee: UGX {student['total_fee']:,}")
    print(f"Amount Paid: UGX {student['amount_paid']:,}")
    print(f"Outstanding Balance: UGX {student['balance']:,}")

    if student["balance"] == 0:
        print("\nThis student has already fully paid.")
        return

    while True:

        amount_input = input(
            "\nEnter payment amount (UGX): "
        ).strip()

        try:
            amount = int(amount_input)

            if amount <= 0:
                print("Payment must be greater than zero.")

            elif amount > student["balance"]:
                print(
                    f"Payment cannot exceed the outstanding "
                    f"balance of UGX {student['balance']:,}."
                )

            else:
                break

        except ValueError:
            print("Please enter a valid whole number.")

    # Update student's payment information
    student["amount_paid"] += amount
    student["balance"] = (
        student["total_fee"] - student["amount_paid"]
    )

    payment_record = {
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    payments[reg_number].append(payment_record)

    print("\nPayment recorded successfully!")
    print(f"Payment Made: UGX {amount:,}")
    print(f"Total Paid: UGX {student['amount_paid']:,}")
    print(f"Remaining Balance: UGX {student['balance']:,}")

    if student["balance"] == 0:
        print("STATUS: FULLY PAID")
    else:
        print("STATUS: PARTIALLY PAID")

    save_data(hostels, students, payments)


# ============================================================
# 10. SEARCH STUDENT
# ============================================================

def search_student(students):
    """
    Searches for a student by name or registration number.
    """

    print("\n" + "=" * 60)
    print("                  SEARCH STUDENT")
    print("=" * 60)

    if not students:
        print("No students are registered.")
        return

    search = input(
        "Enter student name or registration number: "
    ).strip().lower()

    found = False

    for reg_number, student in students.items():

        if (
            search in student["name"].lower()
            or search in reg_number.lower()
        ):

            print("\nStudent Found")
            print("-" * 40)
            print(f"Name: {student['name']}")
            print(f"Registration Number: {reg_number}")
            print(f"Block: {student['block']}")
            print(f"Room: {student['room']}")
            print(f"Total Fee: UGX {student['total_fee']:,}")
            print(f"Amount Paid: UGX {student['amount_paid']:,}")
            print(f"Balance: UGX {student['balance']:,}")

            found = True

    if not found:
        print("\nNo student matched your search.")


# ============================================================
# 11. VIEW STUDENT DETAILS
# ============================================================

def view_student_details(students, payments):
    """
    Displays complete information about a selected student,
    including their payment history.
    """

    print("\n" + "=" * 60)
    print("                 STUDENT DETAILS")
    print("=" * 60)

    if not students:
        print("No students are registered.")
        return

    reg_number = input(
        "Enter registration number: "
    ).strip().upper()

    if reg_number not in students:
        print("Student not found.")
        return

    student = students[reg_number]

    print("\n----------------------------------------")
    print(f"Name: {student['name']}")
    print(f"Registration Number: {reg_number}")
    print(f"Block: {student['block']}")
    print(f"Room: {student['room']}")
    print(f"Total Fee: UGX {student['total_fee']:,}")
    print(f"Amount Paid: UGX {student['amount_paid']:,}")
    print(f"Outstanding Balance: UGX {student['balance']:,}")
    print("----------------------------------------")

    print("\nPayment History:")

    if not payments.get(reg_number):
        print("No payments have been made.")

    else:

        for number, payment in enumerate(
            payments[reg_number], start=1
        ):

            print(
                f"{number}. UGX {payment['amount']:,} "
                f"- {payment['date']}"
            )


# ============================================================
# 12. OCCUPANCY REPORT
# ============================================================

def occupancy_report(hostels):
    """
    Generates a full occupancy report for each hostel block.
    """

    print("\n" + "=" * 70)
    print("                    OCCUPANCY REPORT")
    print("=" * 70)

    for block, rooms in hostels.items():

        total_capacity = 0
        total_occupied = 0

        print(f"\n{block}")
        print("-" * 70)

        for room_number, details in rooms.items():

            capacity = details["capacity"]
            occupied = len(details["students"])
            available = capacity - occupied

            total_capacity += capacity
            total_occupied += occupied

            if occupied == capacity:
                status = "FULL"
            elif occupied == 0:
                status = "EMPTY"
            else:
                status = "AVAILABLE"

            print(
                f"{room_number}: "
                f"{occupied}/{capacity} occupied | "
                f"{available} spaces left | "
                f"{status}"
            )

        print(
            f"\n{block} Total: "
            f"{total_occupied}/{total_capacity} occupied"
        )


# ============================================================
# 13. FEE DEFAULTERS
# ============================================================

def fee_defaulters(students):
    """
    Displays students whose outstanding balance is
    greater than a user-specified threshold.
    """

    print("\n" + "=" * 60)
    print("                   FEE DEFAULTERS")
    print("=" * 60)

    if not students:
        print("No students are registered.")
        return

    while True:

        threshold_input = input(
            "Enter outstanding balance threshold (UGX): "
        ).strip()

        try:
            threshold = int(threshold_input)

            if threshold < 0:
                print("Threshold cannot be negative.")
            else:
                break

        except ValueError:
            print("Please enter a valid whole number.")

    found = False

    print(
        f"\nStudents with outstanding balance above "
        f"UGX {threshold:,}:"
    )

    print("-" * 70)

    for reg_number, student in students.items():

        if student["balance"] > threshold:

            print(
                f"Name: {student['name']}\n"
                f"Registration Number: {reg_number}\n"
                f"Room: {student['room']}\n"
                f"Outstanding Balance: "
                f"UGX {student['balance']:,}"
            )

            print("-" * 70)

            found = True

    if not found:
        print("No students meet the defaulter criteria.")


# ============================================================
# 14. VIEW ALL STUDENTS
# ============================================================

def view_all_students(students):
    """
    Displays all registered students.
    """

    print("\n" + "=" * 80)
    print("                     ALL REGISTERED STUDENTS")
    print("=" * 80)

    if not students:
        print("No students are registered.")
        return

    print(
        f"{'Reg Number':<18}"
        f"{'Name':<25}"
        f"{'Room':<10}"
        f"{'Paid':<15}"
        f"{'Balance':<15}"
    )

    print("-" * 80)

    for reg_number, student in students.items():

        print(
            f"{reg_number:<18}"
            f"{student['name']:<25}"
            f"{student['room']:<10}"
            f"UGX {student['amount_paid']:<10,}"
            f"UGX {student['balance']:<10,}"
        )


# ============================================================
# 15. MAIN MENU
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("       HOSTEL ROOM BOOKING AND FEES MANAGEMENT")
    print("=" * 60)

    # Load saved records
    hostels, students, payments = load_data()

    # Display occupancy when program starts
    display_startup_occupancy(hostels)

    while True:

        print("\n")
        print("=" * 60)
        print("                    MAIN MENU")
        print("=" * 60)

        print("1.  Register Student and Allocate Room")
        print("2.  De-register Student / Vacate Room")
        print("3.  Record Fee Payment")
        print("4.  Search Student")
        print("5.  View Student Details")
        print("6.  View Occupancy Report")
        print("7.  View Fee Defaulters")
        print("8.  View All Students")
        print("9.  Save Data")
        print("10. Exit")

        print("=" * 60)

        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":

            register_student(
                hostels,
                students,
                payments
            )

        elif choice == "2":

            deregister_student(
                hostels,
                students,
                payments
            )

        elif choice == "3":

            record_payment(
                hostels,
                students,
                payments
            )

        elif choice == "4":

            search_student(students)

        elif choice == "5":

            view_student_details(
                students,
                payments
            )

        elif choice == "6":

            occupancy_report(hostels)

        elif choice == "7":

            fee_defaulters(students)

        elif choice == "8":

            view_all_students(students)

        elif choice == "9":

            save_data(
                hostels,
                students,
                payments
            )

        elif choice == "10":

            save_data(
                hostels,
                students,
                payments
            )

            print("\nThank you for using the Hostel Management System.")
            print("Goodbye!")

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select a number from 1 to 10."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()