import urllib
import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Test Google form
url = "https://docs.google.com/forms/d/e/1FAIpQLSf_wC3PzH3nd832UbQqnvcfT07DcWudRalSQvDsVoJv4qGUuA/formResponse"
	
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
name_box = soup.find('input', attrs={'name': 'fbzx'})


# Find form ID
print("Form id: " + name_box['value'])

# Find entry input fields
input = soup.find_all('input', {'name': re.compile('entry.')})
pp.pprint(list(map(lambda x : x['name'], input)))


for tag in input:
    pp.pprint(tag['name'])
    opts = tag.parent.find_all("div", { "role" : "radio" })
    if opts:
        pp.pprint(list(map(lambda x : x['data-value'], opts)))
    else:
        opts = tag.parent.find_all("div", { "role" : "checkbox" })
        pp.pprint(list(map(lambda x : x['aria-label'], opts)))


# Hardcoded the data
values= {
'entry.1491116351_sentinel' : "",
'entry.1491116351' : 'Opcja 2',
'entry.1491116351' : 'Opcja 1',
'entry.564186924':'Opcja 1',
'entry.66323047':'Opcja 1',
'fvv' : '1',
'draftResponse ': '[null,null, ' + name_box['value'] + ']',
'pageHistory':'0',
'fbzx': name_box['value']
}

data = urllib.parse.urlencode(values).encode("utf-8")
	
# Send HTTP POST request
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)

# Read the response
html = response.read()

soup = BeautifulSoup(html, 'html.parser')
name_box = soup.find('input', attrs={'class': 'freebirdFormviewerViewResponseConfirmationMessage'})
#print(soup.prettify())

