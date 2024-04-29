from user import User
from name import Name

def main():
    user = User(Name("John","Doe"), "Admin", "johndoe", 1)
    print(user)

if __name__ == "__main__":
    main()