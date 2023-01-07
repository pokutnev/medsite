import random
from homepage.models import *

def __generate_sfc():
    Name = ['Roman', 'Lida', 'Galina', 'Sofia', 'Anastasia', 'Nikolay', 'Eduard', 'Irina', 'Julia', 'Ivan']

    return Name[random.randint(0, len(Name) - 1)] + '.' + Name[random.randint(0, len(Name) - 1)][0] + '.' + Name[random.randint(0, len(Name) - 1)][0]

def __generate_address():
    Name = ['Romanovs', 'Lenin', 'Glory', 'Sovet', 'Story', 'Noviy', 'Urban', 'Irtal', 'July', 'Ivanov']

    return Name[random.randint(0, len(Name) - 1)] + ' st. ' + str(random.randint(1,100))

def __generate_prof():
    Name = ['Therapist', 'Senior Doctor', 'Doctor on duty', 'Intern']

    return Name[random.randint(0, len(Name) - 1)]

def __generate_diagnosis():
    Name = ['Flu', 'Coronavirus', 'Psoriasis', 'Hypertension', 'Tachycardia', 'Concussions', 'Schizophrenia']

    return Name[random.randint(0, len(Name) - 1)]

def __generate_datetime():
    y = str(random.randint(2020, 2022))
    mo = str(random.randint(1, 12))
    d = str(random.randint(1, 28))
    h = str(random.randint(8, 21))
    mi = str(random.randint(0, 59))
    s = str(random.randint(0, 59))

    if int(h) < 10:
        h = '0'+ h
    if int(mi) < 10:
        mi = '0'+ mi
    if int(s) < 10:
        s = '0'+ s

    return y + '-' + mo + '-' + d + ' ' + h + ':' + mi

def generate_contact(Contact_id):
    return Contact(sfc=__generate_sfc(), phone_num=random.randint(79000000000, 79999999999),
                   address=__generate_address())

def generate_customer(Customer_id, Cont_id):
    return Customers(contact_id=Cont_id)

def generate_doctor(Doctor_id, Cont_id):
    return Doctors(contact_id=Cont_id, profession=__generate_prof())

def generate_timetable(tt_id, cus, doc):
    return Timetable(meetdate=__generate_datetime(), diagnosis=__generate_diagnosis(),
                     customer=cus, doctor=doc)