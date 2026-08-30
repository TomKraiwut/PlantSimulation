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
                   "เปิดตัวอย่างโมเดล Factory 51 จาก Start Page ได้ด้วยตัวเอง",
                   "ควบคุมมุมมอง 3 มิติด้วยเมาส์/คีย์บอร์ด และโต้ตอบกับ Object ด้วย Click/Double-click/Right-click ได้",
                   "เข้าใจแนวคิด Event-Controlled Simulation และควบคุมการรันผ่าน EventController ได้"],
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

BODY[("basic", 1)] = f'''
<h2>Discrete Event Simulation คืออะไร</h2>
<p>Plant Simulation จำลองระบบแบบ <strong>Discrete Event Simulation (DES)</strong> — คือการจำลอง
"เหตุการณ์" ที่เกิดขึ้นเป็นจุดๆ ตามเวลา (เช่น ชิ้นงานมาถึง, เครื่องเริ่มทำงาน, เครื่องทำงานเสร็จ)
แทนที่จะคำนวณทุกวินาทีต่อเนื่อง ทำให้จำลองกระบวนการผลิตหลายวัน/หลายเดือนได้ในเวลาไม่กี่วินาทีบนคอมพิวเตอร์</p>

<div class="note">
<strong>นิยาม — Plant Simulation Model คืออะไร:</strong> พูดให้ตรงไปตรงมาที่สุด โมเดลจำลองคือ <em>การเลียนแบบระบบ</em>
ที่สร้างขึ้นจากความรู้หรือสมมติฐานเกี่ยวกับพฤติกรรมของส่วนต่างๆ ในระบบนั้น โดยมีจุดประสงค์เพื่อให้ได้ข้อมูลเชิงลึกเกี่ยวกับพฤติกรรมของ
<em>ทั้งระบบ</em> — ไม่ได้จำลองทุกรายละเอียดให้เหมือนจริง 100% แต่เลือกจำลองเฉพาะส่วนที่ส่งผลต่อคำถามที่อยากตอบ
</div>

{side_by_side(
    screenshot("assets/images/basic/01-01.png", "ตัวอย่างโมเดล 3D ของสายการผลิตใน Plant Simulation"),
    step_list([
        "ผังพื้นโรงงาน (เส้นสีเทาจางด้านหลัง) — แบบ Layout จริงที่ใช้เป็นพื้นหลังอ้างอิงตำแหน่งวาง Object",
        "กลุ่มเครื่องจักรสีเขียว-ฟ้า — แต่ละกลุ่มแทนสถานีเครื่องจักร/ประมวลผลในสายการผลิตจริง",
        "เส้นทางสีส้ม — เส้นทางลำเลียงชิ้นงานที่เชื่อมแต่ละสถานีเข้าด้วยกัน",
        "พาเลทสีเขียวด้านล่าง — จุดพักสินค้าสำเร็จรูปก่อนส่งออกจากไลน์",
    ])
)}

<h2>Simulation กับ Digital Twin</h2>
<p><strong>Simulation</strong> (การจำลองสถานการณ์) คือการสร้างแบบจำลองของระบบหรือกระบวนการในโลกจริงขึ้นมา เพื่อศึกษาพฤติกรรม
ทดสอบสมมติฐาน หรือคาดการณ์ผลลัพธ์ที่จะเกิดขึ้นภายใต้เงื่อนไขต่างๆ โดยไม่ต้องลงมือทำกับสถานการณ์จริง — เน้นออกแบบและทดสอบ
"สิ่งที่อาจจะเกิดขึ้น" (What-if scenarios)</p>
<p><strong>Digital Twin</strong> ต่อยอดจากแนวคิดนี้อีกขั้นหนึ่ง: เป็นแบบจำลองเสมือนจริงของวัตถุหรือกระบวนการที่ <em>เชื่อมโยงกับข้อมูลจริง
อย่างต่อเนื่อง</em> ทำให้แสดงข้อมูลเชิงลึกของสิ่งที่เป็นอยู่ปัจจุบันแบบเรียลไทม์ (Real-time monitoring) และพยากรณ์เหตุการณ์ที่อาจจะเกิดขึ้น
จากข้อมูลที่ได้รับ (Prediction) ได้ — พูดง่ายๆ คือโมเดล Plant Simulation ที่เริ่มสร้างในคอร์สนี้เป็นจุดตั้งต้น พอต่อเข้ากับข้อมูลจริงจาก
หน้างานก็ต่อยอดกลายเป็น Digital Twin ได้ต่อไป</p>

{side_by_side(
    screenshot("assets/images/basic/01-02.jpg", "การผสาน Digital Twin เข้ากับเครื่องจักรจริงระหว่างขั้นตอนติดตั้ง/ตรวจสอบ"),
    step_list([
        "ลดต้นทุน — ทดสอบและแก้ปัญหาในโลกดิจิทัลก่อนลงทุนจริง",
        "ทำนายล่วงหน้า — รู้ว่าอะไรจะเสียก่อนที่มันจะเสียจริง",
        "ตัดสินใจได้ดีขึ้น — มีข้อมูลเรียลไทม์ประกอบการวิเคราะห์",
        "ออกแบบได้แม่นยำ — จำลองสถานการณ์ได้ไม่จำกัดจำนวนครั้ง",
    ])
)}

{screenshot("assets/images/basic/01-03.jpg", "ตัวอย่าง Plant Simulation Model ของคลังสินค้าอัตโนมัติขนาดใหญ่", caption="โมเดลระดับนี้จำลองทั้งชั้นวางสินค้าอัตโนมัติ (AS/RS), สายพานลำเลียง, และเส้นทางขนย้ายในคลังสินค้าจริง — ใช้หลัก DES เดียวกับโมเดลง่ายๆ ที่กำลังจะสร้างในคอร์สนี้ เพียงแค่ขยายสเกลขึ้น")}

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

<h2>เปิดตัวอย่างโมเดล Factory 51</h2>
<p>วิธีที่เร็วที่สุดในการทำความคุ้นเคยกับหน้าตาโปรแกรมคือเปิดโมเดลตัวอย่างที่ติดมากับโปรแกรมดูก่อน — <strong>Factory 51</strong>
คือโมเดลสาธิตที่ Siemens แนบมาให้ทุกเครื่องที่ติดตั้ง Plant Simulation ใช้แสดงภาพ 3D ของโรงงานแบบครบวงจร</p>
<ol class="steps">
<li>เปิดโปรแกรม Plant Simulation</li>
<li>ไปที่เมนู <code>Window → Start Page</code></li>
<li>ในหน้า Start Page ไปที่คอลัมน์ <code>Getting Started</code> คลิก <code>Example Models</code></li>
<li>ในรายการที่เปิดขึ้นมา คลิกเลือก <code>Factory 51</code></li>
<li>ถ้าเครื่องใช้ Student License จะมีหน้าต่างแจ้งเตือนว่าโมเดลนี้เกิน 80 Objects (เกินสิทธิ์ Student License) ให้คลิก
<code>Yes</code> เพื่อเปิดแบบ Viewer License แทน</li>
</ol>

{screenshot("assets/images/basic/02-01.jpg", "ขั้นตอนเปิดโมเดลตัวอย่าง Factory 51 จาก Start Page", caption="Start Page → Getting Started → Example Models → Factory 51 → ยืนยัน Viewer License")}

<div class="note">
<strong>ทดสอบจริงแล้วพบว่า:</strong> โมเดล Factory 51 มี Object เกิน 80 ตัวจริงตามที่โปรแกรมแจ้ง — เมื่อลองเชื่อมต่อผ่าน COM/สคริปต์ภายนอก
(แทนการเปิดผ่านหน้าจอโปรแกรมตรงๆ) จะเจอ error <code>"Remote access is not allowed with this license"</code> ทันที นี่คือข้อจำกัดจริงของ
Viewer/Student License ที่ควรรู้ไว้ — โมเดลขนาดนี้ต้องเปิดผ่าน GUI เท่านั้น จะควบคุมจากภายนอกแบบที่สอนในบท Advanced ไม่ได้จนกว่าจะมี License เต็ม
</div>

<h2>ภาพรวมโมเดล Factory 51</h2>
<p>เมื่อเปิดขึ้นมาแล้ว จะเห็นภาพ 3D ของโรงงานจำลองที่มีครบทุกโซนตั้งแต่รับวัตถุดิบจนถึงส่งสินค้าออก — เป็นตัวอย่างที่ดีของสิ่งที่พูดถึงในบทที่แล้ว
เรื่อง "พฤติกรรมของทั้งระบบ" ที่มองเห็นได้ด้วย 3D Visualization/3D Animation</p>

{screenshot("assets/images/basic/02-02.jpg", "ภาพรวมโซนต่างๆ ในโมเดล Factory 51")}

<table>
<tr><th>โซน</th><th>ประกอบด้วย</th></tr>
<tr><td><strong>Inbound</strong></td><td>Truck, Forklift, Robot, Crane — รับวัตถุดิบเข้าสู่โรงงาน</td></tr>
<tr><td><strong>Production Plant (P1 &amp; P2)</strong></td><td>Polishing, Milling, Paint, Drying, Clean, QC, PostProcess, Pack — สองสายการผลิตขนาน</td></tr>
<tr><td><strong>Robot Auto Packing</strong></td><td>AGV Load/Unload, AGV Charger — หุ่นยนต์บรรจุภัณฑ์และสถานีชาร์จ AGV</td></tr>
<tr><td><strong>Warehouse</strong></td><td>ASRS (Automated Storage/Retrieval System), WMS — คลังสินค้าอัตโนมัติ</td></tr>
<tr><td><strong>Outbound</strong></td><td>Conveyor, Truck — ส่งสินค้าสำเร็จรูปออกจากโรงงาน</td></tr>
</table>

<h2>ควบคุมมุมมอง 3 มิติด้วยเมาส์และคีย์บอร์ด</h2>
<p>ก่อนเดินสำรวจโมเดล Factory 51 ควรคุ้นเคยกับการควบคุมกล้อง 3D ก่อน — ใช้ได้ทั้งเมาส์และคีย์บอร์ดร่วมกัน</p>
<table>
<tr><th>การควบคุม</th><th>ผลลัพธ์</th></tr>
<tr><td>เลื่อนลูกกลิ้งเมาส์ (Scroll Wheel)</td><td>ซูมเข้า/ออก — กด <code>Shift</code> ค้างเพื่อซูมเร็ว, กด <code>Ctrl</code> ค้างเพื่อซูมช้า</td></tr>
<tr><td>กดลูกกลิ้งเมาส์ค้าง + ลาก</td><td>หมุนมุมมอง (Rotate) รอบจุดศูนย์กลางฉากหรือรอบ Object ที่เลือก</td></tr>
<tr><td>กด <code>Ctrl</code> + ลูกกลิ้งเมาส์ค้าง + ลาก</td><td>เลื่อนมุมมองแนวขนาน (Pan)</td></tr>
</table>

{screenshot("assets/images/basic/02-03.jpg", "ไอคอนเปรียบเทียบ Rotate กับ Pan")}

<table>
<tr><th>ปุ่มคีย์บอร์ด</th><th>ผลลัพธ์</th></tr>
<tr><td><code>W</code> / <code>S</code></td><td>เดินเข้าใกล้ / เดินออกห่างจาก Object ในมุมมอง 3D</td></tr>
<tr><td><code>Q</code> / <code>E</code></td><td>เดินไปทางซ้าย / ทางขวาของ Object</td></tr>
<tr><td><code>A</code> / <code>D</code></td><td>หันซ้าย / หันขวา</td></tr>
<tr><td><code>Z</code> / <code>Shift + Z</code></td><td>ลดระดับตัวเอง / ยกระดับตัวเองขึ้น</td></tr>
</table>

<h2>โต้ตอบกับ Object: Click / Double-click / Right-click</h2>
<p>สามวิธีหลักในการโต้ตอบกับ Object ในมุมมอง 3D (และ 2D เช่นกัน) — ใช้บ่อยที่สุดตลอดทั้งคอร์สนี้</p>
<table>
<tr><th>การกระทำ</th><th>ผลลัพธ์</th></tr>
<tr><td><strong>Click</strong> (คลิกซ้ายครั้งเดียว)</td><td>เลือก Object (Select)</td></tr>
<tr><td><strong>Double Click</strong></td><td>เปิด Object Window — หน้าต่าง Attribute ของ Object นั้น</td></tr>
<tr><td><strong>Right Click</strong></td><td>เปิดเมนู Quick tools — ทางลัดไปยังคำสั่งที่ใช้บ่อย เช่น Edit 3D Properties, Show Attributes and Methods (F8), Find Object (F3)</td></tr>
<tr><td><strong>Double Click</strong> บน Object ที่มี Frame ซ้อนอยู่ข้างใน</td><td>เปิด Frame ข้างในนั้น (กด <code>Shift + Enter</code> เพื่อย้อนกลับออกมา)</td></tr>
</table>

{side_by_side(
    screenshot("assets/images/basic/02-04.jpg", "หน้าต่าง Attribute ของ Object PickAndPlaceBottom เปิดจากการ Double Click"),
    screenshot("assets/images/basic/02-05.jpg", "เมนู Quick tools เปิดจากการ Right Click")
)}

<div class="tip">
<strong>Tip:</strong> ถ้าหน้าต่างเพี้ยนหรือ panel หายไป ไปที่เมนู <code>View → Reset Window Layout</code>
(หรือใกล้เคียง แล้วแต่เวอร์ชัน) เพื่อคืนค่าเลย์เอาต์เริ่มต้น
</div>

<h2>Time-Oriented Simulation และ Event-Controlled Simulation</h2>
<p>Plant Simulation เป็นโปรแกรมจำลองแบบ <strong>discrete, event-controlled</strong> — หมายความว่าโปรแกรมจะตรวจสอบเฉพาะ
"จุดเวลาที่มีเหตุการณ์เกิดขึ้นจริง" ในโมเดลเท่านั้น (สอดคล้องกับ Discrete Event Simulation ที่พูดถึงในบทที่ 1) ไม่ใช่คำนวณทุกช่วงเวลาต่อเนื่อง
ควบคุมการรันทั้งหมดผ่าน Object <strong>EventController</strong> ตัวเดียว</p>
<ol class="steps">
<li>คลิกที่ปุ่ม <code>Start/Stop Simulation</code> เพื่อเริ่ม/หยุดการจำลอง</li>
<li>ดับเบิลคลิกที่ <code>EventController</code> เพื่อเปิดหน้าต่างควบคุม (แท็บ Controls/Settings)</li>
<li>ปรับตัวเลื่อน <code>Slower ↔ Faster</code> เพื่อปรับความเร็วของแบบจำลอง แล้วสังเกตพฤติกรรมการทำงาน</li>
</ol>

{screenshot("assets/images/basic/02-06.jpg", "หน้าต่างควบคุม EventController — ปุ่ม Play/Pause และตัวเลื่อนความเร็ว")}

<div class="note">
<strong>เล่นสนุกได้ด้วย:</strong> ในโมเดล Factory 51 ลองเดินสำรวจฉาก 3D ด้วยปุ่มคีย์บอร์ดด้านบนดูให้ทั่ว — มีห้องเล็กๆ ซ่อนอยู่ในโมเดล
ให้ลองหา "Beer room" ดู เป็นวิธีฝึกการควบคุมกล้อง 3D แบบไม่เครียดก่อนไปสร้างโมเดลของตัวเองในบทถัดไป
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
<tr><td><strong>Conveyor</strong></td><td>เส้นทางลำเลียงชิ้นงานระหว่างสถานีแบบมีความเร็ว/ความยาว</td><td><code>Length</code>, <code>Speed</code></td></tr>
<tr><td><strong>Station</strong></td><td>สถานีประมวลผล/แปรรูปชิ้นงาน (จำลองเครื่องจักร 1 หัว)</td><td><code>ProcTime</code> — เวลาแปรรูปต่อชิ้น</td></tr>
<tr><td><strong>Buffer</strong></td><td>จุดพักชิ้นงานเมื่อสถานีถัดไปไม่ว่าง</td><td><code>Capacity</code> — ความจุสูงสุด</td></tr>
<tr><td><strong>Drain</strong></td><td>จุดสิ้นสุด ชิ้นงานออกจากระบบ (สินค้าสำเร็จรูป)</td><td>ไม่ต้องตั้งค่าอะไรพิเศษ</td></tr>
<tr><td><strong>EventController</strong></td><td>ตัวควบคุมเวลาจำลอง (นาฬิกาของโมเดล) ต้องมีเสมอในทุกโมเดล</td><td><code>SimTime</code> อ่านค่าเวลาจำลองปัจจุบัน</td></tr>
</table>

<div class="note">
<strong>ข้อควรรู้:</strong> ทุก Object มีแอตทริบิวต์ <code>Name</code> (ชื่อ) และ <code>InternalClassType</code>
(ชื่อประเภทจริงในภาษาอังกฤษ เช่น "Source", "Drain") ที่ใช้อ้างอิงได้ทั้งจาก GUI และจากสคริปต์ (ดูบท Advanced)
</div>

<h2>ลำดับการไหลของชิ้นงานทั่วไป</h2>
<p><code>Source → (Conveyor) → Station → (Buffer) → Station → (Conveyor) → Drain</code></p>
<p>ไม่จำเป็นต้องมี Conveyor/Buffer ทุกจุด — เชื่อม Object ติดกันตรงๆ ก็ทำงานได้ แค่ไม่มีระยะทาง/เวลาขนส่งจำลองอยู่ในนั้น</p>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> ถ้าไม่ใส่ EventController ลงในโมเดลเลย จะเกิดอะไรขึ้นเมื่อกด Start?
</div>
<div class="tip"><strong>เฉลย:</strong> โมเดลจะรันไม่ได้เลย — EventController คือนาฬิกาของทั้งระบบ ไม่มี EventController = ไม่มีเวลาให้เดินหน้า</div>
'''

BODY[("basic", 4)] = '''
<h2>สร้างโมเดลแรก: สายการผลิตง่ายๆ</h2>
<p>ทำตามขั้นตอนนี้เพื่อสร้างโมเดล <code>Source → Station → Drain</code></p>
<ol class="steps">
<li>เปิด Class Library → เลือกหมวด <code>MaterialFlow</code></li>
<li>ลาก <strong>Source</strong>, <strong>Station</strong>, <strong>Drain</strong> มาวางเรียงกันบน Frame</li>
<li>ลาก <strong>EventController</strong> มาวางไว้มุมใดก็ได้ (จำเป็นต่อการรัน — ดูบทที่ 3)</li>
<li>เชื่อมต่อ Object โดยคลิกที่มุมขวาบนของแต่ละ Object แล้วลากไปยัง Object ถัดไป (จะเห็นลูกศรเชื่อม)</li>
<li>ดับเบิลคลิก <strong>Source</strong> เพื่อตั้งค่า <code>Interval</code> เช่น สร้างชิ้นงานทุก 5 วินาที</li>
<li>ดับเบิลคลิก <strong>Station</strong> เพื่อตั้งค่า <code>ProcTime</code> เช่น 10 วินาทีต่อชิ้น</li>
<li>กดปุ่ม <strong>Start Simulation</strong> (▶) ที่ Toolbar ด้านบน</li>
</ol>

<div class="tip">
<strong>Tip:</strong> ถ้าเชื่อมต่อ Object ไม่ติด ให้เช็คว่าจุดเชื่อม (Connector) เป็นสีเขียวหรือไม่ — สีแดงหมายถึงยังเชื่อมไม่สำเร็จ
</div>

<h2>ตัวอย่าง: ทำนายผลก่อนรันจริง</h2>
<p>โมเดล <code>Source(Interval=5s) → Station(ProcTime=10s) → Drain</code></p>
<div class="note">
<strong>คำถามฝึกคิด:</strong> Source ผลิตชิ้นงานเร็วกว่า Station แปรรูปเสร็จ (5s &lt; 10s) จะเกิดอะไรขึ้นเมื่อรันไปนานๆ?
</div>
<div class="tip"><strong>เฉลย:</strong> Station รับชิ้นงานไม่ทัน Source เลยจะถูก <strong>Blocked</strong>
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
<p>คลิกขวาที่ Object ประเภทประมวลผล (เช่น <strong>Station</strong>) แล้วเลือก <code>Statistics</code> เพื่อดู:</p>
<table>
<tr><th>สถานะ</th><th>ความหมาย</th></tr>
<tr><td><strong>Working</strong></td><td>เวลาที่เครื่องกำลังแปรรูปชิ้นงานจริง — ยิ่งสูงยิ่งใช้งานคุ้ม</td></tr>
<tr><td><strong>Waiting</strong></td><td>เวลาที่รอชิ้นงานเข้ามา (ว่างงาน) — สูงแปลว่าต้นทางป้อนช้าเกินไป</td></tr>
<tr><td><strong>Blocked</strong></td><td>เวลาที่ทำงานเสร็จแล้วแต่ส่งต่อไม่ได้ (สถานีถัดไปไม่ว่าง) — สูงแปลว่าปลายทางเป็นคอขวด</td></tr>
</table>

<div class="tip">
<strong>คำถามฝึกคิด:</strong> ถ้า Station มีค่า Blocked สูงมาก ควรแก้ปัญหาที่ตัว Station นี้เอง หรือที่อื่น?
</div>
<div class="tip"><strong>เฉลย:</strong> ควรแก้ที่ <em>สถานีถัดไป</em> (ปลายทางที่รับต่อ) ไม่ใช่ตัว Station เอง — เพราะ Blocked สูง
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
<a href="basic-03.html">Basic บทที่ 3</a></p>

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
<li>สาย Station เรียงต่อกัน 15-20 สถานี เชื่อมด้วย Conveyor (ดู <a href="basic-04.html">Basic บทที่ 4</a>)</li>
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
