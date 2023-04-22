DROP TABLE IF EXISTS subject CASCADE;
DROP TABLE IF EXISTS teacher CASCADE;
DROP TABLE IF EXISTS timetable CASCADE;

CREATE TABLE subject
(
	id INT NOT NULL PRIMARY KEY,
	title TEXT NOT NULL,
	type TEXT NOT NULL
);

CREATE TABLE teacher
(
	id INT NOT NULL PRIMARY KEY,
	full_name TEXT NOT NULL,
	subject_id INT NOT NULL REFERENCES subject(id)
);

CREATE TABLE timetable
(
	id INT NOT NULL PRIMARY KEY,
	week INT NOT NULL,
	day TEXT NOT NULL,
	subject_id INT NOT NULL REFERENCES subject(id),
	room_numb TEXT NOT NULL,
	num INT NOT NULL
);

CREATE OR REPLACE PROCEDURE insert_values
(
	subject.title, 
	subject.type, 
	teacher.full_name, 
	timetable.week, 
	timetable.day, 
	timetable.room_numb, 
	timetable.num
)
LANGUAGE plpgsql AS $$
DECLARE
	new_subject_id INT;
	new_teacher_id INT;
	new_timetable_id INT;
BEGIN
	SELECT COALESCE(MAX(id), 0) + 1 INTO new_subject_id FROM subject;
	SELECT COALESCE(MAX(id), 0) + 1 INTO new_teacher_id FROM teacher;
	SELECT COALESCE(MAX)
