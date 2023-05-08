import requests, json, re, os
from parsel import Selector


def get_selector(input):
    query = ' '.join(input)
    params = {
        "q": query,
        "hl": "en",     # language
        "gl": "us",     # country of the search, US -> USA
        "tbm": "shop"   # google search shopping
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    selector = Selector(html.text)

    return selector


def get_original_images(input):
    selector = get_selector(input)
    all_script_tags = "".join(
        [
            script.replace("</script>", "</script>\n")
            for script in selector.css("script").getall()
        ]
    )
	
    image_urls = []
    
    for result in selector.css(".Qlx7of .sh-dgr__grid-result"):
        # https://regex101.com/r/udjFUq/1
        url_with_unicode = re.findall(rf"var\s?_u='(.*?)';var\s?_i='{result.attrib['data-pck']}';", all_script_tags)

        if url_with_unicode:
            url_decode = bytes(url_with_unicode[0], 'ascii').decode('unicode-escape')
            image_urls.append(url_decode)
            
	# download_original_images(image_urls)	
    return image_urls


def download_original_images(image_urls):
	for index, image_url in enumerate(image_urls, start=1):
		image = requests.get(image_url, headers=headers, timeout=30, stream=True)
	
		if image.status_code == 200:
			print(f"Downloading {index} image...")
			with open(f"images/image_{index}.jpeg", "wb") as file:
				file.write(image.content)


def get_suggested_search_data(input,num_sugg=1):
    print("SEARCHING FOR :")
    print(input)
    google_shopping_data = []
    selector = get_selector(input)
    sugg = []
    for result, thumbnail in zip(selector.css(".Qlx7of .i0X6df"), get_original_images(input)):
        title = result.css(".tAxDx::text").get()		
        product_link = "https://www.google.com" + result.css(".Lq5OHe::attr(href)").get()	
        product_rating = result.css(".NzUzee .Rsc7Yb::text").get()		
        product_reviews = result.css(".NzUzee > div::text").get()		
        price = result.css(".a8Pemb::text").get()		
        store = result.css(".aULzUe::text").get()		
        store_link = "https://www.google.com" + result.css(".eaGTj div a::attr(href)").get()		
        delivery = result.css(".vEjMR::text").get()
		
        store_rating_value = result.css(".zLPF4b .XEeQ2 .QIrs8::text").get()
        store_rating = re.search(r"^\S+", store_rating_value).group() if store_rating_value else store_rating_value
		
        store_reviews_value = result.css(".zLPF4b .XEeQ2 .ugFiYb::text").get()
        store_reviews = re.search(r"^\(?(\S+)", store_reviews_value).group() if store_reviews_value else store_reviews_value

        store_reviews_link_value = result.css(".zLPF4b .XEeQ2 .QhE5Fb::attr(href)").get()
        store_reviews_link = "https://www.google.com" + store_reviews_link_value if store_reviews_link_value else store_reviews_link_value

        compare_prices_link_value = result.css(".Ldx8hd .iXEZD::attr(href)").get()		
        compare_prices_link = "https://www.google.com" + compare_prices_link_value if compare_prices_link_value else compare_prices_link_value

        google_shopping_data.append({
            "title": title,
            "product_link": product_link,
            "product_rating": product_rating,
            "product_reviews": product_reviews,
            "price": price,
            "store": store,
            "thumbnail": thumbnail,
            "store_link": store_link,
            "delivery": delivery,
            "store_rating": store_rating,
            "store_reviews": store_reviews,
            "store_reviews_link": store_reviews_link,
            "compare_prices_link": compare_prices_link,
        })

        # Sort the products by weighted average of ratings in descending order
        weighted_average = lambda x: 0.7*float(x['product_rating'] or 0) + 0.3*float(x['store_rating'] or 0)
        google_shopping_data.sort(key=weighted_average, reverse=True)
        
        # Select the top three products by rating
        sugg = google_shopping_data[:num_sugg]

    #print(json.dumps(sugg, indent=2, ensure_ascii=False))
    # top_suggestions = [json.dumps(s, indent=2, ensure_ascii=False) for s in sugg]
    top_suggestions = sugg
    return top_suggestions

# Test:
# get_suggested_search_data(["black", "formal shoes", "mens"])