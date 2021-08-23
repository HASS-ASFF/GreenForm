
     var SaveForm_membre =  function(){
 		var form = $(this);
 		data = []
 		contentType= false
 		processData = false
 		var string = form.attr("data-url")
 		
 		
 		data = form.serialize()
 		contentType= "application/x-www-form-urlencoded; charset=UTF-8"
 		processData = true

 		$.ajax({

 			url: form.attr('data-url'),
 			contentType: contentType,
 			processData: processData,
 			data : data,
 			type: form.attr('method'),
 		    dataType: 'json',
 			cache : false,
 		    enctype: 'multipart/form-data',
 			success: function(data){
 				if(data.form_is_valid){
 					$('#modal-membre').modal('hide');
                     setTimeout(function(){
                                 location.reload(); 
                            }, 50); 
                    
 				} else {					
 					$('#modal-membre .modal-content').html(data.html_form)

 				}
 			},
 			error: function(xhr, errmsg, err) {
 				console.log(xhr.status + ":" + xhr.responseText)
 			}
 		})
 		return false;
 	}



 ShowForm_membre = function(){
     btn = $(this);
     $.ajax({
         url: btn.attr("data-url"),
         type: 'GET',
         dataType:'json',
         beforeSend: function(){
             $('#modal-membre').modal('show');
         },
         success: function(data){
             $('#modal-membre .modal-content').html(data.html_form);
         }
     });
 };

// //--------------------------------------------MEMBRE(PERSONNE)


// //delete
 $('#pers-table').on("click",".show-form-delete",ShowForm_membre);
 $('#modal-membre').on("submit",".delete-form-pers",SaveForm_membre);

// //--------------------------------------------MEMBRE(CENTRE)

// //delete
 $('#centr-table').on("click",".show-form-delete",ShowForm_membre);
 $('#modal-membre').on("submit",".delete-form-centre",SaveForm_membre);
