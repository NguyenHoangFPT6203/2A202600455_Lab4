from langchain_core.tools import tool

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "Vietjet Air",      "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "11:00", "arrival": "12:20", "price": 1200000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietjet Air",      "departure": "06:40", "arrival": "08:40", "price": 1100000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:00", "price": 2000000, "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "13:00", "arrival": "15:00", "price": 1700000, "class": "economy"},
        {"airline": "Vietravel Airlines", "departure": "16:20", "arrival": "18:20", "price": 1450000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:30", "arrival": "08:30", "price": 1300000, "class": "economy"},
        {"airline": "Vietjet Air",      "departure": "09:00", "arrival": "11:00", "price": 900000,  "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "12:00", "arrival": "14:00", "price": 1100000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "15:00", "arrival": "17:00", "price": 2500000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "08:20", "price": 1400000, "class": "economy"},
        {"airline": "Vietjet Air",      "departure": "10:00", "arrival": "11:20", "price": 850000,  "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "10:00", "price": 1900000, "class": "economy"},
        {"airline": "Vietjet Air",      "departure": "11:00", "arrival": "13:00", "price": 1400000, "class": "economy"},
    ]
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "InterContinental Danang Sun Peninsula Resort", "stars": 5, "price_per_night": 5000000, "area": "Mỹ Khê",  "rating": 5},
        {"name": "Furama Resort Danang", "stars": 4, "price_per_night": 3000000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Novotel Danang Premier Han River", "stars": 4, "price_per_night": 1500000, "area": "Sơn Trà", "rating": 4},
        {"name": "Sanouva Danang Hotel", "stars": 3, "price_per_night": 800000, "area": "Hải Châu", "rating": 3.5},
        {"name": "A La Carte Danang Beach Hotel", "stars": 4, "price_per_night": 1000000, "area": "An Thượng", "rating": 4},
    ],
    "Phú Quốc": [
        {"name": "JW Marriott Phu Quoc Emerald Bay Resort & Spa", "stars": 5, "price_per_night": 4500000, "area": "Bãi Dài", "rating": 5},
        {"name": "Vinpearl Resort Phu Quoc", "stars": 4, "price_per_night": 3500000, "area": "Bãi Trường", "rating": 4.5},
        {"name": "Salinda Resort Phu Quoc Island", "stars": 4, "price_per_night": 2000000, "area": "Dương Đông", "rating": 4},
        {"name": "La Veranda Resort Phu Quoc - MGallery", "stars": 3, "price_per_night": 1200000, "area": "Dương Đông", "rating": 3.5},
    ],
    "Hồ Chí Minh": [
        {"name": "The Reverie Saigon", "stars": 5, "price_per_night": 4000000, "area": "District 1", "rating": 5},
        {"name": "Park Hyatt Saigon", "stars": 4, "price_per_night": 2500000, "area": "District 1", "rating": 4.5},
        {"name": "Hotel Nikko Saigon", "stars": 4, "price_per_night": 1500000, "area": "District 3", "rating": 4},
        {"name": "Liberty Central Saigon Citypoint Hotel", "stars": 3, "price_per_night": 900000, "area": "District 2", "rating": 3.5},
    ]
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm các chuyến bay từ origin đến destination.
    Tham số:
    - origin: Nơi khởi hành (ví dụ: "Hà Nội")
    - destination: Nơi đến (ví dụ: "Hồ Chí Minh")
    Trả về: Danh sách các chuyến bay với hãng , giờ bay, giá vé.
    Nếu không tìm thấy chuyến bay, trả về thông báo không có chuyến.
    """

    origin = origin.strip()
    destination = destination.strip()

    flights = FLIGHTS_DB.get((origin, destination))

    # Nếu không có, thử tra ngược lại
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."
        
    flights.sort(key=lambda x: x["price"])
    
    # # Format kết quả
    # result = []
    # for f in flights:
    #     price_formatted = f"{f['price']:,}".replace(",", ".") + "đ"
        
    #     result.append(
    #         f"{f['airline']} ({f['class']})\n"
    #         f"- Giờ bay: {f['departure']} - {f['arrival']}\n"
    #         f"- Giá: {price_formatted}\n"
    #     )
    
    # return "\n".join(result)
    return flights


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn

    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    city = city.strip()

    hotels = HOTELS_DB.get(city)

    if not hotels:
        return f"Không tìm thấy khách sạn tại {city}."
    
    # Lọc theo giá
    filtered_hotels = [
        h for h in hotels 
        if h["price_per_night"] <= max_price_per_night
        ]
    
    if not filtered_hotels:
        return []
    
    # Sắp xếp theo giá rating giảm dần
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)

    # # Format output
    # result = []
    # for h in filtered_hotels:
    #     price_formatted = f"{h['price_per_night']:,}".replace(",", ".") + "đ"
    #     result.append(
    #         f"{h['name']} ({h['stars']} sao)\n"
    #         f"- Khu vực: {h['area']}\n"
    #         f"- Giá: {price_formatted}VND/đêm\n"
    #         f"- Rating: {h['rating']}\n"
    #     )

    # return "\n".join(result)
    return filtered_hotels

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ đi các khoản chi phí .
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả các khoản chi phí, mỗi khoản cách nhau bởi dấu phẩu,
      định dạng  'tên_khoản:số_tiền' (Ví dụ: 'vé_máy bay:890000,khách_sạn:650000')
      Trả về bảng chi tiết các khoản chi và số tiền còn lại.
      Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        # Parse chuỗi expenses thành dict
        expense_items = {}
        items = [item.strip() for item in expenses.split(",") if item.strip()]

        for item in items:
            if ":" not in item:
                return "Lỗi định dạng expenses. Vui lòng dùng format 'tên_khoản: số_tiền'."

            name, value = item.split(":", 1)
            name = name.strip()
            value = value.strip()

            if not value.isdigit():
                return f"Số tiền không hợp lệ cho khoản '{name}'."

            expense_items[name] = int(value)

        # Tính tổng chi
        total_expense = sum(expense_items.values())

        # Tính còn lại
        remaining = total_budget - total_expense

        # Format tiền kiểu Việt Nam
        def format_vnd(amount: int) -> str:
            return f"{amount:,}".replace(",", ".") + "đ"

        # Tạo bảng chi tiết
        result_lines = ["Bảng chi phí:"]

        for name, value in expense_items.items():
            result_lines.append(f"- {name}: {format_vnd(value)}")

        # result_lines.append("")
        # result_lines.append(f"Tổng chi: {format_vnd(total_expense)}")
        # result_lines.append(f"Ngân sách: {format_vnd(total_budget)}")
        # result_lines.append(f"Còn lại: {format_vnd(remaining)}")

        # Nếu vượt ngân sách
        if remaining < 0:
            result_lines.append(
                f"\nVượt ngân sách {format_vnd(abs(remaining))}! Cần điều chỉnh chi phí."
            )

        # return "\n".join(result_lines)
    
        return {
            "expenses": expense_items,
            "total_expense": total_expense,
            "remaining": remaining
        }

    except Exception:
        return "Có lỗi xảy ra khi tính toán ngân sách. Vui lòng kiểm tra lại dữ liệu đầu vào."
    

# if __name__ == "__main__":
#     print(calculate_budget(5000000, "vé máy bay:890000, khách sạn:650000, ăn uống:1200000"))