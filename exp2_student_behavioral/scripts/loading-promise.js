/**
 * Creates a loading problem promise. When problems fully load in, the rest of 
 * the experiment is loaded in.
 */
 var worker_id,student_id,hints,problems,urlParams;
 var hints_loaded=false;
 var completed=false;
 var bonus=0;
 var block_bonus=0;
 const num_trials = 40; // Equal to the total count of problems each student sees.
 var max_block_bonus = 5.0/num_trials;
 const hints_filepath = "scripts/new_sample_teacher.json";
 const problems_filepath = "scripts/problems.json"; 
 const uniform_betting_priors = [25, 25, 25, 25]; 

$(document).ready(function() {
    urlParams = parseURLParams(window.location.href);
    worker_id = urlParams['workerId'][0];
    
    // Prepare screen by hiding all the webpages
    $('#templates').hide();

    // Load hints
    if (urlParams.hasOwnProperty('debug')) {
        var hint_request = $.getJSON(hints_filepath, function(data){
            console.log('WARNING: USING DEBUG TIMELINE');
            student_id = 'debug';
            hints = data;
            hints_loaded = true;
        });
    } else {
        var hint_request = $.get('select_assignment.php?=workerId='+worker_id, function(data){
            // Parse data
            response = JSON.parse(data);
            if (response['data']) {
                hints_loaded=true;
                data_dict = response['data'];

                student_id = parseInt(data_dict['student_id']);
                hints = JSON.parse(data_dict['trial_order']);
                console.log('Loaded available assignment from database: ' + student_id);
                // console.log(hints);
            } else {
                console.log('Error! No HITs available');
            }
        });
    }

    // Load problems
    var prob_request = $.getJSON(problems_filepath, function(data){
        console.log('Loaded problems');
        problems = data;
    });

    // When both requests are done, continue on with the task!
    $.when(hint_request, prob_request).done(function(){
        console.log('Done loading! Proceeding to main task');
        $('#loading-prompt').hide();
        if (hints_loaded) {
            let script = document.createElement('script');
            script.src = 'scripts/exp-timeline.js';
            document.head.append(script);
        } else {
            var fail_msg = $('#failure-msg').html();
            $('#jspsych-display').html(fail_msg);
        }
    });
});