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
 * array to string util function
 */

function personInLine(list) {
    
    var str = ''
    
    //append person list
    if(list) {
    jQuery.each(list,  function(){
        str = str + this.name + ", " ;
    });
    str = str.substr(0, (str.length-2))
    }
    return str
    
}



/**
 * calula idade
 */

function datOuIdade() {
    if (document.getElementById('aprox').checked==false) {
        document.getElementById('Anos').disabled=true;
        document.getElementById('Anos').value="";
        document.getElementById('dataNasc').disabled=false;
    }else{
        document.getElementById('dataNasc').disabled=true;
        document.getElementById('dataNasc').value="";
        document.getElementById('Anos').disabled=false;
    }
}
function calculaidade() {

    dNasc = document.getElementById('dataNasc').value;
    x = dNasc.split("/");
    var mm = x[1];
    var dd = x[0];
    var yy = x[2];
    
    var thedate = new Date()
    var mm2 = thedate.getMonth() + 1;
    var dd2 = thedate.getDate();
    var yy2 = thedate.getFullYear();
    
    var yourage = yy2 - yy
        if (mm2 < mm) {
        yourage = yourage - 1;
        }
        if (mm2 == mm) {
            if (dd2 < dd) {
            yourage = yourage - 1;
            }
        }
    return yourage;
}
function calculaData() {
    idade = document.getElementById('Anos').value;
    
    var thedate = new Date()
    var mm2 = thedate.getMonth() + 1;
    var dd2 = thedate.getDate();
    var yy2 = thedate.getFullYear();
    
    var anoNasc = yy2 - idade;
    
    var dtNasc = dd2 + "/" + mm2 + "/" + anoNasc;
    return dtNasc;

}

function displayAge() {
    if (document.getElementById('dataNasc').value == "") {
        document.getElementById('dataNasc').value = calculaData();
    }else{
        document.getElementById('Anos').value = calculaidade();
    }
}

