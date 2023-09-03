import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-81e4e-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "75038":
        {
            'name': "Eldar Ryzhov",
            'speciality': 'FKTI',
            'starting_year': 2020,
            'year': 4,
            'room': 27,
            'group': '0204'
        },
    "83710":
        {
            'name': "Roman Surjan",
            'speciality': 'FKTI',
            'starting_year': 2020,
            'year': 4,
            'room': 19,
            'group': '0204'
        }
}

for key, value in data.items():
    ref.child(key).set(value)