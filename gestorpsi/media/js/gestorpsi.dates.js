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

var schedule_options = {
    dateFormat: 'dd/mm/yy',
    'onSelect': function(date) {
        $('p.description').text(date);
    }
    //    ,firstDay: 1,
}

var calendar_date = {
    dateFormat: 'dd/mm/yy'
//    , firstDay: 1
}

$(document).unbind().ready(function(){
    $("div.schedule_month").datepicker(schedule_options);
    $('input.calendar.date:not([mask])').datepicker(calendar_date);
});









