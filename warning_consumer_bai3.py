import pika

# Cấu hình kết nối RabbitMQ
AMQP_HOST = 'localhost'
AMQP_PORT = 5672
ALERT_EXCHANGE = 'iot_alert_exchange'
WARNING_QUEUE = 'warning_queue'
BINDING_KEY = 'warning'

def on_warning_received(ch, method, properties, body):
    event_text = body.decode('utf-8')
    print(f"[{WARNING_QUEUE}] Da nhan: {event_text}")

def start_warning_listener():
    conn_params = pika.ConnectionParameters(host=AMQP_HOST, port=AMQP_PORT)
    conn = pika.BlockingConnection(conn_params)
    channel = conn.channel()

    # Khai báo exchange direct và queue
    channel.exchange_declare(exchange=ALERT_EXCHANGE, exchange_type='direct')
    channel.queue_declare(queue=WARNING_QUEUE, durable=True)

    # Ràng buộc queue với exchange theo routing key 'warning'
    channel.queue_bind(exchange=ALERT_EXCHANGE, queue=WARNING_QUEUE, routing_key=BINDING_KEY)

    channel.basic_consume(
        queue=WARNING_QUEUE,
        on_message_callback=on_warning_received,
        auto_ack=True
    )

    print(' [*] Cho canh bao muc WARNING...')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[*] Da dung warning consumer.")
    finally:
        conn.close()

if __name__ == '__main__':
    start_warning_listener()