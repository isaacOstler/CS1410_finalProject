from user import User
from name import Name

def test_user_init():
    name = Name("John", "Doe")
    user = User(name, "Captain", "johndoe", "12345", isAdmin=True)
    assert user.name == name
    assert user.rank == "Captain"
    assert user.username == "johndoe"
    assert user.id == "12345"
    assert user.isAdmin == True

def test_user_str():
    name = Name("John", "Doe")
    user = User(name, "Captain", "johndoe", "12345", isAdmin=True)
    assert str(user) == f"User #12345: John Doe, (Captain)"

def test_user_csv_functionality():
    name = Name("John", "Doe")
    user = User(name, "Captain", "johndoe", "12345", isAdmin=True)
    User.save_user(user)
    user2 = User.get_user_by_id("12345")
    assert str(user2.name) == str(name)
    assert user2.rank == "Captain"
    assert user2.username == "johndoe"
    assert user2.id == "12345"
    assert user2.isAdmin == True
    User.delete_user("12345") # clean up
    # test that the user was deleted
    user3 = User.get_user_by_id("12345")
    assert user3 == None