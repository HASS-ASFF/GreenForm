
    var SaveForm_personne =  function(){
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
					$('#modal-pers').modal('hide');
                    setTimeout(function(){
                                location.reload(); 
                           }, 50); 
                    
				} else {					
					$('#modal-pers .modal-content').html(data.html_form)

				}
			},
			error: function(xhr, errmsg, err) {
				console.log(xhr.status + ":" + xhr.responseText)
			}
		})
		return false;
	}

//--------------------------------------------MEMBRE(PERSONNE)

ShowForm_personne = function(){
    btn = $(this);
    $.ajax({
        url: btn.attr("data-url"),
        type: 'GET',
        dataType:'json',
        beforeSend: function(){
            $('#modal-pers').modal('show');
        },
        success: function(data){
            $('#modal-pers .modal-content').html(data.html_form);
        }
    });
};

$(".show-form").click(ShowForm_personne);
$("#modal-pers").on("submit",".create-form",SaveForm_personne);

//update
$('#pers-table').on("click",".show-form-update",ShowForm_personne);
$('#modal-pers').on("submit",".update-form",SaveForm_personne);

//delete
$('#pers-table').on("click",".show-form-delete",ShowForm_personne);
$('#modal-pers').on("submit",".delete-form",SaveForm_personne);



//--------------------------------------------MEMBRE(CENTRE)


var SaveForm_centre =  function(){
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
				$('#modal-centr').modal('hide');
				setTimeout(function(){
							location.reload(); 
					   }, 50); 
				
			} else {					
				$('#modal-centr .modal-content').html(data.html_form)

			}
		},
		error: function(xhr, errmsg, err) {
			console.log(xhr.status + ":" + xhr.responseText)
		}
	})
	return false;
}

ShowForm_centre = function(){
    btn = $(this);
    $.ajax({
        url: btn.attr("data-url"),
        type: 'GET',
        dataType:'json',
        beforeSend: function(){
            $('#modal-centr').modal('show');
        },
        success: function(data){
            $('#modal-centr .modal-content').html(data.html_form);
        }
    });
};

$(".show-form").click(ShowForm_centre);
$("#modal-centr").on("submit",".create-form",SaveForm_centre);

//update
$('#centr-table').on("click",".show-form-update",ShowForm_centre);
$('#modal-centr').on("submit",".update-form",SaveForm_centre);

//delete
$('#centr-table').on("click",".show-form-delete",ShowForm_centre);
$('#modal-centr').on("submit",".delete-form",SaveForm_centre);
