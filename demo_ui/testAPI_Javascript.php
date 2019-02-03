<!DOCTYPE html>
<html>
<body>

<h1>The XMLHttpRequest Object</h1>

<input type="text" id="question">
<button type="button" onclick="loadDoc()">Request data</button>

<div id="answer"></div>
 
<script>
function loadDoc() {
  var xhttp = new XMLHttpRequest();
  var question = document.getElementById("question").value;
  document.getElementById("answer").innerHTML = document.getElementById("answer").innerHTML + question + "<br>";
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("answer").innerHTML = document.getElementById("answer").innerHTML + this.responseText + "<br><br>";
      // alert(this.responseText);
    }
  };
  xhttp.open("POST", "http://127.0.0.1:8888/chat/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("question="+question);
}
</script>

</body>
</html>
