const express = require('express');
const path = require('path');
const { title } = require('process');
const cookieParser = require('cookie-parser');
const app = express();
const PORT = 4131;

app.set('views', path.join(__dirname, 'static', 'templates'));
app.set('view engine', 'pug'); 


app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use('/css', express.static(path.join(__dirname, 'static', 'resources', 'css')));
app.use('/js', express.static(path.join(__dirname, 'static', 'resources', 'js')));
app.use('/images', express.static(path.join(__dirname, 'static', 'resources', 'images')));


app.use(express.static('static'));

function typeset_dollars(amount) {
    return `$${amount.toFixed(2)}`;
}

const projects = [
    {
        title: 'Fix Toilet',
        status: 'Not Done',
        description: 'Repair the leaking toilet in the main bathroom.',
        category: 'repair',
        id: 1,
        deadline: '2024-12-20 12:00',
        Comments: [
            {User: 'James Rodriguez', comment: 'I will buy the necessary parts.'},
            {User: 'Emily Chen', comment: 'I can help with the installation.'},
        ]
    },
    {
        title: 'Install New TV',
        status: 'Not Done',
        description: 'Mount the new TV in the living room and set up the sound system.',
        category: 'improvement',
        id: 2,
        deadline: '2024-10-25 15:00',
        Comments: [
            {User: 'Alice Johnson', comment: 'I will handle the wiring.'},
            {User: 'Bob Smith', comment: 'I can help with the mounting.'},
        ]
    },
    {
        title: 'Fix Garage Door',
        status: 'Not Done',
        description: 'Repair the garage door that is not closing properly.',
        category: 'repair',
        id: 3,
        deadline: '2024-12-05 10:00',
        Comments: [
            {User: 'Charlie Brown', comment: 'I will check the sensors.'},
        ]
    },
    {
        title: 'Paint Bedroom',
        status: 'Not Done',
        description: 'Paint the master bedroom with a new color.',
        category: 'improvement',
        id: 4,
        deadline: '2024-12-15 09:00',
        Comments: [
            {User: 'David Wilson', comment: 'I will buy the paint and brushes.'},
            {User: 'Eva Green', comment: 'I can help with the painting.'},
        ]
    },
    {
        title: 'Re-organize Basement',
        status: 'Done',
        description: 'Sort and organize items in the basement.',
        category: 'organization',
        id: 5,
        deadline: '2024-12-01 14:00',
        Comments: [
            {User: 'Frank Miller', comment: 'I will bring storage boxes.'},
            {User: 'Grace Lee', comment: 'I can help with sorting items.'},
        ]
    },
    {
        title: 'Organize Kitchen Pantry',
        status: 'Done',
        description: 'Clean and organize the kitchen pantry.',
        category: 'organization',
        id: 6,
        deadline: '2024-12-10 11:00',
        Comments: [
            {User: 'Hannah White', comment: 'I will buy new containers.'},
            {User: 'Ian Black', comment: 'I can help with labeling.'},
        ]
    }
];

app.get(['/', '/main'], (req, res) => {
    res.render('mainpage');
});

app.get('/projects', (req, res) => {
    res.render('projects', {projects});
});

app.get('/projects/:id', (req, res) => {
    const project = projects.find(project => project.id === parseInt(req.params.id));
    if (project) {
        res.render('projectLst', { project });
    } else {
        res.status(404).render('404');
    }
});


app.get('/create', (req, res) => {
    res.render('create');
});

app.post('/create', (req, res) => { 
    const { title, status, description, category, deadline } = req.body;
    const id = projects.length + 1;
    projects.push({ title, status, description, category, id, deadline });
    res.redirect('/projects');
});

app.get('/profile', (req, res) => {
    res.render('profile');
});

app.get('/logout', (req, res) => {
    res.redirect('/main');
});


app.delete('/api/delete_project', (req, res) => {
    const { project_id } = req.body;
    const index = projects.findIndex(project => project.id === parseInt(project_id));
    
    if (index !== -1) {
        projects.splice(index, 1);  
        res.status(204).send();  
    } else {
        res.status(400).send("Project not found.");
    }
});

app.put('/api/update_status', (req, res) => {
    const { project_id, status } = req.body;
    const project = projects.find(project => project.id === parseInt(project_id));
    
    if (project) {
        project.status = status;
        res.status(204).send();
    } else {
        res.status(400).send("Project not found.");
    }
});

app.use((req, res) => {
    res.status(404).render('404');
});


app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});