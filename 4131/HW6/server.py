from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib  # Only for parse.unquote and parse.unquote_plus.
import json
import base64
from typing import Union, Optional
import re
import datetime
import time
# If you need to add anything above here you should check with course staff first.
listings = [
    {
        'title': 'Banned Air Jordan Ones',
        'image': 'https://m.media-amazon.com/images/I/7137GjFiZ6L._AC_SY395_.jpg',
        'description': 'The iconic Air Jordan Ones that were banned from the NBA. A piece of sneaker history.',
        'category': 'sports',
        'id': 1,
        'sale_date': '2024-12-15 12:00',  
        'end_date': '2024-11-15 18:00',
        'bids': [
            {'bidder': 'James Rodriguez', 'amount': 50000, 'comment': 'An absolute must-have for any collector.'},
            {'bidder': 'Emily Chen', 'amount': 52000, 'comment': 'The story behind these shoes makes them priceless.'},
            {'bidder': 'William Carter', 'amount': 54000, 'comment': 'I won\'t stop until these are mine.'},  
        ]
    },
    {
        'title': 'Back to the Future Nike Shoes',
        'image': 'https://www.hollywoodreporter.com/wp-content/uploads/2019/07/nike-publicity-h_2019.jpg?w=1296&h=730&crop=1',
        'description': 'The self-lacing Nike Mag from Back to The Future, a perfect blend of movie memorabilia and futuristic fashion.',
        'category': 'actors',
        'id': 2,
        'sale_date': '2024-12-15 12:00',  
        'end_date': '2024-11-12 20:30',
        'bids': [
            {'bidder': 'Sarah Johnson', 'amount': 120000, 'comment': 'These are a dream come true!'},
            {'bidder': 'Lucas Brown', 'amount': 125000, 'comment': 'Can\'t let this piece of nostalgia slip away.'},  
            {'bidder': 'Ava Clark', 'amount': 130000, 'comment': 'A true collector\'s item.'},  
            {'bidder': 'Joe Clark', 'amount': 1300000, 'comment': 'A true item.'} 
        ]
    },
    {
        'title': 'Michael Jackson\'s Dance Shoes',
        'image': 'https://external-preview.redd.it/3eal1lLVFglo657rVhdHecbOHu2yX8zyBFxII12IcaI.jpg?auto=webp&s=ca8ee13b158be85f58692410dc3962dbd27099f5',
        'description': 'The iconic shoes worn by Michael Jackson when he unveiled the Moonwalk.',
        'category': 'music',
        'id': 3,
        'sale_date': '2024-12-15 12:00',  
        'end_date': '2024-11-10 22:00',
        'bids': [
            {'bidder': 'Mia Wilson', 'amount': 100000, 'comment': 'An essential piece of pop culture history.'},
            {'bidder': 'Ethan Lee', 'amount': 105000, 'comment': 'It would be an honor to own these.'},
            {'bidder': 'Sophia Martinez', 'amount': 110000, 'comment': 'These shoes have so much legacy behind them.'}
        ]
    },
    {
        'title': 'Mike Tyson\'s Final Boxing Shoes',
        'image': 'https://minotaurclothing.co.uk/wp-content/uploads/2022/10/The-Mike-Tyson-look-Boot.jpg',
        'description': 'The shoes worn by Mike Tyson in his final professional boxing match. A tribute to a legendary career.',
        'category': 'sports',
        'id': 4,
        'sale_date': '2024-12-15 12:00',  
        'end_date': '2024-11-18 16:00',
        'bids': [
            {'bidder': 'Daniel Thompson', 'amount': 60000, 'comment': 'A fitting tribute to an incredible fighter.'},
            {'bidder': 'Ella Rivera', 'amount': 62000, 'comment': 'The perfect piece for any Tyson fan.'},
            {'bidder': 'Jacob Harris', 'amount': 64000, 'comment': 'These shoes are worth every penny.'}
        ]
    }
]

def render_listing(listing):
    listing_html = f"""  
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>{escape_html(listing['title'])}</title>
        <link rel="stylesheet" href="/main.css">
        <script src="/bid.js" defer></script>
        <style>
            .new-bid {{ display: none; }} 
        </style>
    </head>
    <body>
        <nav>
            <ul class="NavBar">
                <li><a href="/main">About Us</a></li>
                <li><a href="/gallery">Gallery</a></li>
                <li><a href="/create">Add Listing</a></li>

                <form action="" method="GET" class="NavBar">
                    <label for="seachBar"></label>
                    <input type="search" name="q" id="seachBar">

                    <label for="dropDown"></label>
                    <select name="Categories" id="dropDown">
                        <option value="All">All Categorys</option>
                        <option value="sports">Sports</option>
                        <option value="actors">Actors/Movie</option>
                        <option value="music">Music</option>
                    </select>
                    
                    <input type="submit" id="submit_btn">
                </form>
            </ul>
        </nav>

        <div>
            <h1 class="listing-title">{escape_html(listing['title'])}</h1>
                <div class="content">
                    <div class="column">
                         <img src="{listing.get('image', 'default-image-url.jpg')}" alt="{escape_html(listing['title'])}" class="product-image">
                        <div class="description-box">
                            <p>{escape_html(listing['description'])}</p>
                        </div>
                    </div>
                    <div class="column">
                        <div class="btn_title">
                            <h2 class="adding-title">Bids</h2>
                            <button type="button" id="bid-btn"> Place Bid</button>
                        </div>
                        <ul>
                        <div class="line"></div>
                        <li class='new-bid'> 
                            <form action="/place_bid" method="POST" class="new-bid">
                                <input type="hidden" name="listing_id" value="{listing['id']}">
                                <label for="new-bid-name">Your Name:</label>
                                <input type="text" name="new-bid-name" id="new-bid-name" placeholder="Your Name" required>

                                <label for="new-bid-amount">Amount:</label>
                                <input type="number" name="new-bid-amount" id="new-bid-amount" placeholder="Amount" required>

                                <label for="new-bid-comment">Comment:</label>
                                <textarea name="new-bid-comment" id="new-bid-comment" placeholder="Comment" required></textarea>
                                
                                <input type="submit" name="new-bid-submit" id="new-bid-submit" required>
                            </form>
                        </li>
                        """
    if 'bids' in listing:                    
        for bid in listing['bids']:
            listing_html += f"""
                <li class="bid-box">
                    <span class="bidder-name">{escape_html(bid['bidder'])}</span>
                    <span class="bid-amount">{typeset_dollars(bid['amount'])}</span>
                    <p class="bid-comment">{escape_html(bid['comment'])}</p>
                </li>
                """
    else:
        listing_html += "<li>No bids yet.</li>"    

    listing_html += """
                        </ul>
                    </div>
                </div>     
        </body>
    </html>
    """
    return listing_html 

def render_gallery(query, category):
    gallery = f"""  
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Historical Shoes Auction</title>
        <link href="main.css" rel="stylesheet">
        <script src="/table.js" defer></script>
        <script src="/hover.js" defer></script>
    </head>
    <body>
        <nav>
            <ul class="NavBar">
                <li><a href="/main">About Us</a></li>
                <li><a href="/gallery">Gallery</a></li>
                <li><a href="/create">Add Listing</a></li>

                <form action="" method="GET" class="NavBar">
                    <label for="seachBar"></label>
                    <input type="search" name="q" id="seachBar">

                    <label for="dropDown"></label>
                    <select name="Categories" id="dropDown">
                        <option value="All">All Categorys</option>
                        <option value="sports">Sports</option>
                        <option value="actors">Actors/Movie</option>
                        <option value="music">Music</option>
                    </select>
                    
                    <input type="submit" id="submit_btn">
                </form>
            </ul>
        </nav>
        <div class="gallery-right">
            <h1 class="gallery-title">Gallery</h1>
            <table class="galleryTable">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Number of Bids</th>
                        <th>Category</th>
                        <th>Top Bid</th>
                        <th> Sale Date </th>
                        <th>Auction Ends</th>
                        <th>Delete</th>
                    </tr>
                </thead>
                <tbody Class="tableData">
        """



    if not query and category == "All":
        for listing in listings:
            # data_image = listing['image']
            # data_description = listing['description']
            if listing['bids']:
                top_bid = typeset_dollars(listing['bids'][-1]['amount'])
            else:
                top_bid = "$0.00"
            gallery += f"""
                <tr class="listing-row" data-image="{listing['image']}">
                <td><a href="/listing/{listing['id']}">{listing['title']}</a></td>
                <td>{len(listing['bids'])}</td>
                <td>{listing['category']}</td>
                <td>{top_bid}</td>
                <td>{listing['sale_date']}</td>
                <td class="auction-end-time">{listing['end_date']}</td>
                <th><button class="delete-btn" data-listing-id="{listing['id']}">Delete</button></th>
                </tr>
            """
    else:
        filtered_listings = [listing for listing in listings if query.lower() in listing['title'].lower()] if query else listings.copy()

        if category != "All":
            filtered_listings = [listing for listing in filtered_listings if listing['category'] == category]

        for listing in filtered_listings:
            if listing['bids']:
                top_bid = typeset_dollars(listing['bids'][-1]['amount'])
            else:
                top_bid = "$0.00"
            gallery += f"""
                <tr class="listing-row" data-image="{listing['image']}">
                    <td><a href="/listing/{listing['id']}">{listing['title']}</a></td>
                    <td>{len(listing['bids'])}</td>
                    <td>{listing['category']}</td>
                    <td>{top_bid}</td>
                    <td>{listing['sale_date']}</td>
                    <td class="auction-end-time">{listing['end_date']}</td>
                    <th><button class="delete-btn" data-listing-id="{listing['id']}">Delete</button></th>


                </tr>
            """

    gallery += """
            </table>
        </div>
        <div class="gallery-left">
            <div class="img-desc-js">
                 <img id="preview-image" src="https://m.media-amazon.com/images/I/7137GjFiZ6L._AC_SY395_.jpg" alt="preview Image" style="max-width: 100%;">
            </div>
        </div>
    </body>
    </html>
    """

    return gallery

def parse_cookies(cookie_header):
    cookies = {}
    if cookie_header:
        cookie_list = cookie_header.split(";")
        for cookie in cookie_list:
            key, value = cookie.split("=")
            cookies[key.strip()] = value.strip()
    return cookies



def add_new_listing(params): 
    required_fields = ["title-form", "Image-form", "Descript-form", "Categories-form", "sale-Form"]
    for field in required_fields:
        if field not in params or not params[field]:
            return False  



    new_id = max([listing["id"] for listing in listings]) + 1 if listings else 1
    new_listing = {
        "id": new_id,
        "title": params["title-form"],
        "image_url": params["Image-form"],
        "description": params["Descript-form"],
        "category": params["Categories-form"] ,
        "sale_date": "10/23/2024",
        "end_date": params["sale-Form"],
        "bids": [] 
    }

    listings.append(new_listing)
    return True

def add_new_bid(params):
    print(params)
    listing_id = int(params.get("listing_id", -1))
    
    # Validate listing ID and other fields
    listing = next((lst for lst in listings if lst["id"] == listing_id), None)
    if not listing or not params.get("bidder_name") or not params.get("new_bid_amount"):
        return False  # Missing fields or invalid listing

    bid_amount = float(params["new_bid_amount"])
    current_max_bid = max([bid["amount"] for bid in listing.get("bids", [])], default=0)

    # Check if the new bid amount is greater than the current max bid
    if bid_amount <= current_max_bid:
        return False  

    new_bid = {
        "bidder": params["bidder_name"],
        "amount": bid_amount,
        "comment": params.get("comment", "")
    }
    listing["bids"].append(new_bid)
    print("this is listing bids", listing['bids'])
    return True




# Provided helper function. This function can help you implement rate limiting


rate_limit_store = []


def pass_api_rate_limit() -> tuple[bool, int | None]:
    """This function will keep track of rate limiting for you.
    Call it once per request, it will return how much delay would be needed.
    If it returns 0 then process the request as normal
    Otherwise if it returns a positive value, that's the number of seconds
    that need to pass before the next request"""
    from datetime import datetime, timedelta

    global rate_limit_store
    # you may find it useful to change these for testing, such as 1 request for 3 seconds.s
    RATE_LIMIT = 4  # requests per second
    RATE_LIMIT_WINDOW = 10  # seconds
    # Refresh rate_limit_store to only "recent" times
    rate_limit_store = [
        time
        for time in rate_limit_store
        if datetime.now() - time <= timedelta(seconds=RATE_LIMIT_WINDOW)
    ]
    if len(rate_limit_store) >= RATE_LIMIT:
        return (
            RATE_LIMIT_WINDOW - (datetime.now() - rate_limit_store[0]).total_seconds()
        )
    else:
        # Add current time to rate_limit_store
        rate_limit_store.append(datetime.now())
        return 0


def escape_html(str):
    # this i s a bare minimum for hack-prevention.
    # You might want more.
    str = str.replace("&", "&amp;")
    str = str.replace('"', "&quot;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    str = str.replace("'", "&#39;")
    return str


def unescape_url(url_str):
    import urllib.parse

    # NOTE -- this is the only place urllib is allowed on this assignment.
    return urllib.parse.unquote_plus(url_str)


def parse_query_parameters(response):
    pairs = response.split("&")
    parsed_params = {}

    for pair in pairs:
        key = unescape_url(pair.split("=")[0])
        value = unescape_url(pair.split("=")[1])
        parsed_params[key] = value

    return parsed_params


def typeset_dollars(number):
    return f"${number:.2f}"


# The method signature is a bit "hairy", but don't stress it -- just check the documentation below.
# NOTE some people's computers don't like the type hints. If so replace below with simply: `def server(method, url, body, headers)`
# The type hints are fully optional in python.
def server(
    request_method: str,
    url: str,
    request_body: Optional[str],
    request_headers: dict[str, str],
) -> tuple[Union[str, bytes], int, dict[str, str]]:
    """
    `method` will be the HTTP method used, for our server that's GET, POST, DELETE, and maybe PUT
    `url` is the partial url, just like seen in previous assignments
    `body` will either be the python special `None` (if the body wouldn't be sent (such as in a GET request))
         or the body will be a string-parsed version of what data was sent.
    headers will be a python dictionary containing all sent headers.

    This function returns 3 things:
    The response body (a string containing text, or binary data)
    The response code (200 = ok, 404=not found, etc.)
    A _dictionary_ of headers. This should always contain Content-Type as seen in the example below.
    """
    # feel free to delete anything below this, so long as the function behaves right it's cool.
    # That said, I figured we could give you some starter code...

    response_body = None
    status = 200
    response_headers = {}

    # Parse URL -- this is probably the best way to do it. Delete if you want.
    parameters = None
    if "?" in url:
        url, query_string = url.split("?", 1)
        parameters = parse_query_parameters(query_string)
        
    cookies_header = request_headers.get("Cookie", "")
    cookies = parse_cookies(cookies_header)
    bidder_name_cookie = cookies.get("bidder_name", "")


    # To help you get rolling... the 404 page will probably look like this.
    # Notice how we have to be explicit that "text/html" should be the value for
    # header: "Content-Type" now instead of being returned directly.
    # I am sorry that you're going to have to do a bunch of boring refactoring.

    if url == "/" or url == "/main":  
        response_body = open("static/html/mainpage.html").read()
        status = 200  
        response_headers["Content-Type"] = "text/html; charset=utf-8"

    elif url == "/gallery":
        var = parameters if parameters else {}
        gallery_var = var.get('q', '')
        category_var = var.get('Categories', 'All')
        response_body = render_gallery(gallery_var, category_var)
        status = 200
        response_headers["Content-Type"] = "text/html; charset=utf-8"

    elif url.startswith("/listing/"):
        listing_id = url.split("/")[2]
        listing = next((lst for lst in listings if lst["id"] == int(listing_id)), None)
        if listing:
            response_body = render_listing(listing)
            status = 200
            response_headers["Content-Type"] = "text/html; charset=utf-8"
        else:
            response_body = open("static/html/404.html").read()
            status = 404
            response_headers["Content-Type"] = "text/html; charset=utf-8"
    
    
    
    elif url == "/create":
        response_body = open("static/html/create.html").read()
        status = 200  
        response_headers["Content-Type"] = "text/html; charset=utf-8"

    elif url == "/main.css":
        response_body = open("static/css/main.css", "r").read()
        status = 200  
        response_headers["Content-Type"] = "text/css; charset=utf-8"

    elif url == "/images/proj.jpeg":
        img_file = open("static/images/proj.jpeg", "rb")
        response_body = img_file.read()
        img_file.close()  
        status = 200  
        response_headers["Content-Type"] = "image/jpeg; charset=utf-8"

    elif url == "/bid.js": 
        response_body = open("static/js/bid.js").read()
        status = 200  
        response_headers["Content-Type"] = "application/javascript; charset=utf-8"
    
    elif url == "/new_listing.js": 
        response_body = open("static/js/new_listing.js").read()
        status = 200  
        response_headers["Content-Type"] = "application/javascript; charset=utf-8"

    elif url == "/table.js": 
        response_body = open("static/js/table.js").read()
        status = 200  
        response_headers["Content-Type"] = "application/javascript; charset=utf-8"


    elif url == "/api/place_bid" and request_method == "POST":
    
        content_type = request_headers.get("Content-Type", "")
        if content_type != "application/json":
            return "Invalid Content-Type", 400, {"Content-Type": "application/json"}
        
        try:
            body = json.loads(request_body)
        except json.JSONDecodeError:
            return "Invalid JSON", 400, {"Content-Type": "application/json"}
        listing_id = int(body.get("listing_id", -1))
        if add_new_bid(body):
            status = 201
            response_body = json.dumps(listings[listing_id]["bids"])
            response_headers["Content-Type"] = "application/json"
        else:   
            status = 400
            response_body = json.dumps(listings[listing_id]["bids"])
            response_headers["Content-Type"] = "application/json"

        if bidder_name_cookie:
            bidder_name = bidder_name_cookie
        else:
            bidder_name = body.get("bidder_name")
            response_headers["Set-Cookie"] = f"bidder_name={bidder_name}; SameSite=Strict"

    elif url == "/api/delete_listing" and request_method == "DELETE":
        content_type = request_headers.get("Content-Type", "")
        
        if content_type != "application/json":
            return "Invalid Content-Type", 400, {"Content-Type": "text/plain"}

        try:
            body = json.loads(request_body)
        except json.JSONDecodeError:
            return "Invalid JSON", 400, {"Content-Type": "text/plain"}

        listing_id = body.get("listing_id")
        if not listing_id:
            return "Missing listing_id", 400, {"Content-Type": "text/plain"}

        listing = next((lst for lst in listings if lst["id"] == listing_id), None)
        if listing:
            listings.remove(listing)
            status = 204
            response_body = json.dumps({"message": "Listing deleted successfully"})
            response_headers["Content-Type"] = "application/json"
        else:
            status = 400
            response_body = json.dumps({"message": "Listing not found"})
            response_headers["Content-Type"] = "application/json"




    else:
        response_body = open("static/html/404.html").read()
        status = 404
        response_headers["Content-Type"] = "text/html; charset=utf-8"

    
    
    
    return response_body, status, response_headers


# You shouldn't need to change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def c_read_body(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get("Content-Length", 0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")
        return body

    def c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)

        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)

    def do_POST(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response(
                "Couldn't read body as text", 400, {"Content-Type": "text/plain"}
            )
            raise

        try:
            # Step 2: handle it.
            message, response_code, headers = server(
                "POST", self.path, body, self.headers
            )
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response(
                "The server function crashed.", 500, {"Content-Type": "text/plain"}
            )
            raise

    def do_GET(self):
        try:
            # Step 1: handle it.
            message, response_code, headers = server(
                "GET", self.path, None, self.headers
            )
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response(
                "The server function crashed.", 500, {"Content-Type": "text/plain"}
            )
            raise

    def do_DELETE(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response(
                "Couldn't read body as text", 400, {"Content-Type": "text/plain"}
            )
            raise

        try:
            # Step 2: handle it.
            message, response_code, headers = server(
                "DELETE", self.path, body, self.headers
            )
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response(
                "The server function crashed.", 500, {"Content-Type": "text/plain"}
            )
            raise


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
