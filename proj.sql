create database if not exists mysql_project;
use mysql_project;

create table if not exists bmi_persons
(
id int primary key auto_increment,
name varchar(20),
age decimal(2,0),
phone decimal(10,0),
gender enum('m','f'),
bmi decimal(4,2)
);

desc bmi_persons;

select * from bmi_persons;
