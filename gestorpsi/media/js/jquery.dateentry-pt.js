/* http://keith-wood.name/dateEntry.html
   Portuguese initialisation for the jQuery date entry extension
   Written by Dino Sane (dino@asttra.com.br) and Leonildo Costa Silva (leocsilva@gmail.com). */
(function($) {
	$.dateEntry.regional['pt'] = {dateFormat: 'dmy/',
		monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
		'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
		monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun',
		'Jul','Ago','Set','Out','Nov','Dez'],
		dayNames: ['Domingo','Segunda-feira','Terça-feira',
		'Quarta-feira','Quinta-feira','Sexta-feira','Sábado'],
		dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'],
		spinnerTexts: ['Agora', 'Campo anterior', 'Campo Seguinte', 'Aumentar', 'Diminuir']};
	$.dateEntry.setDefaults($.dateEntry.regional['pt']);
})(jQuery);
