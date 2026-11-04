# -*- coding: utf-8 -*-
"""Overview 4: Python GA Demo -- from PtS2606_3_PythonGADemo.pptx"""
from gen_site import screenshot, step_list, side_by_side

OBJECTIVES = [
    "ติดตั้ง pymoo และเปิดโมเดลตัวอย่าง Python GA Demo ให้รัน Python ได้ (อนุญาตให้โมเดลเข้าถึงคอมพิวเตอร์)",
    "อ่านโจทย์ ตั้งค่า GA ใน GAConfigure และรู้ว่า PythonModule แต่ละตัวทำอะไร",
    "รัน GA อ่าน Report และ Pareto Front แล้วใส่คำตอบกลับโมเดลด้วย Method ApplySolution ได้",
]

BODY = f'''
<p class="lead" style="max-width:46em;">โมเดลตัวอย่างตัวที่สามที่ติดมากับ Plant Simulation 2606 ต่อจาก <a href="overview-02.html">Factory 51</a>
และ <a href="overview-03.html">Small Parts Production</a> — ยังไม่ต้องสร้างโมเดลเอง แค่เปิดตัวอย่างของ Siemens ที่ใช้ Python
(ไลบรารี <strong>pymoo</strong>) หา<strong>ลำดับงาน</strong>และ<strong>ขนาด Buffer</strong> ที่ดีที่สุด 2 เป้าหมายพร้อมกัน ทั้งหมด 9 ขั้นตอน
ให้เห็นว่าโมเดลจำลองต่อกับ Python เพื่อหาคำตอบอัตโนมัติได้แบบไหน (บท 01–09 จะสอนสร้างโมเดลของตัวเอง เริ่มที่
<a href="lessons-01.html">บท 01 สร้างโมเดลแรก</a>)</p>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 · Python 3.12, 3.13 หรือ 3.14 · ไลบรารี pymoo (pip) · ไฟล์
<code>Examples\\Demo\\Python_GA_Demo.spp</code> &nbsp;·&nbsp; ผลที่วัดได้ใน 2606: ผลผลิต <strong>452 → 732 ชิ้น/วัน</strong> หลังใช้คำตอบของ GA
</div>
<div class="note"><strong>2 เป้าหมายพร้อมกัน:</strong> ผลผลิตสูงสุด + ต้นทุน Buffer ต่ำสุด → GA ไม่ได้ให้คำตอบเดียว แต่ให้ชุดคำตอบที่ดีคนละด้าน
(Pareto) ให้คนเลือก</div>

<h2>ภาพรวม 9 ขั้นตอน</h2>
<table>
<tr><th>ขั้น</th><th>หัวข้อ</th><th>ทำอะไร</th></tr>
<tr><td>1</td><td>ติดตั้ง pymoo</td><td><code>python -m pip install pymoo</code></td></tr>
<tr><td>2</td><td>เปิดตัวอย่าง + Save As</td><td><code>Examples\\Demo\\Python_GA_Demo.spp</code></td></tr>
<tr><td>3</td><td>อนุญาต Python</td><td><code>Model Settings › Security</code></td></tr>
<tr><td>4</td><td>อ่านโจทย์</td><td>ไลน์ 10 ชนิด มี Set-up · 452 ชิ้น/วัน</td></tr>
<tr><td>5</td><td>ตั้งค่า GA</td><td>GAConfigure: 10 รุ่น × 30 คำตอบ</td></tr>
<tr><td>6</td><td>ดูโค้ด Python</td><td>9 PythonModule + SimTemplate</td></tr>
<tr><td>7</td><td>กด Start/Stop</td><td>13–25 วินาทีบนเครื่องที่ทดสอบ</td></tr>
<tr><td>8</td><td>อ่าน Report</td><td>กราฟ 2 เป้าหมาย + Pareto</td></tr>
<tr><td>9</td><td>ใส่คำตอบกลับโมเดล</td><td>Method ApplySolution → 732</td></tr>
</table>

<h2>Workflow: ใครทำอะไร</h2>
<table>
<tr><th>ลำดับ</th><th>งาน</th><th>รายละเอียด</th><th>ใครทำ</th></tr>
<tr><td>1</td><td>เตรียมเครื่อง</td><td>ติดตั้ง pymoo · อนุญาตให้โมเดลเข้าถึงคอมพิวเตอร์ · Save ไฟล์</td><td>ผู้ใช้ (ขั้น 1–3)</td></tr>
<tr><td>2</td><td>ตั้งโจทย์</td><td>GAConfigure: ตัวแปร ช่วงค่า ต้นทุน จำนวนรุ่น</td><td>ผู้ใช้ (ขั้น 4–5)</td></tr>
<tr><td>3</td><td>สร้างคำตอบ</td><td>pymoo (NSGA-II) สุ่ม ผสม กลายพันธุ์ คำตอบรุ่นละ 30 ตัว</td><td>Python</td></tr>
<tr><td>4</td><td>ประเมินคำตอบ</td><td>PlantSimulationConsole รันโมเดล 1 วันต่อคำตอบ อ่านผลที่ Drain</td><td>PtS Console</td></tr>
<tr><td>5</td><td>เลือกคำตอบ</td><td>อ่าน Report + Pareto · ใส่คำตอบกลับ · รันยืนยัน</td><td>ผู้ใช้ (ขั้น 8–9)</td></tr>
</table>
<p>ในตัวเลข (วัดใน PtS 2606): <strong>10</strong> รุ่น (Generations) · <strong>30</strong> คำตอบต่อรุ่น · <strong>2</strong> เป้าหมายพร้อมกัน ·
ผลผลิตเพิ่ม <strong>62%</strong> (คำตอบที่ 1)</p>
<div class="tip"><strong>เบื้องหลัง:</strong> Python ไม่ได้รันโมเดลเอง แต่เขียนไฟล์ SimTalk แล้วเรียก <code>PlantSimulationConsole.exe</code>
ให้เปิดไฟล์ <code>.spp</code> ที่ Save ไว้มารันทีละคำตอบ ผลผลิตที่ได้ส่งกลับให้ pymoo คิดรุ่นถัดไป</div>

<h2>ขั้นที่ 1: ติดตั้ง Python และ pymoo</h2>
{screenshot("assets/images/overview/04-01.jpg", "Command Prompt: ตรวจรุ่น Python ติดตั้ง และตรวจ pymoo")}
{step_list([
    "<code>python --version</code> — ต้องเป็น 3.12, 3.13 หรือ 3.14 (Help 2606) · เครื่องที่ทดสอบใช้ 3.14.6",
    "<code>python -m pip install pymoo</code> — ติดตั้ง pymoo พร้อม numpy, scipy, matplotlib",
    "<code>python -m pip show pymoo</code> — ตรวจว่าติดตั้งแล้ว · เครื่องที่ทดสอบได้ Version 0.6.2",
])}
<div class="note"><strong>มี Python หลายตัว:</strong> ใช้ <code>setPythonDLLPath("...\\python314.dll")</code> ระบุตัวที่ Plant Simulation ใช้ (Help 2606)
· ติดตั้งให้เสร็จก่อนเปิด Plant Simulation</div>
<p>ติดตั้งครั้งเดียวต่อเครื่อง — ภาพนี้ถ่ายหลังติดตั้งแล้วจึงขึ้น <em>Requirement already satisfied</em> ถ้าติดตั้งครั้งแรกจะขึ้น
<em>Successfully installed ... pymoo-0.6.2</em></p>

<h2>ขั้นที่ 2: เปิดตัวอย่าง Python_GA_Demo แล้ว Save As</h2>
{side_by_side(
    screenshot("assets/images/overview/04-02.jpg", "Frame Example มองจากด้านบน: ไลน์ผลิต แผง Python GA, ReadMe และ Current Limitations"),
    step_list([
        "<strong>Example</strong> — ไลน์ผลิตที่ GA จะปรับ (ขั้นที่ 4)",
        "<strong>Python GA</strong> — แผงควบคุม: Start/Stop, Show Report, Drop-down เลือกคำตอบ",
        "<strong>ReadMe</strong> — วิธีใช้ 5 ข้อจาก Siemens",
        "<strong>Current Limitations</strong> — ปรับได้แค่ลำดับ + ขนาด Buffer · เป้าหมายตายตัว · ประเมินคำตอบละ 1 รอบ",
    ])
)}
<div class="note"><strong>เปิดไฟล์:</strong> <code>File › Open</code> → <code>...\\Plant Simulation 2606\\Examples\\Demo\\Python_GA_Demo.spp</code>
แล้ว <code>File › Save As</code> ไปโฟลเดอร์ของตัวเองทันที (GA ใช้ไฟล์ที่ Save ไว้) &nbsp;·&nbsp; Class Library › Models › Example</div>
<p>Plant Simulation เปิดโมเดลเป็น 3D ภาพนี้เป็นมุมมองจากด้านบน (Planning View) — Frame GA ถูกวางเป็นแผงสีน้ำเงินใน Example</p>

<h2>ขั้นที่ 3: อนุญาตให้โมเดลเรียก Python</h2>
{side_by_side(
    screenshot("assets/images/overview/04-03.jpg", "หน้าต่าง Model Settings แท็บ General ส่วน Security"),
    step_list([
        "<code>File › Model Settings</code> แท็บ <code>General</code>",
        "<strong>Security</strong> — คลิกช่อง <code>Prohibit Access to the Computer</code> ให้เครื่องหมายถูกหายไป ☐ (ตัวอย่างเปิดไว้ ☑)",
        "<code>OK</code> แล้ว <code>File › Save</code>",
    ])
)}
<div class="note"><strong>ทำไม:</strong> ถ้ายังมีเครื่องหมายถูก ☑ PythonModule รันโค้ดไม่ได้ (Help 2606) · กด Start/Stop แล้วขึ้น error
<em>Access to the computer is prohibited</em> · ปิดเฉพาะโมเดลที่ไว้ใจ</div>

<h2>ขั้นที่ 4: โจทย์ — ไลน์ 10 ชนิด เปลี่ยนชนิดต้อง Set-up</h2>
{screenshot("assets/images/overview/04-04.jpg", "Frame Example หลังรัน 1 วัน: Source, Station, Buffer, Station2, Drain")}
{step_list([
    "<strong>Source</strong> — ปล่อยงาน 10 ชนิด T1–T10 วนตามลำดับในตาราง <code>Delivery</code>",
    "<strong>Station</strong> — 0:10 ต่อชิ้น + Set-up เมื่อเปลี่ยนชนิด",
    "<strong>Buffer</strong> — ความจุ 15 ชิ้น",
    "<strong>Station2</strong> — Negexp เฉลี่ย 1:00 + เครื่องเสีย (Availability 95%)",
    "<strong>452 ชิ้น</strong> — ผลผลิต 1 วัน (ลำดับเดิม, Buffer 15)",
])}
<div class="note"><strong>โจทย์ของ GA:</strong> หาลำดับ T1–T10 และความจุ Buffer (1–20) ที่ได้ชิ้นงานมากที่สุด และจ่ายค่า Buffer น้อยที่สุด (1 หน่วยต่อ 1 ช่อง)</div>

<h3>Set-up ตามชนิด — ตาราง setupMatrix</h3>
<p>ดับเบิลคลิก <code>Station</code> › แท็บ <code>Times</code> แล้วดับเบิลคลิก <code>setupMatrix</code></p>
{screenshot("assets/images/overview/04-05.jpg", "แท็บ Times ของ Station: Set-up Time = Matrix(Type)")}
{screenshot("assets/images/overview/04-06.jpg", "ตาราง setupMatrix: เวลา Set-up ระหว่างชนิด T1–T10")}
{step_list([
    "<code>Set-up Time = Matrix(Type)</code> — ดูเวลาในตาราง setupMatrix ตามชนิดชิ้นงาน",
    "<strong>แถว / คอลัมน์ = ชนิดก่อน–หลัง</strong> — ห่างกัน 1 ชนิด = 1:00 · ห่าง 9 ชนิด = 9:00",
    "<strong>ชนิดเดียวกัน = 0</strong> — ไม่ต้อง Set-up",
    '<strong>แถว "-"</strong> — ชิ้นแรก ยังไม่มีชนิดก่อนหน้า',
])}
<div class="note"><strong>ลำดับเดิมเสียเวลา:</strong> T5 T6 T4 T1 T3 T7 T2 T8 T9 T10 → Set-up รวม 30 นาทีต่อ 10 ชิ้น (คิดจากตาราง)
· ลำดับที่ไล่ชนิดใกล้กัน ต่ำสุด 18 นาที</div>
<p>ตรวจได้: 10 ชิ้นใช้ 100 วินาที + 30 นาที ≈ 31.7 นาที → 1 วันได้ราว 455 ชิ้น ใกล้กับ 452 ที่วัดได้
(30 และ 18 นาทีคิดจากตาราง setupMatrix รวมตอนวนกลับจาก T10 ไป T5 ไม่ได้วัดจากโมเดล)</p>

<h2>ขั้นที่ 5: ตั้งค่า GA ใน Method GAConfigure</h2>
<p>ดับเบิลคลิก <code>GAConfigure</code> (ภาพบน) และตาราง <code>GA.Input</code> (ภาพล่าง)</p>
{screenshot("assets/images/overview/04-07.jpg", "โค้ดใน Method GAConfigure และตาราง GA.Input")}
{step_list([
    "<code>Generations 10, Population 30</code> — 10 รุ่น รุ่นละ 30 คำตอบ",
    "<code>Parallel false, Threads 1</code> — รันทีละคำตอบ",
    "<strong>ตัวแปรที่ 1</strong> <code>root.Buffer.Capacity</code> ช่วง 1–20 ต้นทุน 1 ต่อช่อง",
    "<strong>ตัวแปรที่ 2</strong> <code>root.Delivery</code> = ลำดับของ 10 ชนิด",
])}
<div class="tip"><strong>ตาราง GA.Input:</strong> ค่าของตัวอย่างอยู่ในตารางนี้แล้ว คอลัมน์ variable / min / max / cost · บทนี้ใช้ค่าเดิม
(ยังไม่ได้ทดสอบการแก้โจทย์) — ตัวแปรแบบ Buffer มี min max cost ตัวแปรแบบตารางลำดับใส่แค่ชื่อตาราง</div>

<h2>ขั้นที่ 6: ข้างใน Frame GA — PythonModule ทำอะไรบ้าง</h2>
<p>ดับเบิลคลิก Frame <code>GA</code></p>
{screenshot("assets/images/overview/04-08.jpg", "Frame GA: แผง Python GA, GA Logic และ PythonModule ทั้งหมด")}
{step_list([
    "<strong>Optimizer</strong> — เริ่มที่นี่: ตั้ง NSGA-II ของ pymoo แล้วสั่งค้นหา",
    "<strong>Problem</strong> — อ่าน GA.Input → ตัวแปร 11 ตัว (Buffer 1 + ลำดับ 10)",
    "<strong>FitnessEvaluator</strong> — ให้คะแนน 2 ค่า: ผลผลิต + ต้นทุน Buffer",
    "<strong>SimHandler</strong> — เขียนไฟล์ simtalk แล้วเรียก PlantSimulationConsole.exe",
    "<strong>SimTemplate</strong> — Method ที่ Console รันกับทุกคำตอบ",
    "<strong>HtmlReport</strong> — HTMLHandler วาดกราฟ · SolutionHandler เขียน Solutions + Drop-down",
    "<strong>Custom…</strong> — สุ่ม / ผสม / กลายพันธุ์ แยกยีนลำดับกับยีน Buffer",
])}
<p>จากโค้ดในโมเดล: ยีนลำดับใช้ Edge Recombination + Inversion · ยีน Buffer ใช้ Uniform crossover + PM mutation ·
ประชากร 30 รุ่นละ 30 ลูก ตัดคำตอบซ้ำ</p>

<h3>โค้ด Python ในโมดูล Optimizer</h3>
{side_by_side(
    screenshot("assets/images/overview/04-09.jpg", "หน้าต่าง PythonModule Optimizer"),
    step_list([
        "<code>from pymoo…</code> — ใช้ NSGA-II และตัวดำเนินการของ pymoo (ติดตั้งในขั้นที่ 1)",
        "<code>import PlantSimulation as ps</code> — ตัวเชื่อม Python กับโมเดล",
        "<code>ps.importPythonModule(current.Problem)</code> — เรียกโมดูลอื่นใน Frame เดียวกัน (<code>current</code> = Frame GA)",
        "<code>Import</code> — โหลดโค้ดเข้า Python หลังแก้ (<code>Shift + Import</code> = ล้างค่าเดิม, Help 2606)",
    ])
)}
<div class="tip"><strong>NSGA-II:</strong> GA หลายเป้าหมาย — เก็บทุกคำตอบที่ไม่มีคำตอบอื่นดีกว่าทุกด้าน (Pareto) แทนการรวมเป็นคะแนนเดียว
· ฟังก์ชัน start ในโมดูลนี้ถูกเรียกเมื่อคลิก Start/Stop และรัน GA ใน thread แยก</div>

<h2>ขั้นที่ 7: คลิก Start/Stop แล้วรอ</h2>
{screenshot("assets/images/overview/04-10.jpg", "แผง Python GA: ซ้าย = กำลังรัน, ขวา = จบแล้ว")}
{step_list([
    "<code>Start/Stop</code> — คลิกแล้วไฟเป็นสีเขียว = GA กำลังรัน",
    "<code>OptimizationDone</code> ✗ ระหว่างรัน",
    "<code>OptimizationDone</code> ✓ จบแล้ว 13–25 วินาทีบนเครื่องที่ทดสอบ (5 รอบ)",
    "<strong>Drop-down</strong> — แสดงคำตอบ เช่น <code>Throughput: 732 Cost: 7</code>",
])}
<div class="note"><strong>แก้โมเดลแล้วต้อง Save:</strong> GA รันไฟล์ <code>.spp</code> ที่ Save ไว้ผ่าน PlantSimulationConsole ไม่ใช่โมเดลที่เปิดอยู่
· คลิก Start/Stop อีกครั้ง = หยุดกลางทาง · ถ้าเกิด error ให้ปิด Plant Simulation แล้วเปิดใหม่ตาม ReadMe</div>

<h2>ขั้นที่ 8: Show Report — ผลดีขึ้นทุกรุ่น</h2>
<p>คลิก <code>Show Report</code> — HtmlReport เปิดเป็นแท็บในหน้าต่างหลัก</p>
{screenshot("assets/images/overview/04-11.jpg", "HtmlReport: กราฟ Throughput และ Cost ตามรุ่น")}
{step_list([
    "<strong>Number of Generations 10, Population 30</strong> — ตามที่ตั้งในขั้นที่ 5",
    "<strong>เส้นเขียว = ดีที่สุดในรุ่น</strong> — ผลผลิตขึ้นถึง 732 ราวรุ่นที่ 5–6",
    "<strong>เส้นน้ำเงิน = ค่าเฉลี่ย</strong> — จาก ~370 เป็น ~655 ทั้งรุ่นดีขึ้น",
    "<strong>Cost</strong> — เส้นเขียว = ต่ำสุด 1 ตั้งแต่รุ่นแรก",
])}
<div class="tip"><strong>อ่านกราฟ:</strong> ผลผลิต (Throughput) ยิ่งสูงยิ่งดี · ต้นทุน (Cost) ยิ่งต่ำยิ่งดี · เส้นเขียวคือด้านที่ดีของทั้งสองกราฟ
(ค่าเฉลี่ยอ่านจากกราฟโดยประมาณ ค่า 732 และ 1 อ่านจากตาราง Solutions)</div>

<h3>Pareto Front — 2 คำตอบ ให้คนเลือก</h3>
<p>เลื่อนลงใน HtmlReport</p>
{screenshot("assets/images/overview/04-12.jpg", "Current Pareto Front และ Solution Table")}
{step_list([
    "<strong>704 ชิ้น ต้นทุน 1</strong> — Buffer 1 ช่อง",
    "<strong>732 ชิ้น ต้นทุน 7</strong> — Buffer 7 ช่อง",
    "<strong>Solution Table</strong> — ค่ายีนของแต่ละคำตอบ: Buffer + ตำแหน่งของ T1–T10",
])}
<div class="note"><strong>Pareto Front:</strong> ไม่มีคำตอบไหนดีกว่าทุกด้าน — ได้เพิ่ม 28 ชิ้น/วัน ต้องเพิ่ม Buffer 6 ช่อง → คนตัดสินใจว่าคุ้มหรือไม่
· GA รัน 5 รอบบนเครื่องที่ทดสอบ ได้ 2 คำตอบนี้ทุกรอบ เพราะโค้ดตั้ง seed = 3 ไว้คงที่</div>

<h2>ขั้นที่ 9: Drop-down ใน 2606 ใส่คำตอบไม่ครบ</h2>
{side_by_side(
    screenshot("assets/images/overview/04-13.jpg", "Drop-down ในแผง Python GA แสดง 2 คำตอบ"),
    step_list([
        "<strong>เลือกคำตอบใน Drop-down</strong> — SolutionHandler เขียนคำตอบลงโมเดล",
    ])
)}
<p><strong>วัดจริง:</strong> Buffer เปลี่ยนเป็น 7 / 1 แต่ลำดับใน Delivery ไม่เปลี่ยน → รันได้แค่ 452 / 450 ชิ้น &nbsp;·&nbsp;
<strong>ที่เห็นในโค้ด:</strong> ไม่ได้เรียงแถวตาม Orig ก่อนแบบที่ SimTemplate ทำ และเขียนยีนลำดับแค่ 9 จาก 10 ช่อง</p>
<table>
<tr><th>วิธีใส่คำตอบ (รัน Example 1 วัน)</th><th>คำตอบ 1 (Buffer 7)</th><th>คำตอบ 2 (Buffer 1)</th></tr>
<tr><td>GA รายงาน (Solutions)</td><td>732</td><td>704</td></tr>
<tr><td>Drop-down ของตัวอย่าง</td><td>452</td><td>450</td></tr>
<tr><td>Method ApplySolution (ด้านล่าง)</td><td>732</td><td>704</td></tr>
</table>
<div class="note"><strong>สรุป:</strong> ใช้ Drop-down ดูรายการคำตอบได้ แต่ใส่คำตอบลงโมเดลด้วย Method ApplySolution (ด้านล่าง) แล้วรันยืนยันทุกครั้ง
(ทดสอบใน PtS 2606 ทั้ง 2 คำตอบหลัง Reset โมเดล)</div>

<h3>ใส่คำตอบด้วย Method ApplySolution</h3>
<p><strong>สร้าง Method:</strong> <code>Toolbox › Information Flow › Method</code> ลากลง Frame <code>Example</code> ตั้งชื่อ <code>ApplySolution</code> แล้ววางโค้ดนี้:</p>
<pre><code>var i := 1                                   // row of GA.Solutions (1 = highest throughput)
// apply Pareto solution i (row i of GA.Solutions) the way GA.SimTemplate does
EventController.reset
Delivery.sort(4, "up")                       // column Orig: rows back to T1..T10
for var p := 1 to Delivery.YDim
    Delivery[5, p] := GA.Solutions[4 + p, i]   // genes -&gt; column Chrom
next
Delivery.sort(5, "up")                       // column Chrom: the new order
Buffer.Capacity := GA.Solutions[4, i]</code></pre>
{screenshot("assets/images/overview/04-14.jpg", "โค้ด ApplySolution และ Frame Example หลังรัน 1 วันได้ 732 ชิ้น")}
{step_list([
    "<code>var i := 1</code> — แถวของ GA.Solutions (1 = 732, 2 = 704)",
    "<code>Reset</code> — ล้างชิ้นงาน ก่อนลดความจุ Buffer",
    "<strong>เรียง Orig → ใส่ Chrom → เรียง Chrom</strong> — ได้ลำดับใหม่ แบบเดียวกับ SimTemplate",
    "<code>Buffer.Capacity</code> ตามคำตอบ แล้วกด <code>F5</code> ในหน้าโค้ด",
    "<code>Start</code> ที่ EventController — รัน 1 วัน ได้ 732 ชิ้น",
])}
<div class="tip"><strong>ทดสอบแล้วใน 2606:</strong> i = 1 ได้ 732, i = 2 ได้ 704</div>

<h2>สรุปผล: ไลน์เดิม เทียบคำตอบของ GA (วัดใน 2606)</h2>
<table>
<tr><th>หัวข้อ</th><th>ไลน์เดิม</th><th>คำตอบ 1</th><th>คำตอบ 2</th></tr>
<tr><td>ลำดับใน Delivery</td><td>T5 T6 T4 T1 T3 T7 T2 T8 T9 T10</td><td>T2 T1 T3 T6 T10 T9 T8 T7 T5 T4</td><td>T9 T10 T8 T4 T3 T1 T2 T5 T6 T7</td></tr>
<tr><td>Buffer (= ต้นทุน)</td><td>15</td><td>7</td><td>1</td></tr>
<tr><td>Set-up ต่อรอบ 10 ชิ้น</td><td>30 นาที</td><td>18 นาที</td><td>18 นาที</td></tr>
<tr><td>ผลผลิต 1 วัน</td><td>452 ชิ้น</td><td>732 ชิ้น (+62%)</td><td>704 ชิ้น (+56%)</td></tr>
</table>
<p>ผลผลิตวัดจริง: รัน Example 1 วันหลังใส่คำตอบด้วย ApplySolution · Set-up คิดจาก setupMatrix · GA 5 รอบ ได้ 2 คำตอบเดิมทุกรอบ</p>

<h2>Python GA เทียบ GAWizard ในโปรแกรม</h2>
<table>
<tr><th>หัวข้อ</th><th>GAWizard (มีในโปรแกรม)</th><th>Python GA Demo (pymoo)</th></tr>
<tr><td>ติดตั้งเพิ่ม</td><td>ไม่ต้อง</td><td>Python 3.12–3.14 + pymoo · ปิด Prohibit Access</td></tr>
<tr><td>เป้าหมาย</td><td>ค่า Fitness เดียว (รวมหลายเรื่องเป็นคะแนนเดียว)</td><td>2 เป้าหมายแยกกัน → ชุดคำตอบ Pareto</td></tr>
<tr><td>ตั้งโจทย์</td><td>หน้าต่าง GAWizard + ตาราง GA</td><td>Method GAConfigure + ตาราง Input</td></tr>
<tr><td>ปรับวิธีของ GA</td><td>ตามตัวเลือกในหน้าต่าง</td><td>แก้โค้ด Python ได้ทุกส่วน</td></tr>
<tr><td>ข้อจำกัดของตัวอย่าง</td><td>—</td><td>ลำดับ + Buffer เท่านั้น · เป้าหมายตายตัว · คำตอบละ 1 รอบ</td></tr>
</table>
<div class="tip"><strong>เลือกใช้:</strong> เลือก GAWizard เมื่อโจทย์มีเป้าหมายเดียวและไม่อยากติดตั้งอะไรเพิ่ม · เลือก Python GA เมื่ออยากเห็น trade-off
หลายเป้าหมาย หรือต้องการปรับวิธีค้นหาเอง (คอลัมน์ Python GA มาจากตัวอย่างนี้และ Current Limitations ของ Siemens)</div>

<h2>ปัญหาที่พบบ่อย และวิธีแก้ (2606)</h2>
<table>
<tr><th>อาการ</th><th>วิธีแก้</th></tr>
<tr><td>กด Start/Stop แล้วขึ้น <em>Access to the computer is prohibited</em></td><td>ขั้นที่ 3: คลิกช่อง <code>Prohibit Access to the Computer</code> ออก แล้ว Save</td></tr>
<tr><td>Python หา pymoo ไม่เจอ</td><td><code>pip install pymoo</code> ใน Python ตัวที่ Plant Simulation ใช้ (<code>setPythonDLLPath</code> ถ้ามีหลายตัว)</td></tr>
<tr><td>Python รุ่นเก่ากว่า 3.12</td><td>2606 รองรับ 3.12, 3.13, 3.14 เท่านั้น (Help 2606)</td></tr>
<tr><td>เลือก Drop-down แล้วผลผลิตยังเท่าเดิม (452)</td><td>ใส่คำตอบด้วย Method ApplySolution (ขั้นที่ 9)</td></tr>
<tr><td><code>ValueError: Capacity … must not be smaller than the number of MUs</code></td><td>Reset โมเดลก่อนใส่คำตอบ (ApplySolution ทำให้แล้ว)</td></tr>
<tr><td>แก้โมเดลแล้ว GA ยังให้ผลเดิม</td><td>Save ก่อนกด Start/Stop: GA รันไฟล์ที่ Save ไว้</td></tr>
<tr><td>Error แล้วกดใหม่ไม่ทำงาน</td><td>ปิด Plant Simulation แล้วเปิดใหม่ (ReadMe) · numpy ไม่รองรับการเริ่ม Python ใหม่ในโปรแกรมเดิม (Help)</td></tr>
<tr><td>รันหลายรอบได้คำตอบเดิม</td><td>ปกติ: Optimizer ตั้ง seed = 3 · แต่ละคำตอบประเมินแค่ 1 รอบ</td></tr>
</table>

<div class="note">
<strong>คำถามฝึกคิด:</strong> คำตอบ 1 และคำตอบ 2 มีเวลา Set-up เท่ากัน (18 นาทีต่อรอบ 10 ชิ้น) แต่ทำไมคำตอบ 1 ได้ผลผลิตมากกว่า 28 ชิ้น/วัน?
</div>
<div class="tip"><strong>เฉลย:</strong> ต่างกันที่ขนาด Buffer (7 กับ 1) — Station2 มีเวลาสุ่ม (Negexp เฉลี่ย 1:00) และเครื่องเสีย (Availability 95%)
จึงต้องมีที่พักงานหน้า Station2 Buffer ที่ใหญ่กว่าช่วยให้ไลน์ไม่สะดุด แต่ต้องจ่ายต้นทุนเพิ่ม 6 ช่อง — คนต้องเลือกจาก Pareto ว่าคุ้มหรือไม่
· ต่อไปเริ่มสร้างโมเดลของตัวเองที่ <a href="lessons-01.html">บท 01 สร้างโมเดลแรก</a></div>
'''
