import pika
import json

# Cấu hình thông số kết nối
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
LISTEN_QUEUE = 'sensor_data_queue'

# Ngưỡng kích hoạt cảnh báo môi trường
MAX_SAFE_TEMP = 35.0
MIN_SAFE_HUMIDITY = 40.0

def process_sensor_event(ch, delivery_method, properties, payload_bytes):
    try:
        sensor_info = json.loads(payload_bytes.decode('utf-8'))
        device_name = sensor_info.get('device_id', 'Unknown')
        current_temp = float(sensor_info.get('temperature', 0.0))
        current_humid = float(sensor_info.get('humidity', 0.0))

        print(f"\nDevice: {device_name}")
        print(f"Temperature: {current_temp}")
        print(f"Humidity: {current_humid}")

        if current_temp > MAX_SAFE_TEMP:
            print("CANH BAO: Nhiet do cao")
        if current_humid < MIN_SAFE_HUMIDITY:
            print("CANH BAO: Do am thap")
    except (json.JSONDecodeError, KeyError, ValueError) as err:
        print(f"[!] Loi phan tich du lieu sensor: {err}")

def start_monitor():
    conn_params = pika.ConnectionParameters(host=BROKER_HOST, port=BROKER_PORT)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue=LISTEN_QUEUE, durable=True)
    channel.basic_consume(
        queue=LISTEN_QUEUE,
        on_message_callback=process_sensor_event,
        auto_ack=True
    )

    print(' [*] Monitor dang cho du lieu sensor...')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[*] Da dung monitor.")
    finally:
        connection.close()

if __name__ == '__main__':
    start_monitor()