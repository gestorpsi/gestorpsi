/**

Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

*/

/** 
* student list
*/
function updateStudent(url, deactive, app, extra){
    if (!app) app = "careprofessional/student";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */
        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/careprofessional/student/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '</td>';
                tableTR += '<td><span class="phone">' + this.phone + '</span><br />';
                tableTR += '<span class="email">' + this.email + '</span></td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive, extra);
        $("ul.paginator a").unbind().click(function(){
            updateStudent($(this).attr('href'), deactive, app, extra);
            return false;
        });
    });  

    return false;
}
