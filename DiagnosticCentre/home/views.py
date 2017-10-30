# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render
from DiagnosticCentre import connection
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import datetime
import cloudant
import json
from django.contrib import messages

# Create your views here.

def home(request):
	# vcap_config = os.environ.get('VCAP_SERVICES')
	# decoded_config = json.loads(vcap_config)
	# for key in decoded_config.keys():
	# if key.startswith('cloudant'):
	# cloudant_creds = decoded_config[key][0]['credentials']
	# cloudant_user = str(cloudant_creds['username'])
	# cloudant_pass = str(cloudant_creds['password'])
	# cloudant_url = str(cloudant_creds['url'])
	# cloudant_user = "f95c6130-1964-448c-a8d7-257d80b30e65-bluemix"
	# cloudant_pass = "9aabf072adfc481b889e322f7824c79b4c517eb187a447bf7fba90120b278c1d"
	# cloudant_url = "https://f95c6130-1964-448c-a8d7-257d80b30e65-bluemix:9aabf072adfc481b889e322f7824c79b4c517eb187a447bf7fba90120b278c1d@f95c6130-1964-448c-a8d7-257d80b30e65-bluemix.cloudant.com"
	# print(cloudant_creds)
	# client = Cloudant(cloudant_user, cloudant_pass, url=cloudant_url, connect=True, auto_renew=True)
	# my_database = client['users']
	context = {}
	if 'user_id' in request.session:
		client = connection.create()

		my_database = None
		if 'user_type' in request.session:
			if request.session['user_type'] == 'O':
				my_database = client['lab']
			else:
				my_database = client['users']

		for doc in my_database:
			pass

		user_id = request.session['user_id']

		if user_id in my_database:
			context = {'name': request.session['user_id']}

	return render(request, "home/home.html", context)

def profile(request):

	context = {"name": '', "is_lab": False}

	if 'user_id' in request.session:
		client = connection.create()

		my_database = None
		if 'user_type' in request.session:
			if request.session['user_type'] == 'O':
				my_database = client['organization']
				context['is_lab'] = True
			else:
				my_database = client['users']

		for doc in my_database:
			pass

		user_id = request.session['user_id']

		if user_id in my_database:
			user = my_database[user_id]
			if request.session['user_type'] == 'O':
				context['test'] = user
			else:
				context['user'] = user
				orgs = client['lab']

				for doc in orgs:
					pass

				if 	user['lab'] in orgs:
					lab = labs[user['lab']]
					context['user_test'] = org['name']

			context['user_email'] = user['_id']

			if 'addcode' in request.session:
				add = request.session['addcode']

				if add == 0:
					context['alert'] = 'danger'
					context['alertmessage'] = 'Something Went Wrong! PLease try again!'
				elif add == 1:
					context['alert'] = 'success'
					context['alertmessage'] = 'Added Successfully'
				elif add == 2:
					context['alert'] = 'danger'
					context['alertmessage'] = 'User Does not Exist'
				elif add == 3:
					context['alert'] = 'danger'
					context['alertmessage'] = 'lorem ipsum'

				del request.session['addcode']

			return render(request, "home/profile.html", context)
		else:
			del request.session['user_id']
			del request.session['user_type']
			request.session['authcode'] = 0
			return HttpResponseRedirect("/login?redirect=/profile")

	return HttpResponseRedirect("/login?redirect=/profile")

def test(request, testname):
	if "user_id" in request.session:
		if request.method == "POST":
			date = request.POST.get('date')
			time = request.POST.get('timeslot')
			print date, time
			client = connection.create()
			my_database = client['appointments']
			doc = {'email': request.session['user_id'], "type": testname, "date": date, "time": time}
			new_doc = my_database.create_document(doc)
			# if new_doc.exists():
			# 	print "abcd"

			return HttpResponseRedirect('/appointments')
		else:
			base = datetime.datetime.today()
			date_list = [(base - datetime.timedelta(days=x)).date for x in range(0, 5)]
			date_list = date_list[::-1]
			time_slots = ["9PM", "10PM", "11PM", "12PM", "2PM", "3PM", "4PM", "5PM", "6PM"]
			context = {
				'dates': date_list,
				'times': time_slots,
				'title': testname,
			}
			return render(request, "home/blood.html", context)
	else:
		return HttpResponseRedirect('/')

def appointments(request):
	if "user_id" in request.session:
		client = connection.create()
		my_database = client['appointments']
		res = cloudant.query.Query(my_database, selector={"email":request.session['user_id']},fields=['_id', 'type', 'date', 'time'])
		# print res
		appoints = res(limit=20, skip=0)["docs"]
		# print "abceeeeeeeeeeeeeeeee "+appoints[0]["_id"]
		context = {
			'appointments': appoints,
		}
		return render(request, 'home/appointments.html', context)
	else:
		return HttpResponseRedirect('/')

def checkAvailability(request):
	testname = request.GET.get('testname')
	date = request.GET.get('date')
	time = request.GET.get('time')
	client = connection.create()
	my_database = client['appointments']
	res = cloudant.query.Query(my_database, selector={"type":testname, "date" : date, "time": time} ,fields=['type', 'date', 'time'])
	count = res(limit=100, skip=0)["docs"]
	if len(count) >= 10:
		message = "Not Available"
	else:
		message = "Available"

	context = {
		'message' : message,
	}
	return HttpResponse(json.dumps(context),content_type="application/json")

def cancel(request):
	if "user_id" in request.session and request.method=="POST":
		ids = request.POST.get('id')
		print ids
		client = connection.create()
		my_database = client['appointments']
		count = my_database[ids]
		count.delete()
		messages.info(request, 'Appointment Cancelled!')
		return HttpResponseRedirect('/appointments')
	else:
		return HttpResponseRedirect('/')
