import urllib
import urllib.request as urllib2
from bs4 import BeautifulSoup

url = "https://docs.google.com/forms/d/e/1FAIpQLSf_wC3PzH3nd832UbQqnvcfT07DcWudRalSQvDsVoJv4qGUuA/formResponse"
	
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

print(soup)	