const customerForm = document.getElementById('customer-form')
const photoInput = document.getElementById('id_photo')
// console.log(photoInput)
const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const progressBox = document.getElementById('progress-box')
const cancelBox = document.getElementById('cancel-box')
const cancelBtn = document.getElementById('cancel-btn')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
// console.log(csrf)
photoInput.addEventListener('change', ()=>{
    progressBox.classList.remove('not-visible')
    cancelBox.classList.remove('not-visible')
    const img_data = photoInput.files[0]
    const url = URL.createObjectURL(img_data)
    console.log(img_data)
    const fd = new FormData()
    // console.log(csrf)
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('photo', img_data)
    $.ajax({
        type: 'POST',
        url: customerForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        beforeSend: function() {
            alertBox.innerHTML = ""
            imageBox.innerHTML = ""

        },
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e=>{
                // console.log(e)
                if (e.lengthComputable) {
                    const percent = e.loaded / e.total * 100
                    progressBox.innerHTML = `<div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100">
                    <div class="progress-bar" style="width: ${percent}%"></div>
                  </div><p>${percent.toFixed(1)}%</p>`
                }
            })
            cancelBtn.addEventListener('click', ()=>{
                xhr.abort()
                setTimeout(()=>{
                    customerForm.reset()
                    progressBox.innerHTML = ""
                    cancelBox.classList.add('not-visible')
    
                }, 2000)
            })
            return xhr

        },
        success: function(response) {
            // console.log(response)
            cancelBox.classList.add('not-visible')
            // progressBox.classList.add('not-visible')
            imageBox.innerHTML = `<img src="${url}" width="300px">`
            alertBox.innerHTML = `<div class="alert alert-success" role="alert">Successfully Uploaded..</div>`
        },
        error: function(error) {
            console.log(error)
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">Error happened..</div>`
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})

