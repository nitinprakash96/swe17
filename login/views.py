# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from DiagnosticCentre import connection, authhelper

"""
authcode

0: Something Else
1: Wrong Username or Password
2: Registered Sucessfull
4: Organization Not Yet Verified
"""

class LoginHandler(View):
	def get(self,request):
		if "user_type" in request.session:
			return HttpResponseRedirect("/")
		context = {}
		if 'redirect' in request.GET:
			context["redirect"] = request.GET['redirect']
		else:
			context["redirect"] = '/'

		if 'authcode' in request.session:
			if request.session["authcode"] == 0:
				context['alert'] = 'danger'
				context["alertmessage"] = "Something went Wrong! PLease try again!"

			elif request.session["authcode"] == 1:
				context['alert'] = 'danger'
				context["alertmessage"] = "Wrong Username or Password"

			elif request.session["authcode"] == 2:
				context['alert'] = 'success'
				context["alertmessage"] = "Registration was successful! Log In to Continue"

			elif request.session["authcode"] == 4:
				context['alert'] = 'warning'
				context["alertmessage"] = "Lorem ipsum"

			del request.session['authcode']
		else:
			context["alert"] = False

		return render(request, "login/login.html", context)

	def post(self,request):
		# print request.POST.get('type')
		if request.POST.get('type') == 'customer':
			redirect = '/'
			if 'redirect' in request.POST:
				redirect = request.POST['redirect']

			if 'email' in request.POST and 'pwd' in request.POST:

				pwd = authhelper.crypt(request.POST['pwd'])
				email = request.POST['email']
				client = connection.create()
				my_database = client['users']
				for i in my_database:
					pass
				if email in my_database:
					doc = my_database[email]
					if doc['password'] == pwd:
						request.session['user_id'] = doc['_id']
						request.session['user_type'] = 'U'
						return HttpResponseRedirect(redirect)

				request.session['authcode'] = 1
				return HttpResponseRedirect("/login?redirect="+redirect)

			request.session['authcode'] = 0
			return HttpResponseRedirect("/login?redirect="+redirect)
		else:
			redirect = '/staffview'

			# if 'redirect' in request.POST:
			# 	redirect = request.POST['redirect']

			if 'email' in request.POST and 'pwd' in request.POST:
				pwd = authhelper.crypt(request.POST['pwd'])
				email = request.POST['email']
				client = connection.create()
				my_database = client['staff']

				for i in my_database:
					pass

				if email in my_database:
					doc = my_database[email]

					if doc['password'] == pwd:
						request.session['user_id'] = doc['_id']
						request.session['user_type'] = 'S'
						request.session['staff_type'] = doc['type']
						if doc['type'] == 'SS':
							redirect = '/staffview'
						else:
							redirect = '/schedule'
						return HttpResponseRedirect(redirect)

				request.session['authcode'] = 1
				return HttpResponseRedirect("/login?redirect="+redirect)

			request.session['authcode'] = 0
			return HttpResponseRedirect("/login?redirect="+redirect)


class LogoutHandler(View):
	def get(self,request):
		redirect = '/'
		if 'redirect' in request.GET:
			redirect = request.GET['redirect']

		if 'user_type' in request.session:
			del request.session['user_type']
		if 'user_id' in request.session:
			del request.session['user_id']
		if 'admin_id' in request.session:
			del request.session['admin_id']
		if 'staff_type' in request.session:
			del request.session['staff_type']

		return HttpResponseRedirect(redirect)

class RegisterUser(View):
	def get(self,request):
		return render(request, "register/register.html", {})

	def post(self, request):
		data = request.POST

		if 'name' in data and 'email' in data and 'pwd' in data:
			name = data['name']
			_id = data['email']
			pwd = authhelper.crypt(data['pwd'])
			client = connection.create()
			my_database = client['users']
			doc = {"_id": _id, "name": name, "password": pwd}
			new_doc = my_database.create_document(doc)
			if new_doc.exists():
				request.session['authcode'] = 2
				return HttpResponseRedirect("/login?redirect=/")
			else:
				request.session['authcode'] = 3
				return HttpResponseRedirect("/register/user")

		else:
			request.session['authcode'] = 0
			return HttpResponseRedirect("/register/user")
