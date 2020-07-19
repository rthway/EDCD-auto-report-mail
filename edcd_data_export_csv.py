import mysql.connector
import csv 

header = ['IP', 'Name', 'age','Gender','VDC','date_diagnosed','Ward','District','Diag']
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="openmrs"
)

mycursor = mydb.cursor()

sql = "SELECT \
pi.identifier AS 'IP', \
CONCAT_WS(' ', pn.given_name, pn.middle_name, pn.family_name) as 'Name', \
TIMESTAMPDIFF(Month,p.birthdate,CURDATE()) AS age, \
p.gender, \
pa.city_village as 'VDC', \
date(o.obs_datetime) as 'date_diagnosed', \
pa.address1 as 'Ward', \
pa.county_district as 'District', \
(select name from concept_name where concept_id = o.value_coded AND \
       o.voided IS FALSE and concept_name_type = 'FULLY_SPECIFIED' and voided = '0') as Diag \
FROM \
person p \
INNER JOIN \
patient_identifier pi ON p.person_id = pi.patient_id \
AND pi.identifier != 'CKT100208' \
AND pi.voided = '0' \
INNER JOIN \
person_name pn ON pn.person_id = p.person_id \
AND pn.voided = '0' \
INNER JOIN \
person_address pa ON pa.person_id = pn.person_id \
AND pa.voided = '0' \
INNER JOIN \
visit v ON v.patient_id = p.person_id \
INNER JOIN \
obs o ON o.person_id = p.person_id \
and o.voided = '0' \
and o.concept_id = '15' AND o.value_coded in ('5501', '5505', '4863', '5499', '5500', '4640', '6929', '5487', '5496', '4163', '4653','5486','5510','5498')  \
 \
where p.voided = '0' \
and date(o.obs_datetime) between DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND DATE_SUB(CURDATE(),INTERVAL 1 DAY) \
group by IP, Name, age, gender, VDC, Ward, District, diag \
ORDER BY date_diagnosed ASC"

mycursor.execute(sql)

myresult = mycursor.fetchall()
c = csv.writer(open('/home/race/edcd.csv', 'w'))
c.writerow(header)
for x in myresult:
    c.writerow(x)
