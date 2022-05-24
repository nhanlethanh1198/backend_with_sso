staffDescription = """
API List for Staff
"""

staffLogin = """
Access: Staff Only

Action: Staff Login to system and return token

Request Body(JSON):
- phone: string
- password: string

"""

addStaff = """
Access: Staff Only (Admin)

Action: Add new staff

Request Body(FormData):
- fullname (str): Fullname of staff
- email (str): Email of staff
- phone (str): Phone of staff
- dob (str): Date of birth of staff
- address (str): Address of staff
- role (str): Role of staff (admin, staff, customer)
- password (str): Password of staff
- avatar_img (binary): Avatar of staff
- id_card_img_1 (binary): Front of ID card of staff
- id_card_img_2 (binary): Back of ID card of staff

"""


