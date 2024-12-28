const picField = document.getElementById("id_pic");

picField.onchange = function() {
    if(this.files[0].size > 10*1048576){
       alert("File too large. Size should not exceed 10 MB.");
       this.value = "";
    }
}

const pdfField = document.getElementById("id_pdf");

pdfField.onchange = function() {
    if(this.files[0].size > 10*1048576){
       alert("File too large. Size should not exceed 10 MB.");
       this.value = "";
    }
}    
