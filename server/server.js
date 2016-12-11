var express = require('express');
var app = express();
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));

var port = process.env.PORT || 8080;

var router = express.Router();

router.get('/', function (req, res) {
    res.json({message: 'hooray! welcome to our api!'})
});

router.route('/catalog')
    .get(function(req, res) {
       res.json([
           {
               'title': 'Автомат Cyma AK-74М (CM040C)',
               'producer': 'Cyma, Китай',
               'photo': 'http://airsoft-rus.ru/upload/resize_cache/iblock/1df/900_600_12f28b1e9c3c5899ab618b8ff44e28632/460fed87-1dfa-11e2-9cbf-10bf4871b40e_b225fd71-e070-11e5-81ed-94de8003c4f2.jpeg',
               'price': '10 300',
               'link': 'http://airsoft-rus.ru/catalog/1026/41109/'
           },
           {
               'title': 'Пистолет Cyma Glock 18C AEP (CM030)',
               'producer': 'Cyma, Китай',
               'photo': 'http://airsoft-rus.ru/upload/resize_cache/iblock/4b1/189_150_0/658f9df0-7a61-11e2-bc35-10bf4871b40e_5a201324-f72d-11e5-9a13-94de8003c4f2.jpeg',
               'price': '3 800',
               'link': 'http://airsoft-rus.ru/catalog/1026/41109/'
           }, {
               'title': 'Автомат Cyma AK-105 (CM040D)',
               'producer': 'Cyma, Китай',
               'photo': 'http://airsoft-rus.ru/upload/resize_cache/iblock/59e/189_150_0/460fed89-1dfa-11e2-9cbf-10bf4871b40e_b225fd65-e070-11e5-81ed-94de8003c4f2.jpeg',
               'price': '10 300',
               'link': 'http://airsoft-rus.ru/catalog/1026/41109/'
           },
           {
               'title': 'Дробовик S&T Benelli M4 без приклада (K1203)',
               'producer': 'S&T, Китай',
               'photo': 'http://airsoft-rus.ru/upload/resize_cache/iblock/f61/189_150_0/ccc98e8d-84c6-11e3-9890-d43d7e97909d_20599a3e-d004-11e5-8ca3-94de8003c4f2.jpeg',
               'price': '3 905',
               'link': 'http://airsoft-rus.ru/catalog/1026/41109/'
           },
           {
               'title': 'Пистолет-пулемёт Cyma FN P90 с глушителем ',
               'producer': 'Cyma, Китай',
               'photo': 'http://airsoft-rus.ru/upload/resize_cache/iblock/f08/189_150_0/62a88dea-3f5d-11e5-9e6a-94de8003c4f2_e6c87f06-d57a-11e5-a937-94de8003c4f2.jpeg',
               'price': '7 900',
               'link': 'http://airsoft-rus.ru/catalog/1026/41109/'
           }
       ])
    });

router.route('/bears')
    .post(function(req, res) {
        var bear = new Bear();
        bear.name = req.body.name;

        bear.save(function(err) {
            if (err)
                res.send(err);
            res.json({ message: 'Bear created!' });
        });
    })
    .get(function(req, res) {
        Bear.find(function(err, bears) {
            if (err)
                res.send(err);
            res.json(bears);
        });
    });

app.use('/api', router);

app.listen(port);
console.log('Magic happens on port ' + port);
