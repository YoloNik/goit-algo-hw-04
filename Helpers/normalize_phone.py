import re
def normalize_phone(phone_number:str):
	"""normalize phone number 

	Args:
		phone_number (str): raw phone number

	Returns:
		_type_: cleaned phone number
	"""
	cleaned = re.sub(r'[^\d+]', '', phone_number.strip())

	if cleaned.startswith('+'):
		if cleaned.startswith('+380'):
			return cleaned
		else:
			return cleaned

	if cleaned.startswith('380'): return '+' + cleaned
	return '+38' + cleaned

