# Device Registry Service Using Flask

## Run Service

- `python flaskService.py`

## Usage

All responses will have the form

```json
{
    "command": "Any command request",
    "response": "Response regarding the command execution",
	"error": "Error Status (if Any)",
}
```

### List all devices

**Definition**

`GET /devices`

**Response**

- `200 OK` on success

```json
{
  "command": "devices",
  "error": "none",
  "response": [
    {
      "deviceId": "10e1d24fa4b7",
      "deviceName": "Home1",
      "sensors": "{'temperature': '64741f70d21a', 'pressure': 'df7a97ed80f7'}"
    }
  ]
}
```

### Registering a new device

**Definition**

`POST /addDevice`

**Arguments**

- `"deviceId":string` a globally unique identifier for this device
- `"deviceName":string` a friendly name for this device
- `"preSenId":string` a unique identifier for the connected pressure sensor
- `"tempSenId":string` a unique identifier for the connected temperature sensor

If a device with the given identifier already exists, then the error generated will be sent.

**Response**

- `200` on success

```json
{
  "command": "addDevice",
  "error": "none",
  "response": "10e1d24fa4b7"
}
```


### Update Device name

`POST /updateDevice`

**Response**

- `200 OK` on success

```json
{
  "command": "updateDevice",
  "error": "none",
  "response": "10e1d24fa4b7"
}
```

### Send/Save Data of device

**Definition**

`POST /deviceData`

**Response**

- `200 OK` on success

```json
{
  "command": "deviceData",
  "error": "none",
  "response": "10e1d24fa4b7"
}
```

### Retrive Data from server

**Definition**

`GET /getData`

**Response**

- `200 OK` on success

```json
{
  "command": "getData",
  "error": "none",
  "response": [
    {
      "id": 1,
      "pressure": 22.0,
      "temperature": 30.0,
      "timestamp": "Sun, 27 Mar 2022 12:38:00 GMT"
    },
    {
      "id": 2,
      "pressure": 43.0,
      "temperature": 44.0,
      "timestamp": "Sun, 27 Mar 2022 12:59:25 GMT"
    }
  ]
}
```

### API Requests

**Examples**

- List Devices: http://localhost:5000/devices/

- Add Device: http://localhost:5000/addDevice?deviceId=10e1d24fa4b7&deviceName=Work1&preSenId=df7a97ed80f7&tempSenId=64741f70d21a

- Change Device Name: http://localhost:5000/updateDevice?deviceId=10e1d24fa4b7&newDeviceName=Residence1

- Upload/Send Data: http://localhost:5000/deviceData?deviceId=10e1d24fa4b7&presValue=22&tempValue=30

- Retrive Data: http://localhost:5000/getData?deviceId=10e1d24fa4b7&startTime=20220327T113800Z&endTime=20220327T133800Z


### MySQL Database 

**Steps For Database Configuration**

- Download 'Iot.db' to your desktop and Open Chrome/Any Browser
- Use Phpmyadmin to manage your MySQL database (We are using XAMPP Server)
- Use the SQL Query "'CREATE DATABASE shorelineiot;"' to create an empty database.
- Select the 'Shorelineiot.db' in Import Tab/ drag and drop the 'Shorelineiot.db' into the Import Page.
- After the file has been uploaded, scroll down to the bottom and click the "GO" button.
- Now, you can check the database configured as per our requirement.


### Some Generated MAC Addresses:
- `10e1d24fa4b7`
- `df7a97ed80f7`
- `64741f70d21a`
- `bd36d3bf2556`
- `a719fa29a525`
- `beb9150b5c5a`
