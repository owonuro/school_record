from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import shelve
import helper


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)

class Pupil(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	f_name = db.Column(db.String(200), nullable = False)
	l_name = db.Column(db.String(200), nullable = False)
	gender = db.Column(db.String(200), nullable = False)
	dob = db.Column(db.DateTime)
	classroom = db.Column(db.String(50), nullable = False)
	scores = db.relationship('Score', backref = 'pupil', lazy =True )
	date_created = db.Column(db.DateTime, default = datetime.utcnow )
	
	def __repr__(self):
		return '<Pupil %r>' %self.id
		

class Score(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	pupil_id = db.Column(db.Integer, db.ForeignKey('pupil.id'),
        nullable=False)
	test_1= db.Column(db.Integer)
	test_2 = db.Column(db.Integer)
	exam = db.Column(db.Integer)
	subject_name = db.Column(db.String(50), nullable = False)
	classroom = db.Column(db.String(50), nullable = False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow )
	
	def __repr__(self):
		return '<Score %r>' %self.id
		

class Classroom(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable = False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow )
	
	def __repr__(self):
		return '<Class %r>' %self.name
		
		
class Subject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable = False)
	classroom = db.Column(db.String(50), nullable = False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow )
	
	def __repr__(self):
		return '<Subject %r>' %self.name
		
	


@app.route('/')
def home():
	today = helper.curr_date()
	class_list =Classroom.query.order_by(Classroom.name).all()
	class_list2 = [a.name for a in class_list]
	pupil_list = Pupil.query.order_by(Pupil.classroom).all()
	pupil_list2 = [a.classroom for a in pupil_list]
	subject_list = Subject.query.order_by(Subject.classroom).all()
	subject_list2 = [a.classroom for a in subject_list]
	classes2 = helper.pupil_listf(classa = class_list2,pupils= pupil_list2,subject =subject_list2)
	return render_template('index.html', classes = class_list, classes2 = classes2, today = today )
	
	
	
@app.route('/create_class')
def create_class():
	today = helper.curr_date()
	return render_template('create_class.html', today = today)
	
	
@app.route('/add_pupil', methods =['GET','POST'])
def add_pupil():
	today = helper.curr_date()
	if request.method == 'GET':
		return redirect('/')
	
	elif request.method == 'POST':
		class_room = request.form['class-name']
		class_list_1 = Classroom.query.all()
		class_list_2 =[a.name for a in class_list_1 if a.name == class_room ] 
		if len(class_list_2) > 0:
			cl_list = [a.name for a in class_list_1]
			return render_template('add_pupil.html', cln =class_room, class_list = cl_list)
		else:
			new_class = Classroom(name = class_room)
			cl_list = [a.name for a in class_list_1]
			try:
				db.session.add(new_class)
				db.session.commit()
				return render_template('add_pupil.html', cln =class_room, class_list = cl_list)
			except Exception as e:
				return f'There was {e} error \n'
		
@app.route('/add_more_pupil', methods =['GET','POST'])
def add_more_pupil():
	today = helper.curr_date()
	if request.method == 'GET':
		return redirect('/')
	elif request.method == 'POST':
		class_room = request.form['class-name']
		s_name = request.form['surname']
		
		f_name = request.form['first-name']
		sex = request.form['sex']
		#Want to work on making this a global variable
		working_classroom = class_room
		#I used the shelve module to save  a wide used variable as flask would not allow global variable to function properly
		shelve_data = shelve.open('shelve_data')
		shelve_data['class'] = class_room
		shelve_data.close()
		new_pupil = Pupil(classroom = class_room, l_name=s_name, f_name = f_name, gender = sex)
		class_list = Classroom.query.all()
		cl_list = [a.name for a in class_list]
		
	try:
		db.session.add(new_pupil)
		db.session.commit()
		return render_template('add_more_pupil.html', cln =class_room, fn =f_name, sn = s_name, sex = sex, class_list = cl_list, today = today)
	except Exception as e:
			msg = 'There was an issue adding your task!'
			return f'There was {e} error \n'		

@app.route('/add_subject')
def add_subject():
	today = helper.curr_date()
	#I used the shelve module to save  a wide used variable as flask would not allow global variable to function properly
	shelve_data = shelve.open('shelve_data')
	class_room = shelve_data['class']
	shelve_data.close()
	class_list = Classroom.query.all()
	cl_list = [a.name for a in class_list]
	
	return render_template('add_subject.html', cln =class_room, class_list = cl_list, toady = today )
	
	
@app.route('/add_more_subject', methods =['POST','GET'])
def add_more_subject():
	today = helper.curr_date()
	if request.method == 'GET':
		return redirect('/')
	elif request.method == 'POST':
		#I used the shelve module to save  a wide used variable as flask would not allow global variable to function properly
		shelve_data = shelve.open('shelve_data')
		class_room = shelve_data['class']
		shelve_data.close()
		new_subject = Subject(name = request.form['subject'],classroom = request.form['class-name'] )
		
	try:
		db.session.add(new_subject)
		db.session.commit()
		subjects = Subject.query.all()
		asub = [a.name for a in subjects if a.classroom == class_room]
		class_list = Classroom.query.all()
		cl_list = [a.name for a in class_list]
		return render_template('add_more_subject.html', cln =class_room, sub = asub, class_list = cl_list )
	except Exception as e:
			msg = 'There was an issue adding your task!'
			return f'There was {e} error \n'	
			
@app.route('/classroom/<class_name>')
def classroom(class_name):
	today = helper.curr_date()
	pupils = Pupil.query.filter_by(classroom = class_name).order_by(Pupil.l_name).all()
	subjects = Subject.query.filter_by(classroom = class_name).all()
	shelve_data = shelve.open('shelve_data')
	shelve_data['class'] = class_name
	shelve_data.close()
	return render_template('classroom.html', cl_name = class_name, pupils = pupils, subjects = subjects,today = today)
	
'''
@app.route('/classroom/<class_name>/sub')
def classroom_sub(class_name):
	today = helper.curr_date()
	subjects = Subject.query.filter_by(classroom = class_name).all()
	sub_list = [a for a in subjects if a.classroom == class_name]
	shelve_data = shelve.open('shelve_data')
	shelve_data['class'] = class_name
	shelve_data.close()
	return render_template('classroom_subject.html', cl_name = class_name, sub_list = sub_list, today = today)	
'''
	
@app.route('/delete/<int:id>')
def delete(id):
	delete_pupil = Pupil.query.get_or_404(id)
	try:
		db.session.delete(delete_pupil)
		db.session.commit()
		shelve_data = shelve.open('shelve_data')
		class_name = shelve_data['class']
		shelve_data.close()
		return redirect('/classroom/' + class_name)
	except Exception as e:
		return f"There was \n{e}\nError "
		

@app.route('/delete_1/<int:id>')
def delete_1(id):
	delete_sub = Subject.query.get_or_404(id)
	delete_score = Score.query.filter_by(subject_name =  delete_sub.name, classroom = delete_sub.classroom).all()
	for scores in delete_score:
		try:
			db.session.delete(scores)
			db.session.commit()
		except Exception as e:
			return f"There was \n{e} \nproblem!"
	try:
		db.session.delete(delete_sub)
		db.session.commit()
		shelve_data = shelve.open('shelve_data')
		class_name = shelve_data['class']
		shelve_data.close()
		return redirect('/classroom/' + class_name)
	except Exception as e:
		return f"There was \n{e} \nproblem!"
		

@app.route("/<class_name>/<subject_name>/score", methods =['POST', 'GET'])
def score_route(class_name, subject_name):
	today = helper.curr_date()
	if request.method == 'GET':
		pupils = Pupil.query.filter_by(classroom = class_name).order_by (Pupil.l_name).all()
		scores = Score.query.filter_by(subject_name = subject_name, classroom = class_name).all()
		result = None
		scores_2 = [a.pupil_id for a in scores]
	elif request.method == 'POST':
		result = request.form
		pupil_id = 0
		test1_score = 0
		test2_score = 0
		exam_score = 0
		test_id = 0
		rtest1_score =0
		rtest2_score =0
		rexam_score = 0
		for a, b in result.items():
			if a.startswith('test1'):
				test = a.split('_')
				pupil_id = test[1]
				test1_score = b
			elif a.startswith('test2'):
				test = a.split('_')
				pupil_id = test[1]
				test2_score = b
			elif a.startswith('exam'):
				exam_score = b
				new_score = Score(pupil_id = pupil_id, test_1 = test1_score, test_2 = test2_score, exam = exam_score, subject_name = subject_name, classroom = class_name)
				try:
					db.session.add(new_score)
					db.session.commit()
				except Exception as e:
					return f'There was \n{e} Error!'
			elif a.startswith('rtest1'):
				test2 = a.split('_')
				test2_id =int (test2[1])
				rtest1_score = b
			elif a.startswith('rtest2'):
				test2 = a.split('_')
				test2_id =int (test2[1])
				rtest2_score = b
			elif a.startswith('rexam'):
				rexam_score = b
				edit_score =Score.query.get_or_404(test2_id)
				edit_score.test_1 = rtest1_score
				edit_score.test_2 = rtest2_score				
				edit_score.exam = rexam_score
				try:
					db.session.commit()
				except Exception as e:
					return f'There was \n{e} \nError!'
					
		pupils = Pupil.query.filter_by(classroom = class_name).order_by (Pupil.l_name).all()
		scores = Score.query.filter_by(subject_name = subject_name, classroom = class_name).all()	
		scores_2 = [a.pupil_id for a in scores]
	return render_template('scores.html', cl_name = class_name, sub_name = subject_name, pup_list = pupils, scores = scores, result = result, scores_2 =scores_2, today = today)

@app.route("/<class_name>/<subject_name>/score_edit")
def score_route_edit(class_name, subject_name):
	today = helper.curr_date()
	pupils = Pupil.query.filter_by(classroom = class_name).order_by(Pupil.l_name).all()
	scores = Score.query.filter_by(subject_name = subject_name, classroom = class_name).all()
	#I need to recheck this and comment properly
	scores_2 = [a.pupil_id for a in scores]
	return render_template('scores_edit.html', today = today, cl_name = class_name, sub_name = subject_name, pup_list = pupils, scores = scores, scores_2 = scores_2 )

@app.route("/<class_name>/broad_sheet", methods =['POST', 'GET'])
def broad_sheet(class_name):
	today = helper.curr_date()
	pupils = Pupil.query.filter_by(classroom = class_name).order_by(Pupil.l_name).all()
	scores = Score.query.filter_by(classroom = class_name).all()
	subject_list = Subject.query.filter_by(classroom = class_name).order_by(Subject.name).all()
	subject_list2 = [a.name for a in subject_list]
	broad_sheet1 = helper.broad_sheet_f(pupils = pupils, subjects = subject_list2, scores = scores)
	return render_template('test.html', cl_name = class_name, broad_sheet = broad_sheet1, subjects = subject_list2)
	
	
@app.route('/pupil/<int:id>')
def pupil(id):
	pupil_d = Pupil.query.get_or_404(id)
	
	scores = Score.query.filter_by(pupil_id = id).all()
	subject_list = Subject.query.filter_by(classroom = pupil_d.classroom).order_by(Subject.name).all()
	subject_list2 = [a.name for a in subject_list]
	pupil_scores = helper.pupil_scores(pupil = pupil_d, subjects = subject_list2, scores = scores)
	
	return render_template('pupil.html', pupil = pupil_d, broad_sheet = pupil_scores, subjects = subject_list2)
	

if __name__=='__main__':
	db.create_all()
	app.run(host='0.0.0.0', debug=True)
