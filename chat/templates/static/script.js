function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


$('.bi-bell-fill').click(function () {
    window.location.href = '/notifications/';
});

$('#profile').click(function () {
    window.location.href = '/profile/';
});

$('.bi-person-plus-fill').click(function () {
    window.location.href = '/suggest/';
});

$('.list-group-item.list-group-item-action').click(function () {
  $(this).addClass('active');
});

$(document).ready(function() {
    $('#change-password').change(function() {
        if (this.checked) {
            $('#NewPassword').show();
        } else {
            $('#NewPassword').hide();
        }
    });
});


  
  // Show the selected file name in the tooltip when a file is chosen
  document.querySelector('#file-input').addEventListener('change', function() {

    const fileInput = document.querySelector('#file-input');
    const tooltip = document.querySelector('#file-tooltip');

    // if (fileInput.files.length > 0) {
    //     let fileNames = [];
    //     for (let i = 0; i < fileInput.files.length; i++) {
    //       fileNames.push(fileInput.files[i].name);
    //     }
    //     tooltip.innerHTML = fileNames.join(', ');
    //   } else {
    //     tooltip.innerHTML = 'Choose File';
    //   }
    if (fileInput.files.length > 0) {
      const fileName = fileInput.files[0].name;
      tooltip.innerHTML = fileName;
    

    } else {
      tooltip.innerHTML = 'Choose';
    }
  });
  


const id = JSON.parse(document.getElementById('json-username').textContent);
const msg_id = JSON.parse(document.getElementById('json-msg-username').textContent);
// const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + id
    + '/'
);

socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

socket.onerror = function(e){
    console.log("ERROR OCCURED");
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    console.log(data);
    let msg_body = document.getElementById('chat-body');
    if(data.username == msg_id){
        let file_input = document.getElementById("file-input")
		var form_data = new FormData();
		form_data.append("files", file_input.files[0]);
		form_data.append("message",data.message);
		form_data.append("username",data.username);
        form_data.append("csrfmiddlewaretoken", csrftoken);
		console.log(file_input.files);
        if (file_input.files[0] != null){
            $.ajax({
                method: "POST",
                url: "/post_files/",
                processData: false,
                contentType: false,
                mimeType: "multipart/form-data",
                data: form_data,
                success: function(res) {
                    console.log("Successfully Saved Message and File!");
                },
                error: function(err) {
                    console.error("Error occurred while saving message and file:", err);
                }
            });

        // document.querySelector('#chat-body').innerHTML += `<div class="msg-sent">
        //                                                         <span class="msg">${data.message}</span>
        //                                                         <span class="timestamp">12.05pm</span>
        //                                                     </div>`
        file_html = '<div class="attachment w-auto d-flex">' +
                        '<button class="btn attach shadow-none"><i class="bi bi-file-earmark-fill fs-2 text-white"></i></button>' +
                        '<div class="file" style="overflow: hidden;">' +
                        '<p><a href="/static/'+file_input.files[0].name+'" download class="fs-5 w-auto text-dark" style="overflow: hidden;">'+file_input.files[0].name+'</a></p>'+
                            '<span>24kb</span> ' +
                        '</div>' +
                    '</div>'
        }
        else {
            file_html = ''
        }
        msg_body.innerHTML += '<div class="msg-sent">' + file_html +
                                '<span class="msg">'+ data.message +'</span>'+
                                '<span class="timestamp">' + new Date().toLocaleTimeString(); + '</span>' +
                                '</div>'
    }else{
       msg_body.innerHTML += '<div class="msg-receive">' + 
                                '<span class="msg">'+ data.message +'</span>'+
                                '<span class="timestamp">' + new Date().toLocaleTimeString(); + '</span>' +
                                '</div>'
    }
}
document.querySelector('#msg_send').onclick = function(e){
    const msg_box = document.querySelector('#msg-box');
    const message = msg_box.value;
    console.log(message+" "+msg_id);

        socket.send(JSON.stringify({
            'message':message,
            'username':msg_id,
            "files":"",
        }));

        msg_box.value = '';
}











// msg_id
const online_status = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/online/'
)

online_status.onopen = function(e){
    console.log("CONNECTED TO ONLINE CONSUMER");
    online_status.send(JSON.stringify({
        'username':msg_id,
        'type':'open'
    }))
}

window.addEventListener("beforeunload", function(e){
    online_status.send(JSON.stringify({
        'username':msg_id,
        'type':'offline'
    }))
})

online_status.onclose = function(e){
    console.log("DISCONNECTED FROM ONLINE CONSUMER")
}


online_status.onmessage = function(e){
    var data = JSON.parse(e.data)
    // if(data.username != msg_id){
    //     var user_to_change = document.getElementById(`${data.username}_status`)
    //     var small_status_to_change = document.getElementById(`${data.username}_small`)
    //     if(data.online_status == true){
    //         user_to_change.style.color = 'green'
    //         small_status_to_change.textContent = 'Online'
    //     }else{
    //         user_to_change.style.color = 'grey'
    //         small_status_to_change.textContent = 'Offline'
    //     }
    // }
}