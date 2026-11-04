# -*- coding: utf-8 -*-
"""Overview 2: Example Models - Factory 51 -- from PtS2606_1_Factory51.pptx"""
from gen_site import screenshot, step_list, side_by_side

OBJECTIVES = [
    "เปิด Start Page และเปิดโมเดลตัวอย่าง Factory 51 ได้ด้วยตัวเอง",
    "ซูม เลื่อน หมุนมุมมอง 3D และโต้ตอบกับวัตถุด้วยคลิก / ดับเบิลคลิก / คลิกขวาได้",
    "เปิด Frame ด้านในแล้วกลับออกมา และสั่ง Start / Reset / ปรับความเร็วผ่าน EventController ได้",
]

BODY = f'''
<p class="lead" style="max-width:46em;">โมเดลตัวอย่างตัวแรก — ยังไม่ต้องสร้างอะไรเอง แค่เปิดโรงงานตัวอย่าง <strong>Factory 51</strong>
ที่ติดมากับโปรแกรม เพื่อฝึกใช้หน้าจอ ควบคุมมุมมอง 3D โต้ตอบกับวัตถุ และสั่งรันซิมูเลชัน ทั้งหมด 7 ขั้นตอน
(ถ้ายังไม่รู้ว่า Plant Simulation และ DES คืออะไร อ่าน <a href="overview-01.html">บทนำ</a> ก่อน)
แล้วต่อด้วยโมเดลตัวอย่างตัวที่สอง <a href="overview-03.html">Small Parts Production</a></p>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 และโมเดล <code>Factory51.spp</code> (อยู่ใน <code>Examples\\Demo</code> ของโฟลเดอร์ติดตั้ง)
— ใช้ Student License ได้ โดยเปิดแบบ Viewer &nbsp;·&nbsp; ผลที่วัดได้ใน 2606: มีรถบรรทุกเข้ามา <strong>5 คัน</strong> ภายในเวลาจำลอง 48:40 นาที
</div>

<h2>ภาพรวม 7 ขั้นตอน</h2>
<table>
<tr><th>ขั้น</th><th>หัวข้อ</th><th>ทำอะไร</th></tr>
<tr><td>1</td><td>เปิด Start Page</td><td><code>Window → Start Page</code></td></tr>
<tr><td>2</td><td>Example Models</td><td>เลือก Factory 51</td></tr>
<tr><td>3</td><td>รู้จักโรงงาน</td><td>รับของ ผลิต คลัง ส่งของ</td></tr>
<tr><td>4</td><td>ควบคุมมุมมอง 3D</td><td>ซูม เลื่อน หมุน</td></tr>
<tr><td>5</td><td>คลิก / ดับเบิลคลิก / คลิกขวา</td><td>เลือกวัตถุ เปิดหน้าต่าง และ Quick tools</td></tr>
<tr><td>6</td><td>เปิด Frame ด้านใน</td><td>เข้า-ออก Frame P1</td></tr>
<tr><td>7</td><td>EventController</td><td>Start / Reset / ความเร็ว</td></tr>
</table>
<div class="note"><strong>แบบฝึก:</strong> ท้ายบทให้ลองหา "Beer room" ที่ซ่อนอยู่ในโรงงาน เพื่อฝึกซูม เลื่อน และหมุนมุมมอง</div>

<h2>ขั้นที่ 1: เปิด Start Page</h2>
{side_by_side(
    screenshot("assets/images/overview/02-01.jpg", "แท็บ Window และหน้า Start Page ของ Plant Simulation 2606"),
    step_list([
        "เปิด Plant Simulation 2606 แล้วคลิกแท็บ <code>Window</code>",
        "คลิก <code>Start Page</code> (ปกติจะขึ้นเองตอนเปิดโปรแกรม)",
        "ในกลุ่ม <code>Getting Started</code> คลิก <code>Example Models</code>",
    ])
)}
<div class="note">
<strong>Start Page:</strong> มีปุ่ม <strong>Load Last Model</strong>, <strong>Recent Models</strong> และ <strong>Open Model File</strong> —
ถ้าไม่เห็นปุ่ม <strong>Create New Model</strong> แสดงว่ายังมีโมเดลอื่นเปิดค้างอยู่ &nbsp;·&nbsp; Plant Simulation 2606 เพิ่มปุ่ม
<strong>QuickStart</strong> และ <strong>New Features</strong> เข้ามาใหม่
</div>

<h2>ขั้นที่ 2: เปิดโมเดลตัวอย่าง Factory 51</h2>
{side_by_side(
    screenshot("assets/images/overview/02-02.jpg", "หน้าต่าง Example Models"),
    screenshot("assets/images/overview/02-03.jpg", "โมเดล Factory 51 ที่เปิดแล้วในหน้าต่าง 3D")
)}
{step_list([
    "คลิก <code>Factory 51</code> ในหน้าต่าง Example Models",
    "โมเดลจะอยู่ใน Class Library → <code>Models → Factory51</code>",
    "แถบ <em>The model contains outdated libraries</em> กด <code>X</code> ปิดได้ บทนี้ไม่ต้องอัปเดต",
    "โมเดลเปิดในหน้าต่าง 3D (แท็บล่างชื่อ <code>3D.Models.Factory51</code>)",
    '2606 มีตัวอย่างเพิ่ม เช่น <strong>Python GA Demo</strong> (ดู<a href="overview-04.html">บท Python GA Demo</a>) และ <strong>Standard Object Examples</strong>',
])}
<div class="note">
<strong>Student License:</strong> โมเดล Factory 51 มีวัตถุเกิน 80 ตัว โปรแกรมจะถาม — กด <code>Yes</code> เพื่อเปิดแบบ <strong>Viewer</strong>
(ดูและรันได้ แต่บันทึกการแก้ไขไม่ได้)
</div>

<h3>Factory 51 — Overview</h3>
{screenshot("assets/images/overview/02-04.jpg", "ภาพรวมโซนต่างๆ ในโมเดล Factory 51", caption="Factory 51 — Overview: รับของ (Inbound) → ผลิต (P1 &amp; P2) → AGV / Robot Auto Packing → คลัง (Warehouse) → ส่งของ (Outbound)")}

<h2>ขั้นที่ 3: รู้จัก Factory 51 — ระบบทั้งโรงงานใน 3D</h2>
{side_by_side(
    screenshot("assets/images/overview/02-05.jpg", "ตำแหน่งของแต่ละโซนใน Factory 51"),
    step_list([
        "<strong>Inbound</strong> — รถบรรทุก โฟล์คลิฟต์ หุ่นยนต์ เครน",
        "<strong>P1 / P2</strong> — โรงผลิต: ขัด กัด พ่นสี อบ ล้าง QC แพ็ก (Polishing, Milling, Paint, Drying, Clean, QC, PostProcess, Pack)",
        "<strong>AGV</strong> — ขนส่งด้วย AGV + จุดชาร์จ (AGV Load/Unload, AGV Charger, Robot Auto Packing)",
        "<strong>คลัง HBW</strong> — คลังสินค้าอัตโนมัติ (ASRS, WMS)",
        "<strong>Outbound</strong> — สายพาน + รถบรรทุกส่งของ",
    ])
)}

<h2>ขั้นที่ 4: ควบคุมมุมมอง 3D ด้วยเมาส์</h2>
{side_by_side(
    screenshot("assets/images/overview/02-06.jpg", "มุมมองเริ่มต้น เทียบกับหลังซูม เลื่อน และหมุน"),
    step_list([
        "<strong>หมุนล้อเมาส์</strong> = ซูมเข้า-ออก (<code>Shift</code> เร็ว ×10, <code>Ctrl</code> ช้า ×0.1)",
        "<strong>คลิกขวาค้างแล้วลาก</strong> = เลื่อนฉาก (Pan) — หรือกดล้อค้างแล้วลาก",
        "<code>Ctrl</code> + <strong>คลิกขวาค้างแล้วลาก</strong> = หมุนฉาก — หรือกดซ้าย+ขวาค้าง",
        "กด <code>V</code> = View All เห็นทั้งฉาก",
    ])
)}
<div class="note">
<strong>ระวัง:</strong> ลากหมุนนิดเดียวพอ ถ้าหมุนจนมุมเพี้ยน กด <code>V</code> จะไม่คืนมุมกล้อง — ให้ใช้แท็บ <code>View</code>
(<code>From Top</code> / <code>Front</code>) หรือเปิดโมเดลใหม่
</div>

<h3>ควบคุมฉากด้วยเมาส์และคีย์บอร์ด</h3>
{screenshot("assets/images/overview/02-07.jpg", "การควบคุมฉาก 3D ด้วยเมาส์และคีย์บอร์ด", caption="ป้าย Hold Wheel - Rotate ในภาพมาจากเวอร์ชันก่อน — ใน 2606 กดล้อค้าง = เลื่อน และ Ctrl + คลิกขวาค้าง = หมุน ตามขั้นที่ 4 · ปุ่ม View All (V) อยู่ในแท็บ View กลุ่ม Scene")}
<table>
<tr><th>ปุ่ม</th><th>ผลลัพธ์</th></tr>
<tr><td><code>W</code> / <code>S</code></td><td>เดินเข้าใกล้ / ถอยออกจากวัตถุในหน้าต่าง 3D</td></tr>
<tr><td><code>Q</code> / <code>E</code></td><td>เดินไปทางซ้าย / ทางขวา</td></tr>
<tr><td><code>A</code> / <code>D</code></td><td>หันซ้าย / หันขวา</td></tr>
<tr><td><code>Z</code> / <code>Shift + Z</code></td><td>ลดระดับตัวเองลง / ยกตัวเองขึ้น</td></tr>
</table>
<p>การหมุนมี 2 แบบ: <strong>Rotate around center of the scene</strong> (หมุนรอบกลางฉาก) และ <strong>Rotate around object</strong> (หมุนรอบวัตถุ)</p>

<h3>Object Windows, Open Frame และ Quick tools</h3>
{screenshot("assets/images/overview/02-08.jpg", "คลิกเลือกวัตถุ ดับเบิลคลิกเปิดหน้าต่าง ดับเบิลคลิกเปิด Frame และคลิกขวาเปิด Quick tools")}
<table>
<tr><th>เมาส์</th><th>ผลลัพธ์</th></tr>
<tr><td>Click</td><td>Select Object — เลือกวัตถุ</td></tr>
<tr><td>Double Click (วัตถุทั่วไป)</td><td>Object Windows — เปิดหน้าต่างตั้งค่าของวัตถุ</td></tr>
<tr><td>Double Click (วัตถุที่เป็น Frame)</td><td>Open Frame inside — เปิด Frame ด้านใน (กลับด้วย <code>Shift + Enter</code>)</td></tr>
<tr><td>Right Click</td><td>Open Quick tools — แถบปุ่มและเมนูลัด</td></tr>
</table>

<h3>Time-Oriented กับ Event-Controlled Simulation</h3>
<p>Plant Simulation เป็นโปรแกรมจำลองแบบ <strong>discrete, event-controlled</strong> — โปรแกรมตรวจสอบเฉพาะ
"จุดเวลาที่มีเหตุการณ์เกิดขึ้น" ในโมเดลเท่านั้น ไม่ได้คำนวณทุกช่วงเวลาต่อเนื่องแบบ Time-oriented
และควบคุมการรันผ่านวัตถุ <strong>EventController</strong> (รายละเอียดในขั้นที่ 7)</p>
{screenshot("assets/images/overview/02-09.jpg", "ปุ่ม Start/Stop Simulation, นาฬิกา EventController และหน้าต่าง EventController ใน Factory 51")}
{step_list([
    "<code>Start/Stop Simulation</code> — ปุ่มในฉาก เริ่ม / หยุด",
    "ดับเบิลคลิกนาฬิกา = Open EventController",
    "แถบ <code>Slower</code> / <code>Faster</code> ในหน้าต่าง EventController",
])}

<h2>ขั้นที่ 5: คลิก ดับเบิลคลิก และคลิกขวาที่วัตถุ</h2>
{screenshot("assets/images/overview/02-10.jpg", "คลิกเลือกสายพาน Line10, หน้าต่างของวัตถุ และเมนู Quick tools")}
{step_list([
    "<strong>คลิก</strong> = เลือกวัตถุ (ขึ้นสีเหลือง) — ในภาพคือสายพาน <code>Line10</code>",
    "<strong>ดับเบิลคลิก</strong> = เปิดหน้าต่างของวัตถุ (ตั้งค่า เวลา เสีย ฯลฯ)",
    "<strong>คลิกขวา</strong> = Quick tools: แถบปุ่ม Start / Stop / Reset ด้านบน",
    "เมนูลัด เช่น <code>Open</code> (Enter), <code>Show Statistics Report</code> (F6), <code>Show Attributes and Methods</code> (F8)",
])}

<h2>ขั้นที่ 6: เปิด Frame ด้านใน และกลับออกมา</h2>
{screenshot("assets/images/overview/02-11.jpg", "เปิด Frame P1 และเมนู Open Location")}
{step_list([
    "<strong>ดับเบิลคลิก</strong> วัตถุในโรงผลิต (เช่นบูธขัดผิวใน P1) → เปิด Frame <code>P1</code> แยกออกมา",
    "แท็บล่างเปลี่ยนเป็น <code>3D.Models.Factory51.P1</code>",
    "กลับ Frame หลัก: <code>Shift + Enter</code> หรือคลิกขวาที่ว่าง → <code>Open Location</code>",
    "<code>Backspace</code> = Previous Scene (มุมมองก่อนหน้า)",
])}

<h2>ขั้นที่ 7: EventController — เริ่ม หยุด รีเซ็ต และความเร็ว</h2>
{side_by_side(
    screenshot("assets/images/overview/02-12.jpg", "ปุ่ม Start/Stop Simulation, Reset Simulation และนาฬิกา EventController ในฉาก"),
    screenshot("assets/images/overview/02-13.jpg", "หน้าต่าง EventController ที่เวลา 48:40")
)}
{step_list([
    "คลิก <code>Start/Stop Simulation</code> (ปุ่มในฉาก) เพื่อเริ่ม / หยุด",
    "<code>Reset Simulation</code> = เวลากลับไป 0",
    "ดับเบิลคลิกนาฬิกา <strong>EventController</strong>",
    "<code>Time</code> = เวลาจำลองตอนนี้ (48:40)",
    "แถบ <code>Slower</code> / <code>Faster</code> ปรับความเร็ว",
    "<code>Real-time × 3</code> = เร็วกว่าเวลาจริง 3 เท่า",
])}

<h2>แบบฝึก: หา Beer room ใน Factory 51</h2>
<p>ฝึกซูม เลื่อน และหมุนมุมมองให้คล่อง — ในโรงงานมีห้องเล็กๆ ซ่อนอยู่ ลองหาเองก่อนแล้วค่อยดูเฉลย</p>
<details>
<summary>ดูเฉลย</summary>
{side_by_side(
    screenshot("assets/images/overview/02-14.jpg", "โรงผลิต P1 มองจากด้านบน ตำแหน่งใต้ชั้นลอย"),
    screenshot("assets/images/overview/02-15.jpg", "ซูมเข้าใกล้ ประตู Beer อยู่ข้างห้อง Bathroom")
)}
{step_list([
    "ซูมเข้าโรงผลิต P1 มองใต้ชั้นลอย (แถวป้าย Maintenance / Bathroom)",
    "ประตู <strong>Beer</strong> อยู่ข้างห้อง Bathroom",
])}
</details>

<h2>ปัญหาที่พบบ่อย และสิ่งที่ต่างใน 2606</h2>
<table>
<tr><th>อาการ / จุดที่ต่าง</th><th>วิธีแก้ / คำอธิบาย</th></tr>
<tr><td>Student License: เกิน 80 objects</td><td>กด <code>Yes</code> เพื่อเปิดแบบ Viewer (ดูและรันได้ แต่บันทึกการแก้ไขไม่ได้)</td></tr>
<tr><td>กดล้อค้างแล้วไม่หมุน</td><td>2606: <code>Ctrl</code> + คลิกขวาค้างลาก = หมุน, กดล้อค้าง = เลื่อน</td></tr>
<tr><td>หมุนจนมุมกล้องเพี้ยน</td><td>กด <code>V</code> ไม่คืนมุม → แท็บ <code>View</code>: <code>From Top</code> / <code>Front</code> หรือเปิดโมเดลใหม่</td></tr>
<tr><td>ป้ายชื่อวัตถุค้างบนจอ</td><td>เลื่อนเมาส์ไปพื้นที่ว่างในฉาก ป้ายจะหายไป</td></tr>
<tr><td>แถบ outdated libraries</td><td>กด <code>X</code> ปิดได้ บทนี้ไม่ต้อง Manage Libraries</td></tr>
<tr><td>Example Models / Start Page</td><td>2606 เพิ่ม Python GA Demo, Standard Object Examples, QuickStart, New Features และ Copilot</td></tr>
</table>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ถ้าอยากรู้ว่าวัตถุตัวหนึ่ง (เช่นสายพาน Line10) ตั้งค่าอะไรได้บ้าง และอยากดูสถิติของมันเร็วๆ ควรทำอย่างไร?
</div>
<div class="tip"><strong>เฉลย:</strong> ดับเบิลคลิกเพื่อเปิดหน้าต่างของวัตถุ (ตั้งค่า เวลา เสีย ฯลฯ) และคลิกขวา → <code>Show Statistics Report</code>
หรือกด <code>F6</code> เพื่อดูสถิติ — โมเดลตัวอย่างถัดไป <a href="overview-03.html">Small Parts Production</a> ใช้เครื่องมือวิเคราะห์ต่อจากนี้</div>
'''
