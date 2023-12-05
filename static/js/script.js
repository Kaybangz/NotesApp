// $(document).ready(function() {
//     // Update the timer every second
//     setInterval(updateTimer, 1000);

//     // Handle click events for timer controls
//     $('#start-pomodoro').click(function() {
//         $.ajax({
//             url: '/start_pomodoro',
//             method: 'POST',
//             success: function() {
//                 updateTimer();
//             }
//         });
//     });

//     $('#pause-pomodoro').click(function() {
//         $.ajax({
//             url: '/pause_pomodoro',
//             method: 'POST',
//             success: function() {
//                 updateTimer();
//             }
//         });
//     });

//     $('#resume-pomodoro').click(function() {
//         $.ajax({
//             url: '/resume_pomodoro',
//             method: 'POST',
//             success: function() {
//                 updateTimer();
//             }
//         });
//     });

//     $('#reset-pomodoro').click(function() {
//         $.ajax({
//             url: '/reset_pomodoro',
//             method: 'POST',
//             success: function() {
//                 updateTimer();
//             }
//         });
//     });
// });

// function updateTimer() {
//     // Fetch the current timer state and elapsed time from the server
//     $.ajax({
//         url: '/',
//         method: 'GET',
//         success: function(data) {
//             var pomodoroState = data.pomodoro_state;
//             var pomodoroElapsedTime = data.pomodoro_elapsed_time;

//             // Update the timer display based on the timer state and elapsed time
//             $('#timer').text(pomodoroElapsedTime);

//             // Disable or enable controls based on the timer state
//             if (pomodoroState == 'working') {
//                 $('#start-pomodoro').attr('disabled', true);
//                 $('#pause-pomodoro').attr('disabled', false);
//                 $('#resume-pomodoro').attr('disabled', true);
//             } else if (pomodoroState == 'paused') {
//                 $('#start-pomodoro').attr('disabled', true);
//                 $('#pause-pomodoro').attr('disabled', true);
//                 $('#resume-pomodoro').attr('disabled', false);
//             } else {
//                 $('#start-pomodoro').attr('disabled', false);
//                 $('#pause-pomodoro').attr('disabled', true);
//                 $('#resume-pomodoro').attr('disabled', true);
//             }
//         }
//     });
// }
// $(document).ready(function() {
//     $('#start-btn').click(function() {
//         $.get('/start', {
//             work_time: $('#work-time').text(),
//             break_time: $('#break-time').text()
//         });
//     });
//     $('#stop-btn').click(function() {
//         // Stop the timer
//     });
//     $('#reset-btn').click(function() {
//         // Reset the timer
//     });
// });

// var timer = document.getElementById('timer');
//         var startBtn = document.getElementById('start-btn');
//         var stopBtn = document.getElementById('stop-btn');
//         var resetBtn = document.getElementById('reset-btn');

//         startBtn.addEventListener('click', function() {
//             $.post('/start', function(data) {
//                 timer.textContent = data.time_left;
//             });
//         });

//         stopBtn.addEventListener('click', function() {
//             $.post('/stop', function(data) {
//                 timer.textContent = data.time_left;
//             });
//         });

//         resetBtn.addEventListener('click', function() {
//             $.post('/reset', function(data) {
//                 timer.textContent = data.time_left;
//             });
//         });

var timer = document.getElementById('timer');
var startBtn = document.getElementById('start-btn');
var stopBtn = document.getElementById('stop-btn');
var resetBtn = document.getElementById('reset-btn');

startBtn.addEventListener('click', alert("Hello there"))

// startBtn.addEventListener('click', function() {
//     $.post('/start', function(data) {
//         timer.textContent = data.time_left;
//         setInterval(function() {
//             $.post('/update', function(data) {
//                 timer.textContent = data.time_left;
//             });
//         }, 1000);
//     });
// });

// stopBtn.addEventListener('click', function() {
//     $.post('/stop', function(data) {
//         timer.textContent = data.time_left;
//     });
// });

// resetBtn.addEventListener('click', function() {
//     $.post('/reset', function(data) {
//         timer.textContent = data.time_left;
//     });
// });