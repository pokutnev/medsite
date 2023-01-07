from django.db import models
from django.contrib.auth.models import User

class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey("Contact", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    sfc = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sfc

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

class Doctors(models.Model):
    id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey("Contact", on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'

class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey("Customers", on_delete=models.CASCADE)
    doctor = models.ForeignKey("Doctors", on_delete=models.CASCADE)
    meetdate = models.DateTimeField()
    diagnosis = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Расписание'