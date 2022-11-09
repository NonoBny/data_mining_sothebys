
<img src="img_for_README.png"/>

The art market industry, an industry as opaque as it is intriguing, innovative, and attractive. Indeed, few could have
predicted that the global sales at public auctions of art and antiques would eventually generate billions. In 2020, the
sales value of this market amounted to 17.6 billion USD and in 2021, the total sales of Sotheby’s worldwide, including
both the public and private channels, totaled 7.3 billion USD, the highest figure recorded by the company to date. With
art pieces from names as prestigious as Picasso, Bansky or Warhol, from widely different art scenes, luxurious items
highly sought such as Patek Philip watches, extremely rare wines, and other wonders, as well as luxury properties and an
online platform entirely dedicated to NFT sales, Sotheby’s is one of the two auction houses dominating the market.
We have chosen to work on their website, https://www.sothebys.com/, to be able to get the data from their past auction
sales.

How does how web scrapper work? As the data from the sales is protected by password authentication, we first log into
the website. Then we dynamically get to the result page which will allow us to extract the data point that are relevant
for our project. Indeed, we decided to generate a list of all the past auctions collections, moving through a for loop
to number of pages we wish to scam through – by changing the constant _**NUMBER_OF_PAGES**_. For each result page, we extract
the link for each collection with the function _get_url_n_sale_total()_, which enables us to navigate to each collection thanks to selenium and to be able to extract
the data of all the items for each collection. We are creating a dictionary for each of the collection, with five
“general” information: **Title of Collection**, **Date of Auction**, **Time of Auction**, **Place of Auction** and **Type of Items** (as the
first five keys for each of the dictionary). Within the dictionary, the last key is the **Items** one (to list all the items of each
collection), for which we have created two nested dictionaries: one within the other, to have Sotheby’s index of the
item be the key, then as a value for each item a dictionary that list the data points we were able to extract for each
item. For each item, we have **Title of Item**, **Estimated Price**, **Selling price**, **Currency**, **Reserve**, and an extra key **Author**
for the Art pieces type of item collections.
