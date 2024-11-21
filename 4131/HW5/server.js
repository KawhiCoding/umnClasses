const express = require('express');
const path = require('path');
//const cookesParser = require('cookie-parser');
const app = express();
const PORT = 4131;

app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'static', 'templates'));


app.use(express.json());
app.use(express.urlencoded({ extended: false }));
//app.use(cookesParser());
app.use('/css', express.static(path.join(__dirname, 'static', 'resources', 'css')));
app.use('/js', express.static(path.join(__dirname, 'static', 'resources', 'js')));
app.use('/images', express.static(path.join(__dirname, 'static', 'resources', 'images')));


app.use(express.static('static'));

const listings = [
    {
        title: 'Banned Air Jordan Ones',
        image: 'https://m.media-amazon.com/images/I/7137GjFiZ6L._AC_SY395_.jpg',
        description: 'The iconic Air Jordan Ones that were banned from the NBA. A piece of sneaker history.',
        category: 'sports',
        id: 1,
        sale_date: '2024-12-15 12:00',  
        end_date: '2024-11-15 18:00',
        bids: [
            {bidder: 'James Rodriguez', amount: 50000, comment: 'An absolute must-have for any collector.'},
            {bidder: 'Emily Chen', amount: 52000, comment: 'The story behind these shoes makes them priceless.'},
            {bidder: 'William Carter', amount: 54000, comment: 'I won\'t stop until these are mine.'},  
        ]
    },
    {
        title: 'Back to the Future Nike Shoes',
        image: 'https://www.hollywoodreporter.com/wp-content/uploads/2019/07/nike-publicity-h_2019.jpg?w=1296&h=730&crop=1',
        description: 'The self-lacing Nike Mag from Back to The Future, a perfect blend of movie memorabilia and futuristic fashion.',
        category: 'actors',
        id: 2,
        sale_date: '2024-12-15 12:00',  
        end_date: '2024-11-12 20:30',
        bids: [
            {bidder: 'Sarah Johnson', amount: 120000, comment: 'These are a dream come true!'},
            {bidder: 'Lucas Brown', amount: 125000, comment: 'Can\'t let this piece of nostalgia slip away.'},  
            {bidder: 'Ava Clark', amount: 130000, comment: 'A true collector\'s item.'},  
            {bidder: 'Joe Clark', amount: 1300000, comment: 'A true item.'} 
        ]
    },
    {
        title: 'Michael Jackson\'s Dance Shoes',
        image: 'https://external-preview.redd.it/3eal1lLVFglo657rVhdHecbOHu2yX8zyBFxII12IcaI.jpg?auto=webp&s=ca8ee13b158be85f58692410dc3962dbd27099f5',
        description: 'The iconic shoes worn by Michael Jackson when he unveiled the Moonwalk.',
        category: 'music',
        id: 3,
        sale_date: '2024-12-15 12:00',  
        end_date: '2024-11-10 22:00',
        bids: [
            {bidder: 'Mia Wilson', amount: 100000, comment: 'An essential piece of pop culture history.'},
            {bidder: 'Ethan Lee', amount: 105000, comment: 'It would be an honor to own these.'},
            {bidder: 'Sophia Martinez', amount: 110000, comment: 'These shoes have so much legacy behind them.'}
        ]
    },
    {
        title: 'Mike Tyson\'s Final Boxing Shoes',
        image: 'https://minotaurclothing.co.uk/wp-content/uploads/2022/10/The-Mike-Tyson-look-Boot.jpg',
        description: 'The shoes worn by Mike Tyson in his final professional boxing match. A tribute to a legendary career.',
        category: 'sports',
        id: 4,
        sale_date: '2024-12-15 12:00',  
        end_date: '2024-11-18 16:00',
        bids: [
            {bidder: 'Daniel Thompson', amount: 60000, comment: 'A fitting tribute to an incredible fighter.'},
            {bidder: 'Ella Rivera', amount: 62000, comment: 'The perfect piece for any Tyson fan.'},
            {bidder: 'Jacob Harris', amount: 64000, comment: 'These shoes are worth every penny.'}
        ]
    }
]

app.get(['/', '/main'], (req, res) => {
    res.render('mainpage');
});

app.get('/gallery', (req, res) => {
    res.render('gallery', { listings, typeset_dollars });
});

function typeset_dollars(amount) {
    return `$${amount.toFixed(2)}`;
}

app.get('/listing/:id', (req, res) => {
    const listing = listings.find(listing => listing.id === parseInt(req.params.id));
    if (listing) {
        // Pass both the listing and typeset_dollars function to the Pug template
        res.render('listing', { listing, typeset_dollars });
    } else {
        res.status(404).render('404');
    }
});

//if successful, redirect to confirmation.pug if not redirect to error.pug 
app.get('/create', (req, res) => {
    res.render('create');
});

app.post('/create', (req, res) => {
    console.log(req.body);  // Log the body of the request to see the data
    const { title, image, description, category, sale_date, end_date } = req.body;
    
    // Validate data
    if (title && image && description && category && sale_date && end_date) {
        listings.push({
            title,
            image,
            description,
            category,
            id: listings.length + 1,
            sale_date,
            end_date,
            bids: []
        });
        res.redirect('/confirmation');
    } else {
        console.log("Missing data");  // Log error if data is missing
        res.redirect('/error');
    }
});


app.get('/confirmation', (req, res) => {
    res.render('confirmation');
});

app.get('/error', (req, res) => {
    res.render('error');
});

app.delete('/api/delete_listing', (req, res) => {
    const { listing_id } = req.body;
    const index = listings.findIndex(listing => listing.id === parseInt(listing_id));
    
    if (index !== -1) {
        listings.splice(index, 1);  // Remove the listing from the array
        res.status(204).send();  // No content, successful delete
    } else {
        res.status(400).send("Listing not found.");
    }
});


app.use((req, res) => {
    res.status(404).render('404');
});





app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});