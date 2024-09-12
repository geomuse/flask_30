from pymongo import MongoClient

# 连接到本地 MongoDB 实例
client = MongoClient('mongodb://localhost:27017/')

# 选择数据库（如果不存在则会自动创建）
db = client['recipe']

# 选择集合（类似于表）
collection = db['info']

# print(collection)

# 插入单个文档
recipe = {
    "name": "Sweet and Sour Chicken",
    "servings": 4,
    "prep_time": "20 minutes",
    "ingredients": [
        {"name": "chicken breast", "quantity": 500, "unit": "g"},
        {"name": "bell pepper", "quantity": 1, "unit": "pcs"}
    ],
    "instructions": [
        "Cut chicken breast into bite-sized pieces.",
        "Heat oil in a pan and fry the chicken until golden brown."
    ]
}

# 插入到集合中
# collection.insert_one(recipe)

# 查询所有文档
for recipe in collection.find():
    print(recipe)
    print('\n')

# r = [ recipe for recipe in collection.find() ]
# print(r)