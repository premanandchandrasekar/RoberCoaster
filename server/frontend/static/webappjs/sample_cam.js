Webcam.attach('#webcam');

Webcam.set({
    width: 640,
    height: 480,
    dest_width: 640,
    dest_height: 480,
});

flag = true

function take_snapshot() {
    var data_uri = Webcam.snap();
    Webcam.upload(data_uri, "api/latest/camupload", function(code, res) {
        res = JSON.parse(res);
        $("#textcam").html(res.text);
        if(res.pan != "11"){
            $("#pan").html("<span style='margin-left: 358px;font-size:12px;text-shadow: 0 0 5px #008000;'>Your PAN id: </span><span style='margin-left:10px;text-shadow: 0 0 5px #008000;color:orange;'>" + res.pan + "</span>");
            $("#pan_no").val(res.pan);
            if(typeof fillform != "undefined"){
                fillform();
            }
        }
        flag = true;
    } );

}

window.setTimeout(function(){
    window.setInterval(function(){
        if(flag){
            flag = false;
            take_snapshot();
        }
    }, 100);
}, 5000);

