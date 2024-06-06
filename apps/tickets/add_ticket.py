import requests

url = 'http://localhost:5000/tickets/add_ticket'
data = {
    'utente_apertura': 'user1',
    'utente_segnalato': 'user2',
    'id_task': 'task123',
    'note': 'Some notes about the task',
    'tag': 'tag1',
    'data_apertura': '2024-06-05 12:00:00',
    'data_chiusura': '2024-06-06 12:00:00'
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print('Ticket added successfully from code')
else:
    print('Failed to add ticket from code')
