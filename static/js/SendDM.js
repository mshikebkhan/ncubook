// Send DM 
function SendDM(user_id) {
      // Close DM Modal
      CloseModal('dm');

      // Collect Data From Post Form
      user_id = user_id;
      body = document.getElementById("id_dm_form_textarea").value;

      // Update Count & Create DM On Front End
      if(document.getElementById("id_dm_count")){
        document.getElementById('id_dm_count').textContent++;

        var user_pic_source =  document.getElementById("id_dm_form_user_pic").src;            
        var dm =
        `<div class="card" style="background-color: #E1FFC7;">
           <div class="card-content">
              <div class="media">
              <figure class="media-left">
                <img src="`+user_pic_source+`" class="user-profile-pic">
              </figure>
              <div class="media-content">
                <div class="content">
                  <p>
                    <strong>You</strong>
                    <br>`+body+`<br>
                    <small>0 minutes ago</small>
                  </p>
                </div>
              </div>
              </div>
           </div>
        </div>
        <br>`;
        
        $('#id_dm_privacy_note_br').after(dm);

      } 
      // Check If Form Is Not Empty Add Fire Ajax Request
      if (body.trim() != "")
      {
            
            // Reset & Disable Post Form
            document.getElementById("id_dm_form").reset();

            $.ajax({
                // Fire Ajax Request
                headers: {
                  "X-CSRFToken": getCookie("csrftoken")
                },
                type: 'POST',
                url: '../../../send_dm/',
                data:{
                  user_id: user_id,
                  body: body,
                },                

            });

      }
};

