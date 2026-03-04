import yaml
def load_users():
    with open("config.yaml","r")as file:
        data=file.read()
    config=yaml.safe_load(data)
    return config["users"]


    
