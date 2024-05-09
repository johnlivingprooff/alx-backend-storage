-- lists all students who have a score under 80 (strict)

CREATE VIEW need_meeting AS
SELECT student_name
FROM students
WHERE score < 80
AND (last_meeting IS NULL OR last_meeting < DATE_SUB(NOW(), INTERVAL 1 MONTH));
