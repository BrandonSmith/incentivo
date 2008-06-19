var tl;
function onLoad() {
  var eventSource = new Timeline.DefaultEventSource();
  var bandInfos = [
    Timeline.createBandInfo({
        eventSource:    eventSource,
        date:           "May 1 2007",
        width:          "70%", 
        intervalUnit:   Timeline.DateTime.MONTH, 
        intervalPixels: 100
    }),
    Timeline.createBandInfo({
        showEventText:  false,
        trackHeight:    0.5,
        trackGap:       0.2,
        eventSource:    eventSource,
        date:           "May 1 2007",
        width:          "30%", 
        intervalUnit:   Timeline.DateTime.YEAR, 
        intervalPixels: 200
    })
  ];
  bandInfos[1].syncWith = 0;
  bandInfos[1].highlight = true;
  bandInfos[1].eventPainter.setLayout(bandInfos[0].eventPainter.getLayout());  
  
  tl = Timeline.create(document.getElementById("my-timeline"), bandInfos);
  Timeline.loadXML("/resources/financas-pessoais-calendario.xml", function(xml, url) { eventSource.loadXML(xml, url); });
}

var resizeTimerID = null;
function onResize() {
    if (resizeTimerID == null) {
        resizeTimerID = window.setTimeout(function() {
            resizeTimerID = null;
            tl.layout();
        }, 500);
    }
}