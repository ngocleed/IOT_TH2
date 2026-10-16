import pika

# Cấu hình kết nối và exchange
AMQP_HOST = 'localhost'
AMQP_PORT = 5672
ALERT_EXCHANGE = 'iot_alert_exchange'
EXCHANGE_TYPE = 'direct'

def dispatch_system_alerts():
    parameters = pika.ConnectionParameters(host=AMQP_HOST, port=AMQP_PORT)
    conn = pika.BlockingConnection(parameters)
    mq_channel = conn.channel()

    try:
        # Khai báo exchange kiểu direct
        mq_channel.exchange_declare(exchange=ALERT_EXCHANGE, exchange_type=EXCHANGE_TYPE)

        # Danh sách các thông điệp cảnh báo theo các cấp độ
        alert_events = [
            ("info", "He thong giam sat hoat dong on dinh"),
            ("warning", "Nhiet do phong may chu vuot nguong warning"),
            ("critical", "Cam bien tram do bi mat ket noi critical")
        ]

        for severity, message_body in alert_events:
            mq_channel.basic_publish(
                exchange=ALERT_EXCHANGE,
                routing_key=severity,
                body=message_body.encode('utf-8')
            )
            print(f" [x] Da gui muc '{severity}': {message_body}")
    finally:
        conn.close()

if __name__ == '__main__':
    dispatch_system_alerts()