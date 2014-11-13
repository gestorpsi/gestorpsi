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
* client list of service
*/
function updateClientService(url, deactive, app) {
    return false;
}

/** 
* user list
*/

function updateUser(url, deactive, app) {
    if (!app) app = "user";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.person_id + '"><td class="title">';
                tableTR += '<a href="/user/' + this.person_id + '/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '<br />' + this.username;
                tableTR += '</td>';
                tableTR += '<td><span class="phone"></span><br />';
                tableTR += '<span class="lixao"></span></td>';
                tableTR += '<td>';
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);
        $("ul.paginator a").unbind().click(function(){
            updateUser($(this).attr('href'), deactive, app);
            return false;
        });
    });  

    return false;
}

/** 
* employee list
*/

function updateEmployee(url, deactive, app) {
    if (!app) app = "employee";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/employee/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '</td>';
                tableTR += '<td><span class="phone">' + this.phone + '</span><br />';
                tableTR += '<span class="email">' + this.email + '</span></td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);
        $("ul.paginator a").unbind().click(function(){
            updateEmployee($(this).attr('href'), deactive, app);
            return false;
        });
    });  

    return false;
}

/** 
* contact list
*/

function updateContact(url, deactive, app) {
    if (!app) app = "contact";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                var class_content = ""
                var type = ''
                
                if(this.type == 1) type = 'organization';
                if(this.type == 2) type = 'professional';

                if (this.type == '1' && this.type_org == 'LOCAL') class_content = "clinic local";
                if (this.type == '1' && this.type_org == 'GESTORPSI') class_content = "clinic gestorpsi";
                if (this.type == '2' && this.type_org == 'LOCAL') class_content = "person local";
                if (this.type == '2' && this.type_org == 'GESTORPSI') class_content = "person gestorpsi";
                
                tableTR += '<tr class="' + class_content + '" id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/contact/form/' + type + '/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                
                if(this.profession) tableTR += ' (' + this.profession + ')';
                
                tableTR += '<br /> ';
                
                if(this.organization) tableTR += this.organization + ' ';
                if(this.phone) tableTR +=  ' ' + this.phone;
                if(this.email) tableTR +=  ' '+ this.email;

                tableTR += '</td>';
                tableTR += '<td><span class="phone"></span><br />';
                tableTR += '<span class="email"></span></td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);
        $('div.registers_available span.object_length span').text(json['util']['object_length']);
        $('div.registers_available span.organizations_length span').text(json['util']['organizations_length']);
        $('div.registers_available span.professionals_length span').text(json['util']['professionals_length']);
        $("ul.paginator a").unbind().click(function(){
            updateContact($(this).attr('href'), deactive, app);
            return false;
        });
    });  

    return false;
}

/** 
* room list
*/


function updateRoom(url, deactive, app) {
    if (!app) app = "place/room";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/place/room/' + this.id + '/" title="' + this.name + '">' + this.name + '</a> <br />' + this.place + ' - ' + this.type  ;
                tableTR += '</td>';
                tableTR += '<td>' ;
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);
        $("ul.paginator a").unbind().click(function(){
            updateRoom($(this).attr('href'), deactive, app);
            return false;
        });
    });  

    return false;

}

/** 
* covenant list
*/

function updateCovenant(url) {

    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/covenant/' + this.id + '/edit/" title="' + this.name + '">' + this.name + '</a><br />' + this.price;
                tableTR += '</td>';
                tableTR += '<td><span class="phone">' + this.price + '</span><br />';
                tableTR += '</td>';
                tableTR += '</tr>';
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);

        /*
        $("ul.paginator a").unbind().click(function(){
            updatePlace($(this).attr('href'), deactive, app);
            return false;
        });
        */
    });  

    return false;
}

/** 
* place list
*/

function updatePlace(url, deactive, app) {
    if (!app) app = "place";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/place/' + this.id + '/" title="' + this.name + '">' + this.name + '</a><br />'+ this.type;
                tableTR += '</td>';
                tableTR += '<td><span class="phone">' + this.phone + '</span><br />';
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);
        $("ul.paginator a").unbind().click(function(){
            updatePlace($(this).attr('href'), deactive, app);
            return false;
        });
    });  

    return false;
}

/** 
* device list
*/

function updateDevice(url, deactive, app) {
    if (!app) app = "device";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/device/' + this.id + '/" title="' + this.model + '">' + this.model + ' - ' + this.name + '</a>';
                tableTR += '<br />' + this.type;
                tableTR += '</td>';
                tableTR += '<td><span class="phone"></span><br />';
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);
        $("ul.paginator a").unbind().click(function(){
            updateDevice($(this).attr('href'), deactive, app);
            return false;
        });
    });  

    return false;
}

/** 
* device type list
*/

function updateDeviceType(url, deactive, app) {
    if (!app) app = "device/type";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */
        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/device/type/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '<br />';
                tableTR += '</td>';
                tableTR += '<td><span class="phone"></span><br />';
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list_type', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list_type');
        $("ul.paginator a").unbind().click(function(){
            updateDeviceType($(this).attr('href'), deactive, app);
            return false;
        });
    });  

    return false;
}

/** 
* service list
*/

function updateService(url, deactive, app) {
    if (!app) app = "service";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/service/form/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '<br />' + this.description;
                tableTR += '</td>';
                tableTR += '<td><span class="phone"></span><br />';
                tableTR += '<span class="email"></span></td>';
                tableTR += '<td>'
                if(this.is_group) {
                    if(!json['util']['is_student']) { // include group links if not student user
                        if(this.have_client_to_list)
                            tableTR += '<a style="padding-bottom: 5px; text-decoration:none" href="/service/' + this.id + '/group/" class="group" title="Listar grupos deste serviço">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>';
                        if(this.can_add_group)
                            tableTR += '<a style="padding-bottom: 5px; text-decoration:none" href="/service/' + this.id + '/group/add/" class="group_add" title="Adicionar Grupo neste serviço">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>';
                    }
                }
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);
        $("ul.paginator a").unbind().click(function(){
            updateService($(this).attr('href'), deactive, app)
            return false;
        });
    });  

    return false;
}

/** 
* client referral list
*/

function updateReferral(url) {
    $.getJSON(url, function(json) {
        // flush list
        $('div#client_referral_list div.client_referral_list table tbody').html('');
        var tableTR = '';

        jQuery.each(json,  function(){
            var str_professional = ''; 
            var str_professional_inline = ''; 
            var str_service = '';

            str_professional_inline = personInLine(this.professional);

            /**
            * populate table
            */

            tableTR += '<tr id="' + this.id + '" class="referral_off">';
            tableTR += '<td align="left" id="' + this.id + '" class="title"><a id="'+ this.id +'" class="referral_details">' + this.service + '</a><br>' + str_professional_inline + '</td>';

            // LIGADO
            if ( (this.status) == '01'){

                tableTR += '<td class="referralKey" id="' + this.id + '">';
                tableTR += '<div class="title button_disable"> <a class="referral_off" id="' + this.id + '"href="#top' + this.id + '"> Desligar </a> </div> ';
                tableTR += '<div class="confirm_disable" style="display:none;" id="' + this.id + '">';
                tableTR += '<strong>Confirma desligamento?</strong> <br /> <a href="#teste" class="confirm_yes" id="' + this.id + '"> Sim </a> &nbsp;&nbsp; | &nbsp;&nbsp; <a class="confirm_not" id="' + this.id + '"> Nao </a> </div> </td>';

            } else { 

            // DESLIGADO
                    tableTR += '<td class="c_referral_off "><div class="referralKeyDisable"> Desligado </div></td>';

            }
            tableTR += '</tr>';

            // TABLE WITCH DETAILS OF REFERRAL OF THE CLIENT
            tableTR += '<div style="display:none;" class="referral_details' + this.id + '">';
            tableTR += '<label><p><strong> Data: </strong> ' + this.data + '</p></label>';
            tableTR += '<label><p><strong> Reason: </strong> ' + this.reason + '</p></label>';
            tableTR += '<label><p><strong> Annotation: </strong> ' + this.annotation + '</p></label>';
            tableTR += '<label><p><strong> Available time: </strong> ' + this.available_time+ '</p></label>';
            tableTR += '<label><p><strong> Priority: </strong> ' + this.priority + '</p></label>';
            tableTR += '<label><p><strong> Impact: </strong> ' + this.impact + '</p></label>';
            tableTR += '</div>';
        });

        if(tableTR == '') {
            $('div#edit_form .client_referral_list div.msg_area').show();
        }
        $('div.client_referral_list table tbody').html(tableTR);
        
        $('table.zebra tr:odd').addClass('zebra_0');
        $('table.zebra tr:even').addClass('zebra_1');

    });  

    return false;
}



/** 
* professional list
*/

function updateProfessional(url, deactive, app) {
    if (!app) app = "careprofessional";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/careprofessional/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '</td>';
                tableTR += '<td><span class="phone">' + this.phone + '</span><br />';
                tableTR += '<span class="email">' + this.email + '</span></td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);
        $("ul.paginator a").unbind().click(function(){
            updateProfessional($(this).attr('href'), deactive, app);
            return false;
        });
    });  

    return false;
}

/** 
* student list
*/

function updateStudent(url, deactive, app) {
    if (!app) app = "careprofessional/student";
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/careprofessional/student/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '</td>';
                tableTR += '<td><span class="phone">' + this.phone + '</span><br />';
                tableTR += '<span class="email">' + this.email + '</span></td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator(app, json['paginator'], json['util'], 'div#list', deactive);
        $("ul.paginator a").unbind().click(function(){
            updateStudent($(this).attr('href'), deactive, app);
            return false;
        });
    });  

    return false;
}

/***
 * service group select; details about referral , professionals
 */
function referralMultSelect(url) {
    $.getJSON(url, function(json) {
                jQuery.each(json,  function(){
                    $('form div.main_area div select#m-selectable').append(new Option(this.client + this.prof0 + this.prof1 + this.prof2 , this.id));
                });
    });
}
