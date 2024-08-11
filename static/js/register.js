$(function () {
    function bindCaptchaBtnClick() {
        $('#captcha-btn').click(function (event) {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert('please enter email');
                return;
            }
            $this.off('click');

            $.ajax('/auth/captcha?email=' + email, {
                method: 'GET',
                success: function (result) {
                    if (result['code'] == 200) {
                        alert('Captcha send successfully!');
                    } else {
                        alert(result['message'])
                    }
                },
                fail: function (error) {
                    console.log(error);
                }
            })

            let countdown = 6;
            let timer = setInterval(function () {
                if (countdown <= 0) {
                    $this.text('Get Captcha');
                    clearInterval(timer);
                    bindCaptchaBtnClick();
                } else {
                    countdown--;
                    $this.text(countdown + 's');

                }

            }, 1000);
        })
    }

    bindCaptchaBtnClick();
});