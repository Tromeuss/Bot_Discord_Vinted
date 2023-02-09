import urllib
from bs4 import BeautifulSoup
#import urlparse
import mechanize

url = "https://www.vinted.fr/vetements?search_text=Air%20Force%201&search_id=8272236835&catalog[]=1231&size_id[]=778&size_id[]=780&size_id[]=782&size_id[]=784&size_id[]=785&size_id[]=786&size_id[]=787&size_id[]=788&color_id[]=12&color_id[]=1&brand_id[]=53&status_ids[]=6&status_ids[]=1&status_ids[]=2&status_ids[]=3&status_ids[]=4&order=newest_first"

br=mechanize.Browser()
br.open(url)
with open ("data.html","w+") as f:
  f.write(str(br.response().read()))