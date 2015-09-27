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


function updateChart(json, force_type) {

    /**
     * update chart
     * read data from json, then bind graph
     */

    var graphs = new Array();

    if(!json) {
        $('#report_chart').hide();
    } else {

        /**
         * chart type fetch by json, or forced by jquery without request
         */

        lines_show = false;
        bars_show = false;
        points_show = false;
        
        if (!force_type) {
            if(json[0]['type']['lines'] == 'true') lines_show = true;
            if(json[0]['type']['bars'] == 'true') bars_show = true;
            if(json[0]['type']['points'] == 'true') points_show = true;
        } else {
            if(force_type['lines']) lines_show = true;
            if(force_type['bars']) bars_show = true;
            if(force_type['points']) points_show = true;
        }
        
        for (var i in json) {
            i = parseInt(i);
            var plot_ticks = new Array();
            var plot_data = new Array();

            for (var col in json[i]['data']) {
                col = parseInt(col);
                axis_x = json[i]['data'][col][0];
                axis_y = json[i]['data'][col][1];
                if(bars_show)
                    plot_ticks.push([col+0.5, axis_x]);
                else
                    plot_ticks.push([col, axis_x]);
                plot_data.push([col, axis_y]);
            }

            graphs[i] = {
                 label: json[i]['title'], 
                 data: plot_data,
                 lines: { 'show': lines_show },
                 bars: { 'show': bars_show },
                 points: { 'show': points_show }
            };
        }

        $.plot($("#report_chart"),
            graphs, 
            { 
                 xaxis: { 
                   ticks: plot_ticks 
                } 
             } 
         );
            $('#report_chart').show();
    }
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
     * updated chart
     * note: moved to google API chart (server side)
     */

    //$.getJSON('/report/admission/chart/?' + data, function(json) { 
        //updateChart(json);
        //json_data = json; // save json callback in a global variable
    //});

    /**
     * update admission data
     */

    $('div#report_table').load('/report/admission/?'+data);

    /**
     * update demographic data
     */
    
    //$('div#admission_demographic_data').load('/report/admission/demographic/?'+data);
        

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
     * updated chart 
     * note: moved to google API chart (server side)
     */

    //$.getJSON('/report/referral/chart/?' + data, function(json) { 
        //updateChart(json);
        //json_data = json; // save json callback in a global variable
    //});

    /**
     * update admission data
     */
    
    $('div#report_table').load('/report/referral/?'+data);
    /**
     * update demographic data
     */
    
    //$('div#admission_demographic_data').load('/report/admission/demographic/?'+data);
        

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



function updateReceive(data) {

    /**
     * update all receive data
     */
    if(!data) data = '';
    
    /**
     * append chart types view to url
     */
    data += chart_type_to_url();

    /**
     * update receive data, call view
     */
    $('div#report_table').load('/report/receive/?'+data);

    /**
     * update save form
     */
    $('div#save_form').load('/report/receive/save/?'+data)
    
    /**
     * get date then update form fields
     */
    $.getJSON('/report/date/?'+data, function(json) {
        $('.report_main [name=date_start]').val(json['date_start']);
        $('.report_main [name=date_end]').val(json['date_end']);
    });
}



function updateEvent(data) {

    /**
     * update all receive data
     */
    if(!data) data = '';
    
    /**
     * append chart types view to url
     */
    data += chart_type_to_url();

    /**
     * update receive data, call view
     */
    $('div#report_table').load('/report/event/?'+data);

    /**
     * update save form
     */
    $('div#save_form').load('/report/event/save/?'+data)
    
    /**
     * get date then update form fields
     */
    $.getJSON('/report/date/?'+data, function(json) {
        $('.report_main [name=date_start]').val(json['date_start']);
        $('.report_main [name=date_end]').val(json['date_end']);
    });
}
