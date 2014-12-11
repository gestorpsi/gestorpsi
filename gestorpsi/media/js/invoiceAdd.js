/* Tiago de Souza Moraes  / tiago@futuria.com.br
 * add new invoice. Selected org from GCM search
 * get org id from URL 
 * */

$(document).ready(function() {

    // url format: .../invoice/add/?org=e59d94ba-f4d2-41e9-8ad0-f7cb6f1e4b27
    url = (window.location.href);
    org_id = url.split("=")[1]; // e59d94ba-f4d2-41e9-8ad0-f7cb6f1e4b27
    $('select#id_organization option[value=' + org_id + ']').prop('selected',true);

});
