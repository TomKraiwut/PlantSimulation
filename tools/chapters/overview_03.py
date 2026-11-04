# -*- coding: utf-8 -*-
"""Overview 3: Small Parts Production -- from PtS2606_2_SmallPartsProduction.pptx"""
from gen_site import screenshot, step_list, side_by_side

OBJECTIVES = ["เปิดโมเดลตัวอย่าง Small Parts Production และรันเทียบไลน์เดิมกับไลน์ที่ปรับแล้วได้",
                       "หาคอขวดของไลน์ประกอบด้วย Station Utilization, Bottleneck Analyzer และ Ranking ได้",
                       "หาขนาด Buffer ที่พอด้วย Experiment Manager และอ่านผลพลังงานจาก Energy Analyzer ได้"]

BODY = f'''
<p class="lead" style="max-width:46em;">โมเดลตัวอย่างตัวที่สองต่อจาก <a href="overview-02.html">00A Factory 51</a> — ยังไม่ต้องสร้างอะไรเอง
แค่เปิดไลน์ประกอบชิ้นงานเล็กที่ Siemens ทำไว้แล้ว และลองใช้เครื่องมือวิเคราะห์ทีละขั้น 10 ขั้นตอน: รันไลน์เดิม ดูกราฟ
หาคอขวด เพิ่ม Buffer หาขนาด Buffer ที่พอด้วย Experiment Manager และดูการใช้พลังงาน
ให้เห็นภาพว่าเรียนจบชุดสอนแล้วจะวิเคราะห์ไลน์จริงได้แบบไหน (บท 01–09 จะสอนสร้างและวิเคราะห์ไลน์ของตัวเองทีละเรื่อง)</p>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 และโมเดล <code>Small Parts Production.spp</code> (อยู่ใน <code>Examples\\Demo</code>
ของโฟลเดอร์ติดตั้ง) &nbsp;·&nbsp; ผลที่วัดได้ใน 2606: ผลผลิต <strong>1,400 → ~1,460 ชิ้น/วัน</strong> (Assembly1 → Assembly2)
</div>

<h2>ลำดับการวิเคราะห์</h2>
<table>
<tr><th>ลำดับ</th><th>งาน</th><th>ทำอะไร</th><th>ใครทำ</th></tr>
<tr><td>1</td><td>รันไลน์เดิม</td><td>Assembly1 รัน 1 วัน ดู Throughput และพลังงาน</td><td>ผู้ใช้</td></tr>
<tr><td>2</td><td>ดูกราฟ</td><td>Station / Worker Utilization และกะทำงาน</td><td>ผู้ใช้</td></tr>
<tr><td>3</td><td>หาคอขวด</td><td>Bottleneck Analyzer + Ranking</td><td>Plant Sim</td></tr>
<tr><td>4</td><td>เพิ่ม Buffer</td><td>Assembly2 มี Buffer หน้า MS4</td><td>ผู้ใช้</td></tr>
<tr><td>5</td><td>หาขนาด Buffer</td><td>Experiment Manager 8 การทดลอง</td><td>Plant Sim</td></tr>
<tr><td>6</td><td>ดูพลังงาน</td><td>Energy Analyzer + สายพานหยุดอัตโนมัติ</td><td>Plant Sim</td></tr>
</table>

<h2>ขั้นที่ 1: เปิดโมเดลตัวอย่าง Small Parts Production</h2>
{side_by_side(
    screenshot("assets/images/overview/03-01.jpg", "โมเดล Small Parts Production และ Class Library"),
    step_list([
        "<code>File → Open</code> แล้วเลือก <code>...\\Plant Simulation 2606\\Examples\\Demo\\Small Parts Production.spp</code>",
        "Class Library → <code>Models</code> มี <strong>Assembly1</strong> (ไลน์เดิม) และ <strong>Assembly2</strong> (เพิ่ม Buffer)",
        "แถบ <em>The model contains outdated libraries</em> กด <code>X</code> ปิดได้ บทนี้ไม่ต้องอัปเดต",
        "Frame เปิดเป็นหน้าต่าง 3D มุมมองจากด้านบน (2606 ไม่มีหน้าต่าง 2D แยก)",
        "Assembly2 เปิดซ้อนอยู่ด้านหลัง ปิดไว้ก่อนได้",
    ])
)}
<div class="note"><strong>ข้อควรจำ:</strong> ไฟล์ใน Program Files บันทึกทับไม่ได้ — ถ้าจะแก้ให้ <code>File → Save As</code> ไปโฟลเดอร์งานของตัวเองก่อน</div>

<h2>ขั้นที่ 2: รัน Assembly1 แล้วดู Throughput</h2>
{screenshot("assets/images/overview/03-02.jpg", "Assembly1 ระหว่างรันและหลังรันจบ 1 วัน")}
{step_list([
    "กด <code>Start</code> ในโมเดล (รันจบ 1 วันทันที) หรือ ▶ ที่ <code>Home → Event Controller</code> ถ้าอยากเห็นชิ้นงานวิ่ง",
    "ระหว่างรัน ชิ้นงานต่อคิวยาวหน้า MS3 / MS4",
    "จบ 1 วัน: Throughput <strong>1,400 ชิ้น</strong>",
    "พลังงานทั้งไลน์ <strong>14.3 kWh</strong> (Energy saving measures = ปิด, จุดแดง)",
])}

<h2>ขั้นที่ 3: Station Utilization — สัดส่วนเวลาของทุกสถานี</h2>
{screenshot("assets/images/overview/03-03.jpg", "เมนู Show ของ Station Utilization และกราฟสัดส่วนเวลา")}
{step_list([
    "คลิกขวาที่ <code>Station Utilization</code>",
    "เลือก <code>Show</code>",
    "<strong>MS4</strong> Waiting ต่ำสุด 1.4% และ Failed สูงสุด 3.3% → งานไม่เคยขาด = <strong>คอขวด</strong>",
    "MS1–MS5 เป็นสถานีคน ทำงาน 2 กะ จึงมี Unplanned 33% (สีฟ้า)",
])}

<h2>ขั้นที่ 4: Worker Utilization และ ShiftCalendar</h2>
{screenshot("assets/images/overview/03-04.jpg", "กราฟ Worker Utilization และหน้าต่าง ShiftCalendar")}
{step_list([
    "คลิกขวา <code>Worker-Utilization</code> → <code>View Chart</code>",
    "Worker / Worker_Round: Working ประมาณ 25–29%",
    "Adjuster (ช่างปรับเครื่อง) ทำงานน้อย รอเป็นส่วนใหญ่",
    "ดับเบิลคลิก <code>ShiftCalendar</code>: Shift-1 06:00–14:00, Shift-2 14:00–22:00",
    "คอลัมน์ <code>Pauses</code> = เวลาพักในแต่ละกะ",
])}

<h2>ขั้นที่ 5: Bottleneck Analyzer — Show Analysis</h2>
{screenshot("assets/images/overview/03-05.jpg", "เมนู Show Analysis และแท่งสถานะบนสถานี")}
{step_list([
    "คลิกขวาที่ <code>Bottlenecks</code>",
    "เลือก <code>Show Analysis</code>",
    "แท่งสีขึ้นบนทุกสถานี: <strong>เขียว</strong> Working, <strong>เทา</strong> Waiting, <strong>เหลือง</strong> Blocked, <strong>แดง</strong> Failed",
    "MS4 แท่งเขียวสูง แทบไม่มีสีเทา ต่างจาก AS3 / AS4 ที่สีเทาสูง",
])}

<h2>ขั้นที่ 6: Ranking — เรียงตารางหาคอขวด</h2>
{screenshot("assets/images/overview/03-06.jpg", "หน้าต่างเลือกเกณฑ์ Ranking และตาราง ResourceStats")}
{step_list([
    "คลิกขวา <code>Bottlenecks</code> → <code>Ranking</code>",
    "เลือกเกณฑ์ <code>Working</code>",
    "กด <code>OK</code> ได้ตาราง <code>ResourceStats</code>",
    "คลิกขวาหัวคอลัมน์ <code>waiting</code> → <code>Sort Ascending</code>",
    "MS4, MS2, MS1: waiting ต่ำ + blocked ต่ำ = <strong>คอขวด</strong>",
    "ParallelProc / AS6: waiting ต่ำแต่ blocked สูง = ถูกปลายทางบล็อก <em>ไม่ใช่</em>คอขวด",
])}

<h2>ขั้นที่ 7: Assembly2 — เพิ่ม Buffer หน้า MS4 แล้วเทียบผล</h2>
{screenshot("assets/images/overview/03-07.jpg", "Assembly2 ที่มี Buffer หน้า MS4 และกราฟ Station Utilization")}
{step_list([
    "ดับเบิลคลิก <code>Models → Assembly2</code> ใน Class Library แล้วกด <code>Start</code>",
    "Throughput ~1,460 ชิ้น (วัดได้ 1,462–1,466 จาก 4 รอบ; Assembly1 = 1,400)",
    "Buffer B (<code>Buffer1</code>) อยู่ระหว่าง AS3 กับ MS4",
    "Energy saving measures เปิด (จุดเขียว)",
    "Station Utilization: MS4 ไม่มีสีเหลือง (Blocked) แล้ว (หัวกราฟยังเขียน Assembly 1 ตามตัวอย่างของ Siemens)",
])}

<h2>ขั้นที่ 8: BufferOptimization — กำหนด Output, Input และ Experiments</h2>
{screenshot("assets/images/overview/03-08.jpg", "หน้าต่าง Experiment Manager และ Define Output Values")}
{step_list([
    "ดับเบิลคลิก <code>BufferOptimization</code> (Experiment Manager) → <code>Define Output Values</code>",
    "<code>root.Drain.statDeleted</code> = Throughput, <code>High Values are Better</code> = true → OK",
    "<code>Define Input Values</code> (ภาพถัดไป)",
    "<code>Define Experiments</code> (ภาพถัดไป)",
    "<code>Observations per experiment</code> = 5 (รันซ้ำ 5 รอบต่อการทดลองแล้วเฉลี่ย)",
])}
{screenshot("assets/images/overview/03-09.jpg", "Define Input Values และตาราง Experiments")}
{step_list([
    "<code>root.Buffer1.capacity</code> = ความจุของ Buffer B → OK",
    "<code>Active</code> = true ทุกแถว = รันทุกการทดลอง",
    "Capacity of buffer 2, 4, 6 … 16 รวม 8 การทดลอง → OK",
])}
<div class="tip"><strong>ทำซ้ำ:</strong> อยากทดลองค่าอื่น แก้ตัวเลขในคอลัมน์ Capacity of buffer หรือเพิ่มแถวได้เลย</div>

<h2>ขั้นที่ 9: รันการทดลอง และอ่าน Report</h2>
{screenshot("assets/images/overview/03-10.jpg", "ปุ่ม Start ของ Experiment Manager และ Report ผลการทดลอง")}
{step_list([
    "กด <code>Start</code> รอข้อความ <em>The experiment run is finished</em> (ประมาณ 10 วินาที) → OK",
    "ครบ 8/8 การทดลอง 5/5 รอบ",
    "Buffer ตั้งแต่ <strong>6</strong> ขึ้นไป = 1,478.8 ชิ้น (เฉลี่ย) ค่าเท่ากันหมด → <strong>6 ก็พอ</strong>",
    "Report เปิดเองหลังรันจบ หรือกด <code>Evaluation → Report</code>",
    "สรุปค่าที่ดีที่สุด: Throughput สูงสุด 1,478.8",
    "บันทึก / พิมพ์ Report จากปุ่มมุมซ้ายบน",
])}

<h2>ขั้นที่ 10: Energy — ตั้งค่าพลังงานของสายพาน และอ่าน Energy Analyzer</h2>
{screenshot("assets/images/overview/03-11.jpg", "หน้าต่างสายพาน F1 และแท็บ Energy")}
{step_list([
    "ใน Assembly2 ดับเบิลคลิกสายพาน <code>F1</code>",
    "<code>Automatic Stop</code> = สายพานหยุดเองเมื่อว่าง (ตัวที่ทำให้ประหยัดไฟ)",
    "คลิกแท็บ <code>Energy</code>",
    "<code>Active</code> = นับพลังงานของวัตถุนี้",
    "<code>Working</code> 1 kW ขณะลำเลียง",
    "<code>Operational</code> 0.3 kW ขณะเปิดรอ",
])}
{screenshot("assets/images/overview/03-12.jpg", "เมนู Energy Analyzer, กราฟพลังงานแยกตามวัตถุ และ Power Input ตามเวลา")}
{step_list([
    "คลิกขวา <code>Energy Analyzer</code>",
    "<code>Show Chart</code> = พลังงานแยกตามวัตถุ",
    "<code>Show Plotter</code> = Power Input ตามเวลา",
    "สถานีอัตโนมัติ AS / PreProduction ใช้ไฟมากสุด",
    "หลัง 22:00 (หมดกะ) Power Input ลดจาก ~37 kW เหลือ ~10 kW",
])}
<div class="note"><strong>ผล:</strong> Assembly2 ใช้ 11.6 kWh เทียบ Assembly1 14.3 kWh (ลด ~19%) ในขณะที่ได้ชิ้นงานมากขึ้น</div>

<h2>สรุปผล: Assembly1 เทียบ Assembly2 (วัดใน 2606)</h2>
<table>
<tr><th>หัวข้อ</th><th>Assembly1 (ไลน์เดิม)</th><th>Assembly2 (ปรับแล้ว)</th><th>หมายเหตุ</th></tr>
<tr><td>Throughput / วัน</td><td>1,400 ชิ้น</td><td>1,462–1,466 ชิ้น</td><td>รัน 1 วัน, 4 รอบ</td></tr>
<tr><td>พลังงาน / วัน</td><td>14.3 kWh</td><td>11.5–11.6 kWh</td><td>ลด ~19%</td></tr>
<tr><td>Buffer หน้า MS4</td><td>ไม่มี</td><td>B (Buffer1)</td><td>ขนาด 6 ก็พอ (ขั้นที่ 9)</td></tr>
<tr><td>Energy saving measures</td><td>ปิด</td><td>เปิด</td><td>สายพาน Automatic Stop</td></tr>
<tr><td>คอขวด</td><td>MS4 (Waiting 1.4%)</td><td>MS4 ไม่ Blocked แล้ว</td><td>ดูขั้นที่ 3, 6, 7</td></tr>
</table>

<h2>ปัญหาที่พบบ่อย และวิธีแก้ (2606)</h2>
<table>
<tr><th>อาการ</th><th>วิธีแก้</th></tr>
<tr><td>กด Start ในโมเดลแล้วจบทันที ไม่เห็นชิ้นงานวิ่ง</td><td>กด Reset แล้วใช้ ▶ ที่ <code>Home → Event Controller</code> (Real time) ปรับความเร็วด้วยแถบเลื่อน</td></tr>
<tr><td>Show Analysis แล้วมองไม่เห็นแท่ง</td><td>แท่งเป็น 3D มองจากด้านบนจะแบน → เอียงมุมกล้อง / ซูมเข้า</td></tr>
<tr><td>แถบ The model contains outdated libraries</td><td>กด <code>X</code> ปิดได้ บทนี้ไม่ต้อง Manage Libraries</td></tr>
<tr><td>Plotter แสดงแค่ช่วงสั้นๆ</td><td>เปิด Plotter ไว้ระหว่างรัน แล้วหยุดในช่วงเวลาที่สนใจ</td></tr>
<tr><td>Throughput ของ Assembly2 ไม่ตรงกับหน้านี้</td><td>ปกติ ต่างได้ไม่กี่ชิ้นต่อรอบ ใช้ Experiment Manager ที่เฉลี่ยหลายรอบ</td></tr>
<tr><td>บันทึกโมเดลไม่ได้</td><td>ไฟล์อยู่ใน Program Files → <code>File → Save As</code> ไปโฟลเดอร์ของตัวเอง</td></tr>
</table>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ในขั้นที่ 6 ทำไม ParallelProc / AS6 ที่ waiting ต่ำเหมือน MS4 จึง<em>ไม่ใช่</em>คอขวด?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะ blocked สูง — เครื่องทำเสร็จแล้วแต่ส่งต่อไม่ได้ แปลว่าปัญหาอยู่ที่ปลายทาง ไม่ใช่ที่ตัวมันเอง
คอขวดจริงต้อง waiting ต่ำ <em>และ</em> blocked ต่ำ (ทำงานตลอดเวลา) แบบ MS4 — ใช้หลักเดียวกันนี้ใน<a href="lessons-02.html">บท 02 คอขวด และ ParallelStation</a></div>
'''
