const express = require('express');
const sqlite3 = require('sqlite3');
const bodyParser = require('body-parser');  // Add this
const app = express();
const PORT = 5000;
const { exec } = require('child_process');

app.use(express.json());
app.use(bodyParser.urlencoded({ extended: false })); // Add this
app.use(express.static('public')); 

const validDB = new sqlite3.Database('validAddress.db', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        console.error('Error connecting to the SQLite database:', err.message);
    } else {
        console.log('Connected to the validAddress database.');
    }
});

const invalidDB = new sqlite3.Database('invalidAddress.db', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        console.error('Error connecting to the SQLite database:', err.message);
    } else {
        console.log('Connected to the invalidAddress database.');
    }
});

app.get('/invalid', (req, res) => {
    invalidDB.all("SELECT * FROM invalidAddress", [], (err, rows) => {
        if (err) {
            res.status(400).json({"error": err.message});
            return;
        }
        res.json({"invalidAddress": rows});
    });
});

app.get('/valid', (req, res) => {
    validDB.all("SELECT * FROM validAddress", [], (err, rows) => {
        if (err) {
            res.status(400).json({"error": err.message});
            return;
        }
        res.json({"validAddress": rows});
    });
    
});

// Serve the index.html on root
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');

});

app.post('/sold', (req, res) => {
    const query = req.body.query;
    if (!query) {
        return res.status(400).send("Invalid input");
    }

    // Using the LIKE keyword with "%" wildcards to match any sequence of characters before or after the query.
    // The query checks for both "Sold (Public Records)" and "Sold (MLS)" statuses.
    validDB.all(`SELECT * FROM validAddress WHERE city LIKE ? AND (status = "Sold (Public Records)" OR status = "Sold (MLS)" OR status = "Sold" OR status = "Listing Removed" OR status = "Closed" OR status = "Delisted")`, [`%${query}%`], (err, rows) => {
        if (err) {
            return res.status(400).json({"error": err.message});
        }

        if (rows.length === 0){
            res.sendFile(__dirname + '/public/error.html')
        }else {
            res.json(rows);
        }
    });
});

app.post('/active', (req, res) => {
    const query = req.body.query;
    if (!query) {
        return res.status(400).send("Invalid input");
    }

    // Using the LIKE keyword with "%" wildcards to match any sequence of characters before or after the query.
    // The query checks for both "Sold (Public Records)" and "Sold (MLS)" statuses.
    validDB.all(`SELECT * FROM validAddress WHERE city LIKE ? AND (status = "Price Changed" OR status = "Listed" OR status = "Active")`, [`%${query}%`], (err, rows) => {
        if (err) {
            return res.status(400).json({"error": err.message});
        }

        if (rows.length === 0){
            res.sendFile(__dirname + '/public/error.html')
        }else{
            res.json(rows);
        }
    });
});


app.post('/search', (req, res) => {
    const query = req.body.query;

    // Input validation
    if (!query) {
        return res.status(400).send("Invalid input");
    }

    // Specify the columns you want to include, excluding 'id' and 'history'
    // possible columns to select "id,history,address, city, status, statusDate, dataDate"
    const columns = "address, city, status"; 

    validDB.all(`SELECT ${columns} FROM validAddress WHERE city LIKE ?`, [`%${query}%`], (err, rows) => {
        if (err) {
            return res.status(400).json({"error": err.message});
        }

        if (rows.length === 0){
            res.sendFile(__dirname + '/public/error.html')
        } else {
            res.json(rows);
        }
    });
});

//TODO
app.post('/predictions', (req, res) => {
    const query = req.body.query;

    // Input validation
    if (!query) {
        return res.status(400).send("Invalid input");
    }

    // Specify the columns you want to include, excluding 'id' and 'history'
    // possible columns to select "id,history,address, city, status, statusDate, dataDate"
    const columns = "address, city, status"; 

    validDB.all(`SELECT ${columns} FROM validAddress WHERE city LIKE ?`, [`%${query}%`], (err, rows) => {
        if (err) {
            return res.status(400).json({"error": err.message});
        }

        if (rows.length === 0){
            res.sendFile(__dirname + '/public/error.html')
        } else {
            res.json(rows);
        }
    });
});



app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
