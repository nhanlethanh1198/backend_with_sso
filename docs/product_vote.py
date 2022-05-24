productVoteDescription = """
List of Api for votting product by user.
"""

voteListInProduct = """
Access: All

Action: Get Vote list in Product by product_code.

Params: product_code (str)
"""

addNewVoteForProduct = """
Access: User Only

Action: Create new vote for product.

Params: product_code (str)

Request body(JSON):
- vote_score (int): Score of vote.
- comment (str): Comment of vote.
- tags (list): List of tags.
"""

checkUserIsBuyThisProduct = """
Access: User Only

Action: Check user is bought this product.

Params: product_code (str)
"""

getVoteProductByVoteId = """
Access: All

Action: Get Vote product by vote_id.

Params: vote_id (int)
"""

updateVoteForProduct = """
Access: User Only

Action: Update vote for product.

Params: vote_id (int), product_code (str)

Request body(JSON):
- vote_score (int): Score of vote.
- comment (str): Comment of vote.
- tags (list): List of tags.
"""

