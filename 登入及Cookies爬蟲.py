import requests
#s=requests.Session()#自動處理Cookies，第4、9行requests換成s且不用打cookies
params={'username':'Rex','password':'password'}
r=requests.post('http://pythonscraping.com/pages/cookies/welcome.php',params)
print(r.text)
print('Cookie is set to:')
print(r.cookies.get_dict())
print('-------------------')
r=requests.get('http://pythonscraping.com/pages/cookies/profile.php',cookies=r.cookies)
print(r.text)