// Open Menu, Update Trigger
function OpenThreeDotMenu(id) {
      $("#menu_id_"+id).addClass("is-active");
      document.getElementById("menu_trigger_id_"+id).setAttribute("onclick", "CloseThreeDotMenu("+id+")");
      newTriggerHTML = '<i class="is-pulled-right fa fa-ellipsis-h" aria-hidden="true"></i>'
      document.getElementById("menu_trigger_id_"+id).innerHTML = newTriggerHTML;

};

// Close Menu, Update Trigger
function CloseThreeDotMenu(id) {
      $("#menu_id_"+id).removeClass("is-active");
      document.getElementById("menu_trigger_id_"+id).setAttribute("onclick", "OpenThreeDotMenu("+id+")");
      newTriggerHTML = '<i class="is-pulled-right fa fa-ellipsis-v" aria-hidden="true"></i>'
      document.getElementById("menu_trigger_id_"+id).innerHTML = newTriggerHTML;      
};
