import requests

data = {
    'utente_apertura': 'user1',
    'utente_segnalato': 'user2',
    'id_task': 'task1',
    'note': 'Just a note about the task',
    'tag': 'tag1',
    'data_apertura': '01-06-2024 12:00:00',
    'data_chiusura': '06-06-2024 12:00:00'
}, {
    'utente_apertura': 'user3',
    'utente_segnalato': 'user5',
    'id_task': 'task2',
    'note': 'It is a note',
    'tag': 'tag3',
    'data_apertura': '02-06-2024 10:00:00',
    'data_chiusura': '04-06-2024 12:00:00'
}, {
    'utente_apertura': 'user2',
    'utente_segnalato': 'user3',
    'id_task': 'task3',
    'tag': 'tag4',
    'data_apertura': '04-06-2024 12:03:00',
    'data_chiusura': '06-06-2024 09:30:00'
}, {
    'utente_apertura': 'user4',
    'utente_segnalato': 'user1',
    'id_task': 'task4',
    'note': 'Another note...',
    'tag': 'tag5',
    'data_apertura': '05-06-2024 11:11:00',
    'data_chiusura': '06-06-2024 10:45:00'
}

print(data)

response = requests.post( json=data)

if response.status_code == 200:
    print('Ticket added successfully')
else:
    print('Failed to add ticket')