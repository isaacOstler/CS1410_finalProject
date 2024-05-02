from formQuestion import FormQuestion
from apparatus import Apparatus
from enum import Enum
from uuid import uuid4
from datetime import datetime

class Frequency(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4

class FormTemplate:
    def __init__(self, name, apparatus: Apparatus, frequency: Frequency = Frequency.DAILY, questions: list[FormQuestion] = [], template_id = None):
        self.name = name
        self.apparatus = apparatus
        self.frequency = frequency
        self.questions = questions
        if(template_id == None):
            self.template_id = uuid4()
        else:
            self.template_id = template_id

    def addQuestion(self, question: FormQuestion):
        self.questions.append(question)

    def removeQuestion(self, question: FormQuestion):
        self.questions.remove(question)

    def __repr__(self) -> str:
        return f"{self.name},{self.apparatus},{self.frequency},{self.questions},{self.template_id}"

class Form(FormTemplate):
    def __init__(self, formTemplate: FormQuestion, dateAssigned: datetime = None, completed: bool = False, completed_by: str = "", form_id = None):
        super().__init__(formTemplate.name, formTemplate.apparatus, formTemplate.frequency, formTemplate.questions, formTemplate.template_id)
        self.completed = completed
        self.dateAssigned = dateAssigned
        self.completed_by = completed_by
        if(form_id == None):
            self.form_id = uuid4()
        else:
            self.form_id = form_id

        if(dateAssigned == None):
            self.dateAssigned = datetime.now()
        else:
            self.dateAssigned = dateAssigned
    
    @staticmethod
    def from_template(formTemplate: FormTemplate, **kwargs):
        return Form(formTemplate, **kwargs)