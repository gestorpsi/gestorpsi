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

var json_data = [];

/**
 * a little helper to read chart type choices
 * then convert it to a url string parameter
 */

function chart_type_to_url() {
    url = '';
    $('input[type=radio][name=chart_type]').each(function() {
        url += '&' + $(this).val() + '='  + $(this).attr('checked');
    });
    return url;
}


function updateAdmission(data) {

    /**
     * update all admission data
     */

    if(!data) data = '';
    
    /**
     * append chart types view to url
     */

    data += chart_type_to_url();

    /**
     * update admission data
     */

    $('div#report_table').load('/report/admission/?'+data);

    /**
     * update save form
     */

    $('div#save_form').load('/report/admission/save/?'+data)
    
    /**
     * get date then update form fields
     */
    
    $.getJSON('/report/date/?'+data, function(json) {
        $('.report_main [name=date_start]').val(json['date_start']);
        $('.report_main [name=date_end]').val(json['date_end']);
        if(json['accumulated']) {
            $('.report_main [name=accumulated]').val(json['accumulated']);
        }
    });
}

function updateReferral(data) {

    /**
     * update all admission data
     */
    
    if(!data) data = '';
    
    /**
     * append chart types view to url
     */

    data += chart_type_to_url();

    /**
     * update admission data
     */
    
    $('div#report_table').load('/report/referral/?'+data);

    /**
     * update save form
     */

    $('div#save_form').load('/report/referral/save/?'+data)
    
    /**
     * get date then update form fields
     */
    
    $.getJSON('/report/date/?'+data, function(json) {
        $('.report_main [name=date_start]').val(json['date_start']);
        $('.report_main [name=date_end]').val(json['date_end']);
        if(json['accumulated']) {
            $('.report_main [name=accumulated]').val(json['accumulated']);
        }
    });
}

function updateSavedReports() {
    /**
     * load data into knowledge table
     */

    $.get('/report/saved/', function(html) {
        $('div.reports_saved #reports_saved_html').html(html);
    });
}

function updateOccurrence(data) {


    if(!data) data = '';
    data += chart_type_to_url();

    $('div#report_table').load('/report/occurrence/?'+data);
}
