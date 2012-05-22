(function($)
{
	$(document).ready(function()
	{
		$('input').each(function()
		{
			var mask = $(this).attr('mask')+'';
			if( mask != 'undefined' && mask.length > 0 )
			{
				$(this).mask(mask);
			}
		});
	});
})(django.jQuery);