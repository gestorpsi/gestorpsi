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
 * New referral. Show professional subscription and covenant of service when change service.
 * upate Tiago de Souza Moraes / 11 10 2016
 **/

function referral_edit(select_field) {

        // remove all professional of select
        $('select#id_professional').html('');
        // delete combobox 
        $('div#ms-id_professional').remove();
        // hide
        $('label[for="id_professional"]').hide();


        // remove all covenant of select
        $('select#id_covenant').html('');
        // delete combobox 
        $('div#ms-id_covenant').remove();
        // hide
        $('label[for="id_covenant"]').hide();


        if ( select_field.val() != '' ){ 

            // professionals
            var HTML='';
            $.getJSON("/service/" + select_field.val() + "/listprofessional/", function(json) {
                jQuery.each(json,  function(){
                    HTML += '<option value="' + this.id + '">' + this.name + '</option>';
                });
                // add new elements in select
                $('select#id_professional').html(HTML);
                // reload combobox
                $('select#id_professional').multiSelect();
            });
            
            // to check if is a group service
            $.ajax({
                type: "GET",
                url: "/service/" + select_field.val() + "/group/json/",
                success: function(msg){
                    if (msg == 'False'){
                        $('select#id_group').hide();
                        $('select#id_group').parent().hide();
                        $('select#id_group option').remove();
                    } else {
                        // clean options
                        $('select#id_group option').remove();
                        // reload group select
                        $.getJSON("/service/" + select_field.val() + "/group/json/", function(json) {
                            jQuery.each(json,  function(){
                                $('select#id_group').append(new Option(this.name, this.id));
                            });
                        });
                        // show select and label
                        $('select#id_group').parent().show();
                        $('select#id_group').show();
                    }
                }
            });
                     

            // covenant of service
            var TEMP='';
            $.getJSON("/covenant/list/service/" + select_field.val() + "/", function(json) {
                jQuery.each(json, function(){

                            if ( this.events > 0 ){ 
                                TEMP += '<option value="' + this.id + '">' + this.name +' - '+ this.charge +' (' + this.events + ') - R$ '+ this.price + '</option>';
                            } else { 
                                TEMP += '<option value="' + this.id + '">' + this.name +' - '+ this.charge +' - R$ '+ this.price + '</option>';
                            }
                });
                // add new elements in select
                $('select#id_covenant').html(TEMP);
                // reload combobox
                $('select#id_covenant').multiSelect();
            });

            // show
            $('label[for="id_covenant"]').show();
            $('label[for="id_professional"]').show();
        }

        // show selects
        $('div#covenant-div-id').show();
        $('div#professional-div-id').show();
}



$(function() {

    /**
    * referral service/professional select
    * when select a service, display only professionals related
    * when select a professional, display only services related
    */
    $('select.referral[name=service] option').click(function() {
        var service = $(this);
        if($(service).hasClass('all')) {
            $('select.referral[name=professional] option').show();
        } else {
            $('select.referral[name=professional] option').hide();
            $('select.referral[name=professional] option').each(function() {
                if($(service).hasClass($(this).val())) {
                    $(this).show();
                }
            });
        }
    });


    $('select.referral[name=professional] option').click(function() {
        var professional = $(this);
        if($(professional).hasClass('all')) {
            $('select.referral[name=service] option').show();
        } else {
            $('select.referral[name=service] option').hide();
            $('select.referral[name=service] option').each(function() {
                if($(professional).hasClass($(this).val())) {
                    $(this).show();
                }
            });
        }
    }); 

    /**
     * referral - disable client
    */

    //Disable button
    $('div#edit_form div.edit_form div.client_referral_list table.newtab tr.referral_off div.button_disable a.referral_off').click(function() {
        $("div#edit_form div.edit_form div.client_referral_list table.newtab tr.referral_off div.button_disable a[id=" + this.id + "]").hide();
        $("div#edit_form div.edit_form div.client_referral_list table.newtab tr.referral_off div[id=" + this.id + "]").show();
     }); 


    // Confirm_not
    $('div#edit_form div.edit_form div.client_referral_list a.confirm_not').click(function() {
        $("div#edit_form div.edit_form div.client_referral_list tr.referral_off div.button_disable a[id=" + this.id + "]").show();
        $("div#edit_form div.edit_form div.client_referral_list tr.referral_off div[id=" + this.id + "]").hide();
    }); 
            

    // Confirm_yes
    $('div#edit_form div.edit_form div.client_referral_list a.confirm_yes').click(function() {
        // remove id selected
        $('div#edit_form div.edit_form div.client_referral_list tr[id='+ this.id +'] td').addClass('c_referral_off');
        $('div#edit_form div.edit_form div.client_referral_list tr[id='+ this.id +'] td div').remove();
        // remove from db
        $.getJSON("/referral/" + $(this).attr("id") + "/off/", function(json) {
                // return all href the normal status
                $("div#edit_form div.edit_form div.client_referral_list div.button_disable a").show();
                $("div#edit_form div.edit_form div.client_referral_list div.confirm_disable").hide();
        }); 
    });
     

    /*
     * select to choose service - referral client
     */
    $('div.hide_on_first li').hide();
    $('form#client_referral_form select[name=service]:not(.check_change select, select.check_change)').bind("keyup change", function(){
        referral_edit($(this));
    });
    

    /**
     * check if combo state has been changed, then bind save button
     */
    $('select.check_change, .check_change select').change(function () {

        if(!confirm($('input[name=message_referral_changing]').val())) { 
            // reset to original state
            $(this).children('option').attr('selected', '');
            $(this).children('option[value='+$(this).attr('original_state')+']').attr('selected', 'selected');
            return false; 
        } else {
            if($(this).attr('name') == 'service') {
                referral_edit($(this));
            }
        }
    });

    $('.check_change input[type=checkbox]').click(function () {
            if(!confirm($('input[name=message_referral_changing]').val())) { return false; }
    });

    /**
     * admission - show or hide select option / referral and indication
     **/
    // referral
    $("div.admission_referral select[name=referral]").unbind().change(function(){

        if (this.value == '7' || this.value == '8' ){
            if (this.value == '7' ){
                    $("div.admission_ref_prof").hide()
                    $("div.admission_ref_org").show()
            } else {
                    $("div.admission_ref_prof").show()
                    $("div.admission_ref_org").hide()
            }
        } else {
            // never  7 or 8 
            $("div.admission_ref_prof").hide()
            $("div.admission_ref_org").hide()
        }
    });

    // indication
    $("div.admission_indication select[name=indication]").unbind().change(function(){
        if (this.value == '3' || this.value == '4' ){
            if (this.value == '3'){
                $("div.admission_ind_prof").hide()
                $("div.admission_ind_org").show()
            } else {
                $("div.admission_ind_prof").show()
                $("div.admission_ind_org").hide()
            }
        } else {
            // never 3 or 4 
            $("div.admission_ind_prof").hide()
            $("div.admission_ind_org").hide()
        }
    });

    /**
     * referral - show details of client
     **/
    $("a.referral_details").click( function() {
        $('div.referral_details'+this.id).toggle();
    });

    /** 
     * Referral
     * hide foreign referral in form
     */
    $('form.client_referral label input[name=referral_type]').click(function() {
        if($(this).val() == 'referral')
            $('form.client_referral label.referral_type_referral').show();
        else
            $('form.client_referral label.referral_type_referral').hide();
    });

}); /* main function */ 
