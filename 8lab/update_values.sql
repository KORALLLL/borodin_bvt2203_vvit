CREATE OR REPLACE PROCEDURE update_values
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
	my_subject_id INT;
BEGIN
	SELECT subject_id INTO my_subject_id FROM timetable
	WHERE day = timetable_day AND week = timetable_week AND num = timetable_num;

	
	UPDATE subject SET type = subject_type, title=subject_title WHERE id = my_subject_id;
	UPDATE teacher SET full_name = teacher_fullname WHERE subject_id = my_subject_id;
	UPDATE timetable SET room_numb = timetable_room_numb WHERE subject_id = my_subject_id;
END;
$$;


CALL update_values(2,1,2,'Н-514','Лекция','Шаймарданова Л. К.', 'Высшая математика');
