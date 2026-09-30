#!/usr/bin/env python3
"""Validate generated locale pages, discovery metadata and local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json, xml.etree.ElementTree as ET
from datetime import date, datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parent.parent/'docs'
BASE='https://no-sleep-pika.online'
# Editorial content dates are recorded in Korea; CI runners use UTC.
TODAY=datetime.now(ZoneInfo('Asia/Seoul')).date()
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.assets=[];self.alternates={};self.canonical=None;self.lang=None;self.h1=0;self.structured=[];self.in_json=False;self.buffer='';self.title=False;self.description=False;self.ids=set();self.og_url=None;self.robots='';self.title_text='';self.in_title=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):
   assert a['id'] not in self.ids,('duplicate id',a['id'])
   self.ids.add(a['id'])
  if tag=='html':self.lang=a.get('lang')
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True;self.in_title=True
  if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
  if tag=='meta' and a.get('name')=='robots':self.robots=a.get('content','')
  if tag=='meta' and a.get('property')=='og:url':self.og_url=a.get('content')
  if tag=='link':
   if a.get('rel')=='canonical':self.canonical=a.get('href')
   if a.get('rel')=='alternate' and a.get('hreflang'):self.alternates[a['hreflang']]=a.get('href')
   if a.get('rel') in ('stylesheet','icon'):self.assets.append(a.get('href',''))
  if tag=='a':self.links.append(a.get('href',''))
  if tag in ('img','script'):self.assets.append(a.get('src',''))
  if tag=='script' and a.get('type')=='application/ld+json':self.in_json=True;self.buffer=''
 def handle_data(self,data):
  if self.in_json:self.buffer+=data
  if self.in_title:self.title_text+=data
 def handle_endtag(self,tag):
  if tag=='title':self.in_title=False
  if tag=='script' and self.in_json:self.structured.append(json.loads(self.buffer));self.in_json=False
pages=sorted(ROOT.rglob('index.html'))
assert len(pages)==19, f'Expected 15 locale pages, 2 installation guides and 2 usage guides, got {len(pages)}'
canonical=set()
parsed={}
titles=set()
for path in pages:
 page=Page();page.feed(path.read_text())
 assert page.lang and page.title and page.description,path
 assert page.h1==1,(path,'must have one H1')
 assert page.canonical and page.canonical.startswith(BASE),path
 relative=path.relative_to(ROOT)
 expected_url=BASE+'/'+str(relative.parent).strip('.')
 if not expected_url.endswith('/'):expected_url+='/'
 assert page.canonical==expected_url,(path,'self canonical',page.canonical,expected_url)
 assert page.canonical not in parsed,(path,'duplicate canonical')
 parsed[page.canonical]=page
 assert page.og_url==page.canonical,(path,'sharing URL')
 assert 'index' in page.robots and 'noindex' not in page.robots,(path,'indexability')
 assert page.title_text not in titles,(path,'duplicate title')
 titles.add(page.title_text)
 expected_alternates = 3 if set(('install','guide')) & set(relative.parts) else 16
 assert len(page.alternates)==expected_alternates and 'x-default' in page.alternates,(path,'hreflang')
 assert page.structured,(path,'structured data')
 entities=[entity for block in page.structured for entity in block.get('@graph',[block])]
 for entity in entities:
  assert 'aggregateRating' not in entity and 'review' not in entity,(path,'no fabricated ratings')
  if entity.get('@type')=='SoftwareApplication':
   assert entity['downloadUrl'].endswith('/pika-'+entity['softwareVersion']+'.pkg'),(path,'release mismatch')
   assert entity['downloadUrl'] in page.links,(path,'structured data must match visible download')
   assert entity['url']==page.canonical,(path,'localized app URL')
 canonical.add(page.canonical)
 for href in page.links+page.assets+list(page.alternates.values()):
  if not href or href.startswith(('#','data:','mailto:')):continue
  url=urlparse(href)
  if url.scheme and url.netloc!=urlparse(BASE).netloc:continue
  local=unquote(url.path)
  target=(ROOT/local.lstrip('/')) if local.startswith('/') else path.parent/local
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(path,href,target)
 print('PASS',path.relative_to(ROOT),page.lang)
for url,page in parsed.items():
 assert page.alternates.get(page.lang)==url,(url,'missing self hreflang')
 for language,alternate in page.alternates.items():
  assert alternate in parsed,(url,'unknown alternate',alternate)
  assert parsed[alternate].alternates==page.alternates,(url,'nonreciprocal hreflang',alternate)
  if language!='x-default':assert parsed[alternate].lang==language,(url,'wrong alternate language')
 for href in page.links:
  target=urlparse(href)
  if target.fragment and (not target.netloc or target.netloc==urlparse(BASE).netloc):
   destination=url if not target.path else BASE+target.path
   assert destination in parsed and unquote(target.fragment) in parsed[destination].ids,(url,'broken anchor',href)
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
sitemap=ET.parse(ROOT/'sitemap.xml')
items=sitemap.findall('s:url',ns)
urls={item.find('s:loc',ns).text for item in items}
assert len(items)==len(urls),'duplicate sitemap URLs'
assert urls==canonical,(urls,canonical)
for item in items:
 url=item.find('s:loc',ns).text
 alternates={el.attrib['hreflang']:el.attrib['href'] for el in item.findall('x:link',ns)}
 assert alternates==parsed[url].alternates,(url,'sitemap and HTML hreflang mismatch')
 modified=item.find('s:lastmod',ns)
 assert modified is not None and date.fromisoformat(modified.text)<=TODAY,(url,'invalid modification date')
# User guides must be reachable by real links without executing JavaScript.
reachable={BASE+'/'}
pending=list(reachable)
while pending:
 page=parsed[pending.pop()]
 for href in page.links:
  target=urlparse(href)
  if target.path.startswith('/') and not target.netloc:destination=BASE+target.path
  elif target.netloc==urlparse(BASE).netloc:destination=BASE+target.path
  else:continue
  if destination in parsed and destination not in reachable:reachable.add(destination);pending.append(destination)
assert reachable==canonical,('orphaned pages',canonical-reachable)
assert 'Sitemap: '+BASE+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
assert (ROOT/'CNAME').read_text().strip()=='no-sleep-pika.online'
print('PASS 19 pages: reciprocal hreflang, sitemap dates, canonical/OG consistency, schema release, crawlable guides, assets and anchors')
