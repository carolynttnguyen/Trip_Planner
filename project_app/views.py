from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.IndexValidator(request.POST)
        # validate input
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')

        # check is user email already exist
        existing_user_list = User.objects.filter(email=request.POST['email'])
        if len(existing_user_list) > 0 :
            messages.error(request, 'Email already exist.')
            return redirect('/')

        # create user
        user_pw = request.POST['password']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw,
        )
        print(new_user)
        # set session data
        request.session['user_id']= new_user.id
        request.session['user_name'] = f"{new_user.first_name} {new_user.last_name}"
        return redirect('/dashboard')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        logged_user = User.objects.filter(email=request.POST['email'])
    # check if email is in db
        if logged_user:
            # if user is logged set user, and checkpw
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f"{logged_user.first_name} {logged_user.last_name}"
            return redirect('/dashboard')
    return redirect('/')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    logged_user = User.objects.get(id=request.session['user_id'])
    #variable to grab trips that user(id) has also joined 
    context = {
        'logged_user': logged_user,
        'other_plans': logged_user.other_travelers_joining.all().order_by("travel_date_from"),
        'trips': Trip.objects.filter(planned_by=logged_user).order_by("travel_date_from"),
        'other_users': User.objects.all().exclude(id=logged_user.id),
        'planned_trips': Trip.objects.exclude(other_travelers= logged_user).order_by("travel_date_from"),
    }
    return render(request, 'dashboard.html', context)



def add(request):
    return render(request, 'add_trip.html')

def create(request):
    if request.method =='POST':
        trip_errors = Trip.objects.tripValidator(request.POST)
        # validate user input
        if trip_errors:
            for error in trip_errors:
                messages.error(request, trip_errors[error])
            return redirect('/addtrip')
        # create trip 
        new_trip = Trip.objects.create(
            planned_by = User.objects.get(id= request.session['user_id']),
            destination = request.POST['destination'],
            description = request.POST['description'],
            travel_date_from = request.POST['travel_date_from'],
            travel_date_to = request.POST['travel_date_to'],
        )
        new_trip.save()
        return redirect('/dashboard')
    return redirect('/addtrip')


def view_trip(request, tripId):
    if request.method == 'GET':
        trip_id = tripId
        logged_user =User.objects.get(id=request.session['user_id'])
        context = {
            "trip" : Trip.objects.get(id=trip_id),
            'joined_travelers': User.objects.filter(other_travelers_joining=trip_id)
        }
        return render(request, 'view_trip.html', context)
    return redirect('/dashboard')

def cancel(request, planID):
    # removes from your trips, and back to other User's Travel Plans
    this_traveler = User.objects.get(id=request.session['user_id'])
    this_trip= Trip.objects.get(id=planID)
    this_trip.other_travelers.remove(this_traveler)
    return redirect('/dashboard')

def delete(request,id):
    # appears if logged in user posted the trips
    # removes trip from database
    delete_trip = Trip.objects.get(id=id)
    delete_trip.delete()
    return redirect('/dashboard')

def join_trip(request, user_id, tripID):
    this_trip = Trip.objects.get(id=tripID)
    this_trip.other_travelers.add(user_id)
    this_trip.save()
    return redirect('/dashboard')

def logout(request):
    # del request.session[]
    request.session.clear()
    return redirect('/')