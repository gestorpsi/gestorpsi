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

function updateAdmissionChart(json) {

    /**
     * update chart
     * read data from json, then bind graph
     */

    var graphs = new Array();

    if(!json) {
        $('#report_chart').hide();
    } else {
    
    for (var i in json) {
        i = parseInt(i);
        var plot_ticks = new Array();
        var plot_data = new Array();

        for (var col in json[i]['data']) {
            col = parseInt(col);
            axis_x = json[i]['data'][col][0];
            axis_y = json[i]['data'][col][1];
            plot_ticks.push([col+0.5, axis_x]);
            plot_data.push([col, axis_y]);
        }
        
        
        lines_show = (json[i]['lines'])?true:false;
        bars_show = (json[i]['bars'])?true:false;
        points_show = (json[i]['points'])?true:false;

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
     * updated chart
     */

    $.getJSON('/report/admission/chart/?' + data, function(json) { 
        updateAdmissionChart(json);
    });

    /**
     * update admission data
     */

    $('div#admission_table').load('/report/admission/?'+data);

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

