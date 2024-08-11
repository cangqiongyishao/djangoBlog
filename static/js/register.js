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