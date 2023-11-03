import { GoogleMap, LoadScript, Polygon, Circle, MarkerClustererF } from '@react-google-maps/api';
import {COORDS, POLYGONS} from "../shared/index.js";

const containerStyle = {
    width: '400px',
    height: '400px',
};

const center = {
    lat: 19.4287,
    lng: -99.12766,
};

const markerOptions = {
    strokeColor: "#C0392B",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#E74C3C",
    fillOpacity: 0.2,
    clickable: false,
    draggable: false,
    editable: false,
    zIndex: 1
};

const circleOptions = {
    ...markerOptions,
    visible: true,
    radius: 50000,
};

const polygonOptions = {
    ...markerOptions,
    geodesic: false,
}


const Map = ({ isEvent, region, states }) => {
    // MarkerClusterF is needed to render Polygon or Circle in strict mode
    return (
        <LoadScript
            googleMapsApiKey={import.meta.env.VITE_MAPS_API_KEY}
            language="es"
            region="MX"
        >
            <GoogleMap
                mapContainerStyle={containerStyle}
                center={center}
                zoom={6}
                on
            >
                {!isEvent &&
                    <MarkerClustererF>
                        {() =>
                        <>
                            {states.map(s =>
                                <Polygon paths={POLYGONS[s]} options={polygonOptions} key={s}/>)}
                        </>
                        }
                    </MarkerClustererF>
                }
                {isEvent &&
                    <MarkerClustererF>
                        {() => <Circle options={circleOptions} center={COORDS[region]}/>}
                    </MarkerClustererF>
                }

            </GoogleMap>
        </LoadScript>
    );
}

export { Map };