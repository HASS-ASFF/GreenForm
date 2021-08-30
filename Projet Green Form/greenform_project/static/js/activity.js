
    var SaveForm =  function(){
		var form = $(this);
		data = []
		contentType= false
		processData = false
		var string = form.attr("data-url")
		if(string.includes("modify")){
			formData = new FormData(this);
			data = formData
		}
		else {
			data = form.serialize()
		    contentType= "application/x-www-form-urlencoded; charset=UTF-8"
			processData = true
		}
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
					$('#modal-act').modal('hide');
                    setTimeout(function(){
                                location.reload(); 
                           }, 50); 
                    
                    
				} else {					
					$('#modal-act .modal-content').html(data.html_form)

				}
			},
			error: function(xhr, errmsg, err) {
				console.log(xhr.status + ":" + xhr.responseText)
			}
		})
		return false;
	}

//--------------------------------------------ACTIVITY 

    ShowForm = function(){
        btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'GET',
            dataType:'json',
            beforeSend: function(){
                $('#modal-act').modal('show');
            },
            success: function(data){
                $('#modal-act .modal-content').html(data.html_form);
            }
        });
    };

    $(".show-form").click(ShowForm);

    $("#modal-act").on("submit",".create-form",SaveForm);

    //update
    $('#act-table').on("click",".show-form-update",ShowForm);
    $('#modal-act').on("submit",".update-form",SaveForm);

    //delete
    $('#act-table').on("click",".show-form-delete",ShowForm);
    $('#modal-act').on("submit",".delete-form",SaveForm);

	//participate
	$('#act-table').on("click",".form-participate",ShowForm);
	$('#modal-act').on("submit",".act-form-part",SaveForm);

	//view details
	$('#act-table').on("click",".form-details",ShowForm);
