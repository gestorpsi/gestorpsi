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
 * verify mozilla user
 */

$(document).ready(function(){
  $('body').hide();
  
  if(!$.browser.mozilla) {
      $('div.login .ff_ok').hide();
      $('div.login div.ff_not_ok').show();
  }
  
  $('body').fadeIn(1000);
 
  $('div.login div.ff_not_ok a.login_unlock').click(function() {
      $('div.login div.ff_not_ok').hide();
      $('div.login .ff_ok').fadeIn(1000);
  });
});



