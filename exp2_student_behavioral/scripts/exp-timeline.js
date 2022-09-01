/**
 * This file drives the student experiment. It loads in the pre-processed data 
 * from the teaching experiment, instructions the participant ("student"), and 
 * collects their betting stategy across assigned problems. 
 * 
 * Essentially, a student betting problem consists of being presented with a 
 * problem and having the student bet on the correct answers (hypotheses). More
 * information on the experimental set up can be found in the README.md
 * 
*/

$(document).ready(function() {

  $('#templates').hide();   

  /**
   * Initialize all of the instruction betting sliders depenging on what section
   * of the instructions (as indicated by the instruction num) the participant
   * is on. Used only when instructing the participants on betting chips. 
   * 
   * @param {Integer} instruction_num the instruction page number
   */
  function init_instruction_betting_sliders(instruction_num) {

    const hypothesis_order = ["A", "B", "C", "D"];

    for (let i = 0; i < hypothesis_order.length; ++i) {
      const slider_id = "#" + hypothesis_order[i] + 
          "-instructions-betting-slider-" + instruction_num;
      new Slider(slider_id, {tooltip: 'hide'});
    };
  };

  /**
   * Checks if the quiz response given was the correct response. If it was, this
   * function updates the participant's count of correct quiz responses. 
   * 
   * @param {!Array<String>} data all the experiment data collected so far
   */
  function check_if_correct(data) {
    if (data.correct) {
      ++num_quiz_correct;
    };
  };

  // All the local variables that are updated as the participant runs
  // the experiment.
  let num_instruction_loops = 0;
  let num_quiz_correct = 0;
  let num_quiz_loops = 0;

  const max_quiz_loops = 2;

  const preload = {
    type: 'preload',
    auto_preload: true,
    images: [
      'images/player_intro.png', 
      'images/player_roles_student.png',
      'images/student_graduation.png',
      'images/student_fail.png' 
    ],
  };

  const consent = {
    type:'consent',
  };

  const fullscreen = {
    type: 'fullscreen'
  };

  const instructions = {
      type: 'instructions',
      pages: [
        sprintf($('#instructions').html(),
          'How to play',
          'Please pay attention to the instructions! There is a quiz at the \
          end. If your answers indicate that you have not read the \
          instructions we will repeat them.',
          'images/player_intro.png'
        ),
        sprintf($('#instructions-example').html(),
          'How to play',
          'In this game, you’re going to be a <strong>student</strong>! You’re \
          going to be betting on multiple choice questions like this one:'
        ),
        sprintf($('#instructions-example').html(),
          'How to play',
          'You might be wondering: “I have no idea how to answer this \
          question! What am I supposed to bet on?!”'
        ),
        sprintf($('#instructions').html(),
          'How to play',
          'Don’t worry, we’ll give you hints! <strong>  These hints have been \
          picked out by people who played an earlier version of this study. \
          </strong> These people played the role of the teacher; their job was \
          to give hints that would help students like you pick out the right \
          answer. <strong> Working together, both you and your teachers will \
          win more money if you pick the right answers! </strong>',
          'images/player_roles_student.png' 
        ),
        sprintf($('#instructions-canvas').html(),
          'How to play',
          'See the gray square right below? That’s the \
          <strong>canvas</strong>.',
          'This is where we’ll show the hints that teachers picked out.'
        ),
        sprintf($('#instructions-hint').html(),
          'How to play',
          'This is what two hints look like!',
          'This teacher flipped two grey tiles to reveal part of the correct \
          answer.'
        ),
        sprintf($('#instructions-hint').html(),
          'How to play',
          'See the row of options below?',
          'In this game, <strong> you’ll place bets on which of these options \
          is the correct answer. </strong>'
        ),
      ],
      show_clickable_nav: true,
      allow_backward: false,
      button_label_next: 'Next',  
  };

  const instructions_chips_timeline = [
    {
      type: 'instructions',
      pages: [
        sprintf($('#instructions-chips-1').html(),
          'How to play',
          "On each trial, we'll give you 100 'chips', and you'll place bets by \
          distributing those chips among the four options using the sliders \
          below. The higher the value on the slider, the more chips we'll place on that option.",
          "<strong>The more chips you place on the \
          right answer, the bigger your bonus will be. </strong>"
        )
      ],
      show_clickable_nav: true,
      allow_backward: false,
      button_label_next: 'Next',
      on_load: function() {
        init_instruction_betting_sliders(1);
      }
    },
    {
      type: 'instructions',
      pages: [
        sprintf($('#instructions-chips-2').html(),
          'How to play',
          'For example, if there’s a chance that several options could be \
          right, you can improve your chances of getting a bonus by \
          distributing the chips among multiple options. <em>Remember to bet \
          more chips on the options that are more likely to be right.</em>'
        )
      ],
      show_clickable_nav: true,
      allow_backward: false,
      button_label_next: 'Next',
      on_load: function() {
        init_instruction_betting_sliders(2);
      }
    }, 
    {
      type: 'instructions',
      pages: [
        sprintf($('#instructions-chips-3').html(),
          'How to play',
          'If you think an option is <em>definitely wrong</em>, \
          move the slider all the way to the left;',
          'If you think an option is <em>definitely right</em>, you should \
          go “all in” and move the slider all the way to the right.'
        )
      ],
      show_clickable_nav: true,
      allow_backward: false,
      button_label_next: 'Next',
      on_load: function() {
        init_instruction_betting_sliders(3);
      }
    },
    {
      type: 'instructions',
      pages: [
        sprintf($('#instructions-chips-4').html(),
          'How to play',
          'At the end of the game, <strong> we will calculate your bonus based \
          on the bets that you placed on 15 random trials.</strong> Please \
          answer the questions carefully and bet based on how likely each \
          option is to be right.'
        )
      ],
      show_clickable_nav: true,
      allow_backward: false,
      button_label_next: 'Next',
      on_load: function() {
        init_instruction_betting_sliders(4);
      }
    }
  ];

  // TODO: change the button appearance for "Repeat Instructions" (light red)
  // and "Take Quiz" (light green)
  const optional_repeat_node = {
    type: 'html-button-response',
    stimulus: sprintf('<h1>Quiz</h1> \
      <p>That’s it! Now it’s time to test out what you know! If you like, \
      you can flip back through the instructions to review. Once you start \
      the quiz, you won’t be able to check the instructions. If your answers \
      indicate that you’ve haven’t been paying attention, you may have to\
      repeat all of your training!</p> <img class = "hero"\
      src="images/player_intro.png" />'
    ),
    choices: ['Repeat Instructions', 'Take Quiz'], 
    show_clickable_nav: true,
    on_finish: function(data) {
      if (jsPsych.pluginAPI.compareKeys(data.response, 0)) {
        ++num_instruction_loops;
        data.response = 'Repeat Instructions';
        jsPsych.data.write({'response': 'Repeat Instructions'});
      } else {
        num_quiz_correct = 0;
        data.response = 'Take Quiz';
        jsPsych.data.write({'response': 'Take Quiz'});
      };
    }
  };

  const practice_problem = {
    type: "practice-bet"
  }

  const instructions_timeline = {
    timeline: [instructions].concat(instructions_chips_timeline).concat([
      practice_problem, optional_repeat_node]),
    loop_function: function(data) {
      var response = jsPsych.data.getLastTrialData().values()[0]["response"];
      if (jsPsych.pluginAPI.compareKeys(response, "Repeat Instructions")) {
        return true;
      };
      return false;
    }
  };
  
  const quiz_feedback = {
    type: "instructions",
    pages: [
      function() {
        ++num_quiz_loops;
        let prompt = '';
        let img = '';

        if (num_quiz_correct >= 2) {
          prompt = 'Great job, you passed! Please press the button below to ' +
              'start.';
          img = 'student_graduation.png';
        } else if (num_quiz_loops + 1 > max_quiz_loops) {
          prompt = 'Please press the button below to start.';
          img = 'student_graduation.png';
        } else {
          prompt = 'Oh no! Please press the button below to repeat ' + 
              'the instructions.';
          img = 'student_fail.png'; 
        };

        return sprintf('<h4>You answered <strong>%i of 3</strong> questions \
          correctly.</h4> <img class = "hero" src = "images/%s"> <h4>%s</h4>', 
          num_quiz_correct, img, prompt);
      }
    ],
    show_clickable_nav: true,
    allow_backward: false,
    button_label_next: 'Next',
  };

  const quiz_timeline = [
    {
      type:'quiz-multi-choice',
      prompt: "<h4>1. Where are these hints coming from?</h4>",
      options: [
        '(A) They come from real humans who played an earlier version of ' +
            'this HIT.',
        '(B) They were randomly generated.',
        '(C) Nobody knows!'
      ],
      expected: '(A) They come from real humans who played an earlier version' +
          ' of this HIT.',
      name: 'hints',
      on_finish: check_if_correct
    },
    {
      type:'quiz-multi-choice',
      prompt: '<h4>2. How should you distribute your chips in each bet?</h4>',
      options: [
        '(A) I should put all of my chips on the prettiest option.',
        '(B) I should distribute the chips across all four options, ' +
            'putting more chips on options that are more likely to be right.',
        '(C) If an option is definitely <em> wrong </em>, I should bet 0 ' +
            'chips on that option; if an option is definitely correct, ' + 
            'I should go “all in” and bet 100 chips on that option.',
        '(D) A & B',
        '(E) B & C'
      ],
      expected: '(E) B & C',
      name: 'distribute',
      on_finish: check_if_correct,
    },
    {
      type:'quiz-multi-choice',
      prompt: "<h4>3. Which of these statements correctly describes how your \
        bonus is calculated?</h4>",
      options: [
        '(A) My bonus will be calculated based on the bets I placed on 15 ' + 
            'random trials.',
        '(B) I can <em> increase </em> my bonus if I bet more chips on the ' + 
            'options that are more likely to be right',
        '(C) Betting on the right answer increases both my teacher’s bonus ' +
            'and my bonus.',
        '(D) All of the above'
      ],
      expected: '(D) All of the above',
      name: 'bonus',
      on_finish: check_if_correct,
    },
    quiz_feedback
  ];

  // The complete combined timeline node of all the instruction and quiz
  // Introduction will loop again if the quiz has been failed and they have
  // not maxed out on quiz repetitions. 
  const introduction = {
    timeline: [instructions_timeline].concat(quiz_timeline),
    loop_function: function(data) {
      return (num_quiz_correct < 2) & (num_quiz_loops < max_quiz_loops);
    },
    on_finish: function(data) {
      jsPsych.data.write({
        "num_instruction_loops": num_instruction_loops,
        "num_quiz_loops": num_quiz_loops
      });
    }
  };
  
  // This is where the crux of the experiment is set up. The student timeline
  // is populated with all the student problems using the student-bet plugin
  var student_timeline = [];
  var block_length;
  for (let num_trial = 0; num_trial < num_trials; ++num_trial) {
    block_length = hints[num_trial].states.length;

    for (let num_hint = 0; num_hint < block_length; ++num_hint) {
      let student_betting_problem = {
        type: 'student-bet',
        num_trial: num_trial, 
        num_hint: num_hint,
        total_hints: block_length,
        /**
         * A function that returns a uniform prior, meaning there there are 25
         * chips placed on each hypothesis) for the first hint (num_hint = 0) or 
         * returns the previous betting strategy that the particant gave when
         * 0 < num_hint < 3. Bets are in the hypothesis order.
         */
        betting_priors: function() {
          if (jsPsych.pluginAPI.compareKeys(num_hint, 0)) {
            return uniform_betting_priors;
          } else {
            return jsPsych.data.getLastTrialData().values()[0]["bets"];
          };
        },
        on_finish: function(data) {
          block_bonus += data.bonus;
          bonus += data.bonus;
        }
      };

      student_timeline.push(student_betting_problem);
    }

    // Give feedback
    let feedback = {
      type: 'student-feedback',
      num_trial: num_trial,
      num_hint: block_length,
      final_bets: function() {
        return jsPsych.data.getLastTrialData().values()[0]["bets"];
      },
      block_bonus: function() {
        return block_bonus;
      },
      running_total: function() {
        return bonus
      },
      on_finish: function() {
        block_bonus = 0;
      }
    };

    student_timeline.push(feedback);  

  }

  const check = {
    type: 'survey-text',
    questions: [{
      prompt: "To prove you are a human, please describe the HIT you just completed in a few sentences.",
      required: true,
      rows: 5
    }]
  };

  const survey = {
    type: 'post-survey'
  };

  // The entire experiment timeline. 
  const timeline = [preload, consent, fullscreen, introduction].concat(
      student_timeline).concat([check, survey]);
  // const timeline = [practice_problem];

  /// Initialize the whole experiment and display the debrief page afterwords.
  jsPsych.init({
    timeline: timeline,
    display_element: 'jspsych-display',
    show_progress_bar: true,
    on_finish: function() {
      completed = true;

      // Submit data
      var urlParams = parseURLParams(window.location.href);

      data = {
        worker: urlParams.workerId[0],
        assignment: urlParams.assignmentId[0],
        hit: urlParams.hitId[0],
        timestamp: Date.now(),
        version: '2022-02-14_student_v2',
        cond: student_id,
        problem_order: JSON.stringify(hints),
        data: jsPsych.data.get().json()
      };

      if (urlParams.hasOwnProperty('debug')) {
        console.log(data);
      } else {
        save_data(data);
      }
      
      var debrief_txt = $('#debrief').html();
      $('#jspsych-display').html(debrief_txt);
    },
  });

});

// special event: what to do when the page is closed
$(window).on('beforeunload', function(){

  var fd = new FormData();
	fd.append('worker_id', worker_id);
  fd.append('student_id', student_id);
  if (completed) {
    fd.append('completed', completed);
  }

  for (var value of fd.values()) {
    console.log(value);
  }

  navigator.sendBeacon('close_assignment.php', fd);

  console.log('Assignment closed.');
});