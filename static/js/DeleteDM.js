// Delete DM
function DeleteDM(dm_id) {
  
      // Delete DM Div & Its br
      dm = document.getElementById('id_dm_div_'+dm_id);
      dm.remove();
      br = document.getElementById('id_dm_div_br_'+dm_id);
      br.remove();

      // Update DM Count
      document.getElementById('id_dm_count').textContent--;

      $.ajax({
          // Send data packet including dm id to the server.
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
          type: 'POST',
          url: '../../../delete_dm/' + dm_id + '/',

      });

};
