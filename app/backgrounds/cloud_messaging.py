from app import firebase
from fastapi.encoders import jsonable_encoder

from app.logger import AppLog


def push_new_system_notification(data: dict):
    #  Get Token of all user and staff from the client FCM SDKs.
    tokens = ["flpAeZe9QKO6Smt-pn4Gsh:APA91bHJqpqaF7bIVwuENc64z-6JFQTk_bhCrGT0XhZjG9h53hm40grGlTKbQmbbiYKqN6mfzIFLh9nQpNlBGYpLiMZMry-IG2l1HzWUlU3dRYsXO1Af8rKuRR6wXBKVUiod0LNaFrgq"]
    try:
        firebase.send_notification_multicast(tokens, jsonable_encoder(data))
    except Exception as e:
        AppLog.error(e)
        print(e)



