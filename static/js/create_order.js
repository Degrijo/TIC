$(function() {
    mWrap = new MapsWrapper({
        mapDivId: "map2d" // тут указываем ID canvas’a, в котором будет рисоваться карта
    });
});
console.log('here')
MapsWrapper = function(properties) {
    this.initialize(properties);
};
$.extend(MapsWrapper.prototype, {
    v2DMapDiv                : null,
    v2DMapComponent   : null,

    initialize: function(prop){
        this.v2DMapDiv = prop.mapDivId;
        this.initMap();
    },

    initMap: function(){
        var GlobalParams = {
            staticMapUrl: ["http://gate.looxity.ru:8088/map.html", "http://zain.looxity.ru:8088/map.html", "http://kaph.looxity.ru:8088/map.html"],
            initCrd     : {x: 7445, y: 9925},
            initZoom    : 0.25,
            zoomList    : [1, 0.5, 0.25, 0.1, 0.05, 0.025],
            miniMap     : true,
            tools       : {scaler: true, polygoner: true}
        };
        this.v2DMapComponent = new CanvasMapper (this.v2DMapDiv);
        this.v2DMapComponent.initialize(GlobalParams);
    }
});
