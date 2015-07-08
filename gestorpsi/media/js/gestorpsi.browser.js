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

$(document).ready(function(){

  /**
   * if found any version of browser MSIE
   */

	var userAgent = navigator.userAgent.toLowerCase(); 
	$.browser.msie = /msie/.test(navigator.userAgent.toLowerCase());

	if($.browser.msie)
	{
		$('div.login .browser_alert').show();
	}

});
