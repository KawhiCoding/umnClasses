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

[print(parse_query_parameters("?color=%237766a9&mood=hate+it+it&name=buloova"))]