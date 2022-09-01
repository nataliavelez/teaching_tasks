/*
 * Example plugin template
 */

jsPsych.plugins["consent"] = (function() {

  var plugin = {};

  plugin.info = {
    name: "consent",
    parameters: {
    }
  }

  plugin.trial = function(display_element, trial) {
    // Fill in page
    var content = $('#templates #consent').html();
    $(display_element).html(content);
    $(display_element).addClass('consent');

    // Key elements in consent form
    var checkbox = $(display_element).find('input[type="checkbox"]');
    var cont_btn = $(display_element).find('button');

    // Activate button when checkbox is ticked
    $(display_element).find('input[type="checkbox"]').on('click', function(){
      if (this.checked) {
        cont_btn.prop('disabled', false);
        cont_btn.one('click', function(){
          
          // Save data
          var trial_data = {
            consent: checkbox.prop('checked')
          };

          // End trial
          $(display_element).removeClass('consent');
          jsPsych.finishTrial(trial_data);

        });

      } else {
        // Disable if participant unchecks
        cont_btn.unbind('click');
        cont_btn.prop('disabled', true);

      }
    })
    
  };

  return plugin;
})();
