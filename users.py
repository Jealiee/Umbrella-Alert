import yaml

CONFIG_FILE = "config.yaml"


def load_users():
    with open(CONFIG_FILE, "r") as file:
        config = yaml.safe_load(file)
    return config.get("users", [])

def save_users(users):
    with open(CONFIG_FILE, 'w') as file:
        yaml.safe_dump({"users":users}, file, sort_keys =False)

def add_user(user_id, city, latitude, longitude, chat_id):
    users = load_users()

    if any(u['chat_id'] == chat_id for u in users):
        print('User already exists')
        return  
    new_user ={'chat_id': chat_id, 'city': city, 'latitude': latitude, 'longitude':longitude}

    users.append(new_user)
    save_users(users)
    print ('User added successfully.')
