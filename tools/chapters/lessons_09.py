# -*- coding: utf-8 -*-
"""Lessons 9: Python in Plant Simulation -- from 09_Python.pptx"""
from gen_site import screenshot, step_list, side_by_side

OBJECTIVES = [
    "ติดตั้ง Python 3.14 กับ pandas / matplotlib และเพิ่ม PythonModule ลงใน Class Library ได้",
    "เขียน print ตัวแปร และอ่าน / เขียนค่าของวัตถุในโมเดลด้วย current.ชื่อวัตถุ.ชื่อค่า ได้",
    "สร้างฟังก์ชันด้วย def แล้วให้ Method ของ SimTalk เรียกใช้ด้วย .call ได้",
    "ใช้ pandas นับชิ้นงานต่อชั่วโมงจากตาราง และวาดกราฟด้วย matplotlib ได้",
]

# ---- code samples (plain strings: no f-string escaping needed; < > & already escaped) ----
CODE_HELLO = '''<pre><code># A line that starts with # is a comment
print("Hello Plant Simulation")

a = 7          # variable a = 7 (use =, not :=)
b = 9
print(a + b)   # 16

machine = "Station1"   # text goes in quotes
print("Machine:", machine)</code></pre>'''

CODE_READWRITE = '''<pre><code># current = the Frame this PythonModule is in

# 1) read a value: current.&lt;object&gt;.&lt;attribute&gt;
print("ProcTime before:", current.Station.ProcTime)

# 2) write a new value with = (seconds)
current.Station.ProcTime = 45
print("ProcTime after:", current.Station.ProcTime)

# 3) a Variable: read and write .Value
print("Target before:", current.Target.Value)
current.Target.Value = 80
print("Target after:", current.Target.Value)</code></pre>'''

CODE_CALC = '''<pre><code># def makes a function; the line ends with :
# lines inside the function are indented 4 spaces
def oee(availability, performance, quality):
    return availability * performance * quality

def percent(x):
    return round(x * 100, 1)

# test when you click Import
print("OEE =", percent(oee(0.90, 0.95, 0.99)), "%")</code></pre>'''

CODE_CALLPYTHON = '''<pre><code>// call the Python function oee in the PythonModule Calc
var r: real := Calc.call("oee", 0.90, 0.95, 0.99)
OEE := r
print "OEE from Python =", r</code></pre>'''

CODE_ANALYSE = '''<pre><code>import os
import pandas as pd                 # tables
import matplotlib
matplotlib.use("Agg")               # draw into a file, no window
import matplotlib.pyplot as plt     # charts
import PlantSimulation as ps

# 1) read the whole table PartLog (row 0 = column names)
rows = current.PartLog[None]
df = pd.DataFrame(rows[1:], columns=rows[0])
print("Parts:", len(df))

# 2) count the parts finished in each hour
df["Hour"] = (df["Time"] // 3600 + 1).astype(int)
per_hour = df.groupby("Hour").size()
print(per_hour)
print("Mean per hour:", round(per_hour.mean(), 1))</code></pre>'''

CODE_PLOT = '''<pre><code># 3) bar chart, saved as a picture next to the model
ax = per_hour.plot(kind="bar", color="#FA000F", figsize=(7, 4), …
ax.set_xlabel("Hour")
ax.set_ylabel("Parts")
ax.set_title("Parts per hour")
plt.tight_layout()
path = os.path.join(ps.getCurrentDirectory(), "P4_parts_per_hour.png")
plt.savefig(path)
plt.close()
print("Saved:", path)</code></pre>'''

BODY = f'''
<p class="lead" style="max-width:46em;">บทนี้สำหรับคนที่ไม่เคยเขียน Python มาก่อน — 6 ขั้นตอน จากติดตั้ง Python ถึงกราฟผลผลิต
ทุก Frame ในไฟล์ <code>09_Python.spp</code> ทำไว้ให้แล้ว แค่เปิดหน้าโค้ด อ่านทีละบรรทัด แล้วกด <code>Import</code> ดูผลใน Console
ผลที่วัดได้: Python เปลี่ยน ProcTime 60 → 45 วินาที ผลผลิตขึ้นจาก <strong>59 → 79 ชิ้น/ชม.</strong> (วัดจริง 2606)</p>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 · Python 3.12–3.14 (python.org) · ไฟล์ <code>09_Python.spp</code> (4 Frame P1–P4)
· พื้นฐาน Method จาก<a href="lessons-07.html">บท 07 SimTalk</a>
</div>

<h2>ภาพรวม: 6 ขั้นตอน</h2>
<table>
<tr><th>ขั้น</th><th>เรื่อง</th><th>ทำอะไร</th></tr>
<tr><td>1</td><td>ติดตั้ง Python</td><td>Python 3.14 + pandas, matplotlib ครั้งเดียวต่อเครื่อง</td></tr>
<tr><td>2</td><td>PythonModule</td><td>เพิ่มวัตถุ Py ลง Class Library แล้ววางใน Frame</td></tr>
<tr><td>3</td><td>Hello</td><td>print, ตัวแปร, คอมเมนต์ แล้วกด Import</td></tr>
<tr><td>4</td><td>อ่าน / เขียนค่า</td><td>Python เปลี่ยน ProcTime และ Variable ในโมเดล</td></tr>
<tr><td>5</td><td>ฟังก์ชัน</td><td>def สูตร OEE แล้วให้ Method เรียกใช้</td></tr>
<tr><td>6</td><td>ตาราง + กราฟ</td><td>pandas นับชิ้นต่อชั่วโมง matplotlib วาดกราฟ</td></tr>
</table>

<h2>4 Frame ในไฟล์นี้</h2>
<table>
<tr><th>Frame</th><th>วัตถุหลัก</th><th>เรียนอะไร</th><th>ผลที่วัดได้ (2606)</th><th>ขั้นที่</th></tr>
<tr><td>P1_Hello</td><td>PythonModule Hello</td><td>print, ตัวแปร, คอมเมนต์</td><td>Console: Hello Plant Simulation, 16</td><td>3</td></tr>
<tr><td>P2_ReadWrite</td><td>PythonModule ReadWrite, Station, Variable Target</td><td>อ่าน / เขียนค่าของวัตถุ</td><td>79 ชิ้น/ชม. หลังแก้ ProcTime เป็น 45 s</td><td>4</td></tr>
<tr><td>P3_Function</td><td>PythonModule Calc, Method CallPython</td><td>def แล้วให้ Method เรียกด้วย .call</td><td>OEE 84.6% (0.84645)</td><td>5</td></tr>
<tr><td>P4_Data</td><td>ตาราง PartLog, Method LogPart / Init, PythonModule Analyse</td><td>pandas + matplotlib</td><td>517 ชิ้นใน 8 ชม. · เฉลี่ย 64.6 ชิ้น/ชม.</td><td>6</td></tr>
</table>

<h2>Workflow: Python ทำงานคู่กับโมเดลอย่างไร</h2>
<table>
<tr><th>ลำดับ</th><th>งาน</th><th>ทำอะไร</th><th>ที่ไหน</th></tr>
<tr><td>1</td><td>เขียนโค้ด</td><td>พิมพ์ Python ในหน้าต่างของ PythonModule (แท็บ Content)</td><td>PythonModule</td></tr>
<tr><td>2</td><td>กด Import</td><td>Plant Simulation ส่งโค้ดให้ Python รัน ผล print ขึ้นใน Console</td><td>ปุ่ม Import</td></tr>
<tr><td>3</td><td>อ่าน / เขียนค่า</td><td><code>current.Station.ProcTime</code> ใช้จุดคั่นเหมือน SimTalk</td><td>P2_ReadWrite</td></tr>
<tr><td>4</td><td>Method เรียก</td><td><code>Calc.call("oee", …)</code> ส่งค่าเข้าไปและรับผลกลับ</td><td>P3_Function</td></tr>
<tr><td>5</td><td>วิเคราะห์ข้อมูล</td><td>อ่านตารางผลการรัน นับ สรุป วาดกราฟ</td><td>P4_Data</td></tr>
</table>
<div class="note"><strong>Python ไม่ได้มาแทน SimTalk:</strong> SimTalk เร็วกว่าเพราะเรียกฟังก์ชันที่คอมไพล์แล้ว (Help 2606)
ใช้ Python เมื่ออยากได้ความสามารถของไลบรารี เช่น pandas จัดการตาราง matplotlib วาดกราฟ scikit-learn ทำ machine learning</div>

<h2>พื้นฐาน Python 7 ข้อ เทียบกับ SimTalk ที่รู้แล้ว</h2>
<table>
<tr><th>เรื่อง</th><th>SimTalk (บท 07)</th><th>Python</th><th>จำง่าย ๆ</th></tr>
<tr><td>ให้ค่าตัวแปร</td><td><code>a := 7</code></td><td><code>a = 7</code></td><td>Python ใช้ = ตัวเดียว</td></tr>
<tr><td>ประกาศตัวแปร</td><td><code>var a: integer := 7</code></td><td><code>a = 7</code></td><td>ไม่ต้องบอกชนิด Python รู้เอง</td></tr>
<tr><td>คอมเมนต์</td><td><code>// ข้อความ</code> หรือ <code>-- ข้อความ</code></td><td><code># ข้อความ</code></td><td>Python ไม่อ่านหลัง #</td></tr>
<tr><td>แสดงผล</td><td><code>print a</code></td><td><code>print(a)</code></td><td>Python ต้องมีวงเล็บ</td></tr>
<tr><td>จบบล็อก if / for / def</td><td><code>end</code> · <code>next</code></td><td>ย่อหน้า 4 ช่อง</td><td>บรรทัดหัวลงท้ายด้วย <code>:</code></td></tr>
<tr><td>อ้างถึงวัตถุ</td><td><code>Station.ProcTime</code></td><td><code>current.Station.ProcTime</code></td><td>ขึ้นต้นด้วย current</td></tr>
<tr><td>ตัวพิมพ์เล็ก-ใหญ่</td><td>Print = print</td><td>print ≠ Print</td><td>พิมพ์คำสั่ง Python ให้ตรงทุกตัว</td></tr>
</table>
<div class="tip"><strong>ไม่ต้องพิมพ์เอง:</strong> ตัวอย่างโค้ดทุกตัวในบทนี้อยู่ในไฟล์ 09_Python.spp แล้ว
· ข้อที่คนเริ่มต้นพลาดบ่อยที่สุดคือย่อหน้าไม่เท่ากัน และใช้ <code>:=</code> แบบ SimTalk ใน Python
· ตาราง DataTable ของ Plant Simulation ยังเริ่มนับแถว/คอลัมน์ที่ 1 เหมือนเดิม แม้ list ของ Python จะเริ่มที่ 0</div>

<h2>ขั้นที่ 1: ติดตั้ง Python 3.14 จาก python.org</h2>
{side_by_side(
    screenshot("assets/images/lessons/09-01.jpg", "หน้า Python Releases for Windows บน python.org"),
    step_list([
        "<code>Downloads</code> › <code>Windows</code> — หน้า Python Releases for Windows",
        "<strong>Python 3.14.x</strong> ใน Stable Releases (Siemens รองรับ 3.12, 3.13, 3.14)",
        "<code>Windows installer (64-bit)</code> — ดาวน์โหลดไฟล์ .exe",
        "ดับเบิลคลิกไฟล์ คลิกช่อง <code>Add python.exe to PATH</code> ให้ขึ้นเครื่องหมายถูก ☑ แล้ว <code>Install Now</code> (ไม่มีในภาพ)",
    ])
)}
<div class="note"><strong>เครื่องที่ทำบทนี้:</strong> ใช้ Python 3.15.1 ทำได้ทุกขั้นในบท แต่ 3.15 ไม่อยู่ในรายการที่ Siemens รองรับ งานจริงใช้ 3.14
(ภาพถ่ายวันที่ 4 พ.ย. 2026 รุ่นล่าสุดของ 3.14 คือ 3.14.10) · ติดตั้งให้เสร็จก่อนเปิด Plant Simulation
· ถ้ามี Python หลายเวอร์ชันใช้ <code>setPythonDLLPath</code></div>

<h2>ขั้นที่ 1: ติดตั้งไลบรารี pandas และ matplotlib</h2>
{screenshot("assets/images/lessons/09-02.jpg", "Command Prompt: ผลของ python --version, pip show และท้ายผลของ pip install")}
<p>Windows › พิมพ์ <code>cmd</code> › Command Prompt แล้วพิมพ์ทีละบรรทัด:</p>
<pre><code>python --version
python -m pip install pandas matplotlib
python -m pip show pandas matplotlib</code></pre>
{step_list([
    "<code>python --version</code> — ต้องขึ้นเลขเวอร์ชัน ถ้าไม่ขึ้น = ตอนติดตั้งช่อง Add python.exe to PATH ไม่มีเครื่องหมายถูก",
    "<code>python -m pip install pandas matplotlib</code> — รอจนขึ้น <em>Successfully installed</em>",
    "<code>python -m pip show pandas matplotlib</code> — ตรวจว่าติดตั้งแล้ว และอยู่ใน Python ตัวเดียวกัน",
])}
<div class="tip"><strong>pip คืออะไร:</strong> ตัวติดตั้งไลบรารีที่มากับ Python · pandas = จัดการตาราง · matplotlib = วาดกราฟ
· ติดตั้งครั้งเดียวต่อเครื่อง ใช้อินเทอร์เน็ต · ภาพบนคือผลของคำสั่งตรวจ ภาพล่างคือท้ายผลของ pip install (ในภาพไม่เห็นบรรทัดคำสั่ง
เพราะสั่งผ่านสคริปต์ตอนถ่าย เวลาพิมพ์เองจะเห็นคำสั่งอยู่เหนือผล) · ถ้า Plant Simulation เปิดอยู่ตอนติดตั้ง ให้ปิดแล้วเปิดใหม่</div>

<h2>ขั้นที่ 2: เพิ่ม PythonModule ลงใน Class Library</h2>
{side_by_side(
    screenshot("assets/images/lessons/09-03.jpg", "หน้าต่าง Manage Class Library แท็บ Basic Objects › InformationFlow"),
    screenshot("assets/images/lessons/09-04.jpg", "ปุ่ม Home › Manage Class Library และไอคอน Py ใน Toolbox › Information Flow")
    + step_list([
        "<code>Home</code> › <code>Manage Class Library</code> — ปุ่มขวาสุดของริบบอน (ภาพขวา)",
        "<code>Basic Objects</code> — แท็บแรกของหน้าต่าง",
        "<code>InformationFlow</code> — เปิดกลุ่มนี้",
        "คลิกช่อง <code>PythonModule</code> ☑ อยู่ใต้ Method",
        "<code>OK</code> แล้ว Toolbox › Information Flow จะมีไอคอน <strong>Py</strong>",
        "ลากไอคอน Py ลงใน Frame เหมือนวาง Method แล้วตั้งชื่อ",
    ])
)}
<div class="note"><strong>ไฟล์ใหม่ยังไม่มี PythonModule:</strong> ไฟล์ใหม่ของ Plant Simulation 2606 ยังไม่มี PythonModule ใน Class Library
(.InformationFlow มี Method, Variable, DataTable … แต่ไม่มี PythonModule) ต้องเพิ่มตามขั้นนี้ 1 ครั้งต่อไฟล์
· ไฟล์ 09_Python.spp เพิ่มไว้แล้ว ภาพนี้จึงมีเครื่องหมายถูกอยู่แล้ว</div>

<h2>ขั้นที่ 3: P1_Hello — print และตัวแปร</h2>
{side_by_side(
    screenshot("assets/images/lessons/09-05.jpg", "หน้าต่าง PythonModule Hello และ Console หลังกด Import"),
    step_list([
        "<code># …</code> — คอมเมนต์ อธิบายโค้ด Python ข้ามไป",
        '<code>print("…")</code> — แสดงข้อความใน Console',
        "<code>a = 7</code> · <code>b = 9</code> — สร้างตัวแปรเก็บค่า แล้ว <code>print(a + b)</code> ได้ 16",
        "<code>Import</code> — ส่งโค้ดให้ Python รัน (หรือกด F5 ในช่องโค้ด)",
        "Console — ผลขึ้นตามลำดับบรรทัด: Hello Plant Simulation, 16, Machine: Station1",
    ])
)}
<p>โค้ดใน PythonModule <code>Hello</code> (Frame P1_Hello › ดับเบิลคลิก Hello):</p>
''' + CODE_HELLO + f'''
<div class="tip"><strong>ไม่เห็น Console:</strong> แท็บ <code>Window</code> › <code>Console</code> · ข้อความผิดพลาดของ Python ก็ขึ้นที่นี่ (ภาษาอังกฤษ)
· <code>machine = "Station1"</code> คือตัวแปรข้อความ ต้องอยู่ในเครื่องหมายคำพูด · Import ครั้งต่อไปจะรันโค้ดซ้ำ · Shift + Import = ล้างตัวแปรเก่าก่อน (Help 2606)</div>

<h2>ขั้นที่ 4: P2_ReadWrite — อ่านและเขียนค่าในโมเดล</h2>
{side_by_side(
    screenshot("assets/images/lessons/09-06.jpg", "หน้าต่าง PythonModule ReadWrite และ Console ก่อน / หลัง"),
    step_list([
        "<code>current</code> = Frame ที่ PythonModule นี้วางอยู่",
        "<code>current.Station.ProcTime</code> — อ่านเวลาทำงาน ได้ 0:01:00 (1 นาที)",
        "<code>current.Station.ProcTime = 45</code> — เขียนค่าใหม่ ตัวเลขคือวินาที",
        "<code>current.Target.Value = 80</code> — Variable ต้องมี <code>.Value</code>",
        "Console ก่อน / หลัง: 0:01:00 → 0:00:45 · 60 → 80",
    ])
)}
<p>โค้ดใน PythonModule <code>ReadWrite</code> (Frame P2_ReadWrite › ดับเบิลคลิก ReadWrite › Import):</p>
''' + CODE_READWRITE + f'''
<div class="tip"><strong>อ่านง่าย ๆ:</strong> current . ชื่อวัตถุ . ชื่อค่า — เหมือน SimTalk แค่ขึ้นต้นด้วย current
· Frame P2_ReadWrite: Source (ปล่อยงานทุก 30 วินาที) → Station (ProcTime 1:00) → Drain และ Variable ชื่อ Target = 60
· Python คืนค่า ProcTime เป็นชนิดเวลา (timedelta) จึงพิมพ์เป็น 0:01:00
· คำอื่นที่ใช้ชี้วัตถุ: <code>root</code> = Frame บนสุดที่มี EventController · <code>basis</code> = ราก Class Library (<code>basis.Models.P2_ReadWrite.Station</code>) · <code>self</code> = PythonModule เอง</div>

<h2>ขั้นที่ 4: ผล — รัน 1 ชั่วโมง ได้ 79 ชิ้น (เดิม 59)</h2>
{screenshot("assets/images/lessons/09-07.jpg", "Frame P2_ReadWrite หลังรัน (ซ้าย) และ Drain › Statistics (ขวา)")}
{step_list([
    "<code>Target: 80</code> — ค่าที่ Python เขียนลง Variable แสดงบน Frame",
    "<code>Station</code> — ทำงานชิ้นละ 45 วินาทีแล้ว (เดิม 60)",
    "<code>Drain</code> — <code>Home</code> › <code>Start</code> รันจนจบ 1 ชั่วโมง แล้วดับเบิลคลิก Drain",
    "<strong>Entries 79</strong> — ชิ้นที่ออกจากไลน์ใน 1 ชั่วโมง · ก่อน Import ได้ 59",
])}
<div class="note"><strong>ค่าที่ Python เขียนจะอยู่ในโมเดล</strong> จนกว่าจะแก้กลับ · ไม่ Save = ไฟล์ไม่เปลี่ยน · จะกลับค่าเดิม: ดับเบิลคลิก Station ใส่ 1:00
· Source ปล่อยงานทุก 30 s จึงไม่ใช่คอขวด · Import ซ้ำได้ผลเหมือนเดิมเพราะโค้ดเขียนค่าคงที่ 45 และ 80</div>

<h2>ขั้นที่ 5: P3_Function — สร้างฟังก์ชันด้วย def</h2>
{side_by_side(
    screenshot("assets/images/lessons/09-08.jpg", "หน้าต่าง PythonModule Calc และ Console OEE = 84.6 %"),
    step_list([
        "<code>def oee(availability, performance, quality):</code> — ชื่อฟังก์ชัน + ค่าที่รับเข้า ลงท้ายด้วย <code>:</code>",
        "ย่อหน้า 4 ช่อง — บรรทัดที่ย่อหน้าคือเนื้อในของฟังก์ชัน",
        "<code>return</code> — ส่งผลลัพธ์กลับ = A × P × Q",
        "<code>Import</code> — รันบรรทัด print ท้ายไฟล์ เพื่อทดสอบ",
        "<strong>OEE = 84.6 %</strong> — 0.90 × 0.95 × 0.99 = 0.84645 → <code>percent()</code> ปัดเป็น 84.6",
    ])
)}
<p>โค้ดใน PythonModule <code>Calc</code> (Frame P3_Function › ดับเบิลคลิก Calc › Import):</p>
''' + CODE_CALC + f'''
<div class="tip"><strong>ฟังก์ชันคืออะไร:</strong> สูตรที่ตั้งชื่อไว้ เรียกใช้ซ้ำกี่ครั้งก็ได้ · <code>percent(oee(...))</code> = ส่งผลของ oee เข้า percent ต่อ
· <code>round(x * 100, 1)</code> = คูณ 100 แล้วปัดทศนิยม 1 ตำแหน่ง · OEE = Availability × Performance × Quality (ดู OEE ใน<a href="lessons-03.html">บท 03</a>)
· ไม่ต้องติดตั้งอะไรเพิ่ม ใช้ได้กับ Python ทุกเครื่อง</div>

<h2>ขั้นที่ 5: Method เรียกฟังก์ชัน Python ด้วย .call</h2>
{side_by_side(
    screenshot("assets/images/lessons/09-09.jpg", "Method CallPython แท็บ Tools › Run และ Variable OEE บน Frame"),
    step_list([
        '<code>Calc.call("oee", 0.90, 0.95, 0.99)</code> — ชื่อฟังก์ชันอยู่ใน " " ตามด้วยค่าที่ส่งเข้า',
        "<code>OEE := r</code> — ใน SimTalk เขียน Variable ตรง ๆ ไม่มี .Value",
        "แท็บ <code>Tools</code> ของหน้าต่าง Method",
        "<code>Run</code> — รัน Method นี้",
        "<strong>OEE: 0.84645</strong> — Variable บน Frame ได้ค่าจาก Python",
        "Console: <code>OEE from Python =0.84645</code>",
    ])
)}
<p>โค้ด SimTalk ใน Method <code>CallPython</code> (ดับเบิลคลิก CallPython › Tools › Run):</p>
''' + CODE_CALLPYTHON + f'''
<div class="tip"><strong>ไม่ต้องกด Import ก่อน:</strong> <code>.call</code> โหลดโค้ดให้เอง (ใช้ได้ทันทีหลังเปิดไฟล์)
· ส่งค่าแบบระบุชื่อ: <code>Calc.callKw("oee", ["availability", 0.8, …])</code> ได้ 0.72
· นี่คือวิธีที่ใช้บ่อยที่สุด: เขียนสูตรยาก ๆ ใน Python แล้วให้ Method ของ SimTalk เรียกใช้ระหว่างรัน</div>
<div class="note"><strong>ระวังความต่าง:</strong> ใน Python ต้องเขียน <code>current.OEE.Value</code> แต่ใน SimTalk เขียน <code>OEE := r</code>
(ถ้าใส่ .Value ใน SimTalk จะขึ้น error: <em>A 'real' cannot accept the method 'Value'</em>)</div>

<h2>ขั้นที่ 6: P4_Data — เก็บเวลาที่ชิ้นงานเสร็จลงตาราง</h2>
{screenshot("assets/images/lessons/09-10.jpg", "Frame P4_Data (ซ้าย) และตาราง PartLog หลังรัน 8 ชั่วโมง (ขวา)")}
{step_list([
    "<code>Station</code> — เวลาสุ่ม Uniform 30–80 วินาที",
    "<code>Drain</code> › <code>Controls</code> › <code>Entrance</code> = <code>LogPart</code> — เรียก Method ทุกครั้งที่ชิ้นงานเข้า",
    "<code>LogPart</code> — <code>PartLog.writeRow(1, PartLog.YDim + 1, เลขชิ้น, SimTime)</code>",
    "<code>Init</code> — ล้างตารางเมื่อเริ่มรัน (<code>PartLog.delete</code>)",
    "<code>PartLog</code> — 517 แถว · Time = วินาทีที่ชิ้นงานเสร็จ",
])}
<div class="tip"><strong>ส่วนนี้เป็น SimTalk ทั้งหมด</strong> (<a href="lessons-07.html">บท 07</a>) เพื่อเตรียมข้อมูลให้ Python วิเคราะห์ในขั้นถัดไป
· <code>Home</code> › <code>Start</code> รัน 8 ชั่วโมง ได้ 517 ชิ้น · ชื่อตารางใช้ Log ไม่ได้ เพราะเป็นคำสงวนของ SimTalk จึงตั้งชื่อ PartLog</div>

<h2>ขั้นที่ 6: Analyse — pandas นับชิ้นงานต่อชั่วโมง</h2>
{side_by_side(
    screenshot("assets/images/lessons/09-11.jpg", "หน้าต่าง PythonModule Analyse และผลใน Console"),
    step_list([
        "<code>import pandas as pd</code> — เรียกใช้ไลบรารี ตั้งชื่อย่อ pd",
        "<code>rows = current.PartLog[None]</code> — อ่านทั้งตาราง แถวแรก = หัวตาราง",
        "<code>pd.DataFrame(rows[1:], columns=rows[0])</code> — ทำเป็นตารางของ pandas",
        '<code>groupby("Hour").size()</code> — นับจำนวนแถวในแต่ละชั่วโมง',
        "<code>Import</code> — รันทั้งหมด 1.2 วินาที",
        "ชั่วโมงละ 62–67 ชิ้น — ผลของ <code>print(per_hour)</code>",
        "<strong>Mean per hour: 64.6</strong> — ค่าเฉลี่ยต่อชั่วโมง",
    ])
)}
<p>โค้ดใน PythonModule <code>Analyse</code> บรรทัด 1–17 (ดับเบิลคลิก Analyse › Import หลังรันจบ):</p>
''' + CODE_ANALYSE + f'''
<div class="note"><strong>ต้องรันโมเดลให้จบก่อนกด Import:</strong> ถ้าตารางว่างจะได้ Parts: 0
· <code>Hour = (Time // 3600) + 1</code> คือหารเอาส่วนเต็มด้วย 3600 วินาที แล้วบวก 1 ให้ชั่วโมงแรกเป็น 1
· ตรวจแล้ว: นับเองจากตาราง PartLog ได้ 67, 64, 64, 62, 65, 65, 64, 66 ตรงกับ pandas</div>

<h2>ขั้นที่ 6: matplotlib วาดกราฟแท่ง แล้วบันทึกเป็นรูป</h2>
{screenshot("assets/images/lessons/09-12.jpg", "ท้ายโค้ด Analyse (ซ้าย) และไฟล์ P4_parts_per_hour.png (ขวา)")}
{step_list([
    '<code>per_hour.plot(kind="bar")</code> — กราฟแท่งจากผลนับ',
    "<code>set_xlabel</code> / <code>set_ylabel</code> / <code>set_title</code> — ชื่อแกนและหัวกราฟ",
    "<code>plt.savefig(path)</code> — บันทึกรูปข้างไฟล์โมเดล (<code>ps.getCurrentDirectory()</code>)",
    "ชั่วโมงที่ 4 ต่ำสุด 62 ชิ้น — เห็นความผันผวนทันทีจากกราฟ",
])}
<p>ท้ายโค้ด Analyse บรรทัด 19–28:</p>
''' + CODE_PLOT + f'''
<div class="tip"><strong>matplotlib.use("Agg"):</strong> วาดลงไฟล์ ไม่เปิดหน้าต่าง · ถ้าใช้ <code>plt.show()</code> ต้องปิดหน้าต่างกราฟก่อนกลับไปใช้ Plant Simulation (Help 2606)
· สีแดงตั้งด้วย <code>color="#FA000F"</code> · บรรทัด 20 ในภาพยาวเกินขอบหน้าต่าง (ตรง <code>…</code>) เปิด Analyse ในไฟล์ 09_Python.spp เพื่อดูบรรทัดเต็ม
· ต่อยอด: บันทึกเป็น Excel ด้วย <code>df.to_excel(...)</code> (ต้อง <code>pip install openpyxl</code> เพิ่ม ยังไม่ได้ทดสอบในบทนี้)</div>

<h2>สรุป: คำสั่ง Python ที่ใช้ในบทนี้</h2>
<table>
<tr><th>คำสั่ง</th><th>ทำอะไร</th><th>Frame</th></tr>
<tr><td><code>print("…")</code> · <code>a = 7</code> · <code># …</code></td><td>แสดงผล · สร้างตัวแปร · คอมเมนต์</td><td>P1_Hello</td></tr>
<tr><td><code>current.Station.ProcTime = 45</code></td><td>อ่าน / เขียนค่าของวัตถุใน Frame เดียวกัน</td><td>P2_ReadWrite</td></tr>
<tr><td><code>current.Target.Value = 80</code></td><td>อ่าน / เขียน Variable (ใน Python ต้องมี .Value)</td><td>P2_ReadWrite</td></tr>
<tr><td><code>def oee(a, p, q):  return a * p * q</code></td><td>สร้างฟังก์ชัน (ย่อหน้า 4 ช่อง)</td><td>P3_Function</td></tr>
<tr><td><code>Calc.call("oee", 0.9, 0.95, 0.99)</code></td><td>SimTalk เรียกฟังก์ชัน Python แล้วรับผลกลับ</td><td>P3_Function</td></tr>
<tr><td><code>current.PartLog[None]</code> · <code>pd.DataFrame</code></td><td>อ่านทั้งตาราง แล้วทำเป็นตาราง pandas</td><td>P4_Data</td></tr>
<tr><td><code>groupby(...).size()</code> · <code>plot</code> · <code>savefig</code></td><td>นับตามกลุ่ม · วาดกราฟ · บันทึกรูป</td><td>P4_Data</td></tr>
</table>

<h2>ลองเอง: แก้ตัวเลขในโค้ดแล้วดูผล</h2>
<table>
<tr><th>Frame</th><th>ลองเปลี่ยน</th><th>ผล (วัดจริง 2606)</th><th>เรียนรู้อะไร</th></tr>
<tr><td>P1_Hello</td><td><code>print(a * b)</code></td><td>63 (7 × 9)</td><td><code>*</code> = คูณ</td></tr>
<tr><td>P2_ReadWrite</td><td>ProcTime = 30 แล้ว Start</td><td>119 ชิ้น/ชม.</td><td>Python คุมค่าโมเดลได้</td></tr>
<tr><td>P2_ReadWrite</td><td>ProcTime = 60 (ค่าเดิม)</td><td>59 ชิ้น/ชม.</td><td>เทียบกับ 45 s = 79</td></tr>
<tr><td>P3_Function</td><td><code>Calc.callKw("oee", ["availability", 0.8, "performance", 0.9, "quality", 1.0])</code></td><td>0.72</td><td>ส่งค่าแบบระบุชื่อ</td></tr>
<tr><td>P4_Data</td><td>Station Uniform 30–60 s แล้วรัน + Import</td><td>638 ชิ้น · เฉลี่ย 79.8</td><td>เวลาสั้นลง ผลิตได้มากขึ้น</td></tr>
<tr><td>P4_Data</td><td>Station Uniform 50–60 s</td><td>522 ชิ้น · 64–66 ต่อชม.</td><td>เฉลี่ยใกล้ 30–80 s แต่นิ่งกว่า (62–67)</td></tr>
</table>
<div class="tip"><strong>หลังลอง:</strong> แก้ Station กลับเป็น Uniform 30–80 · ผล <code>print(a * b)</code> = 7 × 9 คิดเอง ไม่ได้รัน
· แถวสุดท้ายเป็นข้อคิดที่ดี: ค่าเฉลี่ยเวลาเท่ากัน (55 s) แต่ช่วงสุ่มแคบกว่า ผลผลิตแต่ละชั่วโมงจึงนิ่งกว่า กราฟจาก matplotlib ช่วยให้เห็นความต่างนี้ทันที</div>

<h2>ปัญหาที่พบบ่อย และวิธีแก้</h2>
<table>
<tr><th>อาการ</th><th>วิธีแก้</th></tr>
<tr><td>กด Import แล้วไม่เห็นอะไร</td><td>แท็บ <code>Window</code> › <code>Console</code></td></tr>
<tr><td><em>Access to the computer is prohibited</em></td><td><code>File</code> › <code>Model Settings</code> › <code>General</code>: คลิกช่อง Prohibit Access to the Computer ให้เครื่องหมายถูกหายไป ☐ แล้ว Save</td></tr>
<tr><td><em>ModuleNotFoundError: No module named 'pandas'</em></td><td>pip install pandas ใน Python ตัวที่ Plant Simulation ใช้ · มีหลายตัวใช้ <code>setPythonDLLPath</code></td></tr>
<tr><td><em>IndentationError</em></td><td>บรรทัดในฟังก์ชันต้องย่อหน้าเท่ากัน (4 ช่อง)</td></tr>
<tr><td><em>SyntaxError</em> ตรง <code>:=</code></td><td>Python ใช้ = ตัวเดียว (<code>:=</code> เป็นของ SimTalk)</td></tr>
<tr><td>Method: <em>A 'real' cannot accept the method 'Value'</em></td><td>ใน SimTalk เขียน <code>OEE := r</code> ไม่ต้องมี .Value (Python ต้องมี)</td></tr>
<tr><td>Plant Simulation ค้างหลังใช้ pandas แล้วเปิดไฟล์ใหม่</td><td>ปิด Plant Simulation แล้วเปิดใหม่ทุกครั้งที่เปลี่ยนไฟล์ (Help 2606)</td></tr>
<tr><td>ตั้งชื่อตาราง Log ไม่ได้</td><td>Log เป็นคำสงวนของ SimTalk ใช้ชื่ออื่น เช่น PartLog</td></tr>
</table>
<div class="tip"><strong>Prohibit Access to the Computer:</strong> พบจริงใน<a href="overview-04.html">Python GA Demo</a> (โมเดลตัวอย่างของ Siemens เปิดไว้ ☑)
— ไฟล์ 09_Python.spp ปิดไว้ ☐</div>

<h2>แหล่งเรียนต่อ</h2>
<ul>
<li>Plant Simulation Help 2606 · PythonModule (หน้า 6640–6677) · setPythonDLLPath (หน้า 9617)</li>
<li>Siemens: วิดีโอ PythonModule บน YouTube (ลิงก์จาก Help 2606) — <a href="https://youtu.be/2QJeW5r1AF4" target="_blank" rel="noopener">youtu.be/2QJeW5r1AF4</a></li>
<li>python.org › Downloads › Windows — <a href="https://www.python.org/downloads/windows/" target="_blank" rel="noopener">www.python.org/downloads/windows/</a></li>
<li>Igor Kunjavskij, Plant Simulation 2404 Python module (User Conference 2024)</li>
</ul>
<div class="tip"><strong>ขั้นต่อไป:</strong> Help 2606 › Examples Collection › Tools › NeuralNetworks (scikit-learn ทำนายผลจากโมเดล)
· <a href="overview-04.html">Python GA Demo</a> (GA หลายเป้าหมายด้วย pymoo)</div>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ใน P2_ReadWrite Python เขียน <code>current.Target.Value = 80</code> แต่ใน Method CallPython ของ P3_Function
เขียน <code>OEE := r</code> โดยไม่มี .Value — ถ้าเผลอเขียน <code>OEE.Value := r</code> ใน Method จะเกิดอะไรขึ้น และต้องแก้อย่างไร?
</div>
<div class="tip"><strong>เฉลย:</strong> Method จะขึ้น error <em>A 'real' cannot accept the method 'Value'</em> เพราะใน SimTalk เขียน Variable ตรง ๆ ได้เลย
ให้แก้เป็น <code>OEE := r</code> — ส่วนใน Python ต้องมี <code>.Value</code> เสมอเมื่ออ่าน / เขียน Variable</div>
'''
