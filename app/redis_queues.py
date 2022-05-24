from redis import Redis
from rq import Queue, Retry

from app.speedsms import send_sms

q = Queue(connection=Redis(host='localhost', port=6379))


def send_sms_queue(phone: str, content: str, type_sms: int, sender: str):
    job = q.enqueue(send_sms, phone, content, type_sms, sender, retry=Retry(max=3))
    return job
