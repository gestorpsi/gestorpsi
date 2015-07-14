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
 * floating save box
 */

var name = ".sidebar"; 
var menuYloc = null;


function bindDelete() {

    /**
    *
    * delete fields in forms
    *
    * used in oneToMany relationships registers
    * eg. phones, address, emails, IMs ...
    *
    */

     $('a.remove_from_form').unbind().click(function() {
          var fieldset = $(this).parents('fieldset');
          var total = 0;
          
          // count only visible div's
          $(fieldset).children('div').each(function() {
               if($(this).css('display') != 'none') {
                    total = total + 1;
               }
          });
          
          // remove border top before delete it
          $(fieldset).children('div').removeClass('multirow');

          var div = $(this).parent('label').parent('div');

          if(total>1) {
               $(div).children('label').children('input:text').val('');
               $(div).hide();
          } else {
               $(div).children('label').children('input:text').val('');
          }
          
          // re-draw top borders if exists
          if($(fieldset).hasClass('set_multirow')) {
               $(fieldset).children('div').not(':first').addClass('multirow');
          }

     });
}

function reloadCities(el) {

        $.get('/address/search/cities/state/' + el.val() + '/', function( data ) {
          el.parent('label').parent('div').children('label.city').children('select').html(data); // rebuild city combo
          el.parent('label').parent('div').children('label.city').children('select').children('option[value=' + el.attr('city') + ']').attr('selected', 'selected'); // select city
        });
}

    /**
     * PROFESSION - SYMBOL - PROFESSION DESCRIPTION
     **/

function reload_symbol_profession() { 
    $("select.profession_type option").click(function(){
        //$(this).parents('fieldset').children('label').children('input.profession_symbol').val($(this).attr("symbol"));
        $('div label input[name=symbol].profession_symbol').val($(this).attr("symbol"));
    });
}

/**
 * reload select cities when state in selected, in generic addresses forms
 */

function bindCityCombo() { 
    $('label.state select.city_search').unbind().change(function() {
        reloadCities($(this));
    });
}

function bindMask() {
    /**
    *
    * _automask and automaskme()
    * automatic mask for all input, type text, fields.
    *
    * _dependency and thanks to Masked Input Plugin
    * 	url: http://digitalbush.com/projects/masked-input-plugin/
    *
    * _description:
    *
    * search for a 'mask' attribute in form text fields
    *
    * you only must to define the 'mask' attribute to masked fields
    *
    * eg.:
    * 	<input type="text" name="phone" mask="((999) 9999-9999)" />
    *                                      ^^^^  ^^^^^^ ^^^^^^^^^^
    *
    * masks rules:
    * ------------------
    * a - Represents an alpha character (A-Z,a-z)
    * 9 - Represents a numeric character (0-9)
    * * - Represents an alphanumeric character (A-Z,a-z,0-9)
    *
    */

    $("form input:text[mask]").each(function(){
      $(this).mask($(this).attr('mask'));
    });
}

    /**
     * New referral. Show professional subscription and covenant of service when change service.
     * upate Tiago de Souza Moraes / 27 11 2014
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
            
            // is group
            $('select[name=group] option').remove();
            if(select_field.children(':selected').attr('is_group')=='True') {
                $.getJSON("/service/" + select_field.val() + "/group/json/", function(json) {
                    jQuery.each(json,  function(){
                        $('select[name=group]').append(new Option(this.name, this.id));
                    });
                });
                $('label.referral_group').effect('blind', {'mode':'show'});
            } else {
                $('label.referral_group').hide();
            }
            

            // covenant of service
            var TEMP='';
            $.getJSON("/covenant/list/service/" + select_field.val() + "/", function(json) {
                jQuery.each(json, function(){

                            if (this.events > 0 ){ 
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
    
    bindDelete();
    reload_symbol_profession();
    bindMask();

    /**
     * calc age of client
     */
    
    $("form input:text[name=dateBirth]").keyup(function(){
      displayAge();
    });

    /**
     * reload city combo
     */

    $('#form_organization label.state select.city_search, label.state select.city_search').each(function() {
        if($(this).attr('city') > 0) {
            reloadCities($(this));
        }
    });

    bindCityCombo();
     
     /**
      * other countries address, not registered in database
      * if another country is selected, change form fields ..
      */
     
     $('form select.country').unbind().change(function() {
           if($(this).val() == 33) { // Brazil
               // reset oldvalues
               $(this).parents('div').children('label.noautocomplete').children('input').val('');
               $(this).parents('div').children('label.noautocomplete').hide();
               $(this).parents('div').children('label.autocomplete').show();
           } else {
               // reset oldvalues
               $(this).parents('div').children('label.autocomplete.city').children('select').children('option').attr('selected','');
               $(this).parents('div').children('label.autocomplete').hide();
               $(this).parents('div').children('label.noautocomplete').show();
           }
     });

     /**
      * valid if exist a short name in form organization
      */
     $('input.short_search').unbind().keyup(function() {
         $.ajax({
           type: "GET",
           url: "/organization/check/"+ $(this).val()+"/",
           success: function(msg){
            if (msg == '1'){
               $("div.check_available").hide();
            } else {
               $("div.check_available").show();
            }
           }
         });
     });

     /**
      * valid if exist a user name
      */
     $('input#id_username').unbind().keyup(function() {
         $.ajax({
           type: "GET",
           url: "/user/check/"+ $(this).val()+"/",
           success: function(msg){
            if (msg == '1'){
               $("div.check_available_user").hide();
            } else {
               $("div.check_available_user").show();
            }
           }
         });
     });

     /** 
      * clone div content and append it to form
      */
     
     $('fieldset a.add_to_form').click(function() {
          var next = ($("input.profession_symbol:last").attr("id") + 1 );
          $(this).before('<div>' + $(this).parents('fieldset:first').children('div:first').html() + '</div>');
          $(this).parents('fieldset').children('div:last').children('input').val('');
          $(this).parents('fieldset').children('div:last').children('label').children('input').val('');
          // ADD value in id of the SELECT and INPUT SYMBOL. CHANGE ONLY THE CORRENT INPUT SYMBOL
          $(this).parents('fieldset').children('div:last').children('label').children('input.profession_symbol').attr("id", next);
          $(this).parents('fieldset').children('div:last').children('label').children('select.profession_type').attr("id", next);
          // draw top-border for multirows fieldsets (eg.: address fieldset)
          if($(this).parents('fieldset').hasClass('set_multirow')) {
               $(this).parents('fieldset').children('div').removeClass('multirow');
               $(this).parents('fieldset').children('div').not(':first').addClass('multirow');
          }

          bindDelete();
          reload_symbol_profession();
          bindCityCombo();
          bindMask();

     });
     
     /**
     *
     * image upload
     * 
     * _description:
     *  
     * show upload box when clicked (close automatic, when file is selected).
     * 
     */
     $('a.clips').unbind().click(function() {
          $(this).parents('form').parents('div').children('div.photo_form_upload').show();
          $('div#over').show();
     });

     
    /** 
      * 
      * Room form
      * 
      * _description:
      * 
      * append Room add form
      * 
      */
     
     $('div#edit_form li#add_room a').unbind().click(function() {
          $('div#edit_form #room_form').hide();
          $('div#edit_form .form_room_box').hide();
          $('div#edit_form #fieldset_room_identification').show();
          var total = $("div#edit_form .form_room_box").length + 1;
          
          // add form
          $("div#edit_form #room_more").before('<div class="form_room_box" id="room_'+total+'"><div class="form_room">'+$(".form_room").html()+'</div></div>');
          // clean fields
          $('div#edit_form #room_'+total+' input').val('');
          $('div#edit_form #room_'+total+' textarea').text('');
          
     
          // auto insert new typing item, in the room list
          
          // first we need to clean item with empty names
          $('div#edit_form li.li_rooms').each(function() {
               li = $(this);
               if($(li).text()=='') {
                    li.remove();     
               }
          });
          // create new item in room list
          $('div#edit_form li.li_rooms:last').after('<li class="li_rooms"><a class="notajax" onclick="$(\'#room_form\').hide(); $(\'.form_room_box\').hide(); $(\'#fieldset_room_identification\').show(); $(\'#room_'+total+'\').show();"></a></li>');
          // update room name, in room list when new name is typing 
          $('div#edit_form #room_'+total+' input.update_name').unbind().keyup(function() {
              $('div#edit_form #div_list_rooms').show();
              $('div#edit_form li.li_rooms:last a').text($(this).val());
           });
             
     });
     
    /**
     * select multiple jquery widget plugin
     * http://akibjorklund.com/code/multiselectable/
     */

    $('select.multiselectable').multiselectable({
		selectableLabel: 'Disponíveis',
		selectedLabel: 'Selecionados',
		moveRightText: '>>',
		moveLeftText: '<<',
        template: '<div class="multiselectable"><input type="text" class="multiselectable_filter">' +
            '<div class="m-selectable-from"><label for="m-selectable"></label>' +
            '<select multiple="multiple" id="m-selectable"></select>' +
            '</div>' +
            '<div class="m-selectable-controls">' +
            '<button class="multis-left"></button>' +
            '<button class="multis-right"></button>' +
            '</div>' +
            '<div class="m-selectable-to"><label for="m-selected"></label>' +
            '<select multiple="multiple" id="m-selected"></select>' +
            '</div>' +
        '</div>',
	});
    
    $('div.multiselectable input.multiselectable_filter').keyup(function() {
        var typed = $(this).val();
        if(typed != '') {
            $('select#m-selectable option').hide();
            $('select#m-selectable option').each(function() {
                option = $(this).text().toLowerCase()
                if(option.match(typed.toLowerCase())) {
                    $(this).show();
                }

            });
        } else {
            $('select#m-selectable option').show();    
        }
    });
      
     /** 
      * 
      * Place form
      * 
      * _description:
      * 
      * append Room add form
      * 
      */
     
     $('div#edit_form li#add_room a').unbind().click(function() {
          $('div#edit_form #place_form').hide();
          $('div#edit_form .form_room_box').hide();
          $('div#edit_form #fieldset_room_identification').show();
          var total = $("div#edit_form .form_room_box").length + 1;
          
          // add form
          $("div#edit_form #room_more").before('<div class="form_room_box" id="room_'+total+'"><div class="form_room">'+$(".form_room").html()+'</div></div>');
          // clean fields
          $('div#edit_form #room_'+total+' input').val('');
          $('div#edit_form #room_'+total+' textarea').text('');
          
     
          // auto insert new typing item, in the room list
          
          // first we need to clean item with empty names
          $('div#edit_form li.li_rooms').each(function() {
               li = $(this);
               if($(li).text()=='') {
                    li.remove();     
               }
          });
          // create new item in room list
          $('div#edit_form li.li_rooms:last').after('<li class="li_rooms"><a class="notajax" onclick="$(\'#place_form\').hide(); $(\'.form_room_box\').hide(); $(\'#fieldset_room_identification\').show(); $(\'#room_'+total+'\').show();"></a></li>');
          // update room name, in room list when new name is typing 
          $('div#edit_form #room_'+total+' input.update_name').unbind().keyup(function() {
              $('div#edit_form #div_list_rooms').show();
              $('div#edit_form li.li_rooms:last a').text($(this).val());
           });
             
     });
       
     /** show selected room fieldset  */ 
     $('div#edit_form li.li_rooms a').unbind().click(function() {
         $('div#edit_form #place_form').hide();
         $('div#edit_form .form_room_box').hide();
         $('div#edit_form #fieldset_room_identification').show();
         $('div#edit_form #room_' + $(this).attr('display')).show();
         $('div#edit_form #room_' + $(this).attr('display') + ' input.update_name').unbind().keyup(function() {
             $('div#edit_form #li_room_'+$(this).attr('display')+' a').text($(this).val());
         });
     });
     
     /**
      * 
      * gender are choiced by icons ..
      * 
      * _description:
      * listen from an image click, so ajust selected gender in
      * a hidden input with an attribute id="id_gender"
      * 
      */
     
     $('form div.photo a.gender').unbind().click(function() {
          if($(this).hasClass('active')) {
               $('.gender').removeClass('active');
               $(this).siblings('input.gender').val('');
          } else {
               $('.gender').removeClass('active');
               $(this).addClass('active');
               $(this).siblings('input.gender').val($(this).attr('value'));
          }
     });

     /**
      * 
      * Device Restriction
      * 
      * _description:
      * listen from an select change, so hide/show professional area select
      * 
      */
      $('form select.device_restriction').unbind().change(function() {
         if ($(this).val() == 1) {  // not restricted
            $(this).parents('label').parents('fieldset').children('label.device_restriction').hide();
         } else {
            $(this).parents('label').parents('fieldset').children('label.device_restriction').show();
         }
      })
      


     /**
      * 
      * Device Mobility
      * 
      * _description:
      * listen from an select change, so hide/show selects place/room.
      * 
      */     

     $('form select.device_mobility').unbind().change(function() {
        // reset old values selected when changed
        $('form select[name=place_associated]').val('');
        $('form select[name=room_associated]').val('');
        $(this).parents('label').parents('fieldset').children('label.device_room').children('select').children('option:not(first)').hide();
        if ($(this).val() == 1) { // Fixed Device
            $(this).parents('label').parents('fieldset').children('label.device_room').show();
            $('form select[name=place_associated] option[no_room=True]').attr('disabled', 'disabled');
        } else {
            $(this).parents('label').parents('fieldset').children('label.device_room').hide();
            $('form select[name=place_associated] option').attr('disabled', '');
        }
     });
     
    $('form select.device_place').unbind().change(function() {
        $(this).parents('label').parents('fieldset').children('label.device_room').children('select').children('option:not(first)').hide();
        $(this).parents('label').parents('fieldset').children('label.device_room').children('select').children('option.place_'+$(this).val()).show();
        $(this).parents('label').parents('fieldset').children('label.device_room').children('select').children('option:visible:first').attr('selected','selected');
        if($(this).val()=='') {
            $(this).parents('label').parents('fieldset').children('label.device_room').children('select').children('option:first').attr('checked', 'checked');
            $(this).parents('label').parents('fieldset').children('label.device_room').hide();
        }
    });
     


     /** 
     * service form - Research project name
     */

    $("input.research_project_name[type=checkbox]").click(function(){
    //$(('input.research_project_name[type=checkbox]:checked').size() == '0'){
        //var SHOW = $('input.research_project_name[type=checkbox]:checked').size();
        if ( $('input.research_project_name[type=checkbox]:checked').size() == "1"){
            $("div.research_project_name").show();
        } else {
            $("div.research_project_name").hide();
            $("input[name=research_project_name]").val("");
        }
    });

     /**
     * service types and service areas
     */
     
     $('select.service_area').each(function() {
          select_area = $(this).val();
          // set initial service type     
          $(this).parents('fieldset').children('label').children('select.service_type').children('option').hide();
          $(this).parents('fieldset').children('label').children('select.service_type').children('option[area=' + select_area + ']').show();
          // set initial private areas
          $(this).parents('form').children('div').children('fieldset.service_areas').hide();
          $(this).parents('form').children('div').children('fieldset.area_' + select_area).show();
          // set initial service solicitation with selected area
          $(this).parents('fieldset').children('label').children('select.service_solicitation').children('option').hide();
          $(this).parents('fieldset').children('label').children('select.service_solicitation').children('option.' + 'area_'+ select_area ).show();
     });
     
     $('select.service_area').unbind().change(function() {
          var select = $(this);
          // switch service type
          $(select).parents('fieldset').children('label').children('select.service_type').children('option').hide();
          $(select).parents('fieldset').children('label').children('select.service_type').children('option[area=' + $(this).val() + ']').show();
          $(select).parents('fieldset').children('label').children('select.service_type').children('option[area=' + $(this).val() + ']:first').attr('selected', 'selected');
          // switch service solicitation
          $(select).parents('fieldset').children('label').children('select.service_solicitation').children('option').hide();
          $(select).parents('fieldset').children('label').children('select.service_solicitation').children('option.area_'+$(select).val()).show();
          // show privates areas
          $('form div.service_areas').hide();
          $('form div.area_' + $(this).val()).show();
     });
     
      // quick add
      
     $('div form input.cancel').click(function() {
          $(this).parents('div.form_mini:first, div.form_mini_noinsert:first').effect('slide', {'direction':'up', 'mode':'hide'});
          $(this).parents('div.form:first').hide();
          return false;
     
     });
     
     $('a.form_mini').live('click', function() {
          $('div.form_mini').hide(); // hide all mini form
          var form_mini = $('div.'+$(this).attr('display')).effect('slide', {'direction':'up'});
          
          if(!$(this).hasClass('choose_room')) {
              $.form_mini_link = $(this);
              $(form_mini).children('form').validate({
                   event:"submit",
                   rules: {
                        label: {
                                required: true
                        }
                   },
                   messages: {
                        label: 'Este campo é obrigatório'
                   },
                   submitHandler: function(form) {
                        $(form).ajaxSubmit(form_mini_options);
                   }
              });
          } else {
              $('a#schedule_room_href').attr('href_base', $(this).attr('href'));
              $('select[name=choose_room]').change(function() {
                    $('a#schedule_room_href').attr('href', $('a#schedule_room_href').attr('href_base') + '&room=' + $(this).val());
                    $('a#schedule_room_href').unbind();
            });
          }
          return false;
     });

    $('a#schedule_room_href').click(function() {
        $('.room_required').show();
        return false;
    });
     
     $('a.form_mini_noinsert').unbind().click(function() {
          $(this).parents('form').parents('div').children('div.'+$(this).attr('display')).effect('slide', {'direction':'up'});
          return false;
     });
     
     $('select.toggle_parent_label').change(function() {
         var select = $(this);
         $(select).parents('fieldset').children('label.hidden').hide();
         $(this).children('option').each(function() {
             if($(this).attr('selected')) {
                 if($(this).attr('nick')) {
                     var class_name = $(this).attr('nick');
                     $(select).parents('fieldset').children('label.'+class_name).show();
                 }
             }
         });
     });

    /**
    * bind select itensselected
    * select itens from an available list options (used in Services)
    * copy itens from an select multiple box to first prev sibling
    */

    $('select.itens_available option').unbind().click(function() {
        $(this).parents('fieldset').children('label').children('select.itens_selected').append('<option value="'+$(this).attr('value')+'" selected="selected">'+$(this).text()+'</option>');
        $(this).hide();
        $('select.itens_selected option').unbind().click(function() {
            var select = $(this).parents('select');
            $(this).parents('fieldset').children('label').children('select.itens_available').children('option[value='+$(this).attr('value')+']').show();
            $(this).remove();
            // select itens again
            $(select).children('option').attr('selected','selected');
        });
     });

     
     /**
      * hide all itens available select boxes, and show only the first
      */
     
     $('fieldset select.multiple.itens_available').parents('fieldset').each(function() {
          $(this).children('label').children('select.multiple.itens_available:not(:first)').hide();
     });

     $('fieldset label a.select_multiple_menu').each(function() { $(this).removeClass('active'); });
     $('fieldset label a.select_multiple_menu').parents('label').each(function() { $(this).children('a.select_multiple_menu').not(':first').addClass('active'); });
     
     $('label a.select_multiple_menu').click(function() {
          $(this).parents('fieldset').children('label').children('select.itens_available').hide();
          $(this).parents('fieldset').children('label').children('select.itens_available.' + $(this).attr('display')).show();
          $('fieldset label a.select_multiple_menu').removeClass('active');
          $(this).addClass('active');
     });
     
     
     /**
      * referral service/professional select
      *
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
     * hide and show weekly, monthly and yearly extra option in schedule form
     */

    $('.schedule div.switch input[type=radio]').unbind().click(function() {
        var div = $(this).parents('label').parents('div');
        var elements_to_show = '.' +$(div).attr('clean')+'_'+$(this).val();
        $('.' +$(div).attr('clean')).hide();
        $(elements_to_show).show();
    });

    $('.schedule div.switch input[type=checkbox]').unbind().click(function() {
        var div = $(this).parents('div');
        if(!$(this).attr('checked')) {
            $('.' +$(div).attr('clean')).hide();
        } else {
            $('.' +$(div).attr('clean')).show();
        }
    });

    /**
     * generic switch to display and hide form elements
     */

    $('.generic_switch').unbind().click(function() {
        var el = $(this);
        $(el.attr('hide')).hide();
        $(el.attr('show')).show();
    });

     /**
      * select multiple plugin
      */
     
     /*
     $("#form select[multiple].asm").asmSelect({
          animate: false
     });
     */
     
     /**
      * user - return unsername slugify and firts email
      */

    $('#form select.get_user_json option').unbind().click(function() {
        if ($(this).attr("value")) {
                $.getJSON("/user/" + $(this).attr("value") + "/setformuser/", function(json) {
                    $("#form input[name=username]").val(json[0]);
                    $("#form input[name=email_send_user]").val(json[1]);
                    });
       } else {
                    $("#form input[name=username]").val("");
                    $("#form input[name=email_send_user]").val("");
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
        //$('div#edit_form div.edit_form div.client_referral_list tr[id='+ this.id +']').remove();
        $('div#edit_form div.edit_form div.client_referral_list tr[id='+ this.id +'] td').addClass('c_referral_off');
        $('div#edit_form div.edit_form div.client_referral_list tr[id='+ this.id +'] td div').remove();
        // remove from db
        $.getJSON("/referral/" + $(this).attr("id") + "/off/", function(json) {
                //$('div#edit_form div.edit_form div.client_referral_list tr[id='+ $(this).attr("id") +']').remove();
                // return all href the normal status
                $("div#edit_form div.edit_form div.client_referral_list div.button_disable a").show();
                $("div#edit_form div.edit_form div.client_referral_list div.confirm_disable").hide();
                alert("Cliente desligado com sucesso!");
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
    

    /**
    * devices - change select to fixed when landable chekbox is checked, vice-versa
    * edit device form
    * check box 
    **/
    $('form.edit_device input[id=id_lendable]').click(function(){
        if (this.checked == true ){
            if ($('form.edit_device div#device_form select[name=select_mobility_type]').val() == "1"){
                $('form.edit_device div#device_form select[name=select_mobility_type]').val("2");
                $('form.edit_device div#device_form label.device_room').hide();
            }
        }
    });

    // select type
    $('form.edit_device div#device_form select[name=select_mobility_type]').change(function(){
        if (this.value == "1"){
            $('form.edit_device input[id=id_lendable]').removeAttr("checked");
        }
    });

   // new device form
   //  check box 
    $('form.new_device_form div#device_form input[id=id_lendable]').click(function(){
        if (this.checked == true ){
            if ($('form.new_device_form div#device_form select[name=select_mobility_type]').val() == "1"){
                $('form.new_device_form div#device_form select[name=select_mobility_type]').val("2");
                $('form.new_device_form div#device_form label.device_room').hide();
            }
        }
    });

    // select type
    $('form.new_device_form div#device_form select[name=select_mobility_type]').change(function(){
        if (this.value == "1"){
            $('form.new_device_form div#device_form input[id=id_lendable]').removeAttr("checked");
        }
    });


    /***
    * show professionals of organization of external referral select
    **/
    $('div.main_area select#id_organization').unbind().change(function(){
        $('select[name=professional] option').remove();
        if (this.value != ''){
            $.getJSON("/client/org/" + this.value + "/listprofessional/", function(json) {
                jQuery.each(json,  function(){
                    $('select[name=professional]').append(new Option(this.name, this.id));
                });
            });
        }
                
    });

    /********
    *  ocupation search 
    *********/

        $('a.show_ocup_search').click(function() {
            $('.ocup_search').toggle();
            $('table#ocup_results tbody').html('');
        });
        
        $('a[name=ocup_search_key]').click(function() {
            var typed = $('input[name=ocup_search_key]').val()
            if(typed.length >= 2) {
                $.getJSON('/util/ocupation/?query=' + typed, function(json) {
                    line = '';
                    jQuery.each(json, function() {
                       line += '<tr><td class="ocup_id">' + this.id + '</td><td class="ocup_label"><a style="cursor:pointer;">' + this.name + '</a></td></tr>';
                    });
                    $('table#ocup_results tbody').html(line);
                    $('table#ocup_results tr td a').click(function() {
                        $('input[name=ocup_class]').val($(this).parents('tr').children('td.ocup_id').text());
                        $('span.ocup_name').text($(this).parents('tr').children('td.ocup_label').children('a').text());
                        $('.ocup_search').hide();
                        $('table#ocup_results tbody tr').show();
                        $('input[name=ocup_search_key]').val('');
                    });
                   
                });
            } else {
                $('table#ocup_results tbody').html('');
            }
        });    

    /**
     * load client list when insert new register
     */

    if($('.form_client.autocomplete').html()) {
        $.getJSON("/client/organization_clients/?include_deactivated=True&q=&", function(json_data) {
            var names = json_data['results']
            $('.form_client.autocomplete input[name=name]').click().autocomplete(names, {
                minChars: 0,
                width: 355,
                matchContains: "word",
                autoFill: false,
                formatItem: function(row, i, max) {
                    return row.name
                }
            });
        });
    }

$('.form_client.autocomplete input[name=name]').result(function(event, data, formatted) {
        url = '/client/'+data.id+'/';
        window.location.replace(url);
        return false;
	});
    
    /**
     * datePicker UI calendar
     */
    
    $('input.calendar').datepicker({ dateFormat: 'dd/mm/yy' });
    
    /**
     * color pallete
     */
    
    $('a.pick_color').click(function() {
        $('input[name=service_css_color_class]').val($(this).attr('color'));
        $('a.color_switch div').remove();
        $('a.color_switch').html('<div class="service_name_html color' + $(this).attr('color') + '">&nbsp;</div>');
        $('.color_palette').effect('slide', {'direction':'up', 'mode':'hide'});
    });
    
    $('a.color_switch').live('click', function() {
        $('.color_palette').effect('slide', {'direction':'up'});
    });
    
    $('a.close_palette').click(function() {
        $('.color_palette').hide();
    });
    
    
/* main function */ 
});
