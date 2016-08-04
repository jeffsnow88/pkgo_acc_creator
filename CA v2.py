import requests
import urllib
import io
from tempmail import TempMail #pip install temp-mail
from bs4 import BeautifulSoup
import time




#for key in client.cookies.keys():
#    print('%s: %s' % (key, client.cookies[key]))

#C:\Python27\python.exe "$(FULL_CURRENT_PATH)"


def CreateAcc():
	my_pw = "lglglg"
	#1st Step - DOB/Country
	signup_url = "https://club.pokemon.com/us/pokemon-trainer-club/sign-up/"
	client = requests.Session()
	client.get(signup_url)
	csrftoken = client.cookies['csrftoken'] #pegar o token para passar no post

	#Payload e Post
	sign_up_parameters = {'csrfmiddlewaretoken' : csrftoken,'dob' : "1990-01-01",'country' : "US"	}							
	headers = {'Referer' : signup_url}
	signup_response = client.post(signup_url, data=sign_up_parameters, headers=headers,cookies=client.cookies) #preenche DOB + country
	print 'Filling > Date of Birthday: ' +  sign_up_parameters["dob"] + ' ,Country: ' +  sign_up_parameters["country"]
	

	#2nd Step - validando username
	verify_user_url = "https://club.pokemon.com/api/signup/verify-username"
	client.get(verify_user_url)
	name = raw_input("Username: ")
	
	#Payload e Post
	verify_param = {'name':name}
	headers = {'Referer' : verify_user_url}
	verify_response = client.post(verify_user_url, data=verify_param, headers=headers,cookies=client.cookies) #valida o username
	
	verify_json =  verify_response.json()
	if verify_json['inuse']: #se o username ja estiver em uso encerra
		print name + ': NOT AVAILABLE, BYE!'
		return False
	else:
		print name + ": is available"



	#3rd Step - registrando a conta
	final_signup_url = "https://club.pokemon.com/us/pokemon-trainer-club/parents/sign-up"
	client.get(final_signup_url)
	myemail = name + '@extremail.ru' #https://api.temp-mail.ru/request/domains/
	myemail = "jeffersonferreiraneves+" + name + "@gmail.com"

	
	final_sign_up_parameters = {'csrfmiddlewaretoken':csrftoken, 'username':name, 'password':my_pw, 'confirm_password':'lglglglg', 'email':myemail, 'confirm_email':myemail,
								'public_profile_opt_in':'False','screen_name':'','terms':'on'}		
	headers = {'Referer' : final_signup_url}
	verify_response =client.post(final_signup_url, data=final_sign_up_parameters, headers=headers,cookies=client.cookies) #valida o username	
	print verify_response.url
	print 'Account created: ' + name

	
	exit()
	#3rd Step - Get Activation Link
	print 'Looking for activation e-mail...'
	tm = TempMail(login=name, domain='@extremail.ru')
	temp_mail_box =  tm.get_mailbox() #pegando a cx de email
	while temp_mail_box["error"] == "There are no emails yet":
		print "Still waiting for validation e-mail, sleeping for 3sec"
		time.sleep(3)
		tm = TempMail(login=myemail, domain='@extremail.ru')
		temp_mail_box =  tm.get_mailbox() #pegando a cx de email
	else:
		lastemail = -1
		for emails in temp_mail_box: #vamos buscar o ultimo email do dest especifico
			if "noreply@pokemon.com" in emails["mail_from"]:
				lastemail += 1
				
		html_content =  temp_mail_box[lastemail]["mail_html"] #pegar o html(em unicode)
		soup = BeautifulSoup(html_content, 'html.parser') #unicode -> html
		print 'vou pegar o link'
		for link in soup.find_all('a'): #buscar todos links e ver se contem activated
			activation_link = str(link.get('href'))
			if "activated" in activation_link:
				email_arrived = True
			print "Activation link found: " + activation_link

				
			
	#4th Step - Activate Account
	activate_status = False
	while not activate_status:
		opener = urllib.FancyURLopener({})
		f = opener.open(activation_link).read()
		if ("already" in f) or ("thanks" in f):
			activate_status = True
			print "Account is now validated!"
			with open("Accounts.txt", "a") as myfile:
				myfile.write(name + ":" + my_pw + "\n")
				return True
		else:
			print 'Trying to validate account....'
			
		

CreateAcc()