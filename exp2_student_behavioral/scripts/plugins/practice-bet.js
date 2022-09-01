/**
 * Practice bet is a plug-in that handles a practice trial of a student betting
 * problem.
 * 
 * Instead of iterating over the canvas and hypothesis space here, the canvas
 * and hypothesis space is already pre-filled in the practice-prolem div in 
 * the "index.html" file. 
 * 
 * There are no parameters or trial data written.
 */

jsPsych.plugins["practice-bet"] = (function() {

    var plugin = {};
  
    plugin.info = {
      name: "practice-bet",
      parameters: {}
    }
  
    plugin.trial = function(display_element, trial) {
        
        let bets = Array.from(uniform_betting_priors);

        /**
         * When a slider's change event listener is triggered, this function 
         * handles the new betting by doing the following: 
         * 
         * (1) Calculates the new betting total.
         * (2) If the new betting total is equal to 100, change the tally box 
         *     to green, enable the "Place Bets" button, and, when pressed,
         *     finish trial.
         * (3) If the new betting total is not equal 100, change the tally box 
         *     to red and disable the "Place Bets" button.
         * 
         * @param {Integer} slider_indx the slider index that indentifies which 
         *     slider has changed 
         * @param {Integer} new_bet The new bet that the partcipant made
         */ 
        function handle_betting(slider_indx, new_bet) {

            bets[slider_indx] = new_bet;

            const button = $(display_element).find('button');
            button.prop('disabled', false); 
            button.unbind('click'); 

            button.one('click', function(e){ 
                e.preventDefault();
                const trial_data = {
                    teacher: 'practice',
                    problem: 'practice',
                    bets: bets
                };
                console.log('Practice trial data:');
                console.log(trial_data);
                jsPsych.finishTrial(trial_data);
            });
        };

        let content = $('#templates #practice-problem').html();
        const heading = 'How to play';
        const subheading = 'Let\'s practice!';
        const subsubheading = 'Based on these hints, how would you distribute your chips to place bets?';

        content = sprintf(content, heading, subheading, subsubheading);
        $(display_element).html(content);

        // Initialize all the betting sliders for each hypothesis (option) with 
        // the appropriate values. Here, they are all uniform betting priors.
        const hypothesis_order = ["A", "B", "C", "D"];
        for (let indx = 0; indx < hypothesis_order.length; indx++) {
            const slider_id = "#" + hypothesis_order[indx] + 
                    "-practice-betting-slider";
            new Slider(slider_id,{tooltip: 'hide'}).on('change', 
                function(event) {
                    handle_betting(indx, event.newValue);
                }
            );
        };
    };
  
    return plugin;
  })();
  