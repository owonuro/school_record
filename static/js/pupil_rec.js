/*function  loadMess() {alert("Welcome to advance record keeping software")}*/
const color1 = 'orange'
const color2 = 'wheat'

function displayMe(clicked_id) {
var click = document.getElementById(clicked_id)
click.style.backgroundColor = color2
var pup = document.getElementById('c_pupil')
var sub = document.getElementById('c_subject')
var tea = document.getElementById('c_teacher')
var pupil = document.getElementById('classroom_pupil');
var subject = document.getElementById('classroom_subject');
var teacher = document.getElementById('classroom_teacher');
if (clicked_id == 'c_pupil') {
		if (pupil.style.display == 'none') {
		pupil.style.display = 'block'
		sub.style.backgroundColor = color1
		tea.style.backgroundColor = color1
		teacher.style.display = 'none'
		subject.style.display = 'none'
		}
}
else if (clicked_id == 'c_subject') {
if (subject.style.display == 'none') {
		pupil.style.display = 'none'
		teacher.style.display = 'none'
		pup.style.backgroundColor = color1
		tea.style.backgroundColor = color1
		subject.style.display = 'block'
		}
}
else if (clicked_id == 'c_teacher') {
if (teacher.style.display == 'none') {
		pupil.style.display = 'none'
		teacher.style.display = 'block'
		pup.style.backgroundColor = color1
		sub.style.backgroundColor = color1
		subject.style.display = 'none'
		}
}

}

/*The code below is used to prevent accidental delete. */
var listOfAs;
function selectAs(){
listOfAs = document.getElementsByTagName('a');
for (var i = 0; i < listOfAs.length; i++) {
	var select = listOfAs[i];
	if (select.innerHTML == 'delete') {
		select.addEventListener('click', conD)

}


}
}

function conD(e){
	var con= confirm('Are you sure you want to delete.');
	if (con !== true) {
	e.preventDefault();	
	}
	}
	
/* The accidental delete codev stops here.*/

/*This function is to change the color of currently editted row*/

function par(ele) {
	let select =  ele.parentElement
	let select2 = select.parentElement.style.color = 'red'
	}
	
function par2(ele) {
	let select =  ele.parentElement
	let select2 = select.parentElement.style.color = 'black'
	}
	
	
function inputSum(myclass) {
	var totalSc = 0;
	let select =  myclass.parentElement;
	let select2 = select.parentElement;
	let select3 = select2.children;
	
	for (let x = 0; x < select3.length; x++ ) {
		
		if (select3[x].children) {
			select4 = select3[x].children
			for (let t = 0; t < select4.length; t++ ) {
			
			totalSc += parseInt(select4[t].value);			
			}}	

}
let selectId = select2.id;
let selectId2 = selectId.toString()
let tt = document.getElementById('input-total_' + selectId2);

tt.innerHTML  = totalSc;

}	
	
