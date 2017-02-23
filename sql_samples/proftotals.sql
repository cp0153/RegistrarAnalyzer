select instructor, count(*) from registrar_analyzer_courses
where course_name = 'Computing I'
GROUP BY registrar_analyzer_courses.instructor, registar_analyzer_courses.semester
ORDER BY count(*);