function clearForm(formId) {
  var form = document.getElementById(formId);

  // Clear all input fields except the investigation_id field
  var inputs = form.querySelectorAll('input[type="text"], input[type="datetime-local"], input[type="file"], textarea');
  inputs.forEach(function(input) {
    if (input.name !== 'investigation_id' && input.name !== 'task_id') {
      input.value = '';
    }
  });

  // Reset select fields to their default option
  var selectElements = form.querySelectorAll('select');
  selectElements.forEach(function(select) {
    select.selectedIndex = 0;
  });
}
