/** Global admin object **/
mbbAdmin = {
    color: {
        'green': '#00a65a',
        'gray': '#999999',
        'orange': '#f39c12',
        'red': '#dd4b39',
    },
    list_colors: function (colors, selector) {
        $.each(colors, function (key, value) {
            $('td.field-' + selector + ':contains("' + key + '")')
                .css('color', value);
            $('.admin-filter-' + selector + ' a:contains("' + key + '")')
                .css('color', value);
        });
    },
};

$(document).ready(function ($) {
    'use strict';
    $('.sortedm2m-items a').click(function (event) {
        event.preventDefault();
        $(this).prev('input').trigger('click');
    });
    $('.vTimeField').inputmask({
        mask: '99:99:99',
    });
    $('.vDateField').inputmask({
        mask: '9999-99-99',
    });

    // admin filter select
    (function () {
        $('.admin-filter-select').change(function () {
            window.location.href = $(this).val();
        });
    }());
});
