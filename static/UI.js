const dropZone = document.querySelector(".drag-drop");
const fileInput = document.querySelector("#file");
const browsebtn = document.querySelector(".Browse-btn");

dropZone.addEventListener("dragover", (e)=>{
    e.preventDefault();
    if(!dropZone.classList.contains("dragged")){
        dropZone.classList.add("dragged");
    }
})

dropZone.addEventListener("dragleave", ()=>{
    dropZone.classList.remove("dragged");
})

dropZone.addEventListener("drop", (e)=>{
    e.preventDefault();
    dropZone.classList.remove("dragged");
    const Files=e.dataTransfer.files;
    console.log(Files);
    if(Files.length){
        fileInput.files=Files;
    }
})

browsebtn.addEventListener("click", ()=>{
    fileInput.click();
})

$('.share').on('click', function(){
    $('#shareModal').modal();

    const $this=$(this);
    const fileId=$this.attr('data-fileid');
    const filenameslugified=$this.attr('data-filename');
    const permalink = 'http://localhost:5000/' + 'download/' + fileId + '/' + filenameslugified;

    $('#shareModal .share-link').html(permalink);
});

$('.delete').on('click', function(){
    const $this=$(this);
    const fileId=$this.attr('data-fileid');
    window.location.href="/user/"+fileId;
});

function copytoclipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();
  }