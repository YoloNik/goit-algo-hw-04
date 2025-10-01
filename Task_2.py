import os

cat_info = []

def get_cats_info(path: str) -> list:
	cat_info = []
	try:
		with open(path, "r") as file:
			for line in file:
				parts = line.strip().split(",")
				if len(parts) != 3:
					print(f"Warning: corrupted line skipped: {line.strip()}")
					continue
				id, name, age = parts
				try:
					cat_info.append({"id": id, "name": name, "age": age})
				except ValueError:
					print(f"Warning: invalid age value skipped: {age}")
	except FileNotFoundError:
		print(f"Error: File '{path}' not found.")
		return []
	except Exception as e:
		print(f"Error reading file: {e}")
		return []
	return cat_info

if __name__ == "__main__":
	cats_info = get_cats_info("./DB_files/cats_file.txt")
	print(cats_info)

