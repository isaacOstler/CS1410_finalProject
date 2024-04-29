from name import Name

''' A class that keeps track of a user.  Also has static methods for getting and saving users from a database'''
class User:
    def __init__(self, name: Name, rank, username, id, isAdmin: bool = False):
        if(not isinstance(name, Name)):
            raise TypeError("name must be a Name object")
        self.name = name
        self.rank = rank
        self.username = username
        self.isAdmin = isAdmin
        self.id = id

    def __str__(self):
        return f"User #{self.id}: {str(self.name)}, ({self.rank})"

    @staticmethod
    def get_user_by_id(id):
        ''' Gets a user by their id from the database'''
        pass

    @staticmethod
    def save_user(user):
        ''' Saves a user to the database'''
        pass