# Bài tập RabbitMQ và IoT

## Giới thiệu

**Sinh viên:** Lê Tuấn Minh
**Mã sinh viên:** B23DCCN551 

**Sinh viên:** Lê Duy Ngọc
**Mã sinh viên:** B23DCCN603

**Sinh viên:** Phạm Tuấn Đạt
**Mã sinh viên:** B23DCCN145

Repository gồm 7 chương trình Python minh họa giao tiếp producer/consumer với RabbitMQ:

- Bài 1: gửi và nhận chuỗi văn bản qua queue `iot_lab_queue`.
- Bài 2: producer gửi nhiệt độ và độ ẩm dạng JSON; monitor đọc và cảnh báo theo ngưỡng.
- Bài 3: producer phát cảnh báo qua direct exchange; hai consumer nhận riêng mức `warning` và `critical`.

## Danh sách chương trình

- `producer_bai1.py` và `consumer_bai1.py`: producer và consumer cho Bài 1.
- `sensor_producer_bai2.py` và `monitor_consumer_bai2.py`: producer và monitor cho Bài 2.
- `alert_producer_bai3.py`, `warning_consumer_bai3.py`, `critical_consumer_bai3.py`: producer và hai consumer cho Bài 3.

## Thiết lập môi trường

### Broker sử dụng

Các chương trình sử dụng **RabbitMQ**, một message broker nội bộ giao tiếp bằng giao thức AMQP. Thư viện Python `pika` mở kết nối tới `localhost` với cấu hình cổng AMQP `5672`, tài khoản mặc định `guest`/`guest`. Các script được thiết lập rõ hằng số cấu hình host `localhost` và port `5672` trong `pika.ConnectionParameters`.

### Cài RabbitMQ trên Windows bằng trình duyệt

1. Mở [hướng dẫn cài RabbitMQ trên Windows](https://www.rabbitmq.com/docs/install-windows) bằng trình duyệt, tìm mục **Using the Installer**.
2. Xem [bảng tương thích Erlang/RabbitMQ](https://www.rabbitmq.com/docs/which-erlang), sau đó vào [trang tải Erlang/OTP](https://www.erlang.org/downloads) để tải bộ cài **Windows 64-bit** phù hợp. Cài Erlang trước bằng **Run as administrator**.
3. Quay lại trang RabbitMQ, tải file `rabbitmq-server-{version}.exe` trong mục **Direct Downloads**. Chạy bộ cài bằng **Run as administrator** và hoàn tất các bước. RabbitMQ được cài thành dịch vụ Windows và tự khởi động với cấu hình mặc định.
4. Nhấn `Win + R`, nhập `services.msc`, tìm dịch vụ **RabbitMQ** và kiểm tra trạng thái **Running**. Nếu chưa chạy, bấm **Start**.

### Bật và kiểm tra giao diện quản trị

Trong Start Menu, mở **RabbitMQ Command Prompt (sbin dir)** bằng **Run as administrator**, rồi chạy:

```cmd
rabbitmq-plugins.bat enable rabbitmq_management
rabbitmqctl.bat status
```

Mở http://localhost:15672 bằng trình duyệt và đăng nhập với tên đăng nhập `guest`, mật khẩu `guest`. Giao diện này dùng cổng `15672`; các script Python kết nối AMQP qua cổng `5672`.

Tài khoản `guest` mặc định chỉ cho phép kết nối từ máy cục bộ, phù hợp với `localhost` trong cả 7 script. Plugin quản trị chỉ phục vụ giao diện quản trị, không bắt buộc để chạy các script. Cấu hình này dành cho bài tập cục bộ; không mở các cổng này ra mạng công cộng.

### Chuẩn bị Python

Mở PowerShell tại thư mục repository và cài thư viện:

```powershell
py -m pip install pika
```

Mỗi terminal cần chạy script phải dùng cùng môi trường Python đã cài `pika`. Nếu máy không có lệnh `py`, thay bằng `python`.

## Cách chạy

Consumer thường chạy liên tục, vì vậy mở các terminal riêng. Hãy khởi động consumer trước producer để nhìn thấy message ngay khi gửi. Dừng consumer bằng `Ctrl+C`.

### Bài 1: Queue cơ bản

Terminal 1:

```powershell
python consumer_bai1.py
```

Terminal 2:

```powershell
python producer_bai1.py
```

Producer gửi một message đến queue `iot_lab_queue`, sau đó kết thúc. Consumer in nội dung và thời điểm nhận, ví dụ:

```text
 [x] Da gui: 'Xin chao tu ung dung Python AMQP - Le Tuan Minh - B23DCCN551'
Da nhan message: Xin chao tu ung dung Python AMQP - Le Tuan Minh - B23DCCN551
Thoi gian nhan: 20:55:08
```

Thời gian hiển thị phụ thuộc lúc chạy. Chuỗi có dấu trong terminal có thể hiển thị khác tùy bảng mã. Các khối kết quả minh họa giữ nguyên chữ có dấu hoặc không dấu theo nội dung mà code hiện tại in ra.

### Bài 2: Dữ liệu cảm biến JSON

Terminal 1:

```powershell
python monitor_consumer_bai2.py
```

Terminal 2:

```powershell
python sensor_producer_bai2.py
```

Producer gửi dữ liệu `sensor01` mỗi 3 giây và chạy cho đến khi nhấn `Ctrl+C`. Monitor in nhiệt độ, độ ẩm; nhiệt độ trên `35` thì in cảnh báo nhiệt độ cao, độ ẩm dưới `40` thì in cảnh báo độ ẩm thấp. Giá trị thay đổi ngẫu nhiên trong mỗi lần gửi, ví dụ:

```text
 [x] Sent data: {'device_id': 'sensor01', 'temperature': 37.2, 'humidity': 35.4}
Device: sensor01
Temperature: 37.2
Humidity: 35.4
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
```

### Bài 3: Cảnh báo qua direct exchange

Mở ba terminal. Chạy hai consumer trước:

```powershell
python warning_consumer_bai3.py
```

```powershell
python critical_consumer_bai3.py
```

Sau đó chạy producer trong terminal thứ ba:

```powershell
python alert_producer_bai3.py
```

Producer khai báo exchange `iot_alert_exchange` loại `direct`, rồi gửi ba message với routing key `info`, `warning`, `critical`. Queue `warning_queue` chỉ bind key `warning`, còn `critical_queue` chỉ bind key `critical`. Kết quả:

```text
Producer:
 [x] Da gui muc 'info': He thong giam sat hoat dong on dinh
 [x] Da gui muc 'warning': Nhiet do phong may chu vuot nguong warning
 [x] Da gui muc 'critical': Cam bien tram do bi mat ket noi critical

warning consumer:
[warning_queue] Da nhan: Nhiet do phong may chu vuot nguong warning

critical consumer:
[critical_queue] Da nhan: Cam bien tram do bi mat ket noi critical
```

Không có queue nào bind routing key `info`, nên message `info` không được đưa vào queue và sẽ bị bỏ qua. Thứ tự kết quả trên các terminal consumer có thể khác nhau.

## Lưu ý

Các queue trong các script được khai báo `durable=True`, nhưng các message hiện tại không được publish với chế độ persistent. Exchange của Bài 3 cũng không khai báo durable. Vì vậy, không nên xem các message này là được đảm bảo tồn tại qua lần khởi động lại broker.
