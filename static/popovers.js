document.addEventListener('DOMContentLoaded', function() {
  // Initialize popovers
  var popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
  var popoverList = [].slice.call(popoverTriggerList).map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
});