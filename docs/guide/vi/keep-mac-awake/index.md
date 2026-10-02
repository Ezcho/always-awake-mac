Source: https://no-sleep-pika.online/guide/vi/keep-mac-awake/
Language: vi

MAC GUIDE · 2026-10-02

# Cách giữ Mac không ngủ: clamshell, caffeinate và pika

So sánh nguồn điện và chế độ gập máy, lệnh Terminal và pika. Tìm hiểu điều kiện, giới hạn, khóa màn hình và cách kết thúc phiên.

## Chọn theo công việc

Tắt màn hình, khóa màn hình và ngủ hệ thống khác nhau. Mac bị khóa vẫn có thể làm việc. Với màn hình ngoài hãy kiểm tra clamshell; với việc tạm thời khi mở nắp dùng caffeinate; với việc gập máy không có màn hình ngoài có thể dùng pika và dịch vụ trợ giúp.

## 1. Nguồn điện và chế độ clamshell

Khi mở nắp, kết nối nguồn, màn hình hỗ trợ, bàn phím và chuột; kiểm tra rồi mới gập. Màn hình cấp nguồn có thể thay sạc theo thông số. Chỉ cắm sạc chưa đủ. Số màn hình và độ phân giải tùy model Mac. Chấp thuận phụ kiện trước khi gập nắp.

[Apple · External displays](https://support.apple.com/en-us/102501)

## Cài đặt khi mở nắp

Trên laptop cắm nguồn, tìm tùy chọn ngăn tự động ngủ khi màn hình tắt trong Cài đặt hệ thống → Pin → Tùy chọn. Tên và vị trí tùy phiên bản và model. Có thể giữ mật khẩu khóa. Đây không phải cách đảm bảo chặn mọi giấc ngủ do gập nắp. Ghi lại cài đặt cũ.

[Apple · Sleep and wake settings](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

## 2. Dùng caffeinate tạm thời

Mở Terminal và chạy lệnh dưới. caffeinate có sẵn trong macOS, không cần sudo. Nó ngăn ngủ do không hoạt động, màn hình vẫn có thể tắt. Giữ tiến trình chạy và nhấn Control+C trong cùng Terminal để dừng. Không có thông báo là bình thường; yêu cầu kết thúc khi tiến trình thoát.

```
caffeinate -i
```

## Thời gian, màn hình và lệnh

Ví dụ đầu kéo dài 3.600 giây, một giờ. Ví dụ thứ hai giữ cả màn hình trong 1.800 giây, nửa giờ; bỏ -d nếu không cần. Ví dụ cuối thực sự chạy make đến khi hoàn tất: chỉ dùng trong dự án định biên dịch. Trình khởi chạy thoát ngay có thể kết thúc trước công việc nền thật. Khi chạy một lệnh, -t không được sử dụng.

```
caffeinate -i -t 3600
```

```
caffeinate -di -t 1800
```

```
caffeinate -i make
```

## Khi gập nắp thì sao?

-i dành cho ngủ hệ thống do nhàn rỗi, -d dành cho màn hình. Gập nắp là điều kiện khác, không bảo đảm chạy khi không có màn hình ngoài. -s chỉ có hiệu lực với nguồn AC; -u báo hoạt động người dùng và có thể bật màn hình. Chọn tùy chọn theo chức năng được mô tả.

## 3. Cài đặt pika

pika hỗ trợ macOS 13 trở lên, Apple Silicon và Intel. PKG chính thức đầy đủ cài ứng dụng và dịch vụ trợ giúp quản trị. Tự hoàn tất xác thực và phê duyệt macOS. Mở /Applications/pika.app, kiểm tra kết nối dịch vụ, bật Session, chọn Monitor OFF nếu cần rồi gập nắp. Ngăn ngủ được chuẩn bị trước, chính sách màn hình áp dụng sau khi gập. Khi mở nắp, Monitor chỉ lưu lựa chọn. Session OFF khôi phục cài đặt đã quản lý mà không tắt màn hình ngay. Đóng cửa sổ không thoát ứng dụng.

[Tải pika · 1.0.13](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)

[Trợ giúp cài đặt](https://no-sleep-pika.online/install/)

## Kiểm tra rồi kết thúc

Thử việc ngắn, ghi giờ rồi kiểm tra nhật ký và tiến độ sau đó. Đây là quy trình đề xuất, không phải tuyên bố đã thử mọi model. pmset -g assertions chỉ đọc yêu cầu hiện tại, không chứng minh mạng hoặc hoạt động khi gập liên tục. man caffeinate hiển thị hướng dẫn trên máy.

```
pmset -g assertions
```

```
man caffeinate
```

## Khóa, mạng và nhiệt

Khóa không nhất thiết là ngủ. Wi-Fi, VPN, giới hạn API, chờ phê duyệt hay lỗi ứng dụng vẫn có thể ngắt việc. pika không tiếp tục hội thoại AI hoặc sửa mạng. Đặt Mac đang chạy trên mặt cứng thoáng khí, không trong túi. Bảo vệ pin, nhiệt hoặc lỗi dịch vụ có thể kết thúc phiên; không bảo đảm ngăn mọi quá nhiệt hay cạn pin.

## Nguồn và phạm vi

Bài so sánh do nhà phát triển no-sleep-pika viết, gồm ứng dụng của chính mình. Dựa trên Apple, hướng dẫn macOS caffeinate(8), tài liệu và mã pika 1.0.13. Không phải sự bảo chứng của Apple hay nhà cung cấp AI. Chỉ duy trì phiên trong thời gian cần thiết.

- [Apple: If your external display is dark or low resolution](https://support.apple.com/en-us/102501)

- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

- [Apple: Allow USB and other accessories](https://support.apple.com/en-us/102282)

- `man caffeinate` · macOS System Manager’s Manual

Do nhà phát triển no-sleep-pika viết, có giới thiệu ứng dụng của mình.

[Tải pika](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)[Hướng dẫn gập MacBook →](https://no-sleep-pika.online/guide/vi/macbook-lid-closed/)[Markdown](https://no-sleep-pika.online/guide/vi/keep-mac-awake/index.md)
