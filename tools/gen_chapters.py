# -*- coding: utf-8 -*-
"""Generates all chapter pages + regenerates basic.html hub for consistency.
Run after gen_site.py (reuses its templates by importing it)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_site import SECTIONS, SECTION_ORDER, page_html, chapter_filename, chapter_numbers, chapter_title, chapter_label, hub_page, write, HUB_INTRO, HUB_CARD_DESC, youtube_embed, screenshot, step_list, side_by_side

# ---------------------------------------------------------------------------
# Chapter objectives (2-3 goals per chapter, "เพื่อ..." style)
# ---------------------------------------------------------------------------
OBJECTIVES = {
    ("basic", "00a"): ["เข้าใจว่า Discrete Event Simulation (DES) คืออะไร และ Plant Simulation ใช้แก้ปัญหาแบบไหน",
                   "เปิด Start Page และเปิดโมเดลตัวอย่าง Factory 51 ได้ด้วยตัวเอง",
                   "หมุน ซูม เลื่อนมุมมอง 3D และโต้ตอบกับวัตถุด้วยคลิก / ดับเบิลคลิก / คลิกขวาได้",
                   "เปิด Frame ด้านในแล้วกลับออกมา และสั่ง Start / Reset / ปรับความเร็วผ่าน EventController ได้"],
    ("basic", "00b"): ["เปิดโมเดลตัวอย่าง Small Parts Production และรันเทียบไลน์เดิมกับไลน์ที่ปรับแล้วได้",
                       "หาคอขวดของไลน์ประกอบด้วย Station Utilization, Bottleneck Analyzer และ Ranking ได้",
                       "หาขนาด Buffer ที่พอด้วย Experiment Manager และอ่านผลพลังงานจาก Energy Analyzer ได้"],
    ("basic", "01"): ["รู้จักส่วนต่างๆ ของหน้าจอ และมองโมเดลแบบแปลนด้วย Planning View ได้",
                      "วาง Source → Station → Drain ต่อเส้นด้วย Connector และตั้งค่า Source, Station, EventController ได้",
                      "ใส่ Display แสดงจำนวนชิ้นงาน กด Reset / Start และอ่านผลการจำลองได้"],
    ("basic", "02"): ["แสดงชื่อ Object และวาง Display / Chart บนไลน์ผลิต 5 สถานีได้",
                      "หาคอขวดจากสีของ Chart (Working / Blocked / Waiting) ได้",
                      "แก้คอขวดด้วยเครื่องขนาน หรือ ParallelStation และรู้จักกับดัก Start Processing When Full"],
    ("basic", "03"): ["ตั้งเวลาทำงานแบบสุ่ม (Uniform) และอธิบายได้ว่าทำไมผลผลิตลดลงทั้งที่เวลาเฉลี่ยเท่าเดิม",
                      "ใส่ Buffer เป็นพื้นที่พักงาน และรู้ว่า Buffer ช่วยเมื่อไรและไม่ช่วยเมื่อไร",
                      "ตั้ง Failure ด้วย Availability และ MTTR อ่านแท็บ Statistics คำนวณ OEE และเลือกเวลาจำลองให้นานพอ"],
    ("basic", "04"): ["ต่อ Workplace, WorkerPool และ Broker ให้เครื่องใช้คนทำงานได้",
                      "ตั้ง ShiftCalendar และอ่านสถิติของคนได้"],
    ("basic", "05"): ["ปล่อยงานหลายรุ่นตามตารางและแยกงานดี/งานเสียได้",
                      "เขียน Method สั้นๆ ครั้งแรกเพื่อนับงานเสีย"],
    ("basic", "06"): ["วางไลน์บนผังโรงงานและดูในมุมมอง 3D ได้",
                      "ใช้ AGV ขนของจากคลังเข้าไลน์และเทียบจำนวน AGV ได้"],
    ("basic", "07"): ["หาคอขวดด้วย Bottleneck Analyzer ได้",
                      "ใช้ ExperimentManager หาค่าที่คุ้มที่สุดและสรุปผลเพื่อตัดสินใจได้"],

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
                      "ทำให้ Method ทำงานซ้ำตามรอบเวลาได้โดยไม่ต้องผูกกับเหตุการณ์ของ Object อื่น"],
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

    ("step-by-step", 1): ["อ่านโครงสร้าง Object ในเฟรม Model_Station/Model_ParallelStation ของไฟล์สอนจริงได้",
                          "รู้ว่าเมื่อไหร่ควรใช้ ParallelStation แทน Station เดี่ยวหลายตัว"],
    ("step-by-step", 2): ["ใช้ Chart หลายตัวตอบคำถามคนละแบบในเฟรมเดียวกันได้",
                          "เข้าใจรูปแบบตาราง ORDER/CT/ST แบบ data-driven และวิธีคำนวณ OEE"],
    ("step-by-step", 3): ["แยกหน้าที่ AssemblyStation กับ DismantleStation ได้",
                          "เข้าใจว่าทำไมเฟรม Sorter/Store ต้องมี Store พักงานก่อนประกอบ"],
    ("step-by-step", 4): ["เข้าใจว่า WorkerPool/Broker/Workplace ทำงานร่วมกันอย่างไร",
                          "อธิบายความต่างของ 3 เฟรมที่ค่อยๆ เพิ่มความซับซ้อนของระบบแรงงานได้"],
    ("step-by-step", 5): ["แยกการใช้งาน PickAndPlace, Track (AGV) และ AGVPool+Marker (AMR) ได้",
                          "เลือกระหว่างระบบขนย้ายแบบรางกับแบบอิสระให้เหมาะกับสถานการณ์ได้"],
    ("step-by-step", 6): ["ผูก Method เข้ากับ Button/DropDownList เพื่อสร้างแผงควบคุมได้",
                          "เข้าใจการใช้ Method สั่งภาพเคลื่อนไหว 3 มิติ ไม่ใช่แค่คำนวณตัวเลข"],
    ("step-by-step", 7): ["รู้จัก Object เฉพาะมุมมอง 3 มิติ (AngularConverter, Turntable, Turnplate)",
                          "เข้าใจว่าทำไมต้องตรวจสอบ Object กลุ่มนี้ในมุมมอง 3 มิติเสมอ"],
    ("step-by-step", 8): ["เชื่อมโยง GAWizard เข้ากับ DataTable และ OEE ที่เรียนไปก่อนหน้าได้",
                          "รู้จุดที่ผิดพลาดบ่อยเวลาตั้งค่าเงื่อนไขจบการค้นหาของ GAWizard"],

    ("tips-tricks", 1): ["รู้ทางลัดที่ช่วยให้ทำงานกับโปรแกรมเร็วขึ้นในชีวิตประจำวัน"],
    ("tips-tricks", 2): ["รู้ข้อผิดพลาดที่มือใหม่เจอบ่อย และวิธีเช็คให้ไวก่อนเสียเวลาไล่บั๊กผิดจุด"],
    ("tips-tricks", 3): ["รู้เทคนิคที่ช่วยให้โมเดลใหญ่รันเร็วขึ้นโดยไม่กระทบผลลัพธ์"],
    ("tips-tricks", 4): ["รู้กับดัก syntax/COM ที่พบบ่อยที่สุดเวลาเขียนสคริปต์ควบคุมโมเดล"],
}

# ---------------------------------------------------------------------------
# Chapter bodies (content sections, HTML)
# ---------------------------------------------------------------------------
BODY = {}

def planned_body(topics, frames, extra=""):
    """Outline page for a Basic chapter whose 2606 step-by-step content is still being written."""
    topics_html = "\n".join(f"<li>{t}</li>" for t in topics)
    return f'''
<div class="note">
<strong>กำลังจัดทำ:</strong> บทนี้กำลังเรียบเรียงเป็นแบบ Step by Step บน Plant Simulation 2606 พร้อมภาพหน้าจอทีละขั้น
— ด้านล่างคือโครงหัวข้อของบทที่จะได้เรียน
</div>

<h2>หัวข้อในบทนี้</h2>
<ol class="steps">
{topics_html}
</ol>

<h2>Frame ในไฟล์ของบท</h2>
<p>ไฟล์ <code>.spp</code> ของบทมีหลาย Frame เล่าเรื่องเดียวกัน — เปิดไฟล์ของบทได้เลย ไม่ต้องทำบทก่อนหน้าให้เสร็จ:</p>
<p>{frames}</p>
{extra}'''


BODY[("basic", "00a")] = f'''
<p class="lead" style="max-width:46em;">บทแรกของชุดสอนยังไม่ต้องสร้างอะไรเอง — เปิดโรงงานตัวอย่าง <strong>Factory 51</strong> ที่ติดมากับโปรแกรม
เพื่อฝึกใช้หน้าจอ ควบคุมมุมมอง 3D โต้ตอบกับวัตถุ และสั่งรันซิมูเลชัน ทั้งหมด 7 ขั้นตอน
แล้วต่อด้วยโมเดลตัวอย่างตัวที่สองในบท <a href="basic-00b.html">00B Small Parts Production</a></p>

<h2>Plant Simulation คืออะไร</h2>
<p>Plant Simulation จำลองระบบแบบ <strong>Discrete Event Simulation (DES)</strong> — คือการจำลอง
"เหตุการณ์" ที่เกิดขึ้นเป็นจุดๆ ตามเวลา (เช่น ชิ้นงานมาถึง, เครื่องเริ่มทำงาน, เครื่องทำงานเสร็จ)
แทนที่จะคำนวณทุกวินาทีต่อเนื่อง ทำให้จำลองกระบวนการผลิตหลายวัน/หลายเดือนได้ในเวลาไม่กี่วินาทีบนคอมพิวเตอร์</p>

<div class="note">
<strong>นิยาม — Plant Simulation Model คืออะไร:</strong> โมเดลจำลองคือ <em>การเลียนแบบระบบ</em>
ที่สร้างขึ้นจากความรู้หรือสมมติฐานเกี่ยวกับพฤติกรรมของส่วนต่างๆ ในระบบนั้น โดยมีจุดประสงค์เพื่อให้ได้ข้อมูลเชิงลึกเกี่ยวกับพฤติกรรมของ
<em>ทั้งระบบ</em> — ไม่ได้จำลองทุกรายละเอียดให้เหมือนจริง 100% แต่เลือกจำลองเฉพาะส่วนที่ส่งผลต่อคำถามที่อยากตอบ
</div>

{side_by_side(
    screenshot("assets/images/basic/00a-01.png", "ตัวอย่างโมเดล 3D ของสายการผลิตใน Plant Simulation"),
    step_list([
        "ผังพื้นโรงงาน (เส้นสีเทาจางด้านหลัง) — แบบ Layout จริงที่ใช้เป็นพื้นหลังอ้างอิงตำแหน่งวาง Object",
        "กลุ่มเครื่องจักรสีเขียว-ฟ้า — แต่ละกลุ่มแทนสถานีเครื่องจักร/ประมวลผลในสายการผลิตจริง",
        "เส้นทางสีส้ม — เส้นทางลำเลียงชิ้นงานที่เชื่อมแต่ละสถานีเข้าด้วยกัน",
        "พาเลทสีเขียวด้านล่าง — จุดพักสินค้าสำเร็จรูปก่อนส่งออกจากไลน์",
    ])
)}

<h3>Simulation กับ Digital Twin</h3>
<p><strong>Simulation</strong> คือการสร้างแบบจำลองของระบบหรือกระบวนการในโลกจริงขึ้นมา เพื่อศึกษาพฤติกรรม
ทดสอบสมมติฐาน หรือคาดการณ์ผลลัพธ์ภายใต้เงื่อนไขต่างๆ โดยไม่ต้องลงมือทำกับสถานการณ์จริง — เน้นทดสอบ
"สิ่งที่อาจจะเกิดขึ้น" (What-if scenarios)</p>
<p><strong>Digital Twin</strong> ต่อยอดอีกขั้น: เป็นแบบจำลองที่ <em>เชื่อมโยงกับข้อมูลจริงอย่างต่อเนื่อง</em>
ทำให้ติดตามสิ่งที่เป็นอยู่แบบเรียลไทม์ (Real-time monitoring) และพยากรณ์เหตุการณ์ล่วงหน้า (Prediction) ได้ —
โมเดลที่เริ่มสร้างในชุดสอนนี้คือจุดตั้งต้น พอต่อเข้ากับข้อมูลจริงจากหน้างานก็ต่อยอดเป็น Digital Twin ได้</p>

{side_by_side(
    screenshot("assets/images/basic/00a-02.jpg", "การผสาน Digital Twin เข้ากับเครื่องจักรจริงระหว่างขั้นตอนติดตั้ง/ตรวจสอบ"),
    step_list([
        "ลดต้นทุน — ทดสอบและแก้ปัญหาในโลกดิจิทัลก่อนลงทุนจริง",
        "ทำนายล่วงหน้า — รู้ว่าอะไรจะเสียก่อนที่มันจะเสียจริง",
        "ตัดสินใจได้ดีขึ้น — มีข้อมูลเรียลไทม์ประกอบการวิเคราะห์",
        "ออกแบบได้แม่นยำ — จำลองสถานการณ์ได้ไม่จำกัดจำนวนครั้ง",
    ])
)}

{screenshot("assets/images/basic/00a-03.jpg", "ตัวอย่าง Plant Simulation Model ของคลังสินค้าอัตโนมัติขนาดใหญ่", caption="โมเดลระดับนี้จำลองทั้งชั้นวางสินค้าอัตโนมัติ (AS/RS), สายพานลำเลียง และเส้นทางขนย้ายในคลังสินค้าจริง — ใช้หลัก DES เดียวกับโมเดลง่ายๆ ที่จะสร้างในชุดสอนนี้ เพียงแค่ขยายสเกลขึ้น")}

<table>
<tr><th>โจทย์</th><th>Plant Simulation ช่วยอะไร</th></tr>
<tr><td>ออกแบบสายการผลิตใหม่</td><td>ทดสอบผัง Layout ก่อนลงทุนจริง ลดความเสี่ยงสร้างแล้วใช้ไม่ได้</td></tr>
<tr><td>หาคอขวด (Bottleneck)</td><td>ดูว่าเครื่องไหนเป็นตัวถ่วง Throughput ของทั้งสาย</td></tr>
<tr><td>วางแผนกำลังการผลิต</td><td>ทดลองเพิ่ม/ลดจำนวนเครื่องจักรหรือคนงานแบบ what-if</td></tr>
<tr><td>บริหารสินค้าคงคลัง/โลจิสติกส์</td><td>จำลองคลังสินค้า, AGV, ระบบขนส่งภายในโรงงาน</td></tr>
</table>

<h2>ภาพรวม 7 ขั้นตอนของบทนี้</h2>
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

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 และโมเดล <code>Factory51.spp</code> (อยู่ใน <code>Examples\\Demo</code> ของโฟลเดอร์ติดตั้ง)
— ใช้ Student License ได้ โดยเปิดแบบ Viewer &nbsp;·&nbsp; ผลที่วัดได้ใน 2606: มีรถบรรทุกเข้ามา <strong>5 คัน</strong> ภายในเวลาจำลอง 48:40 นาที
</div>

<h2>ขั้นที่ 1: เปิด Start Page</h2>
{side_by_side(
    screenshot("assets/images/basic/00a-04.jpg", "แท็บ Window และหน้า Start Page ของ Plant Simulation 2606"),
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
{screenshot("assets/images/basic/00a-05.jpg", "หน้าต่าง Example Models และโมเดล Factory 51 ที่เปิดแล้ว")}
{step_list([
    "คลิก <code>Factory 51</code> ในหน้าต่าง Example Models",
    "โมเดลจะอยู่ใน Class Library → <code>Models → Factory51</code>",
    "แถบ <em>The model contains outdated libraries</em> กด <code>X</code> ปิดได้ บทนี้ไม่ต้องอัปเดต",
    "โมเดลเปิดในหน้าต่าง 3D (แท็บล่างชื่อ <code>3D.Models.Factory51</code>)",
    "2606 มีตัวอย่างเพิ่ม เช่น <strong>Python GA Demo</strong> และ <strong>Standard Object Examples</strong>",
])}
<div class="note">
<strong>Student License:</strong> โมเดล Factory 51 มีวัตถุเกิน 80 ตัว โปรแกรมจะถาม — กด <code>Yes</code> เพื่อเปิดแบบ <strong>Viewer</strong>
(ดูและรันได้ แต่บันทึกการแก้ไขไม่ได้) และ License แบบนี้ควบคุมโมเดลจากภายนอกผ่าน COM ไม่ได้
(ขึ้น <code>"Remote access is not allowed with this license"</code>)
</div>

<h2>ขั้นที่ 3: รู้จัก Factory 51 — ระบบทั้งโรงงานใน 3D</h2>
{screenshot("assets/images/basic/00a-06.jpg", "ภาพรวมโซนต่างๆ ในโมเดล Factory 51", caption="Factory 51 — Overview: รับของ → ผลิต → คลัง → ส่งของ")}
{side_by_side(
    screenshot("assets/images/basic/00a-07.jpg", "ตำแหน่งของแต่ละโซนใน Factory 51"),
    step_list([
        "<strong>Inbound</strong> — รถบรรทุก โฟล์คลิฟต์ หุ่นยนต์ เครน รับวัตถุดิบเข้าโรงงาน",
        "<strong>P1 / P2</strong> — โรงผลิต 2 หลัง: ขัด (Polishing) กัด (Milling) พ่นสี อบ ล้าง QC แพ็ก",
        "<strong>AGV</strong> — ขนส่งด้วย AGV พร้อมจุดชาร์จ และ Robot Auto Packing",
        "<strong>คลัง HBW</strong> — คลังสินค้าอัตโนมัติ (ASRS, WMS)",
        "<strong>Outbound</strong> — สายพานและรถบรรทุกส่งของออก",
    ])
)}

<h2>ขั้นที่ 4: ควบคุมมุมมอง 3D ด้วยเมาส์</h2>
{side_by_side(
    screenshot("assets/images/basic/00a-08.jpg", "มุมมองเริ่มต้น เทียบกับหลังซูม เลื่อน และหมุน"),
    step_list([
        "<strong>หมุนล้อเมาส์</strong> = ซูมเข้า-ออก (กด <code>Shift</code> ค้าง = เร็ว ×10, <code>Ctrl</code> ค้าง = ช้า ×0.1)",
        "<strong>คลิกขวาค้างแล้วลาก</strong> = เลื่อนฉาก (Pan) — หรือกดล้อค้างแล้วลาก",
        "<code>Ctrl</code> + <strong>คลิกขวาค้างแล้วลาก</strong> = หมุนฉาก — หรือกดซ้าย+ขวาค้าง",
        "กด <code>V</code> = View All เห็นทั้งฉาก",
    ])
)}
<div class="note">
<strong>ระวัง:</strong> ลากหมุนนิดเดียวพอ ถ้าหมุนจนมุมเพี้ยน กด <code>V</code> จะไม่คืนมุมกล้อง — ให้ใช้แท็บ <code>View</code>
(<code>From Top</code> / <code>Front</code>) หรือเปิดโมเดลใหม่
</div>

<h3>เดินในฉากด้วยคีย์บอร์ด</h3>
{screenshot("assets/images/basic/00a-09.jpg", "การควบคุมฉาก 3D ด้วยเมาส์และคีย์บอร์ด", caption="ภาพนี้มาจากเวอร์ชันก่อน — ใน 2606 กดล้อค้าง = เลื่อน และ Ctrl + คลิกขวาค้าง = หมุน ตามขั้นที่ 4")}
<table>
<tr><th>ปุ่ม</th><th>ผลลัพธ์</th></tr>
<tr><td><code>W</code> / <code>S</code></td><td>เดินเข้าใกล้ / ถอยออกจากวัตถุในหน้าต่าง 3D</td></tr>
<tr><td><code>Q</code> / <code>E</code></td><td>เดินไปทางซ้าย / ทางขวา</td></tr>
<tr><td><code>A</code> / <code>D</code></td><td>หันซ้าย / หันขวา</td></tr>
<tr><td><code>Z</code> / <code>Shift + Z</code></td><td>ลดระดับตัวเองลง / ยกตัวเองขึ้น</td></tr>
</table>

<h2>ขั้นที่ 5: คลิก ดับเบิลคลิก และคลิกขวาที่วัตถุ</h2>
{screenshot("assets/images/basic/00a-10.jpg", "คลิกเลือกสายพาน Line10, หน้าต่างของวัตถุ และเมนู Quick tools")}
{step_list([
    "<strong>คลิก</strong> = เลือกวัตถุ (ขึ้นสีเหลือง) — ในภาพคือสายพาน <code>Line10</code>",
    "<strong>ดับเบิลคลิก</strong> = เปิดหน้าต่างของวัตถุ (ตั้งค่า เวลา การเสีย ฯลฯ)",
    "<strong>คลิกขวา</strong> = Quick tools: แถบปุ่ม Start / Stop / Reset ด้านบน",
    "เมนูลัด เช่น <code>Open</code> (Enter), <code>Show Statistics Report</code> (F6), <code>Show Attributes</code> (F8)",
])}

<h2>ขั้นที่ 6: เปิด Frame ด้านใน และกลับออกมา</h2>
{screenshot("assets/images/basic/00a-11.jpg", "เปิด Frame P1 และเมนู Open Location")}
{step_list([
    "<strong>ดับเบิลคลิก</strong> วัตถุในโรงผลิต (เช่นบูธขัดผิวใน P1) → เปิด Frame <code>P1</code> แยกออกมา",
    "แท็บล่างเปลี่ยนเป็น <code>3D.Models.Factory51.P1</code>",
    "กลับ Frame หลัก: <code>Shift + Enter</code> หรือคลิกขวาที่ว่าง → <code>Open Location</code>",
    "<code>Backspace</code> = Previous Scene (กลับมุมมองก่อนหน้า)",
])}

<h2>ขั้นที่ 7: EventController — เริ่ม หยุด รีเซ็ต และความเร็ว</h2>
<p>Plant Simulation เป็นโปรแกรมจำลองแบบ <strong>discrete, event-controlled</strong> — โปรแกรมตรวจสอบเฉพาะ
"จุดเวลาที่มีเหตุการณ์เกิดขึ้น" ในโมเดลเท่านั้น ไม่ได้คำนวณทุกช่วงเวลาต่อเนื่อง (Time-oriented)
และควบคุมการรันทั้งหมดผ่านวัตถุ <strong>EventController</strong> ตัวเดียว</p>
{screenshot("assets/images/basic/00a-12.jpg", "ปุ่ม Start/Stop Simulation, Reset Simulation และหน้าต่าง EventController ใน Factory 51")}
{screenshot("assets/images/basic/00a-13.jpg", "ปุ่มในฉากและหน้าต่าง EventController")}
{step_list([
    "คลิก <code>Start/Stop Simulation</code> (ปุ่มในฉาก) เพื่อเริ่ม / หยุด",
    "<code>Reset Simulation</code> = เวลากลับไป 0",
    "ดับเบิลคลิกนาฬิกา <strong>EventController</strong>",
    "<code>Time</code> = เวลาจำลองตอนนี้ (ในภาพคือ 48:40)",
    "แถบ <code>Slower</code> / <code>Faster</code> ปรับความเร็ว",
    "<code>Real-time × 3</code> = เร็วกว่าเวลาจริง 3 เท่า",
])}

<h2>แบบฝึก: หา Beer room ใน Factory 51</h2>
<p>ฝึกซูม เลื่อน และหมุนมุมมองให้คล่อง — ในโรงงานมีห้องเล็กๆ ซ่อนอยู่ ลองหาเองก่อนแล้วค่อยดูเฉลย</p>
<details>
<summary>ดูเฉลย</summary>
{screenshot("assets/images/basic/00a-14.jpg", "ตำแหน่ง Beer room ในโรงผลิต P1")}
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

<h2>ภาพรวมชุดสอน 8 บท</h2>
<p>บท 02–07 ใช้<strong>ไลน์ผลิต 5 สถานี</strong> (Source → Station1…5 → Drain, 0:10 นาทีต่อชิ้น) ไลน์เดียวต่อเนื่อง
แต่ละบทเพิ่มปัญหาจริงทีละเรื่อง จนถึงการตัดสินใจลงทุน — 1 บท = 1 ไฟล์ <code>.spp</code> ที่มีหลาย Frame
(<code>Model</code> ก่อนแก้ → <code>Model2</code> แก้ 1 จุด → <code>Model3</code> …)</p>
<table>
<tr><th>บท</th><th>หัวข้อ</th><th>หลังจบบททำได้</th><th>เขียนโค้ด</th></tr>
<tr><td>00A</td><td><a href="basic-00a.html">โรงงานตัวอย่าง Factory 51</a></td><td>เปิด Start Page เปิดตัวอย่าง หมุน/ซูม 3D เปิด Frame ด้านใน สั่ง Run / Reset</td><td>ไม่</td></tr>
<tr><td>00B</td><td><a href="basic-00b.html">โมเดลตัวอย่าง Small Parts</a></td><td>รันเทียบไลน์ ใช้ Bottleneck Analyzer, Experiment Manager และ Energy Analyzer บนโมเดลที่มีอยู่แล้ว</td><td>ไม่</td></tr>
<tr><td>01</td><td><a href="basic-01.html">โมเดลแรก</a></td><td>Source → Station → Drain, ตั้งเวลา, EventController, Display</td><td>ไม่</td></tr>
<tr><td>02</td><td><a href="basic-02.html">คอขวด + ParallelStation</a></td><td>ไลน์ 5 สถานี, Display / Chart, แก้คอขวดด้วยเครื่องขนาน หรือ ParallelStation, กับดัก When Full</td><td>ไม่</td></tr>
<tr><td>03</td><td><a href="basic-03.html">เวลาสุ่ม + Buffer + เครื่องเสีย + OEE</a></td><td>Uniform, Buffer, Failure (Availability, MTTR), แท็บ Statistics, คำนวณ OEE, รันสั้น vs ยาว</td><td>ไม่</td></tr>
<tr><td>04</td><td><a href="basic-04.html">คน + กะทำงาน</a></td><td>Workplace, WorkerPool, Broker, คนคุมเครื่อง, ShiftCalendar, Worker chart</td><td>ไม่</td></tr>
<tr><td>05</td><td><a href="basic-05.html">หลายรุ่น + งานเสีย + Method แรก</a></td><td>Source ตามตาราง, เวลาต่างกันตามรุ่น, FG/NG, Variable, Method สั้น, Sankey</td><td><strong>ใช่</strong> (5–10 บรรทัด)</td></tr>
<tr><td>06</td><td><a href="basic-06.html">ผัง 3D + ขนส่งด้วย AGV</a></td><td>วางไลน์บนผังโรงงาน, 3D view, AGV ขนจากคลังเข้าไลน์, Conveyor</td><td>อาจมี</td></tr>
<tr><td>07</td><td><a href="basic-07.html">วิเคราะห์ + หาค่าที่ดีที่สุด</a></td><td>Bottleneck Analyzer, ExperimentManager, อ่านผล, สรุปเพื่อตัดสินใจ</td><td>ไม่</td></tr>
</table>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ถ้าอยากรู้ว่าวัตถุตัวหนึ่ง (เช่นสายพาน Line10) ตั้งค่าอะไรได้บ้าง และอยากดูสถิติของมันเร็วๆ ควรทำอย่างไร?
</div>
<div class="tip"><strong>เฉลย:</strong> ดับเบิลคลิกเพื่อเปิดหน้าต่างของวัตถุ (เห็นทุกแท็บการตั้งค่า) และคลิกขวา → <code>Show Statistics Report</code>
หรือกด <code>F6</code> เพื่อดูสถิติ</div>
'''

BODY[("basic", "00b")] = f'''
<p class="lead" style="max-width:46em;">โมเดลตัวอย่างตัวที่สองต่อจาก <a href="basic-00a.html">00A Factory 51</a> — ยังไม่ต้องสร้างอะไรเอง
แค่เปิดไลน์ประกอบชิ้นงานเล็กที่ Siemens ทำไว้แล้ว และลองใช้เครื่องมือวิเคราะห์ทีละขั้น 10 ขั้นตอน: รันไลน์เดิม ดูกราฟ
หาคอขวด เพิ่ม Buffer หาขนาด Buffer ที่พอด้วย Experiment Manager และดูการใช้พลังงาน
ให้เห็นภาพว่าเรียนจบชุดสอนแล้วจะวิเคราะห์ไลน์จริงได้แบบไหน (บท 02–07 จะสอนสร้างและวิเคราะห์ไลน์ของตัวเองทีละเรื่อง)</p>

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
    screenshot("assets/images/basic/00b-01.jpg", "โมเดล Small Parts Production และ Class Library"),
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
{screenshot("assets/images/basic/00b-02.jpg", "Assembly1 ระหว่างรันและหลังรันจบ 1 วัน")}
{step_list([
    "กด <code>Start</code> ในโมเดล (รันจบ 1 วันทันที) หรือ ▶ ที่ <code>Home → Event Controller</code> ถ้าอยากเห็นชิ้นงานวิ่ง",
    "ระหว่างรัน ชิ้นงานต่อคิวยาวหน้า MS3 / MS4",
    "จบ 1 วัน: Throughput <strong>1,400 ชิ้น</strong>",
    "พลังงานทั้งไลน์ <strong>14.3 kWh</strong> (Energy saving measures = ปิด, จุดแดง)",
])}

<h2>ขั้นที่ 3: Station Utilization — สัดส่วนเวลาของทุกสถานี</h2>
{screenshot("assets/images/basic/00b-03.jpg", "เมนู Show ของ Station Utilization และกราฟสัดส่วนเวลา")}
{step_list([
    "คลิกขวาที่ <code>Station Utilization</code>",
    "เลือก <code>Show</code>",
    "<strong>MS4</strong> Waiting ต่ำสุด 1.4% และ Failed สูงสุด 3.3% → งานไม่เคยขาด = <strong>คอขวด</strong>",
    "MS1–MS5 เป็นสถานีคน ทำงาน 2 กะ จึงมี Unplanned 33% (สีฟ้า)",
])}

<h2>ขั้นที่ 4: Worker Utilization และ ShiftCalendar</h2>
{screenshot("assets/images/basic/00b-04.jpg", "กราฟ Worker Utilization และหน้าต่าง ShiftCalendar")}
{step_list([
    "คลิกขวา <code>Worker-Utilization</code> → <code>View Chart</code>",
    "Worker / Worker_Round: Working ประมาณ 25–29%",
    "Adjuster (ช่างปรับเครื่อง) ทำงานน้อย รอเป็นส่วนใหญ่",
    "ดับเบิลคลิก <code>ShiftCalendar</code>: Shift-1 06:00–14:00, Shift-2 14:00–22:00",
    "คอลัมน์ <code>Pauses</code> = เวลาพักในแต่ละกะ",
])}

<h2>ขั้นที่ 5: Bottleneck Analyzer — Show Analysis</h2>
{screenshot("assets/images/basic/00b-05.jpg", "เมนู Show Analysis และแท่งสถานะบนสถานี")}
{step_list([
    "คลิกขวาที่ <code>Bottlenecks</code>",
    "เลือก <code>Show Analysis</code>",
    "แท่งสีขึ้นบนทุกสถานี: <strong>เขียว</strong> Working, <strong>เทา</strong> Waiting, <strong>เหลือง</strong> Blocked, <strong>แดง</strong> Failed",
    "MS4 แท่งเขียวสูง แทบไม่มีสีเทา ต่างจาก AS3 / AS4 ที่สีเทาสูง",
])}

<h2>ขั้นที่ 6: Ranking — เรียงตารางหาคอขวด</h2>
{screenshot("assets/images/basic/00b-06.jpg", "หน้าต่างเลือกเกณฑ์ Ranking และตาราง ResourceStats")}
{step_list([
    "คลิกขวา <code>Bottlenecks</code> → <code>Ranking</code>",
    "เลือกเกณฑ์ <code>Working</code>",
    "กด <code>OK</code> ได้ตาราง <code>ResourceStats</code>",
    "คลิกขวาหัวคอลัมน์ <code>waiting</code> → <code>Sort Ascending</code>",
    "MS4, MS2, MS1: waiting ต่ำ + blocked ต่ำ = <strong>คอขวด</strong>",
    "ParallelProc / AS6: waiting ต่ำแต่ blocked สูง = ถูกปลายทางบล็อก <em>ไม่ใช่</em>คอขวด",
])}

<h2>ขั้นที่ 7: Assembly2 — เพิ่ม Buffer หน้า MS4 แล้วเทียบผล</h2>
{screenshot("assets/images/basic/00b-07.jpg", "Assembly2 ที่มี Buffer หน้า MS4 และกราฟ Station Utilization")}
{step_list([
    "ดับเบิลคลิก <code>Models → Assembly2</code> ใน Class Library แล้วกด <code>Start</code>",
    "Throughput ~1,460 ชิ้น (วัดได้ 1,462–1,466 จาก 4 รอบ; Assembly1 = 1,400)",
    "Buffer B (<code>Buffer1</code>) อยู่ระหว่าง AS3 กับ MS4",
    "Energy saving measures เปิด (จุดเขียว)",
    "Station Utilization: MS4 ไม่มีสีเหลือง (Blocked) แล้ว (หัวกราฟยังเขียน Assembly 1 ตามตัวอย่างของ Siemens)",
])}

<h2>ขั้นที่ 8: BufferOptimization — กำหนด Output, Input และ Experiments</h2>
{screenshot("assets/images/basic/00b-08.jpg", "หน้าต่าง Experiment Manager และ Define Output Values")}
{step_list([
    "ดับเบิลคลิก <code>BufferOptimization</code> (Experiment Manager) → <code>Define Output Values</code>",
    "<code>root.Drain.statDeleted</code> = Throughput, <code>High Values are Better</code> = true → OK",
    "<code>Define Input Values</code> (ภาพถัดไป)",
    "<code>Define Experiments</code> (ภาพถัดไป)",
    "<code>Observations per experiment</code> = 5 (รันซ้ำ 5 รอบต่อการทดลองแล้วเฉลี่ย)",
])}
{screenshot("assets/images/basic/00b-09.jpg", "Define Input Values และตาราง Experiments")}
{step_list([
    "<code>root.Buffer1.capacity</code> = ความจุของ Buffer B → OK",
    "<code>Active</code> = true ทุกแถว = รันทุกการทดลอง",
    "Capacity of buffer 2, 4, 6 … 16 รวม 8 การทดลอง → OK",
])}
<div class="tip"><strong>ทำซ้ำ:</strong> อยากทดลองค่าอื่น แก้ตัวเลขในคอลัมน์ Capacity of buffer หรือเพิ่มแถวได้เลย</div>

<h2>ขั้นที่ 9: รันการทดลอง และอ่าน Report</h2>
{screenshot("assets/images/basic/00b-10.jpg", "ปุ่ม Start ของ Experiment Manager และ Report ผลการทดลอง")}
{step_list([
    "กด <code>Start</code> รอข้อความ <em>The experiment run is finished</em> (ประมาณ 10 วินาที) → OK",
    "ครบ 8/8 การทดลอง 5/5 รอบ",
    "Buffer ตั้งแต่ <strong>6</strong> ขึ้นไป = 1,478.8 ชิ้น (เฉลี่ย) ค่าเท่ากันหมด → <strong>6 ก็พอ</strong>",
    "Report เปิดเองหลังรันจบ หรือกด <code>Evaluation → Report</code>",
    "สรุปค่าที่ดีที่สุด: Throughput สูงสุด 1,478.8",
    "บันทึก / พิมพ์ Report จากปุ่มมุมซ้ายบน",
])}

<h2>ขั้นที่ 10: Energy — ตั้งค่าพลังงานของสายพาน และอ่าน Energy Analyzer</h2>
{screenshot("assets/images/basic/00b-11.jpg", "หน้าต่างสายพาน F1 และแท็บ Energy")}
{step_list([
    "ใน Assembly2 ดับเบิลคลิกสายพาน <code>F1</code>",
    "<code>Automatic Stop</code> = สายพานหยุดเองเมื่อว่าง (ตัวที่ทำให้ประหยัดไฟ)",
    "คลิกแท็บ <code>Energy</code>",
    "<code>Active</code> = นับพลังงานของวัตถุนี้",
    "<code>Working</code> 1 kW ขณะลำเลียง",
    "<code>Operational</code> 0.3 kW ขณะเปิดรอ",
])}
{screenshot("assets/images/basic/00b-12.jpg", "เมนู Energy Analyzer, กราฟพลังงานแยกตามวัตถุ และ Power Input ตามเวลา")}
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
คอขวดจริงต้อง waiting ต่ำ <em>และ</em> blocked ต่ำ (ทำงานตลอดเวลา) แบบ MS4 — ใช้หลักเดียวกันนี้ในบท
<a href="basic-07.html">Basic 07 วิเคราะห์ + หาค่าที่ดีที่สุด</a></div>
'''

BODY[("basic", "01")] = f'''
<p class="lead" style="max-width:46em;">สร้างโมเดลแรกของตัวเอง <code>Source → Station → Drain</code> ทีละขั้น 6 ขั้นตอน ตั้งแต่เปิดไฟล์
รู้จักหน้าจอ วาง object และต่อเส้น ตั้งค่า ใส่ตัวเลขด้วย Display จนถึงกด Run แล้วอ่านผล</p>

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
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 และไฟล์ <code>Basic_01_Create_Simple_Model.spp</code> (Frame อยู่ที่ Class Library › Models › Model)
&nbsp;·&nbsp; ผลจำลอง 1 ชั่วโมง: <strong>359 ชิ้น</strong> (เวลาผลิต 10 วินาทีต่อชิ้น)
</div>
<div class="note">
<strong>ข้อควรจำ:</strong> Plant Simulation 2606 ทำงานแบบ 3D อย่างเดียว ถ้าอยากมองแบบแปลนให้ใช้ <strong>Planning View</strong>
(ภาพทุกภาพในบทนี้ใช้ Planning View)
</div>

<h3>ทุกโมเดลทำ 5 ขั้นเหมือนกัน</h3>
<table>
<tr><th></th><th>งาน</th><th>ทำอย่างไร</th><th>ดูที่</th></tr>
<tr><td>1</td><td>วาง object</td><td>เลือกจาก Toolbox แล้วคลิกลงใน Frame</td><td>ขั้นที่ 3</td></tr>
<tr><td>2</td><td>ต่อเส้น</td><td>Connector บอกทางเดินของชิ้นงาน</td><td>ขั้นที่ 3</td></tr>
<tr><td>3</td><td>ตั้งค่า</td><td>ดับเบิลคลิก object ใส่เวลา</td><td>ขั้นที่ 4</td></tr>
<tr><td>4</td><td>ใส่ตัวเลข</td><td>Display แสดงค่าบน Frame</td><td>ขั้นที่ 5</td></tr>
<tr><td>5</td><td>Run + อ่านผล</td><td>EventController: Reset แล้ว Start</td><td>ขั้นที่ 6</td></tr>
</table>
<p>Basic 01 ในตัวเลข: <strong>1</strong> Frame (<code>.Models.Model</code>) · <strong>6</strong> object · <strong>2</strong> Connector ·
<strong>60</strong> นาทีจำลองต่อการรัน</p>

<h2>ขั้นที่ 1: หน้า Start Page เมื่อเปิดโปรแกรม</h2>
{side_by_side(
    screenshot("assets/images/basic/01-01.jpg", "หน้า Start Page ของ Plant Simulation 2606"),
    step_list([
        "<strong>Open Model File</strong> — เปิดไฟล์ <code>Basic_01_Create_Simple_Model.spp</code>",
        "<strong>Recent Models</strong> — ไฟล์ที่เปิดล่าสุด",
        "<strong>Create New Model</strong> — สร้างโมเดลใหม่ว่างๆ เมื่อจะสร้างเอง",
        '<strong>Example Models</strong> — ตัวอย่างโมเดลจาก Siemens (ดูบท <a href="basic-00a.html">00A</a> และ <a href="basic-00b.html">00B</a>)',
    ])
)}
<div class="tip"><strong>ทางลัด:</strong> <strong>Load Last Model</strong> (ช่องบนซ้าย) เปิดไฟล์ที่ใช้ครั้งก่อนได้ในคลิกเดียว ชื่อไฟล์แสดงอยู่บนช่อง</div>

<h2>ขั้นที่ 2: ส่วนต่างๆ ของหน้าจอ</h2>
{side_by_side(
    screenshot("assets/images/basic/01-02.jpg", "หน้าจอหลักของ Plant Simulation 2606 เมื่อเปิด Frame Model"),
    step_list([
        "<strong>Ribbon</strong> — ปุ่มคำสั่ง กลุ่ม Event Controller ใช้ Run / Reset",
        "<strong>Class Library</strong> — คลังทุก object และโมเดล เปิด <code>Models › Model</code>",
        "<strong>Toolbox</strong> — ไอคอน object พร้อมวาง",
        "<strong>Frame</strong> — พื้นที่วางโมเดล (ภาพนี้เป็น Planning View)",
        "<strong>แท็บ Frame</strong> — Frame ที่เปิดอยู่ สลับไปมาได้",
    ])
)}
<div class="note"><strong>วิธีเปิด Frame:</strong> ใน Class Library ดับเบิลคลิก <code>Models › Model</code></div>

<h3>มองโมเดลแบบแปลนด้วย Planning View</h3>
{screenshot("assets/images/basic/01-03.jpg", "Ribbon แท็บ 3D › View: Planning View, Names, Connections และ View All")}
{step_list([
    "<strong>View</strong> — แท็บใต้หัวข้อ 3D (สีน้ำเงินเข้ม)",
    "<strong>Planning View</strong> — มองจากด้านบน เหมือนแปลนโรงงาน",
    "<strong>Names</strong> — แสดงชื่อ object",
    "<strong>Connections</strong> — แสดงเส้นเชื่อมและทิศทาง",
    "<strong>View All</strong> — ซูมให้เห็นทั้งโมเดล",
])}
<div class="note"><strong>ไฟล์นี้ปิดชื่อ object ไว้:</strong> ถ้ากด Names แล้วยังไม่เห็นชื่อ ให้คลิกขวาที่ object ›
<code>Edit 3D Properties</code> › แท็บ <code>Captions</code> › ติ๊ก <code>Name/Label Activated</code></div>

<h2>ขั้นที่ 3: วาง object และต่อเส้น</h2>
<p>object ที่ใช้อยู่ใน Toolbox แท็บ <strong>Material Flow</strong></p>
{screenshot("assets/images/basic/01-04.jpg", "Toolbox แท็บ Material Flow")}
{step_list([
    "<strong>Connector</strong> — ต่อเส้นระหว่าง object",
    "<strong>EventController</strong> — นาฬิกา (1 ตัวต่อ Frame)",
    "<strong>Source</strong> — ปล่อยชิ้นงาน",
    "<strong>Drain</strong> — รับชิ้นงานออก",
    "<strong>Station</strong> — เครื่องจักร ทำทีละ 1 ชิ้น",
])}
<div class="tip"><strong>วิธีวาง / ต่อเส้น:</strong> คลิกไอคอนใน Toolbox แล้วคลิกในพื้นที่ Frame ·
ต่อเส้น: คลิก Connector แล้วคลิก object ต้นทาง → ปลายทาง</div>

<h3>โมเดลแรก Source → Station → Drain</h3>
{side_by_side(
    screenshot("assets/images/basic/01-05.jpg", "โมเดลแรกใน Frame .Models.Model"),
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

<h2>ขั้นที่ 4: ตั้งค่า</h2>
<h3>ตั้งค่า Source</h3>
{side_by_side(
    screenshot("assets/images/basic/01-06.jpg", "หน้าต่างตั้งค่า Source"),
    step_list([
        "<strong>Blocking</strong> — ติ๊กไว้ = ถ้าทางข้างหน้าเต็ม Source จะรอ",
        "<strong>Time of Creation</strong> — <code>Interval Adjustable</code> = ปล่อยตามช่วงเวลา",
        "<strong>Interval = 0</strong> — ปล่อยชิ้นใหม่ทันทีที่ Station ว่าง",
        "<strong>MU</strong> — ชนิดชิ้นงานที่ปล่อย (<code>*.MUs.Part</code>)",
    ])
)}
<div class="note"><strong>ข้อควรจำ:</strong> ดับเบิลคลิก object ใดก็ได้เพื่อเปิดหน้าต่างตั้งค่า แก้แล้วกด <code>Apply</code> หรือ <code>OK</code></div>

<h3>ตั้งเวลาทำงานของ Station</h3>
{side_by_side(
    screenshot("assets/images/basic/01-07.jpg", "หน้าต่างตั้งค่า Station แท็บ Times"),
    step_list([
        "<strong>Processing Time = 0:10</strong> — ทำ 1 ชิ้นใช้ 10 วินาที",
        "<strong>Const</strong> — เวลาเท่ากันทุกชิ้น",
        "<strong>Set-up Time</strong> — เวลาเปลี่ยนรุ่น (ยังไม่ใช้ = 0)",
        "<strong>OK</strong> — บันทึกแล้วปิดหน้าต่าง",
    ])
)}
<div class="tip"><strong>รูปแบบเวลา:</strong> ชม:นาที:วินาที เช่น <code>0:10</code> = 10 วินาที, <code>1:00</code> = 1 นาที, <code>1:00:00</code> = 1 ชั่วโมง</div>

<h3>ตั้งเวลาจำลอง แล้วกด Run</h3>
{side_by_side(
    screenshot("assets/images/basic/01-08.jpg", "หน้าต่าง EventController แท็บ Settings และ Controls"),
    step_list([
        "<strong>Settings</strong> — แท็บตั้งค่าเวลา",
        "<strong>End Time = 1:00:00</strong> — จำลอง 1 ชั่วโมงแล้วหยุดเอง",
        "<strong>Reset</strong> (ปุ่มแดง) — ล้างผลเก่า กดก่อนรันใหม่ทุกครั้ง",
        "<strong>Start</strong> (ปุ่มเขียว) — เริ่มจำลอง ปุ่มเดียวกันมีใน Ribbon › Home",
        "<strong>Slower – Faster</strong> — ปรับความเร็วของภาพเคลื่อนไหว",
    ])
)}
<div class="note"><strong>ระวัง:</strong> ถ้าไม่กด Reset ก่อน Start การจำลองจะเดินต่อจากเวลาเดิม</div>

<h2>ขั้นที่ 5: ใส่ตัวเลขด้วย Display</h2>
<h3>วาง Display บน Frame</h3>
{screenshot("assets/images/basic/01-09.jpg", "Toolbox แท็บ User Interface และไอคอน Display")}
{side_by_side(
    screenshot("assets/images/basic/01-10.jpg", "Display ที่วางไว้ใต้ Drain"),
    step_list([
        "Toolbox คลิกแท็บ <strong>User Interface</strong>",
        "คลิกไอคอน <strong>Display</strong> (รูปตัวเลข 9.86) แล้วคลิกวางใน Frame",
        "ในไฟล์นี้วางไว้ใต้ <strong>Drain</strong> ก่อนรันแสดงเลข 0",
    ])
)}
<div class="tip"><strong>ไอคอนข้างเคียง:</strong> Comment (รูปกระดาษเหลือง) ใช้เขียนข้อความบน Frame · Chart (รูปกราฟแท่ง) ใช้ทำกราฟ</div>

<h3>บอก Display ว่าจะแสดงค่าอะไร</h3>
{side_by_side(
    screenshot("assets/images/basic/01-11.jpg", "หน้าต่าง Display แท็บ Data"),
    step_list([
        "<strong>Path = <code>Drain.statNumIn</code></strong> — จำนวนชิ้นที่เข้า Drain (ชิ้นงานที่เสร็จ)",
        "<strong>Mode = Watch</strong> — เฝ้าดูค่า อัปเดตเองระหว่างรัน",
        "<strong>Value</strong> — ค่าตอนนี้ (ก่อนรัน = 0)",
        "<strong>Active</strong> — ติ๊กไว้ = Display ทำงาน",
    ])
)}
<div class="tip"><strong>ลองเอง:</strong> เปลี่ยน Path เป็น <code>Source.statNumOut</code> จะเห็นจำนวนชิ้นที่ Source ปล่อยออกมา</div>

<h3>ปรับหน้าตาตัวเลข</h3>
{side_by_side(
    screenshot("assets/images/basic/01-12.jpg", "หน้าต่าง Display แท็บ Display"),
    step_list([
        "<strong>Type = Text</strong> — แสดงเป็นตัวเลข",
        "<strong>Color</strong> — สีของตัวเลข",
        "<strong>Font Size = Small</strong> — ขนาดตัวเลข",
        "<strong>Decimal Places</strong> — จำนวนทศนิยม (ไฟล์นี้ = -1)",
    ])
)}
<div class="note"><strong>อีกแบบ:</strong> <code>Type › Bar</code> แสดงเป็นแท่งแทนตัวเลข</div>

<h2>ขั้นที่ 6: กด Run แล้วอ่านผล</h2>
{screenshot("assets/images/basic/01-13.jpg", "Display ก่อนรันและหลังรัน 1 ชั่วโมง และเวลาจำลองที่มุมขวาล่าง")}
{step_list([
    "<strong>ก่อนรัน</strong> — Display = 0",
    "<strong>หลังรัน Display = 359</strong> — ชิ้นงานที่เสร็จใน 1 ชั่วโมง",
    "<strong>1:00:00.0000</strong> — เวลาจำลองที่มุมขวาล่างของหน้าต่าง ครบแล้วหยุดเอง",
])}
<div class="note"><strong>ทำไมไม่ใช่ 360:</strong> Source ปล่อย 360 ชิ้น แต่ชิ้นสุดท้ายยังอยู่ใน Station ตอนหมดเวลา</div>

<h3>ลองเปลี่ยนค่า แล้วดูตัวเลขใน Display</h3>
<table>
<tr><th>ลองเปลี่ยน</th><th>แก้ที่</th><th>Display หลังรัน</th><th>ทำไม</th></tr>
<tr><td>ค่าเดิมในไฟล์</td><td>–</td><td><strong>359</strong></td><td>3600 ÷ 10 = 360 ลบ 1 ชิ้นที่ค้าง</td></tr>
<tr><td>Processing Time = 0:20</td><td>Station</td><td><strong>179</strong></td><td>ช้าลง 2 เท่า ได้ครึ่งเดียว</td></tr>
<tr><td>Processing Time = 0:05</td><td>Station</td><td><strong>719</strong></td><td>เร็วขึ้น 2 เท่า ได้เท่าตัว</td></tr>
<tr><td>Interval = 0:12</td><td>Source</td><td><strong>300</strong></td><td>งานเข้าช้ากว่าที่เครื่องทำได้ · Station ทำงาน 83%</td></tr>
<tr><td>End Time = 8:00:00</td><td>EventController</td><td><strong>2879</strong></td><td>8 ชม. × 360 ลบ 1</td></tr>
</table>
<p>วัดจริงใน Plant Simulation 2606 ด้วยไฟล์ของบท แก้ทีละค่าจากค่าเดิม — กด Reset ก่อน Start ทุกครั้ง</p>

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
<tr><td>Display ยังเป็น 0 หลังรัน</td><td>ตรวจ Path = <code>Drain.statNumIn</code>, ติ๊ก Active และต่อ Connector ถึง Drain</td></tr>
<tr><td>กด Start แล้วผลไม่เริ่มจากศูนย์</td><td>กด Reset (ปุ่มแดง) ก่อน Start ทุกครั้ง</td></tr>
<tr><td>รันไปเรื่อยๆ ไม่หยุด</td><td>EventController › Settings › ใส่ End Time เช่น <code>1:00:00</code></td></tr>
<tr><td>เปิด Names แล้วตัวเลขทับชื่อ Drain</td><td>ลาก Display ลงไปข้างล่างอีกเล็กน้อย</td></tr>
</table>

<div class="tip"><strong>บันทึกงาน:</strong> <code>Ctrl+S</code> บันทึกทับ, <code>File › Save As</code> บันทึกเป็นไฟล์ใหม่ (แนะนำก่อนทดลองแก้ค่าหลายอย่าง) —
ไฟล์ที่บันทึกจากเวอร์ชันใหม่กว่าจะเปิดในโปรแกรมเวอร์ชันเก่ากว่าไม่ได้</div>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ถ้าตั้ง Source Interval = 0:05 (ปล่อยงานทุก 5 วินาที) แต่ Station ยังใช้ 0:10 ต่อชิ้น Display หลังรัน 1 ชั่วโมงจะได้ประมาณเท่าไร?
</div>
<div class="tip"><strong>เฉลย:</strong> ยังได้ประมาณ 359 ชิ้นเท่าเดิม — Station ทำได้แค่ 1 ชิ้นต่อ 10 วินาที งานที่ปล่อยเร็วกว่านั้นต้องรอ (Source ถูก Blocking)
ตัวที่กำหนดผลผลิตคือเครื่องที่ช้าที่สุด หรือ<strong>คอขวด</strong> ซึ่งเป็นหัวข้อของบท <a href="basic-02.html">02</a></div>
'''

BODY[("basic", "02")] = f'''
<p class="lead" style="max-width:46em;">ต่อจากบท 01 — ใช้ไลน์ผลิต 5 สถานีที่จะใช้ไปตลอดชุดสอน อ่านผลจาก Display และ Chart หาเครื่องที่ช้าที่สุด (คอขวด)
แล้วแก้ 2 วิธี: เพิ่มเครื่องขนาน หรือใช้ <strong>ParallelStation</strong> ตัวเดียว ทั้งหมด 11 ขั้น ไม่ต้องเขียนโค้ด</p>

<table>
<tr><th>ลำดับ</th><th>หัวข้อ</th><th>ทำอะไร</th><th>ขั้น</th></tr>
<tr><td>1</td><td>เปิด Frame Model</td><td>ไลน์ 5 สถานี เวลาเท่ากัน 0:10</td><td>1</td></tr>
<tr><td>2</td><td>วาง Display + Chart</td><td>จาก Toolbox แล้วลาก object มาวาง</td><td>2–3</td></tr>
<tr><td>3</td><td>รัน Model อ่านผล</td><td>FG 355 ทุกแท่งสีเขียว</td><td>4</td></tr>
<tr><td>4</td><td>Model2 มีคอขวด</td><td>Station3 ช้าเป็น 0:20 ได้ 177</td><td>5</td></tr>
<tr><td>5</td><td>Model3 เพิ่มเครื่อง</td><td>Station32 วางขนาน ได้ 354</td><td>6</td></tr>
<tr><td>6</td><td>รู้จัก ParallelStation</td><td>เครื่องเดียวหลายช่อง</td><td>7</td></tr>
<tr><td>7</td><td>ตั้งช่อง + เวลา</td><td>X × Y และ 0:20 ต่อชิ้น</td><td>8–9</td></tr>
<tr><td>8</td><td>Model4 กับดัก When Full</td><td>ได้แค่ 177</td><td>10</td></tr>
<tr><td>9</td><td>Model5 เอาติ๊กออก</td><td>กลับมา 354</td><td>11</td></tr>
</table>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 และไฟล์ <code>Basic_02_Bottleneck_ParallelStation.spp</code>
(Class Library › Models › Model … Model5) &nbsp;·&nbsp; ผลผลิตก่อน–หลังแก้คอขวด <strong>177 → 354 ชิ้น/ชม.</strong> ทั้ง 2 วิธี
(ทุกตัวเลขในบทนี้วัดจริงใน Plant Simulation 2606 จำลอง 1 ชั่วโมง)
</div>
<div class="note">
<strong>ต่อจาก Basic 01:</strong> การวาง object ต่อเส้น ตั้งค่า และกด Run ทำเหมือน <a href="basic-01.html">บท 01</a>
บทนี้เน้นอ่านผล หาเครื่องที่ช้าที่สุด แล้วแก้ 2 วิธี
</div>

<h3>5 Frame ในไฟล์นี้ เล่าเรื่องเดียวกัน</h3>
<table>
<tr><th>Frame</th><th>เรื่อง</th><th>ขั้น</th></tr>
<tr><td><code>Model</code></td><td>ไลน์สมดุล ทุกเครื่อง 0:10 ได้ 355 ชิ้น/ชม.</td><td>1–4</td></tr>
<tr><td><code>Model2</code></td><td>Station3 ช้าเป็น 0:20 ทั้งไลน์เหลือ 177 ชิ้น/ชม.</td><td>5</td></tr>
<tr><td><code>Model3</code></td><td>เพิ่ม Station32 ขนานกับ Station3 ได้ 354 ชิ้น/ชม.</td><td>6</td></tr>
<tr><td><code>Model4</code></td><td>ParallelStation 2 ช่อง ติ๊ก When Full ได้แค่ 177 ชิ้น/ชม.</td><td>7–10</td></tr>
<tr><td><code>Model5</code></td><td>ParallelStation เดิม เอาติ๊กออก ได้ 354 ชิ้น/ชม.</td><td>11</td></tr>
</table>

<h2>ขั้นที่ 1: Frame Model ไลน์ 5 สถานี</h2>
{side_by_side(
    screenshot("assets/images/basic/02-01.jpg", "Frame Model ไลน์ 5 สถานี ก่อนรัน (Planning View)"),
    step_list([
        "<strong>Source</strong> — ปล่อยงานทันทีที่ว่าง (Interval 0)",
        "<strong>Station1–5</strong> — ทุกเครื่อง 0:10 ต่อชิ้น",
        "<strong>Drain</strong> — ชิ้นงานที่เสร็จ",
        "<strong>Display</strong> — Production Time = เวลาจำลอง",
        "<strong>Display</strong> — FG = จำนวนชิ้นที่เสร็จ",
        "<strong>Chart</strong> — Resource Statistics สถานะเครื่อง",
        "<strong>EventController</strong> — End 1:00:00",
    ])
)}
<div class="note"><strong>เปิด Frame:</strong> Class Library › Models มี 5 Frame ดับเบิลคลิกเพื่อเปิด ถ้าหน้าต่างเล็ก กดปุ่ม □ มุมขวาบนของ Frame เพื่อขยาย</div>

<h3>แสดงชื่อ Object ใน Frame</h3>
<p>คลิกขวาที่ Object › <code>Edit 3D Properties</code> › แท็บ <code>Captions</code></p>
{side_by_side(
    screenshot("assets/images/basic/02-02.jpg", "เมนูคลิกขวาที่ Station1"),
    screenshot("assets/images/basic/02-03.jpg", "หน้าต่าง Edit 3D Properties แท็บ Captions"),
)}
{step_list([
    "คลิกขวาที่ <strong>Station1</strong>",
    "<code>Edit 3D Properties...</code> — หรือคลิกเลือกแล้วกด <code>Space</code>",
    "แท็บ <code>Captions</code>",
    "ติ๊ก <code>Name / Label Activated</code>",
    "<code>OK</code> — ชื่อขึ้นใต้ Object",
])}

{side_by_side(
    screenshot("assets/images/basic/02-04.jpg", "ก่อน (บน) และหลังตั้งชื่อครบทุก Object (ล่าง)"),
    step_list([
        "<strong>EventController</strong> — ชื่อขึ้นใต้นาฬิกา",
        "<strong>Source</strong> — ทำทีละ Object เหมือนภาพก่อนหน้า",
        "<strong>Station1–5</strong> — ชื่อตรงกับใน Class Library และใน Chart",
        "<strong>Drain</strong> — ชื่อถูกป้าย FG บังอยู่ (วางที่เดียวกัน)",
    ])
)}
<div class="note"><strong>ชื่อไม่ขึ้น:</strong> ดูแท็บ View (ริบบอน 3D) › ปุ่ม <code>Names</code> ต้องเปิดอยู่ ปุ่มนี้เปิด / ปิดชื่อของทุก Object ใน Frame พร้อมกัน
— ตั้งที่ Object ใน Frame มีผลกับ Object นั้นตัวเดียว ถ้าตั้งที่ Class ใน Class Library ทุก Object ที่สืบทอดมาจะแสดงชื่อด้วย</div>

<h2>ขั้นที่ 2: วาง Display และลาก Drain มาวาง</h2>
{side_by_side(
    screenshot("assets/images/basic/02-05.jpg", "Toolbox แท็บ User Interface และ Display ที่วางใหม่"),
    step_list([
        "แท็บ <strong>User Interface</strong> ใน Toolbox",
        "<strong>Display</strong> — คลิกไอคอน 9.86",
        "คลิกใน Frame — วาง Display ใกล้ Drain",
    ])
)}
<div class="tip"><strong>ภาพนี้:</strong> ลบป้าย FG เดิมใน Frame Model ออกก่อน แล้ววางใหม่ให้ดูทีละขั้น (ไม่ได้บันทึกไฟล์) ถ้าทำตาม ให้ลบป้ายเดิมก่อนเหมือนกัน
— Display ใหม่ยังไม่รู้ว่าจะแสดงค่าอะไร บนจอจึงเป็นกรอบเปล่าชื่อ Display</div>

{screenshot("assets/images/basic/02-06.jpg", "ลาก Drain ไปปล่อยบน Display (ซ้าย) และ Display แสดง 0 (ขวา)")}
{step_list([
    "<strong>คลิกค้างที่ Drain</strong> แล้วลากไป",
    "<strong>ปล่อยบน Display</strong> — ห้ามปล่อยบนพื้นว่าง ไม่งั้น Drain จะย้ายที่แทน",
    "<strong>Display แสดง 0</strong> — Path = <code>Drain.statNumIn</code> ตั้งให้เอง = จำนวนชิ้นที่เข้า Drain",
])}

<h3>คลิกขวา Start แล้วอ่านค่า</h3>
{screenshot("assets/images/basic/02-07.jpg", "แถบเครื่องมือเมื่อคลิกขวาที่พื้น Frame (ซ้าย) และค่าหลังรัน 1 ชั่วโมง (ขวา)")}
{step_list([
    "<strong>Start/Stop Simulation</strong> — ปุ่มเขียวในแถบเครื่องมือที่ขึ้นตอนคลิกขวา",
    "<strong>Reset Simulation</strong> — ปุ่มแดง กลับไปเริ่มต้น ค่าบน Display กลับเป็น 0",
    "<strong>355</strong> — ชิ้นที่เสร็จใน 1 ชั่วโมง อีก 5 ชิ้นยังอยู่ในเครื่อง (Work in Process)",
])}
<p>ปุ่ม Start และ Reset เดียวกันนี้อยู่ที่ริบบอน <code>Home › Event Controller</code> ด้วย</p>

<h3>ข้อความนำหน้า และรูปแบบตัวอักษร</h3>
{screenshot("assets/images/basic/02-08.jpg", "หน้าต่าง Display แท็บ Data (ซ้าย) และแท็บ Display (ขวา)")}
{step_list([
    "<strong>Path</strong> — ป้ายเวลา = <code>EventController.SimTime</code>",
    '<strong>Comment</strong> — ข้อความหน้าตัวเลข เช่น "Production Time =" และ "FG ="',
    "แท็บ <strong>Display</strong> — รูปแบบของป้าย",
    "<strong>Font Size</strong> — ขนาดตัวอักษร",
    "<strong>Color</strong> — สีตัวอักษร แล้วกด <code>Apply</code>",
])}
<div class="note"><strong>ป้าย FG:</strong> ใช้ Path = <code>Drain.statNumIn</code> (ได้มาจากการลาก Drain) และ Comment "FG =" บน Frame จึงขึ้นเป็น FG = 355</div>

<h2>ขั้นที่ 3: วาง Chart ดูสถานะเครื่อง</h2>
{side_by_side(
    screenshot("assets/images/basic/02-09.jpg", "วาง Chart ใต้ไลน์ แล้วลาก Station1 มาวาง"),
    screenshot("assets/images/basic/02-10.jpg", "หน้าต่าง Statistics Type"),
)}
{step_list([
    "แท็บ <strong>User Interface</strong>",
    "<strong>Chart</strong> — คลิกไอคอนกราฟแท่ง",
    "คลิกใน Frame — วาง Chart ใต้ไลน์",
    "<strong>ลาก Station1</strong> ไปปล่อยบน Chart",
    "<strong>Resource Statistics</strong> ใน Statistics Type (= สถานะของเครื่อง)",
    "<code>OK</code>",
])}

{screenshot("assets/images/basic/02-11.jpg", "หน้าต่าง Chart หลังรัน (ซ้าย) และเมนูคลิกขวาที่ Chart (ขวา)")}
{step_list([
    "<strong>Station1–5</strong> — ลากทีละเครื่องมาปล่อยบน Chart ได้ 5 แท่ง (ครั้งต่อไปไม่ถาม Statistics Type)",
    "ปุ่ม <strong>×</strong> — ปิดหน้าต่าง Chart",
    "คลิกขวาที่ Chart › <code>Show</code> — เปิดหน้าต่างอีกครั้ง",
])}

<h3>ค่าของ Chart ที่ตั้งให้</h3>
{side_by_side(
    screenshot("assets/images/basic/02-12.jpg", "หน้าต่าง Chart แท็บ Data"),
    step_list([
        "<strong>Collect Data</strong> — ติ๊กไว้ = เก็บข้อมูลระหว่างรัน",
        "<strong>Data Source = Input Channels</strong> — แสดงข้อมูลของ object ที่เลือก",
        "ปุ่ม <strong>Input Channels</strong> — รายการ Station1–5 ที่ลากมาวาง",
        "<strong>Mode = Sample, Interval 1:00</strong> — เก็บค่าทุก 1 นาที",
    ])
)}
<div class="tip"><strong>ไม่ต้องพิมพ์เอง:</strong> ลาก object มาวางบน Chart = เพิ่มเข้า Input Channels ให้เอง ใช้ปุ่มนี้เมื่ออยากลบหรือเรียงลำดับแท่ง</div>

<h3>Chart แบบแบนบน Frame หรือแบบ 3D</h3>
{screenshot("assets/images/basic/02-13.jpg", "แท็บ Display ของ Chart: Model (ซ้าย) และ Model2 (ขวา)")}
{step_list([
    "<strong>Category</strong> — <code>Chart</code> = กราฟแบนบน Frame (Model) · <code>3D Chart</code> = ป้ายกราฟตั้งในฉาก 3D (Model2–Model5)",
    "<strong>Chart Type = 100% Stacked Columns</strong> — แท่งละ 100% แบ่งสีตามสถานะ",
    "<strong>Display in Frame</strong> — ติ๊กไว้ = แสดงกราฟบน Frame แทนไอคอน",
])}
<div class="note"><strong>ระวัง:</strong> 3D Chart วาดใหม่ระหว่างรันแบบมีภาพเคลื่อนไหว ถ้ารันแบบไม่มีภาพเคลื่อนไหว กราฟจะว่าง</div>

{screenshot("assets/images/basic/02-14.jpg", "Model2 › Chart: แท็บ Display (ซ้าย) และปุ่ม 3D › Transformation (ขวา)")}
{step_list([
    "<strong>Category = 3D Chart</strong> — Display in Frame ติ๊กให้เอง",
    "ปุ่ม <strong>3D</strong> มุมซ้ายล่าง — เปิดหน้าต่าง 3D แท็บ Transformation",
    "<strong>Rotation: Angle = 90, Axis X = 1</strong> — หมุน 90 องศารอบแกน X แผ่นกราฟจึงตั้งขึ้นจากพื้น",
    "<strong>Position Z = 4 m</strong> — ยกกราฟขึ้นจากพื้น (X, Y = ตำแหน่งบนพื้น)",
    "<code>Apply</code> แล้ว <code>OK</code> — ดูผลในมุมมอง 3D (ขั้นที่ 5)",
])}

<h2>ขั้นที่ 4: รัน Model 1 ชั่วโมง แล้วอ่านผล</h2>
{side_by_side(
    screenshot("assets/images/basic/02-15.jpg", "Frame Model หลังรัน 1 ชั่วโมง"),
    step_list([
        "<strong>Production Time = 1:00:00</strong> — ครบเวลาแล้วหยุดเอง",
        "<strong>FG = 355</strong> — ชิ้นงานที่เสร็จใน 1 ชั่วโมง",
        "<strong>Chart เขียวเต็มทุกแท่ง</strong> — ทุกเครื่อง Working ~99–100%",
    ])
)}
<div class="note"><strong>ทำไมไม่ใช่ 360:</strong> Source ปล่อย 360 ชิ้น ตอนหมดเวลายังค้างอยู่ใน Station เครื่องละ 1 ชิ้น รวม 5 ชิ้น — ไลน์นี้สมดุล</div>

<h2>ขั้นที่ 5: Model2 — Station3 ช้ากว่าเพื่อน 2 เท่า</h2>
{side_by_side(
    screenshot("assets/images/basic/02-16.jpg", "หน้าต่าง Station3 ใน Model2"),
    screenshot("assets/images/basic/02-17.jpg", "Model2 หลังรัน 1 ชั่วโมง"),
)}
{step_list([
    "<strong>Station3 Processing Time = 0:20</strong> — เครื่องอื่นยัง 0:10",
    "<strong>FG = 177</strong> — ทั้งไลน์ได้แค่ครึ่งเดียว",
])}
<div class="note"><strong>คอขวด (Bottleneck):</strong> ทั้งไลน์เดินได้เร็วเท่าเครื่องที่ช้าที่สุด 3600 ÷ 20 = 180 ชิ้น ใกล้กับ 177 ที่วัดได้</div>

<h3>3D Chart บอกว่าเครื่องไหนเป็นคอขวด</h3>
{side_by_side(
    screenshot("assets/images/basic/02-18.jpg", "3D Chart ของ Model2 หลังรัน 1 ชั่วโมง"),
    step_list([
        "<strong>Station1–2 สีเหลือง</strong> — Blocked ~50% ทำเสร็จแต่ส่งต่อไม่ได้",
        "<strong>Station3 เขียวเต็ม</strong> — Working ~99% = คอขวด",
        "<strong>Station4–5 สีเทา</strong> — Waiting ~51% รองานจากเครื่องก่อนหน้า",
        "<strong>ชื่อสถานะ</strong> — ดูสีจาก legend ด้านขวา",
    ])
)}
<div class="tip"><strong>วิธีจำ:</strong> ก่อนคอขวด = <strong>เหลือง</strong> (Blocked) · หลังคอขวด = <strong>เทา</strong> (Waiting) · คอขวด = <strong>เขียวเต็มแท่ง</strong></div>

<h2>ขั้นที่ 6: Model3 — เพิ่ม Station32 ขนานกับ Station3</h2>
{side_by_side(
    screenshot("assets/images/basic/02-19.jpg", "Frame Model3 ที่มี Station32 วางขนาน"),
    step_list([
        "<strong>Station3</strong> — 0:20 เหมือนเดิม",
        "<strong>Station32</strong> — เครื่องใหม่ 0:20 วางขนานกัน",
        "<strong>Connector 8 เส้น</strong> — Station2 ส่งไป 2 ทาง (Exit Strategy = Cyclic) แล้วรวมเข้า Station4",
        "<strong>FG = 354</strong> — กลับมาเกือบเท่าไลน์สมดุล",
    ])
)}
<div class="note"><strong>ทำไมได้ผล:</strong> 2 เครื่อง × 20 วินาที = เฉลี่ย 10 วินาทีต่อชิ้น เท่ากับเครื่องอื่นในไลน์</div>

{screenshot("assets/images/basic/02-20.jpg", "Chart ของ Model3 หลังแก้ (ซ้าย) และตำแหน่ง Station32 ในฉาก 3D (ขวา)")}
{step_list([
    "<strong>ทุกแท่งสีเขียว</strong> — ไม่มีเครื่องถูกบล็อก หรือรองาน",
    "<strong>แท่ง Station32</strong> — เครื่องใหม่อยู่ใน Input Channels ของ Chart แล้ว",
    "<strong>Station32</strong> — วางหน้า Station3 ในฉาก 3D",
])}
<div class="tip"><strong>คำถาม:</strong> แก้ได้ 177 → 354 แต่ต้องวางเครื่องเพิ่มและต่อเส้นแยกทาง มีวิธีที่ง่ายกว่านี้ไหม → ParallelStation (ขั้นที่ 7)</div>

<h2>ขั้นที่ 7: ParallelStation แทน 2 เครื่อง</h2>
{screenshot("assets/images/basic/02-21.jpg", "Toolbox แท็บ Material Flow: Station และ ParallelStation")}
{screenshot("assets/images/basic/02-22.jpg", "Frame Model4 ที่ใช้ ParallelStation แทน Station3")}
{step_list([
    "<strong>Station</strong> — เครื่อง 1 ช่อง ทำทีละชิ้น",
    "<strong>ParallelStation</strong> — เครื่องหลายช่อง ทำหลายชิ้นพร้อมกัน",
    "วางแทน Station3 ต่อ Connector เข้า 1 ออก 1",
])}
<div class="note"><strong>ต่อเส้นน้อยลง:</strong> 2 เครื่องแยกใช้ Connector เข้า–ออก 4 เส้น ParallelStation ตัวเดียวใช้ 2 เส้น (Model3 8 เส้น → Model4 6 เส้น)</div>

<h2>ขั้นที่ 8–9: ตั้งจำนวนช่อง และเวลาทำงาน</h2>
{side_by_side(
    screenshot("assets/images/basic/02-23.jpg", "หน้าต่าง ParallelStation แท็บ Attributes"),
    step_list([
        "<strong>X-Dimension = 2</strong> — จำนวนช่องแนวนอน",
        "<strong>Y-Dimension = 1</strong> — จำนวนแถว → 2 × 1 = 2 ช่อง",
        "<strong>Start Processing When Full</strong> — ติ๊กไว้ (ค่าเริ่มต้น) = รอให้ครบทุกช่องก่อนเริ่มทำ",
    ])
)}
<div class="note"><strong>ตามคู่มือ:</strong> ค่าเริ่มต้นคือติ๊ก When Full ไว้ ชิ้นใหม่เข้าได้เมื่อชุดเดิมทำเสร็จและออกหมดแล้ว
— ParallelStation ที่วางใหม่จาก Toolbox มีค่าเริ่มต้น 2 × 2 = 4 ช่อง ในไฟล์นี้ตั้งเป็น 2 × 1</div>

{side_by_side(
    screenshot("assets/images/basic/02-24.jpg", "หน้าต่าง ParallelStation แท็บ Times"),
    step_list([
        "<strong>Times</strong> — แท็บตั้งเวลา",
        "<strong>Processing Time = 0:20</strong> — ทุกช่องใช้ 20 วินาทีต่อชิ้น",
    ])
)}
<div class="tip"><strong>คิดเร็ว:</strong> 2 ช่อง × 20 วินาที = เฉลี่ย 10 วินาทีต่อชิ้น เท่ากับเครื่องอื่นในไลน์ ควรได้ ~354 ชิ้น/ชม. เหมือน Model3</div>

<h2>ขั้นที่ 10: Model4 — ได้แค่ 177 ทั้งที่มี 2 ช่อง</h2>
{screenshot("assets/images/basic/02-25.jpg", "Frame Model4 หลังรัน 1 ชั่วโมง")}
{step_list([
    "<strong>ParallelStation</strong> — ติ๊ก When Full ไว้",
    "<strong>FG = 177</strong> — เท่ากับ Model2 ที่มีเครื่องเดียว 20 วินาที",
])}
<div class="note"><strong>ทำไม:</strong> ต้องรอชิ้นที่ 2 เข้ามาให้ครบก่อนเริ่ม และรับชุดใหม่ได้เมื่อออกหมดแล้ว 2 ช่องจึงทำงานเหมือนเครื่องเดียว</div>

{side_by_side(
    screenshot("assets/images/basic/02-26.jpg", "3D Chart ของ Model4 หลังรัน"),
    step_list([
        "<strong>Station1–2 สีเหลือง</strong> — Blocked ~49% ส่งต่อไม่ได้",
        "<strong>ParallelStation</strong> — เขียว 50% เทา 50% = รอชิ้นให้ครบ 2 ช่อง",
        "<strong>Station4–5 สีเทา</strong> — Waiting ~51% รองาน",
        "<strong>ชื่อสถานะ</strong> — ดูสีจาก legend ด้านขวา",
    ])
)}
<div class="tip"><strong>ต่างจาก Model2:</strong> คอขวดใน Model2 เขียวเต็มแท่ง แต่ ParallelStation ที่ติ๊ก When Full เสียเวลาครึ่งหนึ่งไปกับการรอ</div>

<h2>ขั้นที่ 11: Model5 — เอาติ๊ก When Full ออก</h2>
{screenshot("assets/images/basic/02-27.jpg", "ParallelStation ใน Model5 ที่ไม่ได้ติ๊ก When Full และผลหลังรัน")}
{step_list([
    "<strong>Start Processing When Full</strong> — เอาติ๊กออก = เริ่มทำทันทีที่มีชิ้นเข้าช่อง ไม่ต้องรอให้ครบ",
    "<strong>FG = 354</strong> — เท่ากับ 2 เครื่องแยกใน Model3 แต่ต่อเส้นน้อยกว่า",
])}
<div class="tip"><strong>จำง่าย:</strong> ParallelStation ที่ทำงานต่อเนื่องในไลน์ → เอาติ๊ก When Full ออก · ติ๊กไว้เมื่อต้องการให้ทำพร้อมกันทั้งชุด เช่น เตาอบ</div>

{screenshot("assets/images/basic/02-28.jpg", "3D Chart ก่อน–หลังเอาติ๊กออก: Model4 (ซ้าย) และ Model5 (ขวา)")}
{step_list([
    "<strong>ติ๊ก When Full</strong> — ParallelStation ทำงาน 50% · ได้ 177 ชิ้น/ชม.",
    "<strong>เอาติ๊กออก</strong> — ทำงาน 99% ทุกแท่งเขียว · ได้ 354 ชิ้น/ชม. (+100%)",
])}
<div class="note"><strong>บทเรียน:</strong> ก่อนซื้อเครื่องเพิ่ม ให้ดูก่อนว่าเครื่องเดิมทำงานจริงกี่ % — เปลี่ยนแค่ติ๊กเดียว ผลเพิ่มเป็นเท่าตัวโดยไม่ต้องเพิ่มเครื่อง</div>

<h2>สรุป 5 Frame (จำลอง 1 ชั่วโมง)</h2>
<table>
<tr><th>Frame</th><th>สิ่งที่ต่าง</th><th>Connector</th><th>FG (ชิ้น/ชม.)</th><th>เครื่องจุด Station3 ทำงาน</th></tr>
<tr><td><code>Model</code></td><td>ทุกเครื่อง 0:10</td><td>6</td><td><strong>355</strong></td><td>~99% ไลน์สมดุล</td></tr>
<tr><td><code>Model2</code></td><td>Station3 = 0:20</td><td>6</td><td><strong>177</strong></td><td>99% = คอขวด</td></tr>
<tr><td><code>Model3</code></td><td>เพิ่ม Station32 (0:20) ขนานกับ Station3</td><td>8</td><td><strong>354</strong></td><td>~99% ทั้ง 2 เครื่อง</td></tr>
<tr><td><code>Model4</code></td><td>ParallelStation 2 ช่อง 0:20 ติ๊ก When Full</td><td>6</td><td><strong>177</strong></td><td>50% (รอครึ่งเวลา)</td></tr>
<tr><td><code>Model5</code></td><td>ParallelStation 2 ช่อง 0:20 ไม่ติ๊ก</td><td>6</td><td><strong>354</strong></td><td>~99%</td></tr>
</table>
<p>Model3 กับ Model5 ได้ผลเท่ากัน แต่ Model5 ใช้ object และเส้นน้อยกว่า ส่วน Model4 แสดงว่าค่าเริ่มต้นที่ไม่ได้ตรวจ ทำให้ผลเหลือครึ่งเดียว</p>

<h2>ลองเอง</h2>
<p>เดาก่อนว่า FG จะเป็นเท่าไร แล้วรันดู — แก้ทีละค่าจากค่าเดิม และกด Reset ก่อน Start ทุกครั้ง</p>
<h3>ลองเอง 1: เปลี่ยนเวลาแล้วดู FG (Model–Model3)</h3>
<table>
<tr><th>Frame</th><th>ลองเปลี่ยน</th><th>FG หลังรัน</th><th>ทำไม</th></tr>
<tr><td><code>Model</code></td><td>Station1 = 0:20</td><td><strong>177</strong></td><td>คอขวดอยู่ต้นไลน์ ผลเท่ากัน</td></tr>
<tr><td><code>Model</code></td><td>Station5 = 0:20</td><td><strong>177</strong></td><td>คอขวดอยู่ท้ายไลน์ ผลก็เท่ากัน</td></tr>
<tr><td><code>Model2</code></td><td>Station3 = 0:15</td><td><strong>237</strong></td><td>3600 ÷ 15 = 240</td></tr>
<tr><td><code>Model2</code></td><td>Station3 = 0:10</td><td><strong>355</strong></td><td>กลับเป็นไลน์สมดุลเหมือน Model</td></tr>
<tr><td><code>Model3</code></td><td>Station3 และ Station32 = 0:30</td><td><strong>236</strong></td><td>2 เครื่อง ÷ 30 วินาที = 15 วินาทีต่อชิ้น</td></tr>
</table>

<h3>ลองเอง 2: เปลี่ยนช่องและเวลาใน Model4</h3>
<table>
<tr><th>ลองเปลี่ยนที่ ParallelStation</th><th>FG หลังรัน</th><th>ทำไม</th></tr>
<tr><td>เอาติ๊ก When Full ออก</td><td><strong>354</strong></td><td>เหมือน Model5</td></tr>
<tr><td>4 ช่อง (X = 4) × 0:40 ติ๊ก When Full</td><td><strong>140</strong></td><td>ต้องรอให้ครบ 4 ชิ้น ยิ่งช่องมากยิ่งรอนาน</td></tr>
<tr><td>4 ช่อง × 0:40 ไม่ติ๊ก</td><td><strong>352</strong></td><td>เฉลี่ย 10 วินาทีต่อชิ้น เท่าเครื่องอื่น</td></tr>
<tr><td>2 ช่อง × 0:10 ติ๊ก When Full</td><td><strong>236</strong></td><td>เครื่องเร็วขึ้น 2 เท่า แต่ยังแพ้ไลน์ปกติ (355)</td></tr>
<tr><td>3 ช่อง × 0:20 ไม่ติ๊ก</td><td><strong>354</strong></td><td>ช่องเพิ่มไม่ช่วย เครื่องอื่นจำกัดที่ 10 วินาที</td></tr>
</table>

<h2>ปัญหาที่พบบ่อย และวิธีแก้</h2>
<table>
<tr><th>อาการ</th><th>วิธีแก้</th></tr>
<tr><td>3D Chart ว่างหลังรัน</td><td>รันด้วยปุ่ม Start แบบมีภาพเคลื่อนไหว 3D Chart จะวาดใหม่ระหว่างรัน</td></tr>
<tr><td>Planning View มองไม่เห็น 3D Chart</td><td>3D Chart ตั้งขึ้นในฉาก 3D: ปิด Planning View แล้วหมุนมุมกล้อง</td></tr>
<tr><td>Chart ไม่มีแท่งของเครื่องใหม่</td><td>ใส่เครื่องใหม่ (Station32, ParallelStation) ใน Input Channels ของ Chart</td></tr>
<tr><td>เพิ่มเครื่องแล้ว FG ไม่เพิ่ม</td><td>ตรวจ Connector เข้า–ออกเครื่องใหม่ให้ครบ</td></tr>
<tr><td>ParallelStation รับงานชุดเดียวแล้วรอนาน</td><td>แท็บ Attributes › เอาติ๊ก <code>Start Processing When Full</code> ออก</td></tr>
<tr><td>จำนวนช่องไม่ตรงที่ต้องการ</td><td>จำนวนช่อง = X-Dimension × Y-Dimension (ค่าเริ่มต้น 2 × 2 = 4)</td></tr>
<tr><td>เพิ่มช่องแล้ว FG ไม่เพิ่ม</td><td>คอขวดย้ายไปเครื่องอื่นแล้ว ดูสีใน Chart</td></tr>
<tr><td>กด Start แล้วผลไม่เริ่มจากศูนย์</td><td>กด Reset (ปุ่มแดง) ก่อน Start ทุกครั้ง</td></tr>
</table>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ในลองเอง 1 ทำไมการตั้ง Station1 หรือ Station5 เป็น 0:20 ได้ FG 177 เท่ากับตั้ง Station3 ทั้งที่อยู่คนละตำแหน่งในไลน์?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะทั้งไลน์เดินได้เร็วเท่าเครื่องที่ช้าที่สุดเสมอ ไม่ว่าคอขวดจะอยู่ต้น กลาง หรือท้ายไลน์
สิ่งที่ต่างคือสีใน Chart — เครื่องก่อนคอขวดจะเป็นสีเหลือง (Blocked) เครื่องหลังคอขวดเป็นสีเทา (Waiting)
ถ้าคอขวดอยู่ Station1 ก็จะไม่มีสีเหลืองเลย มีแต่สีเทาตามหลัง</div>
'''

BODY[("basic", "03")] = f'''
<p class="lead" style="max-width:46em;">ต่อจากบท 02 — ไลน์ 5 สถานีเดิม เวลาเฉลี่ย 10 วินาทีเท่าเดิม บทนี้ดู 2 เรื่องที่ทำให้ไลน์ได้น้อยกว่าที่คิด:
<strong>เวลาไม่คงที่</strong> (แก้ด้วย Buffer) และ<strong>เครื่องเสีย</strong> (อ่านผลด้วยแท็บ Statistics และ OEE) ทั้งหมด 9 ขั้น ไม่ต้องเขียนโค้ด</p>

<table>
<tr><th>ลำดับ</th><th>หัวข้อ</th><th>ผล</th><th>ขั้น</th></tr>
<tr><td>1</td><td>ตั้งเวลาแบบสุ่ม</td><td>Uniform 0:05–0:15</td><td>1</td></tr>
<tr><td>2</td><td>Model ไม่มี Buffer</td><td>355 เหลือ 276</td><td>2–3</td></tr>
<tr><td>3</td><td>Model2 ใส่ Buffer</td><td>ความจุ 3 ชิ้น ได้ 337</td><td>4</td></tr>
<tr><td>4</td><td>Model3 ไม่มีเครื่องเสีย</td><td>1 กะ 8 ชม. ได้ 2,875</td><td>5</td></tr>
<tr><td>5</td><td>ตั้ง Failure</td><td>Availability 90%, MTTR 5:00</td><td>6</td></tr>
<tr><td>6</td><td>Model4 อ่านผล</td><td>2,484 ชิ้น</td><td>7</td></tr>
<tr><td>7</td><td>Statistics + OEE</td><td>A × P × Q จากสถิติ</td><td>8</td></tr>
<tr><td>8</td><td>Model5 รัน 30 วัน</td><td>เครื่องเสียเข้าใกล้ 10%</td><td>9</td></tr>
<tr><td>9</td><td>ลองเอง</td><td>ความจุ Buffer, Availability, MTTR</td><td>–</td></tr>
</table>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 และไฟล์ <code>Basic_03_Buffer_Failures_OEE.spp</code>
(Class Library › Models › Model … Model5) &nbsp;·&nbsp; ใส่ Buffer 3 ชิ้น ผลผลิต <strong>276 → 337 ชิ้น/ชม.</strong>
(ทุกตัวเลขในบทนี้วัดจริงใน Plant Simulation 2606)
</div>

<h3>5 Frame ในไฟล์นี้ เล่า 2 เรื่อง</h3>
<table>
<tr><th>Frame</th><th>เรื่อง</th><th>ขั้น</th></tr>
<tr><td><code>Model</code></td><td>เวลาสุ่ม ต่อเครื่องตรงกัน ได้ 276 ชิ้น/ชม.</td><td>1–3</td></tr>
<tr><td><code>Model2</code></td><td>ใส่ Buffer ความจุ 3 ระหว่างทุกเครื่อง ได้ 337 ชิ้น/ชม.</td><td>4</td></tr>
<tr><td><code>Model3</code></td><td>กลับเป็นเวลาคงที่ 0:10 ไม่มีเครื่องเสีย 1 กะ ได้ 2,875 ชิ้น</td><td>5</td></tr>
<tr><td><code>Model4</code></td><td>Station3 Availability 90% MTTR 5:00 1 กะ ได้ 2,484 ชิ้น</td><td>6–8</td></tr>
<tr><td><code>Model5</code></td><td>เหมือน Model4 แต่รัน 30 วัน ได้ 324 ชิ้น/ชม.</td><td>9</td></tr>
</table>
<div class="note"><strong>2 เรื่อง:</strong> เรื่องที่ 1 (Model, Model2) เวลาไม่คงที่ทำให้เสียผลผลิต ที่พักงานดึงกลับมาได้ ·
เรื่องที่ 2 (Model3–5) กลับไปใช้เวลาคงที่ เพื่อให้เห็นผลของเครื่องเสียอย่างเดียว ไม่ปนกับเวลาสุ่ม</div>

<h2>ขั้นที่ 1: ตั้งเวลาทำงานแบบสุ่ม (Uniform)</h2>
{side_by_side(
    screenshot("assets/images/basic/03-01.jpg", "Frame Model › Station1 แท็บ Times ตั้งเวลาแบบ Uniform"),
    step_list([
        "<strong>Uniform</strong> — สุ่มเวลาได้ทุกค่าในช่วงที่กำหนด (เลือกจากช่อง Const / Uniform / ชนิดอื่น)",
        "<strong>0:05, 0:15</strong> — ต่ำสุด 5 วินาที สูงสุด 15 วินาที เฉลี่ย 10 วินาที เท่ากับบท 02",
    ])
)}
<div class="tip"><strong>ทำไมใช้เวลาสุ่ม:</strong> งานจริงไม่ได้ใช้เวลาเท่ากันทุกชิ้น · ไฟล์นี้ตั้งทุก Station แบบเดียวกัน · รันซ้ำได้ผลเท่าเดิมทุกครั้ง</div>

<h2>ขั้นที่ 2: Model — เวลาเฉลี่ยเท่าเดิม แต่ได้น้อยลง</h2>
{screenshot("assets/images/basic/03-02.jpg", "Frame Model หลังรัน 1 ชั่วโมง")}
{step_list([
    "<strong>Station1–5</strong> — ทุกเครื่องสุ่ม 0:05–0:15",
    "<strong>ต่อเครื่องตรงกัน</strong> — ไม่มีที่พักงานระหว่างเครื่อง",
    "<strong>FG = 276</strong> — ลดจาก 355 ในบท 02 (−22%)",
])}
<div class="note"><strong>ทำไมลดลง:</strong> เครื่องหน้าเสร็จเร็วแต่เครื่องหลังยังไม่ว่าง → ต้องรอส่ง · เครื่องหลังเสร็จเร็วแต่ไม่มีงานเข้า → ว่าง</div>

<h2>ขั้นที่ 3: Chart — เสียเวลากระจายทั้งไลน์</h2>
{side_by_side(
    screenshot("assets/images/basic/03-03.jpg", "3D Chart ของ Model หลังรัน"),
    step_list([
        "<strong>Station1 สีเหลือง</strong> — Blocked 24% ทำเสร็จแต่ส่งต่อไม่ได้",
        "<strong>Station5 สีเทา</strong> — Waiting 24% รองาน",
        "<strong>สีเขียว</strong> — ทุกเครื่องทำงานแค่ 76–79%",
        "<strong>ชื่อสถานะ</strong> — ดูสีจาก legend ด้านขวา",
    ])
)}
<div class="tip"><strong>ต่างจากบท 02:</strong> ไม่มีเครื่องไหนเขียวเต็มแท่ง ไม่มีคอขวดจุดเดียว แต่ทุกเครื่องเสียเวลาไปกับการรอ</div>

<h2>ขั้นที่ 4: Buffer = พื้นที่พักงานระหว่างเครื่อง</h2>
{screenshot("assets/images/basic/03-04.jpg", "ไอคอน Buffer ใน Toolbox แท็บ Material Flow")}
{side_by_side(
    screenshot("assets/images/basic/03-05.jpg", "หน้าต่าง Buffer1 ใน Model2"),
    step_list([
        "<strong>Buffer</strong> — ไอคอนใน Toolbox (เลื่อนเมาส์ไปชี้จะเห็นชื่อ)",
        "<strong>Capacity = 3</strong> — พักงานได้สูงสุด 3 ชิ้น",
        "<strong>Buffer Type = Queue</strong> — เข้าก่อน ออกก่อน (FIFO)",
    ])
)}
<div class="note"><strong>วิธีวาง:</strong> วาง Buffer ระหว่าง 2 Station แล้วต่อ Connector: Station → Buffer → Station
— Model2 มี Buffer1 ถึง Buffer4 ความจุ 3 ชิ้นทุกตัว วางระหว่างทุกคู่ของ Station</div>

{screenshot("assets/images/basic/03-06.jpg", "Frame Model2 หลังรัน 1 ชั่วโมง")}
{step_list([
    "<strong>Buffer1</strong> — ระหว่าง Station1 กับ Station2",
    "<strong>Buffer4</strong> — ระหว่าง Station4 กับ Station5",
    "<strong>FG = 337</strong> — เพิ่มจาก 276 (+22%) ทุก Station ทำงาน 91–97%",
])}
<div class="tip"><strong>Buffer ช่วยอย่างไร:</strong> ไม่ได้ทำให้เครื่องเร็วขึ้น แต่เครื่องที่เสร็จเร็วมีที่วางงาน ไม่ต้องหยุดรอเครื่องถัดไป</div>

{screenshot("assets/images/basic/03-07.jpg", "3D Chart ก่อน–หลังใส่ Buffer: Model (ซ้าย) และ Model2 (ขวา)")}
{step_list([
    "<strong>ไม่มี Buffer</strong> — Station ทำงาน 76–79% · ได้ 276 ชิ้น/ชม.",
    "<strong>มี Buffer 3 ชิ้น</strong> — ทำงาน 91–97% · ได้ 337 ชิ้น/ชม.",
])}
<div class="note"><strong>สังเกต:</strong> สีเหลืองและสีเทาลดลงมาก เครื่องเดิม เวลาเดิม แค่เพิ่มที่พักงาน — Station5 ยังรองานอยู่บ้าง (Waiting 9%) เพราะเวลาสุ่มทำให้บางช่วงงานมาไม่ทัน</div>

<h2>ขั้นที่ 5: Model3 — 1 กะ ไม่มีเครื่องเสีย</h2>
{side_by_side(
    screenshot("assets/images/basic/03-08.jpg", "Frame Model3 หลังรัน 8 ชั่วโมง"),
    step_list([
        "<strong>End Time = 8:00:00</strong> — จำลอง 1 กะ",
        "<strong>FG = 2,875</strong> — ≈ 8 × 360 ชิ้น",
        "<strong>Chart เขียวทุกแท่ง</strong> — ทุกเครื่องทำงานเต็มที่",
    ])
)}
<div class="tip"><strong>ทำไมกลับเป็นเวลาคงที่:</strong> ดูผลของเครื่องเสียอย่างเดียว ไม่ปนกับเวลาสุ่ม · 8 ชั่วโมงเพราะเครื่องเสียเกิดนานๆ ครั้ง
(ตั้งที่ EventController › Settings › End Time) — Model3 คือไลน์ของบท 02 (ทุกเครื่อง 0:10)</div>

<h2>ขั้นที่ 6: เพิ่มเครื่องเสียให้ Station3</h2>
{side_by_side(
    screenshot("assets/images/basic/03-09.jpg", "Model4 › Station3 แท็บ Failures"),
    step_list([
        "<strong>Failures</strong> — แท็บตั้งเครื่องเสีย",
        "<strong>New…</strong> — เพิ่มรูปแบบเครื่องเสีย 1 แบบ",
        "<strong>Availability = 90%</strong> — เครื่องพร้อมทำงาน 90% ของเวลา",
        "<strong>MTTR = 300</strong> — ซ่อมเฉลี่ยครั้งละ 300 วินาที (5 นาที)",
    ])
)}
<div class="note"><strong>Active:</strong> ติ๊กไว้ทั้งช่องบนและในตาราง = เปิดใช้เครื่องเสีย · เอาติ๊กออกเมื่ออยากรันแบบเครื่องไม่เสีย
— ดับเบิลคลิกแถว Failure ในตารางเพื่อเปิดดูรายละเอียด</div>

{side_by_side(
    screenshot("assets/images/basic/03-10.jpg", "รายละเอียด Failure ของ Station3"),
    step_list([
        "<strong>Availability</strong> (ติ๊ก) — กรอกเป็น % และ MTTR",
        "<strong>Availability = 90%</strong> — เวลาพร้อมทำงาน",
        "<strong>MTTR = 5:00</strong> — เวลาซ่อมเฉลี่ยต่อครั้ง",
        "<strong>Interval = 45:00</strong> — เวลาเฉลี่ยระหว่างเสีย โปรแกรมคำนวณให้",
        "<strong>Duration</strong> — เวลาเสียแต่ละครั้ง สุ่มรอบ 5:00",
        "<strong>Failure Relates To</strong> — SimulationTime = นับตลอดการจำลอง",
    ])
)}
<div class="tip"><strong>ตรวจตัวเลข:</strong> 45 ÷ (45 + 5) = 90% ตรงกับ Availability ที่ตั้ง — ถ้าจะกรอก Interval เอง ให้เอาติ๊ก Availability ออก</div>

<h2>ขั้นที่ 7: Model4 — เครื่องเดียวเสีย ทั้งไลน์หยุดตาม</h2>
{screenshot("assets/images/basic/03-11.jpg", "Frame Model4 หลังรัน 8 ชั่วโมง")}
{side_by_side(
    screenshot("assets/images/basic/03-12.jpg", "Chart ของ Model4 หลังรัน"),
    step_list([
        "<strong>Station3</strong> — มีเครื่องเสีย (เปิดชื่อไว้)",
        "<strong>FG = 2,484</strong> — ลดจาก 2,875 (−14%)",
        "<strong>สีแดง = Failed</strong> — แท่ง Station3 ใน Chart",
    ])
)}
<div class="note"><strong>อ่าน Chart:</strong> Station3 เสีย → Station1–2 ส่งต่อไม่ได้ (เหลือง) → Station4–5 ไม่มีงานเข้า (เทา)</div>

<h2>ขั้นที่ 8: อ่านแท็บ Statistics แล้วคำนวณ OEE</h2>
{side_by_side(
    screenshot("assets/images/basic/03-13.jpg", "Station3 แท็บ Statistics หลังรัน"),
    step_list([
        "<strong>Statistics</strong> — แท็บสถิติของเครื่อง",
        "<strong>Working 86.33%</strong> — เวลาที่ทำงานจริง",
        "<strong>Failed 13.60%</strong> — เวลาที่เครื่องเสีย",
        "<strong>Exits 2,486</strong> — ชิ้นที่ผ่านเครื่องนี้",
    ])
)}
<div class="note"><strong>ทำไมไม่ใช่ 10%:</strong> เครื่องเสียเป็นการสุ่ม 8 ชั่วโมงสั้นเกินไป ค่ายังไม่เฉลี่ย (ดูขั้นที่ 9)
— ค่าในแท็บ Statistics เป็นของการรันล่าสุด กด Reset แล้วค่าจะเริ่มใหม่</div>

<h3>คำนวณ OEE จากสถิติ: OEE = A × P × Q</h3>
<table>
<tr><th>ตัวชี้วัด</th><th>ความหมาย</th><th>Model4 (8 ชม.)</th><th>มาจากไหน</th></tr>
<tr><td><strong>Availability (A)</strong></td><td>เวลาพร้อมทำงาน ÷ เวลาทั้งหมด</td><td>86.4%</td><td>100% − Failed 13.6%</td></tr>
<tr><td><strong>Performance (P)</strong></td><td>ความเร็วจริง ÷ ความเร็วที่ตั้ง</td><td>~100%</td><td>ทำงานที่ 0:10 ตามที่ตั้ง</td></tr>
<tr><td><strong>Quality (Q)</strong></td><td>ของดี ÷ ของทั้งหมด</td><td>100%</td><td>โมเดลนี้ไม่มีของเสีย</td></tr>
<tr><td><strong>OEE</strong></td><td>A × P × Q</td><td><strong>≈ 86%</strong></td><td>ตรวจ: FG 2,484 ÷ เต็ม 2,880 = 86.3%</td></tr>
</table>
<div class="tip"><strong>หาปุ่ม OEE ไม่เจอ?</strong> Plant Simulation ไม่มีปุ่ม OEE ให้ คำนวณจากแท็บ Statistics (นิยาม OEE แบบมาตรฐานทั่วไป)
— ผลผลิตสูงสุดใน 8 ชั่วโมง = 8 × 3600 ÷ 10 = 2,880 ชิ้น</div>

<h2>ขั้นที่ 9: Model5 — รัน 30 วัน ค่าจึงนิ่ง</h2>
{screenshot("assets/images/basic/03-14.jpg", "EventController › Settings ของ Model5 (ซ้าย) และ Station3 › Statistics หลังรัน 30 วัน (ขวา)")}
{step_list([
    "<strong>End Time = 30:00:00:00</strong> — 30 วัน (วัน:ชม:นาที:วินาที)",
    "<strong>Failed 9.99%</strong> — ใกล้ 10% ที่ตั้งไว้",
    "<strong>Working 90.01%</strong> — FG 233,314 ชิ้น = 324 ชิ้น/ชม. = 360 × 90%",
])}
<div class="note"><strong>สรุป:</strong> ผลที่มีการสุ่ม ต้องรันนานพอ หรือรันหลายรอบแล้วเฉลี่ย ก่อนนำไปตัดสินใจ
— Model5 ตั้งเหมือน Model4 ทุกอย่าง ต่างแค่ End Time รันแบบไม่มีภาพเคลื่อนไหวใช้เวลาไม่กี่วินาที</div>

<h3>รันสั้น vs รันยาว (Station3 Availability 90%)</h3>
<table>
<tr><th>เวลาจำลอง</th><th>เครื่องเสียที่วัดได้</th><th>FG ต่อชั่วโมง</th><th>อ่านว่า</th></tr>
<tr><td>8 ชม. (Model4)</td><td>13.6%</td><td>310.5</td><td>สั้นไป สุ่มเจอเสียมาก</td></tr>
<tr><td>24 ชม. (Model4, End 24:00:00)</td><td>9.1%</td><td>327.0</td><td>ยังแกว่ง</td></tr>
<tr><td>30 วัน (Model5)</td><td>10.0%</td><td>324.0</td><td>นิ่ง = 360 × 90%</td></tr>
<tr><td>ไม่มีเครื่องเสีย (Model3, 8 ชม.)</td><td>0%</td><td>359.4</td><td>ฐานเปรียบเทียบ</td></tr>
</table>

<h2>สรุป 5 Frame</h2>
<table>
<tr><th>Frame</th><th>ตั้งค่า</th><th>เวลาจำลอง</th><th>ผลผลิต</th><th>Station ทำงาน</th></tr>
<tr><td><code>Model</code></td><td>เวลาสุ่ม 0:05–0:15 ต่อเครื่องตรงกัน</td><td>1 ชม.</td><td><strong>276</strong> ชิ้น/ชม.</td><td>76–79%</td></tr>
<tr><td><code>Model2</code></td><td>+ Buffer ความจุ 3 ชิ้น</td><td>1 ชม.</td><td><strong>337</strong> ชิ้น/ชม.</td><td>91–97%</td></tr>
<tr><td><code>Model3</code></td><td>เวลาคงที่ 0:10 ไม่มีเครื่องเสีย</td><td>8 ชม.</td><td><strong>2,875</strong> ชิ้น</td><td>~100%</td></tr>
<tr><td><code>Model4</code></td><td>Station3 Availability 90% MTTR 5:00</td><td>8 ชม.</td><td><strong>2,484</strong> ชิ้น</td><td>86%</td></tr>
<tr><td><code>Model5</code></td><td>เหมือน Model4</td><td>30 วัน</td><td><strong>324</strong> ชิ้น/ชม.</td><td>90%</td></tr>
</table>
<p>เทียบกับเวลาคงที่ 0:10 ไม่มีเครื่องเสีย (บท 02) ได้ 355 ชิ้น/ชม. — เวลาสุ่มเสียไป 79 ชิ้นต่อชั่วโมง Buffer ดึงกลับมาได้ 61 ชิ้น
ส่วนเครื่องเดียวเสีย 10% ทั้งไลน์ก็เสีย 10% เพราะไม่มีที่พักงาน</p>

<h2>ลองเอง</h2>
<p>แก้ทีละแถวจากค่าเดิม และกด Reset ก่อน Start ทุกครั้ง</p>
<h3>ลองเอง 1: Buffer และเวลาสุ่ม (Model, Model2)</h3>
<table>
<tr><th>Frame</th><th>ลองเปลี่ยน</th><th>FG หลังรัน</th><th>ทำไม</th></tr>
<tr><td><code>Model2</code></td><td>Buffer1–4 Capacity = 1</td><td><strong>320</strong></td><td>พักได้น้อย ช่วยได้บางส่วน</td></tr>
<tr><td><code>Model2</code></td><td>Buffer1–4 Capacity = 10</td><td><strong>339</strong></td><td>มากกว่า 3 ได้เพิ่มแค่ 2 ชิ้น</td></tr>
<tr><td><code>Model2</code></td><td>ทุก Station เวลา Const 0:10</td><td><strong>355</strong></td><td>เวลาไม่ผันแปร Buffer ไม่ได้ช่วยเพิ่ม</td></tr>
<tr><td><code>Model</code></td><td>Uniform 0:08–0:12 (ช่วงแคบลง)</td><td><strong>320</strong></td><td>ผันแปรน้อย เสียน้อยลง</td></tr>
</table>
<div class="note"><strong>แถวที่ 3 สำคัญ:</strong> Buffer ช่วยเมื่อเวลาผันแปรเท่านั้น ถ้าเวลาคงที่ให้แก้ที่คอขวดแบบ<a href="basic-02.html">บท 02</a></div>

<h3>ลองเอง 2: เปลี่ยนเครื่องเสียแล้วดูผล (Model4, Model5)</h3>
<table>
<tr><th>Frame</th><th>ลองเปลี่ยนที่ Station3</th><th>ผลหลังรัน</th><th>อ่านว่า</th></tr>
<tr><td><code>Model5</code></td><td>Availability = 95%</td><td><strong>341.5</strong> ชิ้น/ชม.</td><td>เสีย 5%</td></tr>
<tr><td><code>Model5</code></td><td>Availability = 80%</td><td><strong>289.0</strong> ชิ้น/ชม.</td><td>เสีย 20%</td></tr>
<tr><td><code>Model5</code></td><td>MTTR = 0:30 (เสียบ่อย สั้น)</td><td><strong>324.3</strong> ชิ้น/ชม.</td><td>เท่าเดิม เมื่อไม่มี Buffer</td></tr>
<tr><td><code>Model5</code></td><td>MTTR = 30:00 (เสียน้อย นาน)</td><td><strong>322.1</strong> ชิ้น/ชม.</td><td>ใกล้เคียงเดิม</td></tr>
<tr><td><code>Model4</code></td><td>MTTR = 0:30 (8 ชม.)</td><td><strong>2,583</strong> ชิ้น</td><td>ต่างจาก 2,484 เพราะการสุ่ม</td></tr>
</table>
<p>แถว MTTR แสดงว่าในระยะยาว ผลขึ้นกับ Availability ไม่ใช่ MTTR เมื่อไลน์ไม่มี Buffer</p>

<h2>ปัญหาที่พบบ่อย และวิธีแก้</h2>
<table>
<tr><th>อาการ</th><th>วิธีแก้</th></tr>
<tr><td>รันซ้ำแล้วผลเท่าเดิมทุกครั้ง</td><td>ปกติ: ตัวเลขสุ่มเริ่มจากค่า seed เดิม เปลี่ยนได้ที่ <code>File › Options</code></td></tr>
<tr><td>Buffer เต็ม / ว่างตลอดเวลา</td><td>เต็ม = เครื่องถัดไปช้ากว่างานที่เข้า · ว่าง = งานเข้าช้ากว่าที่เครื่องถัดไปทำได้</td></tr>
<tr><td>ใส่ Buffer แล้ว FG ไม่เพิ่ม</td><td>ถ้าเวลาคงที่ Buffer ไม่ช่วย ให้หาคอขวดแบบบท 02</td></tr>
<tr><td>ไม่รู้ว่าไอคอนไหนคือ Buffer</td><td>เลื่อนเมาส์ไปชี้ไอคอนใน Toolbox จะเห็นชื่อ</td></tr>
<tr><td>ตั้ง Availability แล้วเครื่องไม่เสีย</td><td>ตรวจช่อง Active ในแท็บ Failures ทั้งช่องบนและในตาราง</td></tr>
<tr><td>เครื่องเสีย % ไม่ตรงที่ตั้ง</td><td>รันนานขึ้น (30 วันได้ 9.99%) หรือรันหลายรอบแล้วเฉลี่ย</td></tr>
<tr><td>หาปุ่ม OEE ไม่เจอ</td><td>ไม่มี ให้คำนวณจากแท็บ Statistics: A × P × Q</td></tr>
<tr><td>3D Chart ว่างหลังรัน</td><td>รันด้วยปุ่ม Start แบบมีภาพเคลื่อนไหว</td></tr>
</table>

<div class="note">
<strong>คำถามฝึกคิด:</strong> หัวหน้าเห็นผล Model4 (รัน 8 ชม.) แล้วสรุปว่า "Station3 เสีย 13.6% ต้องรีบเปลี่ยนเครื่อง" ควรตอบอย่างไร?
</div>
<div class="tip"><strong>เฉลย:</strong> 8 ชั่วโมงสั้นเกินไปสำหรับเหตุการณ์สุ่ม ตัวเลขยังแกว่ง (24 ชม. ได้ 9.1%, 30 วันได้ 10.0%)
ควรรันนานพอหรือรันหลายรอบแล้วเฉลี่ยก่อน — ค่าที่ตั้งไว้คือเสีย 10% และในระยะยาวทั้งไลน์จะเสียผลผลิตประมาณ 10% ตาม
เพราะไม่มีที่พักงานรอบ Station3</div>
'''

BODY[("basic", "04")] = planned_body([
    "Workplace ข้างเครื่อง + WorkerPool + Broker ต่อกันอย่างไร",
    "ให้ Station ต้องใช้คนทำงาน แล้วดูคนเดินระหว่างเครื่อง",
    "คน 2 คนดูแล 5 เครื่อง → ผลผลิตลด ใครรอใคร",
    "ShiftCalendar: 2 กะ + เวลาพัก แล้วดูผลต่อวัน",
    "Worker chart / สถิติของคน (ทำงาน เดิน รอ)",
], "<code>Model</code> ไม่มีคน · <code>Model2</code> คน 2 คน · <code>Model3</code> คน 2 คน + ShiftCalendar 2 กะ")

BODY[("basic", "05")] = planned_body([
    "สร้าง MU 3 รุ่น (A / B / C) ใน Class Library สีต่างกัน",
    "Source ปล่อยงานตามตาราง (DataTable: รุ่น, จำนวน)",
    "Station ใช้เวลาต่างกันตามรุ่น",
    "Station5 ส่งงานดี 95% ไป Drain และงานเสีย 5% ไป Rework",
    "Method แรก: นับงานเสียลง Variable แล้วแสดงบน Display",
    "Sankey Diagram ดูทางเดินของงาน",
], "<code>Model</code> 1 รุ่น · <code>Model2</code> 3 รุ่นตามตาราง · <code>Model3</code> + งานเสีย / Rework + Method",
'<div class="tip">บทนี้เป็นบทแรกที่เขียนโค้ด SimTalk (Method 5–10 บรรทัด) — ดูพื้นฐาน syntax ได้ที่ <a href="advanced-01.html">Advanced บทที่ 1</a></div>')

BODY[("basic", "06")] = planned_body([
    "มุมมอง 3D ของไลน์ และการแก้โครงสร้าง 3D",
    "วางผังโรงงาน: Import DWG หรือ Textured Plate (รูปผังพื้น) พร้อมปรับความโปร่งใส",
    "เปลี่ยนรูปวัตถุ (Exchange Graphics / Import Graphic)",
    "คลังวัตถุดิบ + AGV ขนเข้า Station1",
    "เพิ่ม AGV เป็น 2 คัน แล้วเทียบผลผลิตและ utilization ของ AGV",
    "Conveyor — ลำเลียงชิ้นงานระหว่างเครื่อง",
], "<code>Model</code> ไลน์บนผัง ไม่มี AGV · <code>Model2</code> AGV 1 คัน · <code>Model3</code> AGV 2 คัน")

BODY[("basic", "07")] = planned_body([
    "Bottleneck Analyzer บนไลน์ของบท 06 (Show Analysis, Ranking)",
    "ExperimentManager: Output = ผลผลิต, Input = ขนาด Buffer + จำนวนคน (หรือ AGV)",
    "รันการทดลอง อ่านตาราง Report และกราฟ",
    "เลือกค่าที่คุ้ม (ผลผลิตที่เพิ่ม เทียบเงินที่ต้องลงทุน) และสรุปเพื่อคุยกับผู้บริหาร",
    "ทางต่อ: GA (GAWizard) เมื่อตัวแปรเยอะ",
], "<code>Model</code> ไลน์ + Bottleneck Analyzer · <code>ExperimentManager</code>",
'<div class="tip"><strong>อยากลองก่อน:</strong> เครื่องมือชุดเดียวกันนี้ (Bottleneck Analyzer, Ranking, Experiment Manager, Energy Analyzer) '
'ได้ลองใช้ครบทีละขั้นบนโมเดลตัวอย่างของ Siemens แล้วในบท <a href="basic-00b.html">00B Small Parts Production</a> '
'— บทนี้จะใช้เครื่องมือเดิมกับไลน์ 5 สถานีที่สร้างเองมาตลอดชุด</div>')

BODY[("intermediate", 1)] = '''
<h2>Object ขั้นกลางที่ใช้บ่อย</h2>
<table>
<tr><th>Object</th><th>ใช้ทำอะไร</th><th>ต่างจากตัวพื้นฐานอย่างไร</th></tr>
<tr><td><strong>Buffer</strong></td><td>พักชิ้นงานแบบ FIFO เรียบง่าย</td><td>เทียบกับ Store: Buffer ไม่มีตำแหน่งจัดเก็บย่อย เข้าก่อนออกก่อนเสมอ</td></tr>
<tr><td><strong>Store</strong></td><td>พักชิ้นงานแบบมีตำแหน่ง/ชั้นวางย่อย ดึงออกไม่ต้องเรียงลำดับ</td><td>เหมาะจำลองคลังสินค้า/ชั้นวางจริงที่หยิบสินค้าจากตำแหน่งใดก็ได้</td></tr>
<tr><td><strong>AssemblyStation</strong></td><td>รวมชิ้นงานจากหลายทางเข้าเป็นชิ้นเดียว (เช่น ประกอบชิ้นส่วน A+B)</td><td>Station รับ-ส่งทางเดียว แต่ AssemblyStation รอครบทุกอินพุตก่อนประมวลผล</td></tr>
<tr><td><strong>Track</strong></td><td>เส้นทางที่ให้ Transporter วิ่งบนนั้น (ต่างจาก Conveyor ที่ขนส่งอัตโนมัติ)</td><td>ใช้คู่กับ Transporter เพื่อจำลองรถขนส่ง/AGV ที่ขับเคลื่อนเอง</td></tr>
<tr><td><strong>Transporter</strong></td><td>พาหนะขนส่งชิ้นงานที่ขับเคลื่อนไปมาเองบน Track (อยู่ในหมวด MU ไม่ใช่ MaterialFlow)</td><td>ต่างจาก Conveyor ตรงที่ Transporter เป็นวัตถุเดี่ยวที่ต้องวิ่งไปรับ-ส่งเอง ไม่ใช่สายพานตายตัว</td></tr>
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
ที่ลากไปวางบน Frame ได้โดยตรงแบบ Source/Station — ถ้าอยากปรับแต่งคุณสมบัติของ MU (เช่น ตั้งชื่อ, สี, น้ำหนักเริ่มต้น)
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
<strong>คำถามฝึกคิด:</strong> ทำไมลาก <code>.MUs.Part</code> ไปวางบน Frame ตรงๆ ไม่ได้เหมือน Source/Station?
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
<li>ดับเบิลคลิก Object (เช่น Source หรือ Station) เพื่อเปิด Attribute window</li>
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
<li>ดับเบิลคลิกที่ Object ประเภทประมวลผล (เช่น Station) → ไปแท็บ <strong>Failures</strong></li>
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
<li>เลือก Object หลายตัวที่ต้องการห่อรวมกัน (เช่น Buffer + Station + สถิติที่เกี่ยวข้อง)</li>
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
<p>Object ประเภทประมวลผล (เช่น Station) มีช่อง <code>ExecuteAt.Entrance</code> และ <code>ExecuteAt.Exit</code>
ให้กำหนด Method ที่จะทำงานอัตโนมัติทุกครั้งที่มีชิ้นงานเข้า/ออกจากสถานีนั้น</p>
<ol class="steps">
<li>สร้าง Method object ในหมวด <code>InformationFlow</code> ตั้งชื่อ เช่น <code>OnEntry</code></li>
<li>เขียนโค้ดใน Method นั้น</li>
<li>ที่ Object เป้าหมาย (เช่น Station) เปิด Attribute → ช่อง <code>ExecuteAt.Entrance</code> → กำหนดให้ชี้ไปที่ Method <code>OnEntry</code></li>
<li>รันซิมูเลชัน — Method จะถูกเรียกอัตโนมัติทุกครั้งที่มีชิ้นงานเข้าสถานี ไม่ต้องเรียกเองด้วยมือ</li>
</ol>

<h2>เข้าถึงชิ้นงาน (MU) ปัจจุบัน</h2>
<p>ภายใน Method ที่ผูกกับเหตุการณ์แบบนี้ ตัวแปรพิเศษ <code>@</code> อ้างอิงถึง MU (ชิ้นงาน) ที่กำลังผ่านสถานีอยู่ขณะนั้น</p>
<pre><code>->void;
var mu := @
print "MU " + mu.Name + " entered station"</code></pre>

<h2>ทำงานเป็นระยะเวลาซ้ำๆ โดยไม่ผูกกับเหตุการณ์ของ Object อื่น</h2>
<div class="note"><strong>ข้อควรรู้เรื่องเวอร์ชัน:</strong> Plant Simulation รุ่นปัจจุบัน (ตรวจสอบแล้วกับ V2606) ไม่มี Object
แยกต่างหากชื่อ <code>Trigger</code> อยู่ใน Class Library หมวด <code>InformationFlow</code> อีกต่อไป — เป็นชื่อจากเวอร์ชันเก่า</div>
<p>การให้ Method ทำงานซ้ำตามรอบเวลาคงที่ (ไม่ผูกกับเหตุการณ์ Entrance/Exit ของ Object อื่น) ทำได้โดยให้ Method เรียกตัวเองใหม่
อีกครั้งหลังจากดีเลย์ที่ต้องการผ่านกลไกจัดตารางเวลาของ EventController — ดูรายละเอียด syntax ที่แน่นอนได้จาก Help Manual
ในเครื่อง (หัวข้อ Method scheduling) ก่อนใช้งานจริง เพื่อให้แน่ใจว่าตรงกับเวอร์ชันที่ติดตั้งอยู่</p>

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

<h2>Conveyor</h2>
<p>สายพานลำเลียงระหว่างสถานี มีความเร็ว/ความยาวจำลองเวลาขนส่งจริง ต่างจากการเชื่อม Object ตรงๆ ที่ไม่มีเวลาขนส่งเลย</p>
<div class="tip"><strong>ลองสาธิต:</strong> เพิ่ม Conveyor ยาว 50m ความเร็ว 1m/s คั่นกลาง Source-Drain จะเห็นชิ้นงานใช้เวลาประมาณ 50 วินาทีบน Conveyor ก่อนถึง Drain</div>

<h2>Station</h2>
<p>สถานีประมวลผล 1 หัว ควบคุมด้วย <code>ProcTime</code> — ดูรายละเอียดเต็มที่ <a href="basic-01.html">Basic บทที่ 01</a></p>

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

<h2>Sorter</h2>
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

<h2>เรียก Method ซ้ำตามรอบเวลา</h2>
<p>ไม่มี Object แยกต่างหากชื่อ Trigger ในเวอร์ชันปัจจุบันแล้ว (ชื่อจากเวอร์ชันเก่า) — ทำ Method ให้ทำงานซ้ำตามรอบเวลาโดยไม่ต้องผูกกับ
เหตุการณ์ของ Object อื่นได้ผ่านกลไกจัดตารางเวลาของ EventController แทน — ดู <a href="advanced-02.html">Advanced บทที่ 2</a></p>
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

BODY[("step-by-step", 1)] = '''
<p class="lead" style="max-width:46em;">อ้างอิงเฟรม <code>Model_Station</code> และ <code>Model_ParallelStation</code> จากไฟล์สอนต้นฉบับของ Siemens —
Object พื้นฐานที่สุดที่ต้องรู้ก่อนสร้างโมเดลจำลองการผลิตแรก ดูรายละเอียด Object แต่ละตัวเต็มๆ ได้ที่
<a href="basic-01.html">Basic บทที่ 01</a></p>

<div class="note">
<strong>Object ในเฟรมต้นฉบับ:</strong> <code>Model_Station</code> มี EventController, Source ×2, Station ×6, Drain ×2,
Display ×3, Chart, Connector ×8 — <code>Model_ParallelStation</code> มี EventController, Source ×2, Conveyor,
ParallelStation ×4, Buffer, Drain, Display ×4, Chart, Connector ×7
</div>

<h2>สายการผลิตต่อเนื่องหลายสถานี</h2>
<p>ในเฟรม <code>Model_Station</code> นอกจากสาย <code>Source → Station → Drain</code> เดี่ยวๆ แล้ว ยังมีสายที่ต่อ Station
ถึง 4 ตัวเรียงกัน (<code>Source1 → Station1 → Station2 → Station3 → Drain1</code>) เพื่อสาธิตว่าสายการผลิตจริงมักมีหลายสถานี
ต่อเนื่องกัน ไม่ใช่แค่สถานีเดียว — ผลลัพธ์ Throughput รวมของสายจะถูกจำกัดด้วยสถานีที่ช้าที่สุดในสาย (คอขวด)</p>

<h2>เมื่อ Station เดียวไม่พอ: ParallelStation</h2>
<p>เฟรม <code>Model_ParallelStation</code> สาธิตทางเลือกเมื่อจุดหนึ่งในสายการผลิตต้องมี "เครื่องจักรทำงานแบบเดียวกันหลายเครื่อง
พร้อมกัน" แทนที่จะวาง Station หลายตัวแล้วต้องมี Sorter แยกเส้นทางเอง <strong>ParallelStation</strong> คือ Object เดียวที่มีคิว
รับงานได้จากหลายเครื่องจักรภายในตัวมันเอง กำหนดจำนวน "เครื่อง" ในตัวเดียวได้ที่แท็บ Attributes</p>

<table>
<tr><th>Object เพิ่มเติมในเฟรมนี้</th><th>ใช้ทำอะไร</th></tr>
<tr><td><strong>Conveyor</strong></td><td>ลำเลียงชิ้นงานแบบต่อเนื่อง (มีความเร็ว/ความยาว) ต่างจาก Connector ที่เป็นแค่เส้นเชื่อมตรรกะ</td></tr>
<tr><td><strong>Buffer</strong></td><td>จุดพักชิ้นงานแบบมีความจุจำกัด เมื่อสถานีถัดไปไม่ว่าง</td></tr>
</table>

<div class="tip"><strong>คำถามฝึกคิด:</strong> ถ้ามี Station เดี่ยว 3 ตัวขนานกัน (ต้องมี Sorter + Connector เชื่อมแยก 3 เส้น)
เทียบกับ ParallelStation 1 ตัวที่ตั้งค่า 3 เครื่องภายใน อะไรต่างกัน?<br><br>
<strong>เฉลย:</strong> ผลลัพธ์ Throughput ใกล้เคียงกัน แต่ ParallelStation สร้าง/แก้ไขง่ายกว่ามาก (ไม่ต้องวาง Sorter หรือคุม
Connector หลายเส้น) เหมาะกับกรณีเครื่องจักรเหมือนกันทุกประการ ส่วน Station เดี่ยวหลายตัวเหมาะกับกรณีที่แต่ละเครื่องมีเงื่อนไข/เวลา
ไม่เท่ากัน</div>
'''

BODY[("step-by-step", 2)] = '''
<p class="lead" style="max-width:46em;">อ้างอิงเฟรม <code>Model_Chart</code>, <code>Model_Data_Table</code>, <code>Model_OEE</code>,
<code>Model_EnergyAnalyzer</code> — อ่านผลลัพธ์การจำลอง จัดเก็บข้อมูลด้วยตาราง และคำนวณ OEE / พลังงาน</p>

<div class="note">
<strong>Object ในเฟรมต้นฉบับ:</strong> <code>Model_Chart</code> มี Chart ×3, Display ×4 — <code>Model_Data_Table</code>
เพิ่ม DataTable <strong>ORDER</strong>/<strong>CT</strong>/<strong>ST</strong> — <code>Model_OEE</code> เพิ่ม Display
สำหรับ Availability/Performance/Quality/OEE — <code>Model_EnergyAnalyzer</code> ฝังเฟรมย่อย EnergyAnalyzer และ GAWizard
</div>

<h2>Chart หลายตัว ตอบคนละคำถาม</h2>
<p>เฟรม <code>Model_Chart</code> มี Chart ถึง 3 ตัวเพราะ Chart หนึ่งตัวแสดงได้แค่มุมมองเดียว — ต้องแยก Chart ตามคำถามที่อยาก
ตอบ เช่น สัดส่วนเวลา Working/Waiting/Blocked ของ Station, จำนวนชิ้นงานสะสมที่ Drain ตามเวลา, และปริมาณ WIP ใน Buffer</p>
<div class="tip"><strong>Tip:</strong> ใช้ Display คู่กับ Chart เสมอสำหรับตัวเลขที่ต้องอ่านแม่นยำ (เช่น Throughput สะสม) —
Chart เหมาะกับ "แนวโน้ม/สัดส่วน" ส่วน Display เหมาะกับ "ตัวเลขล่าสุด"</div>

<h2>DataTable — ขับเคลื่อนโมเดลด้วยข้อมูล</h2>
<table>
<tr><th>ตาราง</th><th>ความหมาย</th></tr>
<tr><td><strong>ORDER</strong></td><td>รายการคำสั่งผลิต — ชนิดชิ้นงาน/จำนวนที่ต้องผลิตในแต่ละรอบ</td></tr>
<tr><td><strong>CT</strong> (Cycle Time)</td><td>เวลาแปรรูปของแต่ละชนิดชิ้นงานที่แต่ละสถานี</td></tr>
<tr><td><strong>ST</strong> (Setup Time)</td><td>เวลาปรับตั้งเครื่องเมื่อเปลี่ยนชนิดชิ้นงาน</td></tr>
</table>
<p>แทนที่จะพิมพ์เวลาแปรรูปตายตัวใน Station แต่ละตัว ให้ Station ดึงค่าจากตารางตามชนิดชิ้นงานที่กำลังประมวลผล — bracket
indexing ตัวเดียวกับที่สอนใน <a href="advanced-03.html">Advanced บทที่ 3</a>:</p>
<pre><code>->void;
var partType := @.PartType
Station.procTime := CT[partType, Station.name]</code></pre>
<div class="note"><strong>ทำไมต้องทำแบบนี้:</strong> เมื่อมีหลายชนิดชิ้นงาน การแก้ไขเวลาแปรรูปทำที่ตารางเดียว ไม่ต้องไล่แก้ทีละ
Station — เป็นพื้นฐานสำคัญก่อนไปบทที่ 8 (Optimization) ที่ต้องปรับค่าจากภายนอกโมเดลได้</div>

<h2>OEE — Overall Equipment Effectiveness</h2>
<table>
<tr><th>องค์ประกอบ</th><th>ความหมาย</th></tr>
<tr><td>Availability</td><td>สัดส่วนเวลาที่เครื่องพร้อมทำงาน (ไม่รวมเวลาหยุดเสีย/ตั้งเครื่อง)</td></tr>
<tr><td>Performance</td><td>สัดส่วนความเร็วจริงเทียบกับความเร็วสูงสุดที่ออกแบบไว้</td></tr>
<tr><td>Quality</td><td>สัดส่วนชิ้นงานดีเทียบกับชิ้นงานทั้งหมดที่ผลิต</td></tr>
<tr><td>OEE</td><td>Availability × Performance × Quality — ตัวชี้วัดประสิทธิภาพรวม</td></tr>
</table>
<p>OEE คำนวณจาก Statistics ของ Station โดยตรงผสมกับจำนวนชิ้นงานดี/เสียที่นับได้จาก Drain สองตัวในเฟรมนี้ ไม่จำเป็นต้องมี
Object พิเศษเพิ่ม — ใช้ Method คำนวณสามค่าแล้วคูณกันได้เลย</p>

<h2>EnergyAnalyzer — วิเคราะห์การใช้พลังงาน</h2>
<p>เฟรม <code>Model_EnergyAnalyzer</code> ฝัง Object เครื่องมือ <strong>EnergyAnalyzer</strong> ไว้เป็นเฟรมย่อย ใช้ประเมิน
พลังงานที่ใช้ในแต่ละสถานะของเครื่องจักร (Working/Standby/Off) เหมาะสำหรับวิเคราะห์ต้นทุนพลังงานควบคู่กับ Throughput ก่อน
ตัดสินใจเพิ่ม/ลดจำนวนเครื่องจักร เฟรมนี้ยังฝัง GAWizard ไว้ด้วย เป็นจุดเริ่มก่อนเข้าเนื้อหาเต็มที่
<a href="step-by-step-08.html">บทที่ 8: Optimization ด้วย GAWizard</a></p>

<div class="tip"><strong>คำถามฝึกคิด:</strong> ถ้า OEE ของสถานีหนึ่งต่ำ ควรดูค่าไหนก่อน (A, P, หรือ Q) เพื่อรู้ว่าปัญหาหลักคืออะไร?
<br><br><strong>เฉลย:</strong> ดูทั้งสามค่าแยกกันเสมอ — A ต่ำมักบ่งชี้ปัญหาการหยุดเครื่อง/รอวัตถุดิบ, P ต่ำบ่งชี้เครื่องทำงานช้ากว่าที่
ออกแบบ, Q ต่ำบ่งชี้ปัญหาคุณภาพต้นทาง — ค่า OEE รวมค่าเดียวไม่บอกว่าควรแก้ตรงไหนก่อน</div>
'''

BODY[("step-by-step", 3)] = '''
<p class="lead" style="max-width:46em;">อ้างอิงเฟรม <code>Model_Assembly</code> และ <code>Model_Sorter_and_Store</code> — รวมชิ้นงานหลายชิ้นเป็นหนึ่ง
แยกชิ้นงานออกจากกัน และจัดเก็บ/คัดแยกตามเงื่อนไข</p>

<div class="note">
<strong>Object ในเฟรมต้นฉบับ:</strong> <code>Model_Assembly</code> มี Source ×2, AssemblyStation, DismantleStation,
Buffer ×2, เฟรมย่อย ExperimentManager — <code>Model_Sorter_and_Store</code> มี Source ×4, Store ×3, Sorter,
AssemblyStation, Connector ×17
</div>

<h2>AssemblyStation — ประกอบชิ้นงานหลายชิ้นเป็นหนึ่ง</h2>
<p><strong>AssemblyStation</strong> รับชิ้นงานจากหลายเส้นทางเข้าพร้อมกัน (เช่น ตัวเรือน + ฝา + สกรู) แล้วรวมเป็นชิ้นงาน
ประกอบ 1 ชิ้นก่อนส่งออกทางเดียว ต่างจาก Station ทั่วไปที่มีทางเข้าทางเดียว — ต้องมีชิ้นงานจากทุกทางเข้าครบก่อนจึงจะเริ่มประกอบ</p>
<div class="note"><strong>ข้อควรระวัง:</strong> ถ้าเส้นทางใดเส้นทางหนึ่งขาดชิ้นงาน AssemblyStation จะรอเฉยๆ (ไม่ใช่ Error) —
ถ้า Throughput ต่ำผิดปกติ ให้เช็คว่าทุกเส้นทางป้อนชิ้นงานทันเวลาเท่ากันหรือไม่ นี่คือสาเหตุคอขวดที่พบบ่อยที่สุดของ AssemblyStation</div>

<h2>DismantleStation — แยกชิ้นงานที่ประกอบแล้ว</h2>
<p>ตรงข้ามกับ AssemblyStation — รับชิ้นงานประกอบ 1 ชิ้นเข้ามา แล้วแยกออกเป็นชิ้นส่วนย่อยส่งออกหลายทาง ในเฟรมนี้ใช้คู่กับ
AssemblyStation เพื่อสาธิตวงจรประกอบ → แยก</p>

<h2>Experiment Manager — เปรียบเทียบหลายสถานการณ์</h2>
<p>เฟรมย่อย ExperimentManager สาธิตการรันโมเดลเดียวกันหลายรอบด้วยค่าพารามิเตอร์ต่างกัน โดยไม่ต้องแก้ค่าแล้วรันทีละรอบเอง —
ดูขั้นตอนตั้งค่าเต็มๆ ที่ <a href="advanced-05.html">Advanced บทที่ 5</a> ซึ่งเป็นพื้นฐานก่อนไปถึง
<a href="step-by-step-08.html">GAWizard (บทที่ 8)</a> ที่ค้นหาค่าที่ดีที่สุดแทนการลองทีละ Scenario เอง</p>

<h2>Sorter และ Store — คัดแยกและจัดเก็บ</h2>
<p>เฟรม <code>Model_Sorter_and_Store</code> มี Source ถึง 4 ตัวป้อนชิ้นงานต่างชนิดกันเข้าสู่ <strong>Sorter</strong> ซึ่งแยก
เส้นทางตามเงื่อนไข (เช่นชนิดชิ้นงาน) ไปยัง <strong>Store</strong> 3 ตัวที่เก็บแยกตามประเภท ก่อนป้อนเข้า AssemblyStation อีก
ครั้งเพื่อประกอบจากของที่เก็บไว้</p>
<table>
<tr><th>Object</th><th>ต่างจาก Buffer อย่างไร</th></tr>
<tr><td><strong>Sorter</strong></td><td>ตัดสินใจ "ส่งไปทางไหน" ตามกฎ/Method ที่ผูกไว้ — Buffer ไม่มีการตัดสินใจ แค่พักคิว</td></tr>
<tr><td><strong>Store</strong></td><td>เก็บชิ้นงานแบบสุ่มเข้าถึงได้ (ไม่จำเป็นต้องเป็น FIFO เหมือน Buffer) และดึงออกตามเงื่อนไขได้</td></tr>
</table>

<div class="tip"><strong>คำถามฝึกคิด:</strong> ทำไม AssemblyStation ในเฟรมนี้ต้องรอรับจาก Store 3 ตัว (ไม่ใช่รับตรงจาก Source
เหมือนเฟรมก่อนหน้า)?<br><br><strong>เฉลย:</strong> เพราะ Source แต่ละตัวผลิตชิ้นส่วนไม่พร้อมกัน — ถ้าไม่มี Store พักไว้ก่อน
AssemblyStation จะรอชิ้นส่วนที่มาช้าที่สุดตลอดเวลา การมี Store เป็นบัฟเฟอร์เฉพาะประเภทช่วยให้ AssemblyStation หยิบของที่พร้อม
อยู่แล้วได้ทันที ลดเวลารอ</div>
'''

BODY[("step-by-step", 4)] = '''
<p class="lead" style="max-width:46em;">อ้างอิงเฟรม <code>Model_Basic_Worker</code>, <code>Model_Workers</code>, <code>Model_Worker_Service</code> —
เรียงความซับซ้อนจากน้อยไปมาก สาธิตการจำลองคนงานที่ต้องใช้ร่วมกันระหว่างหลายสถานี ดูภาพรวม Object กลุ่มนี้เพิ่มที่
<a href="object-reference-03.html">Object Reference บทที่ 3</a></p>

<h2>สามชิ้นส่วนของระบบแรงงาน</h2>
<table>
<tr><th>Object</th><th>หน้าที่</th></tr>
<tr><td><strong>WorkerPool</strong></td><td>"คลัง" คนงานที่มีอยู่ในระบบ — กำหนดจำนวนคนและกะการทำงานที่นี่</td></tr>
<tr><td><strong>Broker</strong></td><td>ตัวกลางจับคู่ระหว่างคำขอแรงงานจาก Workplace กับคนงานว่างใน WorkerPool</td></tr>
<tr><td><strong>Workplace</strong></td><td>จุดที่ผูกกับ Station ซึ่งต้องมีคนงานอยู่ด้วยจึงจะเริ่มประมวลผลได้</td></tr>
</table>
<p>ทั้งสามตัวทำงานร่วมกันเสมอเป็นชุด — ถ้าลืม Broker คนงานใน WorkerPool จะไม่ถูกจ่ายงานให้ Workplace เลย</p>

<h2>Model_Basic_Worker — จุดเริ่มต้น</h2>
<p>เฟรมนี้มี Station เดียวกับ Workplace เดียว: คนงาน 1 คนจาก WorkerPool ถูก Broker ส่งไปช่วยที่ Workplace เมื่อมีชิ้นงานมาถึง
รันแล้วสังเกตว่า Station จะ "รอคนงาน" (Waiting on Worker) ก่อนเริ่มประมวลผลทุกครั้งที่มีชิ้นงานใหม่เข้ามา</p>

<h2>Model_Workers — คนงานร่วมกันหลายสถานี</h2>
<p>เพิ่มจำนวน Station/Workplace เป็น 4-6 จุด แต่ WorkerPool ยังมีจำนวนคนงานจำกัด — สาธิตสถานการณ์จริงที่คนงานไม่พอสำหรับทุก
สถานีพร้อมกัน Broker ต้องตัดสินใจว่าจะส่งคนงานไปช่วยจุดไหนก่อน</p>
<div class="tip"><strong>Tip:</strong> ถ้า Throughput ต่ำกว่าที่คาด ให้เช็คสถิติของ Broker ก่อน — มักเป็นเพราะจำนวนคนงานใน
WorkerPool น้อยเกินไปเทียบกับจำนวนจุดที่ต้องการพร้อมกัน ไม่ใช่ปัญหาที่ Station เอง</div>

<h2>Model_Worker_Service — คนงานเดินบริการหลายจุด</h2>
<p>รูปแบบซับซ้อนที่สุด: คนงานไม่ได้ประจำอยู่กับ Station เดียวตลอดกะ แต่เดินไปมาให้บริการหลายสถานีตามคิวที่เกิดขึ้นจริง
(roaming service) เหมาะจำลองสถานการณ์เช่น ช่างเทคนิคที่ดูแลหลายเครื่องจักร</p>

<div class="note"><strong>คำถามฝึกคิด:</strong> ทำไมไฟล์สอนถึงแยกเป็น 3 เฟรม (Basic_Worker → Workers → Worker_Service) แทนที่
จะรวมเป็นเฟรมเดียว?<br><br><strong>เฉลย:</strong> เพื่อแยกตัวแปรที่เพิ่มความซับซ้อนทีละตัว — จากคนงาน 1 คน/สถานีเดียว
ไปสู่คนงานจำกัดที่ต้องแบ่งกันหลายสถานี ไปสู่คนงานที่เดินบริการเชิงรุก ถ้าเรียนรวมทีเดียวจะแยกไม่ออกว่าพฤติกรรมไหนมาจาก Object ไหน</div>
'''

BODY[("step-by-step", 5)] = '''
<p class="lead" style="max-width:46em;">อ้างอิงเฟรม <code>Model_PickAndPlace</code>, <code>Model_AGV</code>, <code>Model_Basic_AMR</code> — แขนกลหยิบวาง
และยานพาหนะขนย้ายอัตโนมัติสองยุค (AGV แบบราง กับ AMR แบบอิสระ)</p>

<h2>PickAndPlace — แขนกลหยิบวาง</h2>
<p><strong>PickAndPlace</strong> ย้ายชิ้นงานจากจุดหนึ่งไปอีกจุดหนึ่งแบบไม่ต่อเนื่อง (หยิบ → เคลื่อนที่ → วาง) ต่างจาก Conveyor
ที่ลำเลียงต่อเนื่อง เฟรม <code>Model_PickAndPlace</code> มี 4 ชุดวางคู่กันสาธิตรูปแบบการใช้งานต่างกัน</p>
<div class="tip"><strong>Tip:</strong> เวลารวมของ PickAndPlace มักเป็นคอขวดที่มองข้าม เพราะแยกเป็น 3 ช่วงเวลา
(หยิบ+เคลื่อนที่+วาง) รวมกัน — ลองแตกดูทีละช่วงใน Statistics ก่อนสรุปว่าเครื่องจักรช้าไม่ใช่ที่แขนกล</div>

<h2>Track — AGV แบบเดินตามราง (ยุคเก่า)</h2>
<p>เฟรม <code>Model_AGV</code> ใช้ Object <strong>Track</strong> กำหนดเส้นทางเดินรถตายตัวบนพื้น แล้วให้ยานพาหนะวิ่งตาม
เส้นทางนั้น จุดขึ้น-ลงสินค้าทำผ่าน PickAndPlace ที่ผูกอยู่บน Track — เหมาะกับโรงงานที่เส้นทางขนย้ายคงที่ ไม่เปลี่ยนบ่อย
(กับดัก Destination/AutomaticRouting ที่พบบ่อยกับ Transporter ดูที่ <a href="advanced-04.html">Advanced บทที่ 4</a>)</p>

<h2>AGVPool + Marker — AMR แบบอิสระ (ยุคใหม่)</h2>
<p>เฟรม <code>Model_Basic_AMR</code> ใช้แนวคิดต่างจาก Track: <strong>Marker</strong> คือจุดอ้างอิงลอยตัวในพื้นที่ (ไม่ใช่
เส้นทางตายตัว) ส่วน <strong>AGVPool</strong> คือกลุ่มยานพาหนะที่คำนวณเส้นทางเดินไปมาระหว่าง Marker เองแบบไดนามิก</p>
<table>
<tr><th></th><th>Track</th><th>AGVPool + Marker</th></tr>
<tr><td>เส้นทาง</td><td>ตายตัว ต้องวาดไว้ล่วงหน้า</td><td>คำนวณเองระหว่าง Marker แต่ละจุด</td></tr>
<tr><td>ความยืดหยุ่น</td><td>ต่ำ — ย้ายจุดต้องแก้ Track</td><td>สูง — ย้าย Marker ได้อิสระ</td></tr>
<tr><td>เหมาะกับ</td><td>เส้นทางขนย้ายคงที่ ปริมาณสูง</td><td>ผังพื้นที่เปลี่ยนบ่อย</td></tr>
</table>
<p>เฟรมนี้ยังสาธิตรูปแบบ Method วงจรชีวิตมาตรฐาน 3 ตัว — <code>INIT</code>/<code>RESET</code>/<code>ENDSIM</code> —
ผูกกับจังหวะเริ่ม/รีเซ็ต/จบของ EventController พร้อมตัวแปร <code>Total_Distance</code> สะสมระยะทางที่ AMR วิ่งทั้งหมด</p>
<div class="note"><strong>รูปแบบนี้ใช้ซ้ำได้ทั่วไป:</strong> การผูก Method ชื่อ INIT/RESET/ENDSIM เข้ากับจังหวะของ
EventController ใช้ได้กับโมเดลไหนก็ได้ ไม่ใช่แค่ AMR — ดูการผูก Method กับเหตุการณ์เต็มๆ ที่
<a href="advanced-02.html">Advanced บทที่ 2</a></div>

<div class="tip"><strong>คำถามฝึกคิด:</strong> ถ้าต้องขยายโกดังเพิ่มโซนใหม่บ่อยๆ ควรเลือก Track หรือ AGVPool+Marker?
<br><br><strong>เฉลย:</strong> AGVPool + Marker เพราะแค่เพิ่ม Marker จุดใหม่โดยไม่ต้องวาดเส้นทางเชื่อมใหม่ทั้งหมด</div>
'''

BODY[("step-by-step", 6)] = '''
<p class="lead" style="max-width:46em;">อ้างอิงเฟรม <code>Model_Method</code> และ <code>Model_3D_Animation</code> — ควบคุมโมเดลด้วยโค้ด ผูก UI เข้ากับ
Method และสั่งภาพเคลื่อนไหว ดู syntax เต็มๆ ที่ <a href="advanced-01.html">Advanced บทที่ 1</a></p>

<h2>ผูก Method เข้ากับ UI — Button และ DropDownList</h2>
<table>
<tr><th>Object</th><th>ใช้ทำอะไร</th></tr>
<tr><td><strong>Button</strong></td><td>เรียก Method หนึ่งตัวเมื่อถูกคลิก — ผูกที่ Attribute <code>Method</code> ของปุ่ม</td></tr>
<tr><td><strong>DropDownList</strong></td><td>ให้ผู้ใช้เลือกค่าจากรายการ แล้วส่งค่าที่เลือกเข้า Method ผ่านตัวแปรที่ผูกไว้</td></tr>
</table>
<ol class="steps">
<li>ลาก Button จากหมวด UserInterface มาวางบน Frame</li>
<li>เปิด Attribute ของ Button → ช่อง Method → เลือก Method ที่สร้างไว้</li>
<li>เขียนโค้ดใน Method ตามพฤติกรรมที่ต้องการ เช่น เปลี่ยนอัตราการผลิตของ Source</li>
<li>ทำแบบเดียวกันกับ DropDownList โดยผูกค่าที่เลือกเข้าตัวแปร แล้วให้ Method อ่านค่านั้นไปใช้ต่อ</li>
</ol>
<div class="tip"><strong>Tip:</strong> ปุ่มสองปุ่มในเฟรมนี้มักใช้สาธิตคู่ Start/Stop หรือ Slow/Fast — แยก Method คนละตัวชัดเจน
ดีกว่ารวมไว้ใน Method เดียวแล้วเช็คเงื่อนไข เพราะดีบักง่ายกว่าเมื่อโมเดลใหญ่ขึ้น</div>

<h2>Model_3D_Animation — สั่งภาพเคลื่อนไหวด้วย Method</h2>
<p>เฟรมนี้มี Method เพียงตัวเดียวแต่ผูกกับสายการผลิตที่มีทั้ง Station และ PickAndPlace — สาธิตว่า Method ไม่ได้ใช้แค่คำนวณ
ค่าตัวเลข แต่ยังสั่งเปลี่ยนรูปลักษณ์/การหมุน/สีของ MU ในมุมมอง 3D ได้โดยตรงผ่าน Attribute ของ MU เอง ทำให้แอนิเมชันสื่อความ
หมายมากกว่าดูแค่ Object เคลื่อนที่เฉยๆ</p>
<div class="note"><strong>ทำไมสำคัญ:</strong> เมื่อพรีเซนต์โมเดลให้ผู้บริหารหรือลูกค้าดู ภาพเคลื่อนไหวที่สื่อความหมาย
(เช่น ชิ้นงานเปลี่ยนสีตอนผ่าน QC) ช่วยให้เข้าใจ Logic ได้เร็วกว่าตัวเลขสถิติล้วนๆ มาก</div>

<div class="tip"><strong>คำถามฝึกคิด:</strong> ควรผูก Method ไว้ที่ ExecuteAt.Entrance หรือ ExecuteAt.Exit ถ้าต้องการนับจำนวน
ชิ้นงานที่ "ผ่านสำเร็จ" ออกจากสถานี?<br><br><strong>เฉลย:</strong> ExecuteAt.Exit — เพราะชิ้นงานที่เข้า (Entrance) อาจยัง
ประมวลผลไม่เสร็จหรือถูกดีดออกเพราะ Error ได้ การนับที่จุดออกจริงเท่านั้นที่ยืนยันว่าสถานีทำงานสำเร็จกับชิ้นงานนั้นแล้ว</div>
'''

BODY[("step-by-step", 7)] = '''
<p class="lead" style="max-width:46em;">อ้างอิงเฟรม <code>Model_3D_Factory</code> — Object เฉพาะที่มีความหมายในมุมมอง 3 มิติเท่านั้น สำหรับเปลี่ยนทิศทาง/
ระดับความสูงของชิ้นงานบนสายพาน</p>

<h2>ทำไมต้องมี Object เฉพาะสำหรับ 3D</h2>
<p>ในมุมมอง 2D สายพานทุกเส้นวาดเป็นเส้นตรงหรือหักมุมได้อิสระโดยไม่ต้องมี Object พิเศษ แต่ในโรงงานจริง การเปลี่ยนทิศทาง/ระดับ
ของสายพานต้องใช้อุปกรณ์จริงซึ่งกินพื้นที่และเวลา — เฟรมนี้รวม Object ที่จำลองอุปกรณ์เหล่านั้นไว้ในที่เดียว</p>

<table>
<tr><th>Object</th><th>ใช้ทำอะไร</th></tr>
<tr><td><strong>AngularConverter</strong></td><td>เปลี่ยนทิศทางการไหลของชิ้นงานเป็นมุมที่กำหนด ระหว่างสายพานสองเส้น</td></tr>
<tr><td><strong>Turntable</strong></td><td>โต๊ะหมุนที่หมุนตัวชิ้นงานเองเพื่อเปลี่ยนทิศทางออก ชิ้นงานหยุดนิ่งบนโต๊ะระหว่างหมุน</td></tr>
<tr><td><strong>Turnplate</strong></td><td>คล้าย Turntable แต่มักใช้กรณีต้องหมุนพร้อมส่งต่อแบบต่อเนื่องมากกว่า</td></tr>
</table>
<p>ทั้งสามตัวอยู่ในหมวด MaterialFlow เช่นเดียวกับ Conveyor — วางแทรกระหว่างสองเส้นทางได้เหมือน Object ลำเลียงทั่วไป
ต่างกันแค่ตอนตั้งค่ามุม/ทิศทางที่ Attribute</p>

<ol class="steps">
<li>วาง Conveyor เส้นแรกเข้า AngularConverter หรือ Turntable</li>
<li>ตั้งค่ามุมการเปลี่ยนทิศทางที่ Attributes (เช่น 90° สำหรับเลี้ยวฉาก)</li>
<li>ต่อ Conveyor เส้นที่สองออกจากอุปกรณ์นั้นในทิศทางใหม่</li>
<li>สลับมุมมองเป็น 3D เพื่อตรวจสอบว่าชิ้นงานเปลี่ยนทิศทาง/หมุนตามที่ตั้งค่าจริง</li>
</ol>
<div class="tip"><strong>Tip:</strong> ในมุมมอง 2D อุปกรณ์เหล่านี้อาจดูเหมือนจุดเชื่อมธรรมดา — ต้องสลับไปมุมมอง 3D เพื่อตรวจสอบ
ว่าตั้งค่ามุม/ทิศทางถูกต้องจริง อย่าพึ่งพา 2D อย่างเดียวเมื่อใช้ Object กลุ่มนี้</div>

<p>เฟรมนี้ยังฝัง WorkerPool + Broker + Workplace (จาก <a href="step-by-step-04.html">บทที่ 4</a>) ไว้ด้วย เพื่อสาธิตโมเดล
ระดับใกล้เคียงโรงงานจริงที่ต้องผสมทั้งการขนย้าย 3 มิติและแรงงานคนในเฟรมเดียวกัน</p>

<div class="note"><strong>คำถามฝึกคิด:</strong> ทำไมควรตรวจสอบ Turntable/Turnplate ในมุมมอง 3D เสมอ ทั้งที่โปรแกรมรัน
ซิมูเลชันได้ปกติแม้ไม่เปิดมุมมอง 3D?<br><br><strong>เฉลย:</strong> ผลลัพธ์ตัวเลขถูกต้องได้แม้ตั้งค่าทิศทาง/มุมผิด เพราะ
Logic การไหลของชิ้นงานคำนวณแยกจากภาพ 3D — แต่ถ้านำโมเดลไปพรีเซนต์หรือใช้ตรวจสอบพื้นที่จริง มุมที่ผิดจะทำให้ข้อสรุปเรื่อง
พื้นที่หน้างานผิดพลาดโดยที่ตัวเลขไม่ฟ้องเลย</div>
'''

BODY[("step-by-step", 8)] = '''
<p class="lead" style="max-width:46em;">อ้างอิงเฟรม <code>Model_GAWizard</code> — ค้นหาลำดับ/พารามิเตอร์ที่ดีที่สุดโดยอัตโนมัติด้วย GAWizard แทนการลองทีละ
Scenario เอง เฟรมนี้รวมทุกอย่างจาก<a href="step-by-step-02.html">บทที่ 2</a> (DataTable + OEE) เข้ากับ GAWizard —
เป็นบทสรุปของไฟล์สอนทั้งไฟล์ ดูขอบเขต/วิธีตั้งค่า GAWizard ผ่าน GUI เต็มๆ ที่ <a href="advanced-06.html">Advanced บทที่ 6</a></p>

<h2>จาก Experiment Manager สู่ Genetic Algorithm</h2>
<p><a href="advanced-05.html">Experiment Manager</a> ให้ผู้ใช้กำหนด Scenario เองทีละชุดแล้วรันเปรียบเทียบ แต่เมื่อตัวแปรที่
ต้องปรับมีจำนวนมาก (เช่น ลำดับการผลิตของหลายรายการใน ORDER table) การไล่ลองเองทุก Scenario เป็นไปไม่ได้ในทางปฏิบัติ —
GAWizard สุ่มสร้างชุดคำตอบ ประเมินผล แล้ว "ผสมพันธุ์/กลายพันธุ์" คำตอบที่ดีที่สุดซ้ำหลายรอบจนได้คำตอบที่ดีขึ้นเรื่อยๆ</p>

<p>ในเฟรมนี้ ตัวแปรที่ GAWizard ปรับคือ<strong>ลำดับรายการใน DataTable ORDER</strong> — เชื่อมโยงตรงกับตาราง ORDER/CT/ST ที่
สอนไว้ใน<a href="step-by-step-02.html">บทที่ 2</a> — ส่วนค่า Fitness คำนวณจากผลลัพธ์ OEE/Throughput ที่ได้จริงหลังรันจำลอง
ด้วยลำดับนั้น</p>

<h2>ตัวดำเนินการทางพันธุกรรม (Genetic Operators)</h2>
<table>
<tr><th>ตัวดำเนินการ</th><th>ความหมาย</th></tr>
<tr><td><strong>Crossover</strong></td><td>ผสมคำตอบสองชุดที่ดีเข้าด้วยกันเป็นคำตอบใหม่ — ถ้าไม่ใช้เลย คำตอบใหม่จะเป็นสำเนาของพ่อแม่เฉยๆ</td></tr>
<tr><td><strong>Mutation</strong></td><td>สุ่มเปลี่ยนบางส่วนของคำตอบหลัง Crossover เพื่อไม่ให้ติดอยู่ที่คำตอบเดิมซ้ำๆ</td></tr>
<tr><td><strong>Inversion</strong></td><td>สลับลำดับบางช่วงในคำตอบ ใช้บ่อยกับปัญหาประเภทลำดับ (Sequence) แบบในเฟรมนี้</td></tr>
<tr><td><strong>Elitism</strong></td><td>เก็บคำตอบที่ดีที่สุดของแต่ละรุ่นไว้ไม่ให้หายไปโดยไม่ตั้งใจจาก Crossover/Mutation</td></tr>
</table>
<div class="note"><strong>ข้อควรระวัง (Elitism + การประเมินที่มีความสุ่ม):</strong> ถ้าค่า Fitness มาจากการรันจำลองที่มีความสุ่ม
อย่าเปิด Elitism แบบเข้มงวด — คำตอบหนึ่งอาจดูดีเพราะโชคช่วยในการสุ่มรอบนั้น แล้วฝังตัวอยู่ในประชากรหลายรุ่นทั้งที่จริงไม่ได้ดีที่สุด</div>

<h2>เงื่อนไขจบการค้นหา — จุดที่พลาดบ่อย</h2>
<p>GAWizard หยุดเมื่อ (1) ครบจำนวนรุ่นที่กำหนด (2) ค่า Fitness ที่ดีที่สุดผ่านเกณฑ์ที่ตั้งไว้ หรือ (3) ค่า Fitness เฉลี่ยผ่าน
เกณฑ์ที่ตั้งไว้</p>
<div class="tip"><strong>ข้อควรระวัง:</strong> ค่าเกณฑ์เริ่มต้นของเงื่อนไข (2)/(3) มักทำให้การค้นหาแบบ Maximize หยุดตั้งแต่
รุ่นแรก เพราะค่าเริ่มต้นต่ำเกินไปจนผ่านเกณฑ์ทันที — ถ้าการค้นหาจบเร็วผิดปกติ (รุ่นเดียวจบ) ให้เช็คค่าเกณฑ์ทั้งสองนี้ก่อนสงสัยว่า
Configuration Method ผิด</div>

<div class="tip"><strong>คำถามฝึกคิด:</strong> ทำไมเฟรมนี้ถึงต้องมี DataTable ORDER/CT/ST อยู่ด้วย ทั้งที่ GAWizard เป็นเครื่องมือ
คนละหมวด?<br><br><strong>เฉลย:</strong> เพราะ GAWizard ไม่ได้ "รู้" เรื่องการผลิตเอง — มันแค่ปรับค่าตามที่ตั้งไว้ (ในที่นี้คือ
ลำดับแถวใน ORDER) แล้วให้โมเดลรันจริงเพื่อวัดผล Data Table คือ "ช่องปรับค่า" ที่แท้จริง ส่วน Station/OEE คือ "ตัวชี้วัด"
ที่บอกว่าค่าที่ปรับนั้นดีแค่ไหน — ถ้าไม่มีระบบขับเคลื่อนด้วยตารางจากบทที่ 2 มาก่อน GAWizard จะไม่มีอะไรให้ปรับเลย</div>
'''

BODY[("case-study", 1)] = '''
<h2>บริบทอุตสาหกรรม</h2>
<p>สายการประกอบยานยนต์มีสถานีเรียงต่อกันหลายสิบสถานี แต่ละสถานีติดตั้งชิ้นส่วนต่างกัน (ประตู, เบาะ, ระบบไฟฟ้า ฯลฯ)
เวลาแปรรูปแต่ละสถานีต่างกันและมีการหยุดสายบ่อยจากปัญหาชิ้นส่วนขาด/เครื่องมือขัดข้อง</p>

<h2>โจทย์ตัวอย่าง</h2>
<p>โรงงานต้องการเพิ่ม Throughput จาก 40 เป็น 50 คัน/กะ โดยยังไม่อยากลงทุนสร้างสถานีใหม่ทั้งหมด — ต้องรู้ก่อนว่าจุดไหนคือคอขวดจริง</p>

<h2>โครงสร้างโมเดล</h2>
<ul>
<li>สาย Station เรียงต่อกัน 15-20 สถานี เชื่อมด้วย Conveyor (ดู <a href="basic-02.html">Basic บทที่ 02</a>)</li>
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
<li>Station ต่อกันจำลองสถานี Print Paste → Place Component → Reflow → AOI</li>
<li>ที่ AOI ใช้ Sorter แยกแผ่นที่ Reject ออกไปเข้าสถานี Rework แยกต่างหาก (<a href="object-reference-01.html">Object Reference: Material Flow</a>)</li>
<li>ตั้ง Failure ที่สถานี Place Component ให้ถี่กว่าสถานีอื่น (หัวจับชิ้นส่วนสึกบ่อย) (<a href="intermediate-04.html">Intermediate บทที่ 4</a>)</li>
<li>ใช้ Method ผูกกับ Sorter ตัดสินใจ Reject/Pass แบบสุ่มตามอัตราจริง (<a href="advanced-02.html">Advanced บทที่ 2</a>)</li>
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
<p>อย่าปล่อยชื่อดีฟอลต์ (<code>Station1</code>, <code>Station2</code>) ไว้นาน — เปลี่ยนเป็นชื่อสื่อความหมายทันทีที่วาง
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
    title = chapter_title(section, idx)
    label = chapter_label(section, idx)
    objs = OBJECTIVES[(section, idx)]
    objs_html = "\n".join(f"          <li>{o}</li>" for o in objs)
    body_content = BODY[(section, idx)].strip()
    numbers = chapter_numbers(section)

    # prev/next
    pos = numbers.index(idx)
    if pos > 0:
        prev_id = numbers[pos - 1]
        prev_href = chapter_filename(section, prev_id)
        prev_label = f"← ก่อนหน้า: {chapter_label(section, prev_id)}. {chapter_title(section, prev_id)}"
    else:
        prev_href = SECTIONS[section]["hub"]
        prev_label = f"← กลับหน้ารวมบท {SECTIONS[section]['label'].split(' — ')[0]}"

    if pos < len(numbers) - 1:
        next_id = numbers[pos + 1]
        next_href = chapter_filename(section, next_id)
        next_label = f"ถัดไป: {chapter_label(section, next_id)}. {chapter_title(section, next_id)} →"
    else:
        sec_idx = SECTION_ORDER.index(section)
        if sec_idx < len(SECTION_ORDER) - 1:
            next_sec = SECTION_ORDER[sec_idx + 1]
            next_href = SECTIONS[next_sec]["hub"]
            next_label = f"ถัดไป: {SECTIONS[next_sec]['label']} →"
        else:
            next_href = "index.html"
            next_label = "จบคอร์ส — กลับหน้าแรก"

    body = f'''        <h1>{label}. {title}</h1>

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
    return page_html(f"{label}. {title}", body, expand_section=section, active_top=section, active_chapter=idx)


if __name__ == "__main__":
    for sec in SECTION_ORDER:
        for i in chapter_numbers(sec):
            write(chapter_filename(sec, i), chapter_page(sec, i))
    # regenerate basic.html hub via the same generator for full consistency
    write(SECTIONS["basic"]["hub"], hub_page("basic"))
