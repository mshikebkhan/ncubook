// Delete Post
function DeletePost(post_id) {
  
      // Delete Post Div & Its br
      post = document.getElementById('id_post_div_'+post_id);
      post.remove();
      br = document.getElementById('id_post_div_br_'+post_id);
      br.remove();

      // Update Post Count
      if(document.getElementById("id_post_count")){
        document.getElementById('id_post_count').textContent--;
      }

      $.ajax({
          // Send data packet including post id to the server.
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
          type: 'POST',
          url: '../../../delete_post/' + post_id + '/',

      });

};
