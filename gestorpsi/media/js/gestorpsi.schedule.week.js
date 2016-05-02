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
    dateFormat: 'yymmdd',
    changeYear: true,
    'onSelect': function(date) {
        $("div#mini_calendar").hide();
        $('#schedule_week').load('/schedule/week/' + date.substr(0,4) + '/' + date.substr(4,2) +'/' + date.substr(6,2) +'/');
    }
}

/**
 * schedule:
 * bind all schedule functions
 */

$('div.schedule').ready(function() {

    // load today daily occurrences and mini-calendar
    $('table.weekly').unbind().ready(function() {
        $("div#mini_calendar").datepicker(schedule_options);
        updateGrid('/schedule/occurrences/');
    });
    
});
