// Vapi widget loader — loads SDK and starts the UK Sofia assistant
(function() {
  var ASSISTANT_ID = "6933946a-8b14-4881-9725-3e4505d3a1eb";
  
  // Load Vapi SDK if not already present
  if (!window.vapiSDK) {
    var script = document.createElement('script');
    script.src = 'https://cdn.vapi.ai/widget.js';
    script.async = true;
    script.onload = function() { startVapi(); };
    script.onerror = function() { console.error('Failed to load Vapi SDK'); };
    document.head.appendChild(script);
  } else {
    startVapi();
  }
  
  function startVapi() {
    if (!window.vapiSDK) return;
    try {
      window.vapiSDK.run({
        assistant: ASSISTANT_ID,
        position: "bottom-right",
        offset: "24px"
      });
    } catch(e) {
      console.error('Vapi start failed:', e);
    }
  }
})();
