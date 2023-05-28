from django.shortcuts import render, redirect

from django.core.mail import BadHeaderError, send_mail

from django.http import HttpResponse,HttpResponseRedirect

from django.contrib import messages

from django.core.mail import EmailMessage

from django.conf import settings

from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout

from django.utils.html import strip_tags

from django.core.mail import EmailMultiAlternatives

import random

from django.contrib.auth.decorators import login_required

from django.contrib.admin.views.decorators import staff_member_required

from .forms import *

# Create your views here.

def home(request):
	return render(request, 'herculesbankapp/index.html')

def current(request):
	return render(request, 'herculesbankapp/current.html')

def kid(request):
	return render(request, 'herculesbankapp/kid.html')

def premium(request):
	return render(request, 'herculesbankapp/premium.html')

def saving(request):
	return render(request, 'herculesbankapp/saving.html')

def corporate(request):
	return render(request, 'herculesbankapp/corporate.html')

def career(request):
	return render(request, 'herculesbankapp/career.html')

def insurance(request):
	return render(request, 'herculesbankapp/insurance.html')

def faq(request):
	return render(request, 'herculesbankapp/faq.html')

def card(request):
	return render(request, 'herculesbankapp/card.html')


def contact(request):
	#if request.method == 'GET':
		#form= ContactForm()
	#else:
		#form = ContactForm(request.POST)
		#if form.is_valid():
			#name= form.cleaned_data['name']
			#email= form.cleaned_data['email']
			#message = form.cleaned_data['message']

			#try:
				#send_mail(name, "Investor {} has sent a message saying: {}".format(email, message),email, ['customercare@standardtrust.co.uk'])
			#except BadHeaderError:
				#return HttpResponse('Invalid header found.')

			#return HttpResponse('Your message has been sent successfully')
	#context={'form': form}
	return HttpResponse('Contact us using support@standardtrust.in')


def about(request):
	return render(request, 'herculesbankapp/about-us.html')


def news(request):
	return render(request, 'herculesbankapp/news.html')

@login_required(login_url='clientsignin')
def dashboard(request):
	if request.user.is_staff:
		return redirect('admindashboard')
	else:
		client= request.user.client
		clientAccountNumber= client.account_number
		clientAccountType= client.account_type
		clientAccountCurrency= client.account_currency
		clientBalance= float(client.deposit) + float(client.uncleared_balance)
	context={'clientAccountNumber':clientAccountNumber, 'clientAccountType':clientAccountType, 'clientBalance':clientBalance, 'clientAccountCurrency':clientAccountCurrency}
	return render(request, 'herculesbankapp/clientdashboard.html', context)

@login_required(login_url='clientsignin')
def account_settings(request):
	client= request.user.client
	form= ClientUserForm(instance=client)
	if request.method=='POST':
		form= ClientUserForm(request.POST, request.FILES, instance=client)
		if form.is_valid():
			form.save()
	context= {'form':form}
	return render(request, 'herculesbankapp/clientaccountsettings.html', context)

@login_required(login_url='clientsignin')
def fundtransfer(request):
	client= request.user.client
	clientAccountNumber= client.account_number
	clientAccountType= client.account_type
	clientAccountCurrency= client.account_currency
	clientBalance= float(client.deposit) + float(client.uncleared_balance)
	if request.method == 'POST':
		destination_account_name= request.POST.get('account_name')
		destination_bank_name= request.POST.get('bank_name')
		destination_bank_code= request.POST.get('bank_code')
		destination_bank_routing_number= request.POST.get('routing_number')
		destination_country= request.POST.get('country')
		destination_account_number= request.POST.get('account_number')
		amount= request.POST.get('amount')
		transfer_pin= request.POST.get('transfer_pin')
		if float(client.deposit) > float(amount):
			client_transfer_pin= client.transfer_pin
			if str(client_transfer_pin) == str(transfer_pin):
				Foreign_transaction.objects.create(
					client= client,
					bank_name= destination_bank_name,
					country= destination_country,
					account_name=destination_account_name,
					bank_code=destination_bank_code,
					routing_number=destination_bank_routing_number,
					account_number= destination_account_number,
					amount= amount,
					)
				return redirect('foreign_transaction')
			else:
				return HttpResponse('Incorrect transfer pin. Try setting a transfer pin in your account settings')
		else:
			return HttpResponse('Your balance is too low to complete this transaction')

	context={'clientAccountNumber':clientAccountNumber, 'clientAccountType':clientAccountType, 'clientBalance':clientBalance, 'clientAccountCurrency':clientAccountCurrency}
	return render(request, 'herculesbankapp/clienttransferpage.html', context)

@login_required(login_url='clientsignin')
def foreign_transaction(request):
	client= request.user.client
	client_deposit= client.deposit
	client_username= client.first_name
	email= client.email
	client_pk= client.id
	client_email= client.email
	otp= list(Otp.objects.all())
	otp_code= random.choice(otp)
	foreign_transaction= Foreign_transaction.objects.filter(client=client)
	foreign_transaction_number= foreign_transaction.count()
	last_foreign_transaction= foreign_transaction.last()
	template= render_to_string('herculesbankapp/otp.html', {'name':client_username, 'otp':otp_code})
	email_message= EmailMessage(
		'Transaction alert on your account!',
		template,
		settings.EMAIL_HOST_USER,
		[client_email],
		)
	email_message.fail_silently= False
	email_message.send()

	if request.method == 'POST':
		otp= request.POST.get('otp')
		try:
			otp_check= Otp.objects.get(otp)
			foreign_transaction= Foreign_transaction.objects.filter(client=client)
			foreign_transaction_number= foreign_transaction.count()
			last_foreign_transaction= foreign_transaction.last()
		except:
		    pass
		if foreign_transaction and float(foreign_transaction_number) < 2:
			amount_sent= last_foreign_transaction.amount
			bank_name= last_foreign_transaction.bank_name
			account_number= last_foreign_transaction.account_number
			client_new_balance= float(client_deposit) - float(amount_sent)
			client_details= Client.objects.filter(id=client_pk)
			client_details.update(deposit=client_new_balance)
			debit_alert_template= render_to_string('herculesbankapp/foreign_debit_alert.html', {'name':client_username, 'amount':amount_sent, 'client_balance':client_new_balance})
			email_message= EmailMessage(
				'Debit alert on your account',
				debit_alert_template,
				settings.EMAIL_HOST_USER,
				[client_email],
				)
			email_message.fail_silently=False
			email_message.send()
			return HttpResponse('Transfer completed successfully')
		else:
			return HttpResponse('We locked your account due to suspicious activity. Please call us on (408) 329-9187')
	context={}
	return render(request, 'herculesbankapp/foreign_transaction.html', context)

def transactionhistory(request):
	client= request.user.client
	clientAccountNumber= client.account_number
	clientAccountType= client.account_type
	clientAccountCurrency= client.account_currency
	clientBalance= float(client.deposit) + float(client.uncleared_balance)
	transactions= Foreign_transaction.objects.filter(client=client)
	context={'clientAccountNumber':clientAccountNumber, 'clientAccountType':clientAccountType, 'clientBalance':clientBalance,
	'clientAccountCurrency':clientAccountCurrency, 'transactions':transactions}
	return render(request, 'herculesbankapp/clienttransactionhistorypage.html', context)

@login_required(login_url='clientsignin')
@staff_member_required
def admindashboard(request):
	clients= Client.objects.all()
	context={'clients':clients}
	return render(request, 'herculesbankapp/admindashboard.html', context)

@login_required(login_url='clientsignin')
@staff_member_required
def admincreateaccount(request):
	form= CreateUserForm()
	if request.method == 'POST':
		form= CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			firstName= form.cleaned_data.get('first_name')
			email= form.cleaned_data.get('email')
			print(firstName)
			template= render_to_string('herculesbankapp/WelcomeEmail2.html', {'name':firstName})
			plain_message= strip_tags(template)
			email_message= EmailMultiAlternatives(
				'Welcome on board to Standard Trust',
				plain_message,
				settings.EMAIL_HOST_USER,
				[email]

				)
			email_message.attach_alternative(template, 'text/html')
			email_message.send()
			return redirect('admindashboard')
	context={'form':form}
	return render(request, 'herculesbankapp/admincreateaccountpage.html', context)

@login_required(login_url='clientsignin')
@staff_member_required
def admingotouserprofile(request, pk):
	client= Client.objects.get(id=pk)
	form= ClientForm(instance=client)
	if request.method=='POST':
		form= ClientForm(request.POST, request.FILES, instance=client)
		if form.is_valid():
			form.save()
	context= {'form':form}
	return render(request, 'herculesbankapp/admingotouserprofilepage.html', context)

@login_required(login_url='clientsignin')
@staff_member_required
def admincreditaccount(request, pk):
	client= Client.objects.get(id=pk)
	client_deposit= client.deposit
	client_id= client.id
	firstName= client.first_name
	if request.method == 'POST':
		amount= request.POST.get('amount')
		if amount:
			newacc_bal= float(client_deposit) + float(amount)
			client_info= Client.objects.filter(id=client_id)
			client_info.update(deposit=newacc_bal)
			template= render_to_string('herculesbankapp/creditalert.html', {'name':firstName, 'newacc_bal':newacc_bal})
			email_message= EmailMessage(
				'Credit on your account!',
				template,
				settings.EMAIL_HOST_USER,
				[email]
				)
			email_message.fail_silently=False
			email_message.send()
			return HttpResponse('Account credited successfully')
		else:
			return HttpResponse('Enter an amount in Euros')
	print(client_deposit)
	context={}
	return render(request, 'herculesbankapp/admincreditaccount.html', context)

@login_required(login_url='clientsignin')
@staff_member_required
def admindebitaccount(request, pk):
	client= Client.objects.get(id=pk)
	client_deposit= client.deposit
	client_id= client.id
	firstName= client.first_name
	if request.method == 'POST':
		amount= request.POST.get('amount')
		if float(client_deposit) > float(amount):
			newacc_bal= float(client_deposit) - float(amount)
			client_info= Client.objects.filter(id=client_id)
			client_info.update(deposit=newacc_bal)
			template= render_to_string('herculesbankapp/debitalert.html', {'name':firstName, 'newacc_bal':newacc_bal})
			email_message= EmailMessage(
				'Debit on your account!',
				template,
				settings.EMAIL_HOST_USER,
				[email]
				)
			email_message.fail_silently=False
			email_message.send()
			return HttpResponse('Account debited successfully')
		else:
			return HttpResponse('Amount is greater than account balance')
	print(client_deposit)
	context={}
	return render(request, 'herculesbankapp/admindebitaccount.html', context)


def clientsignin(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	else:
		if request.method == "POST":
			username= request.POST.get('username')
			password= request.POST.get('passw')

			user= authenticate(request, username=username, password=password)

			if user is not None:
				email= User.objects.get(username=username).email
				print(email)
				template= render_to_string('herculesbankapp/loginAlert.html', {'name':username})
				plain_message= strip_tags(template)
				email_message= EmailMultiAlternatives(
					'Login alert on your account!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[email]

					)
				email_message.attach_alternative(template, 'text/html')
				#email_message.send()
				login(request, user)
				return redirect('dashboard')

			else:
				messages.error(request, "username or password is incorrect")
	return render(request, 'herculesbankapp/clientsignin.html')

def signup(request):
	user_check = request.user.is_authenticated
	if user_check:
		return redirect('dashboard')
	form = CreateUserForm(request.POST or None)
	if form.is_valid():
		form.save()

		username=form.cleaned_data.get('username')
		password= form.cleaned_data.get('password1')
		password_reminder= password[:1]
		password_reminder_two= password[-1:]
		email= form.cleaned_data.get('email')
		template= render_to_string('herculesbankapp/WelcomeEmail2.html', {'name':username,'password':password})
		plain_message= strip_tags(template)
		email_message= EmailMultiAlternatives(
			'Welcome to Standard Trust',
			plain_message,
			settings.EMAIL_HOST_USER,
			[email],

			)
		email_message.attach_alternative(template, 'text/html')
		#email_message.send()

		second_template= render_to_string('herculesbankapp/securityEmail.html', {'name': username, 'password_reminder':password_reminder, 'password_reminder_two':password_reminder_two})
		second_plain_message= strip_tags(second_template)
		second_email_message= EmailMultiAlternatives(
			"Stay updated and discover more with Standard Trust!",
			second_plain_message,
			settings.EMAIL_HOST_USER,
			[email]
			)
		second_email_message.attach_alternative(second_template, 'text/html')
		#second_email_message.send()

		#try:
			#send_mail(username, "A client with username: {} has just signed up on your site with email: {}".format(username, email),settings.EMAIL_HOST_USER, ['customercare@standardtrust.co.uk'])
		#except BadHeaderError:
			#return HttpResponse("Your account has been created but you can't login at this time. please, try to login later")
		user= authenticate(username=username, password=password)
		login(request, user)
		return redirect('dashboard')
	context={'form':form}
	return render(request, 'herculesbankapp/clientregister.html', context)

def logoutuser(request):
	logout(request)
	return redirect('clientsignin')
