<!DOCTYPE html>
<html>
<body>

<h1>Substitute page</h1>
<label for="college_fee">New College Fees</label>
<input type="text" id="college_fee">
<label for="hostel_fee">New Hostel Fees</label>
<input type="text" id="hostel_fee">
<label for="application_fee">New Application Fees</label>
<input type="text" id="application_fee">
<button type="button" onclick="loadDoc()">Update!</button>

<div id="reply"></div>
 
<script>
function loadDoc() {
  var xhttp = new XMLHttpRequest();
  var college_fee = document.getElementById("college_fee").value;
  var hostel_fee = document.getElementById("hostel_fee").value;
  var application_fee = document.getElementById("application_fee").value;
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("reply").innerHTML = document.getElementById("reply").innerHTML + this.responseText + "<br><br>";
      // alert(this.responseText);
    }
  };
  xhttp.open("POST", "http://127.0.0.1:8888/substitute/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("college_fee="+college_fee+"hostel_fee="+hostel_fee+"application_fee="+application_fee);
}
</script>

</body>
</html>
