from http.server import BaseHTTPRequestHandler, HTTPServer
import re


# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.

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

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.


def escape_html(s):
    s = s.replace("&", "&amp;")  
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace("'", "&#39;")  
    return s


def unescape_url(url_str):
    import urllib.parse

    # NOTE -- this is the only place urllib is allowed on this assignment.
    return urllib.parse.unquote_plus(url_str)


def parse_query_parameters(response):
    # Split the query string into key-value pairs
    pairs = response.split("&")
    # Initialize a dictionary to store parsed parameters
    dict = {}
    # Iterate over each key-value pair
    # Split the pair by '=' to separate key and value
    for pair in pairs:
        if '=' in pair:  
            key, value = pair.split('=')  
            dict[key] = value.replace('+', ' ')
        else:
            dict["q"] = ""
            dict["Categories"] = "All"
    return dict

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




# Provided function -- converts numbers like 42 or 7.347 to "$42.00" or "$7.35"
def typeset_dollars(number):
    return f"${number:.2f}"


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
    if not listing or not params.get("new-bid-name") or not params.get("new-bid-amount"):
        return False  # Missing fields or invalid listing

    bid_amount = float(params["new-bid-amount"])
    current_max_bid = max([bid["amount"] for bid in listing.get("bids", [])], default=0)

    # Check if the new bid amount is greater than the current max bid
    if bid_amount <= current_max_bid:
        return False  

    new_bid = {
        "bidder": params["new-bid-name"],
        "amount": bid_amount,
        "comment": params.get("new-bid-comment", "")
    }
    listing.setdefault("bids", []).append(new_bid)
    return True

def server_GET(url: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    path = url

    query = ""
    if "?" in url:
        path, query = path.split("?")

    if path == "/" or path == "/main":
        return open("static/html/mainpage.html").read(),'text/html', 200

    elif path == "/gallery":
        var = parse_query_parameters(query)
        print(var)
        gallery_var = None
        category_var = None
        if len(var) >= 2:
            gallery_var = var['q']
            category_var = var['Categories']
        else:
            gallery_var = ''
            category_var = 'All'
        return render_gallery(gallery_var ,category_var),'text/html', 200

    elif path.startswith("/listing/"):
        part = None
        listings_id = path[9:]
        for listing in listings:
            if int(listing["id"]) == int(listings_id):
                part = listing
                break
        if part:
            return render_listing(part), "text/html", 200
        else: 
            return open("static/html/404.html").read(), 'text/html', 404
    
    elif path == "/create":
        return open("static/html/create.html").read(), 'text/html', 200

    elif path == "/main.css":
        return open("static/css/main.css", "r").read(), "text/css", 200

    elif path == "/images/main":
        return open("static/images/project_image.jpeg").read(), "image/jpeg", 200
    
            
    elif path == "/create":
        return open("static/html/create.html").read(), 'text/html', 200
    
    elif path == "/bid.js": 
        return open("static/js/bid.js").read(), "application/javascript", 200
    
    elif path == "/new_listing.js": 
        return open("static/js/new_listing.js").read(), "application/javascript", 200

    elif path == "/table.js": 
        return open("static/js/table.js").read(), "application/javascript", 200
    else:
        return open("static/html/404.html").read(),'text/html', 404
    

def server_POST(url: str, body: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a POST request to this website.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    adding_new_lst = parse_query_parameters(body)
    adding_new_bid = parse_query_parameters(body)
    path = url

    query = ""
    if "?" in url:
        path, query = url.split("?",1)

    if path == "/create":
        if add_new_listing(adding_new_lst):  
            return open("static/html/create_success.html").read(), 'text/html', 201
        else:
            return open("static/html/create_fail.html").read(), 'text/html', 400

    elif path == "/place_bid":
        if add_new_bid(adding_new_lst):
            return open("static/html/create_success.html").read(), 'text/html', 201
        else:
            return open("static/html/create_fail.html").read(), 'text/html', 400

    return open("static/html/404.html").read(), 'text/html', 404

# You shouldn't need to change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get("Content-Length", 0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")

        message, content_type, response_code = server_POST(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

    def do_GET(self):
        # Call the student-edited server code.
        message, content_type, response_code = server_GET(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
