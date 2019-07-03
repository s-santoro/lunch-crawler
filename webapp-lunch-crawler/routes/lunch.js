var express = require('express');
var router = express.Router();

/* GET query results. */
router.get('/', function(req, res, next) {
  res.send('get results from elastic');
});

module.exports = router;
