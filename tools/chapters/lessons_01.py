# -*- coding: utf-8 -*-
"""Lessons 1: Create a simple model -- from 01_Create_Simple_Model.pptx"""
from gen_site import screenshot, step_list, side_by_side

OBJECTIVES = [
    "รู้จักหน้าจอ Plant Simulation 2606 (Ribbon, Class Library, Toolbox, Frame) และใช้ Planning View ได้",
    "วาง Source → Station → Drain ต่อ Connector และตั้งค่าเวลาของแต่ละ object ได้",
    "ใส่ Display แสดงจำนวนชิ้นงาน รันจำลอง 1 ชั่วโมง แล้วอ่านผลได้",
    "บันทึกโมเดล และส่งต่อโมเดลด้วย Pack and Go ได้",
]

BODY = f'''
<p class="lead" style="max-width:46em;">สร้างโมเดลแรกของตัวเอง <code>Source → Station → Drain</code> ทีละขั้น 6 ขั้นตอน ตั้งแต่เปิดไฟล์
รู้จักหน้าจอ วาง object และต่อเส้น ตั้งค่า ใส่ตัวเลขด้วย Display จนถึงกด Run อ่านผล และบันทึกไฟล์
(บทถัดไป <a href="lessons-02.html">บท 02</a> ต่อยอดเป็นไลน์ 5 สถานีและหาคอขวด)</p>

<h2>ภาพรวม: 6 ขั้น ตั้งแต่เปิดไฟล์ถึงอ่านผล</h2>
<table>
<tr><th>ขั้น</th><th>หัวข้อ</th><th>ทำอะไร</th></tr>
<tr><td>1</td><td>เปิดไฟล์</td><td>Start Page › Open Model File</td></tr>
<tr><td>2</td><td>รู้จักหน้าจอ</td><td>Class Library, Toolbox, Frame, Planning View</td></tr>
<tr><td>3</td><td>วาง object + ต่อเส้น</td><td>Source → Station → Drain ด้วย Connector</td></tr>
<tr><td>4</td><td>ตั้งค่า</td><td>Source, Station, EventController</td></tr>
<tr><td>5</td><td>ใส่ตัวเลขด้วย Display</td><td>แสดงจำนวนชิ้นงานบน Frame</td></tr>
<tr><td>6</td><td>กด Run อ่านผล</td><td>จำลอง 1 ชั่วโมง แล้วลองเปลี่ยนค่า</td></tr>
</table>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 และไฟล์ <code>01_Create_Simple_Model.spp</code> (Frame อยู่ที่ Class Library › Models › Model)
&nbsp;·&nbsp; ผลจำลอง 1 ชั่วโมง: <strong>359 ชิ้น</strong> (เวลาผลิต 10 วินาทีต่อชิ้น ชิ้นงานอยู่ในกระบวนการ 1 ชิ้น)
</div>
<div class="note">
<strong>ข้อควรจำ:</strong> Plant Simulation 2606 ทำงานแบบ 3D อย่างเดียว ถ้าอยากมองแบบแปลนให้ใช้ <strong>Planning View</strong>
(ภาพ Frame ในบทนี้ใช้ Planning View เกือบทุกภาพ)
</div>

<h2>ทุกโมเดลทำ 5 ขั้นเหมือนกัน</h2>
<table>
<tr><th>ลำดับ</th><th>งาน</th><th>ทำอย่างไร</th><th>ดูที่</th></tr>
<tr><td>1</td><td>วาง object</td><td>เลือกจาก Toolbox แล้วคลิกลงใน Frame</td><td>ขั้นที่ 3</td></tr>
<tr><td>2</td><td>ต่อเส้น</td><td>Connector บอกทางเดินของชิ้นงาน</td><td>ขั้นที่ 3</td></tr>
<tr><td>3</td><td>ตั้งค่า</td><td>ดับเบิลคลิก object ใส่เวลา</td><td>ขั้นที่ 4</td></tr>
<tr><td>4</td><td>ใส่ตัวเลข</td><td>Display แสดงค่าบน Frame</td><td>ขั้นที่ 5</td></tr>
<tr><td>5</td><td>Run + อ่านผล</td><td>EventController: Reset แล้ว Start</td><td>ขั้นที่ 6</td></tr>
</table>
<p>บท 01 ในตัวเลข: <strong>1</strong> Frame (<code>.Models.Model</code>) · <strong>6</strong> object ในโมเดล · <strong>2</strong> Connector ·
<strong>60</strong> นาทีจำลองต่อการรัน</p>

<h2>ขั้นที่ 1: หน้า Start Page เมื่อเปิดโปรแกรม</h2>
{side_by_side(
    screenshot("assets/images/lessons/01-01.jpg", "หน้า Start Page ของ Plant Simulation 2606"),
    step_list([
        "<strong>Open Model File</strong> — เปิดไฟล์ <code>01_Create_Simple_Model.spp</code>",
        "<strong>Recent Models</strong> — ไฟล์ที่เปิดล่าสุด",
        "<strong>Create New Model</strong> — สร้างโมเดลใหม่ว่างๆ เมื่อจะสร้างเอง",
        '<strong>Example Models</strong> — ตัวอย่างโมเดลจาก Siemens (ดู <a href="overview-02.html">Factory 51</a> และ <a href="overview-03.html">Small Parts Production</a>)',
    ])
)}
<div class="tip"><strong>ทางลัด:</strong> <strong>Load Last Model</strong> (ช่องบนซ้าย) เปิดไฟล์ที่ใช้ครั้งก่อนได้ในคลิกเดียว ชื่อไฟล์แสดงอยู่บนช่อง</div>

<h2>ขั้นที่ 2: ส่วนต่างๆ ของหน้าจอ</h2>
{screenshot("assets/images/lessons/01-02.jpg", "หน้าจอหลักของ Plant Simulation 2606 เมื่อเปิด Frame Model")}
{step_list([
    "<strong>Ribbon</strong> — ปุ่มคำสั่ง กลุ่ม Event Controller ใช้ Run / Reset",
    "<strong>Class Library</strong> — คลังทุก object และโมเดล เปิด <code>Models › Model</code>",
    "<strong>Toolbox</strong> — ไอคอน object พร้อมวาง",
    "<strong>Frame</strong> — พื้นที่วางโมเดล (ภาพนี้เป็น Planning View)",
    "<strong>แท็บ Frame</strong> — Frame ที่เปิดอยู่ สลับไปมาได้",
])}
<div class="note"><strong>วิธีเปิด Frame:</strong> ใน Class Library ดับเบิลคลิก <code>Models › Model</code></div>

<h2>ขั้นที่ 2: มองโมเดลแบบแปลนด้วย Planning View</h2>
<p>Ribbon › <code>3D</code> › <code>View</code></p>
{screenshot("assets/images/lessons/01-03.jpg", "Ribbon แท็บ 3D › View: Planning View, Names, Connections และ View All")}
{step_list([
    "<strong>View</strong> — แท็บใต้หัวข้อ 3D (สีน้ำเงินเข้ม)",
    "<strong>Planning View</strong> — มองจากด้านบน เหมือนแปลนโรงงาน",
    "<strong>Names</strong> — แสดงชื่อ object",
    "<strong>Connections</strong> — แสดงเส้นเชื่อมและทิศทาง",
    "<strong>View All</strong> — ซูมให้เห็นทั้งโมเดล",
])}
<div class="note"><strong>ไฟล์นี้ปิดชื่อ object ไว้:</strong> ถ้ากด Names แล้วยังไม่เห็นชื่อ ให้คลิกขวาที่ object ›
<code>Edit 3D Properties</code> › แท็บ <code>Captions</code> › คลิกช่อง <code>Name/Label Activated</code> ให้ขึ้นเครื่องหมายถูก ☑ = แสดงชื่อ</div>

<h2>ขั้นที่ 3: object ที่ใช้ใน Toolbox (แท็บ Material Flow)</h2>
{screenshot("assets/images/lessons/01-04.jpg", "Toolbox แท็บ Material Flow")}
{step_list([
    "<strong>Connector</strong> — ต่อเส้นระหว่าง object",
    "<strong>EventController</strong> — นาฬิกา (1 ตัวต่อ Frame)",
    "<strong>Source</strong> — ปล่อยชิ้นงาน",
    "<strong>Drain</strong> — รับชิ้นงานออก",
    "<strong>Station</strong> — เครื่องจักร ทำทีละ 1 ชิ้น",
])}
<div class="tip"><strong>วิธีวาง / ต่อเส้น:</strong> คลิกไอคอนใน Toolbox แล้วคลิกในพื้นที่ Frame ·
ต่อเส้น: คลิก Connector แล้วคลิก object ต้นทาง → ปลายทาง</div>

<h2>ขั้นที่ 3: โมเดลแรก Source → Station → Drain</h2>
{side_by_side(
    screenshot("assets/images/lessons/01-05.jpg", "โมเดลแรกใน Frame .Models.Model"),
    step_list([
        "<strong>Source</strong> — ปล่อยชิ้นงานเข้าระบบ",
        "<strong>Connector</strong> — เส้นลูกศร บอกทางเดินชิ้นงาน",
        "<strong>Station</strong> — เครื่องจักร ทำทีละ 1 ชิ้น",
        "<strong>Drain</strong> — ชิ้นงานออกจากระบบ",
        "<strong>EventController</strong> — นาฬิกาควบคุมการจำลอง",
        "<strong>Display</strong> — ป้ายแสดงตัวเลข (ขั้นที่ 5)",
    ])
)}
<div class="note"><strong>ทิศทาง:</strong> ชิ้นงานเดินตามหัวลูกศรของ Connector: Source → Station → Drain</div>

<h2>ขั้นที่ 4: ตั้งค่า Source</h2>
<p>ดับเบิลคลิก Source</p>
{side_by_side(
    screenshot("assets/images/lessons/01-06.jpg", "หน้าต่างตั้งค่า Source"),
    step_list([
        "<strong>Blocking</strong> — มีเครื่องหมายถูก ☑ = ถ้าทางข้างหน้าเต็ม Source จะรอ",
        "<strong>Time of Creation</strong> — <code>Interval Adjustable</code> = ปล่อยตามช่วงเวลา",
        "<strong>Interval = 0</strong> — ปล่อยชิ้นใหม่ทันทีที่ Station ว่าง",
        "<strong>MU</strong> — ชนิดชิ้นงานที่ปล่อย (<code>*.MUs.Part</code>)",
    ])
)}
<div class="note"><strong>ข้อควรจำ:</strong> ดับเบิลคลิก object ใดก็ได้เพื่อเปิดหน้าต่างตั้งค่า แก้แล้วกด <code>Apply</code> หรือ <code>OK</code></div>

<h2>ขั้นที่ 4: ตั้งเวลาทำงานของ Station</h2>
<p>ดับเบิลคลิก Station</p>
{side_by_side(
    screenshot("assets/images/lessons/01-07.jpg", "หน้าต่างตั้งค่า Station แท็บ Times"),
    step_list([
        "<strong>Processing Time = 0:10</strong> — ทำ 1 ชิ้นใช้ 10 วินาที",
        "<strong>Const</strong> — เวลาเท่ากันทุกชิ้น",
        "<strong>Set-up Time</strong> — เวลาเปลี่ยนรุ่น (ยังไม่ใช้ = 0)",
        "<strong>OK</strong> — บันทึกแล้วปิดหน้าต่าง",
    ])
)}
<div class="tip"><strong>รูปแบบเวลา:</strong> ชม:นาที:วินาที เช่น <code>0:10</code> = 10 วินาที, <code>1:00</code> = 1 นาที, <code>1:00:00</code> = 1 ชั่วโมง</div>

<h2>ขั้นที่ 4: ตั้งเวลาจำลอง แล้วกด Run</h2>
<p>ดับเบิลคลิก EventController</p>
{screenshot("assets/images/lessons/01-08.jpg", "หน้าต่าง EventController แท็บ Settings และแท็บ Controls")}
{step_list([
    "<strong>Settings</strong> — แท็บตั้งค่าเวลา",
    "<strong>End Time = 1:00:00</strong> — จำลอง 1 ชั่วโมงแล้วหยุดเอง",
    "<strong>Reset</strong> (ปุ่มแดง) — ล้างผลเก่า กดก่อนรันใหม่ทุกครั้ง",
    "<strong>Start</strong> (ปุ่มเขียว) — เริ่มจำลอง ปุ่มเดียวกันมีใน Ribbon › Home",
    "<strong>Slower – Faster</strong> — ปรับความเร็วของภาพเคลื่อนไหว",
])}
<div class="note"><strong>ระวัง:</strong> ถ้าไม่กด Reset ก่อน Start การจำลองจะเดินต่อจากเวลาเดิม</div>

<h2>ขั้นที่ 5: วาง Display เพื่อแสดงตัวเลขบน Frame</h2>
<p>Toolbox › <code>User Interface</code></p>
{screenshot("assets/images/lessons/01-09.jpg", "Toolbox แท็บ User Interface และไอคอน Display")}
{side_by_side(
    screenshot("assets/images/lessons/01-10.jpg", "Display ที่วางไว้ใต้ Drain แสดงเลข 0"),
    screenshot("assets/images/lessons/01-11.jpg", "Display ที่วางใหม่เมื่อมองในมุมมอง 3D"),
)}
{step_list([
    "Toolbox คลิกแท็บ <strong>User Interface</strong>",
    "คลิกไอคอน <strong>Display</strong> (รูปตัวเลข 9.86) แล้วคลิกวางใน Frame",
    "ในไฟล์นี้วางไว้ใต้ <strong>Drain</strong> ก่อนรันแสดงเลข 0",
])}
<div class="tip"><strong>ไอคอนข้างเคียง:</strong> Comment (รูปกระดาษเหลือง) ใช้เขียนข้อความบน Frame · Chart (รูปกราฟแท่ง) ใช้ทำกราฟ</div>

<h2>ขั้นที่ 5: บอก Display ว่าจะแสดงค่าอะไร</h2>
<p>ดับเบิลคลิก Display › แท็บ <code>Data</code></p>
{side_by_side(
    screenshot("assets/images/lessons/01-12.jpg", "หน้าต่าง Display แท็บ Data"),
    step_list([
        "<strong>Path = <code>Drain.statNumIn</code></strong> — จำนวนชิ้นที่เข้า Drain (ชิ้นงานที่เสร็จ)",
        "<strong>Mode = Watch</strong> — เฝ้าดูค่า อัปเดตเองระหว่างรัน",
        "<strong>Value</strong> — ค่าตอนนี้ (ก่อนรัน = 0)",
        "<strong>Active</strong> — มีเครื่องหมายถูก ☑ = Display ทำงาน",
    ])
)}
<div class="tip"><strong>ลองเอง:</strong> เปลี่ยน Path เป็น <code>Source.statNumOut</code> จะเห็นจำนวนชิ้นที่ Source ปล่อยออกมา</div>

<h2>ขั้นที่ 5: ปรับหน้าตาตัวเลข</h2>
<p>ดับเบิลคลิก Display › แท็บ <code>Display</code></p>
{side_by_side(
    screenshot("assets/images/lessons/01-13.jpg", "หน้าต่าง Display แท็บ Display"),
    step_list([
        "<strong>Type = Text</strong> — แสดงเป็นตัวเลข",
        "<strong>Color</strong> — สีของตัวเลข",
        "<strong>Font Size = Small</strong> — ขนาดตัวเลข",
        "<strong>Decimal Places</strong> — จำนวนทศนิยม (ไฟล์นี้ = -1)",
    ])
)}
<div class="note"><strong>อีกแบบ:</strong> <code>Type › Bar</code> แสดงเป็นแท่งแทนตัวเลข (ตามคู่มือ Plant Simulation)</div>

<h2>ขั้นที่ 6: อ่านผลหลังจำลอง 1 ชั่วโมง</h2>
{screenshot("assets/images/lessons/01-14.jpg", "Display ก่อนรันและหลังรัน 1 ชั่วโมง และแถบสถานะมุมขวาล่าง (ขยาย)")}
{step_list([
    "<strong>ก่อนรัน</strong> — Display = 0",
    "<strong>หลังรัน Display = 359</strong> — ชิ้นงานที่เสร็จใน 1 ชั่วโมง",
    "<strong>1:00:00.0000</strong> — เวลาจำลองที่มุมขวาล่างของหน้าต่าง ครบแล้วหยุดเอง",
])}
<div class="note"><strong>ทำไมไม่ใช่ 360:</strong> Source ปล่อย 360 ชิ้น แต่ชิ้นสุดท้ายยังอยู่ใน Station ตอนหมดเวลา</div>

<h2>ขั้นที่ 6: ลองเปลี่ยนค่า แล้วดูตัวเลขใน Display</h2>
<table>
<tr><th>ลองเปลี่ยน</th><th>แก้ที่</th><th>Display หลังรัน</th><th>ทำไม</th></tr>
<tr><td>ค่าเดิมในไฟล์</td><td>–</td><td><strong>359</strong></td><td>3600 ÷ 10 = 360 ลบ 1 ชิ้นที่ค้าง</td></tr>
<tr><td>Processing Time = 0:20</td><td>Station</td><td><strong>179</strong></td><td>ช้าลง 2 เท่า ได้ครึ่งเดียว</td></tr>
<tr><td>Processing Time = 0:05</td><td>Station</td><td><strong>719</strong></td><td>เร็วขึ้น 2 เท่า ได้เท่าตัว</td></tr>
<tr><td>Interval = 0:12</td><td>Source</td><td><strong>300</strong></td><td>งานเข้าช้ากว่าที่เครื่องทำได้ · Station ทำงาน 83%</td></tr>
<tr><td>End Time = 8:00:00</td><td>EventController</td><td><strong>2879</strong></td><td>8 ชม. × 360 ลบ 1</td></tr>
</table>
<p>วัดจริงใน Plant Simulation 2606 ด้วยไฟล์นี้ แก้ทีละค่าจากค่าเดิม · กด Reset ก่อน Start ทุกครั้ง</p>

<h2>ขั้นที่ 6: บันทึกโมเดล (Save) และ Pack and Go</h2>
{screenshot("assets/images/lessons/01-15.jpg", "เมนู File › Save, ไฟล์สำรอง .bak และ File › Share › Pack and Go")}
<ul>
<li><strong>ภาพซ้าย:</strong> <code>File › Save</code> (Save Model File) บันทึกโมเดลทับชื่อเดิม · <code>Save As</code> บันทึกเป็นชื่อใหม่</li>
<li><strong>ภาพกลาง:</strong> หลังบันทึก จะมีไฟล์สำรอง (Backup file) เกิดขึ้นคู่กัน เช่น <code>New Model.spp</code> กับ <code>New Model.spp.bak</code></li>
<li><strong>ภาพขวา:</strong> <code>File › Share › Pack and Go</code> สร้างไฟล์ .exe แบบแตกไฟล์เองได้ (self-extracting executable)
ที่รวมโมเดลและทุกไฟล์ที่ต้องใช้เปิดโมเดลใน Plant Simulation เช่น <code>New Model.spp</code> (3,664 KB) ได้ <code>New Model.exe</code> (33,469 KB)</li>
</ul>

<h2>สรุป object ในโมเดลนี้</h2>
<table>
<tr><th>Object</th><th>ใช้ทำอะไร</th><th>ค่าในไฟล์นี้</th></tr>
<tr><td><strong>Source</strong></td><td>ปล่อยชิ้นงานเข้าระบบ</td><td>Interval 0, Blocking, MU = Part</td></tr>
<tr><td><strong>Station</strong></td><td>เครื่องจักรทำทีละ 1 ชิ้น</td><td>Processing Time 0:10</td></tr>
<tr><td><strong>Drain</strong></td><td>ชิ้นงานออกจากระบบ</td><td>นับจำนวนชิ้นที่เสร็จ</td></tr>
<tr><td><strong>Connector × 2</strong></td><td>ทางเดินชิ้นงาน</td><td>Source → Station → Drain</td></tr>
<tr><td><strong>EventController</strong></td><td>นาฬิกาควบคุมการจำลอง</td><td>End Time 1:00:00</td></tr>
<tr><td><strong>Display</strong></td><td>แสดงตัวเลขบน Frame</td><td>Path Drain.statNumIn, Type Text</td></tr>
</table>

<h2>ปัญหาที่พบบ่อย และวิธีแก้</h2>
<table>
<tr><th>อาการ</th><th>วิธีแก้</th></tr>
<tr><td>โมเดลเอียงเป็น 3D มองเส้นไม่ชัด</td><td><code>View › Planning View</code> แล้ว <code>View All</code></td></tr>
<tr><td>ไม่เห็นชื่อ object</td><td><code>View › Names</code> (ถ้ายังไม่ขึ้น: Edit 3D Properties › Captions › Name/Label Activated)</td></tr>
<tr><td>Display ยังเป็น 0 หลังรัน</td><td>ตรวจ Path = <code>Drain.statNumIn</code>, Active ต้องมีเครื่องหมายถูก ☑ และต่อ Connector ถึง Drain</td></tr>
<tr><td>กด Start แล้วผลไม่เริ่มจากศูนย์</td><td>กด Reset (ปุ่มแดง) ก่อน Start ทุกครั้ง</td></tr>
<tr><td>รันไปเรื่อยๆ ไม่หยุด</td><td>EventController › Settings › ใส่ End Time เช่น <code>1:00:00</code></td></tr>
<tr><td>เปิด Names แล้วตัวเลขทับชื่อ Drain</td><td>ลาก Display ลงไปข้างล่างอีกเล็กน้อย</td></tr>
</table>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ในตารางลองเปลี่ยนค่า ถ้าตั้ง Source Interval = 0:12 Display ได้ 300 ชิ้น และ Station ทำงานแค่ 83% — ทำไม Station ถึงไม่ได้ทำงานเต็มเวลา?
</div>
<div class="tip"><strong>เฉลย:</strong> Source ปล่อยงาน 1 ชิ้นทุก 12 วินาที (3600 ÷ 12 = 300 ชิ้น) แต่ Station ทำเสร็จใน 10 วินาที
จึงว่างรองานชิ้นต่อไป 2 ใน 12 วินาที (10 ÷ 12 ≈ 83%) ครั้งนี้ตัวที่จำกัดผลผลิตคือ Source ไม่ใช่ Station —
การหาว่าอะไรจำกัดผลผลิตของไลน์ (คอขวด) คือหัวข้อของ<a href="lessons-02.html">บท 02</a></div>
'''
