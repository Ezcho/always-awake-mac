#!/usr/bin/env python3
"""Validate generated locale pages, discovery metadata and local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent/'docs'
BASE='https://no-sleep-pika.online'
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.assets=[];self.alternates={};self.canonical=None;self.lang=None;self.h1=0;self.structured=[];self.in_json=False;self.buffer='';self.title=False;self.description=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=a.get('lang')
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
  if tag=='link':
   if a.get('rel')=='canonical':self.canonical=a.get('href')
   if a.get('rel')=='alternate' and a.get('hreflang'):self.alternates[a['hreflang']]=a.get('href')
   if a.get('rel') in ('stylesheet','icon'):self.assets.append(a.get('href',''))
  if tag=='a':self.links.append(a.get('href',''))
  if tag in ('img','script'):self.assets.append(a.get('src',''))
  if tag=='script' and a.get('type')=='application/ld+json':self.in_json=True;self.buffer=''
 def handle_data(self,data):
  if self.in_json:self.buffer+=data
 def handle_endtag(self,tag):
  if tag=='script' and self.in_json:self.structured.append(json.loads(self.buffer));self.in_json=False
pages=sorted(ROOT.rglob('index.html'))
assert len(pages)==15, f'Expected 15 locale pages, got {len(pages)}'
canonical=set()
for path in pages:
 page=Page();page.feed(path.read_text())
 assert page.lang and page.title and page.description,path
 assert page.h1==1,(path,'must have one H1')
 assert page.canonical and page.canonical.startswith(BASE),path
 assert len(page.alternates)==16 and 'x-default' in page.alternates,(path,'hreflang')
 assert page.structured,(path,'structured data')
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
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap=ET.parse(ROOT/'sitemap.xml')
urls={el.text for el in sitemap.findall('.//s:url/s:loc',ns)}
assert urls==canonical,(urls,canonical)
assert 'Sitemap: '+BASE+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
assert (ROOT/'CNAME').read_text().strip()=='no-sleep-pika.online'
print('PASS sitemap, robots, canonical, hreflang, structured data and all local links')
