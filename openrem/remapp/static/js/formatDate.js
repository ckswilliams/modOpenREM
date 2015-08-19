function formatDate(d) {
  var dd = d.getDate();
  if ( dd < 10 ) dd = '0' + dd;
  var mm = d.getMonth()+1;
  if ( mm < 10 ) mm = '0' + mm;
  var yyyy = d.getFullYear();
  return yyyy+'-'+mm+'-'+dd;
}