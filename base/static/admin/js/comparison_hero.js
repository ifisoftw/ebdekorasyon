/**
 * Singleton checkbox behavior for is_comparison_hero field
 * When one checkbox is checked, all others in the same column are unchecked
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        // Find all is_comparison_hero checkboxes in the list view
        const checkboxes = document.querySelectorAll('input[name$="-is_comparison_hero"]');

        if (checkboxes.length === 0) return;

        checkboxes.forEach(function (checkbox) {
            checkbox.addEventListener('change', function () {
                if (this.checked) {
                    // Uncheck all other checkboxes in this column
                    checkboxes.forEach(function (other) {
                        if (other !== checkbox) {
                            other.checked = false;
                        }
                    });
                }
            });
        });
    });
})();
