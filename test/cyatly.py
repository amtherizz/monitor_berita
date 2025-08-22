import requests,json,uuid
idusr,idsys = str(uuid.uuid4()),str(uuid.uuid4())
headers = {
    'User-Agent': 'ktor-client',
    'Accept': 'application/json,text/event-stream',
    'streaming': 'true',
    'x-accel-buffering': 'no',
    'accept-charset': 'UTF-8',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI4YWZhZDRiYi00YjEwLTRmNWEtOWIzNS0zNTJhMmMxYTMyZWMiLCJpbnRlZ3JpdHlDaGVjayI6dHJ1ZSwiYmFzZVVybCI6ImNoYXRseTovL29hdXRoIiwicHJvZHVjdFZhbGlkRm9yIjoiQ0hBVExZIiwiaWF0IjoxNzU1NTczNTU0LCJleHAiOjE3NTU1OTUxNTQsInN1YiI6IjhhZmFkNGJiLTRiMTAtNGY1YS05YjM1LTM1MmEyYzFhMzJlYyJ9.kpkcD5BAKLkcMYs4Db6aeYN_519AztCTOnQ7OqRKra4',
}
files = {
    'data': (None, json.dumps({
  "id": "109dc4ec-cbcf-41fb-95d2-5e49b2076cce",
  "model": "vgpt-g3-m",
  "messages": [
                {
                    "content": [
                            {
                              "type": "text",
                              "text": "hai"
                            }
                          ],
                    "id": idusr,
                    "role": "user",
                    "model": "vgpt-g2-4"
                }
            ],
  "temperature": 0.5,
  "stream": False
}), None, {'Content-Type': 'application/json'}),
}

response = requests.post('https://streaming-chatly.vyro.ai/v1/chat/completions', headers=headers, files=files)
print(response.text)