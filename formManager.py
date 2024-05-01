from form import Form, FormTemplate, Frequency
from formQuestion import FormQuestion
from apparatus import Apparatus
import portalocker
from datetime import datetime
from datetime import timedelta
import csv

class FormManager:
    CONST_FORM_TEMPLATES_FILE = 'form_templates.csv'
    CONST_FORMS_FILE = 'forms.csv'

    def __init__(self, form_templates_file = None, forms_file = None):
        '''Grabs forms from the database and stores them in a list'''
        if(form_templates_file != None):
            self.CONST_FORM_TEMPLATES_FILE = form_templates_file
        if(forms_file != None):
            self.CONST_FORMS_FILE = forms_file
        self.formTemplates = self.load_form_templates_from_file_system()
        self.forms = self.load_forms_from_file_system()

    def get_forms(self) -> list[Form]:
        '''Returns the forms list'''
        return self.forms
    
    def get_form_by_id(self, form_id) -> Form:
        '''Returns the form with the given form_id'''
        for form in self.forms:
            if form.form_id == form_id:
                return form
        raise Exception(f"Form {form_id} not found")
    
    def set_forms(self, forms: list[Form]):
        '''Sets the forms list'''
        self.forms = forms
        self.save_form_to_file_system()
    
    def get_form_templates(self) -> list[FormTemplate]:
        '''Returns the form templates list'''
        return self.formTemplates
    
    def get_form_template_by_id(self, template_id) -> FormTemplate:
        '''Returns the form template with the given template_id'''
        for form_template in self.formTemplates:
            if form_template.template_id == template_id:
                return form_template
        raise Exception(f"Form template {template_id} not found")
    
    def set_form_templates(self, form_templates: list[FormTemplate]):
        '''Sets the form templates list'''
        self.formTemplates = form_templates
        self.save_form_templates_to_file_system()

    def _parse_csv_row_to_form_template(self, row):
        # Create a FormTemplate object from the row data and add it to the formTemplates list
        form_template_name = row[0]
        form_apparatus = row[1]
        form_template_frequency = row[2]
        form_template_questions = row[3]
        form_template_id = row[4]

        parsed_questions = []
        # parse the questions
        for question in form_template_questions.split("Form_Question%%"): # question delimiter is Form_Question%%
            if(question == "[" or question == "]" or question == "[]"):
                continue # skip the first and last element

            label = question.split(",")[0]
            type = question.split(",")[1]
            defaultValue = question.split(",")[2]
            value = question.split(",")[3]
            parsed_questions.append(FormQuestion(label, type, defaultValue, value))
        return FormTemplate(form_template_name, Apparatus(form_apparatus), Frequency(int(form_template_frequency)), parsed_questions, form_template_id)

    def load_form_templates_from_file_system(self):
        '''Loads form templates from the file system'''
        loaded_form_templates = []
        with open(self.CONST_FORM_TEMPLATES_FILE, 'r') as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    form_template = self._parse_csv_row_to_form_template(row)
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
        with open(self.CONST_FORMS_FILE, 'r') as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    # Create a Form object from the row data and add it to the forms list
                    parsed_formTemplate = self._parse_csv_row_to_form_template(row)
                    form_assigned = datetime.fromisoformat(row[5])
                    form_completed = row[6] == "True"
                    form_id = row[7]
                    form = Form(parsed_formTemplate, form_assigned, form_completed, form_id)
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
        with open(self.CONST_FORM_TEMPLATES_FILE, 'w') as file:
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

    def save_form_to_file_system(self):
        '''Saves forms to the file system'''
        with open(self.CONST_FORMS_FILE, 'w') as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                #erase the file
                file.seek(0)
                file.truncate()
                csv_writer = csv.writer(file)
                for form in self.forms:
                    # Write the form data to the file
                    compiled_questions = "["
                    for question in form.questions:
                        compiled_questions += str(question) + ","
                    compiled_questions += "]"
                    csv_writer.writerow([form.name, form.apparatus, form.frequency.value, compiled_questions, form.template_id, datetime.isoformat(form.dateAssigned), form.completed, form.form_id])
            except Exception as e:
                print(e)
            finally:
                portalocker.unlock(file)     
    
    def add_form_template(self, form_template: FormTemplate):
        '''Adds a form template to the form templates list'''
        self.formTemplates.append(form_template)
        self.save_form_templates_to_file_system()

    def write_form_template(self, form_template: FormTemplate):
        '''Writes a form template to the form templates list, and saves to file system.  Will overwrite existing form template with same template_id'''
        # Check if the form template already exists in the form templates list
        found = False
        for f in self.formTemplates:
            if f.template_id == form_template.template_id:
                # Overwrite the existing form template
                f = form_template
                found = True
        # Add the form template to the form templates list
        if not found:
            self.formTemplates.append(form_template)
        self.save_form_templates_to_file_system()

    def write_form(self, form: Form):
        '''Writes a form to the forms list, and saves to file system.  Will overwrite existing form with same form_id'''
        # Check if the form already exists in the forms list
        found = False
        for f in self.forms:
            if f.form_id == form.form_id:
                # Overwrite the existing form
                f = form
                found = True
        # Add the form to the forms list
        if not found:
            self.forms.append(form)
        self.save_form_to_file_system()

    def delete_form_template(self, template_id):
        '''Deletes a form template from the form templates list with the given template_id'''
        for form_template in self.formTemplates:
            if form_template.template_id == template_id:
                self.formTemplates.remove(form_template)
                self.save_form_templates_to_file_system()
                return
        raise Exception(f"Form template {template_id} not found, cannot delete")

    def delete_form(self, form_id):
        '''Deletes a form from the forms list with the given form_id'''
        for form in self.forms:
            if form.form_id == form_id:
                self.forms.remove(form)
                self.save_form_to_file_system()
                return
        raise Exception(f"Form {form_id} not found, cannot delete")
    
    def generate_forms(self):
        '''Looks through forms and identifies which forms need to be generated based on the frequency of the form template.  Generates the forms and saves them to the file system.'''
        #first, sort every form into a dictionary by frequency
        forms_by_frequency = {freq.value: [] for freq in Frequency}
        for form_template in self.formTemplates:
            forms_by_frequency[form_template.frequency.value].append(form_template)
        
        #next, cycle through all forms in each frequency, and check to see if a form already has been assigned within it's frequency
        for frequency in forms_by_frequency:
            for form_template in forms_by_frequency[frequency]:
                needs_form = True
                for form in self.forms:
                    #if this form matches a template in 
                    if form_template.template_id == form.template_id:
                        match frequency:
                            case Frequency.DAILY.value:
                                # if the date this form was assigned was after midnight last night, set needs_form to False
                                if form.dateAssigned >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                                    needs_form = False
                            case Frequency.WEEKLY.value:
                                # find the date of the most recent Sunday
                                last_sunday = datetime.now() - timedelta(days=datetime.now().weekday())
                                # if this form was assigned after midnight last Sunday, set needs_form to False
                                if form.dateAssigned >= last_sunday.replace(hour=0, minute=0, second=0, microsecond=0):
                                    needs_form = False
                            case Frequency.MONTHLY.value:
                                # find the date of the first of the month
                                first_of_month = datetime.now().replace(day=1)
                                # if this form was assigned after midnight on the first of the month, set needs_form to False
                                if form.dateAssigned >= first_of_month.replace(hour=0, minute=0, second=0, microsecond=0):
                                    needs_form = False
                            case Frequency.YEARLY.value:
                                # find the date of the first of the year
                                first_of_year = datetime.now().replace(month=1, day=1)
                                # if this form was assigned after midnight on the first of the year, set needs_form to False
                                if form.dateAssigned >= first_of_year.replace(hour=0, minute=0, second=0, microsecond=0):
                                    needs_form = False
                #if needs_form is True, generate a new form
                if needs_form:
                    self.write_form(Form.from_template(form_template))
