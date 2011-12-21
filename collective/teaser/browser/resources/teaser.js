(function($) {

    $(document).ready(function() {
        $('div.ajax_teaser', document).each(function() {
            var elem = $(this);
            var uid = elem.attr('id').substring(7);
            $.ajax({
                url: 'ajax_teaser',
                dataType: 'html',
                data: {uid: uid},
                success: function(data) {
                    $('#teaser-' + uid).replaceWith(data);
                },
                cache: false
            });
        });
    });

})(jQuery);