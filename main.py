from user import User
from name import Name

def main():
    while True:
        # try to login
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        try:
            user = User.sign_in(username, password)
            print(f"Welcome {user.name.first}!")
            break
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()