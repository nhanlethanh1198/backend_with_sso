promotionDescriptions = """
List of API for Promotions
"""

getListPromotion = """
Access: All

Action: Get list of promotions
"""

getPromotionById = """
Access: All

Action: Get info of promotion by id

Params: promotion_id (int)
"""

createPromotion = """
Access: Staff Only

Action: Create New Promotion

Request Body(FormData):
- code (str): The Code for Promotion
- title (str): The Title for Promotion
- time_from: (str): The Time start for Promotion
- time_to: (str): The Time end for Promotion
- image (str): The Image for Promotion 
- promotion_type (str): The Type of Promotion
- detail (str): The Detail for Promotion (optional)
- rule (str): The Rule for Promotion (optional)
"""

updatePromotionById = """
Access: Staff Only

Action: Update Promotion by id

Params: promotion_id (int)

Request Body(FormData):
- code (str): The Code for Promotion (optional)
- title (str): The Title for Promotion (optional)
- time_from: (str): The Time start for Promotion (optional)
- time_to: (str): The Time end for Promotion (optional)
- image (str): The Image for Promotion (optional)
- promotion_type (str): The Type of Promotion (optional)
- detail (str): The Detail for Promotion (optional)
- rule (str): The Rule for Promotion (optional)
"""

userGetPromotion = """
Access: User Only

Action: User get all promotion is activating.

Params: promotion_type (str): The Type of Promotion (optional) (one of: combo, product, system, user; default: system)
"""

userGetPromotionById = """
Access: User Only

Action: User get info of Promotion By promotion_id

Params: promotion_id (int)

"""