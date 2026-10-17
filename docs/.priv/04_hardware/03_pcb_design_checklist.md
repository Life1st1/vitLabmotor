# PCB Layout Phase Checklist

> **Áp dụng cho:** PCB điều khiển nhúng, servo driver/FOC dùng STM32G4, gate driver, MOSFET 3 pha, CAN/RS485/USB và các mạch nguồn công suất.
>
> **Mục tiêu:** Hoàn tất placement, routing, kiểm tra SI/PI/EMI, DFM/DFA/DFT và bộ dữ liệu sản xuất trước khi release PCB.

---

## 0. Thông tin tài liệu

- [ ] Tên dự án/board: `________________________`
- [ ] Revision schematic: `________________________`
- [ ] Revision PCB: `________________________`
- [ ] Người layout: `________________________`
- [ ] Người review: `________________________`
- [ ] Nhà sản xuất PCB/PCBA dự kiến: `________________________`
- [ ] Số lớp PCB: `________`
- [ ] Độ dày PCB: `________ mm`
- [ ] Copper weight: `Outer: ____ oz / Inner: ____ oz`
- [ ] Điện áp bus lớn nhất: `________ V`
- [ ] Dòng pha liên tục/đỉnh: `________ A / ________ A`
- [ ] Ngày review: `____ / ____ / ______`

### Quy ước trạng thái

- `[ ]` Chưa kiểm tra
- `[x]` Đạt
- `N/A` Không áp dụng, cần ghi lý do
- Mọi mục `Fail` phải có issue ID, người xử lý và kết quả kiểm tra lại.

---

# A. Chuẩn bị trước khi layout

## A1. Đầu vào thiết kế

- [ ] Schematic đã hoàn tất review và đóng các lỗi nghiêm trọng.
- [ ] Netlist PCB đồng bộ hoàn toàn với schematic.
- [ ] Tất cả thay đổi pin-swap/gate-swap trong layout đã được back-annotate về schematic.
- [ ] BOM sơ bộ đã kiểm tra package, MPN, trạng thái linh kiện và khả năng mua hàng.
- [ ] Datasheet, application note và reference design quan trọng đã được lưu theo revision.
- [ ] Xác định rõ điện áp, dòng điện, tần số chuyển mạch và nhiệt độ môi trường thiết kế.
- [ ] Có sơ đồ phân vùng chức năng: power, gate drive, MCU, analog sensing, communication, protection.
- [ ] Có sơ đồ dòng công suất và đường hồi dòng quan trọng.
- [ ] Có danh sách các net critical và constraint tương ứng.
- [ ] Có yêu cầu về EMC/ESD, creepage, clearance và cách điện.
- [ ] Có yêu cầu cơ khí: board outline, lỗ bắt vít, connector, heatsink, enclosure, keepout.
- [ ] Có stack-up được nhà sản xuất xác nhận hoặc có stack-up mục tiêu rõ ràng.

## A2. Thiết lập PCB rules

- [ ] Clearance mặc định phù hợp năng lực tiêu chuẩn của nhà sản xuất.
- [ ] Trace width mặc định phù hợp dòng điện và copper weight.
- [ ] Via drill, via diameter và annular ring nằm trong năng lực sản xuất.
- [ ] Thiết lập net class riêng cho:
  - [ ] DC bus và đường dòng lớn.
  - [ ] Ba pha U/V/W.
  - [ ] Gate drive.
  - [ ] Shunt/Kelvin sensing.
  - [ ] USB differential pair.
  - [ ] CAN/RS485.
  - [ ] Clock/crystal.
  - [ ] ADC và tín hiệu analog nhạy nhiễu.
- [ ] Thiết lập differential pair width/gap theo stack-up thực tế.
- [ ] Thiết lập length/skew constraint cho các cặp vi sai cần thiết.
- [ ] Thiết lập clearance riêng theo điện áp bus và tiêu chuẩn áp dụng.
- [ ] Thiết lập copper-to-board-edge, copper-to-slot và component-to-edge.
- [ ] Thiết lập courtyard/component clearance cho assembly và rework.
- [ ] Thiết lập solder-mask expansion và minimum mask sliver.
- [ ] Thiết lập paste rule riêng cho exposed pad, power pad hoặc thermal pad.

---

# B. Stack-up và phân bổ lớp

- [ ] Thứ tự layer đã được xác định và ghi trong fabrication notes.
- [ ] Mỗi lớp signal tốc độ cao có reference plane liên tục liền kề.
- [ ] Không đặt hai lớp signal quan trọng cạnh nhau nếu không có plane che chắn phù hợp.
- [ ] Ground plane có trở kháng thấp và ít bị chia cắt.
- [ ] Power plane không tạo khe cắt qua đường hồi dòng của tín hiệu.
- [ ] Khoảng cách dielectric và độ dày đồng phù hợp yêu cầu impedance/current.
- [ ] Controlled impedance đã được nhà sản xuất tính hoặc xác nhận.
- [ ] Tính impedance có xét solder mask nếu trace được phủ mask.
- [ ] Stack-up đối xứng để giảm cong vênh PCB.
- [ ] Mật độ đồng giữa các lớp và hai mặt tương đối cân bằng.
- [ ] Có layer marker/coupon nếu nhà sản xuất hoặc quy trình chất lượng yêu cầu.

---

# C. Board outline và cơ khí

- [ ] Board outline là contour kín, không trùng nét và đúng đơn vị.
- [ ] Kích thước tổng thể đúng với bản vẽ cơ khí.
- [ ] Vị trí, đường kính và loại lỗ bắt vít đúng: PTH/NPTH.
- [ ] Có copper keepout quanh lỗ vít, spacer và vùng kim loại của enclosure khi cần.
- [ ] Đã kiểm tra đường kính đầu vít, washer và tool access.
- [ ] Connector nằm đúng mép board, đúng hướng cắm/rút và không bị enclosure cản.
- [ ] USB, CAN, nguồn, pha motor và debug connector không bị đảo chiều hoặc mirror.
- [ ] LED, button, DIP switch và test point có thể tiếp cận sau khi lắp vỏ.
- [ ] Linh kiện cao không va chạm heatsink, nắp, dây hoặc board khác.
- [ ] Có keepout cho antenna nếu dùng RF/Wi-Fi/BLE.
- [ ] Khoảng cách linh kiện tới V-cut, tab-route và tooling hole đủ an toàn.
- [ ] Đã kiểm tra PCB ở chế độ 3D từ cả mặt trên và mặt dưới.
- [ ] Đã xuất/đối chiếu STEP với thiết kế cơ khí.
- [ ] Đã in PCB tỷ lệ 1:1 và thử với connector/linh kiện cơ khí quan trọng nếu có thể.

---

# D. Footprint và thư viện

- [ ] Symbol pin number khớp footprint pad number và datasheet.
- [ ] Package đúng biến thể MPN được chọn trong BOM.
- [ ] Kiểm tra top-view/bottom-view của datasheet, đặc biệt với connector và MOSFET.
- [ ] Pin 1, cực tính diode/LED/tụ và orientation IC rõ ràng.
- [ ] Pad size, hole size và slot phù hợp chân linh kiện thực tế.
- [ ] Pad của connector dòng lớn đủ dòng và đủ độ bền cơ khí.
- [ ] Exposed pad đúng kích thước, có thermal via và paste window phù hợp.
- [ ] Không đặt via hở trong pad nếu quy trình PCBA không hỗ trợ via-in-pad filled/capped.
- [ ] Courtyard không chồng lấn bất hợp lý.
- [ ] Khoảng cách body-to-body đủ cho lắp ráp và rework.
- [ ] Silkscreen không nằm trên pad hoặc vùng solderable.
- [ ] 3D model đúng package, cao độ và orientation.
- [ ] Fiducial local được thêm cho BGA/QFN/fine-pitch khi cần.
- [ ] Linh kiện DNP có footprint và ký hiệu assembly rõ ràng.

---

# E. Placement tổng thể

## E1. Phân vùng và luồng tín hiệu

- [ ] Các khối chức năng được nhóm rõ ràng theo sơ đồ dòng tín hiệu và dòng công suất.
- [ ] Đường đi từ connector vào mạch bảo vệ rồi tới mạch xử lý hợp lý.
- [ ] Khối công suất, switching node và cuộn cảm cách xa MCU/ADC/crystal/communication.
- [ ] Analog sensing cách xa node pha, gate drive và cạnh PCB có nhiễu.
- [ ] Driver gần MOSFET; MCU gần driver nhưng không nằm trong vùng switching nóng/nhiễu.
- [ ] Connector nguồn và motor hỗ trợ đường dòng lớn ngắn, rộng, ít vòng lặp.
- [ ] Linh kiện dễ nóng không tập trung gây điểm nóng cục bộ.
- [ ] Linh kiện nhạy nhiệt cách xa MOSFET, shunt, diode và cuộn cảm.
- [ ] Có không gian cho heatsink, airflow hoặc thermal interface material.
- [ ] Linh kiện cùng chức năng có orientation nhất quán để giảm lỗi lắp ráp.
- [ ] Có đủ không gian probe, debug và rework.

## E2. Decoupling và bulk capacitor

- [ ] Mỗi power pin IC có tụ decoupling theo datasheet.
- [ ] Tụ decoupling đặt sát chân nguồn/GND, loop dòng nhỏ nhất.
- [ ] Đường IC → capacitor → ground/power via ngắn và rộng.
- [ ] Không đặt via hoặc đoạn trace dài giữa chân IC và tụ decoupling nếu tránh được.
- [ ] Tụ bulk đặt gần nơi dòng xung được lấy hoặc gần connector nguồn phù hợp chức năng.
- [ ] Tụ DC-link ceramic đặt sát half-bridge để thu nhỏ commutation loop.
- [ ] MLCC đã xét DC-bias, nhiệt độ, tolerance và điện áp định mức.
- [ ] Không đặt MLCC lớn sát mép board, lỗ vít, V-cut hoặc vùng PCB chịu uốn.
- [ ] Có phương án soft termination/flex termination cho MLCC ở môi trường rung/uốn nếu cần.

---

# F. Layout khối công suất và FOC

## F1. DC bus và đường dòng lớn

- [ ] Đường VIN+/VBUS và PGND ngắn, rộng và đối xứng khi cần.
- [ ] Bề rộng trace/plane đã kiểm tra theo dòng liên tục, dòng đỉnh và nhiệt độ cho phép.
- [ ] Không có neck-down không chủ ý tại pad, via hoặc điểm chuyển lớp.
- [ ] Số lượng và kích thước via đủ cho dòng điện và nhiệt.
- [ ] Via dòng lớn bố trí phân bố đều, không chỉ tập trung một phía của pad.
- [ ] Không để antipad/via khác cắt hẹp power plane.
- [ ] Dòng vào và dòng hồi nằm gần nhau để giảm loop area.
- [ ] Có khoảng cách an toàn giữa VBUS, phase node và low-voltage circuitry.
- [ ] Copper pour không tạo island hoặc nhánh cụt không cần thiết.
- [ ] Đã kiểm tra current path trong từng trạng thái đóng cắt của inverter.

## F2. MOSFET half-bridge

- [ ] Ba half-bridge có layout tương đồng để giảm sai khác ký sinh giữa các pha.
- [ ] High-side và low-side MOSFET đặt gần nhau.
- [ ] DC-link ceramic capacitor đặt trực tiếp gần vòng VBUS → HS FET → LS FET → PGND.
- [ ] Commutation loop nhỏ nhất có thể.
- [ ] Switching node copper chỉ lớn vừa đủ cho dòng/nhiệt, không mở rộng không cần thiết.
- [ ] Switching node tránh chạy dưới MCU, driver, shunt amplifier, crystal và communication.
- [ ] Không đặt ground plane hoặc tín hiệu nhạy ngay dưới switching node nếu gây tăng điện dung ký sinh/nhiễu.
- [ ] Drain/source copper phù hợp hướng tản nhiệt dự kiến.
- [ ] Có thermal via dưới/near power package theo datasheet và khả năng sản xuất.
- [ ] Khoảng cách MOSFET cho phép rework và không tạo hotspot quá lớn.

## F3. Gate driver

- [ ] Gate driver đặt sát MOSFET.
- [ ] Vòng HO/LO → gate → source-return ngắn và diện tích nhỏ.
- [ ] Gate trace không chạy song song lâu với phase node hoặc trace công suất nhiễu cao.
- [ ] Gate resistor đặt sát gate MOSFET hoặc theo chiến lược tuning đã chọn.
- [ ] Có footprint tùy chọn cho turn-on/turn-off resistor và diode nếu cần tuning.
- [ ] Gate-source pull-down đặt sát MOSFET.
- [ ] Kelvin source/driver return tách khỏi đường source mang dòng công suất khi package hỗ trợ.
- [ ] Bootstrap diode/capacitor đặt sát chân driver tương ứng.
- [ ] Tụ decoupling GVDD/charge pump đặt đúng vị trí theo datasheet driver.
- [ ] nFAULT/ENABLE/MODE/GAIN có routing sạch, pull-up/down đúng vị trí.
- [ ] Ground của gate driver không bị dòng công suất lớn chạy xuyên qua vùng tham chiếu.
- [ ] Có test point an toàn cho HO, LO, GH/SH/GL hoặc node phù hợp; tránh tạo stub lớn.

## F4. Shunt và current sensing

- [ ] Shunt đặt đúng đường dòng cần đo, không có đường bypass bằng copper khác.
- [ ] Hai đường sense lấy Kelvin trực tiếp từ hai đầu điện trở shunt.
- [ ] Sense+ và Sense− đi thành cặp, gần nhau và có môi trường nhiễu tương đồng.
- [ ] Không lấy sense từ power pour ở vị trí tùy tiện.
- [ ] Cặp sense tránh switching node, gate trace và cuộn cảm.
- [ ] RC filter đặt sát input current-sense amplifier/ADC theo mục đích lọc.
- [ ] Hai nhánh RC vi sai có linh kiện và layout đối xứng.
- [ ] Sense amplifier đặt gần shunt hoặc theo khuyến nghị datasheet.
- [ ] Analog ground return không dùng chung đoạn có dòng gate/power lớn.
- [ ] Input common-mode, dv/dt immunity và clearance đã được xem xét.
- [ ] Với low-side shunt, đã đánh giá ground bounce ảnh hưởng phép đo.
- [ ] Với inline/phase shunt, đã đánh giá điện áp common-mode và switching transient.

## F5. Điện áp bus và phase sensing

- [ ] Divider điện áp cao đặt gần nguồn đo nhưng tín hiệu sau divider được bảo vệ khỏi nhiễu.
- [ ] Chuỗi điện trở divider đáp ứng voltage rating và power rating từng linh kiện.
- [ ] Creepage/clearance quanh phần điện áp cao được đảm bảo.
- [ ] Tụ lọc đặt gần ADC input.
- [ ] Có clamp/protection phù hợp để ADC không vượt giới hạn.
- [ ] Trace ADC không chạy song song hoặc dưới phase node.
- [ ] Ground của divider/RC filter về analog reference đúng điểm.

---

# G. MCU, clock, reset và analog

## G1. STM32G4/MCU

- [ ] MCU placement cho phép fanout sạch và không chia cắt ground plane.
- [ ] Tất cả VDD/VDDA/VREF+/VBAT có decoupling đúng datasheet.
- [ ] VDDA/VREF routing tránh digital return và switching noise.
- [ ] Ground dưới MCU liên tục; có ground stitching via phù hợp.
- [ ] SWD/JTAG connector gần MCU, trace ngắn và không ảnh hưởng boot strap.
- [ ] NRST có routing ngắn, pull-up/filter đúng thiết kế.
- [ ] BOOT/configuration pins có mức xác định và test point nếu cần.
- [ ] ADC pin không đi gần clock, PWM, gate hoặc communication edge tốc độ cao.
- [ ] PWM outputs tới gate driver được route gọn, tránh stub và crosstalk.

## G2. Crystal/oscillator

- [ ] Crystal và load capacitor đặt sát chân oscillator.
- [ ] Hai trace crystal ngắn, cân đối và tránh via nếu có thể.
- [ ] Không có tín hiệu tốc độ cao hoặc switching node chạy dưới/quanh crystal.
- [ ] Ground guard/keepout áp dụng đúng theo khuyến nghị MCU/crystal.
- [ ] Không đặt test point tạo stub trên trace crystal trừ khi thực sự cần.
- [ ] Vỏ crystal được nối ground nếu package và datasheet yêu cầu.

## G3. Analog ground và reference

- [ ] Không tách AGND/DGND tùy tiện làm đứt return path.
- [ ] Nếu dùng net AGND riêng, điểm nối AGND-DGND được xác định rõ và có lý do.
- [ ] Analog current return không đi chung đoạn với gate driver hoặc power switching current.
- [ ] VREF có decoupling, guard và return đúng khuyến nghị.
- [ ] Op-amp/current-sense amplifier có input/output RC ổn định và layout gọn.
- [ ] Các node trở kháng cao ngắn, sạch và tránh vùng ô nhiễm flux nếu nhạy.

---

# H. Nguồn xung và nguồn tuyến tính

- [ ] Placement theo vòng dòng nóng trong datasheet/reference layout.
- [ ] Input capacitor sát chân VIN và PGND của converter.
- [ ] Catch diode/synchronous FET/inductor/output capacitor đặt đúng chuỗi dòng.
- [ ] Switching node nhỏ và cách xa feedback/analog.
- [ ] Feedback trace lấy từ điểm output sạch, không lấy trong đường dòng lớn.
- [ ] Feedback divider đặt sát FB pin.
- [ ] Ground của feedback về quiet ground theo datasheet.
- [ ] Bootstrap capacitor/diode đặt sát IC.
- [ ] Inductor không đặt gần crystal, shunt amplifier hoặc magnetic sensor.
- [ ] Power ground và signal ground nối theo kiến trúc datasheet khuyến nghị.
- [ ] Có copper và thermal via đủ để tản nhiệt regulator.
- [ ] Kiểm tra minimum on-time/off-time, nhưng không dùng layout để che lỗi thiết kế schematic.

---

# I. Giao tiếp và ESD/EMC

## I1. Nguyên tắc chung cho connector ngoài board

- [ ] TVS/ESD protection đặt sát connector, trước khi trace đi sâu vào board.
- [ ] Đường xả ESD từ TVS tới chassis/ground ngắn, rộng, ít via và ít cảm kháng.
- [ ] Không để xung ESD phải chạy xuyên qua vùng MCU trước khi về ground.
- [ ] Connector shield có chiến lược nối chassis/digital ground rõ ràng.
- [ ] Common-mode choke/ferrite đặt đúng thứ tự so với TVS theo mục tiêu thiết kế.
- [ ] Tín hiệu off-board có series resistor/filter/termination khi cần.
- [ ] Khoảng cách giữa connector nhiễu cao và khối analog đủ lớn.

## I2. CAN/CAN-FD

- [ ] CANH/CANL đi thành cặp, gần nhau và tương đối cân bằng.
- [ ] Tránh stub dài tới transceiver, termination hoặc connector.
- [ ] Termination 120 Ω/split termination đặt đúng vị trí và có tùy chọn enable nếu cần.
- [ ] Transceiver đặt gần connector.
- [ ] TVS và common-mode choke bố trí để dòng surge/ESD không đi vào logic ground ngoài ý muốn.
- [ ] Có ground reference hoặc shield strategy cho cable.
- [ ] TXD/RXD tránh chạy gần switching node và gate trace.

## I3. RS485/Modbus

- [ ] A/B đi cặp, kiểm tra naming A/B theo transceiver và connector thực tế.
- [ ] Termination, bias resistor và fail-safe network đúng vị trí.
- [ ] TVS/common-mode protection đặt gần connector.
- [ ] Có kiểm tra isolation/grounding nếu nối thiết bị ở chênh lệch ground lớn.

## I4. USB

- [ ] D+/D− route differential theo impedance mục tiêu.
- [ ] Hai trace cùng môi trường, hạn chế via và stub.
- [ ] Không chạy qua split/void của reference plane.
- [ ] ESD protector đặt sát connector và có capacitance phù hợp.
- [ ] Common-mode choke chỉ dùng khi cần và layout đúng chiều.
- [ ] Không đặt test point kiểu stub dài trên D+/D−.
- [ ] USB shield/chassis connection được xác định rõ.
- [ ] VBUS sense, current limit và power switch routing đúng kiến trúc nguồn.

---

# J. Routing và return path

- [ ] Tất cả net đã route, không còn unrouted/ratsnest.
- [ ] Critical nets được route trước và đúng constraint.
- [ ] Tín hiệu tốc độ cao có reference plane liên tục.
- [ ] Không có trace quan trọng băng qua split, slot hoặc void của reference plane.
- [ ] Khi đổi lớp, có stitching via GND gần signal via nếu cần duy trì return path.
- [ ] Hai tín hiệu nhiễu cao/nhạy nhiễu không chạy song song quá dài.
- [ ] Khoảng cách giữa các nhóm tín hiệu phù hợp crosstalk target.
- [ ] Tránh góc nhọn và copper sliver khó sản xuất.
- [ ] Góc route ưu tiên 45° hoặc bo hợp lý; không coi góc 90° là lỗi duy nhất mà bỏ qua return path.
- [ ] Không có trace neck-down dưới mức cho phép.
- [ ] Không có via stub đáng kể trên đường tốc độ cao nếu yêu cầu nghiêm ngặt.
- [ ] Teardrop được dùng khi quy trình hoặc độ bền cơ khí cần.
- [ ] Trace vào pad hợp lý, không tạo acid trap hoặc solderability issue.
- [ ] Tín hiệu reset, interrupt và fault tránh vùng dv/dt cao.
- [ ] Ground stitching via bố trí dọc mép board, gần connector/shield hoặc quanh vùng nhiễu khi có lý do EMC.
- [ ] Không có ground island chỉ nối bằng một cổ chai mỏng.
- [ ] Return current của từng giao tiếp được hình dung và kiểm tra thủ công.

---

# K. Plane, copper pour và thermal

- [ ] Refill tất cả copper zone sau thay đổi cuối cùng.
- [ ] Không còn orphan copper hoặc island không mong muốn.
- [ ] Ground plane có đủ stitching via.
- [ ] Thermal relief phù hợp giữa khả năng hàn và dòng điện.
- [ ] Pad dòng lớn không bị thermal relief quá yếu.
- [ ] Pad cần hàn tay không bị nối trực tiếp vào plane quá lớn nếu gây khó hàn.
- [ ] Copper balance hợp lý để giảm cong vênh.
- [ ] Khoảng cách plane tới mép board/slot đúng rule.
- [ ] Thermal via không hút thiếc khỏi pad khi không được fill/cap.
- [ ] Có vùng copper tản nhiệt cho MOSFET, regulator, shunt và diode.
- [ ] Đã ước lượng tổn hao chính và đường truyền nhiệt tới PCB/heatsink/air.
- [ ] Sensor nhiệt đặt ở vị trí phản ánh đúng đại lượng cần bảo vệ.
- [ ] NTC không đặt quá gần nguồn nhiệt sai lệch hoặc quá xa MOSFET cần bảo vệ.
- [ ] Đã kiểm tra nhiệt độ linh kiện lân cận tụ điện và connector.

---

# L. Creepage, clearance và an toàn điện

- [ ] Xác định điện áp làm việc, transient và pollution degree/tiêu chuẩn áp dụng.
- [ ] Clearance được kiểm tra theo chênh lệch điện áp thực tế giữa các net.
- [ ] Creepage được kiểm tra theo đường bề mặt, kể cả quanh pad, slot và board edge.
- [ ] Khoảng cách phase-to-phase, phase-to-ground và VBUS-to-low-voltage đạt yêu cầu.
- [ ] Slot cách điện được dùng đúng mục đích và nhà sản xuất xác nhận khả năng gia công.
- [ ] Không có silkscreen/copper/test point làm giảm khoảng cách cách điện.
- [ ] Mounting hardware và heatsink kim loại không vi phạm cách điện.
- [ ] Test point điện áp nguy hiểm được che chắn/ghi nhãn phù hợp.
- [ ] Conformal coating không được mặc định dùng để bù cho clearance thiếu nếu chưa được tiêu chuẩn cho phép.

---

# M. DFM, DFA và panelization

## M1. DFM PCB fabrication

- [ ] Trace/space không dùng giới hạn cực tiểu của fab nếu không cần thiết.
- [ ] Minimum drill, annular ring và aspect ratio đạt năng lực fab.
- [ ] Có kiểm tra via-to-pad, via-to-via và drill-to-copper.
- [ ] Solder-mask sliver đủ lớn.
- [ ] Solder-mask opening không bị thiếu hoặc merge ngoài ý muốn.
- [ ] Copper thieving/balancing do fab thêm không ảnh hưởng vùng RF/antenna/isolation.
- [ ] Surface finish được chỉ định rõ.
- [ ] Controlled impedance và tolerance được ghi rõ.
- [ ] Via tenting, plugging, filling và capping được chỉ định rõ.
- [ ] Castellated hole, edge plating, gold finger hoặc carbon contact được ghi chú đầy đủ nếu có.
- [ ] Board thickness, copper weight và finished hole size rõ ràng.

## M2. DFA/SMT assembly

- [ ] Fiducial global có trên board/panel và không đối xứng gây lắp ngược.
- [ ] Fiducial có solder-mask clearance và copper clearance đúng yêu cầu assembler.
- [ ] Tooling hole có đủ nếu panel/assembly cần.
- [ ] Component-to-edge phù hợp conveyor, stencil và reflow.
- [ ] Linh kiện nặng/cao có chiến lược cố định nếu môi trường rung.
- [ ] Không đặt linh kiện nhỏ sát connector hoặc heatsink gây khó gắp/hàn.
- [ ] Orientation diode, LED, IC và tụ phân cực nhất quán khi có thể.
- [ ] Tombstoning risk được xem xét cho linh kiện nhỏ nối vào copper không cân bằng.
- [ ] Thermal pad paste được chia cửa sổ để tránh float/void quá mức.
- [ ] Fine-pitch footprint có solder-mask/paste rule được assembler chấp nhận.
- [ ] Bottom-side component phù hợp quy trình reflow hai mặt.
- [ ] Wave/selective solder keepout được đảm bảo nếu có THT.

## M3. Panelization

- [ ] Chọn V-cut hay tab-route phù hợp hình dạng và linh kiện gần mép.
- [ ] Khoảng cách linh kiện/copper tới đường tách panel đủ lớn.
- [ ] Mouse-bite không nằm ở vùng cơ khí hoặc connector nhạy.
- [ ] Rail, tooling hole, fiducial và panel mark đầy đủ.
- [ ] Hướng panel hóa giảm cong vênh và phù hợp luồng SMT.
- [ ] Có nhận diện vị trí board trong panel nếu cần trace lỗi reflow theo vị trí.

---

# N. Silkscreen, assembly và nhận diện

- [ ] Reference designator có mặt cho tất cả linh kiện cần lắp/debug.
- [ ] Reference không trùng pad, via hở, board edge hoặc linh kiện khác.
- [ ] Chữ đủ kích thước và line width để nhà sản xuất in được.
- [ ] Pin 1/cực tính nhìn thấy sau assembly khi có thể.
- [ ] Connector pinout, nguồn, polarity và pha U/V/W được ghi rõ.
- [ ] Có cảnh báo điện áp/dòng cao nếu cần.
- [ ] Tên board, revision, serial/QR/barcode area được bố trí.
- [ ] Logo/chứng nhận không được thêm nếu chưa được phép sử dụng.
- [ ] Assembly drawing thể hiện orientation và DNP rõ ràng.
- [ ] Bottom silkscreen không bị mirror sai.

---

# O. DFT, bring-up và debug

- [ ] Có test point cho tất cả rail nguồn chính.
- [ ] Có test point GND gần các điểm đo quan trọng để giảm loop probe.
- [ ] Có test point cho reset, boot, fault, enable và communication.
- [ ] Có điểm đo current-sense output, bus voltage sense và temperature sense.
- [ ] Có vị trí đo PWM/gate phù hợp và an toàn.
- [ ] Test point không tạo stub đáng kể trên USB/crystal/high-speed nets.
- [ ] SWD/JTAG/UART bootloader tiếp cận được sau assembly.
- [ ] Có phương án isolate power stage khi bring-up logic board.
- [ ] Có jumper/0 Ω để tách rail, bypass filter hoặc cô lập khối khi debug nếu cần.
- [ ] Có footprint tuning cho gate resistor, snubber, filter và termination.
- [ ] Có phương án đo dòng đầu vào/pha an toàn.
- [ ] Flying probe/bed-of-nails accessibility được xem xét nếu sản xuất số lượng.
- [ ] Test point có net label trong fabrication/assembly/test document.

---

# P. Kiểm tra tự động và review thủ công

## P1. Kiểm tra CAD

- [ ] ERC schematic không còn lỗi chưa được giải trình.
- [ ] DRC PCB sạch 100%, hoặc waiver được ghi rõ từng lỗi.
- [ ] Không còn unconnected item.
- [ ] Không còn footprint chưa đặt hoặc component ngoài board.
- [ ] Không còn courtyard overlap không được chấp thuận.
- [ ] Differential pair report đạt width/gap/skew constraint.
- [ ] Net length report đã review cho net critical.
- [ ] Drill report không có kích thước bất thường hoặc quá nhiều loại drill không cần thiết.
- [ ] Solder-mask/paste kiểm tra bằng Gerber viewer độc lập.
- [ ] 3D clearance check hoàn tất.

> **Lưu ý:** DRC sạch chỉ chứng minh layout tuân theo bộ rule đã nhập. Cần xác nhận bộ rule đó đúng với yêu cầu điện, cơ khí và năng lực nhà sản xuất.

## P2. Peer review

- [ ] Người thứ hai kiểm tra footprint của connector, MOSFET, driver, MCU và linh kiện phân cực.
- [ ] Người thứ hai kiểm tra board orientation và connector pinout theo cable thực tế.
- [ ] Review theo từng current loop thay vì chỉ nhìn từng net.
- [ ] Review đường return của tín hiệu tốc độ cao và analog.
- [ ] Review power-up, fault và regenerative-braking current paths.
- [ ] Review vị trí TVS và đường xả ESD.
- [ ] Review creepage/clearance theo điện áp thực tế.
- [ ] Review thermal bottleneck và khả năng rework.
- [ ] Tất cả comment có owner, severity, deadline và trạng thái đóng.

---

# Q. Output fabrication và assembly

## Q1. Fabrication package

- [ ] Gerber hoặc ODB++ được tạo từ revision PCB cuối cùng.
- [ ] NC drill PTH và NPTH đúng, slot được thể hiện chính xác.
- [ ] Board outline chỉ xuất một contour đúng.
- [ ] Fabrication drawing có:
  - [ ] Kích thước board và dung sai.
  - [ ] Stack-up.
  - [ ] Material/Tg khi cần.
  - [ ] Finished copper thickness.
  - [ ] Surface finish.
  - [ ] Controlled impedance.
  - [ ] Via treatment.
  - [ ] UL/marking requirement nếu có.
- [ ] IPC-D-356/netlist được xuất nếu fab hỗ trợ kiểm tra netlist.
- [ ] Gerber đã mở bằng viewer độc lập và so với PCB editor.
- [ ] Kiểm tra top/bottom không bị mirror sai.
- [ ] Kiểm tra copper, mask, paste, silk, drill và outline từng layer.

## Q2. Assembly package

- [ ] BOM khớp revision schematic/PCB.
- [ ] BOM có MPN, manufacturer, quantity, DNP và alternative rule.
- [ ] Pick-and-place/CPL đúng origin, rotation và board side.
- [ ] Assembly drawing top/bottom rõ ràng.
- [ ] Stencil/paste data đúng revision.
- [ ] Special assembly notes được cung cấp: heatsink, thermal pad, hand solder, adhesive.
- [ ] Reference designator giữa BOM, CPL và PCB không lệch.
- [ ] Kiểm tra centroid/rotation bằng preview của nhà lắp ráp nếu có.

## Q3. Release control

- [ ] Tất cả file output có cùng revision và timestamp release.
- [ ] Không trộn file từ revision cũ.
- [ ] Release package được nén và checksum nếu quy trình yêu cầu.
- [ ] Có changelog mô tả thay đổi từ revision trước.
- [ ] Có bản PDF schematic và PDF fabrication/assembly drawing đi kèm.
- [ ] Source project đã commit/tag trong version control.
- [ ] Library dependency đã commit hoặc archive để tái tạo thiết kế.
- [ ] Người thiết kế và reviewer đã sign-off.

---

# R. Quality gate trước khi đặt PCB

Không release nếu bất kỳ điều kiện nào sau đây chưa đạt:

- [ ] Không còn lỗi DRC/ERC nghiêm trọng.
- [ ] Footprint và pinout của mọi linh kiện critical đã được kiểm tra với datasheet.
- [ ] Board outline, mounting hole và connector đã được kiểm tra cơ khí.
- [ ] Power path, commutation loop và gate loop đã được review.
- [ ] Shunt Kelvin routing và analog sensing đã được review.
- [ ] Creepage/clearance đã được xác nhận.
- [ ] Thermal path đã được đánh giá.
- [ ] Gerber/drill/mask/paste đã được kiểm tra bằng viewer độc lập.
- [ ] BOM và pick-and-place khớp PCB revision.
- [ ] Issue mức Critical/High đã đóng hoặc có waiver được phê duyệt.

### Sign-off

| Vai trò | Họ tên | Kết luận | Ngày | Chữ ký/Link review |
|---|---|---|---|---|
| PCB Designer |  | Pass / Fail |  |  |
| Hardware Reviewer |  | Pass / Fail |  |  |
| Mechanical Reviewer |  | Pass / Fail / N/A |  |  |
| Manufacturing/PCBA Reviewer |  | Pass / Fail / N/A |  |  |
| Project Approver |  | Approved / Rejected |  |  |

---

# S. Issue log

| ID | Hạng mục | Mô tả lỗi/rủi ro | Severity | Owner | Due date | Trạng thái | Bằng chứng đóng lỗi |
|---|---|---|---|---|---|---|---|
| PCB-001 |  |  | Critical/High/Medium/Low |  |  | Open |  |
| PCB-002 |  |  | Critical/High/Medium/Low |  |  | Open |  |
| PCB-003 |  |  | Critical/High/Medium/Low |  |  | Open |  |

---

# T. Gợi ý phân loại severity

- **Critical:** Có thể gây nguy hiểm, cháy nổ, phá hỏng linh kiện, vi phạm cách điện hoặc khiến board không thể hoạt động.
- **High:** Có khả năng cao gây respin, lỗi chức năng chính, EMC nghiêm trọng hoặc không thể sản xuất/lắp ráp ổn định.
- **Medium:** Ảnh hưởng độ tin cậy, hiệu năng, khả năng debug, yield hoặc tăng chi phí sản xuất.
- **Low:** Cải thiện tính nhất quán, tài liệu, silkscreen, thẩm mỹ hoặc khả năng bảo trì.

---

# U. Tài liệu tham khảo công khai

- Altium, **PCB Design Review Checklist**: https://resources.altium.com/p/pcb-design-and-review-checklist
- Azonenberg, **PCB Layout Review Checklist**: https://github.com/azonenberg/pcb-checklist/blob/master/layout-checklist.md
- Sierra Circuits, **PCB Design Checklist to Build a Flawless Board**: https://www.protoexpress.com/blog/pcb-design-checklist-to-build-flawless-board/

> Checklist này là khung kiểm tra kỹ thuật. Các giá trị cụ thể về trace width, impedance, creepage, clearance, via, nhiệt và EMC phải được tính theo stack-up, điện áp, dòng điện, datasheet, tiêu chuẩn áp dụng và năng lực của nhà sản xuất thực tế.
