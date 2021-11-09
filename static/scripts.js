$("form[name=signup_form").submit(function(e) {

    let $form = $(this);
    let $error = $form.find(".error");
    let data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        
    })

    e.preventDefault();
})