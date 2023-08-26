from flask import Flask, render_template, request,jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/2", methods = ['GET'])
def clickbutton():
    return 'https://www.google.com'

@app.route("/review" , methods = ['POST' ])
def index():

    if (request.method == 'POST'):
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            try:
                flipkart_html = bs(flipkartPage, 'html.parser')
            except Exception as e:
                print(e)
            content = flipkart_html.find_all("div", {"class":"_13oc-S"})

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Title, Price, Rating, Discount, Description, Other -Offer \n"
            fw.write(headers)
            reviews = []
            for title in product_title:
                try:
                    product_title = flipkart_html.find_all("div", {"class": "_4rR01T"})

                except:
                    logging.info("product_title")

                try:
                    product_price = flipkart_html.find_all("div", {"class": "_30jeq3 _1_WHN1"})
                except:
                    product_price = 'No Price'
                    logging.info("Price")

                try:
                    product_rating = flipkart_html.find_all("div", {"class": "_3LWZlK"})

                except:
                    product_rating = 'No Ratings'
                    logging.info("Rating")
                try:
                    product_discount = flipkart_html.find_all("div", {"class": "_3Ay6Sb"})

                except:
                    logging.info("Discount")
                
                try:
                    product_description = flipkart_html.find_all("li", {"class": "rgWa7D"})

                except:
                    logging.info("Description")
                
                try:
                    product_exchange_offer = flipkart_html.find_all("div", {"class": "_2ZdXDB"})

                except:
                    logging.info("Offer")

                mydict = {"Product": searchString, "Name": product_title, "Price": product_price, "Rating": product_rating, "Discount": product_discount,
                          "Description": product_description, "Other Offer": product_exchange_offer}
                reviews.append(mydict)
            logging.info("log my final result {}".format(reviews))
            return render_template(filename='result.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            logging.info(e)
            return 'something is wrong'

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
