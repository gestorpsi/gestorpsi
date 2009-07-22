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
* client list
*/


function updateClient(url) {
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/client/' + this.id + '/home/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '</td>';
                tableTR += '<td><span class="phone">' + this.phone + '</span><br />';
                tableTR += '<span class="email">' + this.email + '</span></td>';
                tableTR += '<td>';
                tableTR += '<a class="admit" href="/admission/' + this.id + '/" title="' + this.name + '"><img src="/media/img/22/ico_reg.png"></a>';
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator('client', json['paginator'], json['util'], 'div#list');

        $("ul.paginator a").unbind().click(function(){
            updateClient($(this).attr('href'))
            return false;
        });
    });  

    return false;
}

/** 
* user list
*/

function updateUser(url) {
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
        buildPaginator('user', json['paginator'], json['util'], 'div#list');
        $("div#list ul.paginator a").unbind().click(function(){
            updateUser($(this).attr('href'))
            return false;
        });
    });  

    return false;
}

/** 
* employee list
*/

function updateEmployee(url) {
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
        buildPaginator('employee', json['paginator'], json['util'], 'div#list');
        $("div#list ul.paginator a").unbind().click(function(){
            updateEmployee($(this).attr('href'))
            return false;
        });
    });  

    return false;
}

/** 
* contact list
*/

function updateContact(url) {
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                //tableTR += '<tr id="' + this.id + '"><td class="title">';

                if (this.type == '1'){ 
                    if (this.type_org == 'LOCAL'){
                        tableTR += '<tr class="clinic local" id="' + this.id + '"><td class="title">';
                        tableTR += '<a href="/contact/' + this.type + '/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                    } else {
                        tableTR += '<tr class="clinic gestorpsi" id="' + this.id + '"><td class="title">';
                        tableTR += '<a  href="/contact/' + this.type + '/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                    }
                } else {
                    if (this.type_org == 'LOCAL'){
                        tableTR += '<tr class="person local" id="' + this.id + '"><td class="title">';
                        tableTR += '<a  href="/contact/' + this.type + '/' + this.id + '/" title="' + this.name + '">' + this.name + '</a><br />' + this.organization;
                    } else {
                        tableTR += '<tr class="person gestorpsi" id="' + this.id + '"><td class="title">';
                        tableTR += '<a  href="/contact/' + this.type + '/' + this.id + '/" title="' + this.name + '">' + this.name + "  ( " + this.profession + " ) " + '</a><br />' + this.organization;
                    }
                }

                tableTR += '</td>';
                tableTR += '<td><span class="phone"></span><br />';
                tableTR += '<span class="email"></span></td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator('contact', json['paginator'], json['util'], 'div#list');
        $('div.registers_available a.object_length span').text(json['util']['object_length']);
        $('div.registers_available a.organizations_length span').text(json['util']['organizations_length']);
        $('div.registers_available a.professionals_length span').text(json['util']['professionals_length']);
        $("ul.paginator a").unbind().click(function(){
            updateContact($(this).attr('href'))
            return false;
        });
    });  

    return false;
}

/** 
* room list
*/


function updateRoom(url) {

    $.getJSON(url, function(json) {
        var tableTR = '';
        
        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/place/room/' + this.id + '/" title="' + this.name + '">' + this.name + '</a> <br />' + this.place ;
                tableTR += '</td>';
                tableTR += '<td>' ;
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator('place/room', json['paginator'], json['util'], 'div#list');
        $("div#list ul.paginator a").unbind().click(function(){
            updateRoom($(this).attr('href'))
            return false;
        });
    });  

    return false;

}

/** 
* place list
*/

function updatePlace(url) {
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/place/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '</td>';
                tableTR += '<td><span class="phone">' + this.phone + '</span><br />';
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator('place', json['paginator'], json['util'], 'div#list');
        $("div#list ul.paginator a").unbind().click(function(){
            updatePlace($(this).attr('href'))
            return false;
        });
    });  

    return false;
}

/** 
* device list
*/

function updateDevice(url) {
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/device/' + this.id + '/" title="' + this.model + '">' + this.name + ' ' + this.model + '</a>';
                tableTR += '<br />' + this.type;
                tableTR += '</td>';
                tableTR += '<td><span class="phone"></span><br />';
                tableTR += '</td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator('device', json['paginator'], json['util'], 'div#list');
        $("div#list ul.paginator a").unbind().click(function(){
            updateDevice($(this).attr('href'))
            return false;
        });
    });  

    return false;
}

/** 
* device type list
*/

function updateDeviceType(url) {
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
        buildPaginator('device/type', json['paginator'], json['util'], 'div#list_type');
        $("div#list_type ul.paginator a").unbind().click(function(){
            updateDeviceType($(this).attr('href'))
            return false;
        });
    });  

    return false;
}

/** 
* service list
*/

function updateService(url) {
    $.getJSON(url, function(json) {
        var tableTR = '';
        
        /**
        * build html
        */

        jQuery.each(json,  function(){
            if(this.id) {
                tableTR += '<tr id="' + this.id + '"><td class="title">';
                tableTR += '<a href="/service/' + this.id + '/" title="' + this.name + '">' + this.name + '</a>';
                tableTR += '<br />' + this.description;
                tableTR += '</td>';
                tableTR += '<td><span class="phone"></span><br />';
                tableTR += '<span class="email"></span></td>';
                tableTR += '<td><a style="padding-bottom: 5px; text-decoration:none" href="/service/' + this.id + '/group/" class="list" title="Listar grupos deste serviço">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>';
                tableTR += '<a style="padding-bottom: 5px; text-decoration:none" href="/service/' + this.id + '/group/add/" class="add" title="Adicionar Grupo neste serviço">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></td>';
                tableTR += '</tr>';
            }
        });

        buildTableList(tableTR, 'div#list', json['util']['has_perm_read']);
        buildPaginator('service', json['paginator'], json['util'], 'div#list');
        $("div#list ul.paginator a").unbind().click(function(){
            updateService($(this).attr('href'))
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
* professional referral list
*/

function updateProfessional(url) {
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
        buildPaginator('careprofessional', json['paginator'], json['util']);
        $("div#list ul.paginator a").unbind().click(function(){
            updateProfessional($(this).attr('href'))
            return false;
        });
    });  

    return false;
}


