#!/usr/bin/env python 

import os
import names
import random
import requests
import time

ID = '1FAIpQLSd6wfSOMJsuQzrEuH8Lz1OQ49djJU6Ua6Qt-LXkJ0_RZEeobw'
ENTRIES = ['1461594992', '1602674151', '146215934']
URL = 'https://docs.google.com/forms/d/e/{}'.format(ID)
NUM_FILL_OUT = 100000

USER_AGENT = {	'Referer':'{}/viewform'.format(URL),
				'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
			 }
EMAIL_FORMATS = ['{}_{}{}'  , '{}{}{}', '{}.{}_{}', '{}', '{}{}']
CAPITALIZATION = [lambda s: s.upper(), lambda s: s.lower(), lambda s: s]
EMAIL_HOSTS = ['yahoo.com', 'outlook.com', 'gmail.com', 'aol.com']

def get_random_words():
	word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	response = requests.get(word_site)
	return response.content.splitlines()

def get_name_cap(name):
	if random.randint(1,1000) < 200:
		return random.choice(CAPITALIZATION)(name)
	else:
		return name

def partial(string):
	if not isinstance(string, str):
		string = str(string)
	return string[:random.randint(1,len(string))]

def main():
	form_data = {'draftResponse':[],
            	 'pageHistory':0}
	
	questions = list()
	cur_dir = os.path.dirname(os.path.abspath(__file__))
	with open(os.path.join(cur_dir, 'random_questions.txt'), 'r') as infile:
		questions = infile.read().splitlines()

	for i in range(NUM_FILL_OUT):
		email_format = random.choice(EMAIL_FORMATS)
		firstname = names.get_first_name()
		lastname = names.get_last_name()
		number = random.randint(1,10000)
		
		num_args = email_format.count('{')
		email_first = firstname.lower()
		email_last = lastname.lower()
		if num_args == 1:
			email_text = email_format.format(partial(email_first))
		elif num_args == 2:
			if bool(random.getrandbits(1)):
				email_text = email_format.format(partial(email_first), partial(number))
			else:
				email_text = email_format.format(email_first, partial(email_last))
		elif num_args == 3:
			email_text = email_format.format(email_first, email_last, number)
		email_host = random.choice(EMAIL_HOSTS)
		email = email_text + '@' + email_host

		if random.randint(1,5) < 3:
			random_question = random.choice(questions).lower()
		else:
			random_question = random.choice(questions)

		form_name = get_name_cap(firstname + ' ' + lastname)
		form_data['entry.{}'.format(ENTRIES[0])] = random_question
		form_data['entry.{}'.format(ENTRIES[1])] = email
		form_data['entry.{}'.format(ENTRIES[2])] = form_name
		print(random_question)
		print(email)
		print(form_name)
		print('')
		print('')
		
		response = requests.post(URL + '/formResponse', data=form_data, headers=USER_AGENT)
		print(response.content)
		time.sleep(random.choice(range(1, 200)))
		

if __name__ == "__main__":
	main()