function SendRequest(user_id, button) {
  // Update Add Buddy button on frontend & send request to server.
  var user_id = user_id;

  // Add Sent button with text Following Class Success.
  var button_text = document.getElementById("id_send_request_button_" + user_id);
  button_text.innerHTML = "<b>Request Sent</b>";

  button.setAttribute("class", "button is-rounded is-success");

  $.ajax({
    // Send data packet including tag id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../send_request/' + user_id + '/',

  });
};

function AcceptRequest(request_id, button) {
  document.getElementById("id_reject_request_button_" + request_id).remove();
  // Update Accept Request button on frontend & send request to server.
  var request_id = request_id;

  // Add Accepted button with text Following Class Success.
  var button_text = document.getElementById("id_accept_request_button_" + request_id);
  button_text.innerHTML = "<b>Request Accepted</b>";

  button.setAttribute("class", "button is-rounded is-success");


  $.ajax({
    // Send data packet including tag id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../accept_request/' + request_id + '/',

  });
};

function RejectRequest(request_id, button) {
  document.getElementById("id_accept_request_button_" + request_id).remove();  
  // Update Reject Request button on frontend & send request to server.
  var request_id = request_id;

  // Add Accepted button with text Following Class Success.
  var button_text = document.getElementById("id_reject_request_button_" + request_id);
  button_text.innerHTML = "<b>Request Rejected</b>";

  button.setAttribute("class", "button is-rounded is-danger");

  $.ajax({
    // Send data packet including tag id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../reject_request/' + request_id + '/',

  });
};