from frontend.client_api import ApiClient, AuthError


client = ApiClient('http://127.0.0.1:8000')
try:
	client.login('Marios', 'wrong-password')
except AuthError as error:
	print('Bad login rejected:', error)

client.login('Marios', '1234')
print('Logged in as', client.username)
print(client.add_item('Test item', 'Added from try_client.py'))
print(client.list_items())