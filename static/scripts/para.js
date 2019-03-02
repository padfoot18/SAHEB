$("#add-new-modal").on("hidden.bs.modal", function () {
    $("#paragraph").focus();
});

$("#add-new-modal").on("shown.bs.modal", function () {
    $("#key_input").focus();
});

var str;
function add_key(new_key) {
    text_area = document.getElementById('paragraph');
    //IE support
    if (document.selection) {
        text_area.focus();
        sel = document.selection.createRange();
        sel.text = new_key;
    }
    //MOZILLA and others
    else if (text_area.selectionStart || text_area.selectionStart == '0') {
        var startPos = text_area.selectionStart;
        var endPos = text_area.selectionEnd;
        text_area.value = text_area.value.substring(0, startPos)
            + "zxyw" + new_key
            + text_area.value.substring(endPos, text_area.value.length);
    } else {
        text_area.value += "zxyw"+ new_key;
    }
}

function add_new() {
    key = $("#key_input").val();
    value = $("#value_input").val();
    if (key != null && value != null){
        $.post(
            "http://localhost:5000/insert/values/",
            {"key": key, "value": value.replace(/\n/gi, "<br>")},
            function (data, status) {
                if (!data["success"])
                    alert(data["error"]);
                else {
                    //add_row_in_table(data["data"]);

                    //$('#add-new-modal').modal('toggle');

                    key = data["data"]["key"];
                    add_key(key);
                    $("#key_input").val("");
                    $("#value_input").val("");
                }
            },
            "json"
        );
    }
}

function seteditable(){
    document.getElementById('paragraph').removeAttribute('readonly');
    edit_btn_block = document.getElementById('not_editable');
    edit_btn_block.style.display = 'None';
    submit_btn_block = document.getElementById('editable');
    submit_btn_block.style.display = 'Block';
    str = document.getElementById('paragraph').value;
}
function cancel_edit(para){
    document.getElementById('paragraph').readOnly = true;
    edit_btn_block = document.getElementById('not_editable');
    edit_btn_block.style.display = 'Block';
    submit_btn_block = document.getElementById('editable');
    submit_btn_block.style.display = 'None';
    document.getElementById('paragraph').value = str;
}
function submit_para(){
    var xhttp = new XMLHttpRequest();
    var new_str = document.getElementById('paragraph').value;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if(document.getElementById('paragraph').value == this.responseText) {
                document.getElementById('paragraph').value = this.responseText
                alert("Update Success");
            }
            else
                alert("Something went wrong");
            cancel_edit();
        }
    };
    xhttp.open("POST", "http://127.0.0.1:5000/edit_para/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send('str='+new_str);
    str = new_str;
}

function getSelectionText() {
    var text = "";
    var activeEl = document.activeElement;
    var activeElTagName = activeEl ? activeEl.tagName.toLowerCase() : null;
    if (
      (activeElTagName == "textarea") || (activeElTagName == "input" &&
      /^(?:text|search|password|tel|url)$/i.test(activeEl.type)) &&
      (typeof activeEl.selectionStart == "number")
    ) {
        text = activeEl.value.slice(activeEl.selectionStart, activeEl.selectionEnd);
    } else if (window.getSelection) {
        text = window.getSelection().toString();
    }
    if (text.length > 0) {
        $("#value_input").val(text);
    }
}