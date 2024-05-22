from kafka import KafkaConsumer, KafkaProducer
import json, yaml, sys, logging
from pydantic import BaseModel, Field
from typing import List, Union
from dateutil import parser
import datetime

class KafkaConfig(BaseModel):
    ip: str = Field(description="IP of the Kafka broker")
    port: int = Field(description="Port of the Kafka broker")
    topic: str = Field(description="Topic to listen")
    group: str = Field(description="Group of the Kafka topic")

class RecordingActionConfig(BaseModel):
    start_message: str = Field(description="Start message", alias="startMessage")
    delta_seconds: int = Field(description="Delta seconds", alias="deltaSeconds")

class RecordingAgentConfig(BaseModel):
    consumed_kafka: KafkaConfig = Field(description="Consumed Kafka", alias="consumedKafka")
    produced_kafka: KafkaConfig = Field(description="Produced Kafka", alias="producedKafka")
    action: RecordingActionConfig

class RecordingMessageSensor(BaseModel):
    id: str

class RecordingMessage(BaseModel):
    command: str
    start: str
    # end: str
    sensor: RecordingMessageSensor

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
        cfg = RecordingAgentConfig.model_validate(data)
    except yaml.YAMLError as exc:
        logging.error(exc)
        exit(1)

try:
    consumed_kafka_broker_url = cfg.consumed_kafka.ip + ":" + str(cfg.consumed_kafka.port)
    consumer = KafkaConsumer(cfg.consumed_kafka.topic,
                         bootstrap_servers=[consumed_kafka_broker_url],
                         auto_offset_reset='latest')
    produced_kafka_broker_url = cfg.produced_kafka.ip + ":" + str(cfg.produced_kafka.port)
    producer = KafkaProducer(bootstrap_servers=[produced_kafka_broker_url])
    logging.warning("Connected to the Kafka.")
except Exception as e:
    logging.error(str(e))
    exit(1)

logging.warning("Starting to listen topic: " + cfg.consumed_kafka.topic)

for message in consumer:

    msg_bytes = message.value
    decoded_msg = msg_bytes.decode("utf-8")

    try:
        sensor_data = DSMinimalSensorData(**json.loads(decoded_msg))
        logging.warning("Sensörden veri alındı.")
    except:
        logging.warning("Sensör dışı mesaj atlanıyor.")
        continue

    if cfg.action.start_message in str(sensor_data.objects):

        logging.warning("Delik tespit edildi. Görüntü kaydı isteği gönderiliyor.")
        
        incoming_ts_dt = parser.parse(sensor_data.timestamp)
        
        recording_start_ts_dt = incoming_ts_dt - datetime.timedelta(seconds=cfg.action.delta_seconds)
        recording_end_ts_dt = incoming_ts_dt + datetime.timedelta(seconds=cfg.action.delta_seconds)
        recording_start_ts_str = recording_start_ts_dt.isoformat(timespec="milliseconds").replace('+00:00', 'Z')
        recording_end_ts_str = recording_end_ts_dt.isoformat(timespec="milliseconds").replace('+00:00', 'Z')

        recording_msg_model = RecordingMessage(
            command="start-recording",
            start=recording_start_ts_str,
            # end=recording_end_ts_str,
            sensor=RecordingMessageSensor(
                id=sensor_data.sensorId
            )
        )

        recording_msg_str = recording_msg_model.model_dump_json(indent=4)
        future = producer.send(topic=cfg.produced_kafka.topic, value=bytes(recording_msg_str, "utf-8"))
        try:
            record_metadata = future.get(timeout=10)
            logging.warning("Görüntü kaydı için komut gönderildi.")
        except Exception as e:
            logging.error("Kayıt mesajı gönderilemedi.")
            logging.error(str(e))
        
        continue