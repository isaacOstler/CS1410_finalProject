from user import User
from name import Name

def main():
    user = User.get_user_by_id(1)
    print(user)
    User.delete_user(user.id)

if __name__ == "__main__":
    main()