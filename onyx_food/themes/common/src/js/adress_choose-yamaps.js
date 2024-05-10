async function initMap() {   
    
    await ymaps3.ready;

    const {YMap, YMapDefaultSchemeLayer, YMapDefaultFeaturesLayer, YMapMarker} = ymaps3;
    const {YMapDefaultMarker} = await ymaps3.import('@yandex/ymaps3-markers@0.0.1')
    // Иницилиазируем карту
    var myMap = new YMap(
        // Передаём ссылку на HTMLElement контейнера
        document.getElementById('map'),

        // Передаём параметры инициализации карты
        {
            location: {
                // Координаты центра карты
                center: [38.798695,48.467692],
                // Уровень масштабирования
                zoom: 10
            }
        }
    );

    // Добавляем слой для отображения схематической карты
    myMap.addChild(new ymaps3.YMapDefaultSchemeLayer());
    // В этом слое будут маркеры.
    myMap.addChild(new ymaps3.YMapDefaultFeaturesLayer()); 
    myMap.addChild(new ymaps3.YMapFeatureDataSource({id: 'featureSource'})
);
    var myMarker;
    
    // Создание метки.
    function createMarker(coords) {
        return new YMapDefaultMarker({
            coordinates: coords,
            title: 'поиск...',
            draggable: true,
            onDragEnd: dragEndHandler
        });
    }
    function dragEndHandler(object, event){
        getAddress(event.coordinates);
    }
    function clickHandler(object, event){
            // Если метка уже создана – просто передвигаем ее.
            if (myMarker) {
                myMarker.update({
                    coordinates: event.coordinates
                });
            }
            // Если нет – создаем.
            else {
                myMarker = createMarker(event.coordinates);
                myMap.addChild(myMarker);
            }
            getAddress(event.coordinates);
    }

    const mapListener = new ymaps3.YMapListener({
        layer: 'any',
        onClick: clickHandler
    });
    

    myMap.addChild(mapListener);
    
    

    // Определяем адрес по координатам (обратное геокодирование).
    function getAddress(coords) {
        var address_components;
        var region, city, street, house;
        fetch('https://geocode-maps.yandex.ru/1.x/?apikey=ac2d9b31-07a3-4895-bd4d-9d10f092172a&geocode='+coords[0]+','+coords[1]+'&format=json')
        .then(response => response.text())
        .then(text => {
            const obj = JSON.parse(text);
            console.log(obj);
            address_components = obj.response.GeoObjectCollection.featureMember[0].GeoObject.metaDataProperty.GeocoderMetaData.Address.Components;
            region = address_components.find((element) => element.kind =='province').name;
            city = address_components.find((element) => element.kind =='locality').name;
            if(address_components.find((element) => element.kind =='street'))
                street = address_components.find((element) => element.kind =='street').name;
            else
                street = address_components.find((element) => element.kind =='district').name;
            house = address_components.find((element) => element.kind =='house').name;
            document.getElementById("add_region").setAttribute("value", region);
            document.getElementById("add_city").setAttribute("value", city);
            document.getElementById("add_street").setAttribute("value", street);
            document.getElementById("add_house").setAttribute("value", house);
            myMarker.update({
                // Формируем строку с данными об объекте.
                title: city+', '+street+', '+house,
                color: '#006efc'
            })
        });
        
            
    }
}