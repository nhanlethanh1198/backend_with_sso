import json

import requests


async def send_sms(phone, content, type_sms, sender):
    # access_token = 'VsKTV2laE9lNX1oD9w8EZiUDA0k7d0_u'
    # buf = access_token + ':x'
    # auth = base64.b64encode(bytes(buf, 'utf-8'))
    # auth = "Basic "+auth.decode("utf-8") 
    # auth = 'Basic '+buf
    payload = json.dumps({
        "to": [phone],
        "content": content,
        "sms_type": type_sms,
        "sender": sender
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic VnNLVFYybGFFOWxOWDFvRDl3OEVaaVVEQTBrN2QwX3U6eA=='
    }
    res = requests.post('https://api.speedsms.vn:443/index.php/sms/send', headers=headers, data=payload)
    res = res.json()
