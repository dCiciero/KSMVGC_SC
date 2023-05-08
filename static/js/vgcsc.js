// var path = window.location.pathname;
// var page = path.split("/").pop();
// console.log( page );
// var btnSetup ;
window.addEventListener('DOMContentLoaded', ({target}) => {
    // alert('Welcome')
    let photo_upload_form = document.querySelector('#frm-upload');
    let doc_upload_form = document.querySelector('#frm_doc_upload');
    let chess_txt = document.querySelector('#txtChess');
    let caption = document.querySelector('#photoCaption');
    let options = document.querySelector('#galleryOptionsWrapper');
    let captionText = document.querySelector('#txtcaption');
    let uploadPhotoFile = document.querySelector('#txtPhotoUpload');
    let uploadDocFile = document.querySelector('#txtDocUpload');

    let uploadType = document.querySelector('#uploadType'); //gets the gallery section's dropdown
    let galleryOptions = document.querySelector('#galleryOptions'); //gets the galler option's dropdown
    let btnUpload = document.querySelector('#btnUpload')
    let btnUploadDoc = document.querySelector('#btnDocUpload')

    let rdbtn_upload_type = document.querySelector('.uploadtype_selection') //gets the div for selecting upload type in UPLOAD SCREEN
    // let rdbtn_upload_type = document.querySelector('.uploadtype_selection')
    let doc_upload_section = document.querySelector('.doc_upload_section')
    let photo_upload_section = document.querySelector('.photo_upload_section')


    let setupScreen = document.querySelector('#setupScreen');
    let msgBox = $("#alertBox");
    let display = document.querySelector('#alert-msg')
    let msg = '';
    let files = '';
    let fileName = '';
    let fileSize = '';
    let search_exco = document.querySelector('#txt_search_exco')
    let search_member = document.querySelector('#txt_search_members')
    let lookupTable = document.querySelector('#membersTable')
    let stable = document.querySelector("#exco_table");

    function closeAlertBox(){
        window.setTimeout(function () {
            $("#alertBox").fadeOut(300)
        }, 3000);
    }
    // doc_upload_section.style.display = rdbtn_upload_type[0].checked ? 'block' : 'none'
    // console.log(target.querySelector('.uploadtype_selection'))

    // Radiobotton switch screen in upload
    if(rdbtn_upload_type != null) {
        rdbtn_upload_type.onclick= (evt)=> {
            // console.log(evt)
            doc_upload_section.style.display = (evt.target.checked && evt.target.id === 'rdbtn_uploadtype_doc') ? 'block' : 'none'
            photo_upload_section.style.display = (evt.target.checked && evt.target.id === 'rdbtn_uploadtype_photo') ? 'block' : 'none'
        }

    }
    if (uploadDocFile != null){
        uploadDocFile.onchange = (e)=> {
            files = e.target.files;
            console.log(e.target.files)
            for (const file of files){
                fileName = file.name
                fileSize = file.size
            }
        }
    }
    if(uploadType != null) {
        uploadType.onchange = ()=>{
            caption.style.display = uploadType.value == 1 ? "block" : "none"
            options.style.display = uploadType.value == 2 ? "block" : "none"
            // if (uploadType.value == 1)
            // {
            //     caption.style.display = "block";
            //     options.style.display = "none";
            // }
            // else if (uploadType.value == 2)
            // {
            //     caption.style.display = "none";
            //     options.style.display = "block";
            // }
            // else
            // {
            //     caption.style.display = "none";
            //     options.style.display = "none";
            // }
        }
    }

    // document.querySelector('#frm-upload').onsubmit = () => {
    //     alert("form submitted");
    //     console.log("Form Submitted");
    // }

    if(btnUploadDoc != null){
        btnUploadDoc.onclick = (e) => {
            e.preventDefault();
            console.log('Processing table update...')
            fetch('/uploader', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    "greeting": "Hello from the browser!",
                    "doc_form": doc_upload_form,
                    "txtChess": chess_txt.value,
                    "doc_file": {"fileName": fileName, "fileSize": fileSize}

                })
            }).then((response) =>{
                return response.text();
            }).then((text) => {
                console.log("POST response: ");
                console.log(text);
            }).catch((err) => {
                console.log(err)
            })
        }

    }

    if(btnUpload != null){
        btnUpload.onclick = (e) => {
//            e.preventDefault();
            // console.log(rdbtn_upload_type.length)
            // rdbtn_upload_type.forEach( (el)=> {
            //     console.log(el.children[0])
            // })
            // for (let i=0; i < rdbtn_upload_type.length; i++) {
            //     if (rdbtn_upload_type[i].children[0].checked){
            //         // console.log('TRUE')
            //         console.log(rdbtn_upload_type[i].children[1].textContent.trim())
            //     }
            // }
            // return false
            files = uploadFile.files;
            console.log(files.length)
            if (uploadType.value == 0){
                console.log(`No option selected ${uploadType.value}, Make sure you select an option` )
                msg = 'Make sure you select an option'
                display.innerHTML = msg;
                msgBox.fadeIn();
                closeAlertBox();
                return false
            }
            else if (uploadType.value == 1){
                if (captionText.value === "") {
                    console.log(`Enter a caption to descibe photo ${captionText.value}` )
                    msg = `Enter a caption to descibe photo`
                    display.innerHTML = msg;
                    msgBox.fadeIn();
                    closeAlertBox();
                    return false
                }
            }
            else{
                if (galleryOptions.value == 0){
                    console.log(`Select options ${galleryOptions.value}` )
                    msg = `Select options `
                    display.innerHTML = msg;
                    msgBox.fadeIn();
                    closeAlertBox();
                    return false
                }
            }
            if ('files' in uploadFile) {
                if (files.length == 0) {
                    msg = 'Please select a file to upload';
                    console.log(msg)
                    display.innerHTML = msg;
                    msgBox.fadeIn();
                    closeAlertBox();
                    return false;
                }
                else{
                    if (files.length == 1) {
                        Img2Upload = files[0];
                        console.log(Img2Upload.name)
                        console.log(Img2Upload.size)
                        // return false
                    }
                    else{
                        if (uploadType.value == 1 && (files.length !== captionText.value.split(',').length)) {
                            msg = 'Enter description corresponding to number of files uploading';
                            console.log(msg)
                            display.innerHTML = msg;
                            msgBox.fadeIn();
                            closeAlertBox();
                            return false;
                        }
                        for (let index = 0; index < files.length; index++) {
                            console.log(files[index].name)
                            console.log(`File size: ${files.item(index).size}, in MB: ${Math.round(files.item(index).size/1024)} mb`)
                            // console.log(files[index].size)
                        }
                    }
                }
            }
            // uploadImage();
            return false;
        }
    }

    function uploadImg() {
        fetch('/upload', {
            method: 'POST',

            //
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                "greeting": "Hello from the browser!"
            })
        }).then((response) =>{
            return response.text();
        }).then((text) => {
            console.log("POST response: ");
            console.log(text);
        })
    }

    function uploadImage(){
        console.log("inside uploadImage")
        const req = new XMLHttpRequest();
        req.headers = {
            'Content-Type': 'application/json'
        }
        req.open("POST", "/upload");
        req.onload = () => {
            if (req.readyState == 4 && req.status == 200) {
               // alert('READY')
            }
            //alert('loded')
            //console.log(req.text)
            console.log(req.responseText)
            const data = JSON.parse(req.responseText)
            console.log(data.success)
        }
        req.onreadystatechange = () => {

        }

        console.log(`Caption: ${captionText.value}`)
        console.log(`Gallery Type: ${galleryOptions.value}`)
        console.log(`Photo Type: ${uploadType.options[galleryOptions.selectedIndex].text}`)
        console.log(`File: ${uploadFile.value}`)
        console.log(`File: ${uploadFile.files}`)
        const data = new FormData();
        captionText = document.querySelector('#txtcaption');
        data.append('galleryType', galleryOptions)
        data.append('fototype', uploadType)
        data.append('file', files)
        data.append('caption', captionText.value)

        req.send(data)
        alert("DONE")
        // return false;
    }

    if (search_exco != null){
        // let table = document.querySelector("#exco_table");
        search_exco.onkeyup = () =>{
            memberLookup(search_exco, stable);
        }
    }

    if (search_member != null){
        search_member.onkeyup = () =>{
            memberLookup(search_member, lookupTable)
        }
    }

    // let setupScreen = document.getElementById('#setupScreen');
    setupScreen.addEventListener('onshow', function () {

        console.log('heyy');
    });

    // This section handles the popup
    $('#setupScreen').on('show.bs.modal', function (event) {
        let menu = $(event.relatedTarget)
        let modalTitle = menu.data('whatever');
        let modal = $(this)
        switch (modalTitle) {
            case "Gallery Section":
                modal.find('.modal-title').text(modalTitle)
                modal.find('.modal-label').text("Event Name")
                break;
            case "Sub Council Executives":
                modal.find('.modal-title').text(modalTitle)
                modal.find('.modal-label').text("Name of Executive")
                break;
            case "Zonal Executives":
                modal.find('.modal-title').text(modalTitle)
                modal.find('.modal-label').text("Name of Exco")
                break;
            case "Offices":
                modal.find('.modal-title').text(modalTitle)
                modal.find('.modal-label').text("Position")
                break;


            default:
                break;
        }

    })

    function memberLookup(name, tablename){
        // console.log(name);
        let filter, table, tr, td, i, txtValue;
        input = name; // document.getElementById(`${name}`);
        filter = input.value.toUpperCase();
        table = tablename;  //document.getElementById(`${tablename}`);
        tr = table.getElementsByTagName("tr");

        // Loop through all table rows, and hide those who don't match the search query
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
            }
        }
    }
    function uploadImageAjax(){
        const req = new XMLHttpRequest();
        req.headers = {
            'Content-Type': 'application/json'
        }
        req.open("POST", "/uploadAjax");
        req.onload = () => {
            if (req.readyState == 4 && req.status == 200) {
                alert('READY')
            }
            alert('loded')
            //console.log(req.text)
            console.log(req.responseText)
            const data = JSON.parse(req.responseText)
            console.log(data.success)
            // document.querySelector('.alert').alert();
        }
        console.log(`Caption: ${captionText.value}`)
        console.log(`Gallery Type: ${galleryOptions.value}`)
        console.log(`Photo Type: ${uploadType.options[galleryOptions.selectedIndex].text}`)
        console.log(`File: ${file.value}`)
        const data = new FormData();
        captionText = document.querySelector('#txtcaption');
        data.append('galleryType', galleryOptions)
        data.append('fototype', uploadType)
        data.append('file', file)
        data.append('caption', captionText.value)

        req.send(data)
        alert("DONE")
        // return false;
    }
    //setupScreen.on('show.bs.modal') = function(event)  {

    // $('#exampleModal').on('show.bs.modal', function (event) {
    //     var button = $(event.relatedTarget) // Button that triggered the modal
    //     var recipient = button.data('whatever') // Extract info from data-* attributes
    //     // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    //     // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    //     var modal = $(this)
    //     modal.find('.modal-title').text('New message to ' + recipient)
    //     modal.find('.modal-body input').val(recipient)
    //   })

    /* =================== */
    // setup section btnSaveEntry
    /* =================== */

    let btnSetup = document.querySelector('#btnSaveEntry');
    if (btnSetup != null){
        // btnSetup = document.querySelector('#btnSaveEntry');
        // console.log(document.getElementById('btnSaveEntry'));
        // console.log(btnSetup)
        // btnSetup.onclick = () => {
        //     alert('clickcedd');
        // }
    }
})