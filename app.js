const express = require('express');
const sqlite3 = require('sqlite3');
const app = express();
const PORT = 5000;

app.use(express.json());

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

// ... other routes and code ...

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
