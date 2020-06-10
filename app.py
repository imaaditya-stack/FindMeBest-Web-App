# WebScraping App to compare the prices of similar products online,
# offered by different brands and retailers

#importing libraries

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, flash, request, redirect, url_for, render_template

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.secret_key = "151FAHUI216892GAOP"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/price', methods=["GET", "POST"])
def price():
    if request.method == "POST":

        search = request.form['inputsearch']

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

        # Amazon

        amazonresponse = requests.get("https://www.amazon.in/s?k="+search.lower(),headers=headers)

        amazoncontent = amazonresponse.content

        #BeautifulSoup Object Initialization
        amazonsoupobject = BeautifulSoup(amazoncontent,"html.parser")

        amazonproducts = amazonsoupobject.find_all("div",attrs={"class": "s-include-content-margin"})

        if len(amazonproducts) < 1:
            flash("Please enter a valid product","danger")
            return redirect(url_for('home'))

        amazondata = []

        for product in range(5):
                #Empty dictionary to store the data in key-value pair
                amazondatadict = {}
        # a-popover-trigger a-declarative
                #Try except blocks
                #Try block store the data
                #If exception occurs it will store empty string

                if search.lower() in amazonproducts[product].find("img",attrs={"class":"s-image"})['alt'].lower():

                    #Restuarant Name
                    try:
                        amazondatadict['productname']=amazonproducts[product].find("img",attrs={"class":"s-image"})['alt']
                    except:
                        amazondatadict['productname']=''

                    try:
                        amazondatadict['producturl']=amazonproducts[product].find("a",attrs={"class":"a-link-normal"},href=True)['href']
                    except:
                        amazondatadict['producturl']=''

                    try:
                        amazondatadict['productimg']=amazonproducts[product].find("img",attrs={"class":"s-image"})['src']
                    except:
                        amazondatadict['productimg']=''

                    try:
                        amazondatadict['productrating']=amazonproducts[product].find("div",attrs={"class":"hGSR34"}).text.strip()
                    except:
                        amazondatadict['productrating']=''

                    #Votes
                    try:
                        amazondatadict['productprice']=amazonproducts[product].find("a",attrs={"class":"a-size-base"}).next_element.next_element.find("span",attrs={"class":"a-offscreen"}).text.strip()
                    except:
                        amazondatadict['productprice']=''

                amazondata.append(amazondatadict)


        # Flipkart

        driver=webdriver.Chrome(ChromeDriverManager().install())

        driver.get("https://www.flipkart.com/search?q="+search)

        #BeautifulSoup Object Initialization
        flipkartsoupobject = BeautifulSoup(driver.page_source,"html.parser")

        flipkartproducts = flipkartsoupobject.find_all("div",attrs={"class": "_1UoZlX"})

        if len(flipkartproducts) < 1:
            flash("Please enter a valid product","danger")
            return redirect(url_for('home'))

        flipkartdata = []

        for product in range(5):
                #Empty dictionary to store the data in key-value pair
                flipkartdatadict = {}
        # a-popover-trigger a-declarative
                #Try except blocks
                #Try block store the data
                #If exception occurs it will store empty
                if flipkartproducts:

                    if search.lower() in flipkartproducts[product].find("div",attrs={"class":"_3wU53n"}).text.strip().lower():

                        try:
                            flipkartdatadict['productname']=flipkartproducts[product].find("div",attrs={"class":"_3wU53n"}).text.strip()
                        except:
                            flipkartdatadict['productname']=''

                        try:
                            flipkartdatadict['producturl']=flipkartproducts[product].find("a",attrs={"class":"_31qSD5"},href=True)['href']
                        except:
                            flipkartdatadict['producturl']=''

                        try:
                            flipkartdatadict['productimg']=flipkartproducts[product].find("img",attrs={"class":"_1Nyybr"})['src']
                        except:
                            flipkartdatadict['productimg']=''

                        try:
                            flipkartdatadict['productprice']=flipkartproducts[product].find("div",attrs={"class":"_1vC4OE"}).text.strip()
                        except:
                            flipkartdatadict['productprice']=''

                flipkartdata.append(flipkartdatadict)


        #Snapdeal


        snapdealresponse = requests.get("https://www.snapdeal.com/search?keyword="+search,headers=headers)

        snapdealcontent = snapdealresponse.content

        #BeautifulSoup Object Initialization
        snapdealsoupobject = BeautifulSoup(snapdealcontent,"html.parser")

        snapdealproducts = snapdealsoupobject.find_all("div",attrs={"class": "product-tuple-listing"})

        if len(snapdealproducts) < 1:
            flash("Please enter a valid product","danger")
            return redirect(url_for('home'))

        snapdealdata = []

        for product in range(5):
                #Empty dictionary to store the data in key-value pair
                snapdealdatadict = {}
        # a-popover-trigger a-declarative
                #Try except blocks
                #Try block store the data
                #If exception occurs it will store empty string

                if search.lower() in snapdealproducts[product].find("p",attrs={"class":"product-title"}).text.strip().lower():

                    try:
                        snapdealdatadict['productname']=snapdealproducts[product].find("p",attrs={"class":"product-title"}).text.strip()
                    except:
                        snapdealdatadict['productname']=''

                    try:
                        snapdealdatadict['ProductPrice']=snapdealproducts[product].find("div",attrs={"class":"product-price-row"}).find("span",attrs={"class":"product-price"}).text.strip()
                    except:
                        snapdealdatadict['productprice']=''

                    try:
                        snapdealdatadict['productimg']=snapdealproducts[product].find("img",attrs={"class":"product-image"})['src']
                    except:
                        snapdealdatadict['productimg']=''

                    try:
                        snapdealdatadict['producturl']=snapdealproducts[product].find("a",attrs={"class":"dp-widget-link"},href=True)['href']
                    except:
                        snapdealdatadict['producturl']=''

                snapdealdata.append(snapdealdatadict)


    return render_template('main.html',amazon=amazondata,flipkart=flipkartdata,snapdeal=snapdealdata,query=search)

if __name__ == '__main__':
    app.run(debug=True)


# The resource was preloaded using link preload but not used within a few seconds from the window's load event. Please make sure it has an appropriate `as` value and it is preloaded intentionally.
