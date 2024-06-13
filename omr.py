import requests
import json
import time
import urllib3

urllib3.disable_warnings()

VPS_IP = "INSERT_IP_HERE"
VPS_PORT = "65500"
OMR_KEY = "INSERT_KEY_HERE"

def get_token(ip, key, username):
    url = f"https://{ip}/token"
    payload = f'password={key}&username={username}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=payload, verify=False)
    response.raise_for_status()
    return response.json().get("access_token")

def add_user(ip, key, user, permission):
    print(f"Trying to add user: {user}")
    token = get_token(ip, key, "admin")
    url = f"https://{ip}/add_user"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({"username": user, "permission": permission, "vpn": "glorytun_udp"})
    response = requests.post(url, headers=headers, data=payload, verify=False)
    response.raise_for_status()
    print(response.text)

def delete_user(ip, key, user):
    print(f"Trying to remove user: {user}")
    token = get_token(ip, key, "admin")
    url = f"https://{ip}/remove_user"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({"username": user})
    response = requests.post(url, headers=headers, data=payload, verify=False)
    response.raise_for_status()
    print(response.text)

def get_user_info(ip, key, username):
    print(f"Getting user info for: {username}")
    token = get_token(ip, key, username)
    url = f"https://{ip}/config"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    user_info = response.json()
    print("User Information:")
    print(json.dumps(user_info, indent=4))

def list_users(ip, key):
    print("Getting all users...")
    token = get_token(ip, key, "admin")
    url = f"https://{ip}/list_users"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    users = response.json()
    print("List of Users:")
    print(json.dumps(users, indent=4))

def main():
    global VPS_IP, VPS_PORT, OMR_KEY
    
    if not VPS_IP:
        VPS_IP = input("Enter VPS IP: ").strip()
    if not VPS_PORT:
        VPS_PORT = input("Enter VPS Port: ").strip()
    if not OMR_KEY:
        OMR_KEY = input("Enter OMR Key: ").strip()

    while True:
        print("Menu:")
        print("1. Add User")
        print("2. Delete User")
        print("3. Get User Info")
        print("4. List Users")
        print("5. Exit")
        option = input("Choose an option: ").strip()

        if option == '1':
            username = input("Enter Username: ").strip()
            permission_input = input("Enter Permission (read/write/admin): ").strip()
            permission_map = {"read": "ro", "write": "rw", "admin": "admin"}
            permission = permission_map.get(permission_input.lower(), "ro")
            add_user(f"{VPS_IP}:{VPS_PORT}", OMR_KEY, username, permission)
        elif option == '2':
            username = input("Enter Username to delete: ").strip()
            delete_user(f"{VPS_IP}:{VPS_PORT}", OMR_KEY, username)
        elif option == '3':
            username = input("Enter Username to get info: ").strip()
            get_user_info(f"{VPS_IP}:{VPS_PORT}", OMR_KEY, username)
        elif option == '4':
            list_users(f"{VPS_IP}:{VPS_PORT}", OMR_KEY)
        elif option == '5':
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
