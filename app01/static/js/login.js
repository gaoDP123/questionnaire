// 刷新验证码
    $(".valide_img").click(function () {
        $(".valide_img")[0].src +="?"
    });
//登录验证
    $("#login").click(function () {
        $.ajax({
            url:"/log_in/",
            type:"POST",
            data:{
                "csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val(),
                "username":$("#username").val(),
                "password":$("#password").val(),
                "valid_code":$("#valid_code").val()
            },
            success:function (data) {
                console.log(data);
                var response=JSON.parse(data);
                if (response["is_login"]){
                    location.href="/index/"
                }
                else {
                    $(".error").html(response["error_msg"]).css("color","red")
                }
            }
        })
    });