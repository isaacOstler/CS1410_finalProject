import apparatus

def test_apparatus():
    app = apparatus.Apparatus("MA261")
    assert app.name == "MA261"
    assert app.__repr__() == "MA261"