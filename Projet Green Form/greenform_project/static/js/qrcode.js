
ShowForm = function(){
    btn = $(this);
    $.ajax({
        url: btn.attr("data-url"),
        type: 'GET',
        dataType:'json',
        beforeSend: function(){
            $('#modal-qrcode').modal('show');
        },
        success: function(data){
            $('#modal-qrcode .modal-content').html(data.html_form);
        }
    });
};



$(".show-img-qrpers").click(ShowForm);
$(".show-img-qrcentr").click(ShowForm);