const express = require('express');
const sqlite3 = require('sqlite3');
const bodyParser = require('body-parser');  // Add this
const app = express();
const PORT = 5000;
const { exec } = require('child_process');

app.use(express.json());
app.use(bodyParser.urlencoded({ extended: false })); // Add this
app.use(express.static('public')); 

const db = new sqlite3.Database('validAddress.db', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        console.error('Error connecting to the SQLite database:', err.message);
    } else {
        console.log('Connected to the SQLite database.');
    }
});

app.get('/valid', (req, res) => {
    db.all("SELECT * FROM validAddress", [], (err, rows) => {
        if (err) {
            res.status(400).json({"error": err.message});
            return;
        }
        res.json({"validAddress": rows});
    });
});

app.get('/setup', (req, res) => {
    exec('python3 setup.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return;
        }
        res.send(stdout);  // This will send the result of the Python script back as the response
    });
});

// Serve the index.html on root
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
app.post('/process-input', (req, res) => {
    const userInput = req.body.userInput;
    console.log("Received user input:", userInput);
    res.send(`You entered: ${userInput}`);
});
