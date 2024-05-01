from user import User
from name import Name

def test_user_init():
    User.CONST_USER_FILE = './test/test_users.csv'
    name = Name("John", "Doe")
    user = User(name, "Captain", "johndoe", "password", is_admin=True, id="12345", hash_password=False)
    assert user.name == name
    assert user.rank == "Captain"
    assert user.username == "johndoe"
    assert user.id == "12345"
    assert user.is_admin == True

def test_user_init_no_id():
    User.CONST_USER_FILE = './test/test_users.csv'
    name = Name("John", "Doe")
    user = User(name, "Captain", "johndoe", "password", is_admin=False, hash_password=False)
    assert user.name == name
    assert user.rank == "Captain"
    assert user.username == "johndoe"
    assert user.id != None
    assert user.is_admin == False

def test_user_str():
    User.CONST_USER_FILE = './test/test_users.csv'
    name = Name("John", "Doe")
    user = User(name, "Captain", "johndoe", "password", is_admin=True, id="12345", hash_password=False)
    assert str(user) == f"User #12345: John Doe, (Captain)"

def test_user_csv_functionality():
    User.CONST_USER_FILE = './test/test_users.csv'
    name = Name("John", "Doe")
    user = User(name, "Captain", "johndoe", "password", is_admin=True, id="12345", hash_password=False)
    User.save_user(user)
    user2 = User.get_user_by_id("12345")
    assert str(user2.name) == str(name)
    assert user2.rank == "Captain"
    assert user2.username == "johndoe"
    assert user2.id == "12345"
    assert user2.is_admin == True
    User.delete_user("12345") # clean up
    # test that the user was deleted
    user3 = User.get_user_by_id("12345")
    assert user3 == None