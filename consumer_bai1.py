import pika
import time

# Cấu hình kết nối RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
QUEUE_NAME = 'iot_lab_queue'

def on_message_received(channel, method_frame, header_frame, body):
    received_timestamp = time.strftime("%H:%M:%S")
    message_content = body.decode('utf-8')
    print(f"Da nhan message: {message_content}")
    print(f"Thoi gian nhan: {received_timestamp}")

def start_listening():
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Khai báo queue đảm bảo tồn tại
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Đăng ký hàm xử lý khi nhận message
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=on_message_received,
        auto_ack=True
    )

    print(' [*] Consumer dang cho message. Nhan CTRL+C de thoat.')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[*] Da dung consumer theo yeu cau.")
    finally:
        connection.close()

if __name__ == '__main__':
    start_listening()