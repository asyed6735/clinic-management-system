"""
Clinic Management System
Author: Abrar Hussain Syed

This program manages patient records, tracks visits, and provides
health advice based on blood pressure and BMI using OOP.
"""

# Import required modules for working with dates
from datetime import date, datetime


# ---------------------------- PATIENT CLASS ----------------------------
class Patient:
    """
    Represents a single patient.

    Stores:
    - Basic patient info (name, DOB, height)
    - Visit history (list of past visits)

    Each visit includes vitals, calculated BMI, and advice.
    """

    def __init__(self, name, dob, height):
        self.name = name
        self.dob = dob
        self.height = height  # stored once and reused for BMI
        self.visits = []      # list to store visit history

    # Calculate BMI using standard formula
    def calculate_bmi(self, weight):
        return (weight / (self.height ** 2)) * 703

    # Analyze blood pressure and return health advice
    def blood_pressure_advice(self, bp):
        try:
            systolic, diastolic = map(int, bp.split("/"))

            # Prevent unrealistic inputs
            if systolic > 300 or diastolic > 200:
                return "❌ Unusually high BP reading. Please recheck input."

            # BP classification logic
            if systolic < 120 and diastolic < 80:
                return "Normal blood pressure."
            elif 120 <= systolic < 130 and diastolic < 80:
                return "Elevated blood pressure."
            elif (130 <= systolic < 140) or (80 <= diastolic < 90):
                return "Stage 1 hypertension."
            elif systolic >= 140 or diastolic >= 90:
                return "Stage 2 hypertension. Consult a doctor."

        except ValueError:
            return "Invalid blood pressure format."

    # Analyze BMI and return weight category
    def weight_advice(self, bmi):
        if bmi < 18.5:
            return f"Underweight (BMI {bmi:.1f})"
        elif bmi < 25:
            return f"Normal weight (BMI {bmi:.1f})"
        elif bmi < 30:
            return f"Overweight (BMI {bmi:.1f})"
        else:
            return f"Obese (BMI {bmi:.1f})"

    # Add a new visit to the patient's history
    def add_visit(self, bp, weight):
        """
        Each visit stores:
        - Date (user input or today's date)
        - Blood pressure
        - Weight
        - Calculated BMI
        - Advice for BP and weight
        """

        # Allow optional date input
        user_date = input("Enter visit date (YYYY-MM-DD) or press Enter for today: ").strip()

        if user_date == "":
            visit_date = date.today().isoformat()
        else:
            try:
                # Validate correct date format
                datetime.strptime(user_date, "%Y-%m-%d")
                visit_date = user_date
            except ValueError:
                print("❌ Invalid date format. Using today’s date.")
                visit_date = date.today().isoformat()

        # Calculate BMI based on weight and stored height
        bmi = self.calculate_bmi(weight)

        # Store visit data in a dictionary
        visit = {
            "date": visit_date,
            "bp": bp,
            "weight": weight,
            "bmi": bmi,
            "bp_advice": self.blood_pressure_advice(bp),
            "weight_advice": self.weight_advice(bmi)
        }

        # Append visit to history list
        self.visits.append(visit)

    # Defines how patient info is displayed
    def __str__(self):
        return f"{self.name} | DOB: {self.dob} | Height: {self.height} in"


# ---------------------------- CLINIC SYSTEM ----------------------------
class ClinicSystem:
    """
    Controls entire system:
    - Stores all patients
    - Handles user input
    - Runs program menu
    """

    def __init__(self):
        self.patients = []  # list of Patient objects

    # Check if patient already exists (same name + DOB)
    def is_duplicate(self, name, dob):
        for patient in self.patients:
            if patient.name.lower() == name.lower() and patient.dob == dob:
                return True
        return False

    # Add a new patient
    def add_patient(self):
        try:
            name = input("Patient name: ").strip()

            # Validate name: only letters and spaces
            if not name.replace(" ", "").isalpha():
                print("❌ Name must contain only letters.\n")
                return

            dob = input("Date of birth (YYYY-MM-DD): ").strip()

            # Validate date format
            try:
                datetime.strptime(dob, "%Y-%m-%d")
            except ValueError:
                print("❌ Invalid date format.\n")
                return

            height = float(input("Height (in inches): "))

            # Prevent duplicate patients
            if self.is_duplicate(name, dob):
                print("❌ Patient already exists.\n")
                return

            # Create and store new patient
            self.patients.append(Patient(name, dob, height))

            print("✅ Patient added successfully.")
            print("ℹ️ Use 'Add Visit' to enter BP and weight.\n")

        except ValueError:
            print("❌ Height must be numeric.\n")

    # Add a visit to an existing patient
    def add_visit(self):
        if not self.patients:
            print("No patients available.\n")
            return

        self.list_patients()

        try:
            index = int(input("Select patient number: ")) - 1
            patient = self.patients[index]

            bp = input("Blood pressure (e.g., 120/80): ").strip()

            # Validate BP format
            if "/" not in bp:
                print("❌ Invalid BP format.\n")
                return

            systolic, diastolic = bp.split("/")

            # Ensure BP values are numeric
            if not (systolic.isdigit() and diastolic.isdigit()):
                print("❌ BP must be numeric values.\n")
                return

            # Prevent unrealistic BP values
            if int(systolic) > 300 or int(diastolic) > 200:
                print("❌ BP value unrealistic.\n")
                return

            weight = float(input("Weight (lbs): "))

            # Add visit using Patient method
            patient.add_visit(bp, weight)

            visit = patient.visits[-1]

            print("\n✅ Visit recorded.")
            print(visit["bp_advice"])
            print(visit["weight_advice"], "\n")

        except (ValueError, IndexError):
            print("❌ Invalid input.\n")

    # View visit history for a selected patient
    def view_visit_history(self):
        if not self.patients:
            print("No patients available.\n")
            return

        self.list_patients()

        try:
            index = int(input("Select patient number: ")) - 1
            patient = self.patients[index]

            if not patient.visits:
                print("No visits recorded.\n")
                return

            print(f"\n--- Visit History for {patient.name} ---")

            # Loop through each visit and display details
            for visit in patient.visits:
                print(
                    f"Date: {visit['date']} | "
                    f"BP: {visit['bp']} | "
                    f"Weight: {visit['weight']} lbs | "
                    f"BMI: {visit['bmi']:.1f}"
                )
                print(f"  - {visit['bp_advice']}")
                print(f"  - {visit['weight_advice']}")
                print("-" * 40)

        except (ValueError, IndexError):
            print("❌ Invalid selection.\n")

    # Display all patients
    def list_patients(self):
        if not self.patients:
            print("No patients found.\n")
            return

        for i, patient in enumerate(self.patients, start=1):
            print(f"{i}. {patient}")
        print()

    # Main menu loop
    def run(self):
        """
        Runs continuously until user selects Exit.
        Uses a loop to keep program active.
        """
        while True:
            print("=== Clinic Management System ===")
            print("1. Add Patient")
            print("2. Add Visit")
            print("3. View Patients")
            print("4. View Visit History")
            print("5. Exit")

            choice = input("Choose an option (1-5): ")

            if choice == "1":
                self.add_patient()
            elif choice == "2":
                self.add_visit()
            elif choice == "3":
                self.list_patients()
            elif choice == "4":
                self.view_visit_history()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("❌ Invalid option.\n")


# ---------------------------- PROGRAM ENTRY ----------------------------
def main():
    """
    Entry point of the program.
    Creates the system and starts the menu.
    """
    system = ClinicSystem()
    system.run()


# Ensures program runs when executed directly
if __name__ == "__main__":
    main()