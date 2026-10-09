from urllib.parse import quote

CATALOG = {
 "home": [
  {"title":"Minimal LED Ceiling Light","category":"lighting","platform":"IKEA","price":2499,"keywords":"modern living room bedroom lighting","query":"modern LED ceiling light"},
  {"title":"Compact Study Table","category":"furniture","platform":"Amazon","price":4999,"keywords":"study bedroom office table","query":"compact study table"},
  {"title":"5-Blade Ceiling Fan","category":"fan","platform":"Amazon","price":3299,"keywords":"bedroom living room fan","query":"5 blade ceiling fan"},
  {"title":"Extendable Dining Table","category":"dining","platform":"IKEA","price":11999,"keywords":"dining modern family","query":"extendable dining table"},
  {"title":"Neutral Wall Art Set","category":"decor","platform":"Flipkart","price":1599,"keywords":"decor living room modern","query":"neutral wall art set"}
 ],
 "party": [
  {"title":"Vegetarian Catering Package","category":"catering","platform":"Zomato","price":450,"keywords":"birthday wedding corporate vegetarian","query":"vegetarian catering"},
  {"title":"Mixed Menu Catering Package","category":"catering","platform":"Swiggy","price":650,"keywords":"birthday wedding corporate mixed","query":"party catering mixed menu"},
  {"title":"Event Decoration Package","category":"decoration","platform":"Amazon","price":5999,"keywords":"birthday wedding decoration","query":"party decoration package"},
  {"title":"Budget Event Stay","category":"accommodation","platform":"OYO","price":1800,"keywords":"guest stay event","query":"budget hotel stay"}
 ],
 "jewelry": [
  {"title":"Pearl Drop Earrings","category":"earrings","platform":"Amazon","price":1299,"keywords":"elegant wedding traditional white pastel","query":"pearl drop earrings"},
  {"title":"Minimal Gold-Tone Necklace","category":"necklace","platform":"Flipkart","price":2199,"keywords":"elegant party office gold red black","query":"minimal gold tone necklace"},
  {"title":"Kundan-Style Stud Set","category":"earrings","platform":"Amazon","price":1799,"keywords":"wedding traditional festive red maroon","query":"kundan style stud earrings"},
  {"title":"Crystal Bracelet","category":"bracelet","platform":"Flipkart","price":999,"keywords":"party elegant pastel blue","query":"crystal bracelet"},
  {"title":"Statement Necklace Set","category":"necklace","platform":"Amazon","price":3499,"keywords":"wedding festive statement maroon green","query":"statement necklace set"}
 ]
}

def catalog_for(kind):
    return CATALOG[kind]

def public_item(x):
    y = dict(x)
    y["url"] = "https://www.google.com/search?q=" + quote(f'{x["platform"]} {x["query"]}')
    return y
