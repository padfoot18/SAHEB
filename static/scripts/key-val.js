// TODO(2) if response/data["success"] = false, then exception occurred in server
$("document").ready(function(){
    $.get("http://127.0.0.1:5000/read/values/", function (data, status){
        add_row_in_table(data);
    }, "json");
});



function update_value(id) {
    if (id != null){
        key = $("#key_"+id).text();
        value = $("#input_"+id).val();
        $.post("http://127.0.0.1:5000/update/values/",
            {"id": id, "value": value.replace(/\n/gi, "<br>")},
            function (data, status) {
                if (status === "success") {
                    val_td = $("#val_"+id);
                    btn = $("#btn_"+id);
                    val_td.empty();
                    val_td.html(data["value"]);
                    btn.text("Edit");
                    btn.attr("onclick", "set_edit_row("+id+")");
                    $("#btn_cancel_"+id).remove();
                }
                else
                    alert("Sorry! Could not update!");
            },
            "json"
        )
    }
}

function set_edit_row(id) {
    val_td = $("#val_"+id);
    value = val_td.html();
    if (typeof(Storage) !== "undefined") {
        sessionStorage.setItem(id, value);
    }
    val_td.empty();
    var x = value.split(/<br>/).length;
    val_td.append("<textarea class='form-control' rows='"+x+"' id='input_"+id+"'></textarea>");
    $("#input_"+id).val(value.replace(/<br>/gi, "\n"));
    btn_td = $("#btn_td_"+id);
    btn = $("#btn_"+id);
    btn.text("Save");
    btn.attr("onclick", "update_value("+id+")");
    btn_td.append("<br><br><button type='button' id='btn_cancel_"+id+"' class='btn btn-primary' onclick='cancel("+id+" )'>Cancel</button>")
}

function cancel(id) {
    if (sessionStorage.getItem(id)){
        value = sessionStorage.getItem(id);
        btn_save = $("#btn_"+id);
        btn_save.text("Edit");
        btn_save.attr("onclick", "set_edit_row("+id+")");
        btn_td = $("#btn_td_"+id);
        $("#btn_cancel_"+id).remove();
        val_td = $("#val_"+id);
        val_td.empty();
        val_td.html(value);
    }
}

function add_row_in_table(data){
    table_body = $("#key-val-tbody");
    for (var i = 0; i < data.length; i++) {
        id = data[i]["id"];
        key = data[i]["key"];
        val = data[i]["value"];
        key_data = "<td id='key_"+id+"'>" + key + "</td>";
        val_td = "<td id='val_"+id+"'>" + val + "</td>";
        edit_btn = "<td id='btn_td_"+id+"'><button id='btn_"+id+"' type='button' class='btn btn-primary' onclick='set_edit_row("+id+")'>Edit</button></td>";
        new_row = "<tr id='row_'"+id+">" + key_data + val_td + edit_btn + "</tr>";
        table_body.append(new_row);
    }
}


function delete_value(id) {
    if (id != null){
        $.post(
            "http://127.0.0.1:5000/delete/values/",
            {"id": id},
            function (data, status) {
                if (!data["success"])
                    alert("There is something wrong, could not delete!");
                else
                    $("#row_"+id).remove();
            }
        )
    }
}
