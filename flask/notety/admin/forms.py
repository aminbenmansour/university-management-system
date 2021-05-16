from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, HiddenField, RadioField, SelectField, IntegerField, BooleanField
from wtforms_components import SelectField as selectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


    

class ClassAdditionForm(FlaskForm):
    class_name = StringField('Class selection',
                           validators=[DataRequired()])

    submit = SubmitField('Next')

class ModuleAdditionForm(FlaskForm):

    sem_choice = RadioField('Semester selection',
                           choices=[('sem1','Semester 1'),
                                ('sem2','Semester 2')], validators=[DataRequired()])


    module_name = StringField('Module name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Add module')




class SubjectAdditionForm(FlaskForm):
    module_select = SelectField("Choose an option", validate_choice=False)

    subject_name = StringField('Subject name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    coef = IntegerField('Subject coefficient', validators=[DataRequired()])


    submit = SubmitField('Add Subject')


##  Remit students grades

class ClassSelectionForm(FlaskForm):
    class_select  = SelectField("Choose a class", validators=[DataRequired(), Length(min=2, max=20)])
    sem_select  = SelectField("Choose a semester", validators=[DataRequired(), Length(min=2, max=20)], choices = [(None, 'Choose semester'),('sem1', 'Semester 1'), ('sem2', 'Semester 2')])
    submit = SubmitField('Next')



class StudentSelectionForm(FlaskForm):
    student_select = SelectField("Choose student", validators=[DataRequired()])

    submit = SubmitField('Confirm')



class RemitSubjectGradeForm(FlaskForm):
    pp = HiddenField()

    tp = StringField('TP grade')
    
    ds = StringField('DS grade',
                           validators=[DataRequired(), Length(min=2, max=20)])

    exam = StringField('Exam name',
                           validators=[DataRequired(), Length(min=2, max=20)])                       

    submit = SubmitField('Confirm')


class ClassesForm(FlaskForm):
    class_select  = SelectField("Choose a class", validators=[DataRequired()])
    submit = SubmitField('Confirm')
