categoriesDescription = """
API for categories.
It is used to get information about categories.

### For Staff

* **Add category**: Add new category. (**POST**)
* **Update category**: Update category. (**PUT**)
* **Lock category**: Lock category. (**PUT**)
* **Get List Category**: Get list of categories. (**GET**)
* **Get Category By Id**: Get category by id. (**GET**)

### For User
* **List all of categories**: Get list of categories with relationship. (**GET**) 
* **User get category by id**: Get category by id. (**GET**)
* **User get children category by id**: Get children category by id. (**GET**)
"""


readCategoriesDescription = """
Access: All

- Get list of categories with relationship.
"""

addCategoryDescription = """
Access: Staff only

Action: Add new category.

### Request (FormData)
- name (str): Name of category.
- parent_id (int): Parent category id.
- img (binary): Image of category.


"""

updateCategoryDescription = """
Access: Staff only

Action: Update Category by category_id.

### Request (FormData)
- name (str): Name of category.
- parent_id (int): Parent category id.
- img (binary)(optional): Image of category.
"""

lockUnlockCategoryDescription = """
Access: Staff only

Action: Lock/Unlock category by category_id.

### Request (JSON):
- is_active (bool): True if category is active.
"""

getListCategoryDescription = """
Access: Staff only

Action: Get list of categories with no relationship.

"""

getCategoryByIdDescription = """
Access: Staff only

Action: Get category by category_id.
"""

userGetCategoryByIdDescription = """
Access: All

Action: Get category by category_id.
"""
getChidlenCategoryByIdDescription = """
Access: All

Action: Get children category by category_id.
"""
