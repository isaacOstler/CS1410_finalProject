from formQuestion import FormQuestion
from apparatus import Apparatus
from form import FormTemplate, Form, Frequency

def test_form_template():
    formTemplate = FormTemplate(
        "MA261 Weekly",
        Apparatus("MA261"),
        Frequency.WEEKLY,
        [
            FormQuestion("Ventilator", "boolean", 1),
        ]
    )
    assert formTemplate.name == "MA261 Weekly"
    assert formTemplate.apparatus.name == "MA261"
    assert formTemplate.frequency == Frequency.WEEKLY
    assert formTemplate.questions[0].label == "Ventilator"
    assert formTemplate.questions[0].type == "boolean"
    assert formTemplate.questions[0].defaultValue == 1

def test_form():
    formTemplate = FormTemplate(
        "MA261 Weekly",
        Apparatus("MA261"),
        Frequency.WEEKLY,
        [
            FormQuestion("Ventilator", "boolean", 1),
        ]
    )
    form = Form.from_template(formTemplate)
    assert form.name == "MA261 Weekly"
    assert form.apparatus.name == "MA261"
    assert form.frequency == Frequency.WEEKLY
    assert form.questions[0].label == "Ventilator"
    assert form.questions[0].type == "boolean"
    #assert form.questions[0].defaultValue == 1
    #support dropped for default value on commit 36cb92a
    assert form.questions[0].value == ""
    assert form.completed == False
    # data assigned should be within 1 second of now
    assert form.dateAssigned.timestamp() - form.dateAssigned.timestamp() < 1
    assert form.form_id is not None