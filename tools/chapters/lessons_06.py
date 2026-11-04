# -*- coding: utf-8 -*-
"""Lessons 6: Track and Transporter -- from 06_Track_and_Transporter.pptx"""
from gen_site import screenshot, step_list, side_by_side

OBJECTIVES = [
    "วาด Track เป็นวงปิดมีมุมโค้ง และให้ AGVSource ปล่อยรถ Transporter วิ่งวนได้",
    "ลาก PickAndPlace ไปวางบน Track เพื่อโหลด/ขนถ่ายชิ้นงานกับรถโดยไม่ต้องเขียน Method ได้",
    "อ่านค่าที่ Plant Simulation สร้างให้ (sensor, Exit, OnSensor) และนับผลด้วย Display ได้",
    "วาด TwoLaneTrack ให้รถวิ่งสวนกันคนละเลนได้",
]

ONSENSOR = '''<pre><code>param SensorID: integer, Front: boolean
--Activating the sensor moves the parts from the
--container to the specified destination
@.stopped := true
var Destination:object := PickAndPlace2
while not @.Empty
  var mu: object := @.cont
  if not mu.move(Destination)
    stopuntil mu.location /= @ and not Destination.isLoading
  end
end
@.stopped := false</code></pre>'''

BODY = f'''
<p class="lead" style="max-width:46em;">ใน<a href="lessons-05.html">บท 05</a> สายพานพาชิ้นงานและพาเลทวิ่ง บทนี้ให้<strong>รถ (Transporter)</strong>
วิ่งบน <strong>Track</strong> ขนชิ้นงานแทน — 3 ขั้น: วาดเส้นทางวงปิด, ลากหุ่นยนต์ PickAndPlace วางบน Track ให้โหลด/ขนถ่ายชิ้นงานขึ้นลงรถ
และ TwoLaneTrack ให้รถวิ่งสวนกัน 2 เลน ทุกขั้นทำด้วยเมาส์และหน้าต่างตั้งค่า <strong>ไม่ต้องเขียน Method เลย</strong>
ผล: <strong>734 ชิ้น ใน 8 ชม.</strong> ด้วยรถ 2 คัน</p>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 และไฟล์ <code>06_Track_and_Transporter.spp</code>
(เฟรม T01_Route, T02_PickAndPlace, T03_TwoLaneTrack) &nbsp;·&nbsp; ทุกตัวเลขในบทนี้วัดจริงใน PtS 2606 ด้วยไฟล์นี้
</div>

<h2>ภาพรวม: 3 ขั้น จากวาดเส้นทาง ถึงรถวิ่งสวนกัน 2 เลน</h2>
<table>
<tr><th>ขั้น</th><th>เรื่อง</th><th>ได้อะไร</th></tr>
<tr><td>1</td><td>วาดเส้นทาง Track</td><td>วงปิด 82.6 m รถ Transporter 2 คัน</td></tr>
<tr><td>2</td><td>PickAndPlace บน Track</td><td>ลากวาง Load / Unload ได้ 734 ชิ้น/8 ชม.</td></tr>
<tr><td>3</td><td>TwoLaneTrack</td><td>รถยกกับรถบรรทุกวิ่งสวนกันคนละเลน</td></tr>
</table>

<h2>3 เฟรมในไฟล์นี้</h2>
<table>
<tr><th>เฟรม</th><th>เนื้อหา</th><th>ขั้นที่</th></tr>
<tr><td>T01_Route</td><td>Track วงปิด + AGVSource สร้างรถ Transporter 2 คันวิ่งวน ยังไม่มีชิ้นงาน</td><td>1</td></tr>
<tr><td>T02_PickAndPlace</td><td>T01 ที่เพิ่มฝั่งชิ้นงาน: Source → PickAndPlace → รถบน Track → PickAndPlace2 → Drain</td><td>2</td></tr>
<tr><td>T03_TwoLaneTrack</td><td>TwoLaneTrack 1 เส้น รถยกมีคนขับ (ForkliftWithHuman) เลน A กับรถบรรทุก (Truck) เลน B</td><td>3</td></tr>
</table>
<div class="tip"><strong>Track กับ Conveyor:</strong> Conveyor พาชิ้นงานวิ่ง ส่วน Track ให้รถ (Transporter) วิ่งเอง ชิ้นงานนั่งไปบนรถ
— Track คือทางวิ่งของรถ ความเร็วตั้งที่ตัวรถ ไม่ใช่ที่ Track</div>

<h2>ขั้นที่ 1: วาดเส้นทาง Track — วงปิดใน 5 ข้อ</h2>
<table>
<tr><th>ข้อ</th><th>ทำอะไร</th></tr>
<tr><td>1</td><td>เลือก Track</td></tr>
<tr><td>2</td><td>คลิกมุม ทำมุมโค้ง</td></tr>
<tr><td>3</td><td>ต่อปลายเข้าต้น</td></tr>
<tr><td>4</td><td>ตั้งค่า Transporter</td></tr>
<tr><td>5</td><td>AGVSource 2 คัน</td></tr>
</table>
<p>เฟรม <code>T01_Route</code> · ผล: วงปิด 34 × 9 m มุมโค้งรัศมี 2 m ยาว <strong>82.6 m</strong></p>

<h2>ขั้นที่ 1.1: เลือก Track จาก Toolbox</h2>
{screenshot("assets/images/lessons/06-01.jpg", "Toolbox แท็บ Material Flow และไอคอน Track สีส้ม")}
{step_list([
    "Toolbox แท็บ <code>Material Flow</code>",
    "คลิกไอคอนสีส้ม <code>Track</code> (ทางวิ่งของรถ Transporter)",
    "ชี้เมาส์ค้างไว้จะขึ้นชื่อ ใช้ตรวจว่าเลือกถูก (ไอคอนข้างกันคือ Converter)",
])}

<h2>ขั้นที่ 1.2: คลิกมุมเส้นทาง ทำมุมโค้ง แล้วกด Finish</h2>
{screenshot("assets/images/lessons/06-02.jpg", "Track วงปิดที่วาดด้วยการคลิกมุม และหน้าต่าง Line/Arc Parameters")}
{step_list([
    "คลิกจุดเริ่ม แล้วคลิกไปตามแนวตรงด้านบน 30 m",
    "ถึงมุม กด <strong>Ctrl</strong> ค้างแล้วคลิก = ส่วนโค้ง ทำซ้ำทุกมุม",
    "มุมขวาล่าง",
    "มุมซ้ายล่าง",
    "ขึ้นมาจบใกล้จุดเริ่ม",
    "ส่วนโค้งใช้ค่าในกรอบ <code>Arc Segments</code>: <code>Curve Angle</code> 90°",
    "<code>Radius</code> 2 m",
    "กด <code>Finish</code>",
])}
<div class="tip"><strong>ความยาว 82.57 m:</strong> ตรง 30 + 5 + 30 + 5 m และโค้ง 90° รัศมี 2 m 4 มุม (มุมละ 3.14 m)
· หน้าต่าง Line/Arc Parameters แสดงค่าของช่วงล่าสุด พิมพ์ตัวเลขแก้ได้</div>

<h2>ขั้นที่ 1.3: ต่อปลาย Track กลับเข้าต้น Track</h2>
{side_by_side(
    screenshot("assets/images/lessons/06-03.jpg", "Toolbox เลือก Connector แล้วต่อปลาย Track เข้าต้น Track"),
    step_list([
        "Toolbox เลือก <code>Connector</code>",
        "คลิกที่ <strong>ปลาย Track</strong> (ฝั่งซ้าย ก่อนถึงจุดเริ่ม)",
        "คลิกที่ <strong>ต้น Track</strong> → เป็นวงปิด รถวิ่งวนได้",
    ])
)}
<div class="note"><strong>ตรวจ:</strong> ชี้เมาส์ที่ Track ต้องเห็นตัวเองเป็นทั้งก่อนหน้าและถัดไป
· ถ้าไม่ต่อ รถจะวิ่งไปถึงปลายแล้วหยุด ต่อแล้วรถวิ่งวนไม่รู้จบ</div>

<h2>ขั้นที่ 1.4: ตั้งค่ารถ Transporter</h2>
{screenshot("assets/images/lessons/06-04.jpg", "หน้าต่าง MUs.Transporter แท็บ Attributes และแท็บ Load Bay")}
{step_list([
    "Class Library &gt; <code>MUs</code> &gt; ดับเบิลคลิก <code>Transporter</code>",
    "<code>Speed</code> 1 m/s (ค่าเริ่มต้น)",
    "ขนาดรถ <code>Length</code> 1.6 m <code>Width</code> 0.8 m",
    "แท็บ <code>Load Bay</code>",
    "<code>X-Dimension</code> 3",
    "<code>Y-Dimension</code> 2",
    "<code>Capacity</code> = 3 × 2 = <strong>6 ชิ้น ต่อคัน</strong>",
])}
<div class="tip"><strong>หลายแบบ:</strong> ไฟล์นี้ใช้ class <code>MUs.Transporter</code> ตรง ๆ ทุกคันที่สร้างจาก class นี้ได้ค่าเดียวกัน
แท็บ Battery ปิดอยู่ (รถไม่ใช้แบต) · ถ้าอยากให้รถหลายแบบ ให้คลิกขวา <code>Duplicate</code> ไป UserObjects แล้วแก้ที่สำเนา</div>

<h2>ขั้นที่ 1.5: AGVSource สร้างรถ 2 คัน แล้วรัน</h2>
{screenshot("assets/images/lessons/06-05.jpg", "หน้าต่าง AGVSource และรถ 2 คันวิ่งวนบน Track")}
{step_list([
    "วาง Source ซ้ายต้น Track ตั้งชื่อ <code>AGVSource</code> ต่อ Connector → Track",
    "<code>Interval Adjustable</code>",
    "<code>Amount</code> 2 = สร้าง 2 คันแล้วหยุด",
    "<code>Interval</code> 0:10 ปล่อยห่างกัน 10 วินาที",
    "<code>MU</code> = <code>*.MUs.Transporter</code> (ลาก Transporter มาวางบน Source ก็ได้)",
    "กดรัน",
    "รถ 2 คันวิ่งวน (ภาพที่เวลาจำลอง 40 วินาที)",
])}
<p>รถวิ่งรอบละ 82.6 วินาที (82.6 m ที่ 1 m/s) Source ไม่สร้างรถเพิ่มเพราะ Amount = 2</p>

<h3>ผลลัพธ์และปัญหาที่พบบ่อย (ขั้นที่ 1)</h3>
<table>
<tr><th>อาการ / ค่า</th><th>ความหมาย / วิธีแก้</th></tr>
<tr><td>Track 82.6 m รถ 2 คัน 1 m/s</td><td>รอบละ 82.6 วินาที รถวิ่งวนถึง 8 ชม.</td></tr>
<tr><td>วาดแล้วได้ Converter</td><td>ไอคอนผิด ใช้ไอคอนสีส้ม Track (ข้อ 1)</td></tr>
<tr><td>มุมเป็นเหลี่ยม ไม่โค้ง</td><td>ตอนคลิกมุมต้องกด Ctrl ค้าง (ข้อ 2)</td></tr>
<tr><td>รถวิ่งถึงปลายแล้วหยุด</td><td>ยังไม่ได้ต่อ Connector ปลาย → ต้น (ข้อ 3)</td></tr>
<tr><td>Source สร้างรถไม่หยุด</td><td>Amount ต้องเป็น 2 ไม่ใช่ -1 (ข้อ 5)</td></tr>
</table>

<h2>ขั้นที่ 2: PickAndPlace บน Track — โหลด/ขนถ่ายด้วยการลากวางใน 6 ข้อ</h2>
<table>
<tr><th>ข้อ</th><th>ทำอะไร</th></tr>
<tr><td>1</td><td>วาง Source หุ่นยนต์ Drain</td></tr>
<tr><td>2</td><td>ลาก PickAndPlace: Load part</td></tr>
<tr><td>3</td><td>ลาก PickAndPlace2: Unload part</td></tr>
<tr><td>4</td><td>ดูสิ่งที่โปรแกรมสร้าง</td></tr>
<tr><td>5</td><td>Display นับชิ้นงาน</td></tr>
<tr><td>6</td><td>รัน 8 ชม.</td></tr>
</table>
<p>เฟรม <code>T02_PickAndPlace</code> · โมเดล: Source → PickAndPlace → รถบน Track → PickAndPlace2 → Drain (Track และรถเหมือนขั้นที่ 1)
· ผล <strong>734 ชิ้น</strong> ใน 8 ชม. รถ 2 คัน (92 ชิ้น/ชม.)</p>

<h2>ขั้นที่ 2.1: วาง Source หุ่นยนต์ 2 ตัว และ Drain</h2>
{side_by_side(
    screenshot("assets/images/lessons/06-06.jpg", "เฟรม T02_PickAndPlace ที่มี Source, PickAndPlace, PickAndPlace2, Drain และ Display"),
    step_list([
        "<code>Source</code> ชิ้นงาน Part <code>Interval</code> 0 (มีงานพร้อมเสมอ)",
        "<code>PickAndPlace</code> ข้าง Track ด้านบน ต่อ Connector Source → PickAndPlace",
        "<code>PickAndPlace2</code> ข้าง Track ด้านล่าง",
        "<code>Drain</code> ต่อ Connector PickAndPlace2 → Drain",
        "<code>Display</code> (ข้อ 5)",
    ])
)}
<div class="tip"><strong>Connector:</strong> ไม่ต้องต่อหุ่นยนต์กับ Track การลากวางในข้อต่อไปผูกให้เอง
· วงแดงรอบหุ่นยนต์คือระยะเอื้อม ต้องวางให้วงแดงคลุม Track</div>

<h2>ขั้นที่ 2.2: ลาก PickAndPlace ไปวางบน Track เลือก Load part</h2>
{screenshot("assets/images/lessons/06-07.jpg", "ลาก PickAndPlace ไปปล่อยบน Track และหน้าต่าง Select the Operation เลือก Load part")}
{step_list([
    "กดเมาส์ค้างที่ <code>PickAndPlace</code>",
    "ลากไปปล่อย<strong>บนเส้น Track</strong> ตรงจุดที่จะให้รถจอด หน้าต่าง <code>Select the Operation</code> ขึ้น",
    "เลือก <code>Load part</code> (วางชิ้นงานขึ้นรถ)",
    "<code>OK</code>",
])}
<div class="tip"><strong>Load part:</strong> รถหยุดเองที่ sensor หุ่นยนต์วางชิ้นงานบนรถ เต็ม 6 ชิ้นแล้วรถวิ่งต่อเอง หุ่นยนต์กลับที่เดิม
· 4 ตัวเลือก: Pick part (หยิบจากราง), Unload part (เอาของลงจากรถ), Place part (วางลงราง), Load part (วางของขึ้นรถ)</div>

<h2>ขั้นที่ 2.3: ลาก PickAndPlace2 ไปวางบน Track เลือก Unload part</h2>
{screenshot("assets/images/lessons/06-08.jpg", "ลาก PickAndPlace2 ไปปล่อยบน Track ด้านล่าง และเลือก Unload part")}
{step_list([
    "ลาก <code>PickAndPlace2</code>",
    "ปล่อยบนเส้น Track ด้านล่าง",
    "<code>Unload part</code> (เอาชิ้นงานลงจากรถ)",
    "<code>OK</code> → PickAndPlace2 ส่งต่อให้ Drain ตาม Connector",
])}

<h2>ขั้นที่ 2.4: สิ่งที่ Plant Simulation สร้างให้</h2>
{screenshot("assets/images/lessons/06-09.jpg", "แท็บ Exit ของ PickAndPlace และแท็บ Controls ของ Track ปุ่ม Sensors")}
{step_list([
    "<code>PickAndPlace</code> แท็บ <code>Exit</code>",
    "<code>Load part onto MU at sensor</code>",
    "<code>Target Object</code> = Track",
    "<code>Target Sensor ID</code> = 1",
    "<code>Track</code> แท็บ <code>Controls</code>",
    "<code>Sensors (2)</code>: ID 1 ที่ 16.7 m (จุดโหลด) · ID 2 ที่ 54.1 m เรียก <code>self.OnSensor</code> ที่โปรแกรมเขียนให้",
])}
<div class="tip"><strong>การลากวางทำ 3 อย่าง:</strong> สร้าง sensor บน Track, ตั้งค่า Exit ของ PickAndPlace และ (Unload part) สร้าง OnSensor ของ Track
· PickAndPlace2 ยังเป็น Exit strategy Cyclic ส่งต่อให้ Drain ตาม Connector</div>

<h3>ขั้นที่ 2.4 (ต่อ): control ที่โปรแกรมเขียนให้ ไม่ต้องแก้</h3>
<p>Track.OnSensor ของ T02_PickAndPlace (อ่านจากไฟล์จริง ใช้อธิบายว่าเกิดอะไรขึ้น ไม่ต้องพิมพ์เอง):</p>
''' + ONSENSOR + f'''
{step_list([
    "Track &gt; คลิกขวา <code>Controls</code> &gt; <code>OnSensor</code>",
    "<code>@.stopped := true</code> รถหยุดที่ sensor 2",
    "ย้ายชิ้นงานบนรถไป PickAndPlace2 ทีละชิ้นจนรถว่าง",
    "<code>@.stopped := false</code> รถวิ่งต่อ",
])}
<div class="note"><strong>สรุป:</strong> ผู้เรียนไม่ได้เขียนโค้ดแม้แต่บรรทัดเดียว Plant Simulation สร้างให้ตอนเลือก Unload part</div>

<h2>ขั้นที่ 2.5: Display นับชิ้นงานที่ Drain</h2>
{side_by_side(
    screenshot("assets/images/lessons/06-10.jpg", "หน้าต่าง Display ตั้ง Path เป็น Drain.statNumIn และ Mode เป็น Watch"),
    step_list([
        "Toolbox แท็บ <code>User Interface</code> วาง <code>Display</code> ข้าง Drain",
        "<code>Path</code> = <code>Drain.statNumIn</code> (จำนวนชิ้นที่เข้า Drain)",
        "<code>Mode</code> = <code>Watch</code> ค่าบนจอเปลี่ยนตามเวลาจริงระหว่างรัน",
        "ค่าปัจจุบัน แสดงบนเฟรมข้าง Drain",
    ])
)}
<div class="tip"><strong>Display:</strong> ไม่ต้องต่อ Connector ใส่ Path ของค่าที่อยากดู ตัวเลขขึ้นบนเฟรมเลย ไม่ต้องเปิด Statistics</div>

<h2>ขั้นที่ 2.6: รัน 8 ชม. แล้วอ่านผล</h2>
{screenshot("assets/images/lessons/06-11.jpg", "มุมมอง 3D ระหว่างรัน และเฟรมหลังรัน 8 ชั่วโมงพร้อม Display")}
{step_list([
    "3D ระหว่างรัน: รถจอดที่ PickAndPlace หุ่นยนต์วางชิ้นงานขึ้นรถ",
    "PickAndPlace2 เอาชิ้นงานลงจากรถส่งเข้า Drain",
    "<code>Display</code> <strong>734 ชิ้น</strong>ใน 8 ชม. (92 ชิ้น/ชม.)",
    "เวลาจำลอง 8:00:00",
])}
<div class="note"><strong>คอขวด = หุ่นยนต์ตัวโหลด:</strong> PickAndPlace ทำงาน 99.9% ของเวลา (ราว 39 วินาที/ชิ้น จาก Use Kinematics for Times)
PickAndPlace2 ทำงาน 74% รถ 2 คันจึงพอ · ชวนลอง: ลดรถเหลือ 1 คัน หรือเพิ่ม Time Factor ของหุ่นยนต์</div>

<h3>ปัญหาที่พบบ่อย และวิธีแก้ (ขั้นที่ 2)</h3>
<table>
<tr><th>อาการ</th><th>วิธีแก้</th></tr>
<tr><td>ลากแล้วหุ่นยนต์ย้ายที่ ไม่มีหน้าต่างเลือก</td><td>ต้องปล่อยเมาส์บนเส้น Track พอดี</td></tr>
<tr><td>รถผ่านหุ่นยนต์ไปเฉย ๆ</td><td>เลือกผิดเป็น Place part → ลากใหม่ เลือก Load part</td></tr>
<tr><td>รถจอดนานที่จุดโหลด</td><td>รถรอจนเต็ม Load Bay 3 × 2 = 6 ชิ้น ลดขนาด Load Bay ถ้าอยากให้ออกเร็ว</td></tr>
<tr><td>มี sensor ซ้ำหลายอัน</td><td>ลากซ้ำได้ sensor ใหม่ทุกครั้ง ลบใน Track &gt; Controls &gt; Sensors</td></tr>
<tr><td>Display ขึ้น 0 ตลอด</td><td>Path ต้องเป็น <code>Drain.statNumIn</code> และ Active เปิดอยู่ ☑</td></tr>
</table>

<h2>ขั้นที่ 3: TwoLaneTrack — รถวิ่งสวนกัน 2 เลนใน 3 ข้อ</h2>
<table>
<tr><th>ข้อ</th><th>ทำอะไร</th></tr>
<tr><td>1</td><td>วาด TwoLaneTrack</td></tr>
<tr><td>2</td><td>Source ปล่อยรถเข้าแต่ละเลน</td></tr>
<tr><td>3</td><td>รันดูรถวิ่งสวนกัน</td></tr>
</table>
<p>เฟรม <code>T03_TwoLaneTrack</code> · Class Library &gt; <code>StandardObjects</code> &gt; <code>Transporters</code>
· 2 เลน: เลน A 296 m · เลน B 288 m กว้าง 5 m ขับชิดขวา</p>
<div class="tip"><strong>ใช้เมื่อไร:</strong> ทางเดียวที่รถวิ่งได้ทั้งไปและกลับคนละเลน เช่น ทางรถยกในโรงงาน ทางรถบรรทุกเข้าลานโหลด</div>

<h2>ขั้นที่ 3.1: วาด TwoLaneTrack แล้วตั้งค่าเลน</h2>
{screenshot("assets/images/lessons/06-12.jpg", "ไอคอน TwoLaneTrack ใน Toolbox เส้นทางที่วาด และหน้าต่างตั้งค่าเลน A/B")}
{step_list([
    "Toolbox ไอคอน <code>TwoLaneTrack</code> (A → / B ←) วาดแบบเดียวกับ Track (ขั้นที่ 1.2)",
    "ปลายด้านนอก = ต้นเลน B",
    "ปลายด้านใน = ต้นเลน A",
    "<code>Lane A</code> ยาว 296 m",
    "<code>Lane B</code> ยาว 288 m",
    "<code>Width</code> 5 m",
    "<code>Track Pitch</code> 2.5 m ระยะห่างเลน",
    "<code>Right-hand Traffic</code> ขับชิดขวา",
])}
<div class="tip"><strong>ทำไมเลนยาวไม่เท่ากัน:</strong> TwoLaneTrack = Track 2 เลนวิ่งสวนทางกันในวัตถุเดียว เลนหนึ่งอยู่ด้านในโค้ง
ปลายแต่ละด้านมีป้าย A / B บอกว่าเลนไหนเข้า (→) เลนไหนออก (←)</div>

<h2>ขั้นที่ 3.2: Source ปล่อยรถสำเร็จรูปเข้าแต่ละเลน</h2>
{screenshot("assets/images/lessons/06-13.jpg", "หน้าต่าง Source ปล่อย ForkliftWithHuman และ Source2 ปล่อย Truck")}
{step_list([
    "<code>Source</code> วางที่ปลายด้านใน ต่อ Connector → TwoLaneTrack (เข้าเลน A)",
    "<code>Amount</code> 1",
    "<code>MU</code> = <code>StandardObjects.Transporters.ForkliftWithHuman</code> (รถยกมีคนขับ)",
    "<code>Source2</code> วางที่ปลายด้านนอก ต่อ Connector → TwoLaneTrack (เข้าเลน B)",
    "<code>Amount</code> 1",
    "<code>MU</code> = <code>StandardObjects.Transporters.Truck</code> (รถบรรทุก ยาว 8.3 m)",
])}
<div class="tip"><strong>รถสำเร็จรูป:</strong> Class Library &gt; StandardObjects &gt; Transporters มี Forklift, ForkliftWithHuman, Truck ลากมาวางบน Source ได้เลย
ทั้ง 3 แบบ Speed 1 m/s เท่า Transporter ต่างกันที่รูปร่าง 3D และขนาด (Truck ยาว 8.3 m กว้าง 2.5 m)</div>

<h2>ขั้นที่ 3.3: รันดูรถวิ่งสวนกัน</h2>
{side_by_side(
    screenshot("assets/images/lessons/06-14.jpg", "รถยกกับรถบรรทุกวิ่งสวนกันที่โค้งด้านล่าง (ซ้าย) และที่เวลา 5:30 (ขวา)"),
    step_list([
        "ราว <strong>150 วินาที</strong> รถยกกับรถบรรทุกวิ่งสวนกันที่โค้งด้านล่าง คนละเลน ไม่ชนกัน (ภาพซ้าย)",
    ])
    + '<p>ราว 300 วินาที รถถึงปลายอีกด้าน แล้วกลับเข้าอีกเลนวิ่งย้อนกลับเอง (ภาพขวา 5:30)</p>'
    + '<p><code>EventController</code> End = 0 รันไปเรื่อย ๆ จนกด Stop</p>'
)}
<div class="tip"><strong>ทำไมไปกลับไม่หยุด:</strong> เลนยาวราว 290 m ที่ 1 m/s จึงถึงปลายราว 5 นาที ไม่มี Drain รถจึงไม่ออกจากโมเดล
· ชวนลอง: ให้ Source2 ปล่อยรถบรรทุก 2 คัน (Amount 2) แล้วดูว่ารถคันหลังต่อแถวในเลนเดียวกัน</div>

<h2>สรุป 3 เฟรม (PtS 2606)</h2>
<table>
<tr><th>เฟรม</th><th>ตั้งค่า</th><th>เวลาจำลอง</th><th>ผล</th></tr>
<tr><td>T01_Route</td><td>Track วงปิด 82.6 m · Transporter 2 คัน 1 m/s</td><td>8 ชม.</td><td>รอบละ 82.6 วินาที</td></tr>
<tr><td>T02_PickAndPlace</td><td>ลาก PickAndPlace / PickAndPlace2 วางบน Track · Display</td><td>8 ชม.</td><td>734 ชิ้น · คอขวด = หุ่นยนต์ตัวโหลด</td></tr>
<tr><td>T03_TwoLaneTrack</td><td>TwoLaneTrack 2 เลน · ForkliftWithHuman + Truck</td><td>End = 0</td><td>สวนกัน ~150 วินาที ไปกลับเอง</td></tr>
</table>
<p>ทุกตัวเลขวัดจริงด้วยไฟล์นี้ใน PtS 2606 · ไม่ต้องเขียน Method ทั้ง 3 เฟรม — ลากหุ่นยนต์วางบน Track แล้วโปรแกรมสร้าง sensor และ control ให้
TwoLaneTrack ให้รถวิ่งไปกลับคนละเลนในเส้นทางเดียว · ต่อยอด: จำนวนรถที่เหมาะ แบตเตอรี่และการชาร์จ (แท็บ Battery ของ Transporter)
และรถ AGV ใน<a href="lessons-08.html">บท 08</a></p>

<h2>ลองเอง</h2>
<table>
<tr><th>เฟรม</th><th>ลองเปลี่ยน</th><th>ดูอะไร</th></tr>
<tr><td>T01_Route</td><td>AGVSource Amount เป็น 4</td><td>ระยะห่างของรถ</td></tr>
<tr><td>T02_PickAndPlace</td><td>ลดรถเหลือ 1 คัน หรือเพิ่ม Time Factor ของหุ่นยนต์</td><td>Display ที่ 8 ชม. เทียบ 734 ชิ้น</td></tr>
<tr><td>T03_TwoLaneTrack</td><td>Source2 ปล่อยรถบรรทุก 2 คัน (Amount 2)</td><td>รถคันหลังต่อแถวในเลนเดียวกัน</td></tr>
</table>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ใน T02_PickAndPlace ได้ 734 ชิ้นใน 8 ชม. ถ้าอยากได้ชิ้นงานมากขึ้น ควรเพิ่มรถ Transporter หรือไม่?
</div>
<div class="tip"><strong>เฉลย:</strong> ไม่ช่วยมาก — คอขวดคือหุ่นยนต์ตัวโหลด PickAndPlace ที่ทำงาน 99.9% ของเวลา (ราว 39 วินาที/ชิ้น)
ส่วน PickAndPlace2 ทำงาน 74% และรถ 2 คันก็พอแล้ว ต้องแก้ที่หุ่นยนต์ตัวโหลด เช่น ปรับ Time Factor ของหุ่นยนต์
(หลักเดียวกับการหาคอขวดใน<a href="lessons-02.html">บท 02</a>)</div>
'''
