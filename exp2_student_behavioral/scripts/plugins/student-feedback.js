/**
 * Student bet is a plug-in that handles a single hint of a student betting
 * problem.
 * 
 * @param {Object} num_trial The trial number that the participant is on (i.e. 
 *   how many problems they have seen thus far). Used since problems are
 *   presented nonsequentially.
 * @param {Integer} num_hint The hint number (0-2) that the partcipant is seeing 
 *   for the specific problem. Hint x means that the participant is seeing x
 *   revealed squares from the teacher for a single problem. 
 * @param {Function} betting_priors A function that returns a uniform prior
 *   meaning there there are 25 chips placed on each hypothesis) for the first
 *   hint (num_hint = 0) or returns the previous betting strategy that the 
 *   particant gave (3 > num_hint > 0). Bets are in the hypothesis order. 
 * 
 * The return statements below are what get written to the data when the trial
 * of this plug-in type finishes (when the participant places their 100 chips
 * as their betting strategy across all four hypotheses). The plugin actually
 * returns itself at the end.
 * 
 * @return {Integer} teacher    Teacher assigned for this problem.
 * @return {Integer} problem    Problem assigned
 * @return {Integer} num_trial    The trial number that the participant is on
 *   (i.e. the total number of problems they have seen so far). Used since 
 *   problems are presented nonsequentially and trial_index is for the whole
 *   experiment)
 * @return {Integer} num_hint     The hint number (0-2) that the partcipant is
 *   seeing for the specific problem. Hint x means that the participant is 
 *   seeing x revealed squares from the teacher for a single problem.
 * @return {!Array<Integer>} bets   Student bets stored in the hypothesis
 *   order. 
 */

 jsPsych.plugins["student-feedback"] = (function() {

    var plugin = {};
  
    plugin.info = {
      name: "student-feedback",
      parameters: {
        num_trial : { 
            type: jsPsych.plugins.parameterType.INTEGER,
            default: undefined
        },
        num_hint : {
            type: jsPsych.plugins.parameterType.INTEGER,
            default: undefined
        },
        final_bets: {
            type: jsPsych.plugins.parameterType.OBJECT,
            default: undefined
        },
        block_bonus: {
            type: jsPsych.plugins.parameterType.FLOAT,
            default: undefined
        },
        running_total: {
            type: jsPsych.plugins.parameterType.FLOAT,
            default: undefined
        }
        }
    }
  
    plugin.trial = function(display_element, trial) {

        const hint = hints[trial.num_trial];
        const hint_state = hint["states"][trial.num_hint-1];
        const hypothesis_order = hint["order"];
        const problem = hint["problem"];
        const problem_states = problems[problem];
        let bets = trial.final_bets;

        let content = $('#templates #student-feedback').html();
        let hint_prompt = '';
        let button_text = '';

        content = sprintf(content, trial.num_trial + 1 , num_trials, trial.block_bonus, trial.running_total);
        $(display_element).html(content);

        // Draw the teacher's hint by iterating over rows and columns of the 
        // canvas space.
        let canvas = $(display_element).find('.student-canvas'); 
        $.each(canvas.find('tr'), function(row){
            $.each($(this).find('td'), function(col){
                if (hint_state[row][col]) {
                    $(this).addClass('selected');
                };
            });
        });

        // Draw the hypotheses (a.k.a. the options for students to bet on) by 
        // iterating over rows and columns of the hypothesis space.
        let hypotheses = $(display_element).find('.hypothesis-wrapper'); 
        $.each(hypotheses, function(i){
            const hypothesis_key = hypothesis_order[i];
            const hypothesis_data = problem_states[hypothesis_key];
            let hypothesis = $(this).find('.hypothesis');

            // highlight true hypothesis
            if (hypothesis_key == 'A') {
                $(this).addClass('true');
            }
            
            // fill in examples
            $.each(hypothesis.find('tr'), function(row){
                $.each($(this).find('td'), function(col){
                    if (hypothesis_data[row][col] > 0) {
                        $(this).addClass('pos');
                    };
                });
            });
        });

        // End trial after 3 seconds
        setTimeout(function(){
            jsPsych.finishTrial();
        }, 3000);

    };
  
    return plugin;
  })();
  