// Add A New Comment 
function AddComment(post_id) {
      // Collect Data From Post Form
      post_id = post_id;
      body = document.getElementById("id_comment_form_textarea").value;

      // Check If Form Is Not Empty Add Fire Ajax Request
      if (body.trim() != "")
      {
            
            // Reset & Disable Post Form
            document.getElementById("id_comment_form").reset();

            $('#id_comment_form_submit').prop('disabled', true);
            $('#id_comment_form_submit').html("Posted")

            // Create A New Comment
            var user_pic_source =  document.getElementById("id_comment_form_user_pic").src;            
            var comment =
            `<article class="media">
              <figure class="media-left">
                <img src="`+user_pic_source+`" class="card-profile-pic">
              </figure>            
              <div class="media-content">
                <div class="content">
                  <p>
                    <a><strong>You</strong></a>
                    <br>`+body+`<br>
                    <small>0 minutes ago</small>
                  </p>
                </div>
              </div>
            </article>`;
            
            $('#id_comment_form').after(comment); 

            // Update Comment Count
            document.getElementById('id_comment_count').textContent++;

            $.ajax({
                // Fire Ajax Request
                headers: {
                  "X-CSRFToken": getCookie("csrftoken")
                },
                type: 'POST',
                url: '../../../add_comment/',
                data:{
                  post_id: post_id,
                  body: body,
                },                

            });

      }
};

