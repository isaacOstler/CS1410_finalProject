from form import Form, FormTemplate, Frequency
from formQuestion import FormQuestion
from apparatus import Apparatus
import portalocker
import csv

class FormManager:
    def __init__(self):
        '''Grabs forms from the database and stores them in a list'''
        self.formTemplates = self.load_form_templates_from_file_system()
        self.forms = self.load_forms_from_file_system()

    def load_form_templates_from_file_system(self):
        '''Loads form templates from the file system'''
        loaded_form_templates = []
        with open('form_templates.csv', 'r') as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    # Create a FormTemplate object from the row data and add it to the formTemplates list
                    form_template_name = row[0]
                    form_apparatus = row[1]
                    form_template_frequency = row[2]
                    form_template_questions = row[3]
                    form_template_id = row[4]

                    parsed_questions = []
                    # parse the questions
                    for question in form_template_questions.split("Form_Question%%"): # question delimiter is Form_Question%%
                        if(question == "[" or question == "]"):
                            continue # skip the first and last element

                        label = question.split(",")[0]
                        type = question.split(",")[1]
                        defaultValue = question.split(",")[2]
                        value = question.split(",")[3]
                        parsed_questions.append(FormQuestion(label, type, defaultValue, value))

                    form_template = FormTemplate(form_template_name, Apparatus(form_apparatus), Frequency(int(form_template_frequency)), parsed_questions, form_template_id)
                    if form_template not in loaded_form_templates:
                        loaded_form_templates.append(form_template)
            except Exception as e:
                print(e)
            finally:
                portalocker.unlock(file)
                self.formTemplates = loaded_form_templates
                return loaded_form_templates

    def load_forms_from_file_system(self):
        '''Loads forms from the file system'''
        loaded_forms = []
        with open('forms.csv', 'r') as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    # Create a Form object from the row data and add it to the forms list
                    form_name = row[0]
                    form_frequency = row[1]
                    form_questions = row[2]
                    form_template_id = row[3]
                    form_completed = row[4]
                    form_assigned = row[5]
                    form_id = row[6]
                    form = Form(form_name, Frequency(form_frequency), form_questions, form_template_id, form_assigned, form_completed, form_id)
                    if form not in loaded_forms:
                        loaded_forms.append(form)
            except Exception as e:
                print(e)
            finally:
                portalocker.unlock(file)
                self.forms = loaded_forms
                return loaded_forms

    def save_form_templates_to_file_system(self):
        '''Saves form templates to the file system'''
        with open('form_templates.csv', 'w') as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                #erase the file
                file.seek(0)
                file.truncate()
                csv_writer = csv.writer(file)
                for form_template in self.formTemplates:
                    # Write the form template data to the file
                    csv_writer.writerow([form_template.name, form_template.apparatus, form_template.frequency.value, form_template.questions, form_template.template_id])
            except Exception as e:
                print(e)
            finally:
                portalocker.unlock(file)        
    
    def add_form_template(self, form_template: FormTemplate):
        '''Adds a form template to the form templates list'''
        self.formTemplates.append(form_template)
        self.save_form_templates_to_file_system()