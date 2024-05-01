from formQuestion import FormQuestion

def test_form_question():
    question = FormQuestion("Ventilator", "boolean", 1)
    assert question.label == "Ventilator"
    assert question.type == "boolean"
    #assert question.defaultValue == 1 
    #support dropped for default value on commit 36cb92a
    assert question.value == ""
    assert question.__repr__() == "Form_Question%%Ventilator,boolean,1,"