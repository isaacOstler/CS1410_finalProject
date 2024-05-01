from formManager import FormManager
from form import FormTemplate, Frequency
from formQuestion import FormQuestion
from apparatus import Apparatus

def test_form_manager():
    formManager = FormManager("./test/test_form_templates.csv", "./test/test_forms.csv")
    # first, erase all forms
    formManager.forms = []
    formManager.formTemplates = []
    # create a new form
    formManager.add_form_template(FormTemplate(
        "MA261 Daily",
        Apparatus("MA261"),
        Frequency.DAILY,
        [
            FormQuestion("Ventilator", "boolean", 1),
        ]
    ))
    formManager.add_form_template(FormTemplate(
        "MA261 Weekly",
        Apparatus("MA261"),
        Frequency.WEEKLY,
        [
            FormQuestion("Ventilator", "boolean", 1),
        ]
    ))
    formManager.add_form_template(FormTemplate(
        "MA261 Monthly",
        Apparatus("MA261"),
        Frequency.MONTHLY,
        [
            FormQuestion("Ventilator", "boolean", 1),
        ]
    ))
    formManager.add_form_template(FormTemplate(
        "MA261 Yearly",
        Apparatus("MA261"),
        Frequency.YEARLY,
        [
            FormQuestion("Ventilator", "boolean", 1),
        ]
    ))
    # check that the forms were added
    assert formManager.formTemplates[0].name == "MA261 Daily"
    assert formManager.formTemplates[1].name == "MA261 Weekly"
    assert formManager.formTemplates[2].name == "MA261 Monthly"
    assert formManager.formTemplates[3].name == "MA261 Yearly"
    # test generating a form from a template
    formManager.generate_forms()
    # check that the form was generated
    assert len(formManager.get_forms()) == 4
    assert formManager.get_forms()[0].name == "MA261 Daily"
    assert formManager.get_forms()[1].name == "MA261 Weekly"
    assert formManager.get_forms()[2].name == "MA261 Monthly"
    assert formManager.get_forms()[3].name == "MA261 Yearly"
