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
 * array to string util function
 */

function personInLine(list) {
    
    var str = ''
    
    //append person list
    if(list) {
    jQuery.each(list,  function(){
        str = str + this.name + ", " ;
    });
    str = str.substr(0, (str.length-2))
    }
    return str
    
}
