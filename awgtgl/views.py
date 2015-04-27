from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.db import transaction
from django.utils import timezone as tz

from django.http import HttpResponse
from datetime import datetime

from awgtgl.models import *
from awgtgl.forms import *

# Create your views here.
@login_required
def home(request):
	return render(request, 'awgtgl/index.html', {})

@login_required
def pathfinder(request):
	return render(request, 'awgtgl/pathfinder.html', {})

@login_required
def journals_hub(request):
	context = {}
	journals = Journal.objects.filter(user=request.user)
	journal_imgs = []
	for journal in journals:
		journal_imgs.append((journal.mapurl, journal))
	context['journals'] = journal_imgs
	return render(request, 'awgtgl/journals_hub.html', context)

@login_required
def make_journal(request):
  new_journal = Journal(user=request.user,
                        mapurl=request.POST['mapurl'])
  new_journal.save()
  return redirect(reverse('journals'))

@login_required
def view_journal(request, id):
	pass

@transaction.atomic
def register(request):
	context = {}

	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'awgtgl/register.html', context)

	form = RegistrationForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'awgtgl/register.html', context)

	new_user = User.objects.create_user(first_name=form.cleaned_data['first_name'],
    									last_name=form.cleaned_data['last_name'],
    									email=form.cleaned_data['email'],
    									username=form.cleaned_data['username'],
    									password=form.cleaned_data['password1'])
	new_user.is_active = False
	new_user.save()

	token = default_token_generator.make_token(new_user)

	email_body = '''
Hi!

To take the first part of your journey into the familiar unknown, click the link below.
http://%s%s

Thanks,

Staff - A Web Guide to Getting Lost
''' % (request.get_host(),
	   reverse('confirm', args=(new_user.username, token)))

	send_mail(subject='Welcome to AWGtGL!',
			      message=email_body,
			      from_email='malexandert@cmu.edu',
			      recipient_list=[new_user.email])

	context['email'] = form.cleaned_data['email']
	return render(request, 'awgtgl/needs-confirmation.html', context)

@transaction.atomic
def confirm_registration(request, username, token):
	user = get_object_or_404(User, username=username)

	if not default_token_generator.check_token(user, token):
		raise Http404

	user.is_active = True
	user.save()

	return render(request, 'awgtgl/confirmed.html', {})
