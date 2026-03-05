import yaml
def load_users():
    with open("config.yaml","r")as file:
        data=file.read()
    config=yaml.safe_load(data)
    return config["users"]


def safe_user(chat_id, city, latitude, longitude):
    users= load_users()

    users.append({"chat_id":chat_id, "city":city, "latitude":latitude, "longitude":longitude})

    with open("config.yaml", "w") as file:
        yaml.safe_dump({"users": users}, file)


    

