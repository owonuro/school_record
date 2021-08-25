import sqlite3, logging as log

log.basicConfig(level = log.DEBUG, format='%(asctime)s > %(levelno)s %(message)s')

class Individual():
	'''This is to model individual'''
	def __init__(self, fname, lname, sex):
		self.name = fname + " " + lname
		self.age = None
		self.sex = sex
		self.state = None
		self.myclass = None
		self.subjects = []
		
	def __str__(self):
		return f'{self.name}'
		
	def __repr__(self):
		return f'{self}'
	
	def my_class(self, cl):
		self.myclass = cl
	
	def add_subject(self, sub):
		self.subjects.append(sub)


class Teacher(Individual):
	'''This class is used to create individuial teacher'''
	def __init__(self, name):
		super().__init__(name)
		self.salary = None
		self.qualification = None
		
		
		
	
		
	
		

class Pupil(Individual):
	
	def __init__(self, fname,lname,sex):
		super().__init__(fname, lname, sex)	
		self.subjects = []
	
	def update_markspu(self, subject, test, score ):
		if len(self.subjects) >=1:
			for sub in self.subjects:
				if sub == subject:
					sub.update_marks(test,score)
	
	def add_subject(self, sub):
		self.sub = Subject(sub)
		self.subjects.append(sub)
		

##################################################################################################################################
	
class Subject():
	'''This is to create subjects'''
	def __init__(self, name, test1 =0, test2 = 0, exam =0):
		self.name = name
		self.test = test1 + test2
		self.exam = exam
		self.total = self.test + self.exam
		
		
	def __repr__ (self):
		return f'{self.name}'
		
		
	def display_marks(self):
		return 0
		
	


############################################################################################################
