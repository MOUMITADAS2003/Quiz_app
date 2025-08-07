
let timeLeft = 60;
let timer;

function startTimer() {
  timer = setInterval(function() {
    if (timeLeft <= 0) {
      clearInterval(timer);
      alert("Time is up! Submitting your quiz.");
      document.forms[0].submit();
    } else {
      document.getElementById("time").innerHTML = timeLeft;
    }
    timeLeft -= 1;
  }, 1000);
}
