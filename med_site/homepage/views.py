import csv
import io
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import TableStyle, Table, SimpleDocTemplate

from homepage.models import *
from homepage.generate import *
from homepage.forms import *



def homepage(request):
    return render(request, "homepage/index.html")

def sign(request):
    formLog = AddLoginForm()
    formReg = AddRegistForm()

    if request.method == 'POST':
        formLog = AddLoginForm(request.POST)
        formReg = AddRegistForm(request.POST)
        if formLog.is_valid():
            print(formLog.cleaned_data)
            user = authenticate(username=formLog.cleaned_data.get("login"), password=formLog.cleaned_data.get("password"))
            if user is not None:
                login(request, user)
                return redirect('homepage')
        if formReg.is_valid():
            print(formReg.cleaned_data)
            user = User.objects.create_user(formReg.cleaned_data.get('login'), '' , formReg.cleaned_data.get('password1'))
            user.first_name = formReg.cleaned_data.get('sfc')
            user.save()
            contact = Contact(sfc=formReg.cleaned_data.get('sfc'), phone_num=formReg.cleaned_data.get('phone_num'),
                              address=formReg.cleaned_data.get('address'), user=user)
            contact.save()
            customer = Customers(contact_id = contact)
            customer.save()
            return redirect('login')


    return render(request, "homepage/logreg.html", {'fl': formLog, 'fr': formReg})

def logout_user(request):
    logout(request)
    return redirect('login')

def doctors(request, profes='', doctor_id=''):
    if not request.user.is_authenticated:
        redirect('login')

    if profes == '':

        docs = Doctors.objects.all()

        d = {}

        for doc in docs:
            if doc.profession in d.keys():
                d[doc.profession] += 1
            else:
                d[doc.profession] = 1

        return render(request, "homepage/doctors.html", {'profs':d.keys()})
    elif doctor_id == '':

        docs = Doctors.objects.filter(profession=profes)

        d = []
        class ch:
            def __init__(self, id, name):
                self.id = id
                self.name = name

        for doc in docs:
            d.append(ch(doc.contact_id.id, doc.contact_id.sfc))

        return render(request, "homepage/doctors.html", {'profs':d, 'choose':profes})

def customers(request):
    return render(request, "homepage/customers.html")

def timetable(request):
    if not request.user.is_authenticated:
        redirect('login')

    if request.user.has_perm('homepage.view_timetable'):
        try:
            doc = Doctors.objects.get(contact_id=Contact.objects.get(user=request.user.id).id)
        except:
            return redirect('new_doc')

    if request.user.has_perm('homepage.view_timetable'):
        doc = Doctors.objects.get(contact_id=Contact.objects.get(user=request.user.id).id)
        TT = Timetable.objects.filter(doctor=doc)
    else:
        cus = Customers.objects.get(contact_id=Contact.objects.get(user=request.user.id).id)
        TT = Timetable.objects.filter(customer=cus)
    return render(request, "homepage/timetable.html", {'Tab':TT})

def generate(request):

    con = Contact.objects.all()
    cus = Customers.objects.all()
    doc = Doctors.objects.all()
    tim = Timetable.objects.all()

    con_c = con.count()
    cus_c = cus.count()
    doc_c = doc.count()
    tim_c = tim.count()

    for i in range(300):#generate customers
        a = generate_contact(i+con_c)
        a.save()
        b = generate_customer(i+cus_c, a)
        b.save()

    con_c += 300
    cus_c += 300

    for i in range(50):#generate doctors
        a = generate_contact(i+con_c)
        a.save()
        b = generate_doctor(i+doc_c, a)
        b.save()

    cus = Customers.objects.all()
    doc = Doctors.objects.all()
    cus_c = cus.count()
    doc_c = doc.count()

    for i in range(500):
        a = generate_timetable(i+tim_c, cus[random.randint(0, cus_c-1)], doc[random.randint(0, doc_c-1)])
        a.save()

    return HttpResponse('OK')

def download_pdf(request):
    cus = Customers.objects.get(contact_id=Contact.objects.get(user=request.user.id).id)
    TT = Timetable.objects.filter(customer=cus)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "timetable-%s.pdf" % str(cus.contact_id.sfc)
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    buff = io.StringIO()

    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=70, leftMargin=70, topMargin=70,
                            bottomMargin=60)
    elements = []

    data = [['Customer', 'Doctor', 'Date&Time', 'diagnosis']]
    for i in TT:
        data.append([i.customer.contact_id.sfc, i.doctor.contact_id.sfc, i.meetdate, i.diagnosis])
    t = Table(data)
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                           ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                           ('VALIGN', (0, 0), (0, -1), 'TOP'),
                           ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                           ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                           ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ]))

    elements.append(t)
    # write the document to
    doc.build(elements)

    print(response.items())

    # response.write(buff.getvalue())
    # buff.close()
    return response

def download_csv(request):
    cus = Customers.objects.get(contact_id=Contact.objects.get(user=request.user.id).id)
    TT = Timetable.objects.filter(customer=cus)

    # Create the HttpResponse object with the appropriate CSV header.

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="timetable.csv"'},
    )

    writer = csv.writer(response, delimiter =';')
    for i in TT:
        writer.writerow([i.customer.contact_id.sfc, i.doctor.contact_id.sfc, i.meetdate, i.diagnosis])

    return response

def appointment(request, profes, id):
    formTT = AppointmentForm()

    if request.method == 'POST':
        formTT = AppointmentForm(request.POST)
        if formTT.is_valid():
            print(formTT.cleaned_data.get('meetdate'))

            cus = Customers.objects.get(contact_id=Contact.objects.get(user=request.user.id).id)
            doc = Doctors.objects.get(contact_id=id)

            meet = Timetable(customer=cus, doctor=doc, meetdate=formTT.cleaned_data.get('meettime'))
            meet.save()
            return redirect('/')
    return render(request, "homepage/appointment.html", {'ftt': formTT, 'profes': profes, 'id': id})

def new_doctor(request):
    form = AddDocProf()

    if request.method == 'POST':
        form = AddDocProf(request.POST)
        if form.is_valid():
            newd = Doctors(contact_id=Contact.objects.get(user=request.user.id), profession=form.cleaned_data.get('prof'))
            newd.save()
            return redirect('timetable')

    return render(request, 'homepage/new_doc.html', {'f': form})

def change_diganosis(request, id):
    form = DiagForm()

    if request.method == 'POST':
        form = DiagForm(request.POST)
        if form.is_valid():

            newd = Timetable.objects.get(id=id)
            newd.diagnosis = form.cleaned_data.get('diag')
            newd.save()
            return redirect('timetable')

    return render(request, 'homepage/new_diag.html', {'f': form, 'id': id})