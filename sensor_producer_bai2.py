import pika
import json
import time
import random

# Cấu hình thông số kết nối
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
TARGET_QUEUE = 'sensor_data_queue'
TRANSMIT_INTERVAL = 3  # Khoảng thời gian gửi giữa các lần đo (giây)

def generate_telemetry_payload(device_name="sensor01"):
    return {
        "device_id": device_name,
        "temperature": round(random.uniform(25.0, 40.0), 1),
        "humidity": round(random.uniform(30.0, 70.0), 1)
    }

def run_sensor_publisher():
    connection_params = pika.ConnectionParameters(host=BROKER_HOST, port=BROKER_PORT)
    conn = pika.BlockingConnection(connection_params)
    mq_channel = conn.channel()
    
    # Khai báo hàng đợi nhận dữ liệu cảm biến
    mq_channel.queue_declare(queue=TARGET_QUEUE, durable=True)

    try:
        while True:
            telemetry_data = generate_telemetry_payload()
            json_payload = json.dumps(telemetry_data)
            
            mq_channel.basic_publish(
                exchange='',
                routing_key=TARGET_QUEUE,
                body=json_payload
            )
            print(f" [x] Sent data: {telemetry_data}")
            time.sleep(TRANSMIT_INTERVAL)
    except KeyboardInterrupt:
        print("\n[*] Da dung sensor publisher.")
    finally:
        conn.close()

if __name__ == '__main__':
    run_sensor_publisher()