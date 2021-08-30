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

	 $('.btn-sign-up-step-2').on('click', function(){
		 $('.step-1').fadeOut();
		 $('.step-2').fadeIn();
	 })

	 $('.btn-sign-back-2').on('click', function(){
		 $('.step-2').fadeOut();
		 $('.step-1').fadeIn();
	 })
     $('.step-2').hide();
		
			$('.type-membre').on('change', function(){
				var selectedValue = $(this).val();
				
				if(selectedValue == 1 ){
					$('.person-fields').hide();
					$('.formation_center-fields').show();
					$('.formation_center-fields-step-1').show()
					$('.formation_center-fields-step-2').hide();
	
				}
				if(selectedValue == 2){
					$('.formation_center-fields').hide();
					$('.person-fields').show();
					$('.person-fields-step-1').show()
					$('.person-fields-step-2').hide();
				}
			});
		//});

		$('.back-step-1-btn').on('click', function(e){
			 $('.step-2').fadeOut();
			 $('.step-1').fadeIn();
		})
		$('.formation_center-fields-step-1-btn').on('click', function(e){
			$('.formation_center-fields-step-1').fadeOut();
			$('.formation_center-fields-step-2').fadeIn();
		});

		$('.formation_center-fields-back-btn').on('click', function(e){
			$('.formation_center-fields-step-2').fadeOut();
			$('.formation_center-fields-step-1').fadeIn();
		});

		$('.person-fields-step-1-btn').on('click', function(e){
			$('.person-fields-step-1').fadeOut();
			$('.person-fields-step-2').fadeIn();
		});

		$('.person-fields-back-btn').on('click', function(e){
			$('.person-fields-step-2').fadeOut();
			$('.person-fields-step-1').fadeIn();
		});

		$('#sign-up-person').on('click', function(e){
			e.preventDefault();
			$('.username_center').remove();
			$('.password_center').remove();
			$('.password2_center').remove();
			$('.email_center').remove();
			$('.nom_center').remove();
			$('.respo_center').remove();
			$('.type_center').remove();
			$('.postal_code_center').remove();
			$('#sign-up-formation_center').remove();
			$("#register-form-1").submit();
		});

		function getFormData($form){
			var unindexed_array = $form.serializeArray();
			var indexed_array = {};
		
			$.map(unindexed_array, function(n, i){
				indexed_array[n['name']] = n['value'];
			});
		
			return indexed_array;
		}
		$('#sign-up-formation_center').on('click', function(e){
			e.preventDefault();

			$('.username_personne').remove();
			$('.password_personne').remove();
			$('.password2_personne').remove();
			$('.email_personne').remove();
			$('.nom_personne').remove();
			$('.prenom_personne').remove();
			$('.sexe_personne').remove();
			$('.adresse_personne').remove();
			$('.num_tel_personne').remove();
			$('.type_personne').remove();
			$('.postal_code_personne').remove();
			$('#sign-up-person').remove();
			//var data1 = getFormData($("#register-form-1"));
			$("#register-form-1").submit();
			var form_data = $("#register-form-1").serialize();
		})
	 });
