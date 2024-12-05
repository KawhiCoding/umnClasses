const express = require('express');
const path = require('path');
//const cookesParser = require('cookie-parser');
const app = express();
const PORT = 4131;

app.set('views', path.join(__dirname, 'static', 'templates'));
app.set('view engine', 'pug'); 


app.use(express.json());
app.use(express.urlencoded({ extended: false }));
//app.use(cookesParser());
app.use('/css', express.static(path.join(__dirname, 'static', 'resources', 'css')));
app.use('/js', express.static(path.join(__dirname, 'static', 'resources', 'js')));
app.use('/images', express.static(path.join(__dirname, 'static', 'resources', 'images')));


app.use(express.static('static'));

const images = [
    {
        title: 'Meerkat',
        image: 'meerkat.jpg',
        description: 'bravard county zoon in florida',
        category: 'nature',
        id: 1,
        uoload_date: '2024-12-15 12:00',  
        image_comments: [
            {User: 'James Rodriguez', comment: 'Very cute.'},
            {User: 'Emily Chen', comment: 'what is there story.'},
            {User: 'William Carter', comment: 'I won\'t stop until these are mine.'},  
        ]
    },
    {
        title: 'flamingo',
        image: 'bird.jpg',
        description: 'The iconic Air Jordan Ones that were banned from the NBA. A piece of sneaker history.',
        category: 'nature',
        id: 1,
        uoload_date: '2024-12-15 12:00',  
        image_comments: [
            {User: 'James Rodriguez', comment: 'An absolute must-have for any collector.'},
            {User: 'Emily Chen', comment: 'The story behind these shoes makes them priceless.'},
            {User: 'William Carter', comment: 'I won\'t stop until these are mine.'},  
        ]
    }
]

app.get(['/', '/main'], (req, res) => {
    res.render('mainpage');
});

app.get('/gallery', (req, res) => {
    res.render('gallery', { images: images });
});

app.get('/create', (req, res) => {
    res.render('create');
});

app.get('/contact', (req, res) => {
    res.render('contact');
});

app.post('/contact', (req, res) => {
    const { first_name, last_name, email, subject, message } = req.body;

    console.log('Contact Form Submission:');
    console.log(`First Name: ${first_name}`);
    console.log(`Last Name: ${last_name}`);
    console.log(`Email: ${email}`);
    console.log(`Subject: ${subject}`);
    console.log(`Message: ${message}`);

    res.send('Thank you for contacting us! We will get back to you shortly.');
});

function typeset_dollars(amount) {
    return `$${amount.toFixed(2)}`;
}



app.use((req, res) => {
    res.status(404).render('404');
});





app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});