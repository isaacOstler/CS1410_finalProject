class FormQuestion:
    def __init__(self, label, type, defaultValue, value = None):
        self.label = label
        self.type = type
        self.defaultValue = defaultValue
        self.value = value
        if(value == None):
            self.value = ""

    def __str__(self) -> str:
        return f"Form_Question%%{self.label},{self.type},{self.defaultValue},{self.value}"

    def __repr__(self) -> str:
        return f"Form_Question%%{self.label},{self.type},{self.defaultValue},{self.value}"