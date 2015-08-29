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

$(document).ready(function() {
    /*
     * if group checkbox checked then show covenant for groups.
     * return all covenants
     */
    $('input#id_modalities_2').change( function(){ 

        var HTML='';
        $('div#id_covenant_list ul').html(''); // clear div

        // by event, group.
        if ( this.checked ){ 
            $.getJSON("/covenant/list/group/" , function(json) {
                jQuery.each(json,  function(){
                    $('div#id_covenant_list ul').append('<li><label><input type="checkbox" name="service_covenant" value="' + this.id + '"/>' + this.name + '</label></li>');
                });
            });

        // all covenants
        } else { 
            $.getJSON("/covenant/list/all/" , function(json) {
                jQuery.each(json,  function(){
                    $('div#id_covenant_list ul').append('<li><label><input type="checkbox" name="service_covenant" value="' + this.id + '"/>' + this.name + '</label></li>');
                });
            });
        }
    });
});
