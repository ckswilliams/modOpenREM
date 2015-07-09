$(document).ready(function(){
    $('#main-menu a').click(function (event) {
        // Prevents the default behavior which is
        // to load the page synchronously
        event.preventDefault();

        $('#main-ajax').load(this.href + ' #sharemenu *', function (data, status) {
            $bar = $('#notification-bar');

            if (status === 'success') {
                $bar.text('The page has been successfully loaded.');
            } else {
                $bar.text('An error occurred.');
            }

            $bar
                .slideDown('normal')
                .delay(2000)
                .slideUp('fast');
        });
    });
});
