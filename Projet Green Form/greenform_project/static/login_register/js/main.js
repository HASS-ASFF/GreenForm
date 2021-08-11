$(function() {
	'use strict';

	
  $('.form-control').on('input', function() {
	  var $field = $(this).closest('.form-group');
	  if (this.value) {
	    $field.addClass('field--not-empty');
	  } else {
	    $field.removeClass('field--not-empty');
	  }
	});
	$('.form-link').on( 'click',  function(e){
	
		$('form').animate({height: "toggle", opacity: "toggle"}, "slow");
	
	 });
});








