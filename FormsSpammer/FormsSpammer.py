from urllib import request, parse
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

def spam( count, url):
    # Initialize Pretty Printer
    pp = pprint.PrettyPrinter(indent=4)

    for x in range(1, count + 1):

        print("\nForm number " + str(x) + " from " + str(count))

        # Open Google Forms 
        # TO DO: Check if url really leads to Google forms
        page = request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        
        # Find form ID
        name_box = soup.find('input', attrs={'name': 'fbzx'})
        print("\nForm id: " + name_box['value'])
        
        entries = []
        
        # Find entry input fields
        input = soup.find_all('input', {'name': re.compile('entry.[0-9]*$')})
        
        # Find possible input values for coresponding entries
        for tag in input:
            opts = tag.parent.find_all("div", { "role" : re.compile('radio$|checkbox|option') })
            values = set()
            for opt in opts:
                val = opt['aria-label'] if opt['role'] == "checkbox" else opt['data-value']
                if val != "":
                    values.add(val.split(",")[-1].strip())
            
            if any(x.name == tag['name'] for x in entries):
                for x in entries:
                    if x.name == tag['name']:
                        x.answers = x.answers.union(values)
                        break
            else:
                entries.append(Entry(tag['name'],values))
        
        # Show found entries with values
        print("\nFound these entries with values:")
        pp.pprint(entries)
        
        values = []
        for entry in entries:
            values.append((entry.name,random.choice(list(entry.answers))))
        
        values = values + [('fvv' , '1'),
        ('draftResponse ', '[null,null, ' + name_box['value'] + ']'),
        ('pageHistory','0'),
        ('fbzx', name_box['value'])
        ]
        
        print('\nValues to be sent to form:')
        pp.pprint(values)
        
        data = parse.urlencode(values).encode("utf-8")
        
        print("\nValues as url params:")
        pp.pprint(data)
        
        # Send HTTP POST request
        req = request.Request(url, data)
        response = request.urlopen(req)
        
        # Read the response
        # TO DO: Check if response was accepted
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        name_box = soup.find('input', attrs={'class': 'freebirdFormviewerViewResponseConfirmationMessage'})

spam(2,"https://docs.google.com/forms/d/e/1FAIpQLSf_wC3PzH3nd832UbQqnvcfT07DcWudRalSQvDsVoJv4qGUuA/formResponse")
