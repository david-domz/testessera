from datetime import datetime, timedelta
import random


_ZULU_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

_PERSON_NAMES = [
	"Liam",
	"Emma",
	"Noah",
	"Olivia",
	"William",
	"Ava",
	"James",
	"Isabella",
	"Oliver",
	"Sophia",
	"Benjamin",
	"Mia",
	"Elijah",
	"Charlotte",
	"Lucas",
	"Amelia",
	"Mason",
	"Harper",
	"Logan",
	"Evelyn",
	"Alexander",
	"Abigail",
	"Ethan",
	"Emily",
	"Daniel",
	"Madison",
	"Aiden",
	"Scarlett",
	"Matthew",
	"Elizabeth",
	"Joseph",
	"Grace",
	"Samuel",
	"Chloe",
	"Sebastian",
	"Camila",
	"David",
	"Sofia",
	"Carter",
	"Avery",
	"Wyatt",
	"Ella",
	"Jayden",
	"Mila",
	"John",
	"Aria",
	"Owen",
	"Eleanor",
	"Dylan",
	"Hannah",
	"Luke",
	"Lily",
	"Gabriel",
	"Addison",
	"Anthony",
	"Aubrey",
	"Isaac",
	"Stella",
	"Grayson",
	"Zoe",
	"Jack",
	"Nora",
	"Julian",
	"Leah",
	"Christopher",
	"Hazel",
	"Joshua",
	"Violet",
	"Andrew",
	"Lillian",
	"Sam",
	"Zoey",
	"Ryan",
	"Natalie",
	"Hunter",
	"Penelope",
	"Nathan",
	"Riley",
	"Christian",
	"Lucy",
	"Isaiah",
	"Alyssa",
	"Caleb",
	"Ellie",
	"Josiah",
	"Paisley",
	"Aaron",
	"Nora",
	"Eli",
	"Brooklyn",
	"Landon",
	"Liliana",
	"Jonathan",
	"Savannah",
	"Nolan",
	"Maya",
	"Jeremiah",
	"Hailey",
	"Easton",
	"Aaliyah"
]

_PERSON_SURNAMES = [
	"Smith",
	"Johnson",
	"Williams",
	"Brown",
	"Jones",
	"Miller",
	"Davis",
	"Garcia",
	"Rodriguez",
	"Martinez",
	"Hernandez",
	"Lopez",
	"Gonzalez",
	"Wilson",
	"Anderson",
	"Thomas",
	"Taylor",
	"Moore",
	"Jackson",
	"Martin",
	"Lee",
	"Perez",
	"Thompson",
	"White",
	"Harris",
	"Clark",
	"Lewis",
	"Robinson",
	"Walker",
	"Young",
	"Allen",
	"King",
	"Wright",
	"Scott",
	"Nguyen",
	"Hill",
	"Turner",
	"Mitchell",
	"Jenkins",
	"Cook",
	"Morgan",
	"Hughes",
	"Reed",
	"Bennett",
	"Ross",
	"Brooks",
	"Coleman",
	"Mason",
	"Butler",
	"Parker",
	"Miller",
	"Cox",
	"Gray",
	"Wood",
	"Hayes",
	"Russell",
	"Rogers",
	"Gomez",
	"Long",
	"Stewart",
	"Morales",
	"James",
	"Reyes",
	"Foster",
	"Sullivan",
	"Mendoza",
	"Bishop",
	"Murray",
	"Ford",
	"Gardner",
	"Boyd",
	"Harvey",
	"Olson",
	"Howell",
	"Dean",
	"Hansen",
	"Weaver",
	"Dunn",
	"Haynes",
	"Caldwell",
	"Lowe",
	"Barker",
	"Mata",
	"Warner",
	"Berry",
	"Luna",
	"Willis",
	"Higgins",
	"Potter"
]


def utc_now_zulu_str() -> str:
	"""E.g. 2023-09-20T10:30:00Z """

	return datetime.strftime(datetime.utcnow(), _ZULU_TIME_FORMAT)


def delta_ago_zulu_str(days: float = 0, seconds: float = 0, minutes: float =0, hours: float = 0) -> str:
	"""E.g. 2023-09-20T10:30:00Z """

	return datetime.strftime(datetime.utcnow() - timedelta(days, seconds, minutes=minutes, hours=hours), _ZULU_TIME_FORMAT)


def mac_address() -> str:
	"""E.g. 10:66:61:0E:3F:C1 """

	# The first byte of a MAC address should start with a 0 in the least significant bit
	# 0x00 to 0x7F in hexadecimal
	first_byte = random.randint(0, 127)
	mac_list = [first_byte]

	for _ in range(5):
		random_byte = random.randint(0, 255)
		mac_list.append(random_byte)

	return ':'.join(f'{byte:02X}' for byte in mac_list)


def phone_number() -> str:

	first_digit = random.choice([6, 7, 9])
	rest_digits = ''.join(str(random.randint(0, 9)) for _ in range(8))

	return f'+34{first_digit}{rest_digits}'


def person_name() -> str:
	"""E.g. Isaiah """

	return random.choice(_PERSON_NAMES)


def person_full_name() -> str:
	"""E.g. Isaiah Morgan """

	random_name = random.choice(_PERSON_NAMES)
	random_surname = random.choice(_PERSON_SURNAMES)

	return f'{random_name} {random_surname}'
