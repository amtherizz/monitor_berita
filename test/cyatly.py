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
token = "0.a_pKlnA0-Fh8lmhNJo7vqwxq3bqJ6JrYUTSxf3uAsRxRl-EUNhkm07yRYlVx5uQso1rGOhhzot70Bj_GQhGV1-bC_HI0Gd7fZFkBwk2J9GlwM7CxU1RIvMIJYX6VpnvI3FcjVxTkN4vCfJ6ubQ8fy3efTm1Nz_wUA2vYvwgJiixUL2N8Ea9NWOd9BFZVCyApPLGvdgNG0z8icW50vV2v2H3bzvm0TMxqhNrphkaxM1rVq59fwDt-Ec04uVbkhK-cAkmMF8HVvEI8N17us5CzbGN70B16OqMdnYplx1GZ1Qh54nFzVSGGEvbkZQuu6bl-pBS5IrnEzS7NdiV2MVfbbFSUMY1OYx5e9KPez0EoCa7d5-eViOAoRKmzZxQ2gGFJ2TVrAbBO0sRq0EFK8VPjd3AZGqngeLbjFE8jd2s6aMBjNoAR09FJV4aOXCC5uolvp7QID6WUeXjnR6zUqFh9p-iG5SsbR51qQn7kqkz30Ua2GMru8JKk4IcIjeW_5OnwIUt49W0mKr9SnawDCE6BLg9dl62Bo_6eLM5nHqzCnVKYjCd45xGfTqdd5pGYXQMnuURB-5Rd5SjplsI8IVb7x9Eklql3C_MZMjevunmdTDXPQ001t9-kD591HIVH-mR3zN3qW11WeDuvebsYNkn87DBRLpRaO__R9pcWIqNz6KRQCEHT_JthlFHbaMgvgPx3Q6lry_gn1sb_8JpUsnhIyzwULj9er-NkeCAb8csLOzWfkV4Ds_tPKvjnH5UwlBNtNO0m5laRkGf_vRLBa4S-U1EfX2GEcWsYzk-ZrsoWn6G3pMIBiiX_LUY4dLgPKZzMv9CYE6ZbgJ2gZWTo3KV7p62rGngM8IO9Cpq5bFjHkOgd6DUp-tgyPKDlqPiynRyb.C63VBa0Yl1Koehc2-fCuKA.e95540b463ecb89675951a35aa418bd33f63f3cc0a70215ddb9bc97ad63f9f81"
print(token)
import json,time
url = "https://auth.vyro.ai/apis/v1/auth/custom/login?redirect=chatly:%2F%2Foauth%2Fvyro&isSubscribed=true"

payload = {
  "email": "muhamadidris2025@hotmail.com",
  "password": ",PL'&j^ift.$,89",
  "captcha": token,
  "isSubscribed": True
}

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