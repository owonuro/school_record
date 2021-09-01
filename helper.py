#helper function for flask
from datetime import datetime, date, time

#This function is used at the index page to get details(no.) of pupils and subject in each class. 
def pupil_listf(classa,pupils,subject):
	class_l = {}
	for cl in classa:
		class_l.setdefault(cl, [0,0])
		for pup in pupils:
			if cl == pup:
				class_l[cl][0] = class_l[cl][0] + 1
	for cl in classa:
		class_l.setdefault(cl, [0,0])
		for sub in subject:
			if cl == sub:
				class_l[cl][1] = class_l[cl][1] + 1
	return class_l
	
def curr_date():
	today = str(date.today())
	return today
	
	
	
def broad_sheet_f(pupils, subjects, scores):
	"""This helper function is used to create the broadsheet data for easy processing."""
	if len(subjects) < 1:
		return None
	elif len(scores) < 1:
		return None
	record = {}
	for pup in pupils:
		name = pup.l_name + ' ' + pup.f_name
		record.setdefault(name,{})
		pupil_record = []		
		for score in scores:
			if pup.id == score.pupil_id:
				pupil_record.append(score)
		for sub in subjects:
			record[name].setdefault(sub, [])
			for rec in pupil_record:
				if sub == rec.subject_name:
						record[name][sub].append(rec.test_1 + rec.test_2)
						record[name][sub].append(rec.exam)
						record[name][sub].append(rec.test_1 + rec.test_2 + rec.exam)
						
		record[name].setdefault('grand_total', 0)
		total =0
		for key, value in record[name].items():
			if key != 'grand_total' and len(value) > 1:
				total += value[2]
		record[name]['grand_total'] = total
						
	return record
	
	
	
def pupil_scores(pupil, subjects, scores):
	"""This helper function is used to create the broadsheet data for easy processing."""
	if len(subjects) < 1:
		return None
	elif len(scores) < 1:
		return None
	record = {}
	for sub in subjects:
		record.setdefault(sub, [])
		for rec in scores:
			if sub == rec.subject_name:
					record[sub].append(rec.test_1 + rec.test_2)
					record[sub].append(rec.exam)
					record[sub].append(rec.test_1 + rec.test_2 + rec.exam)
	#This is to calculate over 40					
	record.setdefault('grand_total', [])
	total =0
	for key, value in record.items():
		if key != 'grand_total' and len(value) > 1:
			total += value[0]
	record['grand_total'].append(total)
	#This is to calculate over 60
	total =0
	for key, value in record.items():
		if key != 'grand_total' and len(value) > 1:
			total += value[1]
	record['grand_total'].append(total)
	#This is to calculate over 100
	total =0
	for key, value in record.items():
		if key != 'grand_total' and len(value) > 1:
			total += value[2]
	record['grand_total'].append(total)
						
	return record
	

	
