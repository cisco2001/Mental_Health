from django.shortcuts import render, redirect
from mental_health.models import Student, Appointment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import get_user_model



# Create your views here.
@login_required
def dashboard(request):
	return render(request, "dashboard/dashboard.html")

@login_required
def user_profile(request):
    user = request.user  # This will be an instance of the Student model
    context = {
        'user_profile': user,  # Pass the Student instance to the template
    }
    return render(request, "dashboard/profile.html", context)

@login_required
def update_profile(request):
    try:
        student = request.user
    except Student.DoesNotExist:
        # Handle the case where a student profile doesn't exist for the user
        student = None

    if request.method == "POST":
        # Get data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        course = request.POST.get('course')
        university = request.POST.get('university')
        date_obj = datetime.strptime(birth_date, '%d %B %Y').date()

        if student is None:
            # Create a new student profile if it doesn't exist
            student = Student.objects.create(user=request.user, first_name=first_name, last_name=last_name, birth_date=birth_date, phone_number=phone_number, gender=gender, course=course, university=university)
        else:
            # Update existing student profile
            student.first_name = first_name
            student.last_name = last_name
            student.birth_date = date_obj
            student.phone_number = phone_number
            student.gender = gender
            student.course = course
            student.university = university
            student.save()

        messages.success(request, "Your profile has been updated successfully.")
        return redirect('update_profile')

    return render(request, "dashboard/profile.html", {'user_profile': student})

User = get_user_model()

@login_required
def book_appointment(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff")
        date = request.POST.get("date")
        text = request.POST.get("text")
        
        date_obj = datetime.strptime(date, '%d %B %Y').date()

        if not staff_id or not date:
            messages.error(request, "Please select a staff member and date.")
            return redirect('book_appointment')

        try:
            staff_member = User.objects.get(pk=staff_id, is_staff=True)
        except User.DoesNotExist:
            messages.error(request, "Selected staff member does not exist.")
            return redirect('book_appointment')

        appointment = Appointment(
            student=request.user,
            staff=staff_member,
            date=date_obj,
            text=text,
        )
        appointment.save()
        messages.success(request, "Appointment booked successfully!")
        #return redirect('appointment_status')
    
    staff_members = User.objects.filter(is_staff=True)
    return render(request, 'dashboard/book_appointment.html', {'staff_members': staff_members})

@login_required
def view_appointments(request):
    # Retrieve appointments for the current student
    appointments = Appointment.objects.filter(student=request.user)

    context = {
        'appointments': appointments
    }
    return render(request, 'dashboard/appointment_list.html', context)