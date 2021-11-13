# decorator of schedule
from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect
from bs4 import BeautifulSoup
import requests
import re
def index(request):
    return render(request,"index.html")
def scrape(request):
    try:
        url=request.POST.get("_url")
        if "http://" in url or "https://" in url:
            r=requests.get(url)
        else:
            r=requests.get(f"https://{url}")
    except:
        return HttpResponse(f"Error : {url} Not Found. ")
    else:
        soup=BeautifulSoup(r.content,"html.parser")
        # Trick 1 (StackOverflow) :
        try:
            meta_description=soup.find("meta",property="og:description")
            meta_description_content=meta_description["content"]
        # Trick 2 (My Trick) :
        # for i in meta:
        #     meta_descripion=str(i)
        #     if "description" in meta_descripion:
        #         pattern=re.compile(r'content="')
        #         for j in pattern.finditer(meta_descripion):
        #             print(meta_descripion[j.span()[1]:-1])
        except:
            return
        # Now Find First Img Tag :
        try:
            first_img=soup.find("img")
            first_img_src=first_img["src"]
        except:
            return 
        # Now Find Title :
        try:
            website_title=soup.find("title")
            website_title_content=website_title.string
        except:
            return 
        # Now Push Content To scraping.html
    params={
        "website_url":r.url if r.url else "Invalid URL",
        "meta_description":meta_description_content if meta_description_content else "Website Does Not Have Any Meta Description Tags",
        "first_image":first_img_src if first_img_src else "Website Does Not Any Have Image Tags",
        "website_title":website_title_content if website_title_content else "Website Does Not Have Any Title Tag",
    }
    return render(request,"scraping.html",params)