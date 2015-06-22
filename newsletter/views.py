from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

from .forms import ContactForm, SignUpForm
from .models import SignUp
# Create your views here.
def home(request):
	title = 'Sign Up Now'

	form = SignUpForm(request.POST or None)

	context = {
		"title": title,
		"form": form,
	}
	

	if form.is_valid():
		instance = form.save(commit=False)

		full_name = form.cleaned_data.get("full_name")
		if not full_name:
			full_name = "New"
		instance.full_name = full_name
		# if not instance.full_name:
		# 	instance.full_name = 'Justin'
		instance.save()
		context = {
			"title": 'Thank You'
		}

	if request.user.is_authenticated() and request.user.is_staff:
		#print SignUp.objects.all()
		# for instance in SignUp.objects.all():
		# 	print instance.full_name

		queryset = SignUp.objects.all().order_by('-timestamp')#.filter(full_name__icontains="Justin")
		context = {
			"queryset": queryset
		}
	
	return render(request, 'home.html',context)


def contact(request):
	title='Contact Us'
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key, value in form.cleaned_data.iteritems():
		# 	print key, form.cleaned_data.get(key)
		form_email = form.cleaned_data.get('email')
		form_message = form.cleaned_data.get('message')
		form_full_name = form.cleaned_data.get('full_name')
		#print email, message, full_name
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'yourotheremail@gmail.com']
		contact_message = """
		%s: %s via %s
		"""%(form_full_name, form_message, form_email)
		
		send_mail(subject, 
			contact_message, 
			from_email, 
			[to_email], 
			fail_silently=False)
	context = {
		"form":form,
		"title":title

	}
	return render(request, "forms.html", context)