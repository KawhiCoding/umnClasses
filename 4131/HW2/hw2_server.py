from http.server import BaseHTTPRequestHandler, HTTPServer
import re

listings = [
     {
        'id': 1,
        'title': 'Lake Street Auction House',
        'image_url': 'https://images.squarespace-cdn.com/content/v1/5e669116eea473063ca33484/1657915819906-KO3AMOTQDSPBFHLRYH1W/070822lsc102.jpg?format=2500w', 
        'description': 'A historic auction house located on Lake Street, known for its rare and valuable antiques.',
        'category': 'Historic',
        'sale_date': '2024-10-28',  
        'end_date': '2024-11-04',   
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
        'end_date': '2024-11-27',   
        'bids': [
            {'name': 'Olivia Martinez', 'amount': 195000, 'comment': 'A rare gem that I must own!'},
            {'name': 'Sophia Davis', 'amount': 200000, 'comment': 'Absolutely stunning.'},
            {'name': 'Jack Wilson', 'amount': 205000, 'comment': 'I can already imagine this in my collection.'}
        ]
    },
    {
        'id': 3,
        'title': 'Minnhaha Auction House',
        'image_url': 'https://www.architectureinc.com/hubfs/Architecture_Incorporated_May2021/Images/1_Minnehaha_Co_Courthouse.jpg',
        'description': 'A renowned modern auction house located near Minnehaha Falls, offering a diverse selection of contemporary collectibles and art pieces.',
        'category': 'Modern',
        'sale_date': '2024-12-01',  
        'end_date': '2024-12-08',  
        'bids': [
            {'name': 'David Thompson', 'amount': 130000, 'comment': 'A brilliant addition to my collection.'},
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
        'end_date': '2024-11-12',   
        'bids': [
            {'name': 'Alice Johnson', 'amount': 175000, 'comment': 'A masterpiece, worth every penny!'},
            {'name': 'Michael Lee', 'amount': 180000, 'comment': 'Excited to add this to my gallery.'},
            {'name': 'Samantha Green', 'amount': 185000, 'comment': 'A true investment piece for the future.'}
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
    </head>
    <body>
        <div>
            <nav>
                <ul>
                    <li id="aboutUsNav"><a href="/">About us</a></li>
                    <li id="galleryNav"><a href="/gallery">Gallery</a></li>
                    <li>
                        <form action="" method="GET">
                            <input name="q" type="search" placeholder="Search...">
                            <select name="Categories" id="Categories">
                                <option value="All">All Categories</option>
                                <option value="Historic">Historic</option>
                                <option value="Modern">Modern</option>
                                <option value="Luxery">Luxery</option>
                            </select>
                            <input type="submit" name="search" id="searchbtn" value="Search">
                        </form>
                    </li>
                </ul>
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
                    <p><strong>End Date:</strong> {listing['end_date']}</p>
                </div>
            </div>
            <div class="right-column">
                <h2>Bids</h2>
                <ul>
    """

    for bid in listing['bids']:
        listing_html += f"""
            <li class="bid-box">
                <span class="bidder-name">{escape_html(bid['name'])}</span>
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
            <nav>
                <ul>
                    <li id="aboutUsNav"><a href="/">About us</a></li>
                    <li id="galleryNav"><a href="/gallery">Gallery</a></li>
                    <li>
                        <form action="" method="GET">
                            <input name="q" type="search" placeholder="Search...">
                            <select name="Categories" id="Categories">
                                <option value="All">All Categories</option>
                                <option value="Historic">Historic</option>
                                <option value="Modern">Modern</option>
                                <option value="Luxury">Luxury</option>
                            </select>
                            <input type="submit" id="searchbtn">
                        </form>
                    </li>
                </ul>
            </nav>
        </div>
        <h1>Auction House Gallery</h1>
        <table class="gallery-table">
            <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Category</th>
                <th>Sale Date</th>
                <th>End Date</th>
            </tr>
    """

    if not query and category == "All":
        for listing in listings:
            gallery_html += f"""
                <tr>
                    <td><a href="/listing/{listing['id']}">{listing['title']}</a></td>
                    <td>{listing['description']}</td>
                    <td>{listing['category']}</td>
                    <td>{listing['sale_date']}</td>
                    <td>{listing['end_date']}</td>
                </tr>
            """
    else:
        filtered_listings = [listing for listing in listings if query.lower() in listing['title'].lower()] if query else listings.copy()

        if category != "All":
            filtered_listings = [listing for listing in filtered_listings if listing['category'] == category]

        for listing in filtered_listings:
            gallery_html += f"""
                <tr>
                    <td><a href="/listing/{listing['id']}">{listing['title']}</a></td>
                    <td>{listing['description']}</td>
                    <td>{listing['category']}</td>
                    <td>{listing['sale_date']}</td>
                    <td>{listing['end_date']}</td>
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


def server(url):
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe#test`
    then the `url` parameter will have the value "/contact?name=joe". So you can expect the PATH
    and any PARAMETERS from the url, but nothing else.

    This function is called each time another program/computer makes a request to this website.
    The URL reppartents the requested file.

    This function should return two strings in a list or tuple. The first is the content to return
    The second is the content-type.
    """
    # YOUR CODE GOES HERE!
    path = url

    query = ""
    if "?" in url:
        path, query = path.split("?")

    if path == "/" or path == "/main":
        return open("static/html/mainpage.html").read(),'text/html'

    elif path == "/gallery":
        var = parse_query_parameters(query)
        print(var)
        gallery_var = None
        category_var = None
        if len(var) >= 2:
            gallery_var = var['q']
            category_var = var['Categories']
        return render_gallery(gallery_var ,category_var),'text/html'

    elif path == "/main.css":
        return open("static/css/main.css", "r").read(), "text/css"

    if path == "/images/main":
        return open("static/images/project_image.jpeg", "rb").read(), "image/jpeg"
    
    elif path.startswith("/listing/"):
        part = None
        listings_id = path[9:]
        for listing in listings:
            if int(listing["id"]) == int(listings_id):
                part = listing
                break
        return render_listing(part), "text/html"
        
    else:
        return open("static/html/404.html").read(),'text/html'


# You shouldn't need to change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the student-edited server code.
        message, content_type = server(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(200)
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
