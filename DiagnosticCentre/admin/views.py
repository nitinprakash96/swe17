# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from DiagnosticCentre import connection, authhelper
import cloudant

# Create your views here.

class AdminLogin(View):
	def get(self, request):
		if "user_type" in request.session:
			return HttpResponseRedirect("/")
		context = {}
		if 'authcode' in request.session:
			if request.session["authcode"] == 0:
				context['alert'] = 'danger'
				context["alertmessage"] = "Something looks Wrong"

			elif request.session["authcode"] == 1:
				context['alert'] = 'danger'
				context["alertmessage"] = "Wrong Username or Password"

			elif request.session["authcode"] == 2:
				context['alert'] = 'success'
				context["alertmessage"] = "Registration was successful! Log In to Continue"

			del request.session['authcode']
		else:
			context["alert"] = False
		return render(request, "admin/login.html", context)

	def post(self, request):
		client = connection.create()
		my_database = client['admin']

		if 'email' in request.POST and 'pwd' in request.POST:
			email = request.POST['email']
			pwd = request.POST['pwd']
			for i in my_database:
				pass
			if email in my_database:
				doc = my_database[email]
				if doc['password'] == pwd:
					request.session['admin_id'] = doc['_id']
					request.session['user_id'] = "Admin"
					request.session['user_type'] = "A"
					return HttpResponseRedirect("/managestaff")

			request.session["authcode"] = 1
			return HttpResponseRedirect("/admin")

		else:
			request.session["authcode"] = 0
			return HttpResponseRedirect("/admin")

class managestaff(View):
	def get(self, request):
		if ("user_type" in request.session and request.session['user_type'] != "A") or "user_type" not in request.session:
			return HttpResponseRedirect("/")

		client = connection.create()
		my_database = client['staff']
		# stafftemp = cloudant.query.Query(my_database, selector={},fields=['_id', 'name'])
		staff = cloudant.result.Result(my_database.all_docs, include_docs=True)
		context = {
			'staff':staff,
		}
		return render(request, "admin/managestaff.html", context)

	def post(self, request):
		client = connection.create()
		my_database = client['admin']

		if 'email' in request.POST and 'pwd' in request.POST:
			email = request.POST['email']
			pwd = request.POST['pwd']
			for i in my_database:
				pass
			if email in my_database:
				doc = my_database[email]
				if doc['password'] == pwd:
					request.session['admin_id'] = doc['_id']
					request.session['user_id'] = "Admin"
					request.session['user_type'] = "A"
					return HttpResponseRedirect("/managestaff")

			request.session["authcode"] = 1
			return HttpResponseRedirect("/admin")

		else:
			request.session["authcode"] = 0
			return HttpResponseRedirect("/admin")