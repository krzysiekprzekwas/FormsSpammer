from urllib import request, parse
from bs4 import BeautifulSoup
import datetime
import re
import pprint
import random
from faker import Faker
class Entry:

   def __init__(self, description, id, type, answers):
      self.id = id
      self.description = description
      self.type = type
      self.answers = answers
   
   def __str__(self):
      return self.description + " " + self.id + " " + self.type + " " + ''.join(str(a)+ " " for a in self.answers)

   def __repr__(self):
      return str(self)

def spam( count, url):
    # Initialize Pretty Printer
    pp = pprint.PrettyPrinter(indent=4)
    fake = Faker()

    base_time = datetime.datetime.now()

    # Open Google Forms 
    # TO DO: Check if url really leads to Google forms
    page = request.urlopen(url)
    
    finish_time = datetime.datetime.now()

    content = page.read()

    download_time = finish_time - base_time
    print("Download time:",download_time.microseconds * 10**-6,"seconds")
    print("Page size:",len(content),"bytes")
    print("Download speed: %.2f MB/s" % ((len(content)* 10**-6)/(download_time.microseconds * 10**-6)))

    soup = BeautifulSoup(content, 'html.parser')

    entries = []
    
    submit = soup.find_all('div', {'class': 'freebirdFormviewerViewNavigationSubmitButton'})
    
    if not submit:
        print("\nMulti page forms not supported!")

        
    # Find entry input fields
    input = soup.find_all('input', {'name': re.compile('entry.[0-9]*$')})
    
    # Find possible input values for coresponding entries
    for tag in input:

        opts = tag.parent.find_all("div", { "role" : re.compile('checkbox') })
        type = 'checkbox'

        if not opts:
            opts = tag.parent.find_all("div", { "role" : re.compile('radio$|option') })
            type = 'radio'

        # Find common anscestor and extract entry desciption
        container =  tag.find_parent("div", { "role" : re.compile('listitem') })
        description = container.find("div", { "role" : re.compile('heading') }).text

        values = set()
        for opt in opts:
            val = opt['aria-label'] if opt['role'] == "checkbox" else opt['data-value']
            if val != "":
                values.add(val.split(",")[-1].strip())
        
        if any(x.id == tag['name'] for x in entries):
            for x in entries:
                if x.id == tag['name']:
                    x.answers = x.answers.union(values)
                    break
        else:
            entries.append(Entry(description, tag['name'], type, values))
    
    # Show found entries with values
    print("\nFound these entries with values:")
    pp.pprint(entries)
        

    for x in range(1, count + 1):

        print("\nForm number " + str(x) + " from " + str(count))

        # Open Google Forms 
        # TO DO: Check if url really leads to Google forms
        page = request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        
        # Find form ID
        name_box = soup.find('input', attrs={'name': 'fbzx'})
        print("\nForm id: " + name_box['value'])
        
        # Choose random values for inputs
        values = []
        for entry in entries:
            if entry.type == 'radio' and len(entry.answers) != 0:
                values.append((entry.id,random.choice(list(entry.answers))))
            elif entry.type == 'radio' and len(entry.answers) == 0:
                values.append((entry.id,fake.text(max_nb_chars=100, ext_word_list=None)))
            else:
                samples = random.sample(entry.answers, random.randint(0, len(entry.answers)))

                for a in samples:
                    values.append((entry.id,a))
        
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
        
        req = request.Request(url, data)
        base_time = datetime.datetime.now()
        
        # Send HTTP POST request
        response = request.urlopen(req)

        finish_time = datetime.datetime.now()
        html = response.read()
    
        upload_time = finish_time - base_time
        print("Upload time:",upload_time.microseconds * 10**-6,"seconds")
        print("Page size:",len(html),"bytes")
        print("Upload speed: %.2f MB/s" % ((len(html)* 10**-6)/(upload_time.microseconds * 10**-6)))
        
        # Read the response
        
        soup = BeautifulSoup(html, 'html.parser')
        name_box = soup.find('input', attrs={'class': 'freebirdFormviewerViewResponseConfirmationMessage'})

        if name_box:
            print("Form sent")

spam(1,"https://docs.google.com/forms/d/e/1FAIpQLSf_wC3PzH3nd832UbQqnvcfT07DcWudRalSQvDsVoJv4qGUuA/formResponse")
