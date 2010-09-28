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

$(function() {
    
    /**
     * load first data
     */
    
    updateAdmission();

    /**
     * load report saved list
     */

    updateSavedReports();
    

    /**
     * bind any click to hide message are if exists
     */
    
    $('a, button').click(function() { 
        $('#msg_area').hide();    
    });

    /**
     * bind tab navigation
     */
    
    $('ul#sub_report li a').click(function() {
        $('ul#sub_report li a').removeClass('active');
        $(this).addClass('active');
        $('.tab_content').hide();
        $($(this).attr('display')).show();
    });

    /**
     * bind export data tab
     */
    
    $('a.export_data_tab').click(function() {
        $('.dashboard_overview').hide();
        $('.report_filter_nav').show();
        $('.export_data_form').show();
    });

    /**
     * bind overview data tab
     */
    
    $('a.overview_tab').click(function() {
        $('.dashboard_overview').show();
        $('.export_data_form').hide();
    });

    /**
     * bind the datepicker
     */

    $('.report_main [name=date_start], .report_main [name=date_end]').datepicker({ dateFormat: 'dd/mm/yy' });

    /**
     * bind filter form
     * update admission stats data
     */
    
    $('#report_filter [name=update]').click(function() {
        $('div.loaded_report_title').hide();
        
        var form = $(this).parents('form:first');
        var date_start =form.children('[name=date_start]').val();
        var date_end =form.children('[name=date_end]').val();
        
        var data = 'date_start=' + date_start + '&date_end=' + date_end;
        
        updateAdmission(data);

        return false;
    }); 

    /**
     * bind close link in dialog box
     */

    $('a.close_dialog').live('click' ,function() {
        $(this).parents('div.dialog').hide();
    });
    
    /**
     * display client list
     * this open a dialog with a list of clients related to stats filter
     */
    
    $('table.report a.report_clients').live('click', function() {
        $('div#report_clients').load($(this).attr('href'));
        $('div.client_dialog').draggable({ handle: 'h1'});
        return false;
    });
    
    
    /**
     * bind del, undelete and 'empty trash' button in saved reports
     */
    
    $('.saved_table a.del_report').live('click', function() {
        $.get($(this).attr('href'), function() {
            updateSavedReports();
        });
        return false;
    });
    
    /**
     * load admission saved report
     */
    
    $('.saved_table a.report_load_admission').live('click', function() {

        /**
         * select dashboard tab
         */
        
        $('ul#sub_report li a').removeClass('active');
        $('ul#sub_report li a:first').addClass('active');
        $('.tab_content').hide();
        $('div.saved_successfully').hide();
        $('div.dashboard').show();
        $('div.loaded_report_title h4').text($(this).attr('title'));
        $('div.loaded_report_title small span').text($(this).attr('date'));
        $('div.loaded_report_title').show();

        /**
         * update admission
         */
                    
        updateAdmission($(this).attr('data'));
        
        return false;
    });
    
    /**
     * load admission from filters in the right bar
     */
    
    $('a.report_filter').click(function() {
        updateAdmission($(this).attr('data'));
        $('div.loaded_report_title').hide();
        return false;
    });
    
    $('div.loaded_report_title button[name=close_report]').click(function() {
        $('div.loaded_report_title').hide();
        $('div.report_filter_nav').fadeIn();
    });
    
     
     /**
      * bind form save actions
      */

     $('form#report_filter button[name=save]').unbind().click(function() {
          $('div.report_save_container').effect('slide', {'direction':'up'});
          return false;
     });
     
     $('form.report_save input[name=cancel]').live('click', function() {
          $('div.report_save_container').effect('slide', {'direction':'up', 'mode':'hide'});
          return false;
     });

    /**
     * form submit in gestorpsi.report.forms.js file
     * ...
     */

});


