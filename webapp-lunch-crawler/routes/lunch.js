const express = require('express');
const router = express.Router();
const fetch = require('node-fetch');

/* GET query results. */
router.get('/', function (req, res, next) {
  let query = req.query;
  itemKey = Object.keys(query).find(key => key === 'item');
  locKey = Object.keys(query).find(key => key === 'location');
  if (!itemKey || !locKey) return res.status(400).send("please provide correct query");
  let cleanedItem = getCleanedQuery(query[itemKey]);
  if (cleanedItem.length < 2 || query[locKey] < 2) {
    return res.status(400).send("please provide correct query");
  }
  // elastic search
  elasticFetching(cleanedItem, query[locKey]).then(restaurants => res.send(restaurants)).catch(err => console.log(err));
});


const elasticFetching = async (item, location) => {
  // fetch from elastic
  return fetch(`http://localhost:9200/restaurants/_search?pretty=true&q=${item}&size=1000`)
    .then(res => res.json())
    .catch(err => console.log(err));
};

const getCleanedQuery = (query) => {
  // same preprocessing steps like prod-pipeline
  query = query.replace(/[^éàèÉÀÈäöüÄÖÜa-zA-Z]+/g, ' ');  // remove special characters
  query = query.toLowerCase();
  queryLen = query.length;
  for (x = 0; x <= queryLen; x++) {
    query = query.replace(/(\s+|^)[a-z](\s+|$)/, ' ');  // remove single characters
    queryLen = query.length;
  }
  query = query.replace(/\s+/g, ' ');                    // remove multispaces
  return query;
}

module.exports = router;
