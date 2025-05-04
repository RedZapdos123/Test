(async () =>{
    //Configurations for downloads
    //the start file ID.
    const startID = 3215;
    //The end file ID.
    const endID = 3315;
    //The delay between the downloads(in milliseconds).
    const pauseMs = 500;
  
    //Loop through each file ID for extraction, and downloading.
    for(let id = startID; id <= endID; id++){
      const pageUrl = `https://erp.iiita.ac.in/popup/acad1/report/receipt//${id}/2/`;
  
      try{
        //Fetch the page HTML with your session cookies.
        const resp = await fetch(pageUrl,{
        //Include the logged-in cookies.
          credentials: "include"
        });
        if(!resp.ok) throw new Error(`HTTP ${resp.status}`);
  
        //Read the HTML as text.
        const html = await resp.text();
  
        //Parse the HTML string into a Document Object Model (DOM).
        const doc = new DOMParser().parseFromString(html, "text/html");
  
        //Search for the PDF URL, and store it for extraction, and downloading the PDF.
        let pdfUrl = null;
        const embed = doc.querySelector('embed[type="application/pdf"]');
        const objectEl = doc.querySelector('object[type="application/pdf"]');
        if(embed && embed.src){
          pdfUrl = embed.src;
        } else if(objectEl && objectEl.data){
          pdfUrl = objectEl.data;
        }
  
        if(!pdfUrl){
          console.warn(`ID ${id}: PDF URL not found.`);
          continue;
        }
  
        //Trigger the native download.
        const link = document.createElement('a');
        link.href = new URL(pdfUrl, location.origin).href;
        link.download = `${id}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
  
        console.log(`Queued download for ${id}.pdf`);
      } catch (err){
        console.error(`❌ ID ${id} failed:`, err);
      }
  
      //Throttle to avoid hammering the server.
      await new Promise(res => setTimeout(res, pauseMs));
    }
  
    console.log("All downloads have been completed.");
  })();
  