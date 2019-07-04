var express = require('express');
var router = express.Router();

/* GET query results. */
router.get('/', function (req, res, next) {
  let query = req.query;
  itemKey = Object.keys(query).find(key => key === 'item');
  locKey = Object.keys(query).find(key => key === 'location');
  if (!itemKey || !locKey) res.status(400).send("please provide correct query");
  let cleanedItem = getCleanedQuery(query[itemKey]);
  if (cleanedItem.length < 2 || query[locKey] < 2) res.status(400).send("please provide correct query");
  // elastic
  //elasticFetching(query[key]).then(restaurants => res.send(restaurants)).catch(err => console.log(err));
  res.status(200).json({itemKey: cleanedItem, locKey: query[locKey]});
});


const elasticFetching = async (item, location) => {
  // fetch from elastic
  return fetch(`http://localhost:9200/menu/_search?pretty=true&q=${item}&q=${location}`)
  .then(res => console.log(res))
  // TODO: add menus to elastic and retrieve them
  .then()
  .catch(err => console.log(err));
};

const getCleanedQuery = (query) => {
  // same preprocessing steps like prod-pipeline
  query = query.replace(/[^éàèÉÀÈäöüÄÖÜa-zA-Z]+/g, ' ');  // remove special characters
  query = query.toLowerCase();
  queryLen = query.length;
  for(x = 0; x <= queryLen; x++) {
      query = query.replace(/(\s+|^)[a-z](\s+|$)/, ' ');  // remove single characters
      queryLen = query.length;
  }
  query = query.replace(/\s+/g, ' ');                    // remove multispaces
  return query;
}

module.exports = router;
