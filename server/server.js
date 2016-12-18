var express = require('express');
var pg = require('pg');
var app = express();
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));

var dbClient = new pg.Client({
    user: process.env.DB_USER || null,
    password: process.env.DB_PASSWORD || null,
    database: process.env.DB_NAME || 5432,
    port: process.env.DB_PORT || null,
    host: process.env.DB_HOST || null,
    ssl: true
});
dbClient.connect();

var port = process.env.PORT || 5050;

var router = express.Router();

router.get('/', function (req, res) {
    res.json({message: 'hooray! welcome to our api!'})
});

router.route('/catalog')
    .get(function(req, res) {

        console.log(req.query.q);

        var searchText = req.query.q.replace('\'', '').replace('\"', '');

        var query = dbClient.query("select p1.* from product p1 left join product p2 on (p1.link = p2.link and p1.timestamp < p2.timestamp) where p2.timestamp is null and lower(p1.title) like lower('%" + searchText + "%');");
        var rows = [];

        query.on('row', function(row) {
            rows.push(row);
        });
        query.on('end', function(result) {
            console.log(result.rowCount + ' rows were received');
            res.json(rows);
        });
    });

router.route('/redirect')
    .get(function(req, res) {
        var url = req.query.url;
        console.log('Redirect to ' + url);
        res.redirect(url);
    });

app.use('/api', router);
app.timeout = 0;
app.listen(port);
console.log('Magic happens on port ' + port);
