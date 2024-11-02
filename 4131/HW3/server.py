from http.server import BaseHTTPRequestHandler, HTTPServer
import re


# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.

listings = [
     {
        'id': 1,
        'title': 'Lake Street Auction House',
        'image_url': 'https://images.squarespace-cdn.com/content/v1/5e669116eea473063ca33484/1657915819906-KO3AMOTQDSPBFHLRYH1W/070822lsc102.jpg?format=2500w', 
        'description': 'A historic auction house located on Lake Street, known for its rare and valuable antiques.',
        'category': 'Historic',
        'sale_date': '2024-10-28',  
        'end_date': '2024-10-30',
        
        'bids': [
            {'name': 'Charlie Baker', 'amount': 160000, 'comment': 'A beautiful piece that is worth the price.'},
            {'name': 'Jessica Rivera', 'amount': 165000, 'comment': 'Simply exquisite!'},
            {'name': 'Liam Carter', 'amount': 170000, 'comment': 'Ive been waiting for something like this for years.'}
        ]
    },
    {
        'id': 2,
        'title': 'UMN Auction House',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/UMN-EddyHall.jpg/220px-UMN-EddyHall.jpg',
        'description': 'A modern auction house affiliated with the University of Minnesota, specializing in contemporary art and design.',
        'category': 'Modern',
        'sale_date': '2024-11-20',  
        'end_date': '2024-11-29', 
        
        'bids': [
            {'name': 'bobby Jackson', 'amount': 45, 'comment': 'maybe.'},
            {'name': 'Olivia Martinez', 'amount': 195000, 'comment': 'A rare gem that I must own!'},
            {'name': 'Sophia Davis', 'amount': 200000, 'comment': 'Absolutely stunning.'},
            {'name': 'Jack Wilson', 'amount': 205000, 'comment': 'I can already imagine this in my collection.'},
            {'name': 'Jack Black', 'amount': 205001, 'comment': 'this is for me.'}
        ]
    },
    {
        'id': 3,
        'title': 'Minnhaha Auction House',
        'image_url': 'https://www.architectureinc.com/hubfs/Architecture_Incorporated_May2021/Images/1_Minnehaha_Co_Courthouse.jpg',
        'description': 'A renowned modern auction house located near Minnehaha Falls, offering a diverse selection of contemporary collectibles and art pieces.',
        'category': 'Modern',
        'sale_date': '2024-12-01',  
        'end_date': '2024-12-12',  
       
        'bids': [
            {'name': 'David Thompson', 'amount': 130000, 'comment': 'A brilliant addition to my collection.'},
            {'name': 'Dillan Clark', 'amount': 134000, 'comment': 'The craftsmanship is amazing.'},
            {'name': 'Emily Clark', 'amount': 135000, 'comment': 'The craftsmanship is unmatched.'},
            {'name': 'Henry Ford', 'amount': 140000, 'comment': 'This will definitely be the centerpiece of my home.'}
        ]
    },
    {
        'id': 4,
        'title': 'New-prauge Auction House',
        'image_url': 'https://thumbs.dreamstime.com/z/random-building-asheville-north-carolina-usa-taken-december-67611951.jpg?ct=jpeg',
        'description': 'An upscale auction house in New Prague, specializing in luxury items including rare jewelry, fine art, and exclusive collectibles.',
        'category': 'Luxery',
        'sale_date': '2024-11-05',  
        'end_date': '2024-11-22',  
        
        'bids': [
            {'name': 'Alice Johnson', 'amount': 175000, 'comment': 'A masterpiece, worth every penny!'},
            {'name': 'Michael Lee', 'amount': 180000, 'comment': 'Excited to add this to my gallery.'},
            {'name': 'Samantha Green', 'amount': 185000, 'comment': 'A true investment piece for the future.'},
            {'name': 'Alice John', 'amount': 195000, 'comment': 'worth every penny!'},
            {'name': 'Michael laeah', 'amount': 380000, 'comment': 'wow its a great gallery.'},
            {'name': 'Samantha brown', 'amount': 485000, 'comment': 'I have this in the bag.'}
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


def parse_query_parameters(partponse):
    pairs = partponse.split('&')
    storedPares = {}

    for pair in pairs:
        if '=' in pair:  
            key, value = pair.split('=')  
            storedPares[key] = value.replace('+', ' ')
        else:
            storedPares["q"] = ""
            storedPares["Categories"] = "All"
    return storedPares

def render_listing(listing):
    listing_html = f"""
    <html>
    <head>
        <title>{escape_html(listing['title'])}</title>
        <link rel="stylesheet" href="/main.css">
        <script>
            function openForm() {{
                document.getElementById("myForm").style.display = "block";
            }}

            function closeForm() {{
                document.getElementById("myForm").style.display = "none";
            }}
        </script>
    </head>
    <body>
        <div>
            <nav id="navbar">
                <ul id="main-nav">
                    <li><a href="/">About Us</a></li>
                    <li><a href="/gallery">Gallery</a></li>
                    <li><a href="/create">Add Listing</a></li>
                </ul>
                <form action="" method="GET" id="search-form">
                    <input name="q" type="search" aria-label="Search">
                    <select name="category" id="category-select">
                        <option value="All">All Categories</option>
                        <option value="Historic">Historic</option>
                        <option value="Modern">Modern</option>
                        <option value="Luxury">Luxury</option>
                    </select>
                    <input type="submit" name="search" id="search-btn" value="Search">
                </form>
            </nav>
        </div>
        <h1>{escape_html(listing['title'])}</h1>
        <div class="content">
            <div class="left-column">
                <img src="{listing['image_url']}" alt="{escape_html(listing['title'])}" class="product-image">
                <div class="description-box">
                    <p><strong>Description:</strong> {escape_html(listing['description'])}</p>
                    <p><strong>Category:</strong> {escape_html(listing['category'])}</p>
                    <p><strong>Sale Date:</strong> {listing['sale_date']}</p>
                </div>
            </div>
            <div class="right-column">
                <div class="bids-header-container">
                    <h2 class="bids-header">Bids</h2> 
                    <button class="place-bid-btn" onclick="openForm()">Place Bid</button> <!-- Corrected onclick function -->
                </div>
                 <div class="form-popup" id="myForm" style="display: none;">
                        <form action="/place_bid" method "POST" class="form-container">
                            <p>Place Your Bid</p> 

                            <label for="name"><b>Your Name</b></label>
                            <input type="text" placeholder="Enter Name" name="name" required>

                            <label for="amount"><b>Amount:</b></label>
                            <input type="text" placeholder="Enter Amount" name="amount" required>

                            <label for="comment"><b>Comment:</b></label> 
                            <input type="text" placeholder="Enter a Comment" name="comment" required>

                            <button type="submit" class="btn">Submit Bid</button> 
                            <button type="button" class="btn cancel" onclick="closeForm()">Close</button>
                        </form>
                    </div>
                <ul>
    """

    for bid in listing['bids']:
        listing_html += f"""
            <li class="bid-box">
                <span class="bidder-name"><strong>{escape_html(bid['name'])}</strong></span><br>
                <span class="bid-amount">{typeset_dollars(bid['amount'])}</span>
                <p class="bid-comment">{escape_html(bid['comment'])}</p>
            </li>
        """

    listing_html += """
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

    return listing_html


def render_gallery(query, category):
    gallery_html = """
    <html>
    <head>
        <title>Auction Gallery</title>
        <link rel="stylesheet" href="/main.css">
    </head>
    <body>
        <div>
            <nav id="navbar">
                <ul id="main-nav">
                    <li><a href="/">About Us</a></li>
                    <li><a href="/gallery">Gallery</a></li>
                    <li><a href="/create">Add Listing</a></li>
                </ul>
                <form action="" method="GET" id="search-form">
                    <input name="q" type="search" aria-label="Search">
                    <select name="category" id="category-select">
                        <option value="All">All Categories</option>
                        <option value="Historic">Historic</option>
                        <option value="Modern">Modern</option>
                        <option value="Luxury">Luxury</option>
                    </select>
                    <input type="submit" name="search" id="search-btn" value="Search">
                </form>
            </nav>
        </div>
        <h1>Auction House Gallery</h1>
        <table class="gallery-table">
            <tr>
                <th>Listing</th>
                <th>Number of Bids</th>
                <th>Category</th>
                <th>Top Bid</th>
                <th>Sale Date</th>
                <th>Auction Ends</th>
            </tr>
    """

    filtered_listings = listings

    if query:
        filtered_listings = [listing for listing in listings if query.lower() in listing['title'].lower()]

    if category != "All":
        filtered_listings = [listing for listing in filtered_listings if listing['category'] == category]

    if not filtered_listings:
        gallery_html += """
            <tr>
                <td colspan="6">No listings found.</td>
            </tr>
        """
    else:
        for listing in filtered_listings:
            num_bids = len(listing['bids'])
            top_bid = max([bid['amount'] for bid in listing['bids']], default=0)  # Use default=0 if no bids
            gallery_html += f"""
            <tr>
                <td><a href="/listing/{listing['id']}">{listing['title']}</a></td>
                <td>{num_bids}</td>
                <td>{listing['category']}</td>
                <td>{typeset_dollars(top_bid)}</td>
                <td>{listing['sale_date']}</td>
                <td>{listing['end_date']}</td>
            </tr>
            """
            # If you want to show the image for each listing, you can do it here.
            # If you only want to show one image, you should handle it outside the loop.
            gallery_html += f"""
            <tr>
                <td colspan="6" class="hover_img">
                    <img src="{listing['image_url']}" class="image_switcher" alt="{listing['title']}">
                </td>
            </tr>
            """

    gallery_html += """
        </table>
    </body>
    </html>
    """

    return gallery_html




# Provided function -- converts numbers like 42 or 7.347 to "$42.00" or "$7.35"
def typeset_dollars(number):
    return f"${number:.2f}"

def add_new_listing(params): 
    print(params)
    required_fields = ["title-form", "Image-form", "Descript-form", "Categories-form", "sale-Form"]
    for field in required_fields:
        if field not in params or not params[field]:
            return False  # Missing field



    new_id = max([listing["id"] for listing in listings]) + 1 if listings else 1
    new_listing = {
        "id": new_id,
        "title": params["title-form"],
        "image_url": params["Image-form"],
        "description": params["Descript-form"],
        "category": params["Categories-form"] ,
        "sale_date": "10/23/2024",
        "end_date": params["sale-Form"],
    }

    listings.append(new_listing)
    return True

def add_new_bid(params):
    listing_id = int(params.get("listing_id", -1))
    # Validate listing ID and other fields
    listing = next((lst for lst in listings if lst["id"] == listing_id), None)
    if not listing or not params.get("name") or not params.get("amount"):
        return False  # Missing fields or invalid listing

    bid_amount = float(params["amount"])
    if bid_amount <= max([bid["amount"] for bid in listing.get("bids", [])], default=0):
        return False  # Bid too low

    new_bid = {
        "name": params["name"],
        "amount": bid_amount,
        "comment": params.get("comment", "")
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

    elif path == "/main.css":
        return open("static/css/main.css", "r").read(), "text/css", 200

    if path == "/images/main":
        return open("static/images/project_image.jpeg", "rb").read(), "image/jpeg", 200
    
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
    
    if path == "/bid.js": 
        return open("static/js/bid.js").read(), "application/js", 200
    
    if path == "/new_listing.js": 
        return open("static/js/new_listing.js").read(), "application/js", 200

    if path == "/table.js": 
        return open("static/js/table.js").read(), "application/js", 200
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

    elif path == "/create":
        print("this should work")
        if add_new_listing(adding_new_lst):  
            return open("static/html/create_success.html").read(), 'text/html', 201
        else:
            return open("static/html/create_fail.html").read(), 'text/html', 400

    elif path == "/place_bid":
        if add_new_bid(adding_new_bid):
            return open("static/html/create_success.html").read(), 'text/html', 201
        else:
            return open("static/html/create_fail.html").read(), 'text/html', 400

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
