async function main () {
    const videoLive = document.querySelector('#videoLive')
    const canvas = document.querySelector("canvas");
  
    const ctx = canvas.getContext("2d");

    let width = canvas.width;
    let height = canvas.height;
    
    const stream = await navigator.mediaDevices.getUserMedia({ // <1>
      video: true,
      audio: true,
    })
  
    videoLive.srcObject = stream;
  
    const updateCanvas = () => {
      ctx.drawImage(videoLive, 0, 0, width, height);
      
      var base64Data = canvas.toDataURL("image/png");
      
      var data = JSON.stringify(base64Data);
      var request = new XMLHttpRequest();
      request.open("POST", "https://192.168.3.6:5000/img_data");
      request.setRequestHeader("Content-Type", "application/json");
      request.send(data);

      videoLive.requestVideoFrameCallback(updateCanvas);


    }


    
    
    videoLive.requestVideoFrameCallback(updateCanvas);
  }
  
  main();