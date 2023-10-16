
$(function() {
    $('#super-form').submit(function(e) {
        e.preventDefault();
        var _this = $(this)
        $('.err-msg').remove();
        var el = $('<div>')
        el.addClass("alert alert-danger err-msg")
        el.hide()
        if (_this[0].checkValidity() == false) {
            _this[0].reportValidity();
            return false;
        }
        dataku = new FormData($(this)[0]);
        commpress(el,_this);
    })
});

function commpress(el,_this){
    // var canvas = document.createElement('canvas')
    // var canvasContext = canvas.getContext('2d')
    var fileToUpload = $('#kyt_image').prop('files')[0];
    // canvas.setAttribute("style", 'opacity:0;position:absolute;z-index:-1;top: -100000000;left:-1000000000;width:320px;height:240px;')
    // document.body.appendChild(canvas);
    
    var img = new Image;
    img.onload = function() {
        var canvas = document.createElement('canvas')
        var perferedWidth = 800;
        var ratio = perferedWidth / img.width;
        canvas.width = img.width * ratio;
        canvas.height = img.height * ratio;
        var canvasContext = canvas.getContext('2d')
        canvas.setAttribute("style", 'opacity:0;position:absolute;z-index:-1;top: -100000000;left:-1000000000;width:320px;height:240px;')
        document.body.appendChild(canvas);
        canvasContext.drawImage(img, 0, 0, canvas.width, canvas.height);
            var base64Image= canvas.toDataURL('image/png')
        console.log(base64Image);
        // Post to server
        // sendImage(base64Image)
        dataku.append("uploadfile", base64Image);

        $.ajax({
            headers: {
                "X-CSRFToken": '{{csrf_token}}'
            },
            url: "{% url 'save_permohonan_perbaikan' %}",
            data: dataku,
            cache: false,
            contentType: false,
            processData: false,
            method: 'POST',
            type: 'POST',
            dataType: 'json',
            error: err => {
                console.log(err)
                alert("An error occured", 'error');
            },
            success: function(resp) {
                if (typeof resp == 'object' && resp.status == 'success') {
                    el.removeClass("alert alert-danger err-msg");
                    location.reload();
                    alert('success');
                } else if (resp.status == 'failed' && !!resp.msg) {
                    el.text(resp.msg)
                } else {
                    el.text("An error occured", 'error');
                }
                _this.prepend(el)
                el.show('slow')
                $("html, body, .modal").scrollTop(0);
            }
        })


        document.body.removeChild(canvas)
        URL.revokeObjectURL(img.src)

    }
    // console.log(fileToUpload);
    img.src = URL.createObjectURL(fileToUpload);
};