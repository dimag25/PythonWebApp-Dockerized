
            var dbCount=0 ;
              function getOption() {
                    selectElement = document.querySelector('#moviesWebsites');
                    output = selectElement.options[selectElement.selectedIndex].value;
                    document.querySelector('#resultDownload').value = output;
                }

       async function start_download() {
            await taskStart();
            await sleep(15000);
            taskEnd();
            showMessage();
        }

             async function updateMongoDB() {
        var toast = Metro.toast.create;
                var options = {
                showTop: true,
                timeout: 5000,
                keepOpen: true
            }
        handleProgressBar();
        toast("Updating Mongo DB in progress ....<br>Please don't close the Application", async function(){
            updateDB();
            }, null, "bg-green fg-white",options);
        }

        function updateDB(){
            $.ajax({
                url: '/updateDB',
                type: 'GET',
                data: $('dbCount'),  success: function(data) {
            dbCount= data.dbCount;
            console.log(dbCount);  // I can se data but I need outside ajax call
        }
            });
        }

        async function  handleProgressBar(){
        progress = $("#progress-observe").data("progress")
            m_counter=0
            while(m_counter<dbCount){
              m_counter += 100;
              await sleep(1000);
              progress.val((m_counter/dbCount).toFixed(2) * 100);
            }
      }


      async function handleProgressFinish(){
      alert('Update Mongo DB Completed Successfully!!!');
     }





            function taskStart(){
            progress = Metro.activity.open({
                type: 'square',
                overlayColor: '#fff',
                overlayAlpha: 1,
                text: '<div class=\'mt-2 text-small\'>Please wait,while downloading movies...</div>',
                overlayClickClose: true
            });
        }

        function showMessage(){
     var notify = Metro.notify;

        if(movies=="Error"){
        notify.create("Error Occurs while downloading" , "Failed to  downloaded", {
            cls: "alert",keepOpen: true
        });
        }
            else{
        notify.create(" Movies!!" , "Successfully Updated", {
            cls: "bg-green fg-white", keepOpen: true
        });
            }

             notify.setup({
            width: 3000,
            duration: 50000,
            animation: 'easeOutBounce'
        });
    }





    function taskEnd() {
            Metro.activity.close(progress);
        }

function callbackFunc(response) {
    // do something with the response
    //showMessage(response);
    console.log("success!!!");
}


//sleep for millisceond
      function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
      }


$( document ).ready(function() {

    $('#btnUpdateDB').on('submit',function(event){
//This is where the data is sent
    $.ajax({
        url: '/updateDB',
        type: 'GET',
        data: $('dbCount'),
    })
//this is done when the response is received
    .done(function(data) {
        console.log("success " + data);
    });

    event.preventDefault();
});

        $("#btnHome").on("click",function () {
            $("#sectionHome").delay(500).fadeIn('500');
             $("#aboutSection").fadeOut('500');
            $("#sectionResult").fadeOut('500');
            $("#TorrentsSectionResult").fadeOut('500');
           $("#updateDBSection").delay(250).fadeOut('500');
        });

            $("#btnOnlineResult").on("click",function () {
            $("#sectionResult").delay(500).fadeIn('500');
             $("#sectionHome").fadeOut('500');
            $("#aboutSection").fadeOut('500');
            $("#TorrentsSectionResult").fadeOut('500');
           $("#updateDBSection").delay(250).fadeOut('500');
        });

             $("#btnTorrentsResult").on("click",function () {
            $("#sectionHome").fadeOut('500');
           $("#sectionResult").fadeOut('500');
             $("#updateDBSection").fadeOut('500');
            $("#TorrentsSectionResult").delay(500).fadeIn('500');
            $("#aboutSection").delay(250).fadeOut('500');
        });

            $("#btnUpdateDB").on("click",function () {
            $("#sectionHome").fadeOut('500');
            $("#sectionResult").fadeOut('500');
            $("#TorrentsSectionResult").fadeOut('500');
           $("#aboutSection").delay(250).fadeOut('500');
            $("#updateDBSection").delay(500).fadeIn('500');
        });
               $("#btnAbout").on("click",function () {
            $("#aboutSection").delay(500).fadeIn('500');
             $("#sectionHome").fadeOut('500');
            $("#sectionResult").fadeOut('500');
            $("#TorrentsSectionResult").fadeOut('500');
           $("#updateDBSection").delay(250).fadeOut('500');
        });
});
