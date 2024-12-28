// Open Send DM Modal
function OpenSendDM(user_id) {
  
      // Prepare Modal
      button = document.getElementById('id_dm_form_submit');
      button.setAttribute("onclick", "SendDM("+user_id+")");

      // Open Modal
      OpenModal('dm');

};
