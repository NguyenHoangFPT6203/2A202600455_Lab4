# Lab 4 Test Results - TravelBuddy

Ket qua ghi tu `python run_lab4_tests.py` (Part 4 - kiem thu).

## Test 1 - Direct Answer (No Tool)
- **Input**: "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."
- **Expected**: Agent chao hoi, gioi thieu kha nang, khong goi tool.
- **Tools invoked**: `[]`
- **Actual (TravelBuddy)**: Chào bạn! Rất vui được hỗ trợ bạn trong việc lên kế hoạch du lịch. Bạn có ý tưởng nào về điểm đến, hoặc bạn muốn khám phá những nơi nào ở Việt Nam? Ngoài ra, cho mình biết thêm về thời gian đi và ngân sách của bạn nếu có, để mình có thể tư vấn cụ thể hơn nhé!
- **Pass/Fail**: Pass

## Test 2 - Single Tool Call
- **Input**: "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"
- **Expected**: Agent goi `search_flights` va tra danh sach chuyen bay.
- **Tools invoked**: `['search_flights']`
- **Actual (TravelBuddy)**: Dưới đây là thông tin chuyến bay từ Hà Nội đi Đà Nẵng:

1. **Hãng hàng không**: Vietjet Air
   - **Giờ khởi hành**: 08:30
   - **Giờ đến**: 09:50
   - **Giá vé**: 890.000 VND (hạng phổ thông)

2. **Hãng hàng không**: Bamboo Airways
   - **Giờ khởi hành**: 11:00
   - **Giờ đến**: 12:20
   - **Giá vé**: 1.200.000 VND (hạng phổ thông)

3. **Hãng hàng không**: Vietnam Airlines
   - **Giờ khởi hành**: 06:00
   - **Giờ đến**: 07:20
   - **Giá vé**: 1.450.000 VND (hạng phổ thông)

4. **Hãng hàng không**: Vietnam Airlines
   - **Giờ khởi hành**: 14:00
   - **Giờ đến**: 15:20
   - **Giá vé**: 2.800.000 VND (hạng thương gia)

Bạn có muốn đặt vé hay cần thêm thông tin gì không?
- **Pass/Fail**: Pass

## Test 3 - Multi-Step Tool Chaining
- **Input**: "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"
- **Expected**: Lien tiep `search_flights` -> `search_hotels` -> `calculate_budget`, sau do tong hop.
- **Tools invoked**: `['search_flights', 'search_hotels', 'calculate_budget']`
- **Actual (TravelBuddy)**: Dưới đây là thông tin chuyến đi của bạn từ Hà Nội đến Phú Quốc trong 2 đêm:

### Chuyến bay:
1. **Vietjet Air**: 
   - Giờ bay: 06:40 - 08:40
   - Giá vé: 1.100.000 VNĐ
   
2. **Vietravel Airlines**:
   - Giờ bay: 16:20 - 18:20
   - Giá vé: 1.450.000 VNĐ
   
3. **Bamboo Airways**:
   - Giờ bay: 13:00 - 15:00
   - Giá vé: 1.700.000 VNĐ
   
4. **Vietnam Airlines**: 
   - Giờ bay: 07:00 - 09:00
   - Giá vé: 2.000.000 VNĐ

### Khách sạn:
1. **Salinda Resort Phu Quoc Island** (4 sao)
   - Giá: 2.000.000 VNĐ/đêm (tổng cho 2 đêm: 4.000.000 VNĐ)
   - Khu vực: Dương Đông
   - Đánh giá: 4 sao

2. **La Veranda Resort Phu Quoc - MGallery** (3 sao)
   - Giá: 1.200.000 VNĐ/đêm (tổng cho 2 đêm: 2.400.000 VNĐ)
   - Khu vực: Dương Đông
   - Đánh giá: 3.5 sao

### Tổng chi phí ước tính:
- **Vé máy bay**: 1.100.000 VNĐ
- **Khách sạn (Salinda)**: 4.000.000 VNĐ
- **Tổng**: 5.100.000 VNĐ

### Kết luận:
Với ngân sách 5 triệu, bạn sẽ thiếu khoảng 100.000 VNĐ nếu chọn khách sạn Salinda. Nếu bạn chọn **La Veranda Resort**, tổng chi sẽ là 3.500.000 VNĐ (1.100.000 VNĐ vé máy bay + 2.400.000 VNĐ khách sạn), và bạn sẽ còn lại 1.100.000 VNĐ cho các chi phí khác.

Gợi ý thêm là bạn nên kiểm tra kỹ lại giá của các phòng khách sạn và vé máy bay trước khi đặt để đảm bảo không bị thiếu ngân sách nhé! Nếu cần thêm thông tin khác, cứ hỏi mình nhé!
- **Pass/Fail**: Pass

## Test 4 - Missing Info
- **Input**: "Tôi muốn đặt khách sạn"
- **Expected**: Hoi lai thong tin thieu truoc khi goi tool.
- **Tools invoked**: `[]`
- **Actual (TravelBuddy)**: Bạn có thể cho mình biết thành phố mà bạn muốn đặt khách sạn và ngân sách tối đa mỗi đêm không?
- **Pass/Fail**: Pass

## Test 5 - Guardrail / Refusal
- **Input**: "Giải giúp tôi bài tập lập trình Python về linked list"
- **Expected**: Tu choi lich su, chuyen huong sang du lich.
- **Tools invoked**: `[]`
- **Actual (TravelBuddy)**: Xin lỗi, nhưng mình không thể giúp bạn với yêu cầu lập trình hay bài tập. Tuy nhiên, nếu bạn có câu hỏi nào về du lịch, đặt vé máy bay hoặc phòng khách sạn, mình rất vui lòng hỗ trợ! Bạn có kế hoạch đi đâu không?
- **Pass/Fail**: Pass

## Tong ket
- So test dat: **5/5**
- Log console day du: xem file `test_console_log.txt` (cung thu muc).
