$(function() {
    mWrap = new MapsWrapper({
        mapDivId: "map2d" // тут указываем ID canvas’a, в котором будет рисоваться карта
    });
});

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
        let GlobalParams = {
            staticMapUrl: ["http://gate.looxity.ru:8088/map.html", "http://zain.looxity.ru:8088/map.html", "http://kaph.looxity.ru:8088/map.html"],
            initCrd     : {x: user_country[0], y: user_country[1]},
            initZoom    : 0.25,
            zoomList    : [1, 0.5, 0.25, 0.1, 0.05, 0.025],
            miniMap     : true,
            tools       : {scaler: true, polygoner: true},
            zoom: 0.5
        };
        this.v2DMapComponent = new CanvasMapper(this.v2DMapDiv);
        this.v2DMapComponent.initialize(GlobalParams);
    }
});
