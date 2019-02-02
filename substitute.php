<!DOCTYPE html>
<html>
<head>
	<title>Substitute data</title>
  <style>
        th, td, p, input {
            font:14px Verdana;
        }
        table, th, td 
        {
            border: solid 1px #DDD;
            border-collapse: collapse;
            padding: 2px 3px;
            text-align: center;
        }
        th {
            font-weight:bold;
        }
    </style>
</head>
<body onload="read_data()">
  <h1 align="center">Database Pairs:</h1>
<div id="database_data" align="center"></div>

<div id="add_data">
  <h1>Add Key Pair</h1>
  <label for="add_key">Key :</label>
  <input type="text" name="add_key" id="add_key">
  <label for="add_value">Value :</label>
  <input type="text" name="add_value" id="add_value">
  <button onclick="add_pair()">Add Pair</button>
</div>

<div id="update_data">
  <h1>Update Key Pair</h1>
  <label for="update_key">Key :</label>
  <input type="text" name="update_key" id="update_key">
  <label for="update_value">Value :</label>
  <input type="text" name="update_value" id="update_value">
  <button onclick="update_pair()">Update</button>
</div>

<div id="delete_data">
  <h1>Delete Key Pair</h1>
  <label for="delete_key">Key :</label>
  <input type="text" name="delete_key" id="delete_key">
  <button onclick="delete_pair()">Delete</button>
</div>


<script>
function read_data() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var data = this.responseText;
      var myPairs = JSON.parse(data);
      //document.getElementById("answer").innerHTML = values; 
      // EXTRACT VALUE FOR HTML HEADER. 
        var col = [];
        for (var i = 0; i < myPairs.length; i++) {
            for (var key in myPairs[i]) {
                if (col.indexOf(key) === -1) {
                    col.push(key);
                }
            }
        }

        // CREATE DYNAMIC TABLE.
        var table = document.createElement("table");

        // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

        var tr = table.insertRow(-1);                   // TABLE ROW.

        for (var i = 0; i < col.length; i++) {
            var th = document.createElement("th");      // TABLE HEADER.
            th.innerHTML = col[i];
            tr.appendChild(th);
        }

        // ADD JSON DATA TO THE TABLE AS ROWS.
        for (var i = 0; i < myPairs.length; i++) {

            tr = table.insertRow(-1);

            for (var j = 0; j < col.length; j++) {
                var tabCell = tr.insertCell(-1);
                tabCell.innerHTML = myPairs[i][col[j]];
            }
        }

        // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
        var divContainer = document.getElementById("database_data");
        divContainer.innerHTML = " ";
        divContainer.appendChild(table);
    }
  };
  xhttp.open("POST", "http://127.0.0.1:8888/api/v1/read/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("");
}

function add_pair() {
  var xhttp = new XMLHttpRequest();
  var key = document.getElementById("add_key").value;
  var value = document.getElementById("add_value").value;
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      alert(this.responseText);
    }
  };
  xhttp.open("POST", "http://127.0.0.1:8888/api/v1/insert/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("key="+key+"&value="+value);
}

function update_pair() {
  var xhttp = new XMLHttpRequest();
  var key = document.getElementById("update_key").value;
  var value = document.getElementById("update_value").value;
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      alert(this.responseText);
    }
  };
  xhttp.open("POST", "http://127.0.0.1:8888/api/v1/update/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("key="+key+"&value="+value);
}

function delete_pair() {
  var xhttp = new XMLHttpRequest();
  var key = document.getElementById("delete_key").value;
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      alert(this.responseText);
    }
  };
  xhttp.open("POST", "http://127.0.0.1:8888/api/v1/delete/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("key="+key);
}

</script>

</body>
</html>