from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib import auth
from .models import Profile,Campaign,Client
from django.http import JsonResponse
import random
import re
import string


def home(request):
    return render(request,'home.html')

def aboutus(request):
    return render(request,'aboutus.html')

def healthinsurance(request):
    return render(request,'healthinsurance.html')

def vehicle_health_insurance(request):
    return render(request,'vehicle_health_insurance.html')

def loginpage(request):
    return render(request,'loginpage.html')

@login_required(login_url='loginpage')
def userhome(request):
    return render(request,'userhome.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('adminhome')
            else:
                return redirect('userhome')
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'loginpage.html')


#Admin-home sections
@login_required(login_url='loginpage')
def adminhome(request):
    return render(request,'adminhome.html')

def generate_random_password(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def validate_username(request):
    username = request.GET.get('username', '')
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'exists': exists})

def validate_email(request):
    email = request.GET.get('email', '')
    exists = User.objects.filter(email__iexact=email).exists()
    return JsonResponse({'exists': exists})

def validate_phone(request):
    phone = request.GET.get('phone', '')
    exists = Profile.objects.filter(phone_number=phone).exists()
    return JsonResponse({'exists': exists})

def add_agent(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        photo=request.FILES.get('image')
        password = generate_random_password()

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('add_agent')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email address already exists')

        user = User.objects.create_user(
            first_name=fname,
            last_name=lname,
            username=username,
            email=email,
            password=password
        )

        # ✅ Create profile manually
        Profile.objects.create(user=user, phone_number=phone,photo=photo)

        send_mail(
            subject='Agent login details',
            message=(
                f'Hello Agent:{username}\n'
                f'Your temporary password:{password}\n'
                f'Please login and reset your password.\n\n'
                f'Regards,\nInsureNow Team'
            ),
            from_email='your_email@gmail.com',
            recipient_list=[email],
            fail_silently=False
        )

        messages.success(request, f"Agent {username} added and email sent.")
        return redirect('add_agent')

    return render(request, 'add_agent.html')

def agent_details(request):
    # if will filter the user table  on the basic so superuser ,is_staff then remaining will be displayed
    agents=User.objects.filter(is_superuser=False,is_staff=False).select_related('profile')  
    return render(request,'agent_details.html',{'agents':agents})

def edit(request,id):
    agents=User.objects.get(id=id)
    return render(request,'edit.html',{'agents':agents})

@login_required
def edit_agent(request, id):
    agent = get_object_or_404(User, id=id)

    if request.method == "POST":
        agent.first_name = request.POST.get('fname')
        agent.last_name = request.POST.get('lname')
        agent.username = request.POST.get('uname')
        agent.email = request.POST.get('email')
        agent.save()

        phone_number = request.POST.get('phonenumber')
        photo = request.FILES.get('photo')  # ✅ Get uploaded photo if available

        if hasattr(agent, 'profile'):
            agent.profile.phone_number = phone_number
            if photo:
                agent.profile.photo = photo  # ✅ Save new photo
            agent.profile.save()
        else:
            Profile.objects.create(user=agent, phone_number=phone_number, photo=photo)

        return redirect('agent_details')  # ✅ Replace this with your agent list URL name

    return render(request, 'edit.html', {'agents': agent})

def delete_agent(request,id):
    agent=User.objects.get(id=id)
    agent.delete()
    return redirect('agent_details')



def add_campaign(request):
    agents = User.objects.filter(is_staff=False)
    return render(request,'add_campaign.html',{'agents': agents})

def add_campaign_details(request):
    if request.method == 'POST':
        campaignname = request.POST['cname']
        place = request.POST['place']
        time = request.POST['time']
        image = request.FILES.get('image')
        agent_id = request.POST.get('agent_id')

        try:
            agent = User.objects.get(id=agent_id)  # replace with Agent.objects.get(...) if using Agent model
        except User.DoesNotExist:
            messages.error(request, '❌ Selected agent does not exist.')
            return redirect('add_campaign')

        campaign = Campaign(
            campaignname=campaignname,
            place=place,
            time=time,
            image=image,
            agent=agent  
        )
        campaign.save()

        messages.success(request, '✅ Campaign details added successfully')
        return redirect('add_campaign')

    return render(request, 'add_campaign.html')

def show_campaign(request):
    camp=Campaign.objects.all()
    return render(request,'show_campaign.html',{'camp':camp})

def edit_campaign(request,id):
    camp=Campaign.objects.get(id=id)
    agents = User.objects.filter(is_staff=False)
    return render(request,'edit_campaign.html',{'camp':camp,'agents':agents})

def edit_campaign_details(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    agents = User.objects.filter(is_staff=False)

    if request.method == 'POST':
        campaign.campaignname = request.POST['camp']
        campaign.place = request.POST['place']
        campaign.time = request.POST['time']

        image = request.FILES.get('image')  
        if image:
            campaign.image = image

        agent_id = request.POST.get('agent_id')
        if agent_id:
            try:
                agent = User.objects.get(id=agent_id)
                campaign.agent = agent
            except User.DoesNotExist:
                pass  # Handle error if needed

        campaign.save()
        return redirect('show_campaign')
    
    return render(request, 'edit_campaign.html', {'camp': campaign, 'agents': agents})


def delete_campaign(request,id):
    camp=get_object_or_404(Campaign,id=id)
    camp.delete()
    return redirect('show_campaign')

def client_application_details(request):
    client=Client.objects.all()
    return render(request,'client_application_details.html',{'cli':client})

def logoutadmin(request):
    auth.logout(request)
    return redirect('loginpage')

# user section

@login_required
def useredit(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        # Update Profile model fields
        profile.phone_number = request.POST.get('phone_number')
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']

        user.save()
        profile.save()
        messages.success(request, "Your profile was updated successfully!")
        return redirect('useredit')

    return render(request, 'useredit.html', {'user': user, 'profile': profile})


@login_required
def reset_password(request):
    if request.method == 'POST':
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if not request.user.check_password(current):
            messages.error(request, "❌ Current password is incorrect.")
        elif new != confirm:
            messages.error(request, "❌ New passwords do not match.")
        else:
            request.user.set_password(new)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in after password change
            messages.success(request, "✅ Password updated successfully!")
            return redirect('loginpage')  # Redirect wherever appropriate

    return render(request, 'reset_password.html')


def client(request, id):
    campaigns = Campaign.objects.filter(agent_id=id)
    agent = User.objects.get(id=id)  # Get the agent assigned to the campaign

    return render(request, 'client.html', {
        'campaigns': campaigns,
        'agent': agent,
    })

@login_required
def user_client(request):
    agent = request.user
    campaigns = Campaign.objects.filter(agent=agent)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        aadhar = request.POST.get('aadhar', '').replace(" ", "")
        pan = request.POST.get('pan')
        income = request.POST.get('income')
        children = request.POST.get('children')
        policy = request.POST.get('other_policy')
        address = request.POST.get('address')
        job = request.POST.get('job')
        education = request.POST.get('education')
        dob = request.POST.get('dob')
        rate = request.POST.get('rate')

        # If agent has multiple campaigns, assign the first one
        campaign = campaigns.first() if campaigns.exists() else None

        Client.objects.create(
            agent=agent,
            campaign=campaign,
            name=name,
            email=email,
            phone_number=phone,
            aadhar=aadhar,
            pan=pan,
            income=income,
            children=children,
            other_policy=policy,
            address=address,
            job=job,
            education=education,
            dob=dob,
            rate=rate
        )

        messages.success(request, "✅ Client added successfully!")
        return redirect('user_client')

    return render(request, 'user_client.html', {'campaigns': campaigns})


def validate_email_client(request):
    email = request.GET.get('email', '')
    exists = Client.objects.filter(email__iexact=email).exists()
    return JsonResponse({'exists': exists})


def validate_phone_client(request):
    phone = request.GET.get('phone', '')
    exists = Client.objects.filter(phone_number=phone).exists()
    return JsonResponse({'exists': exists})

def validate_aadhar(request):
    aadhar = request.GET.get('aadhar', '').replace(" ", "")  # Normalize
    exists = Client.objects.filter(aadhar=aadhar).exists()
    return JsonResponse({'exists': exists})

def validate_pan(request):
    pan = request.GET.get('pan', '')
    exists = Client.objects.filter(pan__iexact=pan).exists()
    return JsonResponse({'exists': exists})

def logoutuser(request):
    auth.logout(request)
    return redirect('loginpage')
        





