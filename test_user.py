from user import User
from name import Name

def test_user_init():
    name = Name("John", "Doe")
    user = User(name, "Captain", "johndoe", 12345, isAdmin=True)
    assert user.name == name
    assert user.rank == "Captain"
    assert user.username == "johndoe"
    assert user.id == 12345
    assert user.isAdmin == True

def test_user_str():
    name = Name("John", "Doe")
    user = User(name, "Captain", "johndoe", 12345, isAdmin=True)
    assert str(user) == f"User #12345: John Doe, (Captain)"