import pika

# Cấu hình kết nối RabbitMQ
AMQP_HOST = 'localhost'
AMQP_PORT = 5672
ALERT_EXCHANGE = 'iot_alert_exchange'
CRITICAL_QUEUE = 'critical_queue'
BINDING_KEY = 'critical'

def on_critical_received(ch, method, properties, body):
    critical_text = body.decode('utf-8')
    print(f"[{CRITICAL_QUEUE}] Da nhan: {critical_text}")

def start_critical_listener():
    conn_params = pika.ConnectionParameters(host=AMQP_HOST, port=AMQP_PORT)
    conn = pika.BlockingConnection(conn_params)
    channel = conn.channel()

    # Khai báo exchange direct và queue
    channel.exchange_declare(exchange=ALERT_EXCHANGE, exchange_type='direct')
    channel.queue_declare(queue=CRITICAL_QUEUE, durable=True)

    # Ràng buộc queue với exchange theo routing key 'critical'
    channel.queue_bind(exchange=ALERT_EXCHANGE, queue=CRITICAL_QUEUE, routing_key=BINDING_KEY)

    channel.basic_consume(
        queue=CRITICAL_QUEUE,
        on_message_callback=on_critical_received,
        auto_ack=True
    )

    print(' [*] Cho canh bao muc CRITICAL...')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[*] Da dung critical consumer.")
    finally:
        conn.close()

if __name__ == '__main__':
    start_critical_listener()