from flask import jsonify, render_template, url_for, flash, redirect, request, session, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from notety import db, bcrypt
from notety import grades, students_collection, data_collection, admin_collection
from notety import data as ddata
from notety.models import Admin
from bson.objectid import ObjectId

from notety.admin.forms import (LoginForm, ClassAdditionForm, ModuleAdditionForm,
                                   SubjectAdditionForm, ClassSelectionForm, StudentSelectionForm, RemitSubjectGradeForm, ClassesForm)
import ast
from werkzeug.datastructures import ImmutableMultiDict

admin = Blueprint('admin', __name__)
data = ddata


@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = admin_collection.find_one(
            {'username': form.username.data})
        if admin and admin['password'] == form.password.data:
            admin = Admin()
            login_user(admin, remember=False)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Please check username and password', 'danger')
    return render_template('admin/basics/login.html', title='Admin Login', form=form)


@admin.route('/admin/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@admin.route('/admin/home', methods=['GET'])
@login_required
def home():
    return render_template('common/home.html', title='Welcome Home - Admin')


@admin.route('/admin/system-management/add_class/', methods=['GET', 'POST'])
@login_required
def add_class():
    form = ClassAdditionForm()
    if form.validate_on_submit():
        data["class_name"] = form.class_name.data
        flash(f'Your can now add modules to {data["class_name"]}', 'success')
        form = ModuleAdditionForm()
        return redirect(url_for('admin.add_module', data=data, form=form))
    return render_template('admin/system/classes-management.html', form=form, title='Manage Classes')


@admin.route('/admin/system-management/add_module/', methods=['GET', 'POST'])
@login_required
def add_module():
    form = ModuleAdditionForm()
    if form.validate_on_submit():

        module = {
            "module_name": form.module_name.data,
            "subjects": []
        }

        sel_sem = form.sem_choice.data
        data[sel_sem].append(module)

        flash(f'Module added', 'success')
        flash(f'Your can now add subjects to added modules', 'info')

        return redirect(url_for('admin.add_module', form=SubjectAdditionForm()))
    return render_template('admin/system/modules-management.html', title='Add modules to class', data=data, form=form)


@admin.route('/admin/system-management/add_subject/', methods=['GET', 'POST'])
@login_required
def add_subject():
    form1 = SubjectAdditionForm(prefix="form1")
    form2 = SubjectAdditionForm(prefix="form2")
    form1.module_select.choices = [(None, "Choose an option")]
    form2.module_select.choices = [(None, "Choose an option")]

    form1.module_select.choices += [(module["module_name"],
                                     module["module_name"]) for module in data['sem1']]
    form2.module_select.choices += [(module["module_name"],
                                     module["module_name"]) for module in data['sem2']]

    if form1.submit.data and form1.validate_on_submit():

        subject_data = {
            "subject": form1.subject_name.data,
            "coef": form1.coef.data,
        }

        modules = data['sem1']
        index = 0
        for module in modules:
            if module["module_name"] == form1.module_select.data:
                break
            index += 1

        modules[index]["subjects"].append(subject_data)
        index = 0

    if form2.submit.data and form2.validate_on_submit():

        subject_data = {
            "subject": form2.subject_name.data,
            "coef": form2.coef.data
        }

        modules = data['sem2']
        index = 0
        for module in modules:
            if module.get("module_name") == form2.module_select.data:
                break
            index += 1
        modules[index]["subjects"].append(subject_data)
        index = 0

    flash(f'Operation succeded', 'info')
    return render_template('admin/system/subjects-management.html', title= f'Add subjects to modules', data=data, form1=form1, form2=form2)


@admin.route('/admin/system-management/upload_data', methods=['GET', 'POST'])
@login_required
def upload_data(data=data):
    data_collection.insert_one(data)
    data = ddata
    return redirect(url_for('admin.home'))


@admin.route('/admin/system-management/grades/step1', methods=['GET', 'POST'])
@login_required
def remit_grades_step1():

    all_classes = data_collection.find()

    form0 = ClassSelectionForm(prefix="classes")

    form0.class_select.choices = [(None, "Choose a class")]
    form0.class_select.choices += [(one_class["class_name"],
                                    one_class["class_name"]) for one_class in all_classes]

    if form0.validate_on_submit():

        fetched_data = data_collection.find_one(
            {"class_name": form0.class_select.data})
        fetched_data = dict(fetched_data)

        fetched_students = students_collection.find(
            {"class_name": form0.class_select.data})

        fetched_students_list = []
        for fetched_student in fetched_students:
            fetched_student.pop('_id', None)
            fetched_student.pop('password', None)
            fetched_student.pop('image_file', None)

            fetched_students_list.append(dict(fetched_student))

        fetched_data.pop('_id', None)

        session['students_list'] = fetched_students_list
        session['data'] = fetched_data
        # session['modules_list'] = modules_list
        # session['forms_list'] = forms_list
        session['sem'] = form0.sem_select.data

        return redirect(url_for('admin.remit_grades_step2'))

    return render_template('admin/grades/grades-remission-step1.html', title="Choose Among Classes", form0=form0)

    #####################################################


@admin.route('/admin/system-management/grades/step2', methods=['GET', 'POST'])
@login_required
def remit_grades_step2():

    students_list = session['students_list']

    form01 = StudentSelectionForm(prefix="students")
    form01.student_select.choices = [(None, "Choose a student")]
    for student in students_list:
        form01.student_select.choices += [(student['cin'],
                                           student['f_name'] + " " + student['l_name'])]

    if form01.validate_on_submit():
        std = form01.student_select.data

        student = students_collection.find_one({'cin': int(std)})
        student = dict(student)

        student.pop('_id', None)
        student.pop('password', None)
        student.pop('class_name', None)
        student.pop('inscription_date', None)
        session['student'] = student

        return redirect(url_for('admin.remit_grades_step3', data=data))
    return render_template('admin/grades/grades-remission-step2.html', title='Choose Among Students', form01=form01, data=data)

    ##########################################


@admin.route('/admin/system-management/grades/step3', methods=['GET', 'POST'])
@login_required
def remit_grades_step3():
    data = session['data']
    push_data = data
    student = session['student']
    sem = session['sem']

    modules = data[sem]
    modules_list = []
    forms_list = dict()

    for module in modules:
        subject_list = []
        i = 0
        for subject in module['subjects']:
            subject_list.append(subject)
            str = f'{ module["module_name"] }.{ subject["subject"] }'
            #forms_list.append( ((RemitSubjectGradeForm(prefix=str)), str))
            forms_list[f'{subject["subject"]}'] = RemitSubjectGradeForm(prefix=str)


        modules_list.append(
            {'module': module["module_name"], 'subject': subject_list})
    # end choices


    if request.method == 'POST':  
        imd = ImmutableMultiDict(request.form)
        imd = imd.to_dict(flat=False)



        p = None
        for key, value in imd.items() :   # iter on both keys and values
            if key.endswith('-pp') and value[1] != '':
               p = key[:-3]
               break
        
        p = p.split('.')
        mod = p[0]
        sub = p[1]

        index = 0
        for module in modules:
            if module.get("module_name") == mod:
                break
            index += 1

        i = 0
        for subject in push_data[sem][index]["subjects"]:
            if subject.get("subject") == sub:
                break
            i += 1
   
        push_data["student"] = student
        push_data[sem][index]["subjects"][i]["tp"] = request.form[f'{mod}.{sub}-tp']
        push_data[sem][index]["subjects"][i]['ds'] = request.form[f'{mod}.{sub}-ds']
        push_data[sem][index]["subjects"][i]['exam'] = request.form[f'{mod}.{sub}-exam']

        session['final_push_data'] = push_data[sem]

        
        flash('Add other grades or submit added ones to database', 'info')
    # , forms_list=forms_list
    return render_template('admin/grades/grades-remission-step3.html', title='Submit Grades', forms=forms_list, modules=modules_list)


@admin.route('/admin/system-management/grades/push', methods=['GET', 'POST'])
@login_required
def remit_grades_push():
    final_push_data = session['final_push_data']
    data = session['data']
    sem = session['sem']
    stud = session['student']
    exist = grades.find_one({'student.email': stud['email'] })
    if exist is  None:
        data[sem] = final_push_data
        grades.insert(data)

    else:
        grades.update_one({'student.email': stud['email'] }, { '$set':{ sem: final_push_data } }, upsert=True)

    # grades.insert(final_push_data)

    session.pop('final_push_data')
    session.pop('students_list')
    session.pop('data')
    session.pop('student')
    session.pop('sem')

    flash('Grades where pushed to database succesfully', 'info')
    return redirect(url_for('main.home'))


@admin.route('/admin/system-management/classes/', methods=['GET', 'POST'])
@login_required
def view_classes():
    data = data_collection.find({}, {'class_name': 1})
    classes_final = list()
    for st in data:
        st = dict(st)
        classes_final.append(st['class_name'])

    return render_template('admin/access/view-classes.html', classes=classes_final, title='Consult Your Classes')



@admin.route('/admin/system-management/classes/delete/<string:name>/', methods=['GET', 'POST'])
@login_required
def delete_classes(name):

    data_collection.delete_one({'class_name': name})
    students_collection.delete_many({'class_name': name})
    grades.delete_many({'class_name': name})

    flash('Deletion have been done successfully', 'success')
    return redirect(url_for('admin.view_classes'))





@admin.route('/admin/system-management/students/', methods=['GET', 'POST'])
@login_required
def view_students():

    classes = data_collection.find({}, {'class_name':1})

    classes_final = list()
    for st in classes:
        st = dict(st)
        classes_final.append(st)

    form = ClassesForm()
    form.class_select.choices = [(None, 'Choose Class')]
    form.class_select.choices += [(mah_class['class_name'], mah_class['class_name']) for mah_class in classes_final]

    if form.validate_on_submit():
        dt = form.class_select.data
        students = students_collection.find({'class_name': dt}, {'_id': 1, 'f_name': 1, 'l_name': 1, 'email': 1, 'cin': 1})

        students_final = list()
        for st in students:
            st = dict(st)
            students_final.append(st)

        
        return render_template('admin/access/view-students.html', form=form, students=students_final, title='Consult Students')


    return render_template('admin/access/view-students.html', form=form, title='Consult Students')
    

@admin.route('/admin/system-management/students/delete/<string:id>/', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    students_collection.delete_one({'_id': ObjectId(id)})
    flash('Deletion have been done successfully', 'success')
    return redirect(url_for('admin.view_students'))