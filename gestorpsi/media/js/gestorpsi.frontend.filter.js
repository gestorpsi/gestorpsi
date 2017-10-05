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

$(document).ready(function(){

    // auto load filter after selected.
    $('select#autoloadfilter').bind('change', function(){
        var url = $(this).val(); // get selected value
        if (url){ // require a URL
            window.location = url; // redirect
        }
        return false;
    });
});
