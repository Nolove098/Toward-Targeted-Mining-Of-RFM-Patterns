# Toward Targeted Mining Of RFM Patterns (TaRFM) - Python Implementation

Đây là bản triển khai bằng ngôn ngữ Python cho thuật toán **TaRFM**, dựa trên bài báo nghiên cứu *"Toward Targeted Mining of RFM Patterns"* (IEEE TNNLS 2025). Thuật toán này giúp khai thác có định hướng các mẫu RFM (Recency, Frequency, Monetary) trong cơ sở dữ liệu giao dịch.

## Yêu cầu hệ thống
- **Python 3.8+** (không yêu cầu cài đặt thư viện bên ngoài).
- `git` để sao chép mã nguồn (nếu cần).

## Cấu trúc mã nguồn

```
tarfm_python/
├── src/
│   ├── model/           # Cấu trúc dữ liệu: Transaction, RFMTriple, RFMListNode, TaRFMPattern
│   ├── order/           # Tính toán TWU và TaRFM Order
│   ├── core/            # Thuật toán chính: TaRFM, GetRFMList, GetTaRFMPatterns
│   ├── io/              # Đọc cơ sở dữ liệu giao dịch và tiện ích (Utility)
│   └── main.py          # Entry point của ứng dụng
├── data/
│   └── sample/          # Dữ liệu thử nghiệm (transactions, utility, foodmartFIM)
└── tests/
    └── test_phases.py   # Kịch bản kiểm thử (Unittest)
```

## Cách chạy chương trình

Đầu tiên, bạn cần di chuyển thư mục hiện tại (CWD) vào đúng thư mục mã nguồn:

```bash
cd tarfm_python
```

Sau đó, bạn có thể chạy dự án trực tiếp thông qua tệp `src/main.py`. Mặc định, chương trình được cấu hình để chạy trực tiếp trên bộ dữ liệu `foodmartFIM`.

Mở terminal và gõ lệnh:
```bash
python src/main.py
```

### Chạy với cấu hình tùy chỉnh
Bạn có thể thay đổi các tham số thuật toán thông qua đối số dòng lệnh:

```bash
python src/main.py --tx "đường/dẫn/đến/transactions.txt" \
                   --util "đường/dẫn/đến/external_utility.txt" \
                   --qi "A,B" \
                   --delta 0.01 \
                   --gamma 1.5 \
                   --alpha 0.2 \
                   --beta 80.0
```

**Các tham số:**
- `--tx`: Đường dẫn tới tệp dữ liệu giao dịch (hỗ trợ cả định dạng `item:qty` và định dạng FIM truyền thống chỉ có `item`).
- `--util`: Đường dẫn tới tệp bảng giá/tiện ích mở rộng (External Utility). Nếu mặt hàng không có trong file, giá trị tiện ích mặc định là `1.0`.
- `--qi`: Tập hợp các mặt hàng bạn quan tâm (Query Items), viết liền cách nhau bởi dấu phẩy.
- `--delta` (δ): Tốc độ suy giảm độ mới (Decay rate).
- `--gamma` (γ): Ngưỡng độ mới tối thiểu (Min recency).
- `--alpha` (α): Tỷ lệ tần suất tối thiểu (Min frequency ratio).
- `--beta` (β): Ngưỡng tiền tệ/tiện ích tối thiểu (Min monetary).

### Chạy Unittest

Để kiểm tra độ chính xác của các thuật toán so với bài báo gốc (Sử dụng dữ liệu mẫu nhỏ `data/sample/transactions.txt`), bạn hãy chắc chắn đang đứng ở thư mục `tarfm_python` và chạy bộ kiểm thử:

```bash
python -m unittest discover -s tests
```
*(Nếu bạn đang ở bên ngoài thư mục `tarfm_python`, hãy gọi `cd tarfm_python` trước khi chạy).*
Nếu mọi thứ chính xác, kết quả sẽ in ra `OK`.