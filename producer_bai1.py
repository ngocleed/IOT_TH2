import pika

# Cấu hình kết nối RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
QUEUE_NAME = 'iot_lab_queue'

def send_greeting():
    # Khởi tạo tham số kết nối và kênh truyền AMQP
    conn_params = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    try:
        # Khai báo hàng đợi bền vững
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        # Nội dung thông điệp kèm thông tin sinh viên
        student_message = "Xin chao tu ung dung Python AMQP - Le Tuan Minh - B23DCCN551"
        
        # Gửi thông điệp vào hàng đợi
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=student_message.encode('utf-8')
        )
        print(f" [x] Da gui: '{student_message}'")
    finally:
        connection.close()

if __name__ == '__main__':
    send_greeting()