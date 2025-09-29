import os

employees_salary = []

path = './DB_files'
os.makedirs(path, exist_ok=True)

salary_file = f"{path}/salary_file.txt"
if os.path.exists(salary_file):
    with open(salary_file, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 2:
                employees_salary.append({"name": parts[0], "salary": parts[1]})


def add_or_update_employee(name, salary):
    for emp in employees_salary:
        if emp['name'] == name:
            print(f"Salary for {name} already exists and is {emp['salary']}.")
            choice = input("Do you want to update the salary? (y/n): ").strip().lower()
            if choice == 'y':
                emp['salary'] = salary
                print(f"Salary for {name} updated.")
            else:
                print("Salary not changed.")
            return
    employees_salary.append({"name": name, "salary": salary})
    print(f"Employee {name} added.")

def manage_employees():
    while True:
        name = input("Enter employee name (or 'q' to quit): ").strip()
        if name.lower() == 'q':
            break
        name = name.title()
        salary = input(f"Enter salary for {name}: ").strip()
        add_or_update_employee(name, salary)





with open(salary_file, "w") as file:
    for emp in employees_salary:
        file.write(f"{emp['name']},{emp['salary']}\n")

if __name__ == "__main__":
    manage_employees()
    