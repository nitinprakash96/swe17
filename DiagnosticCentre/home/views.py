# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render
from DiagnosticCentre import connection
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

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
			return HttpResponseRedirect("/profile")

	return render(request, "home/home.html", {})

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
