CREATE OR REPLACE PROCEDURE delete_values
(
	timetable_week INT, 
	timetable_day INT,
	timetable_num INT

)
LANGUAGE plpgsql AS $$
DECLARE
	my_subject_id INT;
	rowss INT;
BEGIN
	SELECT subject_id INTO my_subject_id FROM timetable 
	WHERE day=timetable_day AND week=timetable_week AND num = timetable_num;
	SELECT count(*) INTO rowss FROM timetable
	WHERE subject_id = my_subject_id;
	
	IF rowss > 1
	THEN
		DELETE FROM timetable
		WHERE day=timetable_day AND week=timetable_week AND num = timetable_num;
	ELSE
		DELETE FROM timetable WHERE subject_id = my_subject_id;
		DELETE FROM teacher WHERE subject_id = my_subject_id;
		DELETE FROM subject WHERE id = my_subject_id;
	END IF;
END;
$$;
