/**
 * Collects and stores the survey responses from the particpants after the
 * experiement has run to completion.
 */

jsPsych.plugins["post-survey"] = (function() {

  var plugin = {};

  plugin.info = {
    name: "post-survey",
    parameters: {
    }
  }

  plugin.trial = function(display_element, trial) {

    // Load content
    var content = $('#survey').html();
    $(display_element).html(content);
    
    // Save response
    $(display_element).find('.submit').click(function(e){
        e.preventDefault();
        
        var trial_data = {
            language : $(display_element).find('#survey-language').val(),
            enjoyment : $(display_element).find('input[name="survey-enjoy"]:checked').val(),
            assess : $(display_element).find('input[name="survey-instructions"]:checked').val(),
            age : $(display_element).find("#survey-age").val(),
            gender_cat : $(display_element).find('input[name="survey-gender"]:checked').val(),
            gender_text: $(display_element).find('#gender-other').val(),
            education : $(display_element).find('input[name="survey-education"]:checked').val(),
            comments : $(display_element).find("#survey-comments").val(),
        };
                
        // Save data
        $(display_element).html('');
        jsPsych.finishTrial(trial_data);
    });
  };

  return plugin;
})();
