# CAP API

The CAP API is a json REST API to publish and get earthquake alerts in CAP format.

## API Documentation

The CAP RSS API is a json REST API from which seismic alerts and events can be requested.

### Base URL

```shell
https://rss.sasmex.net/api/v1
```

### Authentication

Authentication is required to post alerts. Include the Authorization header with a valid API key in your requests.

### Endpoints

#### Add new alert

- **Endpoint**: POST /alerts/
- **Description**: Add a new alert
- **Request Format**: JSON
- **Request Example**:

```json
{
  "time": "2023-09-13T15:36:41",
  "states": [40, 41],
  "region": 40101,
  "is_event": false,
  "id": "AlertID3",
  "references": ["ALERTID1", "ALERTID2"]
}
```
- **Response Format**: JSON
- **Response Example**:

```json
{
  "time": "2023-09-13T15:36:41",
  "states": [40, 41],
  "region": 40101,
  "is_event": false,
  "id": "AlertID3",
  "references": ["ALERTID1", "ALERTID2"]
}
```

**Notes**:
- Date time must be in iso format.
- States is a list with the state codes (see state codes below).
- Region uses the code of the region (see region codes below).
- References is a list with the identifiers of the alerts references by the posted alert. It is
only used when the alert is an update of a previous one.

#### Get alert by ID

- **Endpoint**: GET /alerts/{identifier}
- **Description**: Get the alert with the given identifier.
- **Response Format**: JSON
- **Response Example**:

```json
{
  "time": "2023-09-13T15:36:41",
  "states": [40, 41],
  "region": 40101,
  "is_event": false,
  "id": "AlertID3",
  "references": ["ALERTID1", "ALERTID2"]
}
```

#### List alerts

- **Endpoint**: GET /alerts/
- **Description**: List alerts in descending order of date time. Uses pagination.
- **Parameters**:
    - `{page}`:  Page to retrieve. By default, retrieves the first page.
    - `{type}`: The type of alerts to retrieve. It can be 'alert', 'event' or 'all'. The
      default is to use 'all'.
    - `{start_date} (optional)`: The desired date of the alerts. If `end_date`is also passed, it will
    retrieve alerts in the range from the start to end date (inclusive).
    - `{end_date} (optional)`: Range end date of the alerts. Must be used along with `start_date`.
    - `{region} (optional)`: Region name of the alerts. Must be in lower case and no spaces.
    - `{state} (optional)`: State code of the alerts.
- **Response Format**: JSON
- **Response Example**:

```json
{
        "alerts": [
            {
                "time": "2023-09-13T15:00:00",
                "states": [42],
                "region": 41215,
                "is_event": false,
                "id": "ALERT3",
                "references": []
            },
            {
                "time": "2023-09-12T00:00:00",
                "states": [41],
                "region": 41204,
                "is_event": false,
                "id": "ALERT2",
                "references": []
            },
            {
                "time": "2023-09-11T15:00:00",
                "states": [40],
                "region": 41201,
                "is_event": false,
                "id": "ALERT1",
                "references": []
            }
        ],
        "prev": 1,
        "next": 3,
        "count": 3
    }
```

#### Get last alert

- **Endpoint**: GET /alerts/latest/
- **Description**: Get the latest alert.
- **Response Format**: JSON
- **Response Example**:

```json
{
  "time": "2023-09-13T15:36:41",
  "states": [40, 41],
  "region": 40101,
  "is_event": false,
  "id": "AlertID3",
  "references": ["ALERTID1", "ALERTID2"]
}
```


#### Get cap file by identifier

- **Endpoint**: GET /alerts/{identifier}/cap/
- **Description**: Get the alert with the given identifier in CAP file format.
- **Parameters**:
  - `{save}`: Whether to download a cap file or return the contents of the cap file on the json response.
Can only take the values true or false. 
- **Response Format**: CAP file or JSON


## Region codes

Regions and states are represented by codes within the API. Following is a list of states and 
region codes, with their meanings:

### States

| State Code | State Name |
|------------|------------|
| 40         | CDMX       |
| 41         | Guerrero   |
| 42         | Oaxaca     |
| 43         | Michoacan  |
| 44         | Colima     |
| 45         | Jalisco    |
| 46         | Puebla     |
| 47         | Morelos    |
| 48         | Veracruz   |
| 49         | Chiapas    |


### Regions

| Region Code | Region Name        |
|------------|--------------------|
| 41201      | Petatlan Gro       |
| 41202      | Petatlan Gro       |
| 41203      | Atoyac Gro         |
| 41204      | Guerrero           |
| 41205      | Atoyac Gro         |
| 41206      | Acapulco Gro       |
| 41207      | Acapulco Gro       |
| 41208      | SanMarcos Gro      |
| 41209      | Guerrero           |
| 41210      | Guerrero           |
| 41211      | SanMarcos Gro      |
| 41212      | Costa Gro-Oax      |
| 41213      | Petatlan Gro       |
| 41214      | Petatlan Gro       |
| 41215      | Zihuatanejo Gro    |
| 41216      | Guerrero           |
| 41217      | Zihuatanejo Gro    |
| 41218      | Costa Gro-Mich     |
| 41219      | Guerrero           |
| 41220      | Guerrero           |
| 41221      | Guerrero           |
| 41222      | Guerrero           |
| 41223      | Guerrero           |
| 41224      | Guerrero           |
| 41225      | Guerrero           |
| 41226      | Guerrero           |
| 41227      | Guerrero           |
| 41228      | Guerrero           |
| 41229      | Guerrero           |
| 41230      | Guerrero           |
| 41231      | Guerrero           |
| 41232      | Guerrero           |
| 41233      | Guerrero           |
| 41301      | Guerrero           |
| 41302      | Guerrero           |
| 41303      | Guerrero           |
| 41304      | Guerrero           |
| 41305      | Guerrero           |
| 41306      | Guerrero           |
| 41307      | Guerrero           |
| 41308      | Guerrero           |
| 41309      | Guerrero           |
| 41310      | Guerrero           |
| 41311      | Guerrero           |
| 41312      | Guerrero           |
| 41313      | Guerrero           |
| 41401      | Guerrero           |
| 41402      | Guerrero           |
| 42101      | Guerrero           |
| 42201      | Costa Oax-Gro      |
| 42202      | Oaxaca             |
| 42203      | Costa Oax-Gro      |
| 42204      | Pinotepa Oax       |
| 42205      | Pinotepa Oax       |
| 42206      | PtoEscondido Oax   |
| 42207      | Oaxaca             |
| 42208      | PtoEscondido Oax   |
| 42209      | Huatulco Oax       |
| 42210      | Oaxaca             |
| 42211      | Huatulco Oax       |
| 42212      | SalinaCruz Oax     |
| 42213      | Oaxaca             |
| 42214      | SalinaCruz Oax     |
| 42215      | Oax Centro         |
| 42216      | Oaxaca             |
| 42217      | Oaxaca             |
| 42218      | Oax Centro         |
| 42219      | Huatulco Oax       |
| 42220      | Huajuapan Oax      |
| 42221      | Huajuapan Oax      |
| 42222      | Lim Oax-Pue        |
| 42223      | Oax Centro         |
| 42224      | Oax Centro         |
| 42225      | Tuxtepec Oax       |
| 42226      | Tuxtepec Oax       |
| 42227      | Lim Oax-Pue        |
| 42228      | Oax Centro         |
| 42229      | Oax Centro         |
| 42230      | Lim Oax-Pue        |
| 42231      | Oax Centro         |
| 42232      | Oax Centro         |
| 42233      | Lim Ver-Oax        |
| 42234      | Istmo Oax-Chis     |
| 42235      | Oaxaca             |
| 42236      | Istmo Oax-Chis     |
| 42237      | Oax Centro         |
| 42238      | Oaxaca             |
| 42239      | Oaxaca             |
| 42301      | Oaxaca             |
| 42302      | Oaxaca             |
| 42303      | Oaxaca             |
| 42304      | Oaxaca             |
| 42305      | Oaxaca             |
| 42306      | Oaxaca             |
| 42307      | Oaxaca             |
| 42308      | Oaxaca             |
| 42309      | Oaxaca             |
| 42310      | Oaxaca             |
| 42311      | Oaxaca             |
| 42312      | Oaxaca             |
| 42401      | Oaxaca             |
| 43101      | Oaxaca             |
| 43201      | Costa Mich-Gro     |
| 43202      | Playa Azul Mich    |
| 43203      | Playa Azul Mich    |
| 43204      | Costa Mich         |
| 43205      | Costa Mich         |
| 43206      | Costa Mich         |
| 43207      | Costa Mich-Col     |
| 43208      | Costa Mich         |
| 43209      | Costa Mich         |
| 43301      | Costa Mich         |
| 43302      | Costa Mich         |
| 43303      | Costa Mich         |
| 43304      | Costa Mich         |
| 43401      | Costa Mich         |
| 44101      | Costa Mich         |
| 44201      | Costa Col          |
| 44202      | Costa Col          |
| 44203      | Costa Col          |
| 44204      | Costa Col          |
| 44205      | Costa Col          |
| 44301      | Costa Col          |
| 44302      | Costa Col          |
| 44401      | Costa Col          |
| 45101      | Costa Col          |
| 45201      | Costa Jal          |
| 45202      | Costa Jal          |
| 45203      | Costa Jal          |
| 45204      | Costa Jal          |
| 45205      | Costa Jal          |
| 45206      | Costa Jal          |
| 45301      | Costa Jal          |
| 45302      | Costa Jal          |
| 45303      | Costa Jal          |
| 45304      | Costa Jal          |
| 45401      | Costa Jal          |
| 46101      | Costa Jal          |
| 46201      | Puebla             |
| 46202      | Puebla             |
| 46203      | Puebla             |
| 46204      | Puebla             |
| 46205      | Puebla             |
| 46401      | Puebla             |
| 47101      | Puebla             |
| 47301      | Morelos            |
| 47401      | Morelos            |
| 48201      | Veracruz           |
| 48202      | Veracruz           |
| 48203      | Veracruz           |
| 48204      | Veracruz           |
| 48205      | Veracruz           |
| 48206      | Veracruz           |
| 48207      | Veracruz           |
| 48208      | Veracruz           |
| 48209      | Veracruz           |
| 49201      | Chiapas            |
| 49202      | Chiapas            |
| 49203      | Chiapas            |
| 49204      | Chiapas            |
| 49205      | Chiapas            |
| 49206      | Chiapas            |
| 49207      | Chiapas            |
| 49208      | Chiapas            |
| 49209      | Chiapas            |
| 49210      | Chiapas            |
| 49211      | Chiapas            |
| 49212      | Chiapas            |
| 49213      | Chiapas            |
| 49214      | Chiapas            |
| 49215      | Chiapas            |
| 49216      | Chiapas            |
