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
token = "0.tS_fjr_70OgjjZDoVMmCYzeZJ9ooMaBUb8pJ54RF3IQg0mgb7IR8stzaaKEYg6r1zQJ0SvKpMK2ki4J3gUxtHHltHKTFcbfaghwjRijERFPuuZRXzb65vuUMBlAaQydOmO2Ya_IZeHca-nO6gp0P_ERZTI9aCK_07SkSr_Z_rgUQpwyJaSwldtH0REoUufNTUMwJ9t-OeAIZ_wN3tmqfgcuqs1a3x_zFN9mR1ddR5DWBWYHnBlMywDImK7mp0f9Nh5qty6QNEI1iFoZ3iWJjMd-pgYysokMPhTmv3iHowcblHAUwvgDZLnIRHy7M1ElrYQ-E-b8CLmZ-venDjODthAdHEtf1Bp2K3rC2MpHKLMG3L8DyuLFgumAr8K2FZevanI8yltItbH_I-K3o8FCAFAzkrwhcChw5P0P47frSDGHOCAck0A0fwBnlV2-PyjcA8evUiu3aFbRPbj2alJtPeiDOblvNPlBhRSeH7BK6c37gLPB5Jw1jLu15DhhG8-7gyPXmA7eXgsI119eyB0rBTQ3o0f_tvA3UXbe1EU955refnpSMh4SXDZmHBTNe_chIN7hGWj0l41FTkZ6AavXwqlAvu7dFC82VQACLB6V9b9heVcfpeYqUdG-u8mEI5UlduTuq4ao15Gc4eszF4lOnvSaHIfktdOWpZ8LSe3oeFFyXYcRbO15uETEmYF-2JVm6qYzjWEoAKvSFw_jnjCXY4jkaK_KdDjRH0GRXh_FR7U-hjhYMw_YnU9bd5O9b5NVaSq1jx0p0sV3UsYPeTDqI4VvfLaXqGHj4-JZfhhp8FxHIMeaCfYqgYy4p9m_ZqsUSngz_or2jA_FGssMMLgGIZJdImXGz2BHyPW4JMAollt2c5_VSNr_BiQ9LErBGhhrx.wh4d219X6BLBE1Dubc4zlA.4bc3c5437138a2087d22b23b486e799e7864a0797becd486b02935603710b250"

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