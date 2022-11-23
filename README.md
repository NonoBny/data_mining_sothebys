# Data Mining Project - Sotheby's
***
members : _Yosef Schoen, Noa Benayoun_
```
For this project we wanted to scrap the data for each auction / collection available publicly on Sotheby's website :
https://www.sothebys.com/en/
```
<img src="img_for_README.png"/>

## Table of contents
***
* [General info](#general-info)
* [Milestone 1](#milestone_1)
* [Instruction](#instruction)


## General info
***
The art market industry, an industry as opaque as it is intriguing, innovative, and attractive. Indeed, few could have
predicted that the global sales at public auctions of art and antiques would eventually generate billions. In 2020, the
sales value of this market amounted to 17.6 billion USD and in 2021, the total sales of Sotheby’s worldwide, including
both the public and private channels, totaled 7.3 billion USD, the highest figure recorded by the company to date. With
art pieces from names as prestigious as Picasso, Bansky or Warhol, from widely different art scenes, luxurious items
highly sought such as Patek Philip watches, extremely rare wines, and other wonders, as well as luxury properties and an
online platform entirely dedicated to NFT sales, Sotheby’s is one of the two auction houses dominating the market.

## Milestone 1
***
We created a webscraper using the packages **REQUESTS**, **BEAUTIFOULSOUP** and **SELENIUM**.

**REQUESTS** was used to check the availability of the data.
**BEAUTIFOULSOUP** was used to register the HTML data and to find the information desired.
**SELENIUM** was used to navigate into logging, to the result page, and to move back and forth between the collection 
pages.

For each collection, we extracted the data points that were relevant, either on the original result page or on the pages 
of the collection themselves. We are able to extract five "general" information: **Title of Collection**, 
**Date of Auction**, **Time of Auction**, **Place of Auction** and **Type of Items** ; and for each item of the 
collection, we have **Title of Item**, **Estimated Price**, **Selling price**, **Currency**, **Reserve**, and an extra 
key **Author** for the Art pieces type of item collections.

## Instruction
***
```
In order for the program to run on your machine you need to create an account with Sotheby'.  
Then create a txt file called password_id and store your user-name/email in the first line and password on the second line.
```
After being logged, our program dynamically get to the result page which allowed us to extract the data points that 
are relevant to our project. Indeed, we decided to generate a list of all the past auctions collections, moving through 
a for loop to number of pages we wish to scam through – by changing the constant _**NUMBER_OF_PAGES**_. For each result 
page, we extract the link for each collection with the function _get_url_n_sale_total()_, which enables us to navigate
to each collection thanks to selenium and to be able to extract the data of all the items for each collection. 
==> Soon explanation for command line request

