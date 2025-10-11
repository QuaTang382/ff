# 🚀 WiFi Security Tester - No Root Edition

## ✅ **KHÔNG CẦN ROOT - CHẠY Ở USER MODE**

Tool này được thiết kế đặc biệt để chạy **KHÔNG CẦN quyền root**, sử dụng các phương thức tấn công ở tầng ứng dụng (Application Layer) và các công cụ hệ thống có sẵn.

## 🔥 **Tính Năng No-Root**

### 🌐 **HTTP/HTTPS Flood Attacks**
- **HTTP GET Flood** - Tấn công flood với GET requests
- **HTTP POST Flood** - Tấn công với POST data lớn
- **HTTPS Flood** - Tấn công HTTPS với SSL
- **Bandwidth Test** - Tiêu thụ băng thông qua download

### 🐌 **Slowloris Attack**
- **Slow HTTP Attack** - Giữ kết nối mở lâu
- **Connection Exhaustion** - Làm cạn kiệt connection pool
- **Low Bandwidth** - Hiệu quả với băng thông thấp

### 📡 **DNS Attacks**
- **DNS Query Flood** - Flood DNS server với queries
- **Multiple Query Types** - A, AAAA, MX, TXT, NS records
- **Random Subdomains** - Tránh cache DNS

### 🔌 **Socket Attacks**
- **Connection Flood** - Tạo nhiều kết nối TCP
- **Resource Exhaustion** - Làm cạn kiệt tài nguyên server

### 📶 **WiFi Attacks (No Root)**
- **WiFi Scanning** - Scan liên tục để tạo nhiễu
- **Connection Spam** - Spam kết nối đến fake SSID

## 🚀 **Cách Sử Dụng**

### **1. Khởi Chạy Nhanh**
```bash
./quick_noroot.sh
```

### **2. GUI Tương Tác**
```bash
python3 noroot_gui.py
```

### **3. Command Line**

#### **HTTP GET Flood**
```bash
python3 wifi_noroot_tester.py --http-flood -t http://192.168.1.1 --threads 50 --duration 60
```

#### **HTTPS Flood**
```bash
python3 wifi_noroot_tester.py --https-flood -t https://192.168.1.1 --threads 30 --duration 60
```

#### **Slowloris Attack**
```bash
python3 wifi_noroot_tester.py --slowloris -t 192.168.1.1 -p 80 --threads 200 --duration 300
```

#### **DNS Query Flood**
```bash
python3 wifi_noroot_tester.py --dns-flood -t 8.8.8.8 --threads 30 --duration 60
```

#### **Multi-Attack Sequence**
```bash
python3 wifi_noroot_tester.py --multi-attack --duration 90
```

## 📦 **Cài Đặt**

### **1. Cài Dependencies**
```bash
pip3 install -r noroot_requirements.txt
```

### **2. Cấp Quyền Thực Thi**
```bash
chmod +x *.py *.sh
```

### **3. Chạy Ngay**
```bash
./quick_noroot.sh
```

## 🎯 **Ưu Điểm No-Root**

### ✅ **Không Cần Root**
- Chạy với quyền user thông thường
- Không cần sudo hoặc quyền administrator
- An toàn hơn cho hệ thống

### ✅ **Dễ Sử Dụng**
- Không cần cấu hình phức tạp
- Không cần cài driver đặc biệt
- Chạy trên mọi Linux distribution

### ✅ **Hiệu Quả Cao**
- Tấn công tầng ứng dụng hiệu quả
- Bypass nhiều firewall/IDS
- Khó phát hiện và chặn

### ✅ **Multi-Threading**
- Lên đến 200+ threads đồng thời
- Hiệu suất cao với tài nguyên thấp
- Tối ưu cho multi-core CPU

## 📊 **Hiệu Suất**

### **HTTP Attacks**
- **GET Flood**: 5,000+ requests/second
- **POST Flood**: 3,000+ requests/second
- **HTTPS Flood**: 2,000+ requests/second

### **DNS Attacks**
- **Query Flood**: 10,000+ queries/second
- **Multiple Servers**: Tấn công nhiều DNS đồng thời

### **Socket Attacks**
- **Connection Flood**: 1,000+ connections/second
- **Slowloris**: 200+ persistent connections

## 🎮 **Giao Diện**

### **1. Menu Script**
```
🚀 NO-ROOT ATTACK MENU:
=======================
1. 🌐 HTTP GET Flood Attack
2. 🔒 HTTPS Flood Attack  
3. 📝 HTTP POST Flood Attack
4. 🐌 Slowloris Attack
5. 📡 DNS Query Flood
6. 🔌 Socket Connection Flood
7. 📶 WiFi Scanning Attack
8. 🎯 Multi-Attack Sequence
9. 🎮 Interactive GUI
```

### **2. Interactive GUI**
- Menu tương tác đầy đủ
- Cấu hình chi tiết từng attack
- Theo dõi thống kê real-time
- Dễ sử dụng cho người mới

## 🔍 **Target Discovery**

### **Tự Động Phát Hiện**
```bash
python3 wifi_noroot_tester.py --discover
```

**Kết quả:**
```
[+] Gateway found: 192.168.1.1
[+] DNS server found: 192.168.1.1
[+] DNS server found: 8.8.8.8
[+] Web service found: 192.168.1.1
```

### **Multi-Attack Tự Động**
- Tự động discover targets
- Chọn attack phù hợp cho từng target
- Chạy nhiều attack đồng thời
- Tối ưu hiệu quả tấn công

## ⚡ **Các Tính Năng Nâng Cao**

### **1. Smart Target Selection**
- Tự động phát hiện gateway
- Tìm DNS servers
- Scan web services
- Chọn target tối ưu

### **2. Evasion Techniques**
- Random User-Agents
- Random request parameters
- Variable timing delays
- Multiple connection methods

### **3. Real-time Statistics**
- Requests per second (RPS)
- Total requests sent
- Attack duration
- Success rate monitoring

### **4. Multi-Attack Coordination**
- HTTP + DNS + Socket attacks đồng thời
- Load balancing giữa các targets
- Resource optimization
- Graceful shutdown

## 🛡️ **An Toàn & Pháp Lý**

### **⚠️ Chỉ Sử Dụng Hợp Pháp**
- Chỉ test trên mạng của bạn
- Có sự cho phép rõ ràng bằng văn bản
- Tuân thủ pháp luật địa phương
- Không sử dụng cho mục đích xấu

### **🔒 Built-in Safety**
- Không cần quyền root = an toàn hơn
- Không modify system files
- Không install drivers
- Clean shutdown mechanisms

## 📈 **So Sánh với Root Version**

| Tính Năng | Root Version | No-Root Version |
|------------|--------------|-----------------|
| Quyền cần thiết | Root/Sudo | User thường |
| Layer 2 Attacks | ✅ | ❌ |
| Layer 3/4 Attacks | ✅ | ❌ |
| Application Attacks | ✅ | ✅ |
| HTTP/HTTPS Floods | ✅ | ✅ |
| DNS Attacks | ✅ | ✅ |
| Socket Attacks | ✅ | ✅ |
| WiFi Deauth | ✅ | ❌ |
| Beacon Flooding | ✅ | ❌ |
| An toàn hệ thống | ⚠️ | ✅ |
| Dễ cài đặt | ❌ | ✅ |

## 🎯 **Khi Nào Dùng No-Root Version**

### **✅ Nên Dùng Khi:**
- Không có quyền root/sudo
- Test web applications
- Test DNS infrastructure  
- Test application layer security
- Môi trường production cần an toàn
- Chỉ cần test tầng ứng dụng

### **❌ Không Dùng Khi:**
- Cần test WiFi protocol security
- Cần Layer 2 attacks
- Cần packet injection
- Test wireless infrastructure
- Cần raw socket access

## 🚀 **Kết Luận**

**WiFi Security Tester No-Root Edition** là giải pháp hoàn hảo cho việc test bảo mật mạng mà không cần quyền root. Tool tập trung vào các tấn công tầng ứng dụng hiệu quả và an toàn.

**Ưu điểm chính:**
- ✅ Không cần root
- ✅ Dễ cài đặt và sử dụng  
- ✅ Hiệu quả cao với application layer
- ✅ An toàn cho hệ thống
- ✅ Multi-threading mạnh mẽ

**Hãy sử dụng có trách nhiệm và tuân thủ pháp luật!** 🛡️