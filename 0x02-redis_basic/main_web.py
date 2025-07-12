#!/usr/bin/env python3

get_page = __import__('web').get_page

url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://example.com"

print(get_page(url))
print(get_page(url))
print(get_page(url))
