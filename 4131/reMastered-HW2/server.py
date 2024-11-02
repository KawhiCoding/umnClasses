from http.server import BaseHTTPRequestHandler, HTTPServer
import re

listings = [
    {
        'title': 'Banned Air Jordan Ones',
        'image': '/static/images/banned_air_jordan_ones.jpg',
        'description': 'The iconic Air Jordan Ones that were banned from the NBA. A piece of sneaker history.',
        'category': 'Sport',
        'id': 1,
        'end_date': '2024-11-15 18:00',
        'bids': [
            {'bidder': 'James Rodriguez', 'amount': 50000, 'comment': 'An absolute must-have for any collector.'},
            {'bidder': 'Emily Chen', 'amount': 52000, 'comment': 'The story behind these shoes makes them priceless.'},
            {'bidder': 'William Carter', 'amount': 54000, 'comment': 'I wont stop until these are mine.'}
        ]
    },
    {
        'title': 'Back to the Future Nike Shoes',
        'image': '/static/images/back_to_the_future_nike.jpg',
        'description': 'The self-lacing Nike Mag from Back to The Future, a perfect blend of movie memorabilia and futuristic fashion.',
        'category': 'Actor',
        'id': 2,
        'end_date': '2024-11-12 20:30',
        'bids': [
            {'bidder': 'Sarah Johnson', 'amount': 120000, 'comment': 'These are a dream come true!'},
            {'bidder': 'Lucas Brown', 'amount': 125000, 'comment': 'Cant let this piece of nostalgia slip away.'},
            {'bidder': 'Ava Clark', 'amount': 130000, 'comment': 'A true collectors item.'}
        ]
    },
    {
        'title': 'Michael Jacksons Dance Shoes',
        'image': '/static/images/michael_jackson_dance_shoes.jpg',
        'description': 'The iconic shoes worn by Michael Jackson when he unveiled the Moonwalk.',
        'category': 'Music',
        'id': 3,
        'end_date': '2024-11-10 22:00',
        'bids': [
            {'bidder': 'Mia Wilson', 'amount': 100000, 'comment': 'An essential piece of pop culture history.'},
            {'bidder': 'Ethan Lee', 'amount': 105000, 'comment': 'It would be an honor to own these.'},
            {'bidder': 'Sophia Martinez', 'amount': 110000, 'comment': 'These shoes have so much legacy behind them.'}
        ]
    },
    {
        'title': 'Mike Tysons Final Boxing Shoes',
        'image': '/static/images/mike_tyson_final_boxing_shoes.jpg',
        'description': 'The shoes worn by Mike Tyson in his final professional boxing match. A tribute to a legendary career.',
        'category': 'Sport',
        'id': 4,
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
        key, value = pair.split("=")
        dict[key] = value.replace('+', ' ' )
    return dict


def render_listing(listing):
    listing_html = f"""  
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Historical Shoes Auction</title>
        <link href="main.css" rel="stylesheet">
    </head>
    <body>
        <div>
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
                            <option value="all">All Categories</option>
                            <option value="sports">Sports</option>
                            <option value="actors">Actors/Movie</option>
                            <option value="music">Music</option>
                        </select>
                        <input type="submit" id="submit_btn">
                    </form>
                </ul>
            </nav>
        </div>

        <div>
            <h1> {listing[title]} </h1>
            
            
        </div>
    </body>
    </html>
    """
    return listing_html 

def render_gallery():
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
        <div>
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
                            <option value="all">All Categories</option>
                            <option value="sports">Sports</option>
                            <option value="actors">Actors/Movie</option>
                            <option value="music">Music</option>
                        </select>
                        <input type="submit" id="submit_btn">
                    </form>
                </ul>
            </nav>
        </div>
        <h1>Gallery</h1>
        <table class="galleryTable">
            <thead>
                <tr>
                    <td>Listing</td>
                    <td>Number of Bids</td>
                    <td>Top Bid</td>
                    <td>Auction End</td>
                </tr>
            </thead>
            <tbody class="tableData">
                <tr>
                    <td><a href="listing/1">Jordan's Flu Shoes</a></td>
                    <td>8</td>
                    <td>20,000</td>
                    <td>8 hours</td>
                </tr>
                <tr>
                    <td>Tiger Woods Championship</td>
                    <td>20</td>
                    <td>10,000</td>
                    <td>6 hours</td>
                </tr>
                <tr>
                    <td>LeBron Game 6</td>
                    <td>3</td>
                    <td>30,000</td>
                    <td>4 hours</td>
                </tr>
                <tr>
                    <td>Hussein Bolt Last Race</td>
                    <td>4</td>
                    <td>9,000</td>
                    <td>4 hours</td>
                </tr>
            </tbody>
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

   
    if "?" in url:
        path = url.split("?")[0]

    elif path == "/" or path == "/main":
        return open("static/html/mainpage.html").read(),'text/html'
    
    elif path == "/gallery":
        return render_gallery(), 'text/html'
    
    elif path == "/listing":
        return render_gallery(), 'text/html'

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
