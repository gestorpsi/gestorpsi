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

    // select all
    $("a.select-all-future").click( function(){ 
        $("input.occurrence_future").prop('checked','checked');
    });

    // unselect all
    $("a.unselect-all-future").click( function(){ 
        $("input.occurrence_future").removeAttr('checked');
    });

});
