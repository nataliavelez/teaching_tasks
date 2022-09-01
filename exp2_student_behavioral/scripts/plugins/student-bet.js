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

jsPsych.plugins["student-bet"] = (function() {

    var plugin = {};
  
    plugin.info = {
      name: "student-bet",
      parameters: {
        num_trial : { 
            type: jsPsych.plugins.parameterType.Object,
            default: undefined
        },
        num_hint : {
            type: jsPsych.plugins.parameterType.INTEGER,
            default: undefined
        },
        betting_priors: {
            type: jsPsych.plugins.parameterType.FUNCTION,
            default: undefined
        },
        total_hints: {
            type: jsPsych.plugins.parameterType.INTEGER,
            default: undefined
        }
      }
    }
  
    plugin.trial = function(display_element, trial) {
    
        const hint = hints[trial.num_trial];
        const hint_state = hint["states"][trial.num_hint];
        const hypothesis_order = hint["order"];
        const problem = hint["problem"];
        const problem_states = problems[problem];
        let bets = Array.from(trial.betting_priors());

        /**
         * Helper function that returns the sum of all the current bets since
         * there is no built-in sum operator for lists in JavaScript.
         *      
         * @return {Integer} sum over all the bets currently placed on the
         *     bettting sliders
         */
        function get_bet_sums() {
            let sum = 0;
            for (let i = 0; i < bets.length; i++) {
                sum += bets[i]
            }
            return sum;
        };

        /**
         * When a slider's change event listener is triggered, this function 
         * handles the new betting by doing the following: 
         * 
         * (1) Calculates the new betting total.
         * (2) If the new betting total is equal to 100, change the tally box 
         *     to green, enable the "Place Bets" button, and, when pressed,
         *     store, write the trial data, and finish trial.
         * (3) If the new betting total is not equal 100, change the tally box 
         *     to red and disable the "Place Bets" button.
         * 
         * @param {Integer} slider_indx the slider index that indentifies which 
         *     slider has changed and corresponds to the slider indices in 
         *     hypothesis ordering and bets
         * @param {Integer} new_bet The new bet that the partcipant made
         */ 
          function handle_betting(slider_indx, new_bet) {

            bets[slider_indx] = new_bet;

            const betting_total = get_bet_sums();
            const button = $(display_element).find('button');

            button.prop('disabled', false); 
            button.unbind('click'); 
            button.one('click', function(e){ 
                e.preventDefault();
                var reset_sliders = false;

                // Calculate bonus
                max_trial_bonus = max_block_bonus/trial.total_hints;
                final_bet_total = get_bet_sums();

                // Special case: If all bets are zero, reset to a uniform prior
                if (final_bet_total == 0) {
                    reset_sliders = true;
                    bets = [25, 25, 25, 25]
                    final_bet_total = 100;
                }

                bets_rescaled = $.map(bets, function(b){
                    return b/final_bet_total
                });
                correct_bet = hypothesis_order.indexOf('A');
                trial_bonus = max_trial_bonus*bets_rescaled[correct_bet];
                
                // Save data
                const trial_data = {
                    teacher: hints[trial.num_trial]["teacher"],
                    problem: problem,
                    num_trial: trial.num_trial,
                    num_hint: trial.num_hint,
                    bets: bets,
                    bonus: trial_bonus
                };
                jsPsych.finishTrial(trial_data);
            });
        };

        let content = $('#templates #student-betting').html();
        let hint_prompt = '';
        let button_text = '';

        // Customize the prompts based on what number (0-2) hint they are on.
        if (jsPsych.pluginAPI.compareKeys(trial.num_hint, 0)) {
            hint_prompt = 'Here is the first hint the teacher picked out:';
            button_text = 'Next hint';
        } else if (jsPsych.pluginAPI.compareKeys(trial.num_hint, trial.total_hints)) {
            hint_prompt = 'Here is the last hint the teacher picked out:';
            button_text = 'Next hint';
        } else {
            hint_prompt = 'Here is the second hint the teacher picked out:';
            button_text = 'Next problem';
        }
  
        let bet_prompt = 'What is the probability that each of these options \
          is the right answer? (Note: Please place your bets by moving the\
          sliders.)';
        let total_text = 'Total: ' + get_bet_sums();

        content = sprintf(content, trial.num_trial + 1 , num_trials, hint_prompt, bet_prompt);
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
            
            $.each(hypothesis.find('tr'), function(row){
                $.each($(this).find('td'), function(col){
                    if (hypothesis_data[row][col] > 0) {
                        $(this).addClass('pos');
                    };
                });
            });
        });

        // Initialize all the betting sliders for each hypothesis (option) with 
        // the appropriate values (uniform betting priors or participant's 
        // previously bets) and link each slider to an event listener that 
        // handles any new bets.
        var hypothesis_labels = ['A', 'B', 'C', 'D'];
        
        for (let indx = 0; indx < hypothesis_labels.length; indx++) {
            new Slider("#" + hypothesis_labels[indx] + "-betting-slider",{
                value: bets[indx],
                tooltip: "hide"
            }).on('change', function (event) {
                handle_betting(indx, event.newValue);
            });
        };
    };
  
    return plugin;
  })();
  