import json

with open("all_verified.json") as f:
    data = json.load(f)

users = []

for level in data:
    user_id = level["identifier"].split(":")[0]
    if user_id not in users:
        users.append(user_id)
        
with open("all_users.json", "w") as f:
    json.dump(users, f)