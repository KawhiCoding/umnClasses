from http.server import BaseHTTPRequestHandler, HTTPServer
import re

listings = [
    {
        'title': 'Banned Air Jordan Ones',
        'image': 'https://m.media-amazon.com/images/I/7137GjFiZ6L._AC_SY395_.jpg',
        'description': 'The iconic Air Jordan Ones that were banned from the NBA. A piece of sneaker history.',
        'category': 'sports',
        'id': 1,
        'sale_date': '2024-12-15 12;00',
        'end_date': '2024-11-15 18:00',
        'bids': [
            {'bidder': 'James Rodriguez', 'amount': 50000, 'comment': 'An absolute must-have for any collector.'},
            {'bidder': 'Emily Chen', 'amount': 52000, 'comment': 'The story behind these shoes makes them priceless.'},
            {'bidder': 'William Carter', 'amount': 54000, 'comment': 'I wont stop until these are mine.'},
            {'bidder': 'James Rodriguez', 'amount': 50000, 'comment': 'An absolute must-have for any collector.'},
            {'bidder': 'Emily Chen', 'amount': 52000, 'comment': 'The story behind these shoes makes them priceless.'},
            {'bidder': 'William Carter', 'amount': 54000, 'comment': 'I wont stop until these are mine.'}
        ]
    },
    {
        'title': 'Back to the Future Nike Shoes',
        'image': 'https://www.hollywoodreporter.com/wp-content/uploads/2019/07/nike-publicity-h_2019.jpg?w=1296&h=730&crop=1',
        'description': 'The self-lacing Nike Mag from Back to The Future, a perfect blend of movie memorabilia and futuristic fashion.',
        'category': 'actors',
        'id': 2,
        'sale_date': '2024-12-15 12;00',
        'end_date': '2024-11-12 20:30',
        'bids': [
            {'bidder': 'Sarah Johnson', 'amount': 120000, 'comment': 'These are a dream come true!'},
            {'bidder': 'Lucas Brown', 'amount': 125000, 'comment': 'Cant let this piece of nostalgia slip away.'},
            {'bidder': 'Ava Clark', 'amount': 130000, 'comment': 'A true collectors item.'},
            {'bidder': 'joe Clark', 'amount': 1300000, 'comment': 'A true item.'}
        ]
    },
    {
        'title': 'Michael Jacksons Dance Shoes',
        'image': 'https://external-preview.redd.it/3eal1lLVFglo657rVhdHecbOHu2yX8zyBFxII12IcaI.jpg?auto=webp&s=ca8ee13b158be85f58692410dc3962dbd27099f5',
        'description': 'The iconic shoes worn by Michael Jackson when he unveiled the Moonwalk.',
        'category': 'music',
        'id': 3,
        'sale_date': '2024-12-15 12;00',
        'end_date': '2024-11-10 22:00',
        'bids': [
            {'bidder': 'Mia Wilson', 'amount': 100000, 'comment': 'An essential piece of pop culture history.'},
            {'bidder': 'Ethan Lee', 'amount': 105000, 'comment': 'It would be an honor to own these.'},
            {'bidder': 'Sophia Martinez', 'amount': 110000, 'comment': 'These shoes have so much legacy behind them.'}
        ]
    },
    {
        'title': 'Mike Tysons Final Boxing Shoes',
        'image': 'https://minotaurclothing.co.uk/wp-content/uploads/2022/10/The-Mike-Tyson-look-Boot.jpg',
        'description': 'The shoes worn by Mike Tyson in his final professional boxing match. A tribute to a legendary career.',
        'category': 'sports',
        'id': 4,
        'sale_date': '2024-12-15 12;00',
        'end_date': '2024-11-18 16:00',
        'bids': [
            {'bidder': 'Daniel Thompson', 'amount': 60000, 'comment': 'A fitting tribute to an incredible fighter.'},
            {'bidder': 'Ella Rivera', 'amount': 62000, 'comment': 'The perfect piece for any Tyson fan.'},
            {'bidder': 'Jacob Harris', 'amount': 64000, 'comment': 'These shoes are worth every penny.'}
        ]
    }
]


# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.


def escape_html(str):
    str = str.replace("&", "&amp;")
    str = str.replace('"', "&quot;")
    str = str.replace(">", "&gt;")
    str = str.replace('"', "&quot;")
    str = str.replace("'", "&#39;") 
    return str


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
    </head>
    <body>
        <nav>
            <ul class="NavBar">
                <li><a href="/main">About Us</a></li>
                <li><a href="/gallery">Gallery</a></li>
                <li><a href="/add_listing">Add Listing</a></li>

                <form action="" method="GET" class="NavBar">
                    <label for="seachBar"></label>
                    <input type="search" name="seachBar" id="seachBar">

                    <label for="dropDown"></label>
                    <select name="dropDown" id="dropDown">
                        <option value="all">All Categorys</option>
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
                        <img src="{listing['image']}" alt="{escape_html(listing['title'])}" class="product-image">
                        <div class="description-box">
                            <p>{escape_html(listing['description'])}</p>
                        </div>
                    </div>
                    <div class="column">
                        <h2>Bids</h2>
                        <ul>
                        <div class="line"></div>
                        """
    for bid in listing['bids']:
        listing_html += f"""
            <li class="bid-box">
                <span class="bidder-name">{escape_html(bid['bidder'])}</span>
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
    gallery = f"""  
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Historical Shoes Auction</title>
        <link href="main.css" rel="stylesheet">
    </head>
    <body>
        <nav>
            <ul class="NavBar">
                <li><a href="/main">About Us</a></li>
                <li><a href="/gallery">Gallery</a></li>
                <li><a href="/add_listing">Add Listing</a></li>

                <form action="" method="GET" class="NavBar">
                    <input type="search" name="q" id="seachBar">
                    <select name="Categories" id="Categories">
                        <option value="All">All Categorys</option>
                        <option value="sports">Sports</option>
                        <option value="actors">Actors/Movie</option>
                        <option value="music">Music</option>
                    </select>
                    
                    <input type="submit" id="submit_btn">
                </form>
            </ul>
        </nav>

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
            if listing['bids']:
                top_bid = typeset_dollars(listing['bids'][-1]['amount'])
            else:
                top_bid = "$0.00"
            gallery += f"""
                <tr>
                    <td><a href="/listing/{listing['id']}">{listing['title']}</a></td>
                    <td>{len(listing['bids'])}</td>
                    <td>{listing['category']}</td>
                    <td>{top_bid}</td>
                    <td>{listing['sale_date']}</td>
                    <td>{listing['end_date']}</td>
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
                <tr>
                    <td><a href="/listing/{listing['id']}">{listing['title']}</a></td>
                    <td>{len(listing['bids'])}</td>
                    <td>{listing['category']}</td>
                    <td>{top_bid}</td>
                    <td>{listing['sale_date']}</td>
                    <td>{listing['end_date']}</td>
                </tr>
            """

    gallery += """
        </table>
    </body>
    </html>
    """

    return gallery



# Provided function -- converts numbers like 42 or 7.347 to "$42.00" or "$7.35"
def typeset_dollars(number):
    return f"${number:.2f}"


def server(url):
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe#test`
    then the `url` parameter will have the value "/contact?name=joe". So you can expect the PATH
    and any PARAMETERS from the url, but nothing else.

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return two strings in a list or tuple. The first is the content to return
    The second is the content-type.
    """
    
    path = url
    query = ""
    if "?" in url:
        path, query = url.split("?")

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
    
    elif path.startswith("/listing/"):
        part = None
        listings_id = path[9:]
        for listing in listings:
            if int(listing["id"]) == int(listings_id):
                part = listing
                break
        return render_listing(part), "text/html"

    elif path == "/main.css":
        return open("static/css/main.css", "r").read(), "text/css"
    elif path == "/images/main":
        return open("static/images/proj.jpeg", "rb").read(), 'image/jpeg'
    else:
        return open("static/html/404.html").read(), 'text/html'


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
