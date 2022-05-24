productDescription = """
API for products.

It is used to get information about products.


* **Get List Product in category**: Get list of products in category by category_id. (**GET**)
* **Get Product By Code**: Get product by code. (**GET**)
* **Get List Product**: Get list of products. (**GET**)
* **user get product**: Get products by params (category_id, status). (**GET**)
* **Add Product**: Add new product. (**POST**)
* **Update Product**: Update product by product_code. (**PUT**)
* **Update Status Product**: Update status product. (**PUT**)
* **User get Product Sale**: Get list of products sale by params (category_id, status). (**GET**)

"""

getListProductInCategoryDescription = """
Access: All

Action: Get list of products in category by category_id.

Params: category_id (int)
"""

getProductByCode = """
Access: All

Action: Get product by code.

Params: code (str)
"""

getLístProduct = """
Access: Staff Only

Action: Get List Product

Params: category_id (int), status (int), limit (int), page (int)

Note: If category_id is not null, it will get list of products in category.
"""

userGettLístProduct = """
Access: User Only

Action: Get List Product

Params: category_id (int), status (int), limit (int), page (int)

Note: If category_id is not null, it will get list of products in category.
"""

addProduct = """
Access: Staff Only

Action: Add new product.

Request body(FormData):
> required:
- name (str): Name of product.
- category_id (int): Category id.
- price (int): Price of product.
- unit (str): Unit of product.
- weight (int): Weight of product.
- stock (int): Stock of product.
- avatar_img (binary): Image of product.
- belong_to_store (int): Store id.

> optional
- price_sale (int): Price sale of product.
- day_to_shipping (str): Day to shipping of product.
- preserve (str): Preserve of product.
- guide (str): Guide of product.
- make_by (str): Make by of product.
- made_in (str): Made in of product.
- brand (str): Brand of product.
- note (str): Note of product.
- tags (str): Tags of product.
- description (str): Description of product.
"""

updateProduct = """
Access: Staff Only

Action: Add new product.

Request body(FormData):
> required:
- name (str): Name of product.
- category_id (int): Category id.
- price (int): Price of product.
- unit (str): Unit of product.
- weight (int): Weight of product.
- stock (int): Stock of product.
- avatar_img (binary): Image of product.
- belong_to_store (int): Store id.

> optional
- price_sale (int): Price sale of product.
- day_to_shipping (str): Day to shipping of product.
- preserve (str): Preserve of product.
- guide (str): Guide of product.
- make_by (str): Make by of product.
- made_in (str): Made in of product.
- brand (str): Brand of product.
- note (str): Note of product.
- tags (str): Tags of product.
- description (str): Description of product.
"""

updateStatusProduct = """
Access: Staff Only

Action: Update status for product.

Params: product_code (str)

Request body(JSON):
- status (int): Status of product.
>* 0: Lỗi
>* 1: Còn hàng
>* 2: Hết hàng
>* 3: Đang nhập hàng
>* 4: Đã khóa
"""

userGetProductSale = """
Access: All

Action: Get list of products sale

Params: limit (int): page (int)
"""

getProductSale = """
Access: Staff ony

Action: Get list of products sale

Params: limit (int): page (int)
"""

syncProductSale = """
Access: Staff only

Action: Sync product sale
"""

updatePositionProductSale = """
Access: Staff Only

Action: Update Position product for sale

Request Body(JSON):
- list_product (list): List product sale.
>* code (str): Code of product.
>* score (int): Score of product.
"""

getProductTrend = """
Access: All

Action: Get list of products in trending.

Params: filter (str), limit (int), page (int)
- filter: one of them: 'newest', 'vote', 'trend', default is 'newest'
- limit: number of product in one page, default is 20
- page: number of page, default is 1
"""


getProductRelation = """
Access: All

Action: Get list of products in relation in same category.

Params: product_code (str), category_id (int)

"""

getProductSuggest = """
Access: All

Action: Get suggestion products.
"""



