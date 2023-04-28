'''
pip instasll pandas --simple https://simple.douban.com
'''
import pandas as pd

# print("version:",pd.__version__)
# print(pd)
#
# mydataset = {
#     "username": ["docker", "java", "vue"],
#     'sites': ["Google", "Runoob", "Wiki"],
#     'number': [1, 2, 3]
# }
#
#
# myvar = pd.DataFrame(mydataset)
#
# print(myvar)


# sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
#
# myvar = pd.Series(sites)
#
# print(myvar)


data =[
    {
      "id": "A001",
      "name": "菜鸟教程",
      "url": "www.runoob.com",
      "likes": 61
    },
    {
      "id": "A002",
      "name": "Google",
      "url": "www.google.com",
      "likes": 124
    },
    {
      "id": "A003",
      "name": "淘宝",
      "url": "www.taobao.com",
      "likes": 45
    }
]
df = pd.DataFrame(data)

print(df)

URL = 'https://static.runoob.com/download/sites.json'
df = pd.read_json(URL)
print(df)
