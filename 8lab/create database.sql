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
	day INT NOT NULL,
	subject_id INT NOT NULL REFERENCES subject(id),
	room_numb TEXT NOT NULL,
	num INT NOT NULL
);

CREATE OR REPLACE PROCEDURE insert_values
(
	timetable_week INT, 
	timetable_day INT,
	timetable_num INT,
	timetable_room_numb TEXT,
	subject_type TEXT,
	teacher_fullname TEXT,
	subject_title TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
	new_subject_id INT;
	new_teacher_id INT;
	new_timetable_id INT;
BEGIN
	SELECT id INTO new_subject_id FROM subject 
	WHERE subject.title=subject_title and subject.type=subject_type;
	IF new_subject_id IS NULL
	THEN
		SELECT COALESCE(MAX(id), 0) + 1 INTO new_subject_id FROM subject;
		SELECT COALESCE(MAX(id), 0) + 1 INTO new_teacher_id FROM teacher;
		SELECT COALESCE(MAX(id), 0) + 1 INTO new_timetable_id FROM timetable;
		INSERT INTO subject VALUES(new_subject_id, subject_title, subject_type);
		INSERT INTO teacher VALUES(new_teacher_id, teacher_fullname, new_subject_id);
		INSERT INTO timetable VALUES(
			new_timetable_id,
			timetable_week,
			timetable_day,
			new_subject_id,
			timetable_room_numb,
			timetable_num
		);
	ELSE
		SELECT id INTO new_teacher_id FROM teacher WHERE subject_id=new_subject_id;
		SELECT COALESCE(MAX(id), 0) + 1 INTO new_timetable_id FROM timetable;
		INSERT INTO timetable VALUES(
			new_timetable_id,
			timetable_week,
			timetable_day,
			new_subject_id,
			timetable_room_numb,
			timetable_num
		);
	END IF;
END;
$$;

CALL insert_values(1, 2, 1, 'Н-405', 'практика', 'Воронова Е.В.', 'Иностранный язык (до 15 нед.)');
CALL insert_values(1,2,2, 'Н-С/Зал', 'практика', 'Королева С.А.', 'Игровые виды спорта (до 15 нед.)');
CALL insert_values(1,3,3, 'Н-514', 'лекция', 'Шаймарданова Л.К.','Высшая математика (до 17 нед.)');
CALL insert_values(1,3,4, 'Н-226', 'лекция', 'Вальковский С.Н.', 'Физика (до 17 нед.)');
CALL insert_values(1,3,5, 'Н-С/Зал', 'практика', 'Королева С.А', 'Игровые виды спорта (до 15 нед.)');
CALL insert_values(1,4,3, 'А-Л-208', 'практика', 'Фурлетов Ю.М.', 'Введение в информационные технологии (до 15 нед.)');
CALL insert_values(1,4,4, 'А-Л-203', 'лабораторная работа', 'Фурлетов Ю.М.', 'Введение в информационные технологии (до 15 нед.)');
CALL insert_values(1,5,1, 'Н-227', 'лекция', 'Скляр Л.Н.', 'История (история России, всеобщая история) (до 17 нед.)');
CALL insert_values(1,5,2, 'Н-535', 'лекция', 'Полищук Ю.В.', 'Математические основы баз данных (до 15 нед.)');
CALL insert_values(1,5,3, 'Н-314', 'практика', 'Шаймарданова Л.К.', 'Высшая математика (до 15 нед.)');
CALL insert_values(1,5,4, 'Н-314', 'практика', 'Шаймарданова Л.К.', 'Высшая математика (до 15 нед.)');
CALL insert_values(1,6,1, 'А-414', 'лабораторная работа', 'Изотова А.А.', 'Математические основы баз данных (до 15 нед.)');
CALL insert_values(1,6,2, 'А-Л-203', 'практика', 'Потапченко Т.Д.', 'Проектный практикум (до 15 нед.)');
CALL insert_values(1,6,3, 'А-ВЦ-302', 'лабораторная работа', 'Липатов В.Н.', 'Основы DevOps (до 15 нед.)');
CALL insert_values(1,6,4, 'А-ВЦ-302', 'лабораторная работа', 'Липатов В.Н.', 'Основы DevOps (до 15 нед.)');
CALL insert_values(2,1,2, 'Н-514', 'лекция', 'Шаймарданова Л.К.', 'Высшая математика (до 16 нед.)');
CALL insert_values(2,1,3, 'Н-С/Зал', 'практика', 'Королева С.А.', 'Игровые виды спорта (до 16 нед.)');
CALL insert_values(2,1,4, 'Н-404', 'практика', 'Воронова Е.В.', 'Иностранный язык (до 14 нед.)');
CALL insert_values(2,3,1, 'А-Л-205', 'лабораторная работа', 'Фурлетов Ю.М.', 'Введение в информационные технологии (до 16 нед.)');
CALL insert_values(2,3,3, 'А-414', 'практика', 'Городничев М.Г.', 'Основы DevOps (до 16 нед.)');
CALL insert_values(2,4,1, 'Н-332а', 'практика', 'Бурлаков Е.В.', 'Физика (до 18 нед.)');
CALL insert_values(2,4,2, 'Н-332а', 'лабораторная работа', 'Бурлаков Е.В.', 'Физика (до 18 нед.)');
CALL insert_values(2,4,3, 'Н-318', 'практика', 'Скляр Л.Н.', 'История (история России, всеобщая история) (до 18 нед.)');
CALL insert_values(2,4,4, 'Н-404', 'практика', 'Полищук Ю.В.', 'Математические основы баз данных (до 16 нед.)');
CALL insert_values(2,5,3, 'Н-С/Зал', 'практика', 'Королева С.А.', 'Игровые виды спорта (до 16 нед.)');
CALL insert_values(2,5,4, 'Н-318', 'практика', 'Скляр Л.Н.', 'История (история России, всеобщая история) (до 18 нед.)');

SELECT timetable.week, timetable.day, timetable.num, 
timetable.room_numb, subject.type, teacher.full_name, subject.title
FROM subject
JOIN teacher ON (subject.id = teacher.subject_id)
JOIN timetable ON (subject.id = timetable.subject_id)

	
