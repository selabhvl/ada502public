from datetime import datetime
from typing import Any
from uuid import uuid4, UUID
from io import BytesIO
import json
import random
from time import sleep
import polars as pl

import measurements_pb2

class Coordinates:

    def __init__(self, latitude: float, longitude: float) -> None:
        if latitude > 180 or latitude < -180:
            raise AttributeError(f"Error: latitude (given={latitude}) cannot be greater than 180 degrees")
        if longitude > 180 or longitude < -180:
            raise AttributeError(f"Error: longitude (given={longitude}) cannot be greater than 180 degrees")
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return f"{round(self.latitude, 6)} {'N' if self.latitude > 0 else 'S'} {round(self.longitude, 6)} {'E' if self.longitude > 0 else 'W'}"



class Measurement:

    def __init__(self, 
                 id: UUID, 
                 timestamp: datetime,
                 coordinates: Coordinates | None,
                 value: float | int,
                 unit: str
                 ) -> None:
        self.id = id 
        self.timestamp = timestamp
        self.coordinates = coordinates
        self.value = value 
        self.unit = unit

    def __str__(self) -> str:
        return f"{self.id}: {self.value} {self.unit} at time: {self.timestamp} and geo: {self.coordinates}"


def make_random(
        timestamp : datetime | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        value: float | int | None = None,
        unit: str | None = None
    ) -> Measurement:
    if timestamp is None:
        base = 1712729133.863624
        delta = random.randint(-43200, 43200)
        timestamp = datetime.fromtimestamp(base + delta)
    if latitude is None:
        latitude = 60 + (random.random() * 5)
    if longitude is None:
        longitude = 5 + (random.random() * 5)
    if value is None:
        value = random.random() * 50 - 10
    if unit is None:
        unit = random.choice(['degC', '%', 'mm'])
    return Measurement(uuid4(), timestamp, Coordinates(latitude, longitude), value, unit)


class Wire:

    def __init__(self) -> None:
        self.buffer = BytesIO()
        self.length = 0
        
    def write(self, data: bytes):
        self.length += self.buffer.write(data)

    def read_all(self) -> bytes:
        return self.buffer.read(self.length)

    def transmit(self):
        delay = self.length * 8 / (5 * 1000 * 1000) # delay in seconds
        print(f"Transmitting {self.length} bytes with 5 Mbit/s: {delay * 1000}ms network delay")
        self.buffer.seek(0)
        sleep(delay)
#

def naive_json_serialization(m: Measurement, w: Wire) -> None:
    d = {}
    d['timestamp'] = m.timestamp.isoformat()
    d['coordinates'] = m.coordinates.__dict__
    d['id'] = str(m.id)
    d['value'] = m.value
    d['unit'] = m.unit
    w.write(json.dumps(d).encode())

def naive_json_deserialization(data: Any) -> Measurement:
    timestamp = datetime.fromisoformat(data['timestamp'])
    latitude = data['coordinates']['latitude']
    longitude = data['coordinates']['longitude']
    id = UUID(data['id'])
    value = data['value']
    unit = data['unit']
    return Measurement(id, timestamp, Coordinates(latitude, longitude), value, unit)

def naive_json_list_deserializatio(w: Wire) -> list[Measurement]:
    raw = w.read_all()
    data = json.loads(raw.decode())
    result = []
    for m in data:
        result.append(naive_json_deserialization(m))
    return result


def naive_json_list_serialization(ms: list[Measurement], w: Wire) -> None:
    w.write(b"[\n")
    first_flag = True 
    for m in ms:
        if first_flag:
            first_flag = False
        else:
            w.write(b",\n")
        naive_json_serialization(m, w)
    w.write(b"\n]")


def naive_json_roundtrip(ms: list[Measurement]) -> list[Measurement]:
    w = Wire()
    naive_json_list_serialization(ms, w)
    w.transmit()
    return naive_json_list_deserializatio(w)

def serialize_grpc(ms: list[Measurement], w: Wire):
    result = measurements_pb2.MeasurementList()
    for d in ms:
        m = result.measurements.add()
        if d.coordinates is not None:
            m.coordinates.latitude = d.coordinates.latitude
            m.coordinates.longitude = d.coordinates.longitude
        m.id = str(d.id)
        m.timestamp = int(d.timestamp.timestamp())
        if isinstance(d.value, float):
            m.value_float = d.value
        else:
            m.value_int = d.value
        m.unit = d.unit
    w.write(result.SerializeToString())

def deserialize_grpc(w: Wire) -> list[Measurement]:
    ms = measurements_pb2.MeasurementList()
    ms.ParseFromString(w.read_all())
    result = []
    for m in ms.measurements:
        id = UUID(m.id)
        timestamp = datetime.fromtimestamp(m.timestamp)
        c = None
        if m.HasField('coordinates'):
            latitude = m.coordinates.latitude
            longitude = m.coordinates.longitude
            c = Coordinates(latitude, longitude)
        if m.HasField('value_float'):
            value = m.value_float
        else:
            value = m.value_int
        unit = m.unit
        result.append(Measurement(id, timestamp,c, value, unit))
    return result

def grpc_roundtrip(ms: list[Measurement]) -> list[Measurement]:
    w = Wire()
    serialize_grpc(ms, w)
    w.transmit()
    return deserialize_grpc(w)

    
def serialize_parquet(ms: list[Measurement], w: Wire):
    ids = []
    timestamps = []
    latitudes : list[float |None]= []
    longitudes : list[float | None]= []
    units = []
    values = []
    for m in ms:
        ids.append(str(m.id))
        timestamps.append(m.timestamp)
        if m.coordinates:
            latitudes.append(m.coordinates.latitude)
            longitudes.append(m.coordinates.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)
        units.append(m.unit)
        values.append(m.value)
    df = pl.DataFrame({
        'id': ids,
        'timestamp': timestamps,
        'coordinates.latitude': latitudes,
        'coordinates.longitude': longitudes,
        'value': values,
        'unit': units
    })
    df.write_parquet(w.buffer)
    w.length = w.buffer.getbuffer().nbytes

def deserialize_parquet(w: Wire) -> pl.DataFrame:
    return pl.read_parquet(w.read_all())

def parquet_roundtrip(ms: list[Measurement]) -> pl.DataFrame:
    w = Wire()
    serialize_parquet(ms, w)
    w.transmit()
    return deserialize_parquet(w)



