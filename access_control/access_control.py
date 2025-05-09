users = {
    'alice': 'admin',
    'bob': 'user',
    'guest': 'guest'
}

permissions = {
    'admin': ['read', 'write', 'delete'],
    'user': ['read', 'write'],
    'guest': ['read']
}

FILE_NAME = 'data.txt'

def has_permission(username, action):
    role = users.get(username)
    return action in permissions.get(role, [])

def read_file(user):
    if has_permission(user, 'read'):
        with open(FILE_NAME, 'r') as f:
            print("\nFile Content:")
            print(f.read())
    else:
        print("User does not have permission to read the file.")

def write_file(user, text):
    if has_permission(user, 'write'):
        with open(FILE_NAME, 'a') as f:
            f.write(text + '\n')
        print("Text written to file.")
    else:
        print("User does not have permission to write to the file.")

def delete_file(user):
    if has_permission(user, 'delete'):
        open(FILE_NAME, 'w').close()
        print("File cleared.")
    else:
        print("User does not have permission to delete the file.")

def main():
    user = 'guest'
    write_file(user, "cits2006")
    

if __name__ == "__main__":
    open(FILE_NAME, 'a').close()
    main()