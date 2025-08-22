#!/usr/bin/env python3
import requests

base_url = "https://ihexpo-app.eventstrat.ai/api/event/users/170"
headers = {
    'User-Agent': "Dart/3.8 (dart:io)",
    'Accept-Encoding': "gzip",
    'content-type': "application/json",
    'authorization': "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjJiN2JhZmIyZjEwY2FlMmIxZjA3ZjM4MTZjNTQyMmJlY2NhNWMyMjMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaWVtbC0tLWloZXhwbyIsImF1ZCI6ImllbWwtLS1paGV4cG8iLCJhdXRoX3RpbWUiOjE3NTQ3MDQ2MjgsInVzZXJfaWQiOiI1R0VGR2IydVgzVjdKUmlETWs4RlJ2RTdEVmoyIiwic3ViIjoiNUdFRkdiMnVYM1Y3SlJpRE1rOEZSdkU3RFZqMiIsImlhdCI6MTc1NDc1Mzg4OCwiZXhwIjoxNzU0NzU3NDg4LCJlbWFpbCI6ImluZm9Ac2FuZHNtZXJjaGFuZGlzaW5nLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJpbmZvQHNhbmRzbWVyY2hhbmRpc2luZy5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.pO8MpDDrIOb7O1pqNyaw5OqF2kE1TViyBiLQd7KqVrhTRobrj_aohLhnx0DbsmE09d7NitQCCnPBWqpX5Ar0eYUW6S1PQgfJVV3blNNiZEERLZL_UDRwDTxnx_LIfMJwb2T2No6go-bUIZoGEBMc7UhBQhpTTpdfnsDfoGPOn145PKdkRe2CTKEr7wZ54txkOj9dRfVAhU0ipWzW6XapxO0xQYDwoK1R_ZGQTTcpHuUaCGR3M63YMGQuH6umeL1k8r2V7TlKMqKf6FgWHt3HWC3KGbKJilN-W0c--gO3RQzXkupi3X6M_Q09ZmbpIsEurd1wRU8mUnQIzZg2HbH18Q"
}

all_data = []
page_number = 1
page_size = 100
total_records = 0

while True:
    params = {
        'pageSize': page_size,
        'pageNumber': page_number,
        'userCohort': 'EXHIBITOR'
    }
    
    print(f" Fetching page {page_number}...")
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f" Error on page {page_number}: HTTP {response.status_code}")
        print(response.text)
        break
    
    response_data = response.json()
    print(response_data)
    current_page_data = response_data.get('data', [])
    meta = response_data.get('meta', {})
    
    if not current_page_data:
        print("No more data available. Stopping.")
        break
    
    all_data.extend(current_page_data)
    records_fetched = len(current_page_data)
    total_records += records_fetched
    
    print(f" Page {page_number}: Added {records_fetched} records (Total: {total_records})")
    print(f"   Meta: {meta}")  # Debug: Show pagination metadata
    
    # Update total count from meta if available
    if 'userCount' in meta:
        total_records = meta['userCount']
    
    # Move to next page
    page_number += 1

print(f"\n🎉 Completed! Fetched {len(all_data)} exhibitor records.")
print(f"   Total pages processed: {page_number - 1}")
print(f"   First record: {all_data[0]['companyName'] if all_data else 'N/A'}")
print(f"   Last record: {all_data[-1]['companyName'] if all_data else 'N/A'}")