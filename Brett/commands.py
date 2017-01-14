import json

def read_json():
	dic = {}
	with open('companies.json', 'r') as fp:
		dic = json.load(fp)
	return dic

def write_json(dic):
	with open('companies.json', 'w') as fp:
		json.dump(dic, fp, sort_keys=True)

def get_input(prompt):
	so_raw_dude = raw_input(str(prompt) + ' ').strip().lower()	
	return so_raw_dude

def is_valid_status(status):
	return status in ['available', 'unavailable', 'closed']

def add():
	company = raw_input('Enter company name: ').strip()
	company_key = company.lower()
	companies = read_json()
	
	if company_key in companies:
		print('{} is already in the database you moron. Exiting.'.format(company))
		return

	link = get_input('Enter application link:')
	status = get_input("Enter the status of {}: ['available', 'unavailable', or 'closed']".format(company))
	confirm = get_input('Confirm adding {} at {} with status of {}? [y/n]'.format(company, link, status))	
	
	if not is_valid_status(status):
		print('invalid status. stop trying to break our site')
		return

	if(confirm == 'y'):
		print('Writing {} to database'.format(company))
		companies[company_key] = {'name' : company, 'link' : link, 'status' : status}
		write_json(companies)
	else:
		print('Quitting adding {}'.format(company))
		

def update():
	company = raw_input('Enter company name: ').strip()
	print("")
	company_key = company.lower()
	companies = read_json()

	if company_key not in companies:
		print('{} is not in the database. Exiting.'.format(company))
		return
	
	curr_company = companies[company_key]

	print('Current info for {}'.format(company))
	print('Display Name: {}'.format(curr_company['name']))
	print('Link: {}'.format(curr_company['link']))
	print('Satus: {}\n'.format(curr_company['status']))
	command = get_input("Do you want to update 'name', 'link', or 'status'? ")

	confirm = ""
	if(command == 'link'):
		link = get_input('Enter new link: ')
		confirm = get_input('Confirm replacing {} with {} ? [y/n] '.format(curr_company['link'], link))
		curr_company['link'] = link

	elif(command == 'status'):
		status = get_input('Enter new status: ')

		if not is_valid_status(status):
			print('invalid status. stop trying to break our site')
			return

		confirm = get_input('Confirm changing status of {} from {} to {}? [y/n] '.format(company, curr_company['status'], status))
		curr_company['status'] = status

	elif(command == 'name'):
		name = raw_input('Enter new display name: ').strip()
		confirm = get_input('Confirm changing display name from {} to {}? [y/n]'.format(curr_company['name'], name))
		curr_company['name'] = name

	else:
		print('{} is not a valid input. Read the fucking prompt...'.format(command))
		return

	if(confirm == 'y' or confirm == 'yes'):
		companies[company_key] = curr_company
		write_json(companies)
	else:
		print('Stopping update on {}'.format(company))

def check():
	company = raw_input('Enter company name: ').strip()
	company_key = company.lower()
	companies = read_json()

	if company_key not in companies:
		print('{} is not in the database. Exiting.'.format(company))
		return

	curr_company = companies[company_key]

	print('\nCurrent info for {}'.format(company))
	print('Display Name: {}'.format(curr_company['name']))
	print('Link: {}'.format(curr_company['link']))
	print('Satus: {}'.format(curr_company['status']))

	

while(True):
	command = get_input('Add, Update, or Check:')	
	if(command == 'add'):
		add()
		print('-----------\n')
	elif(command == 'update'):
		update()
		print('-----------\n')
	elif(command == 'check'):
		check()
		print('-----------\n')

	
