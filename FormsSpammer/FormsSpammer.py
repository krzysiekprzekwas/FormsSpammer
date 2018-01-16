import urllib
import urllib.request as urllib2
from bs4 import BeautifulSoup

# Test Google form
url = "https://docs.google.com/forms/d/e/1FAIpQLSf_wC3PzH3nd832UbQqnvcfT07DcWudRalSQvDsVoJv4qGUuA/formResponse"
	
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
name_box = soup.find('input', attrs={'name': 'fbzx'})
	
print("Form id: " + name_box['value'])

# Hardcoded the data
values= {
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

html = response.read()

soup = BeautifulSoup(html, 'html.parser')
name_box = soup.find('input', attrs={'class': 'freebirdFormviewerViewResponseConfirmationMessage'})
print(soup.prettify())

