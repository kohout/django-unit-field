"use strict";

(function($) {

    $(document).ready(function() {
        $('.unit-field-input').each(function() {

            // retrieve DOM objects
            var $input = $(this);
            var $unit = $input.nextAll('select').eq(0);

            // required methods
            var preventFloatOszillation = function(value, digits) {
                var _d = Math.pow(10, digits);
                return (Math.round(value * _d) / _d);
            };

            var saveCurrentUnit = function() {
                $input.data('current-unit', $unit.val());
                $input.data('current-input', $input.val());
            };

            var updateUnit = function() {
                var old_input = parseFloat($input.data('current-input'));
                var old_unit  = parseFloat($input.data('current-unit'));
                var new_unit  = parseFloat($unit.val());

                $input.val(preventFloatOszillation(
                    old_input * old_unit / new_unit, 15));

                saveCurrentUnit();
            };

            // add event handler
            $input.change(function() { saveCurrentUnit(); });
            $unit.change(function() { updateUnit(); });

            // initialize the input field
            saveCurrentUnit();
        });
    });

})(jQuery);
