import requests

url = 'http://localhost:5000/tickets/add_ticket'
data = {
    'utente_apertura': 'user1',
    'utente_segnalato': 'user2',
    'id_task': 'task1',
    'note': 'Just a note about the task',
    'tag': 'tag1',
    'data_apertura': '05-06-2024 12:00:00',
    'data_chiusura': '06-06-2024 12:00:00'
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print('Ticket added successfully')
else:
    print('Failed to add ticket')
