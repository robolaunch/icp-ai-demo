from kafka import KafkaConsumer, KafkaProducer
import snap7, json, yaml, sys, logging
from pydantic import BaseModel, Field
from typing import List, Union

class KafkaConfig(BaseModel):
    ip: str = Field(description="IP of the Kafka broker")
    port: int = Field(description="Port of the Kafka broker")
    topic: str = Field(description="Topic to listen")

class PLCActionConfig(BaseModel):
    stop_message: str = Field(description="Stop message", alias="stopMessage")
    start_message: str = Field(description="Start message", alias="startMessage")
    circuit_key_id: int = Field(description="Circuit key ID", alias="circuitKeyID")
    datablock_id: int = Field(description="Datablock ID", alias="datablockID")

class PLCConfig(BaseModel):
    ip: str = Field(description="IP of the PLC")
    rack: int = Field(description="Rack of the PLC")
    slot: int = Field(description="Slot of the PLC")
    action: PLCActionConfig

class PLCClientConfig(BaseModel):
    kafka: KafkaConfig
    plc: PLCConfig

class DSMinimalObject(BaseModel):
    """Represents a single object detected by the sensor."""
    id: str = Field(description="Unique identifier for the object")
    x_min: float = Field(description="Minimum X coordinate of the bounding box")
    y_min: float = Field(description="Minimum Y coordinate of the bounding box")
    x_max: float = Field(description="Maximum X coordinate of the bounding box")
    y_max: float = Field(description="Maximum Y coordinate of the bounding box")
    label: str = Field(description="Label of the detected object")

class DSMinimalSensorData(BaseModel):
    """Represents sensor data in the provided JSON format."""
    version: str = Field(default="4.0", description="Version of the data format")
    id: str = Field(description="Sensor identifier")
    timestamp: str = Field(description="Timestamp of the data (ISO 8601 format)", alias="@timestamp")
    sensorId: str = Field(description="Full sensor ID")
    objects: List[Union[str, DSMinimalObject]] = Field(
        description="List of detected objects or raw object data strings"
    )

#####################################################################################################################
#####################################################################################################################
#####################################################################################################################

if len(sys.argv) < 2:
    logging.error("Konfigürasyon dosyası bulunamadı.")
    exit(1)


with open(sys.argv[1]) as stream:
    try:
        data = yaml.safe_load(stream)
        cfg = PLCClientConfig.model_validate(data)
    except yaml.YAMLError as exc:
        logging.error(exc)
        exit(1)

try:
    kafka_broker_url = cfg.kafka.ip + ":" + str(cfg.kafka.port)
    sensor_topic = cfg.kafka.topic
    consumer = KafkaConsumer(sensor_topic,
                         bootstrap_servers=[kafka_broker_url],
                         auto_offset_reset='latest')
    producer = KafkaProducer(bootstrap_servers=[kafka_broker_url])
    logging.warning("Connected to the Kafka.")
except Exception as e:
    logging.error(str(e))
    exit(1)

try:
    client = snap7.client.Client()
    client.connect(cfg.plc.ip, cfg.plc.rack, cfg.plc.slot)
    logging.warning("Connected to the PLC.")
except Exception as e:
    logging.error(str(e))
    exit(1)

logging.warning("Starting to listen topic: " + cfg.kafka.topic)

for message in consumer:

    msg_bytes = message.value
    decoded_msg = msg_bytes.decode("utf-8")

    if cfg.plc.action.start_message in decoded_msg:
        logging.warning("Anahtar yeniden açılıyor.")

        command = 1
        client.write_area(snap7.types.Areas.PE, cfg.plc.action.datablock_id, cfg.plc.action.circuit_key_id, bytearray([command]))

        current_data = client.read_area(snap7.types.Areas.PE, cfg.plc.action.datablock_id, cfg.plc.action.circuit_key_id, 1)
        logging.warning("Anahtar değeri: " + str(int.from_bytes(current_data, "big")))
        continue

    try:
        sensor_data = DSMinimalSensorData(**json.loads(decoded_msg))
        logging.warning("Sensörden veri alındı.")
    except:
        logging.warning("Sensör dışı mesaj atlanıyor.")
        continue

    if cfg.plc.action.stop_message in str(sensor_data.objects):

        logging.warning("Delik tespit edildi. Anahtar kapatılıyor.")
        
        # stop PLC circuit key

        command = 0
        client.write_area(snap7.types.Areas.PE, cfg.plc.action.datablock_id, cfg.plc.action.circuit_key_id, bytearray([command]))
        
        current_data = client.read_area(snap7.types.Areas.PE, cfg.plc.action.datablock_id, cfg.plc.action.circuit_key_id, 1)
        logging.warning("Anahtar değeri: " + str(int.from_bytes(current_data, "big")))