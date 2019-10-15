function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


$(document).ready(function () {
    $(".form-download").submit(function (e) {
        e.preventDefault();
        console.log($(this).serializeArray());
    });

     $('#load-more-btn').click(function () {
         window.location.href = "/";
     });



    $('#submit-btn').click(async function convertProcess() {
        $(".step1").hide(300);

        let csrf = $("[name ='csrfmiddlewaretoken']").val();



        let xhr = new XMLHttpRequest();
        xhr.responseType = 'text';
        xhr.onreadystatechange = function () {
            let a;
            if (xhr.readyState === 4 && xhr.status === 200) {
                a = document.createElement('a');
                a.href = 'download/' + xhr.response;
                a.style.display = 'none';
                document.body.appendChild(a);
                a.click();
            }
        };
        xhr.open("POST", "convert/");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("X-CSRFToken", csrf);
        let data = {
            form: $(".form-download").serializeArray(),

        }
        xhr.send(JSON.stringify(data));

         $(".step2").show(100);
        await sleep(3000);

        // $.post("convert/", $(".form-download").serializeArray(), function (data) {
        //
        // });
        $(".step2").hide(100);
        $(".step3").show(100);
    });

});
