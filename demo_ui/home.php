<!DOCTYPE html>
<html>
<head>
	<title></title>
</head>
<body on load="read()">

<div id="insert">
<h1> Add a new Sentence</h1>
<label for="new_sentence"> Sentence</label>
<textarea name="sentence" id="new_sentence" required=""></textarea>

<label for="insert_key"> Key </label>
<input type="text" name="key" id="insert_key" required="">

<label for="insert_value"> Value </label>
<input type="text" name="value" id="insert_value" required="">

<button onclick="insert()"> Insert </button>
</div>

<script>
function read(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
    	if (this.readyState == 4 && this.status == 200){
    		alert(this.responseText);
    	}

    };

	xhttp.open("POST", "http://127.0.0.1:5000/api/v2/read/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("");


}

function insert()
{
	 var xhttp = new XMLHttpRequest();
	 var key = document.getElementById("insert_key").value;
     var value = document.getElementById("insert_value").value;
     var sentence=document.getElementById("new_sentence").value
     xhttp.onreadystatechange = function(){
     	if (this.readyState == 4 && this.status == 200){
     		alert(this.responseText);

     	}

     };
     xhttp.open("POST", "http://127.0.0.1:5000/api/v2/insert/", true);
     xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
     xhttp.send("key="+key+"&value="+value+"sentence="+sentence+);

}

</script>
</body>
</html>