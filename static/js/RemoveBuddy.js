function RemoveBuddy(user_id) { 
  // Update Remove Buddy button on frontend & send request to server.
  CloseModal('remove_buddy');
  var user_id = user_id;

  // Add Accepted button with text Following Class Success.
  var button_text = document.getElementById("id_remove_buddy_button_" + user_id);
  button_text.innerHTML = "<b>Buddy Removed</b>";
  button = document.getElementById("id_remove_buddy_button_" + user_id);
  button.setAttribute("class", "dropdown-item is-danger");
  button.setAttribute("onclick", "");

  // Remove Message Button
  var dm_button = document.getElementById("id_dm_button");
  dm_button.remove();  

  $.ajax({
    // Send data packet including tag id to the server.
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    type: 'POST',
    url: '../../../remove_buddy/' + user_id + '/',

  });
};