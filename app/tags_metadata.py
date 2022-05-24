from docs import user, services, categories, products, product_vote, promotions, task

tags_metadata = [
    {
        'name': 'users',
        'description': user.userDescription,
    },
    {
        "name": "services",
        "description": services.serviceDescription,
    },
    {
        "name": "categories",
        "description": categories.categoriesDescription,
    },
    {
        "name": "products",
        "description": products.productDescription
    },

    {
        "name": "Product Vote",
        "description": product_vote.productVoteDescription,
    },
    {
        "name": "promotions",
        "description": promotions.promotionDescriptions,
    },
    {
        "name": "tasks",
        "description": task.taskDescription,
    },
    {
        "name": "staffs",
        "description": "API List for Staff",
    },
    {
        "name": "Staff Vote",
        "description": "API List for Staff by User",
    },
    {
        "name": "orders",
        "description": "API List for Orders By Staff",
    },
    {
        "name": "Combo",
        "description": "API List for Combo",
    },
    {
        "name": "Combo Vote",
        "description": "API List for Combo by User",
    },
    {
        "name": "banners",
        "description": "API List for Banner",
    },
    {
        "name": "stores",
        "description": "API List for Store by Staff",
    },
    {
        "name": "versions",
        "description": "API List for Version",
    },
    {
        "name": "searching",
        "description": "API List for Searching",
    },
]
