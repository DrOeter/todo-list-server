var selectedUser = "";
var selectedList = "";
var selectedEntry = "";
var listCount = 1;

var url = "http://127.0.0.1:5000/";

function request(url, method, data ){
    return new Promise((resolve, reject) => {
        var http = new XMLHttpRequest();
        http.open(method, url, true);
        http.setRequestHeader('Content-type', 'application/json');
        http.onreadystatechange = function() {
            if(http.readyState == 4 && http.status == 200) {
                resolve(http.responseText);
                //document.getElementById(id).innerText = http.responseText;
            }
        }
        http.send(data);
    }) 
}

async function addUser(){
    var user = document.getElementById("user").value;
    request(url + 'user', 'POST', '{"user": "' + user + '"}');
    await getUsers();
}

async function getUsers(){
    var str = await request(url + 'user', 'GET', null);            
    var users = JSON.parse(String(str).replace(/'/g, '"'));
    var box = document.getElementById("userListBox");
    while(box.hasChildNodes()){
        box.removeChild(box.firstChild);
    }
    addToList(users, "userListBox");
}

async function getList(){
    var str = await request(url + 'list/' + selectedList, 'GET', null);
    var list = JSON.parse(String(str).replace(/'/g, '"'));
    var table = document.getElementById("listTable");
    var box = document.getElementById("entryListBox");
    while(table.hasChildNodes()){
        table.removeChild(table.firstChild);
    }
    while(box.hasChildNodes()){
        box.removeChild(box.firstChild);
    }

    list.forEach(function (value, i) {
        document.getElementById("entryListBox").setAttribute("size", "" + Number(i + 1));
        var opt = document.createElement("option");
        opt.text = "Entry " + Number(i + 1);
        opt.value = value['id'];   
        document.getElementById("entryListBox").options.add(opt);
        var row = table.insertRow();

        for (var key in value) {
            let newCell = row.insertCell();
            let newText = document.createTextNode(value[key]);
            newCell.appendChild(newText);
        }
    });   
}        

async function addList(){
    var str = await request(url + 'list-add/' + selectedUser, 'POST', null);            
    var list = JSON.parse(String(str).replace(/'/g, '"'));
    var opt = document.createElement("option");
    opt.text = String(listCount);
    opt.value = list['list_id'];
    document.getElementById("listListBox").options.add(opt);
    listCount++;
}

function addEntry(){
    var name = document.getElementById("name").value;
    var desc = document.getElementById("desc").value;
    var data = '{"name": "' + name + '", "description": "' + desc + '"}';
    request(url + 'list/' + selectedList, 'POST', data);
}    

async function changeEntry(){
    var name = document.getElementById("name").value;
    var desc = document.getElementById("desc").value;
    var data = '{"name": "' + name + '", "description": "' + desc + '"}';
    request(url + 'list/' + selectedList + '/entry/' + selectedEntry, 'PUT', data);
    await getList();
}

function addToList(j, list) {
    for (var key in j) {
        if (j.hasOwnProperty(key)) {
            var opt = document.createElement("option");
            opt.text = key;
            opt.value = j[key];
            document.getElementById(list).options.add(opt);
        }
    }
    return false;
}
async function deleteUser(){
    request(url + 'user/' + selectedUser, 'DELETE', null);
    document.getElementById("userListBox").options.remove(selectedUser);

//    await getUsers();
}

async function deleteEntry(){
    request(url + 'list/' + selectedList + '/entry/' + selectedEntry, 'DELETE', null);
    await getList();
}

function deleteList(){
    request(url + 'list/' + selectedList, 'DELETE', null);
}

function userSelected(value){ 
    selectedUser = value;
}

function listSelected(value){ 
    selectedList = value;
}

function entrySelected(value){ 
    selectedEntry = value;
}