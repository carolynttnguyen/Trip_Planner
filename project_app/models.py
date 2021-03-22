from django.db import models
import re
from datetime import datetime, date, time

# Create your models here.


class UserManager(models.Manager):
    def IndexValidator(self, RegData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # First name - require at least two characters
        if len(RegData['first_name']) < 2:
            errors['first_name'] = 'First Name Must be at least 2 Characters!'
        # Last name - must be at least 2 characters
        if len(RegData['last_name']) < 2:
            errors['last_name'] = 'Last nam Must be at least 2 Characters!'
        # Email- must be in the right format
        if not EMAIL_REGEX.match(RegData['email']):
            errors['email'] = 'Your Email format is invalid!'
        # Password - should be at least 8 Character
        if len(RegData['password']) < 8:
            errors['password'] = 'Password Must contain at least 8 Characters!'
        # Confirm PW needs to match pw
        if RegData['password'] != RegData['confirm_password']:
            errors['confirm_password'] = 'Your password inputs do not match!'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # other_travelers_joining = other users that are joining the trip

    def __repr__(self):
        return f'Show ID: {self.id} | FN {self.first_name} | LN: {self.last_name} | Email: {self.email} | PW: {self.password} | Trips: {self.user_trips} | Joins: {self.other_travelers_joining} '


class TripManager(models.Manager):
    def tripValidator(self, TripData):
        errors = {}
        # no empty entries
        if len(TripData['destination']) < 0:
            errors['destination'] = 'Destination Input cannot be empty!'
        
        if len(TripData['description']) < 0:
            errors['description'] = 'Description cannot be blank!'
        
        if not (TripData['travel_date_from']):
            errors['travel_date_from']= 'Please insert a Travel Start Date!'

        if not (TripData['travel_date_to']):
            errors['travel_date_to']= 'Please insert a Trave Date To!'

        # travel dates should be in future, VALIDATIONS ARE NOT WORKING
        if TripData['travel_date_from'] and TripData['travel_date_to']:
            if TripData["travel_date_from"] > TripData['travel_date_to']:
                errors['invalid_date']='Your Travel Start Date must be before you Travel End Date!'
            if datetime.now() >= datetime.strptime(TripData['travel_date_from'], '%Y-%m-%d'):
                errors['invalid_date2']= 'Your Travel Start Date must be after the current date!'
        return errors

class Trip(models.Model):
    planned_by = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    description = models.TextField()
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    other_travelers = models.ManyToManyField(
        User, related_name='other_travelers_joining')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = TripManager()
