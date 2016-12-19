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

function isNormalInteger(str) {
    return /^\+?(0|[1-9]\d*)$/.test(str);
}

router.route('/catalog')
    .get(function(req, res) {

        var searchText = req.query.search || '';

        var offset = req.query.offset;
        offset = isNormalInteger(offset) ? offset : 0;

        var limit = req.query.limit;
        limit = isNormalInteger(limit) ? limit : 30;

        var order = req.query.order == 'true';

        var searchArray = searchText.split(' ');
        var likeFilters = '';

        if ( !(searchArray.length == 1 && searchArray[0] === '') ) {
            searchArray.forEach(function (val) {
                likeFilters += "AND LOWER(p1.title) LIKE LOWER('%" + val + "%') ";
            });
        }
        var sqlQuery = "SELECT p1.* FROM product p1 \
            LEFT JOIN product p2 \
            ON (p1.link = p2.link AND p1.timestamp < p2.timestamp) \
            WHERE p2.timestamp IS NULL \
            " + likeFilters + "\
            ORDER BY p1.price " + (order ? "ASC" : "DESC") + "\
            OFFSET " + offset + "\
            LIMIT " + limit + ";";

        console.log('DB QUERY: ' + sqlQuery);

        var query = dbClient.query(sqlQuery);
        var rows = [];

        query.on('row', function(row) {
            rows.push(row);
        });
        query.on('end', function(result) {
            console.log('DB ROW COUNT: ' + result.rowCount);
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
