# -*- coding: utf-8 -*-
"""Generates all 19 chapter pages + regenerates basic.html hub for consistency.
Run after gen_site.py (reuses its templates by importing it)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_site import SECTIONS, SECTION_ORDER, page_html, chapter_filename, hub_page, write, HUB_INTRO, HUB_CARD_DESC, youtube_embed, screenshot, step_list, side_by_side

# ---------------------------------------------------------------------------
# Chapter objectives (2-3 goals per chapter, "เพื่อ..." style)
# ---------------------------------------------------------------------------
OBJECTIVES = {
    ("basic", 1): ["เข้าใจว่า Discrete Event Simulation (DES) คืออะไร และต่างจากการคำนวณด้วยมือแบบธรรมดาอย่างไร",
                   "รู้ว่า Plant Simulation ใช้แก้ปัญหาแบบไหนได้บ้างในงานจริง",
                   "เห็นภาพรวมว่าตลอดคอร์สนี้จะได้เรียนอะไรบ้าง"],
    ("basic", 2): ["จำตำแหน่งและหน้าที่ของส่วนประกอบหลักในโปรแกรมได้",
                   "เปิดโปรแกรม สร้างไฟล์โมเดลใหม่ และรู้จัก Frame ได้ด้วยตัวเอง"],
    ("basic", 3): ["จำ Object พื้นฐาน 6 ตัวที่ใช้บ่อยที่สุด และหน้าที่ของแต่ละตัวได้",
                   "รู้ว่า Object แต่ละตัวมีค่า (Attribute) สำคัญอะไรที่ต้องตั้ง"],
    ("basic", 4): ["ลากวางและเชื่อมต่อ Object เป็นสายการผลิตง่ายๆ ได้ด้วยตัวเอง",
                   "ตั้งค่า Interval และ Processing Time ได้ถูกต้อง"],
    ("basic", 5): ["รันและ Reset ซิมูเลชันได้อย่างถูกวิธี",
                   "อ่านและตีความค่า Working / Waiting / Blocked ได้"],
    ("basic", 6): ["บันทึกไฟล์โมเดล (.spp) และเปิดไฟล์เดิมกลับมาทำต่อได้",
                   "มีนิสัยสำรองไฟล์ที่ปลอดภัย ก่อนไฟล์เสียหรือหาย"],

    ("intermediate", 1): ["แยกความแตกต่างของ Buffer/Store, AssemblyStation, Track และ Transporter ได้",
                          "เลือกใช้ Object ที่เหมาะกับสถานการณ์ในโมเดลจริงได้"],
    ("intermediate", 2): ["เข้าใจว่า MU (Movable Unit) คืออะไร และทำไมต้องสร้าง MU class ของตัวเอง",
                          "สร้างและกำหนดให้ Source ผลิต MU class ที่กำหนดเองได้"],
    ("intermediate", 3): ["เข้าใจว่าทำไมค่าคงที่ไม่สะท้อนความจริง และ Distribution แก้ปัญหานี้อย่างไร",
                          "เลือกและตั้งค่า Distribution ที่เหมาะกับ Interval/ProcTime ได้"],
    ("intermediate", 4): ["เข้าใจแนวคิด MTTR/MTBF และผลกระทบต่อสายการผลิต",
                          "ตั้งค่า Failure บน Object ประเภทประมวลผลได้"],
    ("intermediate", 5): ["อ่านผัง Sankey และสีของ Statistics ได้ถูกต้อง",
                          "ใช้ Bottleneck Analyzer หาสถานีที่เป็นคอขวดของสายการผลิตได้"],
    ("intermediate", 6): ["ห่อกลุ่ม Object เป็น Sub-frame และเชื่อมพอร์ตเข้า-ออกได้",
                          "นำโมดูลที่ห่อไว้กลับมาใช้ซ้ำในโมเดลอื่นได้"],

    ("advanced", 1): ["เขียน SimTalk 2.0 ตาม syntax ที่ยืนยันแล้วว่ารันได้จริง ไม่ใช่ syntax เก่า",
                      "เข้าใจโครงสร้าง method header, ตัวแปร, for-loop และ if ใน SimTalk 2.0"],
    ("advanced", 2): ["ผูก Method เข้ากับเหตุการณ์ Entrance/Exit ของสถานีได้",
                      "ใช้ Trigger ให้ Method ทำงานเป็นระยะเวลาซ้ำๆ ได้"],
    ("advanced", 3): ["สร้างและเข้าถึง DataTable/Variable จากโค้ดได้ โดยไม่ติดกับดัก auto-deref",
                      "อ่าน-เขียนค่าในตารางด้วย bracket indexing ได้ถูกต้อง"],
    ("advanced", 4): ["สร้าง Frame และ Object ด้วย createObject จากโค้ดล้วนๆ ได้",
                      "เชื่อมต่อ Object ด้วย Connector.connect และทำให้ Transporter ขับเคลื่อนเองได้"],
    ("advanced", 5): ["ตั้งค่า Scenario หลายชุดใน Experiment Manager ได้",
                      "เปรียบเทียบผลลัพธ์ระหว่าง Scenario เพื่อใช้ตัดสินใจได้"],
    ("advanced", 6): ["เข้าใจขอบเขตของ GAWizard และวิธีตั้งค่าผ่าน GUI",
                      "รู้ว่าเมื่อไหร่ควรใช้ GAWizard กับเมื่อไหร่ควรเขียน optimization เอง"],
    ("advanced", 7): ["เชื่อมต่อ Plant Simulation จากภายนอกผ่าน COM ด้วย Python ได้",
                      "รันโมเดลแบบ headless (ไม่มีหน้าต่างโปรแกรม) สำหรับงาน automation ได้"],

    ("object-reference", 1): ["จำ Object สาย Material Flow ที่ใช้บ่อยที่สุดและหน้าที่ของแต่ละตัวได้ไว",
                              "ทำตามสาธิตสั้นๆ ของแต่ละ Object เพื่อเห็นพฤติกรรมจริงด้วยตาตัวเอง"],
    ("object-reference", 2): ["เข้าใจว่า Object สาย Information Flow แต่ละตัวมีไว้ทำอะไร",
                              "รู้ว่าจะไปดูรายละเอียดเชิงลึกของแต่ละตัวต่อได้จากบทไหน"],
    ("object-reference", 3): ["รู้จัก Object ประเภททรัพยากรและเครื่องมือวิเคราะห์ที่มีให้ใช้",
                              "เลือกเครื่องมือที่เหมาะกับคำถามที่ต้องการตอบได้"],

    ("case-study", 1): ["เห็นตัวอย่างการประยุกต์ใช้ Plant Simulation ในสายการประกอบยานยนต์จริง",
                        "เชื่อมโยงความรู้จากหลายบทเข้าด้วยกันเป็นโมเดลเดียว"],
    ("case-study", 2): ["เห็นตัวอย่างการจำลองคลังสินค้าและระบบขนส่งภายในด้วย Transporter/Track",
                        "เข้าใจโจทย์เฉพาะของงานโลจิสติกส์ที่ต่างจากสายการผลิตทั่วไป"],
    ("case-study", 3): ["เห็นตัวอย่างการจำลองสาย SMT ที่ต้องการความแม่นยำและ Failure สูง",
                        "เข้าใจว่าทำไมอุตสาหกรรมอิเล็กทรอนิกส์ให้ความสำคัญกับ Yield/Rework"],
    ("case-study", 4): ["เห็นตัวอย่างการจำลองสายบรรจุภัณฑ์อาหารที่มีข้อจำกัดเรื่องเวลา",
                        "เข้าใจการนำ Distribution และ Failure มาใช้ร่วมกันในโจทย์จริง"],

    ("tips-tricks", 1): ["รู้ทางลัดที่ช่วยให้ทำงานกับโปรแกรมเร็วขึ้นในชีวิตประจำวัน"],
    ("tips-tricks", 2): ["รู้ข้อผิดพลาดที่มือใหม่เจอบ่อย และวิธีเช็คให้ไวก่อนเสียเวลาไล่บั๊กผิดจุด"],
    ("tips-tricks", 3): ["รู้เทคนิคที่ช่วยให้โมเดลใหญ่รันเร็วขึ้นโดยไม่กระทบผลลัพธ์"],
    ("tips-tricks", 4): ["รู้กับดัก syntax/COM ที่พบบ่อยที่สุดเวลาเขียนสคริปต์ควบคุมโมเดล"],
}

# ---------------------------------------------------------------------------
# Chapter bodies (content sections, HTML)
# ---------------------------------------------------------------------------
BODY = {}

BODY[("basic", 1)] = f'''
<h2>Discrete Event Simulation คืออะไร</h2>
<p>Plant Simulation จำลองระบบแบบ <strong>Discrete Event Simulation (DES)</strong> — คือการจำลอง
"เหตุการณ์" ที่เกิดขึ้นเป็นจุดๆ ตามเวลา (เช่น ชิ้นงานมาถึง, เครื่องเริ่มทำงาน, เครื่องทำงานเสร็จ)
แทนที่จะคำนวณทุกวินาทีต่อเนื่อง ทำให้จำลองกระบวนการผลิตหลายวัน/หลายเดือนได้ในเวลาไม่กี่วินาทีบนคอมพิวเตอร์</p>

{side_by_side(
    screenshot("assets/images/basic/01-01.png", "ตัวอย่างโมเดล 3D ของสายการผลิตใน Plant Simulation"),
    step_list([
        "ผังพื้นโรงงาน (เส้นสีเทาจางด้านหลัง) — แบบ Layout จริงที่ใช้เป็นพื้นหลังอ้างอิงตำแหน่งวาง Object",
        "กลุ่มเครื่องจักรสีเขียว-ฟ้า — แต่ละกลุ่มแทนสถานีเครื่องจักร/ประมวลผลในสายการผลิตจริง",
        "เส้นทางสีส้ม — เส้นทางลำเลียงชิ้นงานที่เชื่อมแต่ละสถานีเข้าด้วยกัน",
        "พาเลทสีเขียวด้านล่าง — จุดพักสินค้าสำเร็จรูปก่อนส่งออกจากไลน์",
    ])
)}

<h2>ใช้ทำอะไรได้บ้าง</h2>
<table>
<tr><th>โจทย์</th><th>Plant Simulation ช่วยอะไร</th></tr>
<tr><td>ออกแบบสายการผลิตใหม่</td><td>ทดสอบผัง Layout ก่อนลงทุนจริง ลดความเสี่ยงสร้างแล้วใช้ไม่ได้</td></tr>
<tr><td>หาคอขวด (Bottleneck)</td><td>ดูว่าเครื่องไหนเป็นตัวถ่วง Throughput ของทั้งสาย</td></tr>
<tr><td>วางแผนกำลังการผลิต</td><td>ทดลองเพิ่ม/ลดจำนวนเครื่องจักรหรือคนงานแบบ what-if</td></tr>
<tr><td>บริหารสินค้าคงคลัง/โลจิสติกส์</td><td>จำลองคลังสินค้า, AGV, ระบบขนส่งภายในโรงงาน</td></tr>
</table>

<div class="tip">
<strong>ทำไมไม่คำนวณมือ:</strong> เมื่อมีความสุ่ม (เช่น เครื่องเสียแบบสุ่ม, เวลาแปรรูปไม่คงที่) และ Object
หลายสิบ-หลายร้อยตัวโต้ตอบกัน การคำนวณมือแทบเป็นไปไม่ได้ — DES จำลองความซับซ้อนนี้ให้อัตโนมัติ
</div>

<h2>ภาพรวมคอร์สนี้</h2>
<p>คอร์สแบ่งเป็น 3 ระดับ: <strong>Basic</strong> รู้จักโปรแกรมและสร้างโมเดลแรก, <strong>Intermediate</strong>
ทำให้โมเดลสมจริงขึ้นด้วย Object เพิ่มเติมและค่าสุ่ม, <strong>Advanced</strong> เขียนสคริปต์ SimTalk
ควบคุมโมเดลและทำ Optimization อัตโนมัติ</p>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ถ้าคุณมีสายการผลิต 5 สถานี แต่ละสถานีมีเวลาทำงานสุ่มไม่เท่ากันทุกครั้ง
จะรู้ได้อย่างไรว่าสถานีไหนเป็นคอขวดโดยไม่ต้องรันสายการผลิตจริง?
</div>
<div class="tip"><strong>เฉลย:</strong> สร้างโมเดลจำลองทั้ง 5 สถานีด้วย Distribution ที่สะท้อนความสุ่มจริง (ดูบท Intermediate 3)
แล้วใช้ Bottleneck Analyzer (บท Intermediate 5) วิเคราะห์ผลจากการรันจำลอง — ไม่ต้องหยุดสายจริงเลย</div>
'''

BODY[("basic", 2)] = f'''
<h2>วิดีโอสาธิต: เปิดโปรแกรมและหน้า Start Page</h2>
<p>วิดีโอนี้สาธิตการเปิดโปรแกรม Plant Simulation ครั้งแรก ไปจนถึงหน้า <strong>Start Page</strong> ที่รวมทางลัดสำคัญ
(Load Last Model, Recent Models, Example Models) — ดูก่อนแล้วค่อยอ่านรายละเอียดแต่ละส่วนด้านล่าง</p>
{youtube_embed("l-p1UY2W5CY", "1. Getting Started - Plant Simulation")}

<h2>ส่วนประกอบหลักของโปรแกรม</h2>
<table>
<tr><th>ส่วนประกอบ</th><th>หน้าที่</th></tr>
<tr><td><strong>Class Library</strong></td><td>คลัง Object ทั้งหมดที่ใช้สร้างโมเดล แบ่งเป็นหมวด เช่น MaterialFlow, InformationFlow, Resources, MUs</td></tr>
<tr><td><strong>Frame</strong></td><td>พื้นที่วาดโมเดล (เหมือน Canvas) ลาก Object มาวางและเชื่อมต่อกันที่นี่ — โมเดลหนึ่งไฟล์มีได้หลาย Frame ซ้อนกัน</td></tr>
<tr><td><strong>Toolbar</strong></td><td>ปุ่มควบคุมการรันซิมูเลชัน (Start, Reset, Speed)</td></tr>
<tr><td><strong>Console</strong></td><td>แสดงข้อความ error/log ระหว่างรันหรือเขียนโค้ด SimTalk</td></tr>
<tr><td><strong>Navigator / Class Library Explorer</strong></td><td>แผงต้นไม้ทางซ้าย ไล่ดูโครงสร้างโมเดลทั้งหมดและ Class Library</td></tr>
<tr><td><strong>Attribute window</strong></td><td>เปิดจากดับเบิลคลิก Object — ตั้งค่าคุณสมบัติเฉพาะของ Object นั้น เช่น Interval, ProcTime</td></tr>
</table>

<h2>เปิดโปรแกรมครั้งแรก</h2>
<ol class="steps">
<li>เปิด Plant Simulation จะมีไฟล์โมเดลว่างเปล่าพร้อม Frame ชื่อ <code>Model</code> ให้อัตโนมัติ</li>
<li>ทางซ้ายจะเห็น Class Library — ลองเปิดหมวด <code>MaterialFlow</code> ดู Object ต่างๆ ที่มีให้ใช้</li>
<li>ลองลาก Object ใดก็ได้มาวางบน Frame เพื่อดูว่าการวางทำงานอย่างไร (ลบออกด้วยปุ่ม Delete ได้ ไม่มีผลเสีย)</li>
<li>บันทึกไฟล์ครั้งแรกด้วย <code>Ctrl+S</code> เพื่อฝึกความเคยชิน (ดูรายละเอียดเพิ่มในบทที่ 6)</li>
</ol>

<div class="tip">
<strong>Tip:</strong> ถ้าหน้าต่างเพี้ยนหรือ panel หายไป ไปที่เมนู <code>View → Reset Window Layout</code>
(หรือใกล้เคียง แล้วแต่เวอร์ชัน) เพื่อคืนค่าเลย์เอาต์เริ่มต้น
</div>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ถ้าอยากรู้ว่า Object ตัวหนึ่งมีคุณสมบัติ (Attribute) อะไรให้ตั้งค่าได้บ้าง ควรทำอย่างไร?
</div>
<div class="tip"><strong>เฉลย:</strong> ดับเบิลคลิกที่ Object นั้นเพื่อเปิด Attribute window — จะเห็นทุกแท็บการตั้งค่าของ Object นั้นโดยเฉพาะ</div>
'''

BODY[("basic", 3)] = '''
<h2>Object พื้นฐาน 6 ตัว</h2>
<p>Object เหล่านี้อยู่ใน Class Library หมวด <code>MaterialFlow</code> เป็นชุดที่ใช้บ่อยที่สุดในการสร้างสายการผลิตแบบง่าย</p>
<table>
<tr><th>Object</th><th>ใช้ทำอะไร</th><th>ค่าสำคัญที่ต้องตั้ง</th></tr>
<tr><td><strong>Source</strong></td><td>จุดกำเนิดชิ้นงาน (MU) เข้าสู่ระบบ</td><td><code>Interval</code> — ความถี่การผลิตชิ้นงานใหม่</td></tr>
<tr><td><strong>Line</strong></td><td>เส้นทางลำเลียงชิ้นงานระหว่างสถานีแบบมีความเร็ว/ความยาว</td><td><code>Length</code>, <code>Speed</code></td></tr>
<tr><td><strong>SingleProc</strong></td><td>สถานีประมวลผล/แปรรูปชิ้นงาน (จำลองเครื่องจักร 1 หัว)</td><td><code>ProcTime</code> — เวลาแปรรูปต่อชิ้น</td></tr>
<tr><td><strong>Buffer</strong></td><td>จุดพักชิ้นงานเมื่อสถานีถัดไปไม่ว่าง</td><td><code>Capacity</code> — ความจุสูงสุด</td></tr>
<tr><td><strong>Drain</strong></td><td>จุดสิ้นสุด ชิ้นงานออกจากระบบ (สินค้าสำเร็จรูป)</td><td>ไม่ต้องตั้งค่าอะไรพิเศษ</td></tr>
<tr><td><strong>EventController</strong></td><td>ตัวควบคุมเวลาจำลอง (นาฬิกาของโมเดล) ต้องมีเสมอในทุกโมเดล</td><td><code>SimTime</code> อ่านค่าเวลาจำลองปัจจุบัน</td></tr>
</table>

<div class="note">
<strong>ข้อควรรู้:</strong> ทุก Object มีแอตทริบิวต์ <code>Name</code> (ชื่อ) และ <code>InternalClassType</code>
(ชื่อประเภทจริงในภาษาอังกฤษ เช่น "Source", "Drain") ที่ใช้อ้างอิงได้ทั้งจาก GUI และจากสคริปต์ (ดูบท Advanced)
</div>

<h2>ลำดับการไหลของชิ้นงานทั่วไป</h2>
<p><code>Source → (Line) → SingleProc → (Buffer) → SingleProc → (Line) → Drain</code></p>
<p>ไม่จำเป็นต้องมี Line/Buffer ทุกจุด — เชื่อม Object ติดกันตรงๆ ก็ทำงานได้ แค่ไม่มีระยะทาง/เวลาขนส่งจำลองอยู่ในนั้น</p>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> ถ้าไม่ใส่ EventController ลงในโมเดลเลย จะเกิดอะไรขึ้นเมื่อกด Start?
</div>
<div class="tip"><strong>เฉลย:</strong> โมเดลจะรันไม่ได้เลย — EventController คือนาฬิกาของทั้งระบบ ไม่มี EventController = ไม่มีเวลาให้เดินหน้า</div>
'''

BODY[("basic", 4)] = '''
<h2>สร้างโมเดลแรก: สายการผลิตง่ายๆ</h2>
<p>ทำตามขั้นตอนนี้เพื่อสร้างโมเดล <code>Source → SingleProc → Drain</code></p>
<ol class="steps">
<li>เปิด Class Library → เลือกหมวด <code>MaterialFlow</code></li>
<li>ลาก <strong>Source</strong>, <strong>SingleProc</strong>, <strong>Drain</strong> มาวางเรียงกันบน Frame</li>
<li>ลาก <strong>EventController</strong> มาวางไว้มุมใดก็ได้ (จำเป็นต่อการรัน — ดูบทที่ 3)</li>
<li>เชื่อมต่อ Object โดยคลิกที่มุมขวาบนของแต่ละ Object แล้วลากไปยัง Object ถัดไป (จะเห็นลูกศรเชื่อม)</li>
<li>ดับเบิลคลิก <strong>Source</strong> เพื่อตั้งค่า <code>Interval</code> เช่น สร้างชิ้นงานทุก 5 วินาที</li>
<li>ดับเบิลคลิก <strong>SingleProc</strong> เพื่อตั้งค่า <code>ProcTime</code> เช่น 10 วินาทีต่อชิ้น</li>
<li>กดปุ่ม <strong>Start Simulation</strong> (▶) ที่ Toolbar ด้านบน</li>
</ol>

<div class="tip">
<strong>Tip:</strong> ถ้าเชื่อมต่อ Object ไม่ติด ให้เช็คว่าจุดเชื่อม (Connector) เป็นสีเขียวหรือไม่ — สีแดงหมายถึงยังเชื่อมไม่สำเร็จ
</div>

<h2>ตัวอย่าง: ทำนายผลก่อนรันจริง</h2>
<p>โมเดล <code>Source(Interval=5s) → SingleProc(ProcTime=10s) → Drain</code></p>
<div class="note">
<strong>คำถามฝึกคิด:</strong> Source ผลิตชิ้นงานเร็วกว่า SingleProc แปรรูปเสร็จ (5s &lt; 10s) จะเกิดอะไรขึ้นเมื่อรันไปนานๆ?
</div>
<div class="tip"><strong>เฉลย:</strong> SingleProc รับชิ้นงานไม่ทัน Source เลยจะถูก <strong>Blocked</strong>
(สถานะรอส่งต่อ เพราะปลายทางไม่ว่าง) — นี่คือคอขวดแบบง่ายที่สุด แก้ได้ด้วยการเพิ่ม Buffer คั่นกลาง
หรือเพิ่มสถานีขนาน (ดูบท Intermediate)
</div>
'''

BODY[("basic", 5)] = '''
<h2>รัน / หยุด / รีเซ็ต</h2>
<table>
<tr><th>ปุ่ม</th><th>ทำอะไร</th></tr>
<tr><td><strong>Start</strong> (▶)</td><td>เริ่มเดินเวลาจำลอง ตาม EventController</td></tr>
<tr><td><strong>Stop/Pause</strong> (⏸)</td><td>หยุดชั่วคราว กด Start ต่อได้จากจุดเดิม</td></tr>
<tr><td><strong>Reset</strong> (⟲)</td><td>ล้างค่าสถิติและตำแหน่งชิ้นงานทั้งหมด กลับสู่เวลา 0</td></tr>
</table>

<div class="note">
<strong>ข้อควรระวัง:</strong> อย่าลืมกด <strong>Reset</strong> ก่อนรันใหม่ทุกครั้งที่เปลี่ยนค่าพารามิเตอร์ ไม่งั้นค่าสถิติจะสะสมปนกับรอบก่อนหน้า
ทำให้ผลวิเคราะห์ผิดพลาด
</div>

<h2>อ่านผลลัพธ์เบื้องต้น</h2>
<p>คลิกขวาที่ Object ประเภทประมวลผล (เช่น <strong>SingleProc</strong>) แล้วเลือก <code>Statistics</code> เพื่อดู:</p>
<table>
<tr><th>สถานะ</th><th>ความหมาย</th></tr>
<tr><td><strong>Working</strong></td><td>เวลาที่เครื่องกำลังแปรรูปชิ้นงานจริง — ยิ่งสูงยิ่งใช้งานคุ้ม</td></tr>
<tr><td><strong>Waiting</strong></td><td>เวลาที่รอชิ้นงานเข้ามา (ว่างงาน) — สูงแปลว่าต้นทางป้อนช้าเกินไป</td></tr>
<tr><td><strong>Blocked</strong></td><td>เวลาที่ทำงานเสร็จแล้วแต่ส่งต่อไม่ได้ (สถานีถัดไปไม่ว่าง) — สูงแปลว่าปลายทางเป็นคอขวด</td></tr>
</table>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> ถ้า SingleProc มีค่า Blocked สูงมาก ควรแก้ปัญหาที่ตัว SingleProc นี้เอง หรือที่อื่น?
</div>
<div class="tip"><strong>เฉลย:</strong> ควรแก้ที่ <em>สถานีถัดไป</em> (ปลายทางที่รับต่อ) ไม่ใช่ตัว SingleProc เอง — เพราะ Blocked สูง
แปลว่าสถานีนี้ทำงานเสร็จเร็วกว่าที่ปลายทางจะรับได้ ปลายทางต่างหากที่เป็นคอขวดจริง
</div>
'''

BODY[("basic", 6)] = '''
<h2>บันทึกไฟล์โมเดล</h2>
<p>Plant Simulation บันทึกไฟล์เป็นนามสกุล <code>.spp</code> — ไฟล์เดียวเก็บทั้งโมเดล, Frame ย่อยทั้งหมด, และ Class Library ที่ปรับแต่งเอง</p>
<ol class="steps">
<li><code>Ctrl+S</code> หรือเมนู <code>File → Save</code> — บันทึกทับไฟล์เดิม</li>
<li><code>File → Save As</code> — บันทึกเป็นไฟล์ใหม่ (แนะนำเมื่อจะทดลองอะไรเสี่ยงๆ กับโมเดล)</li>
<li><code>File → Open</code> — เปิดไฟล์ <code>.spp</code> ที่มีอยู่กลับมาทำต่อ</li>
</ol>

<div class="note">
<strong>ข้อควรระวังเรื่องเวอร์ชัน:</strong> ไฟล์ที่บันทึกจากโปรแกรมเวอร์ชันใหม่กว่า จะ<strong>เปิดไม่ได้</strong>ในโปรแกรมเวอร์ชันเก่ากว่า
(ขึ้น error ประมาณ "model version is higher than the program version") — ถ้าทำงานร่วมกับคนอื่น ควรตกลงกันว่าใช้โปรแกรมเวอร์ชันเดียวกัน
หรือรู้ว่าไฟล์ต้นทางเซฟจากเวอร์ชันไหน
</div>

<h2>นิสัยสำรองไฟล์ที่ควรมี</h2>
<ul>
<li>ก่อนทดลองเปลี่ยนโครงสร้างใหญ่ (เช่น ลบ Frame, แก้สคริปต์เยอะ) ให้ <code>Save As</code> เป็นไฟล์สำรองก่อน เช่น <code>PLT_backup_2026-08-29.spp</code></li>
<li>ตั้งชื่อไฟล์ให้สื่อเวอร์ชัน/วันที่ แทนการเขียนทับไฟล์เดิมตลอด — ย้อนกลับได้เมื่อทำพลาด</li>
<li>ถ้าทำงานเป็นทีม เก็บไฟล์ไว้ในระบบที่มีประวัติการแก้ไข (เช่น โฟลเดอร์ที่ sync กับ cloud หรือ version control) ไม่ใช่แค่ในเครื่องเดียว</li>
</ul>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> เพื่อนร่วมทีมส่งไฟล์ <code>.spp</code> มาให้ แต่เปิดไม่ได้ ขึ้น error เรื่องเวอร์ชัน ควรทำอย่างไรก่อน?
</div>
<div class="tip"><strong>เฉลย:</strong> เช็คว่าเครื่องคุณติดตั้ง Plant Simulation เวอร์ชันเดียวกันหรือใหม่กว่าที่เพื่อนใช้เซฟหรือไม่ —
ถ้าเครื่องมีหลายเวอร์ชันติดตั้งอยู่ ให้เปิดไฟล์ด้วยเวอร์ชันที่เท่ากับหรือใหม่กว่าเวอร์ชันที่บันทึกไฟล์นั้นไว้
</div>
'''

BODY[("intermediate", 1)] = '''
<h2>Object ขั้นกลางที่ใช้บ่อย</h2>
<table>
<tr><th>Object</th><th>ใช้ทำอะไร</th><th>ต่างจากตัวพื้นฐานอย่างไร</th></tr>
<tr><td><strong>Buffer</strong></td><td>พักชิ้นงานแบบ FIFO เรียบง่าย</td><td>เทียบกับ Store: Buffer ไม่มีตำแหน่งจัดเก็บย่อย เข้าก่อนออกก่อนเสมอ</td></tr>
<tr><td><strong>Store</strong></td><td>พักชิ้นงานแบบมีตำแหน่ง/ชั้นวางย่อย ดึงออกไม่ต้องเรียงลำดับ</td><td>เหมาะจำลองคลังสินค้า/ชั้นวางจริงที่หยิบสินค้าจากตำแหน่งใดก็ได้</td></tr>
<tr><td><strong>AssemblyStation</strong></td><td>รวมชิ้นงานจากหลายทางเข้าเป็นชิ้นเดียว (เช่น ประกอบชิ้นส่วน A+B)</td><td>SingleProc รับ-ส่งทางเดียว แต่ AssemblyStation รอครบทุกอินพุตก่อนประมวลผล</td></tr>
<tr><td><strong>Track</strong></td><td>เส้นทางที่ให้ Transporter วิ่งบนนั้น (ต่างจาก Line ที่ขนส่งอัตโนมัติ)</td><td>ใช้คู่กับ Transporter เพื่อจำลองรถขนส่ง/AGV ที่ขับเคลื่อนเอง</td></tr>
<tr><td><strong>Transporter</strong></td><td>พาหนะขนส่งชิ้นงานที่ขับเคลื่อนไปมาเองบน Track</td><td>ต่างจาก Line ตรงที่ Transporter เป็นวัตถุเดี่ยวที่ต้องวิ่งไปรับ-ส่งเอง ไม่ใช่สายพานตายตัว</td></tr>
</table>

<div class="tip">
<strong>เลือกใช้อย่างไร:</strong> ถ้าของแค่ "พักคอย" ธรรมดา ใช้ Buffer พอ — ถ้าต้องจำลองคลังที่หยิบแบบสุ่มตำแหน่งได้ ใช้ Store —
ถ้าต้องรวมชิ้นส่วนหลายทางเป็นหนึ่งเดียว (ประกอบสินค้า) ใช้ AssemblyStation — ถ้ามีรถ/พาหนะขนส่งเอง ใช้ Track + Transporter
</div>

<h2>ตัวอย่าง: จำลองสถานีประกอบ</h2>
<p>โครงสร้าง: <code>Source1(ชิ้นส่วน A) → AssemblyStation ← Source2(ชิ้นส่วน B)</code> จากนั้น <code>AssemblyStation → Drain</code></p>
<div class="note">
<strong>คำถามฝึกคิด:</strong> ถ้า Source1 ผลิตเร็วกว่า Source2 มาก จะเกิดอะไรขึ้นที่ AssemblyStation?
</div>
<div class="tip"><strong>เฉลย:</strong> ชิ้นส่วนจาก Source1 จะสะสมรอที่ทางเข้า AssemblyStation เพราะสถานีต้องรอให้ชิ้นส่วนจาก Source2 มาครบคู่ก่อนจึงประมวลผลได้ —
ควรใส่ Buffer ก่อน AssemblyStation ด้านที่เร็วกว่า เพื่อไม่ให้ Source1 ถูก Block</div>
'''

BODY[("intermediate", 2)] = '''
<h2>MU (Movable Unit) คืออะไร</h2>
<p>MU คือ "ชิ้นงาน" ที่เคลื่อนที่ผ่านระบบ — เก็บอยู่ในหมวด Class Library <code>MUs</code> แบ่งเป็นประเภทหลักคือ
<strong>Part</strong> (ชิ้นงานทั่วไป), <strong>Container</strong> (ภาชนะบรรจุหลายชิ้น), <strong>Transporter</strong> (พาหนะที่ขับเคลื่อนเอง)</p>

<div class="note">
<strong>ข้อควรรู้:</strong> Object ใต้ <code>.MUs</code> เป็น "แม่แบบ" ที่ Source จะ<em>ผลิตสำเนาออกมา</em>ตอนรัน ไม่ใช่ Object
ที่ลากไปวางบน Frame ได้โดยตรงแบบ Source/SingleProc — ถ้าอยากปรับแต่งคุณสมบัติของ MU (เช่น ตั้งชื่อ, สี, น้ำหนักเริ่มต้น)
ต้อง <strong>Duplicate/Derive</strong> ก๊อปปี้ MU ไปไว้ในหมวด <code>UserObjects</code> ของตัวเองก่อน
</div>

<h2>สร้าง MU class ของตัวเอง</h2>
<ol class="steps">
<li>ไปที่ Class Library → <code>MUs → Part</code> (หรือ Container/Transporter ตามต้องการ)</li>
<li>คลิกขวา → <code>Duplicate</code> หรือ <code>Derive</code> แล้วลากไปวางใน <code>UserObjects</code></li>
<li>ตั้งชื่อให้สื่อความหมาย เช่น <code>PartA</code></li>
<li>เปิด Attribute ของ MU ที่สร้างใหม่ ปรับค่าเริ่มต้น (ไอคอน, สี, น้ำหนัก ฯลฯ) ตามต้องการ</li>
<li>ไปที่ <strong>Source</strong> ที่จะผลิต MU นี้ → ตั้งค่าช่อง <code>MU</code> (แอตทริบิวต์ที่กำหนดคลาส MU ที่จะผลิต) ให้ชี้ไปที่ MU ที่สร้างไว้</li>
</ol>

<div class="tip">
<strong>Tip:</strong> ถ้ามี MU หลายแบบให้ Source ผลิตแบบสุ่มหรือเรียงลำดับ ให้ดูช่อง <code>MUSelection</code>
ของ Source — เลือกโหมด Constant (คลาสเดียวคงที่), Sequence (เรียงลำดับ), หรือ Random (สุ่มตามสัดส่วน)
</div>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ทำไมลาก <code>.MUs.Part</code> ไปวางบน Frame ตรงๆ ไม่ได้เหมือน Source/SingleProc?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะ Object ใต้ <code>.MUs</code> เป็นแม่แบบสำหรับให้ Source สร้างสำเนาขึ้นมาตอนรันจำลอง ไม่ใช่ Object
ที่มีตำแหน่งตายตัวในผังโรงงาน — ต้อง Duplicate/Derive ไปเป็นของตัวเองก่อนถึงจะปรับแต่งและใช้อ้างอิงได้</div>
'''

BODY[("intermediate", 3)] = '''
<h2>ทำไมค่าคงที่ไม่สะท้อนความจริง</h2>
<p>ในโรงงานจริง เวลาแปรรูปแต่ละชิ้นไม่เท่ากันเป๊ะทุกครั้ง (คนงานเร็วช้าไม่เท่ากัน, วัตถุดิบไม่สม่ำเสมอ) การใส่ค่าคงที่
(เช่น ProcTime = 10 วินาทีเป๊ะ) ทำให้ผลจำลองดูสวยเกินจริง — <strong>Distribution</strong> คือการบอกโปรแกรมว่า
"ค่านี้ควรสุ่มตามรูปแบบทางสถิติแบบไหน" แทนค่าคงที่</p>

<h2>Distribution ที่ใช้บ่อย</h2>
<table>
<tr><th>ประเภท</th><th>ลักษณะ</th><th>ใช้เมื่อไหร่</th></tr>
<tr><td><strong>Constant</strong></td><td>ค่าคงที่ ไม่สุ่ม</td><td>ค่าเริ่มต้น หรือตอนทำโมเดล smoke test อย่างเร็ว</td></tr>
<tr><td><strong>Uniform</strong></td><td>สุ่มเท่าๆ กันในช่วง [min, max]</td><td>ไม่รู้รูปแบบจริง แต่รู้ช่วงค่าต่ำสุด-สูงสุด</td></tr>
<tr><td><strong>Exponential (negexp)</strong></td><td>ค่าส่วนใหญ่น้อย นานๆ ทีมีค่าสูง (หางยาว)</td><td>เวลาระหว่างการมาถึงแบบสุ่มอิสระ (Poisson process) — พบบ่อยกับ Source.Interval</td></tr>
<tr><td><strong>Normal</strong></td><td>โค้งระฆังคว่ำ ค่าส่วนใหญ่กระจุกรอบค่าเฉลี่ย</td><td>เวลาแปรรูปที่มีความแปรปรวนแบบสมมาตรรอบค่าเฉลี่ย</td></tr>
<tr><td><strong>Table/Empirical</strong></td><td>สุ่มตามข้อมูลจริงที่ป้อนเข้าไปเป็นตาราง</td><td>มีข้อมูลจริงจากโรงงานอยู่แล้ว อยากให้โมเดลสุ่มตามการกระจายจริง ไม่ใช่สูตรสำเร็จรูป</td></tr>
</table>

<h2>วิธีตั้งค่า</h2>
<ol class="steps">
<li>ดับเบิลคลิก Object (เช่น Source หรือ SingleProc) เพื่อเปิด Attribute window</li>
<li>ที่ช่อง Interval หรือ ProcTime แทนที่จะพิมพ์ตัวเลขตรงๆ ให้เลือกรูปแบบ Distribution จาก dropdown</li>
<li>กรอกพารามิเตอร์ของ Distribution นั้น (เช่น Exponential ต้องการค่าเฉลี่ย, Normal ต้องการค่าเฉลี่ยและส่วนเบี่ยงเบนมาตรฐาน)</li>
<li>รันซิมูเลชันหลายรอบ (Reset แล้วรันใหม่) เพื่อดูว่าผลลัพธ์แต่ละรอบต่างกันแค่ไหน — นี่คือธรรมชาติของความสุ่ม</li>
</ol>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> ถ้าตั้ง ProcTime เป็น Exponential ค่าเฉลี่ย 10 วินาที แล้วรัน Reset ซ้ำ 3 รอบ ค่า Statistics
ของแต่ละรอบจะเหมือนกันเป๊ะหรือไม่?
</div>
<div class="tip"><strong>เฉลย:</strong> ไม่เหมือนกันเป๊ะ — เพราะแต่ละรอบสุ่มค่าใหม่ตาม Distribution (เว้นแต่ล็อค Random Seed ไว้ค่าเดิม)
นี่คือเหตุผลที่การวิเคราะห์โมเดลแบบสุ่มมักต้องรันหลายรอบแล้วดูค่าเฉลี่ย/ช่วงความเชื่อมั่น ไม่ใช่ดูแค่รอบเดียว</div>
'''

BODY[("intermediate", 4)] = '''
<h2>MTTR / MTBF คืออะไร</h2>
<table>
<tr><th>คำย่อ</th><th>ความหมาย</th></tr>
<tr><td><strong>MTBF</strong> (Mean Time Between Failures)</td><td>เวลาเฉลี่ยระหว่างที่เครื่องจักรเสียแต่ละครั้ง — ยิ่งมากยิ่งเสียบ่อยน้อย</td></tr>
<tr><td><strong>MTTR</strong> (Mean Time To Repair)</td><td>เวลาเฉลี่ยที่ใช้ซ่อมแต่ละครั้ง — ยิ่งมากยิ่งซ่อมนาน</td></tr>
</table>
<p>โมเดลที่ไม่มี Failure เลยจะให้ผล Throughput สูงเกินจริงเสมอ เพราะโรงงานจริงไม่มีเครื่องจักรที่ทำงานได้ 100% ตลอดเวลา</p>

<h2>ตั้งค่า Failure บน Object</h2>
<ol class="steps">
<li>ดับเบิลคลิกที่ Object ประเภทประมวลผล (เช่น SingleProc) → ไปแท็บ <strong>Failures</strong></li>
<li>เลือกโหมด Failure — ที่พบบ่อยคือ <strong>Availability-based</strong> (กำหนดเปอร์เซ็นต์เวลาที่พร้อมใช้งาน) หรือ
<strong>MTBF/MTTR</strong> (กำหนดตัวเลขทั้งสองค่าตรงๆ)</li>
<li>กรอก MTBF และ MTTR (แต่ละค่าตั้งเป็น Distribution ได้เหมือนบทที่แล้ว เช่น เวลาซ่อมสุ่มตาม Exponential)</li>
<li>รันซิมูเลชัน แล้วเปิด Statistics — จะเห็นสถานะใหม่ <strong>Failed/Down</strong> เพิ่มเข้ามานอกจาก Working/Waiting/Blocked</li>
</ol>

<div class="note">
<strong>ข้อควรรู้:</strong> Failure มักตั้งแบบ "สุ่มตามเวลาทำงานสะสม" ไม่ใช่ "สุ่มตามเวลาปฏิทิน" — เครื่องที่ไม่มีงานทำ (Waiting)
โดยทั่วไปจะไม่นับเป็นช่วงเวลาที่เดินไปสู่การเสีย เพราะยังไม่ได้ทำงานจริง
</div>

<h2>ตัวอย่างการวิเคราะห์</h2>
<p>สถานี A: MTBF = 8 ชั่วโมง, MTTR = 30 นาที → คิดคร่าวๆ ว่าเครื่องพร้อมใช้งานประมาณ 8/(8+0.5) ≈ 94%</p>
<div class="tip">
<strong>คำถามฝึกคิด:</strong> ถ้าวิเคราะห์แล้วพบว่าสถานีคอขวดมี Availability ต่ำมาก (เสียบ่อย) ทางเลือกในการแก้ปัญหามีอะไรบ้าง
นอกจากซื้อเครื่องใหม่?
</div>
<div class="tip"><strong>เฉลย:</strong> เพิ่ม Buffer ก่อน/หลังสถานีนั้นเพื่อดูดซับช่วงเวลาที่เสีย, ลด MTTR ด้วยการเตรียมอะไหล่/ทีมซ่อมให้เร็วขึ้น,
หรือเพิ่มสถานีสำรองขนานเพื่อสลับใช้งานเวลาสถานีหลักเสีย — ลองปรับตัวแปรพวกนี้ในโมเดลเปรียบเทียบกันได้ก่อนตัดสินใจลงทุนจริง</div>
'''

BODY[("intermediate", 5)] = '''
<h2>อ่านผัง Sankey</h2>
<p>Plant Simulation แสดงเส้นทางการไหลของชิ้นงานเป็นผัง <strong>Sankey</strong> ได้ — เส้นยิ่งหนายิ่งมีปริมาณชิ้นงานไหลผ่านมาก
ช่วยเห็นภาพรวมเส้นทางที่มีปริมาณงานสูงได้เร็วกว่าดูตัวเลขในตาราง</p>

<h2>สีของ Statistics</h2>
<table>
<tr><th>สี (ทั่วไป)</th><th>สถานะ</th></tr>
<tr><td>🟢 เขียว</td><td>Working — กำลังทำงาน</td></tr>
<tr><td>🟡 เหลือง</td><td>Waiting — ว่างงาน รอชิ้นงาน</td></tr>
<tr><td>🔴 แดง</td><td>Blocked — ทำเสร็จแล้วแต่ส่งต่อไม่ได้</td></tr>
<tr><td>⚫ ดำ/เทาเข้ม</td><td>Failed/Down — เครื่องเสีย (ถ้าตั้ง Failure ไว้ตามบทที่ 4)</td></tr>
</table>
<p>สีที่แน่นอนปรับได้จากการตั้งค่าโปรแกรม แต่แนวคิด "ยิ่งแดง/ดำเยอะยิ่งมีปัญหา" ใช้ได้เสมอ</p>

<h2>ใช้ Bottleneck Analyzer</h2>
<ol class="steps">
<li>เปิดจาก Class Library หมวด <code>Tools → BottleneckAnalyzer</code> ลากมาวางในโมเดล</li>
<li>เชื่อมโยง/เลือก Object ที่ต้องการวิเคราะห์ (มักเลือกทั้งสายการผลิต)</li>
<li>รันซิมูเลชันตามปกติ จากนั้นเปิดรายงานของ BottleneckAnalyzer</li>
<li>อ่านผล — เครื่องมือจะจัดอันดับสถานีที่เป็นคอขวด (มักดูจากสัดส่วนเวลา Blocked/Waiting สูงสุด) ให้อัตโนมัติ แทนที่จะไล่ดูทีละสถานีเอง</li>
</ol>

<div class="tip">
<strong>Tip:</strong> Bottleneck ที่แท้จริงอาจไม่ใช่สถานีที่ดูยุ่งที่สุด — สถานีที่ค่า Working สูงสุดอาจแค่ "ทำงานหนัก" ในขณะที่ตัวจริง
คือสถานีที่ทำให้สถานีอื่น Blocked บ่อยที่สุดต่างหาก ใช้ Bottleneck Analyzer แทนการเดาเอง
</div>

<div class="note">
<strong>คำถามฝึกคิด:</strong> Export ผลจาก Bottleneck Analyzer หรือ Chart ไปใช้ต่อ (เช่น ทำรายงานให้หัวหน้า) ทำได้ไหม?
</div>
<div class="tip"><strong>เฉลย:</strong> ได้ — Chart ส่วนใหญ่ใน Plant Simulation คลิกขวาแล้วมีตัวเลือก Export เป็นรูปภาพหรือคัดลอกข้อมูลตารางออกไปวางในโปรแกรมอื่นได้</div>
'''

BODY[("intermediate", 6)] = '''
<h2>แนวคิด Sub-frame</h2>
<p>เมื่อโมเดลใหญ่ขึ้น การมี Object เดี่ยวๆ กระจัดกระจายเต็ม Frame เดียวจะดูแลยาก — Plant Simulation ให้ "ห่อ"
กลุ่ม Object ที่ทำงานร่วมกันไว้ใน <strong>Frame ย่อย (Sub-frame)</strong> เดียว แล้วมองจากภายนอกเหมือนเป็น Object ก้อนเดียว</p>

<h2>สร้าง Sub-frame</h2>
<ol class="steps">
<li>เลือก Object หลายตัวที่ต้องการห่อรวมกัน (เช่น Buffer + SingleProc + สถิติที่เกี่ยวข้อง)</li>
<li>คลิกขวา → มองหาตัวเลือกลักษณะ "Group" หรือ "Move to new Frame" (ชื่อเมนูอาจต่างกันเล็กน้อยตามเวอร์ชัน)</li>
<li>Object ที่เลือกจะถูกย้ายเข้าไปอยู่ใน Frame ใหม่ และ Frame นั้นแสดงเป็น Object ก้อนเดียวใน Frame แม่</li>
<li>เพิ่ม <strong>Interface object</strong> (จุดเชื่อมต่อเข้า-ออก) ที่ขอบของ Sub-frame เพื่อให้ภายนอกเชื่อมต่อกับ Sub-frame นี้ได้เหมือน Object ปกติ</li>
</ol>

<h2>ทำให้นำกลับมาใช้ซ้ำได้</h2>
<p>เมื่อ Sub-frame ทำงานตามต้องการแล้ว ลากมันเข้าไปเก็บไว้ใน Class Library หมวด <code>UserObjects</code> ของตัวเอง —
จากนั้นจะสามารถลากมาวางซ้ำได้หลายจุดในโมเดลเดียวกัน หรือคัดลอกไปใช้ในโมเดลอื่น เหมือน "สถานีมาตรฐาน" สำเร็จรูป</p>

<div class="tip">
<strong>Tip:</strong> ตั้งชื่อ Sub-frame และ Interface object ให้สื่อความหมายชัดเจน (เช่น <code>In</code>/<code>Out</code>
สำหรับจุดเชื่อมต่อ) เพราะเมื่อนำไปใช้ซ้ำในโมเดลอื่น คนอื่นจะไม่เห็นรายละเอียดภายในทันที ต้องเข้าใจจากชื่อและพอร์ตที่เห็นจากภายนอก
</div>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ทำไมการห่อเป็น Sub-frame ถึงช่วยเรื่อง "reusable module" มากกว่าการ copy-paste Object กลุ่มเดิมซ้ำๆ?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะ Sub-frame ที่เก็บใน UserObjects เป็นแม่แบบเดียวที่อ้างอิงร่วมกัน — ถ้าต้องแก้ไขพฤติกรรมภายใน (เช่น
เพิ่มสถิติใหม่) แก้ที่แม่แบบเดียวจบ ขณะที่ copy-paste ต้องไล่แก้ทุกจุดที่เคยคัดลอกไว้แยกกัน</div>
'''

BODY[("advanced", 1)] = '''
<h2>SimTalk 2.0 คืออะไร</h2>
<p>SimTalk คือภาษาสคริปต์ของ Plant Simulation เขียนใน Object ประเภท <strong>Method</strong> เพื่อสั่งงาน กำหนดเงื่อนไข
หรือดึง/เปลี่ยนค่าตัวแปรของ Object อื่นในโมเดล เนื้อหาบทนี้อ้างอิง <strong>syntax ที่ทดสอบรันได้จริง</strong> (SimTalk 2.0)
ไม่ใช่ syntax แบบเก่า (<code>is...do...end</code>) ที่อาจเจอในเอกสารเก่าหรือโมเดลรุ่นก่อน</p>

<div class="note">
<strong>หมายเหตุ:</strong> ถ้าเจอโมเดลเก่าที่เขียนด้วย syntax <code>is / do / end</code> คั่นด้วย <code>--</code> comment
นั่นคือ SimTalk รุ่นก่อนหน้า ยังใช้งานได้ในโมเดลเดิม แต่โค้ดใหม่ที่เขียนควรใช้ syntax ของ SimTalk 2.0 ตามบทนี้แทน
</div>

<h2>โครงสร้าง Method</h2>
<p>Method ทุกตัวต้องมีบรรทัด header ก่อนตัวเนื้อโค้ด บอกชนิดค่าที่ return (หรือไม่ return ก็ได้):</p>
<pre><code>->string;              // ไม่มีพารามิเตอร์ คืนค่าเป็น string
var buf := "hello"
return buf</code></pre>
<p>หรือมีพารามิเตอร์:</p>
<pre><code>param x: integer := 0 -> integer;
return x + 1</code></pre>

<h2>Syntax พื้นฐานที่ยืนยันแล้ว</h2>
<table>
<tr><th>Construct</th><th>Syntax</th><th>หมายเหตุ</th></tr>
<tr><td>ประกาศตัวแปร</td><td><code>var x := &lt;expr&gt;</code></td><td>ไม่ต้องระบุชนิดตัวแปร (อนุมานอัตโนมัติ) ไม่มี <code>;</code> ปิดท้าย</td></tr>
<tr><td>for-loop</td><td><code>for var i := 1 to N</code> ... <code>next</code></td><td>ไม่มีคำว่า <code>loop</code>/<code>do</code> ปิดด้วย <code>next</code> ไม่ใช่ <code>end</code></td></tr>
<tr><td>if</td><td><code>if &lt;cond&gt;</code> ... <code>end</code></td><td>ไม่มีคำว่า <code>then</code></td></tr>
<tr><td>ต่อ string</td><td><code>"a" + "b"</code></td><td>ใช้ <code>+</code> ธรรมดา</td></tr>
<tr><td>ตัวอักษรจาก code point</td><td><code>strChr(31)</code></td><td>สร้างตัวคั่นพิเศษที่ไม่ชนกับชื่อ Object</td></tr>
<tr><td>คำสงวน</td><td><code>result</code></td><td>ห้ามใช้เป็นชื่อตัวแปร (<code>var result := ...</code> error) ใช้ชื่ออื่นแทน เช่น <code>buf</code>, <code>acc</code></td></tr>
</table>

<h2>ตัวอย่างจริง: วนลูปอ่านชื่อ Object ทุกตัวใน Frame</h2>
<pre><code>->string;
var buf := ""
for var i := 1 to .Models.Model.NumNodes
    buf := buf + .Models.Model.Node(i).Name + strChr(31) + .Models.Model.Node(i).InternalClassType + strChr(30)
next
return buf</code></pre>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> ทำไมโค้ดตัวอย่างข้างบนใช้ <code>strChr(31)</code>/<code>strChr(30)</code> คั่นข้อมูล แทนที่จะใช้ comma หรือ space ธรรมดา?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะชื่อ Object จริงอาจมี comma หรือ space ปนอยู่ในชื่อได้ ถ้าใช้ตัวคั่นทั่วไปอาจแยกข้อมูลผิดพลาด
<code>strChr(31)</code>/<code>strChr(30)</code> คือ Unit/Record Separator ซึ่งแทบไม่มีทางปรากฏในชื่อ Object จริง จึงปลอดภัยกว่า</div>
'''

BODY[("advanced", 2)] = '''
<h2>ผูก Method เข้ากับเหตุการณ์ Entrance/Exit</h2>
<p>Object ประเภทประมวลผล (เช่น SingleProc) มีช่อง <code>ExecuteAt.Entrance</code> และ <code>ExecuteAt.Exit</code>
ให้กำหนด Method ที่จะทำงานอัตโนมัติทุกครั้งที่มีชิ้นงานเข้า/ออกจากสถานีนั้น</p>
<ol class="steps">
<li>สร้าง Method object ในหมวด <code>InformationFlow</code> ตั้งชื่อ เช่น <code>OnEntry</code></li>
<li>เขียนโค้ดใน Method นั้น</li>
<li>ที่ Object เป้าหมาย (เช่น SingleProc) เปิด Attribute → ช่อง <code>ExecuteAt.Entrance</code> → กำหนดให้ชี้ไปที่ Method <code>OnEntry</code></li>
<li>รันซิมูเลชัน — Method จะถูกเรียกอัตโนมัติทุกครั้งที่มีชิ้นงานเข้าสถานี ไม่ต้องเรียกเองด้วยมือ</li>
</ol>

<h2>เข้าถึงชิ้นงาน (MU) ปัจจุบัน</h2>
<p>ภายใน Method ที่ผูกกับเหตุการณ์แบบนี้ ตัวแปรพิเศษ <code>@</code> อ้างอิงถึง MU (ชิ้นงาน) ที่กำลังผ่านสถานีอยู่ขณะนั้น</p>
<pre><code>->void;
var mu := @
print "MU " + mu.Name + " entered station"</code></pre>

<h2>Trigger: ทำงานเป็นระยะเวลาซ้ำๆ</h2>
<p>ถ้าต้องการให้ Method ทำงานตามเวลา (ไม่ผูกกับเหตุการณ์ของ Object อื่น) ใช้ Object <strong>Trigger</strong>
(อยู่ในหมวด <code>InformationFlow</code>) ตั้งค่าคาบเวลาที่ต้องการ แล้วกำหนดให้เรียก Method ที่ต้องการทุกครั้งที่ครบคาบ</p>

<h2>รูปแบบทั่วไป: Attribute เก็บ reference ไปยัง Method</h2>
<p>สอดคล้องกับรูปแบบที่ใช้ซ้ำทั่วทั้งโปรแกรม — แอตทริบิวต์ที่ควบคุมพฤติกรรม (เช่น <code>Ctrl</code> ของเซนเซอร์บางประเภท)
เก็บ <em>object reference</em> ไปยัง Method โดยตรง กำหนดค่าได้จากโค้ดเช่นกัน:</p>
<pre><code>someSensor.Ctrl := .Models.MyFrame.Node("MyControlMethod")</code></pre>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ถ้าอยากนับจำนวนชิ้นงานที่ผ่านสถานีสะสมตลอดการรัน ควรผูก Method กับ Entrance หรือ Exit?
</div>
<div class="tip"><strong>เฉลย:</strong> ทั้งสองจุดนับได้ในทางทฤษฎี แต่ <strong>Exit</strong> แม่นยำกว่าสำหรับนับ "งานที่เสร็จสมบูรณ์" เพราะ Entrance
นับตอนเข้า ซึ่งชิ้นงานอาจยังไม่ผ่านกระบวนการจริง (เช่น ถ้าสถานีเสียระหว่างประมวลผล) — เลือกจุดผูกให้ตรงกับความหมายของสิ่งที่ต้องการวัด</div>
'''

BODY[("advanced", 3)] = '''
<h2>DataTable และ Variable อยู่ใต้ .InformationFlow</h2>
<p>ต่างจาก Object การไหลของวัสดุ (<code>.MaterialFlow</code>) — DataTable และ Variable อยู่ในหมวด <code>.InformationFlow</code>
สร้างด้วย <code>createObject</code> แบบเดียวกับ Object ทั่วไป:</p>
<pre><code>var t := .InformationFlow.DataTable.createObject(f, 0, 0)
t.Name := "Items"</code></pre>

<div class="note">
<strong>กับดัก auto-deref:</strong> การอ้าง <code>.InformationFlow.Variable</code> เฉยๆ (ไม่ผ่าน <code>.Node()</code>) จะได้
<em>ค่าที่ตัวแปรถืออยู่</em> (ค่าเริ่มต้นเป็น <code>0</code>) ไม่ใช่ตัว Object เอง ทำให้ <code>createObject</code> พัง —
ต้องใช้ <code>.Node("ClassName")</code> เพื่อขอ object reference ตรงๆ แทน:
</div>
<pre><code>var v := .InformationFlow.Node("Variable").createObject(f, 0, 50)
v.Name := "Constraint"</code></pre>
<p>กติกาเดียวกันนี้ใช้กับ <code>Method</code> ด้วย (บทที่ 2) — เป็นกฎทั่วไปของ Object ในหมวด <code>.InformationFlow</code>
ที่ "มีค่า" หรือ "เรียกใช้ได้" ไม่ใช่เฉพาะ Variable</p>

<h2>อ่าน/เขียนค่าใน DataTable</h2>
<p>ใช้ bracket indexing <code>[column, row]</code> โดยทั้งคู่เริ่มนับที่ 1:</p>
<pre><code>return to_str(.Models.Model.DataTable[1, 1])   // อ่านค่า
.Models.Model.DataTable[1, 1] := "hello"       // เขียนค่า</code></pre>
<table>
<tr><th>กติกา</th><th>รายละเอียด</th></tr>
<tr><td>ไม่มี getValue/setValue</td><td>เข้าถึงด้วย bracket indexing เท่านั้น</td></tr>
<tr><td>แถว/คอลัมน์ 0 = หัวตาราง</td><td><code>table[c, 0]</code> อ่านชื่อคอลัมน์, <code>table[0, r]</code> อ่านชื่อแถว</td></tr>
<tr><td><code>XDim</code>/<code>YDim</code> อ่านได้อย่างเดียว</td><td>แต่การเขียนค่าเกินขอบเขตปัจจุบันจะขยายตารางอัตโนมัติ</td></tr>
<tr><td>คอลัมน์ใหม่เป็น string โดยดีฟอลต์</td><td>เขียนตัวเลขตรงๆ (เช่น <code>table[1,1] := 99</code>) จะ error ต้องเขียนเป็น string เช่น <code>"99"</code> จนกว่าจะตั้งชนิดคอลัมน์ผ่าน GUI</td></tr>
</table>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> ทำไม <code>.InformationFlow.Variable.createObject(...)</code> ถึง error ว่า
"A 'integer' cannot accept the method 'createObject'"?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะ path เปล่าๆ ไปที่ <code>Variable</code> auto-deref กลายเป็นค่า integer (ค่าเริ่มต้น 0) ของตัวแปรนั้นไปแล้ว
ไม่ใช่ตัว Object — ต้องใช้ <code>.Node("Variable")</code> เพื่อขอ Object reference ก่อนเรียก <code>createObject</code></div>
'''

BODY[("advanced", 4)] = '''
<h2>สร้าง Object ด้วยโค้ด: createObject</h2>
<p>การสร้าง Object เป็นการเรียก method บน <strong>class template เอง</strong> ไม่ใช่ global function:</p>
<pre><code>var f := .MaterialFlow.Frame.createObject(.Models, 0, 0)
f.Name := "Transporting"
var src := .MaterialFlow.Source.createObject(f, 50, 100)
src.Name := "Source"</code></pre>
<table>
<tr><th>กติกา</th><th>รายละเอียด</th></tr>
<tr><td>container ต้องเป็น Frame หรือ Folder</td><td>อย่างอื่น error "Argument 1 is neither a Frame nor a Folder"</td></tr>
<tr><td>x, y เป็นตำแหน่งบังคับ</td><td>ไม่มี overload แบบไม่ระบุตำแหน่ง</td></tr>
<tr><td>Object ใหม่ได้ชื่ออัตโนมัติ</td><td>ควรตั้งชื่อเองทันทีผ่าน <code>obj.Name := "..."</code></td></tr>
</table>

<h2>เชื่อมต่อ Object: Connector.connect</h2>
<pre><code>.MaterialFlow.Connector.connect(src, trk)
.MaterialFlow.Connector.connect(trk, drn)</code></pre>
<p>สร้าง Connector จริงเหมือนลากด้วยมือ ตรวจสอบได้ด้วย <code>obj.succ(1)</code> ซึ่งอ่านค่า Object ถัดไปที่เชื่อมอยู่</p>

<h2>ทำให้ Transporter ขับเคลื่อนเอง (จุดที่มักพลาด)</h2>
<p>Transporter ที่ Duplicate มาวางบน Track แล้ว แม้ตั้ง <code>Speed</code> ไว้ก็ยัง<strong>ไม่วิ่ง</strong>ถ้าไม่ตั้งค่าทั้งสองนี้ครบ:</p>
<pre><code>veh.Destination := drn          // ปลายทางที่ต้องไปถึง
veh.AutomaticRouting := true    // ให้คำนวณเส้นทางเองผ่าน Connector</code></pre>

<div class="note">
<strong>กับดักตอนเช็คผล:</strong> เช็คว่าชิ้นงานถึงปลายทางหรือยังด้วย <code>Drain.StatDeleted</code> (จำนวนสะสมที่ Drain เคยทำลายไปแล้ว)
<strong>ไม่ใช่</strong> <code>Drain.NumMU</code> (จำนวนที่อยู่ในนั้น ณ ขณะนี้ ซึ่งเป็น 0 เสมอเพราะ Drain ทำลายชิ้นงานทันทีที่รับเข้า)
เช็คตัวหลังผิดจะดูเหมือนโมเดลค้าง ทั้งที่จริงทำงานถูกต้องอยู่แล้ว
</div>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> รันโมเดลที่สร้างด้วยโค้ดไปไม่กี่วินาที แล้ว <code>Drain.StatDeleted</code> ยังเป็น 0 อยู่ ควรสรุปว่าโมเดลพังทันทีหรือไม่?
</div>
<div class="tip"><strong>เฉลย:</strong> ยังสรุปไม่ได้ — โมเดลใหม่ที่สร้างด้วย <code>app.NewModel()</code> มักรันใกล้เคียงเวลาจริง (ไม่เร็วจัดเหมือนโมเดลสำเร็จรูปบางไฟล์)
และ ProcTime ดีฟอลต์มักอยู่ราว 10 วินาที ควรเช็ค <code>EventController.SimTime</code> ว่าเวลาจำลองเดินไปเท่าไหร่แล้ว และเช็ค <code>NumMU</code>
ของแต่ละสถานีว่าชิ้นงานติดอยู่ตรงไหนก่อนสรุปว่าพัง</div>
'''

BODY[("advanced", 5)] = '''
<h2>Experiment Manager คืออะไร</h2>
<p>ใช้สำหรับรันโมเดลหลายๆ รอบด้วยค่าพารามิเตอร์ต่างกันโดยอัตโนมัติ (เช่น เปรียบเทียบจำนวนเครื่องจักร 2 vs 3 เครื่อง)
แทนที่จะเปลี่ยนค่าแล้ว Reset แล้วรันเองทีละรอบ</p>

<h2>ขั้นตอนตั้งค่า</h2>
<ol class="steps">
<li>เปิด <strong>Experiment Manager</strong> จาก Class Library หมวด <code>Tools</code></li>
<li>เพิ่ม Scenario แล้วกำหนดค่าตัวแปร (Input) ที่จะเปลี่ยนในแต่ละรอบ — เช่น จำนวนสถานี, ProcTime, Capacity ของ Buffer</li>
<li>กำหนดค่าที่ต้องการดูผลลัพธ์ (Output) เช่น Throughput, Utilization, StatDeleted ของ Drain</li>
<li>กด <strong>Run All</strong> เพื่อรันทุก Scenario อัตโนมัติแล้วเปรียบเทียบผลในตารางเดียว</li>
</ol>

<div class="tip">
<strong>Tip:</strong> ตั้งชื่อ Scenario ให้สื่อความหมาย (เช่น <code>2_Machines</code>, <code>3_Machines</code>) แทนชื่อดีฟอลต์
<code>Scenario1/2/3</code> — เมื่อ Scenario เยอะขึ้นจะอ่านผลเปรียบเทียบได้ง่ายกว่ามาก
</div>

<h2>ต่อยอดสู่ Optimization</h2>
<p><strong>Optimizer</strong> ต่อยอดจาก Experiment Manager โดยใช้ขั้นตอนวิธีค้นหาอัตโนมัติ (เช่น Genetic Algorithm ผ่าน GAWizard
ดูบทที่ 6) แทนการกำหนด Scenario เองทีละชุด — เหมาะเมื่อพารามิเตอร์ที่ต้องปรับมีหลายตัวจนลองเองทุกชุดไม่ไหว</p>

<div class="note">
<strong>คำถามฝึกคิด:</strong> เมื่อไหร่ควรใช้ Experiment Manager ธรรมดา เมื่อไหร่ควรใช้ Optimizer/GAWizard?
</div>
<div class="tip"><strong>เฉลย:</strong> ถ้าพารามิเตอร์ที่สนใจมีไม่กี่ตัวและมีชุดค่าที่ชัดเจนอยู่แล้ว (เช่น เทียบ 2 กับ 3 เครื่อง) ใช้ Experiment Manager
ธรรมดาพอ ไล่ดูผลได้ตรงไปตรงมา — แต่ถ้าพารามิเตอร์มีหลายตัวและช่วงค่ากว้าง (เช่น หา Capacity ของ Buffer 5 จุดพร้อมกันที่ทำให้ Throughput สูงสุด)
การไล่ลองเองทุกชุดจะใช้เวลานานเกินไป ควรใช้ Optimizer ให้ค้นหาแทน</div>
'''

BODY[("advanced", 6)] = '''
<h2>GAWizard คืออะไร</h2>
<p><strong>GAWizard</strong> คือเครื่องมือ Optimization ด้วย Genetic Algorithm ที่มากับ Plant Simulation
อยู่ในหมวด <code>.Tools</code> เช่นเดียวกับ BottleneckAnalyzer และ ExperimentManager</p>

<div class="note">
<strong>ข้อจำกัดสำคัญ:</strong> GAWizard เป็น Object ที่<strong>สร้างผ่าน GUI wizard เท่านั้น</strong> — เรียก
<code>.Tools.GAWizard.createObject(...)</code> จากโค้ดตรงๆ จะ error ("'GAWizard' cannot be adopted by...")
เอกสารทางการของ Siemens เองก็ยืนยันว่าขั้นตอนคือ "คลิก Tools บน toolbar แล้วแทรก GAWizard เข้าไปในโมเดล" — เป็นการกระทำผ่าน GUI
ล้วนๆ ไม่มีทางสร้างผ่านสคริปต์เพียงอย่างเดียว
</div>

<h2>ขั้นตอนตั้งค่าผ่าน GUI</h2>
<ol class="steps">
<li>เตรียม <strong>DataTable</strong>/<strong>Variable</strong> ที่เก็บพารามิเตอร์ที่จะให้ Optimize (ดูบทที่ 3 สำหรับวิธีสร้าง)</li>
<li>คลิก Tools บน toolbar → แทรก GAWizard เข้าไปในโมเดล</li>
<li>ลากตาราง/ตัวแปรที่ต้องการ Optimize ไปวางบน GAWizard พร้อมกดปุ่ม Shift ค้างไว้ (ตามที่คู่มือระบุ)
หรือลาก Object ประเภท GA (<code>GASelection</code>, <code>GASequence</code>, <code>GARangeAllocation</code>, <code>GASetAllocation</code>)
ไปวางแล้วแก้ไข configuration method ที่เกิดขึ้น</li>
<li>กำหนดค่า Fitness function (สิ่งที่ต้องการ maximize/minimize เช่น Throughput)</li>
<li>รัน GAWizard ให้ค้นหาค่าพารามิเตอร์ที่ดีที่สุดข้ามหลายเจเนอเรชัน</li>
</ol>

<h2>แอตทริบิวต์ที่ใช้บ่อยเมื่อมี instance แล้ว</h2>
<table>
<tr><th>แอตทริบิวต์</th><th>ความหมาย</th></tr>
<tr><td><code>penaltyValue</code></td><td>ค่า fitness ที่ให้กับ individual ที่ parametrize แล้วล้มเหลว</td></tr>
<tr><td><code>DecimalSeparator</code></td><td>ตัวคั่นทศนิยมในรายงาน (<code>.</code> หรือ <code>,</code>)</td></tr>
<tr><td><code>lastGeneration4DuplicatesCheck</code></td><td>จำนวนเจเนอเรชันที่เช็คไม่ให้ประเมินซ้ำ (<code>-1</code> = เช็คทุกเจเนอเรชัน)</td></tr>
<tr><td><code>ShowRuntimeAtEnd</code>, <code>AskForSaveModel</code>, <code>ShowHTMLatEnd</code></td><td>ตัวเลือกโหมด batch เท่านั้น</td></tr>
</table>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> ถ้าต้องการสร้างโมเดล optimization ใหม่แบบอัตโนมัติทั้งหมดโดยไม่แตะ GUI เลย ทำได้ไหม?
</div>
<div class="tip"><strong>เฉลย:</strong> การใช้ GAWizard ของแท้ทำไม่ได้ (ข้อจำกัดข้างบน) แต่มีทางเลือก: (1) เตรียม instance ที่ config ไว้แล้วในโมเดลอื่น
แล้ว duplicate/derive มันแทนการสร้างใหม่จาก class template หรือ (2) เขียน Optimization "ด้วยมือ" เองทั้งหมดจาก DataTable/Variable/Method
(fitness, selection, mutation) ตามที่เรียนในบทที่ 3-4 ซึ่งเป็นการ reimplement สิ่งที่ GAWizard ทำให้อัตโนมัติ แทนที่จะใช้ตัวสำเร็จรูป</div>
'''

BODY[("advanced", 7)] = '''
<div class="note">
<strong>บทเสริม:</strong> บทนี้สำหรับผู้ที่ต้องการเชื่อมต่อ Plant Simulation จากภายนอกโปรแกรม เช่น เขียนสคริปต์ Python
ควบคุมการรันแบบอัตโนมัติ (automation/integration) — ไม่จำเป็นสำหรับการใช้งานโปรแกรมทั่วไป
</div>

<h2>เชื่อมต่อแบบ Headless ผ่าน COM</h2>
<p>Plant Simulation ลงทะเบียน COM ProgID เฉพาะแต่ละเวอร์ชันไว้ ตามรูปแบบ
<code>Tecnomatix.PlantSimulation.RemoteControl.&lt;MAJOR&gt;.&lt;MINOR&gt;</code> เช่นเวอร์ชัน 2201 คือ
<code>Tecnomatix.PlantSimulation.RemoteControl.22.1</code> (สังเกตจุดคั่น ไม่ใช่ <code>.2201</code>)</p>

<div class="note">
<strong>ควรใช้ ProgID เฉพาะเวอร์ชันเสมอ:</strong> ProgID แบบทั่วไป (ไม่ระบุเวอร์ชัน) จะชี้ไปยังเวอร์ชันล่าสุดที่เพิ่งลงทะเบียนตัวเองเป็นค่าเริ่มต้น
ซึ่งเปลี่ยนได้ตามการติดตั้ง — ถ้าต้องการความแน่นอนว่าเชื่อมต่อเวอร์ชันไหน ให้ระบุ ProgID แบบมีเลขเวอร์ชันเสมอ
</div>

<h2>การเชื่อมต่อขั้นต่ำใน Python (ใช้ pywin32)</h2>
<pre><code>import win32com.client

PROGID = "Tecnomatix.PlantSimulation.RemoteControl.22.1"

app = win32com.client.Dispatch(PROGID)
app.SetVisible(False)          # ไม่แสดงหน้าต่างโปรแกรมเลย
app.SetNoMessageBox(True)      # ปิด dialog ที่อาจค้างรอผู้ใช้กด
app.loadModel(r"C:\\path\\to\\Model.spp")
# ... สั่งงานผ่าน ExecuteSimTalk ตามบทที่ 1-4 ...
app.Quit()                     # ปิดให้เรียบร้อยทุกครั้ง</code></pre>

<table>
<tr><th>กติกา</th><th>รายละเอียด</th></tr>
<tr><td><code>SetVisible</code>/<code>SetNoMessageBox</code> ต้องเรียกก่อน <code>loadModel</code></td><td>ถ้าอยากให้การโหลดโมเดลเงียบสนิทตั้งแต่ต้น</td></tr>
<tr><td>ต้อง <code>Quit()</code> ทุกครั้ง</td><td>ไม่ปิดจะมีโปรเซสค้างอยู่เบื้องหลังสะสมไปเรื่อยๆ</td></tr>
<tr><td><code>ExecuteSimTalk</code> รับพารามิเตอร์เดียว</td><td>คือ source code string — path ของ Object ต้องฝังอยู่ในสตริงโค้ดเอง ไม่ใช่พารามิเตอร์แยก</td></tr>
</table>

<h2>รันโค้ด SimTalk จาก Python</h2>
<pre><code>result = app.ExecuteSimTalk('->integer; return .Models.Model.NumNodes')
print(result)</code></pre>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> ทำไมต้องเรียก <code>Quit()</code> ทุกครั้งแม้สคริปต์จะจบการทำงานแล้ว?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะโปรเซส Plant Simulation ที่เปิดผ่าน COM เป็นโปรเซสจริงที่รันอยู่เบื้องหลัง (แม้ตั้ง SetVisible(False) ไว้ก็ตาม)
ถ้าสคริปต์จบโดยไม่ปิดมัน โปรเซสจะยังค้างกินหน่วยความจำอยู่ และถ้ารันสคริปต์แบบนี้ซ้ำหลายรอบโดยไม่ Quit จะมีโปรเซสค้างสะสมเพิ่มขึ้นเรื่อยๆ</div>
'''

BODY[("object-reference", 1)] = '''
<p class="lead" style="max-width:46em;">Object กลุ่มนี้คือสิ่งที่ชิ้นงานไหลผ่านโดยตรง ครอบคลุมทั้งที่เรียนไปแล้วในระดับ Basic/Intermediate
รวมไว้ที่เดียวเป็นแหล่งอ้างอิงเร็วๆ</p>

<h2>Source</h2>
<p>จุดกำเนิดชิ้นงาน (MU) เข้าสู่ระบบ ควบคุมด้วย <code>Interval</code></p>
<div class="tip"><strong>ลองสาธิต:</strong> วาง Source เดี่ยวๆ ต่อ Drain ตั้ง <code>Interval := 2</code> วินาที รันแล้วดู
<code>Drain.StatDeleted</code> เพิ่มขึ้นทุก 2 วินาที — ยืนยันว่า Interval คุมจังหวะการผลิตจริง</div>

<h2>Line</h2>
<p>สายพานลำเลียงระหว่างสถานี มีความเร็ว/ความยาวจำลองเวลาขนส่งจริง ต่างจากการเชื่อม Object ตรงๆ ที่ไม่มีเวลาขนส่งเลย</p>
<div class="tip"><strong>ลองสาธิต:</strong> เพิ่ม Line ยาว 50m ความเร็ว 1m/s คั่นกลาง Source-Drain จะเห็นชิ้นงานใช้เวลาประมาณ 50 วินาทีบน Line ก่อนถึง Drain</div>

<h2>SingleProc</h2>
<p>สถานีประมวลผล 1 หัว ควบคุมด้วย <code>ProcTime</code> — ดูรายละเอียดเต็มที่ <a href="basic-03.html">Basic บทที่ 3</a></p>

<h2>Buffer / Store</h2>
<p>พักชิ้นงานคอยส่งต่อ — Buffer แบบ FIFO ธรรมดา, Store มีตำแหน่งจัดเก็บย่อยหยิบสุ่มได้ ดูเปรียบเทียบที่ <a href="intermediate-01.html">Intermediate บทที่ 1</a></p>

<h2>Drain</h2>
<p>จุดทำลายชิ้นงานเมื่อออกจากระบบ (สินค้าสำเร็จรูป) — <code>StatDeleted</code> คือตัวนับสะสมที่ใช้บ่อยที่สุดเวลาวัด Throughput</p>

<h2>EventController</h2>
<p>นาฬิกาของโมเดล ต้องมีเสมอ 1 ตัวต่อโมเดล อ่านเวลาปัจจุบันด้วย <code>SimTime</code></p>

<h2>AssemblyStation</h2>
<p>รวมชิ้นงานจากหลายทางเข้าเป็นชิ้นเดียว รอครบทุกอินพุตก่อนประมวลผล — ดูตัวอย่างที่ <a href="intermediate-01.html">Intermediate บทที่ 1</a></p>

<h2>Track + Transporter</h2>
<p>เส้นทางให้พาหนะขับเคลื่อนเอง — ต้องตั้ง <code>Destination</code> และ <code>AutomaticRouting</code> ให้ Transporter ถึงจะวิ่งจริง
(กับดักที่พบบ่อย ดูเต็มๆ ที่ <a href="advanced-04.html">Advanced บทที่ 4</a>)</p>

<h2>Diverter</h2>
<p>แยกเส้นทางชิ้นงานออกเป็นหลายทาง มักผูก Method ตัดสินใจว่าจะส่งไปทางไหน (ดูตัวอย่างที่ <a href="examples.html">Example File</a>)</p>
'''

BODY[("object-reference", 2)] = '''
<p class="lead" style="max-width:46em;">Object กลุ่มนี้ไม่ใช่เส้นทางที่ชิ้นงานไหลผ่าน แต่เป็นตัวเก็บข้อมูลและตรรกะที่ควบคุมพฤติกรรมของ Object อื่น
ทั้งหมดอยู่ใต้ <code>.InformationFlow</code> และมีกับดัก auto-deref ร่วมกัน — รายละเอียดเต็มที่ <a href="advanced-03.html">Advanced บทที่ 3</a></p>

<h2>Method</h2>
<p>Object ที่เก็บโค้ด SimTalk เรียกทำงานเองหรือผูกกับเหตุการณ์ของ Object อื่นได้ — ดู <a href="advanced-01.html">Advanced บทที่ 1</a>
และ <a href="advanced-02.html">บทที่ 2</a></p>

<h2>Variable</h2>
<p>ตัวแปรเก็บค่าเดี่ยว อ่าน/เขียนได้ทั้งจาก GUI และสคริปต์ ใช้บ่อยเป็นตัวนับสะสมหรือค่าคงที่ของโมเดล เช่น <code>Constraint</code> ในโจทย์ GA</p>

<h2>DataTable</h2>
<p>ตารางข้อมูล 2 มิติ เข้าถึงด้วย bracket indexing <code>[col, row]</code> — ดู <a href="advanced-03.html">Advanced บทที่ 3</a></p>

<h2>Trigger</h2>
<p>เรียก Method ให้ทำงานเป็นระยะเวลาซ้ำๆ ตามคาบที่ตั้งไว้ ไม่ต้องผูกกับเหตุการณ์ของ Object อื่น — ดู <a href="advanced-02.html">Advanced บทที่ 2</a></p>
'''

BODY[("object-reference", 3)] = '''
<p class="lead" style="max-width:46em;">Object กลุ่มนี้ไม่ได้อยู่ในเส้นทางการไหลของชิ้นงาน แต่เป็นทรัพยากรที่ Object อื่นเรียกใช้ หรือเครื่องมือวิเคราะห์/ทดลองที่ครอบโมเดลทั้งก้อนอยู่อีกที</p>

<h2>Worker / Resource pool</h2>
<p>จำลองคนงานหรือทรัพยากรที่ใช้ร่วมกันระหว่างหลายสถานี — สถานีที่ต้องรอ Worker ว่างก่อนเริ่มงานจะแสดงสถานะรออยู่จนกว่า Worker จะว่าง</p>

<h2>BottleneckAnalyzer</h2>
<p>จัดอันดับสถานีที่เป็นคอขวดให้อัตโนมัติจากผลรัน แทนไล่ดู Statistics ทีละสถานีเอง — ดู <a href="intermediate-05.html">Intermediate บทที่ 5</a></p>

<h2>ExperimentManager</h2>
<p>รันหลาย Scenario เปรียบเทียบผลลัพธ์อัตโนมัติ — ดู <a href="advanced-05.html">Advanced บทที่ 5</a></p>

<h2>GAWizard</h2>
<p>Optimization ด้วย Genetic Algorithm ตั้งค่าผ่าน GUI wizard เท่านั้น สร้างจากโค้ดตรงๆ ไม่ได้ — ดู <a href="advanced-06.html">Advanced บทที่ 6</a></p>
'''

BODY[("case-study", 1)] = '''
<h2>บริบทอุตสาหกรรม</h2>
<p>สายการประกอบยานยนต์มีสถานีเรียงต่อกันหลายสิบสถานี แต่ละสถานีติดตั้งชิ้นส่วนต่างกัน (ประตู, เบาะ, ระบบไฟฟ้า ฯลฯ)
เวลาแปรรูปแต่ละสถานีต่างกันและมีการหยุดสายบ่อยจากปัญหาชิ้นส่วนขาด/เครื่องมือขัดข้อง</p>

<h2>โจทย์ตัวอย่าง</h2>
<p>โรงงานต้องการเพิ่ม Throughput จาก 40 เป็น 50 คัน/กะ โดยยังไม่อยากลงทุนสร้างสถานีใหม่ทั้งหมด — ต้องรู้ก่อนว่าจุดไหนคือคอขวดจริง</p>

<h2>โครงสร้างโมเดล</h2>
<ul>
<li>สาย SingleProc เรียงต่อกัน 15-20 สถานี เชื่อมด้วย Line (ดู <a href="basic-04.html">Basic บทที่ 4</a>)</li>
<li>ตั้ง Failure แบบ MTBF/MTTR ต่างกันในแต่ละสถานีตามข้อมูลจริงจากโรงงาน (<a href="intermediate-04.html">Intermediate บทที่ 4</a>)</li>
<li>ตั้ง ProcTime เป็น Distribution สะท้อนความเร็วคนงานที่ไม่เท่ากันทุกคัน (<a href="intermediate-03.html">Intermediate บทที่ 3</a>)</li>
<li>ใช้ BottleneckAnalyzer หาสถานีคอขวดจริง แทนการเดาจากประสบการณ์ (<a href="intermediate-05.html">Intermediate บทที่ 5</a>)</li>
</ul>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ถ้า BottleneckAnalyzer ชี้ว่าสถานีที่ 12 เป็นคอขวด แต่สถานีนี้ราคาเครื่องจักรทดแทนแพงมาก มีทางเลือกอื่นไหมนอกจากซื้อเครื่องใหม่?
</div>
<div class="tip"><strong>เฉลย:</strong> ลองทดสอบใน Experiment Manager (<a href="advanced-05.html">Advanced บทที่ 5</a>) เปรียบเทียบ Scenario เช่น
เพิ่ม Buffer ก่อน/หลังสถานีนั้น, ลด MTTR ด้วยทีมซ่อมเร็วขึ้น, หรือเพิ่มสถานีสำรองขนานเฉพาะจุด — เห็นผลเปรียบเทียบก่อนตัดสินใจลงทุนจริง</div>
'''

BODY[("case-study", 2)] = '''
<h2>บริบทอุตสาหกรรม</h2>
<p>คลังสินค้าขนาดใหญ่ใช้ AGV (รถขนส่งอัตโนมัติ) วิ่งรับ-ส่งพาเลทระหว่างโซนรับเข้า, ชั้นวาง, และโซนจัดส่ง
ความท้าทายคือจำนวน AGV ที่พอเหมาะ — น้อยไปสินค้าค้าง มากไปลงทุนเกินจำเป็น</p>

<h2>โจทย์ตัวอย่าง</h2>
<p>ต้องการหาจำนวน AGV ต่ำสุดที่ยังทำให้พาเลททุกใบถึงชั้นวางภายใน 15 นาทีหลังรับเข้า</p>

<h2>โครงสร้างโมเดล</h2>
<ul>
<li>Track เป็นโครงข่ายเส้นทางในคลัง, Transporter คือ AGV แต่ละคัน (<a href="intermediate-01.html">Intermediate บทที่ 1</a>)</li>
<li>Store จำลองชั้นวางที่หยิบสินค้าได้ไม่เรียงลำดับ (<a href="intermediate-01.html">Intermediate บทที่ 1</a>)</li>
<li>ตั้ง <code>Destination</code>/<code>AutomaticRouting</code> ให้ AGV แต่ละคันขับเคลื่อนเองตามเส้นทางที่คำนวณ (<a href="advanced-04.html">Advanced บทที่ 4</a>)</li>
<li>ใช้ Experiment Manager ไล่จำนวน AGV ตั้งแต่ 3, 4, 5, ... คัน เปรียบเทียบเวลาเฉลี่ยที่พาเลทถึงชั้นวาง (<a href="advanced-05.html">Advanced บทที่ 5</a>)</li>
</ul>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ทำไมการเพิ่ม AGV จาก 3 เป็น 4 คันอาจลดเวลาเฉลี่ยได้มาก แต่เพิ่มจาก 6 เป็น 7 คันแทบไม่ต่างเลย?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะเมื่อ AGV มีมากพอแล้ว คอขวดที่แท้จริงจะย้ายไปอยู่ที่จุดอื่นแทน เช่น ความเร็วในการหยิบสินค้าที่ Store เอง
หรือความแออัดของเส้นทางที่ AGV วิ่งชนกันบ่อยขึ้น — การเพิ่ม AGV เกินจุดนั้นจึงไม่ช่วยอะไรแล้ว ต้องหาคอขวดใหม่ต่อ</div>
'''

BODY[("case-study", 3)] = '''
<h2>บริบทอุตสาหกรรม</h2>
<p>สาย SMT (Surface-Mount Technology) วางชิ้นส่วนอิเล็กทรอนิกส์ขนาดเล็กมากลงบนแผ่น PCB ด้วยความเร็วสูงและความแม่นยำสูง
ปัญหาหลักคือ Yield (สัดส่วนแผ่นที่ผ่านมาตรฐาน) ไม่ใช่แค่ Throughput</p>

<h2>โจทย์ตัวอย่าง</h2>
<p>สาย SMT มี Reject rate 3% ที่สถานีตรวจสอบ (AOI) ต้องการรู้ว่าถ้าเพิ่มสถานี Rework คู่ขนาน จะช่วยเพิ่ม Throughput สุทธิ (แผ่นที่ผ่านจริง) เท่าไหร่</p>

<h2>โครงสร้างโมเดล</h2>
<ul>
<li>SingleProc ต่อกันจำลองสถานี Print Paste → Place Component → Reflow → AOI</li>
<li>ที่ AOI ใช้ Diverter แยกแผ่นที่ Reject ออกไปเข้าสถานี Rework แยกต่างหาก (<a href="object-reference-01.html">Object Reference: Material Flow</a>)</li>
<li>ตั้ง Failure ที่สถานี Place Component ให้ถี่กว่าสถานีอื่น (หัวจับชิ้นส่วนสึกบ่อย) (<a href="intermediate-04.html">Intermediate บทที่ 4</a>)</li>
<li>ใช้ Method ผูกกับ Diverter ตัดสินใจ Reject/Pass แบบสุ่มตามอัตราจริง (<a href="advanced-02.html">Advanced บทที่ 2</a>)</li>
</ul>

<div class="note">
<strong>คำถามฝึกคิด:</strong> เพิ่มสถานี Rework คู่ขนานแล้ว Throughput สุทธิเพิ่มขึ้น แต่ยังไม่คุ้มกับต้นทุนที่เพิ่ม ควรดูตัวเลขอะไรเพิ่มก่อนตัดสินใจ?
</div>
<div class="tip"><strong>เฉลย:</strong> ควรดู Utilization ของสถานี Rework ที่เพิ่มมาด้วย (จาก Statistics) — ถ้า Utilization ต่ำมาก แปลว่าลงทุนเกินความจำเป็น
ทางที่คุ้มกว่าอาจเป็นการลด Reject rate ที่ต้นทาง (แก้ที่ Place Component) แทนที่จะเพิ่มสถานีรับมือปลายทาง</div>
'''

BODY[("case-study", 4)] = '''
<h2>บริบทอุตสาหกรรม</h2>
<p>สายบรรจุภัณฑ์อาหารมีข้อจำกัดที่อุตสาหกรรมอื่นไม่ค่อยมี — วัตถุดิบมีอายุการเก็บรักษาจำกัด (shelf life) และมักต้องทำความสะอาดสายเป็นระยะ (CIP)
ซึ่งหยุดสายทั้งหมดเป็นเวลานานกว่าการเสียของเครื่องจักรทั่วไป</p>

<h2>โจทย์ตัวอย่าง</h2>
<p>ต้องการวางแผนตารางทำความสะอาด (CIP) ให้กระทบ Throughput น้อยที่สุด โดยไม่ทำให้วัตถุดิบที่รอคิวเกินอายุการเก็บรักษา</p>

<h2>โครงสร้างโมเดล</h2>
<ul>
<li>Source ป้อนวัตถุดิบด้วย Distribution สะท้อนความไม่แน่นอนของซัพพลาย (<a href="intermediate-03.html">Intermediate บทที่ 3</a>)</li>
<li>Buffer ก่อนสถานีบรรจุ ต้องจำกัดเวลาพักคอยไม่ให้เกินอายุการเก็บรักษา — ใช้ Method เช็คเวลาที่ชิ้นงานอยู่ในระบบ (<a href="advanced-02.html">Advanced บทที่ 2</a>)</li>
<li>จำลองรอบ CIP เป็น Failure แบบ Time-based ที่หยุดทั้งสาย ไม่ใช่ Failure สุ่มแบบสถานีเดียว (<a href="intermediate-04.html">Intermediate บทที่ 4</a>)</li>
<li>ใช้ Experiment Manager เทียบตารางเวลา CIP หลายแบบ (<a href="advanced-05.html">Advanced บทที่ 5</a>)</li>
</ul>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ทำไมโมเดลนี้ต้อง "เช็คเวลาที่ชิ้นงานอยู่ในระบบ" ด้วย Method เอง แทนที่จะใช้ Buffer Capacity ธรรมดาคุมพอ?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะ Capacity คุมแค่ "จำนวน" ชิ้นงานที่พักได้ ไม่ได้คุม "เวลา" ที่แต่ละชิ้นพักอยู่ — วัตถุดิบอาหารเสียเมื่อรอนานเกินไป
ไม่ใช่เมื่อ Buffer เต็ม ต้องเขียน Method ผูกกับ Entrance/Exit เพื่อคำนวณเวลาที่แต่ละชิ้นอยู่ในระบบจริงแทน</div>
'''

BODY[("tips-tricks", 1)] = '''
<h2>จำ Layout หน้าจอที่ชอบไว้</h2>
<p>ถ้าเรียงพาเนลจนพอใจแล้ว บันทึก Layout ไว้ (ถ้าเวอร์ชันรองรับ) แทนที่จะจัดใหม่ทุกครั้งที่เปิดโปรแกรม</p>

<h2>ใช้ Navigator แทนการไล่หา Object ด้วยตา</h2>
<p>เมื่อโมเดลมี Object เยอะและซ้อน Frame หลายชั้น การพิมพ์ค้นหาใน Navigator เร็วกว่าการไล่คลิกหาเองมาก</p>

<h2>ตั้งชื่อ Object ตั้งแต่วางครั้งแรก</h2>
<p>อย่าปล่อยชื่อดีฟอลต์ (<code>SingleProc1</code>, <code>SingleProc2</code>) ไว้นาน — เปลี่ยนเป็นชื่อสื่อความหมายทันทีที่วาง
ก่อนที่โมเดลจะใหญ่จนย้อนมาไล่เปลี่ยนทีหลังลำบาก</p>

<h2>คลิกขวาก่อนเสมอเมื่อไม่แน่ใจ</h2>
<p>เมนูคลิกขวาของแต่ละ Object มักมีทางลัดไปหน้าที่ต้องการ (Statistics, Reset, Duplicate) เร็วกว่าเปิด Attribute window แล้วไล่หาแท็บเอง</p>
'''

BODY[("tips-tricks", 2)] = '''
<h2>เช็ค EventController ก่อนเสมอถ้ารันไม่ได้</h2>
<p>อาการ "กด Start แล้วไม่มีอะไรเกิดขึ้นเลย" ส่วนใหญ่มาจากลืมวาง EventController — เช็คจุดนี้ก่อนสงสัยอย่างอื่น</p>

<h2>Reset ก่อนรันใหม่ทุกครั้งที่เปลี่ยนค่า</h2>
<p>ลืม Reset คือสาเหตุอันดับต้นๆ ที่ทำให้ผลวิเคราะห์ผิดเพี้ยน เพราะสถิติสะสมปนกับรอบก่อนหน้า</p>

<h2>Blocked สูง = ปัญหาอยู่ปลายทาง ไม่ใช่ตัวเอง</h2>
<p>ถ้า Object หนึ่ง Blocked บ่อย อย่าเพิ่งแก้ที่ตัวมันเอง — ให้ไล่ดูสถานีถัดไปที่มันส่งงานให้ก่อนเสมอ</p>

<h2>StatDeleted ไม่ใช่ NumMU เวลาเช็คว่าถึงปลายทางหรือยัง</h2>
<p>Drain ทำลายชิ้นงานทันทีที่รับเข้า ทำให้ <code>NumMU</code> เป็น 0 เสมอไม่ว่าโมเดลจะทำงานถูกหรือพัง — ใช้ <code>StatDeleted</code> (ตัวนับสะสม) แทน</p>

<h2>ยังไม่มีชิ้นงานถึงปลายทาง ≠ โมเดลพัง</h2>
<p>เช็ค <code>EventController.SimTime</code> ก่อนสรุปว่าพัง — บางโมเดลรันใกล้เคียงเวลาจริง ต้องรอเวลาจำลองสะสมมากพอก่อนชิ้นงานจะไหลถึงปลายสาย</p>
'''

BODY[("tips-tricks", 3)] = '''
<h2>ปิดภาพเคลื่อนไหว/มุมมอง 3D เวลารันเก็บสถิติ</h2>
<p>ถ้าไม่ต้องการดูภาพเคลื่อนไหวระหว่างรัน (เช่นตอนรันเก็บผลอย่างเดียว) ปิดการแสดงผล/ลดความเร็วแอนิเมชันจะรันเร็วขึ้นมาก
โดยไม่กระทบผลลัพธ์เชิงตัวเลขเลย</p>

<h2>ใช้ Experiment Manager แทนการรันมือซ้ำๆ</h2>
<p>การรันหลาย Scenario ด้วยมือ (เปลี่ยนค่า → Reset → รัน → จด → ทำซ้ำ) ทั้งช้าและเสี่ยงพลาด — ให้ Experiment Manager
รันและเก็บผลอัตโนมัติแทนเสมอเมื่อมีมากกว่า 2-3 Scenario</p>

<h2>โมเดลใหญ่มาก: ทดสอบ logic ด้วยโมเดลย่อยก่อน</h2>
<p>เวลาดีบัก Method หรือโครงสร้างใหม่ ทดสอบใน Frame เล็กๆ ที่มี Object แค่ไม่กี่ตัวก่อน แล้วค่อยย้ายไปใช้กับโมเดลเต็มขนาด —
เร็วกว่ารอโมเดลใหญ่รันครบทุกครั้งที่แก้โค้ดทีละบรรทัด</p>

<h2>ระวังสคริปต์ที่เปิด Plant Simulation ผ่าน COM ซ้ำโดยไม่ Quit</h2>
<p>สคริปต์ automation ที่ลืม <code>app.Quit()</code> จะทิ้งโปรเซสค้างไว้เบื้องหลังทุกครั้งที่รัน สะสมจนกินทรัพยากรเครื่องไปเรื่อยๆ
โดยไม่มีหน้าต่างให้เห็นเลย (ดู <a href="advanced-07.html">Advanced บทที่ 7</a>)</p>
'''

BODY[("tips-tricks", 4)] = '''
<h2>ใช้ ProgID เฉพาะเวอร์ชันเสมอเวลาต่อ COM</h2>
<p>ProgID แบบทั่วไป (ไม่ระบุเวอร์ชัน) อาจชี้ไปเวอร์ชันอื่นได้ถ้าเครื่องมีติดตั้งหลายเวอร์ชัน — ระบุเลขเวอร์ชันเสมอเพื่อความชัวร์
(<a href="advanced-07.html">Advanced บทที่ 7</a>)</p>

<h2>.Node("ClassName") ทุกครั้งที่ createObject กับ Variable/Method</h2>
<p>อ้าง path เปล่าไปที่ Variable/Method จะ auto-deref กลายเป็นค่า/ผลลัพธ์การเรียกแทนที่จะเป็นตัว Object เอง —
ต้องใช้ <code>.Node("ClassName")</code> ตอนสร้าง (<a href="advanced-03.html">Advanced บทที่ 3</a>)</p>

<h2>ห้ามตั้งชื่อตัวแปรว่า result</h2>
<p><code>result</code> เป็นคำสงวนใน SimTalk 2.0 — <code>var result := ...</code> จะ error เสมอ ใช้ชื่ออื่นแทน เช่น <code>buf</code>, <code>acc</code>
(<a href="advanced-01.html">Advanced บทที่ 1</a>)</p>

<h2>ใช้ strChr() คั่นข้อมูลแทน comma/space</h2>
<p>ชื่อ Object จริงอาจมี comma หรือ space ปนอยู่ — ใช้ <code>strChr(31)</code>/<code>strChr(30)</code> เป็นตัวคั่นที่ปลอดภัยกว่าเวลาต่อ string
หลายค่าเข้าด้วยกันแล้วค่อยแยกทีหลัง (<a href="advanced-01.html">Advanced บทที่ 1</a>)</p>
'''

# ---------------------------------------------------------------------------
def chapter_page(section, idx):
    title = SECTIONS[section]["chapters"][idx - 1]
    objs = OBJECTIVES[(section, idx)]
    objs_html = "\n".join(f"          <li>{o}</li>" for o in objs)
    body_content = BODY[(section, idx)].strip()

    # prev/next
    if idx > 1:
        prev_href = chapter_filename(section, idx - 1)
        prev_label = f"← ก่อนหน้า: {idx - 1}. {SECTIONS[section]['chapters'][idx - 2]}"
    else:
        prev_href = SECTIONS[section]["hub"]
        prev_label = f"← กลับหน้ารวมบท {SECTIONS[section]['label'].split(' — ')[0]}"

    n_chapters = len(SECTIONS[section]["chapters"])
    if idx < n_chapters:
        next_href = chapter_filename(section, idx + 1)
        next_label = f"ถัดไป: {idx + 1}. {SECTIONS[section]['chapters'][idx]} →"
    else:
        sec_idx = SECTION_ORDER.index(section)
        if sec_idx < len(SECTION_ORDER) - 1:
            next_sec = SECTION_ORDER[sec_idx + 1]
            next_href = SECTIONS[next_sec]["hub"]
            next_label = f"ถัดไป: {SECTIONS[next_sec]['label']} →"
        else:
            next_href = "index.html"
            next_label = "จบคอร์ส — กลับหน้าแรก"

    body = f'''        <h1>{idx}. {title}</h1>

        <div class="objectives">
          <p>วัตถุประสงค์การเรียนรู้</p>
          <ol>
{objs_html}
          </ol>
        </div>

{body_content}

        <div class="page-nav">
          <a href="{prev_href}">{prev_label}</a>
          <a href="{next_href}">{next_label}</a>
        </div>'''
    return page_html(f"{idx}. {title}", body, expand_section=section, active_top=section, active_chapter=idx)


if __name__ == "__main__":
    for sec in SECTION_ORDER:
        n = len(SECTIONS[sec]["chapters"])
        for i in range(1, n + 1):
            write(chapter_filename(sec, i), chapter_page(sec, i))
    # regenerate basic.html hub via the same generator for full consistency
    write(SECTIONS["basic"]["hub"], hub_page("basic"))
