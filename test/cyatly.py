# import requests,json,uuid
# idusr,idsys = str(uuid.uuid4()),str(uuid.uuid4())
# headers = {
#     'User-Agent': 'ktor-client',
#     'Accept': 'application/json,text/event-stream',
#     'streaming': 'true',
#     'x-accel-buffering': 'no',
#     'accept-charset': 'UTF-8',
#     'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIzYzM1YTRiMi1mZGRhLTQyOGUtYWZhNi1jYTVkMzE3YzYxYTYiLCJpbnRlZ3JpdHlDaGVjayI6dHJ1ZSwiYmFzZVVybCI6ImNoYXRseTovL29hdXRoIiwicHJvZHVjdFZhbGlkRm9yIjoiQ0hBVExZIiwiaWF0IjoxNzU2MTA3NDQyLCJleHAiOjE3NTYxMjkwNDIsInN1YiI6IjNjMzVhNGIyLWZkZGEtNDI4ZS1hZmE2LWNhNWQzMTdjNjFhNiJ9.eA5XZM38lyVl36NF6oD4gd9wPqXyfugBOS0ov4wvQUM',
# }
# files = {
#     'data': (None, json.dumps({
#   "id": "109dc4ec-cbcf-41fb-95d2-5e49b2076cce",
#   "model": "vgpt-g3-m",
#   "messages": [
#                 {
#                     "content": [
#                             {
#                               "type": "text",
#                               "text": "hai"
#                             }
#                           ],
#                     "id": idusr,
#                     "role": "user",
#                     "model": "vgpt-g2-4"
#                 }
#             ],
#   "temperature": 0.5,
#   "stream": False
# }), None, {'Content-Type': 'application/json'}),
# }

# response = requests.post('https://streaming-chatly.vyro.ai/v1/chat/completions', headers=headers, files=files)
# print(response.text)
import requests,time
# import subprocess

# # solver = subprocess.Popen([
# #     "solver",
# #     "--port", "8088",
# #     "--secret", "jWRN7DH6",
# #     "--browser-position",
# #     "--max-attempts", "3",
# #     "--captcha-timeout", "30",
# #     "--page-load-timeout", "30",
# #     "--reload-on-overrun"
# # ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# # time.sleep(3)

# SERVER_URL = "http://127.0.0.1:8088"

# url = f"{SERVER_URL}/solve"

# headers = {
#   'ngrok-skip-browser-warning': '_',
#   'secret': 'jWRN7DH6',
#   'Content-Type': 'application/json'
# }

# json_data = {
#   "site_url": "https://accounts.vyro.ai/auth/sign-in/email?redirect=chatly%3A%2F%2Foauth%2Fvyro&isSubscribed=true&email=muhamadidris2025%40hotmail.com",
#   "site_key": "0x4AAAAAAAKHJu0Qox2uqsT2sss"
# }

# response = requests.get(

#   url=url,
#   headers=headers,
#   json=json_data,
# )

# response.raise_for_status()
# data = response.json()

# {
#   "elapsed": "2.641519",
#   "message": null,
#   "status": "OK",
#   "token": "0.MwOLQ3dg..."
# }

# token = data['token']
token = "0.oYkhFPAarf1LZIcHjM38irJ3XcWM54JpKmXt4bqGG7DnVnEtApX2wqqPSe3lwKlVb2q8mNcgN_BJ704obNvlFKmnl44g0BIP0s5rn4cnAvMEyI4ZJstZGc5LKcGc7SjiTJs4IIi8mffxLhQQ5pD-uo54M5Wu8T1hPqzbEsrf_12nrGUgrCrkk5pv86uHnxJwAyfuBZD5iIyGqxpuNbqnHY79NjcD-_h2h82uEuyEJVAenZO2-DxLjMwcO6bA0ZUw6vhvfTflPNiU5n5d3juE0L4wVfrLgmTr5UNn6kVXVI2XRC7t6kRaU0u9lf4wu8jk4jKcW1VNJr4U8VyXC9FF2vAYYDISSXxLbJ4zRLFzs--bszvRPywljPnzTolwjcT-iYNo9MVr7mOfpVLxnA2rdfgGe64gcX-417NQFY-i_GFLydjglhRhhZW4ql0Mx4LIrKV1CM1E5wB7Qw9vtKw-JCB-YiDb4AHJaCzgegr04aYwtLA8xRKuCY3mwRxX4iOZ4v935yoTmakhWXmdw8uW6UKQLFYPj8ASDcM0xi2s-ao8Ld1QYr-2B8Oo17dyDLU7qmQhcXgQFPoen_0gQzbnSW9ROM7GXn5szmr76LRcJV71fwS6PQw98vZ5amo8wZ0gGzfUR4IKg5dNo6UWTpgnQ5tIv_FkwrcAt_6C9DgoWK0wJ9iUaQTZk2Tdcj11fumiToVCW-mt_2NOu8T-qNEAXwHgfxkxyfrGgkKgH42klERhpBIgf4iakTgDyq1c51Zf-_9kNI4HVJVX7CtR3etz0xajuyHeLkkMWo-mXHjtfLZV2aLj2g1Rmd6e8pjaRGywintGbUSSSmq-JlX4wcY8nxPUizzsUoOol_xIL1DSKo-Q8vKlQWZ4TtGMXVudqGmB.lR2UveWqFXDViXMRWyjDRw.f5acb023b1a540e65c831c3f0d439e6209a03d2cbeba5219e754ad3447140e83"
print(token)
import json,time
url = "https://auth.vyro.ai/apis/v1/auth/custom/login?redirect=chatly:%2F%2Foauth%2Fvyro&isSubscribed=true"

payload = {
  "email": "muhamadidris2025@hotmail.com",
.}

headers = {
  'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
  'Accept': "application/json, text/plain, */*",
  'Accept-Encoding': "gzip, deflate, br, zstd",
  'Content-Type': "application/json",
  'accept-language': "id,en-US;q=0.7,en;q=0.3",
  'origin': "https://accounts.vyro.ai",
  'referer': "https://accounts.vyro.ai/",
  'sec-fetch-dest': "empty",
  'sec-fetch-mode': "cors",
  'sec-fetch-site': "same-site",
  'priority': "u=0",
  'te': "trailers"
}

response = requests.post(url, data=json.dumps(payload), headers=headers).json()
result = response.get('result')
print(response)
if result:
    token : str = result['redirect']
    url = "https://auth.vyro.ai/apis/v1/auth/other/user-info?token=" + token.replace('chatly://oauth/vyro?token=','')
    bearer : dict = requests.get(url).json()
    bearer = bearer.get('result').get('sessionToken')
    print(bearer)

# solver.terminate()