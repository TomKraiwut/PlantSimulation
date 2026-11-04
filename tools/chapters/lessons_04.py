# -*- coding: utf-8 -*-
"""Lessons 4: Workers and shifts -- from 04_Workers_Shifts.pptx"""
from gen_site import screenshot, step_list, side_by_side


def _steps(pairs):
    """step_list with explicit badge numbers, for slides whose red callouts skip a number."""
    lis = "\n".join(
        f'    <li><span class="num">{n}</span><span class="text">{text}</span></li>' for n, text in pairs
    )
    return f'''<ol class="step-list">
{lis}
  </ol>'''


OBJECTIVES = [
    "วาง Workplace, WorkerPool และ Broker ให้เครื่องต้องมีคนคุมด้วย Processing Importer ได้",
    "ทดลองจำนวนคน ความเร็วเดิน (Speed) ความเร็วทำงาน (Efficiency) และอ่าน Worker Chart ได้",
    "ใส่ ShiftCalendar และเปรียบเทียบผังไลน์ I กับ U ได้",
    "เพิ่มคนขนของ ช่างตั้งเครื่อง และช่างซ่อมที่มี Service และ Workplace ของตัวเองได้",
]

BODY = f'''
<p class="lead" style="max-width:46em;">ต่อจาก<a href="lessons-03.html">บท 03</a>: บทก่อนเครื่องทำงานเองได้ บทนี้เครื่องต้องมีคนคุม
ถ้าคนไม่พอ เดินไกล หรือทำงานช้า ผลผลิตลด — 12 ขั้น จากเครื่องไม่มีคน ถึงช่างซ่อม ไลน์บทนี้มี 3 เครื่อง (Station1–3)
เวลา 0:10 ต่อชิ้น ขั้น 11–12 เพิ่มช่างตั้งเครื่องและช่างซ่อมที่ทำงานคนละหน้าที่กับคนคุมเครื่อง
ผลผลิตเปลี่ยนจาก <strong>94 → 356 ชิ้น/ชม.</strong> เมื่อเพิ่มคนจาก 1 คน เป็น 3 คน (วัดจริงใน PtS 2606)</p>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 และไฟล์ <code>04_Workers_Shifts.spp</code>
&nbsp;·&nbsp; Class Library › Models › Model … Model10 &nbsp;·&nbsp; ทุกตัวเลขในบทนี้วัดจาก Plant Simulation 2606 ด้วยไฟล์บทเรียนนี้
</div>

<h2>ภาพรวม: 12 ขั้น จากเครื่องไม่มีคน ถึงช่างซ่อม</h2>
<table>
<tr><th>ขั้น</th><th>เรื่อง</th><th>ทำอะไร</th></tr>
<tr><td>1</td><td>รู้จัก object ของคน</td><td>Workplace, WorkerPool, Broker</td></tr>
<tr><td>2</td><td>วาง Workplace</td><td>เปิด Processing Importer</td></tr>
<tr><td>3</td><td>Broker + WorkerPool</td><td>ตั้งจำนวนคน 3 คน</td></tr>
<tr><td>4</td><td>รัน Model2</td><td>คนยืนคุมเครื่อง ได้ 356</td></tr>
<tr><td>5</td><td>คน 1 คน + Worker Chart</td><td>ได้ 94 คนเดิน 21%</td></tr>
<tr><td>6</td><td>Speed กับ Efficiency</td><td>เดินเร็ว ทำงานเร็ว มีผลแค่ไหน</td></tr>
<tr><td>7</td><td>ShiftCalendar</td><td>2 กะ + เวลาพัก 1 วัน</td></tr>
<tr><td>8</td><td>คน 2 คน</td><td>ได้ 188 คนเดิน 21%</td></tr>
<tr><td>9</td><td>ไลน์ I กับ U</td><td>คน 2 คน 188 → 204</td></tr>
<tr><td>10</td><td>Worker Transport</td><td>คนขนชิ้นงานจาก Source</td></tr>
<tr><td>11</td><td>ช่างตั้งเครื่อง</td><td>Set-up Importer ได้ 299</td></tr>
<tr><td>12</td><td>ช่างซ่อม</td><td>Failure Importer ได้ 271</td></tr>
<tr><td>–</td><td>ลองเอง</td><td>จำนวนคน ความเร็ว ระยะห่างเครื่อง</td></tr>
</table>

<h2>10 Frame ในไฟล์นี้ เล่าเรื่องเดียวกัน</h2>
<table>
<tr><th>Frame</th><th>ตั้งค่า</th><th>ผล (ชิ้น/ชม.)</th><th>ขั้นที่</th></tr>
<tr><td>Model</td><td>3 เครื่อง ไม่มีคน</td><td>357</td><td>1</td></tr>
<tr><td>Model2</td><td>คน 3 คน เครื่องละคน</td><td>356</td><td>2–4</td></tr>
<tr><td>Model3</td><td>คน 1 คน + Worker Chart</td><td>94</td><td>5</td></tr>
<tr><td>Model4</td><td>คน 2 คน Speed 1, Eff 90/80%</td><td>152</td><td>6</td></tr>
<tr><td>Model5</td><td>Model2 + ShiftCalendar 1 วัน</td><td>5,034 (ต่อวัน)</td><td>7</td></tr>
<tr><td>Model6</td><td>คน 2 คน ไลน์ I</td><td>188</td><td>8</td></tr>
<tr><td>Model7</td><td>คน 2 คน ไลน์ U</td><td>204</td><td>9</td></tr>
<tr><td>Model8</td><td>Model2 + คนขนชิ้นงาน</td><td>255</td><td>10</td></tr>
<tr><td>Model9</td><td>Model2 + ช่างตั้งเครื่อง ชิ้น A/B</td><td>299</td><td>11</td></tr>
<tr><td>Model10</td><td>Model2 + ช่างซ่อม เครื่องเสีย</td><td>271</td><td>12</td></tr>
</table>
<div class="tip"><strong>ตัวเลขของไฟล์:</strong> 10 Frame · 3 Station ต่อไลน์ · 1–4 คนต่อไลน์ · 9 Frame ทำจาก Duplicate —
Model3 ถึง Model10 สร้างด้วยคลิกขวา › <code>Duplicate</code> ใน Class Library ของที่วางด้วยเมาส์ใน Model2 ไม่ต้องวางใหม่
(Model7 ทำจาก Duplicate Model6)</div>

<h2>ขั้นที่ 1: object ของคน อยู่ในแท็บ Resources</h2>
{screenshot("assets/images/lessons/04-01.jpg", "Toolbox แท็บ Resources: Workplace, WorkerPool, Broker, ShiftCalendar")}
{step_list([
    "แท็บ <code>Resources</code> ใน Toolbox",
    "<strong>Workplace</strong> — จุดที่คนยืนทำงานข้างเครื่อง",
    "<strong>WorkerPool</strong> — ห้องพักคน กำหนดจำนวนคน",
    "<strong>Broker</strong> — รับคำขอจากเครื่อง แล้วหาคนว่างใน WorkerPool",
    "<strong>ShiftCalendar</strong> — กะทำงาน และเวลาพัก (ขั้นที่ 7)",
])}
<div class="tip"><strong>ลำดับการทำงาน:</strong> ชิ้นงานเข้าเครื่อง → Importer ขอคนจาก Broker → Broker หาคนว่างใน WorkerPool
→ คนเดินไป Workplace → ทำงาน → ชิ้นงานออก &nbsp;·&nbsp; เลื่อนเมาส์ไปชี้ไอคอนจะเห็นชื่อ (ภาพนี้ชี้ที่ Workplace)</div>

<h2>ขั้นที่ 1: Model — 3 เครื่อง ยังไม่มีคน</h2>
{side_by_side(
    screenshot("assets/images/lessons/04-02.jpg", "Frame Model: Source, Station1–3, Drain และ Chart หลังรัน 1 ชั่วโมง"),
    step_list([
        "<strong>Station1–3</strong> 0:10 ต่อชิ้น ไม่ต้องมีคน",
        "<strong>FG = 357</strong> ผลหลังรัน 1 ชั่วโมง",
        "Chart เขียวทุกแท่ง — ทุกเครื่อง Working ~100%",
    ])
)}
<div class="tip"><strong>ไลน์บทนี้:</strong> ใช้ไลน์ของ<a href="lessons-02.html">บท 02</a> ตัดเหลือ 3 เครื่องให้เห็นคนชัด ๆ
Model เป็นฐานเปรียบเทียบ ไม่มีคน ไม่มีกะ · ต่อไปจะให้เครื่องต้องมีคนคุม</div>

<h2>ขั้นที่ 2: วาง Workplace ใต้เครื่อง แล้วเลือก Processing Importer</h2>
{screenshot("assets/images/lessons/04-03.jpg", "Frame Model2 มี Workplace ใต้ทุกเครื่อง และ popup Do you want to activate an importer?")}
{_steps([
    (1, "<strong>Workplace ใต้ Station1</strong> — คลิกไอคอน Workplace แล้วคลิกใต้ป้ายชื่อเครื่อง"),
    (2, "<strong>Station2 และ 3</strong> — ทำซ้ำทีละเครื่อง Workplace ชี้เข้าหาเครื่องเอง"),
    (4, "<strong>Processing Importer</strong> — popup ขึ้นทุกครั้ง = เครื่องนี้ต้องมีคนคุมตอนผลิต"),
])}
<div class="note"><strong>ถ้า popup ไม่ขึ้น:</strong> วาง Workplace ไกลเครื่องเกินไป ลบแล้ววางใหม่ให้ชิดเครื่อง · ทุกเครื่องต้องมี Workplace ของตัวเอง
(ถ้าเครื่องมี Importer แต่ไม่มี Workplace โปรแกรมหยุดพร้อมข้อความ <em>does not have a free workplace</em>)
Setup / Failure / Transport Importer ใช้กับคนตั้งเครื่อง คนซ่อม และคนขนของ — ขั้นนี้ใช้ Processing อย่างเดียว</div>

<h2>ขั้นที่ 2: สิ่งที่โปรแกรมตั้งให้</h2>
{screenshot("assets/images/lessons/04-04.jpg", "Station1 แท็บ Importer › Processing (ซ้าย) และหน้าต่าง Workplace1 (ขวา)")}
{step_list([
    "แท็บ <code>Importer</code> › <code>Processing</code> — งานผลิตต้องใช้คน",
    "<code>Active</code> — ช่องนี้ขึ้นเครื่องหมายถูก ☑ ให้เอง = เปิดใช้คน",
    "<code>Broker</code> = <code>root.Broker</code> — ขอคนจาก Broker ใน Frame นี้",
    "Workplace1: <code>Station</code> = <code>Station1</code> — Workplace นี้เป็นของ Station1",
    "<code>Worker Stays Here After Completing the Job</code> — คนรอที่เครื่องหลังทำเสร็จ ไม่เดินกลับ WorkerPool",
])}
<div class="tip"><strong>ไม่ต้องพิมพ์:</strong> ทั้งหมดนี้ตั้งให้เองตอนเลือก Processing Importer ใช้ตรวจเมื่อคนไม่มาทำงาน</div>

<h2>ขั้นที่ 3: วาง WorkerPool และ Broker</h2>
{side_by_side(
    screenshot("assets/images/lessons/04-05.jpg", "หน้าต่าง WorkerPool แท็บ Attributes"),
    step_list([
        "<code>Workers to Create</code> — ตารางจำนวนคน (ภาพถัดไป)",
        "<code>Travel Mode</code> = <em>Move freely within area</em> = เดินอิสระ หลบสิ่งกีดขวางใน 3D",
        "<code>Broker</code> — WorkerPool ส่งคนผ่าน Broker ตัวนี้",
        "<code>Shift Calendar</code> — ว่างไว้ก่อน (ขั้นที่ 7)",
    ])
)}
<div class="tip"><strong>WorkerPool:</strong> เหมือนห้องพักพนักงาน คนเริ่มที่นี่ และกลับมาที่นี่เมื่อไม่มีงาน
วาง WorkerPool และ Broker จาก Toolbox แท็บ Resources ไว้ข้างไลน์ แล้วดับเบิลคลิก WorkerPool — ช่อง Broker ต้องชี้ไปที่ Broker</div>

<h2>ขั้นที่ 3: ตั้งจำนวนคน และดู Broker</h2>
{screenshot("assets/images/lessons/04-06.jpg", "ตาราง Workers to Create (ซ้าย) และหน้าต่าง Broker (ขวา)")}
{step_list([
    "<code>Worker</code> = <code>.Resources.Worker</code> — คนแบบมาตรฐานใน Class Library",
    "<code>Amount</code> = 3 — 3 คน = เครื่องละคน",
    "ดับเบิลคลิก <code>Broker</code> — ไม่ต้องตั้งค่า ใช้ค่าเริ่มต้น · แท็บ Statistics ดูจำนวนคำขอคน",
])}
<div class="tip"><strong>อ่านตาราง:</strong> หนึ่งแถวในตาราง = คนหนึ่งกลุ่ม Amount คือจำนวนคนในกลุ่มนั้น
ช่อง Speed / Efficiency ใช้กำหนดความเร็วเดิน และความเร็วทำงาน (ขั้นที่ 6)</div>

<h2>ขั้นที่ 4: รัน Model2 — คนเดินมาคุมเครื่อง</h2>
{screenshot("assets/images/lessons/04-07.jpg", "Model2 มุมมอง 3D ระหว่างรัน (ซ้าย) และผลหลัง 1 ชั่วโมง (ขวา)")}
{step_list([
    "คนยืนหน้าเครื่อง — หันหน้าเข้าเครื่องเพราะวาง Workplace ด้วยเมาส์ติดเครื่อง",
    "Workplace — จุดยืนของคน",
    "<strong>FG = 356</strong> — เกือบเท่า Model (357) เพราะมีคนเครื่องละคน ยืนรอที่เครื่องตลอด",
])}
<div class="tip"><strong>ทำไมเกือบเท่าเดิม:</strong> ตอนเริ่มรันคนเดินจาก WorkerPool ไป Workplace แล้วอยู่ที่เครื่อง (Worker Stays Here)
จึงเสียเวลาเดินแค่ตอนแรก ขั้นต่อไปทดลองว่าถ้าคนไม่พอจะเป็นอย่างไร</div>

<h2>ขั้นที่ 5: Duplicate Model2 เป็น Model3 แล้วเหลือคน 1 คน</h2>
{screenshot("assets/images/lessons/04-08.jpg", "เมนูคลิกขวา Model2 ใน Class Library (ซ้าย) และ Workers to Create ของ Model3 (ขวา)")}
{step_list([
    "คลิกขวา <code>Model2</code> ใน Class Library › Models",
    "<code>Duplicate</code> — ได้ Frame ใหม่เหมือนเดิมทุกอย่าง ชื่อ Model22 ให้ <code>Rename</code> เป็น Model3",
    "<code>Amount</code> = 1 — ดับเบิลคลิก WorkerPool › Workers to Create แก้ 3 เป็น 1 › OK",
])}
<div class="note"><strong>คำถามก่อนรัน:</strong> คน 1 คน ดูแล 3 เครื่อง จะได้กี่ชิ้นต่อชั่วโมง? ลองเดาก่อน (คนส่วนใหญ่ตอบ 356 ÷ 3 ≈ 119)
· Duplicate ทำให้ไม่ต้องวาง Workplace WorkerPool Broker ใหม่ Frame ต่อ ๆ ไปในบทนี้ทำแบบเดียวกันทั้งหมด</div>

<h2>ขั้นที่ 5: Worker Chart — ลาก WorkerPool ไปวางบน Chart</h2>
{screenshot("assets/images/lessons/04-09.jpg", "Frame Model3 กับ Chart2 และหน้าต่าง Statistics Type")}
{step_list([
    "<code>Chart</code> จาก Toolbox › User Interface วางข้างไลน์ (ชื่อ Chart2)",
    "ลาก <code>WorkerPool</code> ไปปล่อยบน Chart2 — หน้าต่าง Statistics Type ขึ้นเอง",
    "<code>Group Workers By</code> = <code>Creation Table</code> — แยกแท่งตามแถวในตาราง Workers to Create",
    "<code>OK</code>",
])}
<div class="tip"><strong>Pool กับ Creation Table:</strong> Group Workers By = Pool ได้แท่งเดียวทั้ง WorkerPool · Creation Table แยกตามแถวของตาราง
Model3 มีแถวเดียว Amount = 1 จึงได้แท่ง Worker (1) — ในขั้นที่ 6 ตารางมี 2 แถว จะได้ 2 แท่ง</div>

<h2>ขั้นที่ 5: Model3 — คน 1 คน ดูแล 3 เครื่อง</h2>
{screenshot("assets/images/lessons/04-10.jpg", "Model3 หลังรัน 1 ชั่วโมง และ Chart2 (คลิกขวา Chart2 › Show)")}
{step_list([
    "<strong>FG = 94</strong> — ไม่ถึง 119 ที่เดาไว้ (Model2 คน 3 คน ได้ 356)",
    "Chart เครื่อง: Working ~26% สีเทา = เครื่องรอคน",
    "สีเขียว = <strong>Working 78.9%</strong> คนทำงาน",
    "สีส้ม = <strong>En-route to job 21.1%</strong> คนเดินจากเครื่องหนึ่งไปอีกเครื่อง",
])}
<div class="note"><strong>ทำไมได้ 94:</strong> ชิ้นหนึ่งต้องใช้คน 3 เครื่อง × 10 วิ = 30 วิ → ทำเต็มที่ได้ 3,600 ÷ 30 = 120 ชิ้น
· คนเดิน 21% → 120 × 0.79 ≈ 94</div>

<h2>ขั้นที่ 6: Speed กับ Efficiency คืออะไร</h2>
{screenshot("assets/images/lessons/04-11.jpg", "คลาส Resources › Worker (ซ้าย) และ Workers to Create ของ Model4 (ขวา)")}
{step_list([
    "<code>Efficiency</code> 100% — ความเร็วทำงาน 100% = ใช้เวลาเท่าเวลาเครื่อง 0:10",
    "<code>Speed</code> 1.5 m/s — ความเร็วเดิน ค่าเริ่มต้นของคลาส Worker",
    "<code>Speed</code> = 1 ใส่ในตาราง = คนแถวนั้นเดิน 1 m/s · ช่องว่าง = ใช้ 1.5 ของคลาส",
    "<code>Efficiency</code> = 90 / 80 — 10 วิ ÷ 0.9 = 11.1 วิ · 10 วิ ÷ 0.8 = 12.5 วิ ต่อชิ้น",
])}
<div class="tip"><strong>Model4:</strong> Duplicate Model2 แล้วแก้ตารางเป็น 2 แถว แถวละ 1 คน = คน 2 คนที่ความสามารถต่างกัน
ช่อง Home Location ใส่ Workplace1, Workplace2 (ไม่ทำให้ผลในไลน์นี้ต่าง วัดแล้ว 151–152 ทั้งมีและไม่มี)</div>
<div class="note"><strong>ข้อควรจำ:</strong> อย่าแก้ค่าในคลาส <code>.Resources.Worker</code> เพราะทุก Frame ใช้คลาสเดียวกัน
ให้แก้ในตาราง Workers to Create ของ Frame นั้นแทน</div>

<h2>ขั้นที่ 6: Model4 — คน 2 คน เดินช้าลง และทำงานช้าไม่เท่ากัน</h2>
{screenshot("assets/images/lessons/04-12.jpg", "Model4 หลังรัน 1 ชั่วโมง และ Man_Chart (คลิกขวา › Show)")}
{step_list([
    "<strong>FG = 152</strong> — คน 2 คนแบบค่าเริ่มต้นได้ 188 (ขั้นที่ 8) หายไป 36 ชิ้น",
    "<code>Man_Chart</code> — Worker Chart แบบขั้นที่ 5 ตาราง 2 แถว = 2 แท่ง",
    "แท่งซ้าย = แถว 1 (Eff 90%) ทำงาน ~73%",
    "แท่งขวา = แถว 2 (Eff 80%) ทำงาน ~76% ทำช้าจึงใช้เวลาทำงานนานกว่า",
])}
<div class="tip"><strong>หายไปเพราะอะไร:</strong> วัดทีละอย่าง: Speed 1 อย่างเดียว 188 → 170 · Efficiency 90/80 อย่างเดียว 188 → 166
· สองอย่างรวมกัน 151–152 &nbsp;·&nbsp; ทั้งสองแท่งชื่อ Worker (1) เหมือนกัน ลำดับแท่ง = ลำดับแถวในตาราง</div>

<h3>ผลทดลอง คน 1 คน (Model3) — เปลี่ยนทีละค่า</h3>
<p>แก้ตาราง Workers to Create ของ Model3 › Reset › รัน 1 ชม. (คนเดิน = สีส้ม En-route to job ใน Chart2)</p>
<table>
<tr><th>ลองเปลี่ยน</th><th>FG / ชม.</th><th>คนเดิน</th><th>อ่านว่า</th></tr>
<tr><td>ค่าเริ่มต้น (1.5 m/s, 100%)</td><td>94</td><td>21%</td><td>ฐานของการทดลอง</td></tr>
<tr><td>Speed = 0.75 (ช้าลงครึ่ง)</td><td>77</td><td>35%</td><td>เดินนานขึ้น เวลาทำงานเหลือน้อยลง −18%</td></tr>
<tr><td>Speed = 1 (ค่าใน Model4)</td><td>85</td><td>29%</td><td>เดินช้ากว่าค่าเริ่มต้น</td></tr>
<tr><td>Speed = 3 (เร็วขึ้น 2 เท่า)</td><td>105</td><td>12%</td><td>+12% แต่ไม่ถึง 120 เพราะยังต้องเดิน</td></tr>
<tr><td>Efficiency = 50% (ช้าครึ่ง)</td><td>52</td><td>12%</td><td>ชิ้นละ 20 วิ ต่อเครื่อง ผลลดเกือบครึ่ง</td></tr>
<tr><td>Efficiency = 80% (แถว 2 ของ Model4)</td><td>78</td><td>18%</td><td>ชิ้นละ 12.5 วิ ต่อเครื่อง</td></tr>
<tr><td>Efficiency = 120% (เร็วขึ้น)</td><td>108</td><td>24%</td><td>ชิ้นละ 8.3 วิ ต่อเครื่อง คนเก่งกว่ามาตรฐาน</td></tr>
</table>

<h3>คนพอ กับ คนไม่พอ — ค่าไหนมีผล</h3>
<p>แก้ตาราง Workers to Create ของ Model2 (3 คน) และ Model4 (2 คน) รัน 1 ชม. · แถว 2 คนตั้งในตาราง 2 แถว แถวละ 1 คน</p>
<table>
<tr><th>คน</th><th>ลองเปลี่ยน</th><th>FG / ชม.</th><th>อ่านว่า</th></tr>
<tr><td>3 คน</td><td>ค่าเริ่มต้น (Model2)</td><td>356</td><td>ฐาน: เครื่องละคน</td></tr>
<tr><td>3 คน</td><td>คนที่ 3 Speed = 0.75</td><td>356</td><td>คนยืนประจำเครื่อง ไม่ต้องเดิน Speed ไม่มีผล</td></tr>
<tr><td>3 คน</td><td>คนที่ 3 Efficiency = 80%</td><td>285</td><td>เครื่องของคนนั้นช้าเป็น 12.5 วิ = คอขวด (3,600 ÷ 12.5 = 288)</td></tr>
<tr><td>3 คน</td><td>ทุกคน Efficiency = 120%</td><td>428</td><td>ชิ้นละ 8.3 วิ เร็วกว่าเครื่องที่ไม่มีคน (357)</td></tr>
<tr><td>2 คน</td><td>ค่าเริ่มต้น</td><td>188</td><td>เท่า Model6 (ขั้นที่ 8)</td></tr>
<tr><td>2 คน</td><td>Speed = 1 ทั้งคู่</td><td>170</td><td>เดินช้าลง เพราะต้องเดินไปมาระหว่างเครื่อง</td></tr>
<tr><td>2 คน</td><td>Efficiency 90 / 80 อย่างเดียว</td><td>166</td><td>ทำงานช้าลง</td></tr>
<tr><td>2 คน</td><td>Speed = 1 และ Efficiency 90 / 80 (Model4)</td><td>151</td><td>ผลรวมของสองอย่าง</td></tr>
</table>
<div class="note"><strong>สรุป:</strong> Speed มีผลเมื่อคนต้องเดิน (คนไม่พอ) · Efficiency มีผลเสมอ เพราะเปลี่ยนเวลาทำงานต่อชิ้น
· คนช้าคนเดียวทำให้ทั้งไลน์ช้า (คนที่ 3 = แถว 2 ของตาราง: แถว 1 Amount 2, แถว 2 Amount 1 — คนช้าไปยืนที่ Station3 เครื่องอื่นจึงรอ Working ~80%)</div>

<h2>ขั้นที่ 7: Duplicate Model2 เป็น Model5 แล้ววาง ShiftCalendar</h2>
{side_by_side(
    screenshot("assets/images/lessons/04-13.jpg", "Frame Model5 ที่วาง ShiftCalendar ข้าง Chart"),
    step_list([
        "<code>ShiftCalendar</code> จาก Toolbox › Resources แล้วคลิกวางที่ว่างข้าง Chart",
    ])
)}
<div class="tip"><strong>Frame ใหม่:</strong> คลิกขวา Model2 › Duplicate แบบขั้นที่ 5 (ได้ชื่อ Model22) แล้ว Rename เป็น Model5
· ใช้คน 3 คนของ Model2 เพื่อให้เห็นผลของกะอย่างเดียว</div>

<h2>ขั้นที่ 7: ลาก WorkerPool และเครื่องไปวางบน ShiftCalendar</h2>
{screenshot("assets/images/lessons/04-14.jpg", "Frame Model5 (ซ้าย) และตาราง Shift Times ของ ShiftCalendar (ขวา)")}
{step_list([
    "ลาก <code>WorkerPool</code> ไปปล่อยบน ShiftCalendar = คนทำงานตามกะ",
    "ลาก <code>Station1–3</code> ไปปล่อยบน ShiftCalendar ทีละเครื่อง = เครื่องหยุดนอกกะ",
    "<code>ShiftCalendar</code> — ปล่อยบนไอคอนเท่านั้น ถ้าปล่อยที่ว่าง object จะย้ายที่แทน",
    "2 กะ จันทร์–ศุกร์ 6:00–14:00 และ 14:00–22:00 (ค่าเริ่มต้น)",
    "<code>Pauses</code> — พัก 9:00–9:15, 12:00–12:45 · 18:00–18:30, 20:30–21:00",
])}
<div class="tip"><strong>แก้กะ:</strong> ดับเบิลคลิก ShiftCalendar แก้ตารางกะได้ ใน Model5 ใช้ค่าเริ่มต้น เครื่องทุกเครื่องและ WorkerPool ใช้ปฏิทินเดียวกัน</div>

<h2>ขั้นที่ 7: Model5 รัน 1 วัน — นอกกะเครื่องหยุด</h2>
{screenshot("assets/images/lessons/04-15.jpg", "EventController › Settings (ซ้าย) และ Station3 › Statistics (ขวา)")}
{step_list([
    "<code>End Time</code> = <code>1:00:00:00</code> — 1 วัน เริ่ม 06:00",
    "<strong>Working 58.27%</strong> — ทำงานเฉพาะในกะ",
    "<strong>Paused 8.33%</strong> — เวลาพักในกะ",
    "<strong>Unplanned 33.33%</strong> — 22:00–6:00 นอกกะ",
    "<strong>Exits 5,034</strong> — ชิ้นต่อวัน = FG",
])}
<div class="note"><strong>ตรวจตัวเลข:</strong> กะ 16 ชม. − พัก 2 ชม. = 14 ชม. = 58.3% ของวัน · 14 × 360 ≈ 5,040 ใกล้กับ 5,034 ที่วัดได้</div>

<h2>ขั้นที่ 8: Model6 — คน 2 คน ดูแล 3 เครื่อง</h2>
{screenshot("assets/images/lessons/04-16.jpg", "Model6 หลังรัน 1 ชั่วโมง และ Chart2 ของคน")}
{step_list([
    "<strong>FG = 188</strong> — คน 1 คน 94 → คน 2 คน 188 (2 เท่าพอดี)",
    "Chart เครื่อง: Working ~53% สีเทา = รอคน",
    "สีเขียว = <strong>Working 78.8%</strong> คนทำงาน",
    "สีส้ม = <strong>En-route to job 21.0%</strong> คนเดินไปหาเครื่อง",
])}
<div class="tip"><strong>ทำ Model6:</strong> Duplicate Model2 → Model6 แล้วตั้ง Amount = 2 ในแถวเดียว จึงได้แท่งเดียว Worker (2) · Chart2 ทำแบบขั้นที่ 5</div>

<h2>ขั้นที่ 9: Model7 — จัดไลน์เป็นรูป U</h2>
{screenshot("assets/images/lessons/04-17.jpg", "Model6 ไลน์ I (ซ้าย) และ Model7 ไลน์ U (ขวา)")}
{step_list([
    "<strong>ไลน์ I</strong> — Station3 อยู่ปลายไลน์ คนเดินไกล",
    "<code>Station3</code> — ย้ายมาไว้ใต้ Station2",
    "<code>Workplace3</code> — อยู่ด้านในตัว U ใกล้ Workplace2",
    "<code>Drain</code> — ใต้ Station1 ชิ้นงานกลับมาออกฝั่งเดียวกับที่เข้า",
    "<strong>FG = 204</strong> — คนเท่าเดิม 2 คน",
])}
<div class="note"><strong>ลากย้ายให้ถูก:</strong> Duplicate Model6 → Model7 แล้วลาก Station3, Workplace3, Drain ไปวางที่ว่าง = ย้ายที่
ถ้าปล่อยบน object อื่นจะกลายเป็นการเชื่อม (เช่นปล่อย Station บน Chart = เพิ่มแท่ง) · Connector ตามไปเอง</div>

<h2>ขั้นที่ 9: Worker Chart ไลน์ I กับไลน์ U</h2>
{screenshot("assets/images/lessons/04-18.jpg", "Chart2 ของ Model6 ไลน์ I (ซ้าย) และ Model7 ไลน์ U (ขวา)")}
{step_list([
    "<strong>ไลน์ I</strong> — เดิน 21.0% · ทำงาน 78.8% · ได้ 188 ชิ้น/ชม.",
    "<strong>ไลน์ U</strong> — เดิน 14.3% · ทำงาน 85.5% · ได้ 204 ชิ้น/ชม. (+8.5%)",
])}
<div class="tip"><strong>บทเรียน:</strong> คนเท่าเดิม เครื่องเท่าเดิม แค่จัดผังให้เดินสั้นลง ได้งานเพิ่ม · ถ้ามีคนครบ 3 คน ทั้ง I และ U ได้ 356 เท่ากัน
— ผังมีผลเมื่อคนต้องเดินระหว่างเครื่อง เหมือน Speed ในขั้นที่ 6</div>

<h2>ขั้นที่ 10: Worker Transport — วาง Workplace ใต้ Source</h2>
{screenshot("assets/images/lessons/04-19.jpg", "Model8 วาง Workplace ใต้ Source และ popup Transport Importer")}
{step_list([
    "<code>Source</code> — จุดปล่อยชิ้นงาน",
    "Workplace ใต้ Source — คลิกไอคอน Workplace แล้วคลิกใต้ป้ายชื่อ Source (ได้ชื่อ Workplace0)",
    "<code>Transport Importer</code> — Source มีตัวเลือกเดียว = ต้องมีคนขนชิ้นงานไปเครื่องถัดไป",
])}
<div class="tip"><strong>ต่างจากขั้นที่ 2:</strong> Processing = คนคุมเครื่องตอนผลิต · Transport = คนยกชิ้นงานจาก Source ไป Station1 (เหมือนคนเติมของเข้าไลน์)
· Model8 ทำจากคลิกขวา Model2 › Duplicate ใช้คน 3 คนเท่าเดิม</div>

<h2>ขั้นที่ 10: คนขนชิ้นงานจาก Source ไป Station1</h2>
{screenshot("assets/images/lessons/04-20.jpg", "Source แท็บ Importer › Transport (ซ้าย) และ Model8 มุมมอง 3D ระหว่างรัน (ขวา)")}
{step_list([
    "แท็บ <code>Importer</code> › <code>Transport</code> — ตั้งให้เองจาก popup",
    "<code>Active</code> — เปิดใช้คนขน",
    "<code>Wait For Free Target</code> — รอให้เครื่องถัดไปว่างก่อนเรียกคน",
    "<code>Broker</code> = <code>root.Broker</code> — ขอคนจาก Broker เดียวกับเครื่อง",
    "คนยกชิ้นงาน — เดินจาก Source ไปวางที่ Station1",
])}

<h2>ขั้นที่ 10: Model8 — ผลเมื่อต้องมีคนขนของ</h2>
{side_by_side(
    screenshot("assets/images/lessons/04-21.jpg", "Model8 หลังรัน 1 ชั่วโมง FG = 255"),
    step_list([
        "<strong>FG = 255</strong> — ลดจาก 356 (−28%) คนเท่าเดิม 3 คน",
        "Chart เครื่อง: Working ~71% สีเทา = รอชิ้นงานที่คนยังขนมาไม่ถึง",
    ])
)}
<div class="note"><strong>อ่านผล:</strong> คนใช้เวลาขนของ 4.8% เดินไปหางาน 4.9% · Station1 ต้องรอชิ้นงานจากคนขน ทั้งไลน์จึงช้าลง (วัดจริงใน PtS 2606)</div>

<h2>ขั้นที่ 11: Model9 — ชิ้นงาน 2 ชนิด A กับ B สลับกัน</h2>
{screenshot("assets/images/lessons/04-22.jpg", "Source ของ Model9 (ซ้าย) และ DataTable Parts (ขวา)")}
{step_list([
    "<code>MU Selection</code> = <code>Sequence Cyclical</code> — ปล่อยชิ้นงานตามตาราง วนซ้ำ",
    "<code>Table</code> = <code>Parts</code> — Toolbox › Information Flow › DataTable วางในเฟรม แล้ว Rename เป็น Parts",
    "<code>Parts</code> — แถว 1: Part 20 ชิ้น ชื่อ A · แถว 2: Part 20 ชิ้น ชื่อ B",
])}
<div class="tip"><strong>ทำไมต้อง 2 ชนิด:</strong> เครื่องตั้งเครื่อง (Set-up) เมื่อชื่อชิ้นงานเปลี่ยน A → B · ชิ้นแรกที่เข้าเครื่องก็ต้องตั้งเครื่องด้วย
ใช้คลาส Part เดิม แค่ตั้งชื่อในคอลัมน์ Name ต่างกัน (Set-up Depends On = ชื่อ MU) · Model9 ทำจาก Duplicate Model2</div>

<h2>ขั้นที่ 11: Set-up Time และ Set-up Importer</h2>
{screenshot("assets/images/lessons/04-23.jpg", "Station แท็บ Times (ซ้าย) และแท็บ Importer › Set-up (ขวา)")}
{step_list([
    "<code>Set-up Time</code> = <code>0:10</code> — ตั้งเครื่องครั้งละ 10 วินาที ทุกเครื่อง",
    "<code>Common Resources</code> — ไม่เลือกช่องนี้ = คนตั้งเครื่องเป็นคนละคนกับคนคุมเครื่อง",
    "<code>Active</code> — คลิกช่องให้ขึ้นเครื่องหมายถูก ☑ = เปิด Set-up Importer",
    "<code>Services</code> = <code>SetupTech</code> — ขอคนที่ทำงาน SetupTech ได้",
    "<code>Broker</code> — Broker ของ Frame นี้",
])}
<div class="tip"><strong>ทำครบ 3 เครื่อง:</strong> ทำแบบเดียวกันที่ Station2 และ Station3 · ถ้าคลิกช่อง Common Resources ให้ขึ้นเครื่องหมายถูก ☑
คนคุมเครื่องจะตั้งเครื่องเอง ไม่ต้องมีช่าง</div>

<h2>ขั้นที่ 11: คลาส Technician และช่างตั้งเครื่อง 1 คน</h2>
{screenshot("assets/images/lessons/04-24.jpg", "Resources › Technician › Services (ซ้าย) และ Workers to Create ของ Model9 (ขวา)")}
{step_list([
    "<code>Technician</code> — คลิกขวา Resources › Worker › Duplicate แล้ว Rename · Services เหลือแถวเดียว <code>SetupTech</code>",
    "แถว 2 = <code>.Resources.Technician</code> — ลากคลาส Technician จาก Class Library มาวางในช่อง Worker",
    "<code>Amount</code> = 1 — ช่าง 1 คน ดูแล 3 เครื่อง · แถว 1 คนคุมเครื่อง 3 คนเท่าเดิม",
])}
<div class="note"><strong>ทำไมต้องมีคลาสใหม่:</strong> คลาส Worker ทำได้ทุกงาน (Processing, Set-up, Failure, Transport)
ถ้าใช้ Worker เป็นช่าง ช่างจะถูกเรียกไปคุมเครื่องแทน (ทดลองแล้ว: ช่างไปคุมเครื่องเอง Working 99% คนคุมเครื่องคนหนึ่งว่าง)</div>

<h2>ขั้นที่ 11: Workplace ของช่าง วางเหนือเครื่อง</h2>
{screenshot("assets/images/lessons/04-25.jpg", "popup เมื่อวาง Workplace เหนือเครื่อง (ซ้าย) และ Supported Services ของ Workplace4 (ขวา)")}
{step_list([
    "ปิด popup — วาง Workplace เหนือเครื่องแล้วกด × ไม่เลือกอะไร (Set-up Importer ตั้งในเครื่องแล้ว)",
    "<code>Workplace4–6</code> › Supported Services = <code>SetupTech</code> — ที่ยืนของช่างเท่านั้น",
    "<code>Workplace1–3</code> › Supported Services = <code>Processing</code> — ที่ยืนของคนคุมเครื่องเท่านั้น (ตั้งแบบเดียวกัน ไม่มีในภาพ)",
])}
<div class="note"><strong>ระวัง:</strong> popup เหลือ 2 ตัวเลือกเพราะเครื่องเปิด Processing และ Set-up แล้ว ถ้าเผลอเลือก Transport Importer
ชิ้นงานต้องรอคนยก ไลน์ค้าง FG = 0 (แก้ที่ Station › Importer › Transport เอาเครื่องหมายถูกที่ Active ออก)
· ถ้า Workplace1–3 ยังรับทุก Service ช่างจะไปยืนแทนคนคุมเครื่อง คนคุมเครื่องต้องเดินออกไปแล้วกลับมา ได้ 277</div>

<h2>ขั้นที่ 11: Model9 — ช่างเดินไปตั้งเครื่องทีละเครื่อง</h2>
{screenshot("assets/images/lessons/04-26.jpg", "Model9 มุมมอง 3D ระหว่างรัน (ซ้าย) และ Chart2 หลังรัน 1 ชั่วโมง (ขวา)")}
{step_list([
    "<strong>Technician</strong> — ยืนที่ Workplace เหนือเครื่องที่เพิ่งตั้งเสร็จ",
    "คนคุมเครื่อง — อยู่ที่เดิมตลอด ไม่ต้องหลบให้ช่าง",
    "<strong>Worker (3)</strong> ทำงาน 83%",
    "<strong>Technician (1)</strong> ตั้งเครื่อง 12.8% เดิน 3.5% · <strong>FG = 299</strong>",
])}
<div class="tip"><strong>เทียบผล (1 ชม.):</strong> Model2 ไม่มีการตั้งเครื่อง 356 · ช่างแยกแต่ Workplace1–3 รับทุก Service 277 · Workplace แยกตาม Service 299
— เครื่องละ 4.4% เป็นเวลาตั้งเครื่อง (เปลี่ยนชนิด 16 ครั้ง × 10 วินาที) ที่เหลือคือเวลารอช่างเดินมาจากเครื่องก่อนหน้า</div>

<h2>ขั้นที่ 12: Model10 — เครื่องเสีย และ Failure Importer</h2>
{screenshot("assets/images/lessons/04-27.jpg", "แท็บ Failures (ซ้าย) และแท็บ Importer › Failure (ขวา)")}
{step_list([
    "<code>Availability</code> = 95% — เครื่องพร้อมทำงาน 95% ของเวลา",
    "<code>MTTR</code> = <code>1:00</code> — ซ่อมเฉลี่ยครั้งละ 1 นาที (Failures › New… หรือดับเบิลคลิกแถว Failure)",
    "<code>Active</code> — คลิกช่องให้ขึ้นเครื่องหมายถูก ☑ = ต้องมีคนมาซ่อม",
    "<code>Services</code> = <code>Repair</code> — ขอคนที่ซ่อมได้",
    "<code>Broker</code> — Broker ของ Frame นี้",
])}
<div class="tip"><strong>ทำทั้ง 3 เครื่อง:</strong> Duplicate Model2 → Model10 แล้วตั้งค่าที่ Station1–3 · โปรแกรมคำนวณช่วงเวลาระหว่างเสียให้เอง</div>

<h2>ขั้นที่ 12: Workplace ของช่างซ่อม</h2>
{screenshot("assets/images/lessons/04-28.jpg", "popup Failure Importer (ซ้าย) และ Supported Services ของ Workplace4 (ขวา)")}
{step_list([
    "<code>Failure Importer</code> — วาง Workplace เหนือเครื่องแล้วเลือก Failure Importer ทำทั้ง 3 เครื่อง",
    "<code>Workplace4–6</code> › Supported Services = <code>Repair</code> — ที่ยืนของช่างซ่อม",
    "<code>Workplace1–3</code> › Supported Services = <code>Processing</code> — ที่ยืนของคนคุมเครื่อง (ตั้งแบบเดียวกัน ไม่มีในภาพ)",
])}
<div class="note"><strong>ต้องมี Workplace ของช่าง:</strong> ทดลองแล้ว: ถ้าไม่มี Workplace ที่รับ Repair ช่างไม่มาซ่อมเลย เครื่องเสียค้าง ได้แค่ 58 ชิ้น</div>

<h2>ขั้นที่ 12: คลาส Repairman และช่างซ่อม 1 คน</h2>
{screenshot("assets/images/lessons/04-29.jpg", "Resources › Repairman › Services (ซ้าย) และ Workers to Create ของ Model10 (ขวา)")}
{step_list([
    "<code>Repairman</code> — Duplicate คลาส Worker แบบขั้นที่ 11 · Services เหลือแถวเดียว <code>Repair</code>",
    "แถว 2 = <code>.Resources.Repairman</code> — ลากคลาสมาวางในช่อง Worker",
    "<code>Amount</code> = 1 — ช่างซ่อม 1 คน ดูแล 3 เครื่อง",
])}
<div class="note"><strong>ระวัง:</strong> ถ้า Failure Importer ขอ Service = Failure (ค่าเริ่มต้น) คนคุมเครื่องต้องมาซ่อมกันเอง
ไลน์ค้างที่ 12:40 ได้ 58 ชิ้น — คลาส Worker ทำงาน Failure ได้ คนคุมเครื่องที่ยืนอยู่กับเครื่องจึงติดกันเอง</div>

<h2>ขั้นที่ 12: Model10 — ช่างเดินไปซ่อมเครื่องที่เสีย</h2>
{screenshot("assets/images/lessons/04-30.jpg", "Model10 มุมมอง 3D ระหว่างรัน (ซ้าย) และ Chart2 หลังรัน 1 ชั่วโมง (ขวา)")}
{step_list([
    "<strong>Repairman</strong> — ยืนที่ Workplace เหนือเครื่องที่เพิ่งซ่อม",
    "<strong>Worker (3)</strong> ทำงาน 82% เครื่องเสียคนก็รอ",
    "<strong>Repairman (1)</strong> ซ่อม 23.1% เดิน 0.7% · <strong>FG = 271</strong>",
])}
<div class="tip"><strong>เทียบผล (1 ชม.):</strong> ไม่ใช้คนซ่อม 292 · ช่างซ่อม 1 คน 271 · ช่าง 2 คน 290 · MTTR 2:00 ได้ 242
· เครื่องเสียแบบสุ่ม ตัวเลขเปลี่ยนตามช่วงเวลารัน (เวลาเครื่องเสียรวมช่วงรอช่างเดินมา: Station1 9.4% Station2 13.2% Station3 6.9%)</div>

<h2>สรุป 10 Frame (PtS 2606)</h2>
<table>
<tr><th>Frame</th><th>ตั้งค่า</th><th>เวลาจำลอง</th><th>ผลผลิต</th><th>อ่านว่า</th></tr>
<tr><td>Model</td><td>3 เครื่อง ไม่มีคน</td><td>1 ชม.</td><td>357 ชิ้น</td><td>ฐานเปรียบเทียบ</td></tr>
<tr><td>Model2</td><td>คน 3 คน เครื่องละคน</td><td>1 ชม.</td><td>356 ชิ้น</td><td>คนพอ ไม่เสียผลผลิต</td></tr>
<tr><td>Model3</td><td>คน 1 คน + Worker Chart</td><td>1 ชม.</td><td>94 ชิ้น</td><td>คนเดิน 21%</td></tr>
<tr><td>Model4</td><td>คน 2 คน Speed 1, Efficiency 90 / 80%</td><td>1 ชม.</td><td>152 ชิ้น</td><td>เดินช้า + ทำช้า</td></tr>
<tr><td>Model5</td><td>Model2 + ShiftCalendar 2 กะ</td><td>1 วัน</td><td>5,034 ชิ้น</td><td>ทำงาน 58% ของวัน</td></tr>
<tr><td>Model6</td><td>คน 2 คน ไลน์ I</td><td>1 ชม.</td><td>188 ชิ้น</td><td>คนเดิน 21%</td></tr>
<tr><td>Model7</td><td>คน 2 คน ไลน์ U</td><td>1 ชม.</td><td>204 ชิ้น</td><td>คนเดิน 14%</td></tr>
<tr><td>Model8</td><td>Model2 + Transport Importer ที่ Source</td><td>1 ชม.</td><td>255 ชิ้น</td><td>คนขน + เดิน ~10%</td></tr>
<tr><td>Model9</td><td>Model2 + ชิ้น A/B + ช่างตั้งเครื่อง 1 คน</td><td>1 ชม.</td><td>299 ชิ้น</td><td>ตั้งเครื่อง 4.4% + รอช่าง</td></tr>
<tr><td>Model10</td><td>Model2 + เครื่องเสีย 95% + ช่างซ่อม 1 คน</td><td>1 ชม.</td><td>271 ชิ้น</td><td>เสีย + รอช่างซ่อม</td></tr>
</table>
<div class="tip"><strong>เรื่องของบทนี้:</strong> คนพอ = ผลเท่าเดิม · คนไม่พอ = ผลลด · คนเดินช้า ทำงานช้า ผลลด · กะทำงานลดชั่วโมงผลิต
· จัดผังช่วยดึงกลับมาได้บางส่วน · ช่างแยกหน้าที่ต้องมี Service และ Workplace ของตัวเอง (เวลาเครื่อง 0:10 ต่อชิ้นทุกเครื่อง)</div>

<h2>ลองเอง: เปลี่ยนจำนวนคน ความเร็ว และค่าของช่าง</h2>
<table>
<tr><th>Frame</th><th>ลองเปลี่ยน</th><th>FG หลังรัน 1 ชม.</th><th>ทำไม</th></tr>
<tr><td>Model3</td><td>Workers to Create › Amount = 2</td><td>188</td><td>เหมือน Model6</td></tr>
<tr><td>Model4</td><td>ลบค่า Speed ทั้ง 2 แถว (ใช้ 1.5)</td><td>166</td><td>เหลือแต่ผลของ Efficiency</td></tr>
<tr><td>Model7</td><td>Amount = 1</td><td>102</td><td>ไลน์ U ช่วยคนเดียวได้เล็กน้อย (Model3 ได้ 94)</td></tr>
<tr><td>Model6 / Model7</td><td>Amount = 3</td><td>356</td><td>คนครบ ผังไม่มีผล</td></tr>
<tr><td>Model6</td><td>ย้าย Station2, 3 ให้ห่างกัน 6 m</td><td>156</td><td>เดินไกลขึ้น ได้น้อยลง</td></tr>
<tr><td>Model9</td><td>Set-up Time = 0:30 ทุกเครื่อง</td><td>238</td><td>ตั้งเครื่องนานขึ้น</td></tr>
<tr><td>Model9</td><td>Parts ชนิดละ 40 ชิ้น</td><td>322</td><td>เปลี่ยนชนิดน้อยลง ตั้งเครื่องน้อยลง</td></tr>
<tr><td>Model10</td><td>แถว Repairman › Amount = 2</td><td>290</td><td>เกือบเท่าไม่ต้องรอช่าง (292)</td></tr>
<tr><td>Model10</td><td>MTTR = 2:00 ทุกเครื่อง</td><td>242</td><td>ซ่อมนานขึ้น</td></tr>
</table>
<div class="tip"><strong>วิธีลอง:</strong> เดาก่อนแล้วรันดู · แก้ทีละแถวจากค่าเดิม · ย้ายเครื่องให้ย้าย Workplace ตามไปด้วย · กด <code>Reset</code> ก่อน <code>Start</code> ทุกครั้ง
· Model10 เครื่องเสียแบบสุ่ม ตัวเลขอาจต่างเล็กน้อยถ้ารันนานกว่า 1 ชั่วโมง</div>

<h2>ปัญหาที่พบบ่อย และวิธีแก้</h2>
<table>
<tr><th>อาการ</th><th>วิธีแก้</th></tr>
<tr><td>หยุดพร้อมข้อความ <em>does not have a free workplace</em></td><td>เครื่องนั้นไม่มี Workplace ของตัวเอง วาง Workplace ติดเครื่องแล้วเลือก Processing Importer</td></tr>
<tr><td>วาง Workplace แล้วไม่มี popup</td><td>วางไกลเครื่องเกินไป ลบแล้ววางใหม่ใต้ป้ายชื่อเครื่อง</td></tr>
<tr><td>คนยืนหันหลังให้เครื่อง</td><td>Workplace ไม่ได้วางติดเครื่อง วางใหม่ด้วยเมาส์ให้ชิดเครื่อง</td></tr>
<tr><td>รันแล้ว FG = 0 คนไม่มา</td><td>ตรวจ Broker ของเครื่อง (แท็บ Importer) และของ WorkerPool ต้องเป็นตัวเดียวกัน</td></tr>
<tr><td>ใส่ Speed = 1 แล้วผลลดลง</td><td>ช่องว่าง = 1.5 m/s ของคลาส Worker · ใส่ 1 คือให้เดินช้าลง ถ้าไม่ตั้งใจให้ลบค่าออก</td></tr>
<tr><td>Worker Chart มีแท่งเดียว</td><td>Group Workers By = Pool ทั้งกอง · Creation Table แยกตามแถวในตาราง Workers to Create</td></tr>
<tr><td>ShiftCalendar ไม่มีผล</td><td>ลาก WorkerPool และเครื่องไปปล่อยบน ShiftCalendar · รันนานกว่า 1 กะ</td></tr>
<tr><td>วาง Workplace เหนือเครื่องแล้วไลน์ค้าง FG = 0</td><td>เผลอเลือก Transport Importer ใน popup · Station › Importer › Transport เอาเครื่องหมายถูกที่ Active ออก</td></tr>
<tr><td>ช่างมาแล้วคนคุมเครื่องเดินออกไป</td><td>Workplace1–3 ยังรับทุก Service ช่างจึงไปยืนแทน · ตั้ง Supported Services = Processing</td></tr>
<tr><td>เปิด Failure Importer แล้วไลน์แทบหยุด (58)</td><td>Services ยังเป็น Failure คนคุมเครื่องต้องซ่อมกันเอง · ตั้ง Services = Repair และเพิ่มช่างซ่อม</td></tr>
<tr><td>ลาก object แล้วกลายเป็นแท่งใหม่ใน Chart</td><td>ปล่อยบน Chart = เพิ่มเข้า Chart ถ้าจะย้ายให้ปล่อยบนที่ว่าง</td></tr>
</table>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ใน Model2 (คน 3 คน) ให้คนที่ 3 เดินช้าลงเป็น Speed = 0.75 ผลยังได้ 356 แต่ถ้าให้คนที่ 3 มี Efficiency = 80% ผลลดเหลือ 285 — ทำไมสองค่านี้มีผลต่างกัน?
</div>
<div class="tip"><strong>เฉลย:</strong> เมื่อคนพอ (เครื่องละคน) คนยืนประจำเครื่อง ไม่ต้องเดิน Speed จึงไม่มีผล แต่ Efficiency เปลี่ยนเวลาทำงานต่อชิ้นเสมอ
เครื่องของคนนั้นช้าเป็น 12.5 วิ กลายเป็นคอขวด (3,600 ÷ 12.5 = 288) — คนช้าคนเดียวทำให้ทั้งไลน์ช้า
Speed จะมีผลก็ต่อเมื่อคนไม่พอและต้องเดินระหว่างเครื่อง เช่น Model3 (Speed 0.75 ได้ 77 จาก 94)</div>
'''
