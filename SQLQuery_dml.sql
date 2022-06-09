
-- Filling the department_dim :
-- INSERT INTO dwh.department_dim VALUES (1,'Mathematics & Computation'),(2,'Digital Media & Entertainment Technology'); --
INSERT INTO `dwh`.`department_dim`(`department_id`,`department_name`) select distinct `department_id`, `department_name` from nlidb.department;


-- Filling professors_dim :
INSERT INTO dwh.professors_dim ( professor_id, job_title,first_name,last_name,gender,contact_email,contact_phone,office_number,webpage,date_of_birth )
SELECT  DISTINCT professor_id, job_title, first_name,last_name,gender,contact_email,contact_phone,office_number,webpage,date_of_birth  
FROM   nlidb.professors;

-- Filling publications_dim :
INSERT INTO dwh.publications_dim ( publication_id,publication_title,publication_abstract,journal_name,conference_name)
SELECT  DISTINCT publication_id,publication_title,publication_abstract,journal,conference
FROM   nlidb.publications;

-- Filling research_interest_dim :
INSERT INTO dwh.research_interest_dim (research_area_id,research_area_title,research_area_description )
SELECT  DISTINCT research_area_id,research_area_title,research_area_description
FROM   nlidb.research_interest;

-- Filling research_projects_dim :
INSERT INTO dwh.research_projects_dim (research_project_id,research_project_title,research_project_description )
SELECT  DISTINCT research_project_id,research_project_title,research_project_description
FROM   nlidb.research_projects;

-- Filling research_students_dim :
INSERT INTO dwh.research_students_dim (student_id,student_name,student_email,research_project_title,research_project_description)
SELECT  DISTINCT student_id,student_name,student_email,research_project_title,research_project_description
FROM   nlidb.research_students;

-- Filling calender_dim :
INSERT INTO dwh.calender_dim (item_id,title,description,week_day,time_from,time_to,location,flag,flag_description,start_date,end_date)
SELECT  DISTINCT item_id,title,description,week_day,time_from,time_to,location,flag,flag_description,start_date,end_date
FROM   nlidb.calendar;

-- Filling research_fact_table : 

insert into  dwh.research_fact_table (  research_area_id ,research_project_id,student_id, publication_id, professor_id , department_id,item_id)
select   intr.research_area_id, proj.research_project_id, stud.student_id, pub.publication_id , prof.professor_id, dep.department_id, cal.item_id
from nlidb.professors  as  prof
left join nlidb.research_interest as intr  on intr.professor_id = prof.professor_id
left join nlidb.publications as pub on pub.professor_id = prof.professor_id
left join nlidb.department as dep on dep.department_id = prof.department_id
left join nlidb.research_projects as proj on intr.research_area_id = proj.research_area_id
left Join nlidb.calendar as cal on cal.professor_id = prof.professor_id
left join nlidb.research_students as stud on prof.professor_id = stud.professor_id;

commit;
