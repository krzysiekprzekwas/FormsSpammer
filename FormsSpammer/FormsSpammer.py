import urllib
import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import pprint
import random

class Entry:

   def __init__(self, name, answers):
      self.name = name
      self.answers = answers
   
   def __str__(self):
      return self.name + " " + ''.join(str(a)+ " " for a in self.answers)

   def __repr__(self):
      return str(self)


pp = pprint.PrettyPrinter(indent=4)

# Test Google form
url = "https://docs.google.com/forms/d/e/1FAIpQLSf_wC3PzH3nd832UbQqnvcfT07DcWudRalSQvDsVoJv4qGUuA/formResponse"
	
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
name_box = soup.find('input', attrs={'name': 'fbzx'})


# Find form ID
print("Form id: " + name_box['value'])

entries = []

# Find entry input fields
input = soup.find_all('input', {'name': re.compile('entry.[0-9]*$')})
#pp.pprint(list(map(lambda x : x['name'], input)))

for tag in input:
    opts = tag.parent.find_all("div", { "role" : re.compile('radio$|checkbox|option') })
    values = set()
    for opt in opts:
        val = opt['aria-label'] if opt['role'] == "checkbox" else opt['data-value']
        if val != "":
            values.add(val)

    entries.append(Entry(tag['name'],values))

pp.pprint(entries)

values = []
for entry in entries:
    values.append((entry.name,random.choice(list(entry.answers))))

values = values + [('fvv' , '1'),
('draftResponse ', '[null,null, ' + name_box['value'] + ']'),
('pageHistory','0'),
('fbzx', name_box['value'])
]

data = urllib.parse.urlencode(values).encode("utf-8")

print(data)

# Send HTTP POST request
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)

# Read the response
html = response.read()

soup = BeautifulSoup(html, 'html.parser')
name_box = soup.find('input', attrs={'class': 'freebirdFormviewerViewResponseConfirmationMessage'})
#print(soup.prettify())

