// Delete Comment
function DeleteComment(comment_id) {
  
      // Delete Comment Div
      comment = document.getElementById('id_comment_div_'+comment_id);
      comment.remove();

      // Update Comment Count
      document.getElementById('id_comment_count').textContent--;

      $.ajax({
          // Send data packet including comment id to the server.
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
          type: 'POST',
          url: '../../../delete_comment/' + comment_id + '/',

      });

};
