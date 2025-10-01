import os

path = './DB_files/salary.txt'

def total_salary(path:str) ->tuple:
	employees_salary = []
	try:
		with open(path, "r") as file:
			for line in file:
				parts = line.strip().split(",")
				if len(parts) != 2:
					print(f"Warning: corrupted line skipped: {line.strip()}")
					continue
				name, salary = parts
				try:
					employees_salary.append({"name": str(name), "salary": float(salary)})
				except ValueError:
					print(f"Warning: invalid salary value skipped: {salary}")
	except FileNotFoundError:
		print(f"Error: File '{path}' not found.")
		return 0, 0
	except Exception as e:
		print(f"Error reading file: {e}")
		return 0, 0
	emploee_qty = len(employees_salary)
	total = sum(emp["salary"] for emp in employees_salary)
	avg = total / emploee_qty if emploee_qty > 0 else 0
	return int(total), int(avg)
		


if __name__ == "__main__":
	total, average = total_salary(path)
	print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")


