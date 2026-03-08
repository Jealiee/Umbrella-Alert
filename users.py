import yaml

CONFIG_FILE = "config.yaml"


def load_users():
    with open(CONFIG_FILE, "r") as file:
        config = yaml.safe_load(file)
    return config.get("users", [])

def save_users(users):
    with open(CONFIG_FILE, 'w') as file:
        yaml.safe_dump({"users":users}, file, sort_keys =False)

def add_user(city, latitude, longitude, chat_id, timezone):
    users = load_users()

    if any(u['chat_id'] == chat_id for u in users):
        print('User already exists')
        return  
    new_user ={'chat_id': chat_id, 
               'city': city, 
               'latitude': latitude, 
               'longitude':longitude, 
               'timezone': timezone}

    users.append(new_user)
    save_users(users)
    print ('User added successfully.')

def update_user(chat_id, city, latitude, longitude, timezone):

    with open(CONFIG_FILE, "r") as file:
        data = yaml.safe_load(file)

    users = data["users"]   

    for user in users:
        if user["chat_id"] == chat_id:
            user.update({
                "city": city, 
                "latitude": latitude, 
                "longitude": longitude,
                'timezone': timezone})
            save_users(users)
            print("User updated successfully.")
            return
        
    print("User not found.")