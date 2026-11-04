# -*- coding: utf-8 -*-
"""Lessons 8: AMR -- AGVPool and GAWizard -- from 08_AMR.pptx"""
from gen_site import screenshot, step_list, side_by_side

OBJECTIVES = [
    "สั่ง AGV ใน AGVPool ให้วิ่งผ่าน Marker ด้วย setRoute และ Destination ได้",
    "เขียน Method ขอรถว่าง (getIdleAGV) รับ-ส่งชิ้นงาน แล้วคืนรถเข้าพูลได้",
    "สั่งเส้นทางจาก DataTable และคิดระยะทาง น้ำมัน CO₂ ต่อปีใน ENDSIM ได้",
    "ใช้ GAWizard หาลำดับ Marker ที่สั้นที่สุด และอ่านผลก่อน-หลัง GA ได้",
]

BODY = f'''
<p class="lead" style="max-width:46em;">บทนี้ใช้ <strong>AGVPool</strong> และ <strong>Marker</strong> สร้าง AMR / AGV ที่วิ่งอิสระ
(ไม่ต้องมี Track เหมือนใน<a href="lessons-06.html">บท 06</a>) แล้วสั่งรถทีละคำสั่งด้วย Method ใน 8 ขั้นตอน: เริ่มจากสั่งรถคันแรกวิ่งผ่าน Marker
ให้รถรับ-ส่งชิ้นงาน ใช้รถหลายคัน สร้าง class AGV ของตัวเอง แล้วปิดท้ายด้วยโจทย์เส้นทาง ที่ให้ <strong>GAWizard</strong>
หาลำดับ Marker ที่สั้นที่สุด พร้อมคิดระยะทาง น้ำมัน และ CO₂ ต่อปี</p>

<div class="tip">
<strong>สิ่งที่ต้องมี:</strong> Plant Simulation 2606 · ไฟล์ <code>08_AMR.spp</code> (6 เฟรม) · พื้นฐาน Method จาก<a href="lessons-07.html">บท 07</a>
&nbsp;·&nbsp; ผลที่วัดได้ใน 2606: <strong>359 ชิ้น/ชม.</strong> เมื่อมี AGV 2 คันขึ้นไป (ขั้นที่ 4) · GA ลดเวลาวิ่ง <strong>24%</strong> (ขั้นที่ 8)
</div>

<h2>ภาพรวม: 8 ขั้นตอน จากสั่ง AGV คันแรก ถึง GA หาเส้นทาง</h2>
<table>
<tr><th>ขั้นที่</th><th>เรื่อง</th><th>ทำอะไร</th></tr>
<tr><td>1</td><td>setRoute</td><td>สั่งให้วิ่งผ่าน Marker ตามลำดับ</td></tr>
<tr><td>2</td><td>Destination</td><td>บอกจุดปลาย รถหาทางตาม Connector เอง</td></tr>
<tr><td>3</td><td>รับ-ส่งชิ้นงาน</td><td>move ขึ้นรถ / ลงจากรถ</td></tr>
<tr><td>4</td><td>หลายคัน</td><td>getIdleAGV · NumIdleAGVs · Exit Control</td></tr>
<tr><td>5</td><td>class AGV ของตัวเอง</td><td>Duplicate Transporter · Load Bay 1 x 1</td></tr>
<tr><td>6</td><td>เส้นทางจากตาราง</td><td>DataTable + INIT setRoute</td></tr>
<tr><td>7</td><td>ระยะทาง น้ำมัน CO₂</td><td>ENDSIM คิดผลต่อปี</td></tr>
<tr><td>8</td><td>GAWizard</td><td>หาลำดับ Marker ที่สั้นที่สุด</td></tr>
</table>

<h2>6 Frame ในไฟล์นี้</h2>
<table>
<tr><th>Frame</th><th>ใช้ในขั้นที่</th><th>เรื่อง</th></tr>
<tr><td><code>Model_setRoute</code></td><td>1</td><td>AGVPool + Marker 2 จุด สั่ง setRoute</td></tr>
<tr><td><code>Model_Destination</code></td><td>2</td><td>Marker ต่อ Connector บอกแค่ปลายทาง</td></tr>
<tr><td><code>Model_Load_Unload</code></td><td>3</td><td>รับชิ้นงานจาก Source ไปส่ง Station</td></tr>
<tr><td><code>Model_NumIdleAGVs</code></td><td>4</td><td>AGV 4 คัน + Exit Control</td></tr>
<tr><td><code>Model_Distance</code></td><td>5</td><td>class AGV ของตัวเอง</td></tr>
<tr><td><code>Model</code></td><td>6–8</td><td>โจทย์เส้นทาง Marker 4 จุด + GAWizard</td></tr>
</table>
<p>ขั้นที่ 1–5 ใช้ AGVPool + Marker เหมือนกันทุกเฟรม เพิ่มคำสั่งทีละเรื่อง ขั้นที่ 6–8 คือโจทย์เส้นทางที่ให้ GA จัดลำดับ Marker</p>

<h2>ลำดับการเรียน และผลวัดจริงใน Plant Simulation 2606</h2>
<table>
<tr><th>ลำดับ</th><th>งาน</th><th>คำสั่ง</th><th>Frame</th></tr>
<tr><td>1</td><td>สั่งเส้นทาง</td><td>setRoute / Destination (ขั้นที่ 1–2)</td><td>Model_setRoute</td></tr>
<tr><td>2</td><td>รับ-ส่งงาน</td><td>move ขึ้นรถ ลงรถ (ขั้นที่ 3)</td><td>Model_Load_Unload</td></tr>
<tr><td>3</td><td>หลายคัน</td><td>getIdleAGV + class AGV (ขั้นที่ 4–5)</td><td>Model_NumIdleAGVs</td></tr>
<tr><td>4</td><td>ตาราง + ผลต่อปี</td><td>DataTable, ENDSIM (ขั้นที่ 6–7)</td><td>Frame Model</td></tr>
<tr><td>5</td><td>GA หาเส้นทาง</td><td>GAWizard (ขั้นที่ 8)</td><td>GAWizard</td></tr>
</table>
<table>
<tr><th>AGV 1 คัน</th><th>AGV 2 คันขึ้นไป</th><th>ก่อน GA</th><th>หลัง GA</th></tr>
<tr><td>196 ชิ้น/ชม.</td><td>359 ชิ้น/ชม.</td><td>38 วินาที/รอบ</td><td>29 วินาที/รอบ</td></tr>
</table>

<h2>ขั้นที่ 1: Model_setRoute — AGVPool และ Marker 2 จุด</h2>
<p><code>08_AMR.spp › Model_setRoute</code> · วัตถุอยู่ใน <code>Toolbox › Resources</code></p>
{screenshot("assets/images/lessons/08-01.jpg", "Frame Model_setRoute และหน้าต่าง AGVPool")}
{step_list([
    "<strong>AGVPool</strong> ที่จอดและที่เก็บรถ AGV",
    "<strong>Marker</strong> จุดที่รถวิ่งไป",
    "<strong>Marker1</strong> จุดที่ 2",
    "<strong>INIT</strong> Method ที่ทำงานเองตอนเริ่มรัน",
    "<code>AGV = *.MUs.Transporter</code> class ของรถ",
    "<code>Amount = 1</code> จำนวนรถในพูล",
])}
<div class="tip"><strong>ไม่ต้องมี Track:</strong> Marker ไม่ต้องต่อ Connector ในเฟรมนี้ รถวิ่งเป็นเส้นตรงจากจุดหนึ่งไปอีกจุด (AGV วิ่งอิสระ)</div>

<h2>ขั้นที่ 1: INIT สั่ง setRoute แล้วรัน</h2>
<p>ดับเบิลคลิก <code>INIT</code> (ซ้าย) · <code>Home › Start</code> มุมมอง 3D ที่ 6 วินาที (ขวา)</p>
{screenshot("assets/images/lessons/08-02.jpg", "โค้ด INIT สั่ง setRoute และรถวิ่งในมุมมอง 3D")}
{step_list([
    "<code>AGVPool.cont.setRoute([Marker,Marker1])</code>",
    "<code>AGVPool.cont</code> = รถคันแรกในพูล",
    "รถวิ่งไป Marker แล้วไป Marker1 จบที่ <strong>12.99 วินาที</strong>",
])}
<div class="tip"><strong>End = 0:</strong> EventController ไม่ได้ตั้งเวลาจบ งานหมดเมื่อไรโมเดลหยุดเอง · setRoute รับรายการ Marker ในวงเล็บเหลี่ยม <code>[ ]</code> รถวิ่งผ่านทีละจุดตามลำดับ</div>

<h2>ขั้นที่ 2: Model_Destination — บอกจุดปลาย รถหาทางเอง</h2>
<p><code>08_AMR.spp › Model_Destination</code> · ดับเบิลคลิก <code>INIT</code></p>
{screenshot("assets/images/lessons/08-03.jpg", "Marker ที่ต่อ Connector และโค้ด Destination")}
{step_list([
    "Connector AGVPool → Marker → Marker1",
    "Connector AGVPool → Marker1 (ทางตรง)",
    "<code>AGVPool.cont.Destination := Marker1</code>",
    "รถเลือกทางตาม Connector ไปถึง Marker1 ที่ <strong>9.49 วินาที</strong> (ขั้นที่ 1 ผ่าน Marker ใช้ 12.99)",
])}
<div class="tip"><strong>setRoute กับ Destination:</strong> setRoute = กำหนดทุกจุดเอง · Destination = บอกแค่ปลายทาง รถหาเส้นทางในเครือข่าย Connector ของ Marker เอง</div>

<h2>ขั้นที่ 3: Model_Load_Unload — รับชิ้นงานไปส่ง Station</h2>
<p><code>08_AMR.spp › Model_Load_Unload</code> · ดับเบิลคลิก <code>INIT</code></p>
{screenshot("assets/images/lessons/08-04.jpg", "Frame Model_Load_Unload และโค้ด INIT รับ-ส่งชิ้นงาน")}
{step_list([
    "<strong>Source</strong> ชิ้นงาน Part",
    "<strong>Station</strong> 10 วินาที",
    "<strong>Marker</strong> จุดรับงานข้าง Source",
    "<strong>Marker1</strong> จุดส่งงานข้าง Station",
    "<code>waituntil AGV.DestinationWasReached</code> รอรถถึงก่อน",
    "<code>Source.cont.move(AGV)</code> ขึ้นรถ · <code>AGV.cont.move(Station)</code> ลงรถ",
])}
<pre><code>var AGV:=AGVPool.cont
AGV.setRoute([Marker])
waituntil AGV.DestinationWasReached
Source.cont.move(AGV)

AGV.setRoute([Marker1])
waituntil AGV.DestinationWasReached
AGV.cont.move(Station)</code></pre>
<div class="tip"><strong>ไม่มี Connector:</strong> ระหว่าง Source กับ Station ไม่มี Connector ชิ้นงานไปถึง Station ได้เพราะ Method ย้ายขึ้นรถและลงรถเอง</div>

<h2>ขั้นที่ 3: ผล — ส่งงาน 1 ชิ้นแล้วจบ</h2>
<p><code>Home › Start</code> · มุมมอง 3D ที่ 8 วินาที</p>
{screenshot("assets/images/lessons/08-05.jpg", "AGV รับชิ้นงานไปวางที่ Station ในมุมมอง 3D")}
{step_list([
    "รถรับชิ้นงานที่ Marker แล้ววิ่งไป Marker1",
    "วางลง Station ทำงาน 10 วินาที",
    "INIT ทำงานครั้งเดียว: ส่ง 1 ชิ้น โมเดลหยุดที่ <strong>19.64 วินาที</strong> (Station ทำงาน 51% ของเวลา)",
])}
<div class="note"><strong>ต่อไป:</strong> อยากให้ส่งต่อเนื่อง ต้องเรียก Method ทุกครั้งที่มีชิ้นงาน → ขั้นที่ 4</div>

<h2>ขั้นที่ 4: Model_NumIdleAGVs — AGV 4 คัน และ Exit Control</h2>
<p><code>08_AMR.spp › Model_NumIdleAGVs</code> · <code>Source › Controls</code></p>
{screenshot("assets/images/lessons/08-06.jpg", "Frame Model_NumIdleAGVs และแท็บ Controls ของ Source")}
{step_list([
    "<code>AGVPool Amount = 4</code>",
    "<strong>Method</strong> โค้ดรับ-ส่งงาน",
    "<strong>Display</strong> NumIdleAGVs (รถว่าง) และ StatAverageTraveledDistance",
    "<strong>Drain</strong> หลัง Station",
    "Source แท็บ <code>Controls</code>",
    "<code>Exit = Method</code> เรียก Method ทุกครั้งที่ชิ้นงานจะออกจาก Source",
])}
<div class="tip"><strong>Exit Control:</strong> ทำให้ Method ทำงานใหม่ทุกชิ้น ชิ้นงานหลายชิ้นจึงได้รถคนละคันพร้อมกัน</div>

<h2>ขั้นที่ 4: โค้ด — ขอรถว่าง ส่งงาน แล้วคืนรถ</h2>
<p>ดับเบิลคลิก <code>Method</code></p>
{screenshot("assets/images/lessons/08-07.jpg", "โค้ด Method ขอรถว่าง ส่งงาน และคืนรถ")}
{step_list([
    "<code>waituntil AGVPool.NumIdleAGVs &gt; 0</code> รอจนมีรถว่าง",
    "<code>AGVPool.getIdleAGV</code> หยิบรถว่าง 1 คัน",
    "ไป Marker แล้ว <code>Source.cont.move(AGV)</code>",
    "<code>waituntil Station.Empty</code> รอ Station ว่าง",
    "<code>AGV.cont.move(Station)</code>",
    "<code>AGV.isIdle := True</code> กลับ Marker แล้วคืนรถเข้าพูล",
])}
<pre><code>waituntil AGVPool.NumIdleAGVs &gt; 0
var AGV:=AGVPool.getIdleAGV


AGV.setRoute([Marker])
waituntil AGV.DestinationWasReached
Source.cont.move(AGV)

AGV.setRoute([Marker1])
waituntil AGV.DestinationWasReached
waituntil Station.Empty
AGV.cont.move(Station)

AGV.setRoute([Marker])
waituntil AGV.DestinationWasReached
AGV.isIdle := True</code></pre>
<div class="note"><strong>ลืม isIdle:</strong> ถ้าไม่ตั้ง <code>isIdle := True</code> รถคันนั้นไม่ถูกเรียกอีก ใช้งานได้คันละรอบ</div>
<div class="tip"><strong>หลายตัวพร้อมกัน:</strong> Method เดียวกันทำงานพร้อมกันหลายตัว (ชิ้นละตัว) แต่ละตัวถือรถของตัวเองในตัวแปร <code>AGV</code></div>

<h2>ขั้นที่ 4: ผล 1 ชั่วโมง — Station ทำงานเกือบเต็ม</h2>
<p>รันถึง 1:00:00 (ซ้าย) · มุมมอง 3D ที่ 2 นาที (ขวา)</p>
{screenshot("assets/images/lessons/08-08.jpg", "ผลรัน 1 ชั่วโมงและมุมมอง 3D ของ AGV 4 คัน")}
{step_list([
    "<code>NumIdleAGVs = 0</code> ตอนจบไม่มีรถว่าง",
    "ระยะวิ่งเฉลี่ย <strong>1,648.7 m</strong> ต่อคันใน 1 ชม.",
    "Drain <strong>359 ชิ้น</strong> · Station 10 วินาที ทำได้สูงสุด 360 · ทำงาน 99.7%",
])}
<div class="note"><strong>หมายเหตุ:</strong> ตัวเลขนี้รัน 1 ชั่วโมง โดยตั้ง End ชั่วคราวเป็น 1:00:00 (ในไฟล์เป็น 0) · คอขวด = Station</div>

<h2>ขั้นที่ 5: Model_Distance — class AGV ของตัวเอง</h2>
<p><code>Class Library › UserObjects › AGV</code></p>
{screenshot("assets/images/lessons/08-09.jpg", "หน้าต่าง class AGV แท็บ Attributes และ Load Bay")}
{step_list([
    "<code>Length 1.41 m</code> รถเล็กกว่า Transporter (1.6 m)",
    "<code>Speed 1 m/s</code>",
    "แท็บ <code>Load Bay</code>",
    "<code>X-Dimension 1</code>",
    "<code>Y-Dimension 1</code> บรรทุกครั้งละ 1 ชิ้น (Transporter 3 x 2 = 6)",
    "AGVPool ของเฟรมนี้ <code>AGV = *.UserObjects.AGV</code>",
])}
<div class="tip"><strong>สร้าง class เอง:</strong> <code>Class Library › MUs › Transporter</code> คลิกขวา <code>Duplicate</code> ย้ายไป UserObjects ตั้งชื่อ AGV แล้วแก้ค่า รถทุกคันในพูลใช้ค่าจาก class นี้</div>
<div class="note"><strong>ผล 1 ชม.:</strong> 359 ชิ้นเท่าขั้นที่ 4 · ระยะวิ่งเฉลี่ย 1,646.9 m (เดิม 1,648.7) — งานนี้รถรับทีละชิ้นอยู่แล้ว</div>

<h2>ลองเอง: ต้องใช้ AGV กี่คัน (ขั้นที่ 4)</h2>
<table>
<tr><th>AGVPool Amount</th><th>Drain 1 ชม.</th><th>Station ทำงาน</th><th>ระยะวิ่งเฉลี่ย/คัน</th><th>อ่านว่า</th></tr>
<tr><td>1 คัน</td><td>196 ชิ้น</td><td>54.6%</td><td>3,600 m</td><td>รถวิ่งตลอด ไม่ทัน Station</td></tr>
<tr><td>2 คัน</td><td>359 ชิ้น</td><td>99.7%</td><td>3,287.7 m</td><td>พอแล้ว = เพดานของ Station</td></tr>
<tr><td>3 คัน</td><td>359 ชิ้น</td><td>99.7%</td><td>2,195.0 m</td><td>ผลเท่าเดิม รถเริ่มว่าง</td></tr>
<tr><td>4 คัน (ในไฟล์)</td><td>359 ชิ้น</td><td>99.7%</td><td>1,648.7 m</td><td>เกินความต้องการ</td></tr>
<tr><td>5 คัน</td><td>359 ชิ้น</td><td>99.7%</td><td>1,320.9 m</td><td>ระยะต่อคันลด ผลไม่เพิ่ม</td></tr>
</table>
<div class="tip"><strong>วิธีลอง:</strong> วัดจริงใน PtS 2606 · Model_NumIdleAGVs รัน 1 ชั่วโมง · แก้ <code>AGVPool › Amount</code> แล้วกด <code>Reset</code> ก่อน <code>Start</code>
— ถ้ารถยังอยู่ในโมเดล Plant Simulation ไม่ยอมลด Amount ให้น้อยกว่าจำนวนรถที่มี</div>

<h2>ขั้นที่ 6: Frame Model — AGV 1 คัน วิ่งผ่าน Marker 4 จุด</h2>
<p><code>08_AMR.spp › Frame Model</code> · ไม่มีสายพาน มีแต่เส้นทาง</p>
{screenshot("assets/images/lessons/08-10.jpg", "Frame Model ที่มี AGVPool, Marker M1–M4, DataTable, INIT, ENDSIM และ GAWizard")}
{step_list([
    "<strong>AGVPool</strong> รถ 1 คัน จอดที่ [5, -1] m",
    "<strong>Marker M1–M4</strong> จุดที่ต้องไป วางเป็นสี่เหลี่ยม 9 × 6 m",
    "<strong>DataTable</strong> ลำดับ Marker ที่รถจะวิ่ง",
    "<strong>INIT</strong> Method ที่รันเองตอนเริ่ม สั่งเส้นทาง",
    "<strong>ENDSIM</strong> Method ที่รันเองตอนจบ คิดผล",
    "<strong>Variable</strong> Rounds, Km, L, CO แสดงผล",
    "<strong>GAWizard</strong> ใช้ในขั้นที่ 8",
])}
<div class="tip"><strong>INIT และ ENDSIM:</strong> Method ชื่อนี้ถูกเรียกเองตอน Reset/เริ่ม และตอนจบการรัน (ไม่ต้องผูกกับวัตถุใด) ·
รถวิ่งครบเส้นทางแล้วหยุด ไม่มี event เหลือ การรันจึงจบเองก่อน End 1 ชั่วโมง ·
เฟรมนี้มาจากโมเดลตัวอย่างที่ทำใน Plant Simulation 2504 เปิดบน 2606 ได้เลยโดยไม่ต้องแก้</div>

<h2>ขั้นที่ 6: AGVPool และ Marker</h2>
<p>ดับเบิลคลิก <code>AGVPool</code> (ซ้าย) · ดับเบิลคลิก <code>M1</code> (ขวา)</p>
{screenshot("assets/images/lessons/08-11.jpg", "หน้าต่าง AGVPool และ Marker M1")}
{step_list([
    "<code>AGV = *.MUs.Transporter</code> รถมาตรฐาน 1 m/s · 1 วินาที = 1 เมตร",
    "<code>Amount = 1</code> รถ 1 คันพอสำหรับโจทย์เส้นทาง",
    "<code>Use Rotation of Marker</code> รถหันตามทิศของ Marker เมื่อวิ่งถึง",
    "<code>Name</code> ชื่อ M1–M4 คือชื่อที่ DataTable อ้างถึง",
])}
<div class="note"><strong>ระยะห่าง Marker:</strong> วาง Marker ห่างกันอย่างน้อย 3 m (ใกล้กว่านี้ AGV อาจหยุดเงียบ)</div>

<h2>ขั้นที่ 6: DataTable — คอลัมน์ 1 ชนิด Object เก็บลำดับ Marker</h2>
<p>ดับเบิลคลิก <code>DataTable</code> · คลิกหัวคอลัมน์ 1 › <code>List › Edit Format</code></p>
{screenshot("assets/images/lessons/08-12.jpg", "DataTable และหน้าต่าง List Format แท็บ Data Type")}
{step_list([
    "คลิกหัวคอลัมน์ 1 เลือกทั้งคอลัมน์",
    "<code>Edit Format</code> ริบบอน <code>List › Format</code>",
    "<code>Data Type = Object</code> แท็บ Data Type › <code>OK</code>",
    "พิมพ์ M1, M2, M3, M4 ทีละแถว (แสดงเป็น <code>*.Models.Model.M1</code>) = เรียงตามชื่อ",
])}
<div class="tip"><strong>ทำไมเรียงตามชื่อ:</strong> ในไฟล์ตัวอย่าง 2504 ลำดับเดิมคือ M1, M2, M4, M3 ซึ่งสั้นที่สุดอยู่แล้ว บทนี้จึงเริ่มจาก M1–M4 ให้เห็นว่า GA หาคำตอบที่ดีกว่าได้ ·
คอลัมน์ 2 และ 3 เป็นเลขแถวเดิม ไม่ได้ใช้ในเส้นทาง</div>

<h2>ขั้นที่ 6: Method INIT — สั่งเส้นทางจากตาราง</h2>
<p>ดับเบิลคลิก <code>INIT</code> · โค้ดเปิดในแท็บของหน้าต่างหลัก</p>
{screenshot("assets/images/lessons/08-13.jpg", "โค้ด INIT สั่ง setRoute จาก DataTable")}
{step_list([
    "<code>/* ... */</code> วิธีเดิม: อ่านทีละช่องใส่ x1–x4 แล้วสั่ง <code>setRoute([x1,x2,x3,x4])</code> (ปิดไว้เป็นคอมเมนต์)",
    "<code>AGVPool.cont.setRoute(DataTable)</code> ส่งทั้งตาราง รถวิ่งตามลำดับแถว 1 → 4 สั้นกว่าและเพิ่ม Marker ได้โดยไม่แก้โค้ด",
])}
<pre><code>/*
var x1 := DataTable[1,1]
var x2 := DataTable[1,2]
var x3 := DataTable[1,3]
var x4 := DataTable[1,4]
AGVPool.cont.setRoute([x1,x2,x3,x4])
*/
AGVPool.cont.setRoute(DataTable)</code></pre>
<div class="tip"><strong>AGVPool.cont:</strong> คือรถคันแรกในโรงจอด · INIT ทำงานเองหลัง Reset เมื่อกด Start</div>
<div class="note"><strong>ต้องเป็น Object:</strong> setRoute รับ list หรือ table ที่คอลัมน์ 1 เป็น object ถ้าคอลัมน์เป็น string จะเกิด error
<em>object passed, string expected</em> — นี่คือเหตุผลที่ต้องตั้ง Data Type = Object ในหัวข้อก่อน</div>

<h2>ขั้นที่ 7: Method ENDSIM — ระยะทาง น้ำมัน CO₂ ต่อปี</h2>
<p>ดับเบิลคลิก <code>ENDSIM</code> (ซ้าย) · Variable บน Frame (ขวา)</p>
{screenshot("assets/images/lessons/08-14.jpg", "โค้ด ENDSIM และ Variable Rounds, Km, L, CO")}
{step_list([
    "<code>Rounds = 30,000</code> Variable ใหม่ (integer) สมมุติวิ่งวันละ 100 รอบ × 300 วัน",
    "<code>Km := ระยะทาง / 1000 × Rounds</code> StatTraveledDistance ของรถ (เมตร) → กิโลเมตรต่อปี",
    "<code>L := Km / 10</code> ดีเซล รถวิ่งได้ 10 km ต่อลิตร",
    "<code>CO := L × 2.9793</code> kgCO₂e ต่อลิตร ดีเซลใช้นอกถนน (เครื่องจักรในโรงงาน)",
])}
<pre><code>-- ระยะทางต่อปี (km) = ระยะทาง 1 รอบ (m) / 1000 x จำนวนรอบต่อปี
Km := AGVPool.cont.StatTraveledDistance / 1000 * Rounds
-- น้ำมันดีเซล (ลิตร): รถวิ่งได้ 10 km ต่อลิตร
L := Km / 10
-- การปล่อยคาร์บอน (kgCO2e): ดีเซลใช้นอกถนน 2.9793 kgCO2e ต่อลิตร
CO := L * 2.9793</code></pre>
<div class="tip"><strong>ที่มา:</strong> ตาราง Emission Factor ม.มหิดล 2024 (อ้าง IPCC และ พพ.) — ดีเซลใช้นอกถนน 2.9793, บนถนน 2.7406 kgCO₂e/ลิตร
(ดูหัวข้อที่มาท้ายบท) · ถ้าเป็นรถวิ่งบนถนนใช้ 2.7406</div>

<h2>ขั้นที่ 7: รัน — ลำดับ M1 → M2 → M3 → M4 ใช้ 38.36 วินาที</h2>
<p><code>Home › Start</code> · มุมมอง 3D ระหว่างรัน (ซ้าย) · ผลหลังรัน (ขวา)</p>
{screenshot("assets/images/lessons/08-15.jpg", "AGV วิ่งในมุมมอง 3D และผล Km, L, CO หลังรัน")}
{step_list([
    "<strong>AGV</strong> ออกจาก AGVPool ไป M1 → M2 แล้วตัดทแยงลงไป M3",
    "<strong>M1</strong> Marker เห็นใน 3D เป็นลูกศรสีส้ม",
    "<strong>Km 1,150.7 · L 115.1 · CO 342.8</strong> ระยะ 38.36 m ต่อรอบ × 30,000 รอบ",
])}
<div class="tip"><strong>ทำไมจบที่ 38.36 วินาที:</strong> รถวิ่ง 1 m/s ครบเส้นทางแล้วไม่มีงานต่อ การรันจึงหยุดเอง · SimTime จึงเท่ากับเวลาวิ่ง 1 รอบ ·
ภาพ 3D จับตอน SimTime 12 วินาที รถอยู่ที่ M2 · AGV ที่วิ่งอิสระเห็นในมุมมอง 3D เท่านั้น</div>

<h2>ขั้นที่ 8: GAWizard — แท็บ Define</h2>
<p>ดับเบิลคลิก <code>GAWizard › Define</code></p>
{side_by_side(
    screenshot("assets/images/lessons/08-16.jpg", "หน้าต่าง GAWizard แท็บ Define"),
    step_list([
        "<code>Minimum</code> ยิ่งน้อยยิ่งดี (เวลาวิ่ง)",
        "<code>Generations 5 · Size 10</code> 5 รุ่น รุ่นละ 10 คำตอบ",
        "<code>Optimization parameter</code> สิ่งที่ GA ปรับ = ลำดับแถวของ DataTable (หัวข้อถัดไป)",
        "<code>Fitness by table</code> ค่าที่ใช้ให้คะแนน = SimTime",
        "<code>Observations per individual = 1</code> โมเดลไม่มีค่าสุ่ม รัน 1 ครั้งพอ",
    ])
)}
<div class="note"><strong>GAWizard ใน 2606:</strong> ไม่อยู่ใน Toolbox ต้องเพิ่มจาก <code>Home › Manage Class Library › Libraries › GA Wizard</code> ก่อน (ไฟล์นี้มีแล้ว)</div>
<div class="tip"><strong>จำนวนคำตอบ:</strong> GA ประเมินได้สูงสุด 10 + 2 × 10 × 4 = 90 คำตอบ ซึ่งมากกว่าลำดับที่เป็นไปได้ของ 4 Marker (24 แบบ)
โจทย์ 4 จุดจึงเป็นตัวอย่างสอน ประโยชน์จริงเห็นชัดเมื่อจุดมากขึ้น (ดูหัวข้อลองเองท้ายบท)</div>

<h2>ขั้นที่ 8: สิ่งที่ GA ปรับ และค่าที่ใช้ให้คะแนน</h2>
<p><code>Define › Optimization parameter › Open</code> (ซ้าย) · <code>Fitness › Open</code> (ขวา)</p>
{screenshot("assets/images/lessons/08-17.jpg", "ตาราง ProblemDefinition และตาราง Fitness ของ GAWizard")}
{step_list([
    "<code>Sequence of</code> งานแบบจัดลำดับ",
    "<code>root.DataTable</code> ตารางที่ GA สลับแถว · สร้างโดยกด Shift ค้างแล้วลาก DataTable ไปวางบน GAWizard",
    "<code>4 Elements</code> 4 แถว = Marker 4 จุด",
    "<code>root.EventController.SimTime</code> เวลาที่รันจบ = เวลาวิ่ง 1 รอบ",
    "<code>Weighting 1</code> มีค่าเดียว น้ำหนัก 1",
])}
<div class="tip"><strong>ใช้ระยะทางก็ได้:</strong> ตั้ง fitness เป็น <code>AGVPool.cont.StatTraveledDistance</code> ก็ได้ ที่ 1 m/s ได้ค่าเท่ากัน ·
ตาราง ProblemDefinition และ Fitness อยู่ใน GAWizard เปิดเป็นแท็บในหน้าต่างหลัก</div>

<h2>ขั้นที่ 8: แท็บ Run › Start</h2>
<p><code>Run › Start</code> · ใช้เวลาไม่ถึง 1 วินาที</p>
{side_by_side(
    screenshot("assets/images/lessons/08-18.jpg", "หน้าต่าง GAWizard แท็บ Run หลังรันจบ"),
    step_list([
        "<code>Reset</code> ล้างผล GA ครั้งก่อน",
        "<code>Start</code> GA รันโมเดลซ้ำ ทีละคำตอบ",
        "<code>Best fitness value 29.1416</code> เวลาวิ่งที่ดีที่สุด (วินาที)",
        "<code>Current generation 5</code> ครบ 5 รุ่นแล้วหยุด",
        "<code>Set Parameters</code> ใส่เลขคำตอบ แล้วกดเพื่อนำลำดับนั้นกลับใส่ DataTable",
    ])
)}
<div class="note"><strong>GA สุ่ม:</strong> รันใหม่อาจได้คำตอบต่างไปเล็กน้อย รอบที่วัดเจอ 29.14 ในรุ่นที่ 5 (รุ่น 1–4 ดีสุด 30.65) · เพิ่ม Generations ถ้ายังไม่เจอ</div>
<table>
<tr><th>รุ่น</th><th>ดีสุด (s)</th><th>เฉลี่ย (s)</th><th>แย่สุด (s)</th></tr>
<tr><td>1</td><td>30.65</td><td>38.61</td><td>45.35</td></tr>
<tr><td>2</td><td>30.65</td><td>33.74</td><td>38.17</td></tr>
<tr><td>3</td><td>30.65</td><td>31.67</td><td>34.03</td></tr>
<tr><td>4</td><td>30.65</td><td>30.77</td><td>31.27</td></tr>
<tr><td>5</td><td>29.14</td><td>30.50</td><td>30.65</td></tr>
</table>
<p>วัดจริงใน 2606: 5 รุ่น × 10 ประเมินจริง 90 ครั้ง ใช้เวลา 0.5 วินาที</p>

<h2>ขั้นที่ 8: แท็บ Evaluate — คำตอบดีที่สุด และกราฟรายรุ่น</h2>
<p><code>Evaluate › Best individuals › Show</code> (ซ้าย) · <code>Evolution › Show</code> (ขวา)</p>
{side_by_side(
    screenshot("assets/images/lessons/08-19.jpg", "ตาราง Best individuals ของ GAWizard"),
    screenshot("assets/images/lessons/08-20.jpg", "กราฟ Evolution ค่า fitness รายรุ่น")
)}
{step_list([
    "<code>Gen 5 Ind 10</code> คำตอบที่ดีที่สุด (รุ่น 5 ตัวที่ 10)",
    "<code>Fitness 29.1416</code> ถัดไป 30.65, 31.27 … เรียงจากดีไปแย่",
    "<strong>เส้นแดง</strong> = ดีที่สุดในรุ่น ลดลงในรุ่นที่ 5",
    "<strong>เส้นเขียว</strong> = ค่าเฉลี่ย ลดลงทุกรุ่น ทั้งรุ่นดีขึ้น",
])}
<div class="tip"><strong>อ่านกราฟ:</strong> แกนตั้งของกราฟ Evolution แสดงค่า fitness ที่ GA ปรับสเกลแล้ว (0.29–0.46) ไม่ใช่วินาทีโดยตรง ดูรูปทรงของเส้นพอ</div>

<h2>ขั้นที่ 8: ผลหลัง GA — M1 → M2 → M4 → M3</h2>
<p>เปิด <code>DataTable</code> (ซ้าย) · <code>Start</code> อีกครั้ง (ขวา)</p>
{screenshot("assets/images/lessons/08-21.jpg", "DataTable หลัง GA และผล Km, L, CO ใหม่")}
{step_list([
    "แถว 3–4 สลับกัน รถวิ่งรอบสี่เหลี่ยม ไม่ตัดทแยง",
    "<strong>Km 874.2 · L 87.4</strong> จาก 1,150.7 km และ 115.1 ลิตรต่อปี",
    "<strong>CO 260.5 kgCO₂e</strong> ลดลง 82.4 kg ต่อปี (−24%)",
])}
<div class="tip"><strong>อ่านผล:</strong> ลำดับเดิมในไฟล์ตัวอย่าง 2504 (M1, M2, M4, M3) คือคำตอบที่ GA หาเจอ · ลำดับตามชื่อไม่ใช่ทางสั้นที่สุดเสมอไป ·
หลัง GA จบ DataTable เรียงตามคำตอบที่ดีที่สุดให้เลย ถ้าไม่ใช่ ให้ใช้ <code>Run › Set Parameters</code> ใส่เลขคำตอบ · SimTime หลังรันใหม่ = 29.14 วินาที</div>

<h2>สรุปผล: ก่อน GA เทียบหลัง GA (วัดใน 2606)</h2>
<table>
<tr><th>หัวข้อ</th><th>ก่อน GA</th><th>หลัง GA</th><th>ต่าง</th></tr>
<tr><td>ลำดับใน DataTable</td><td>M1 → M2 → M3 → M4</td><td>M1 → M2 → M4 → M3</td><td>สลับ 2 แถวสุดท้าย</td></tr>
<tr><td>เวลา / ระยะ 1 รอบ</td><td>38.36 s · 38.36 m</td><td>29.14 s · 29.14 m</td><td>−24%</td></tr>
<tr><td>ระยะทางต่อปี (30,000 รอบ)</td><td>1,150.7 km</td><td>874.2 km</td><td>−276.4 km</td></tr>
<tr><td>น้ำมันดีเซลต่อปี (10 km/L)</td><td>115.1 ลิตร</td><td>87.4 ลิตร</td><td>−27.6 ลิตร</td></tr>
<tr><td>CO₂ ต่อปี (2.9793 kg/L)</td><td>342.8 kgCO₂e</td><td>260.5 kgCO₂e</td><td>−82.4 kgCO₂e</td></tr>
</table>
<p>GAWizard 5 รุ่น × 10 · ประเมิน 90 คำตอบ · 0.5 วินาที · จำนวนรอบต่อปีเป็นค่าสมมุติ เพื่อให้เห็นผลเป็นน้ำมัน/คาร์บอน</p>

<h2>ลองเอง: GA กับโจทย์ที่ใหญ่ขึ้น (ขั้นที่ 6–8)</h2>
<table>
<tr><th>ลองเปลี่ยน</th><th>ผล (วัดจริง 2606)</th><th>เรียนรู้อะไร</th></tr>
<tr><td>เพิ่ม M5 [13.5, -4] และ M6 [22.5, -4] ใส่ DataTable 6 แถว</td><td>เรียง M1–M6: 58.47 s → GA 5 × 10: 37.22 s</td><td>−36% ประเมิน 90 จาก 720 ลำดับ</td></tr>
<tr><td>ตรวจคำตอบ: รันครบทั้ง 720 ลำดับ</td><td>ดีที่สุด 37.22 s (มี 2 ลำดับเท่ากัน) · แย่สุด 81.72 s</td><td>GA เจอคำตอบที่ดีที่สุดจริง</td></tr>
<tr><td>6 Marker, GA 10 × 20</td><td>37.22 s (ประเมิน 380)</td><td>ไม่ดีขึ้นอีก = ถึงคำตอบแล้ว</td></tr>
<tr><td><code>.MUs.Transporter</code> Speed = 2 m/s</td><td>SimTime 19.18 s ระยะทางเท่าเดิม 38.36 m</td><td>SimTime ใช้เทียบได้เมื่อความเร็วคงที่</td></tr>
<tr><td>Rounds = 50,000</td><td>1,917.8 km · 191.8 L · 571.4 kgCO₂e</td><td>ผลต่อปีโตตามจำนวนรอบ</td></tr>
</table>
<div class="tip"><strong>เพิ่ม Marker:</strong> คลิกขวา M1 › <code>Duplicate</code> หรือ <code>Toolbox › Resources › Marker</code> แล้วเปลี่ยนชื่อ · GA จะนับจำนวนแถวใหม่หลังกด <code>Reset</code> ในแท็บ Run ·
720 ลำดับใช้เวลารันทั้งหมด 43 วินาที ส่วน GA ใช้ 0.3 วินาที · แก้ Speed กลับเป็น 1 หลังลอง</div>

<h2>ปัญหาที่พบบ่อย และวิธีแก้ (2606)</h2>
<table>
<tr><th>อาการ</th><th>วิธีแก้</th></tr>
<tr><td>AGV ไม่ขยับ / Method หยุดเงียบ</td><td>เปิด Method ดูบรรทัดที่ผิด · ชื่อ Marker ต้องตรงกับโค้ด</td></tr>
<tr><td>ไม่เห็น AGV วิ่ง</td><td>AGV วิ่งอิสระเห็นในมุมมอง 3D เท่านั้น</td></tr>
<tr><td><code>setRoute(DataTable)</code> error: object passed, string expected</td><td>คอลัมน์ 1 ของ DataTable ต้องเป็น Data Type = Object (Edit Format)</td></tr>
<tr><td>หา GAWizard ใน Toolbox ไม่เจอ</td><td><code>Home › Manage Class Library › Libraries</code> › คลิกช่อง GA Wizard ให้ขึ้นเครื่องหมายถูก ☑ › <code>OK</code></td></tr>
<tr><td>GA ได้คำตอบไม่เท่ากันทุกครั้ง</td><td>GA สุ่ม · เพิ่ม Number of generations หรือ Size of generation แล้วรันใหม่</td></tr>
<tr><td>Km / L / CO ยังเป็นค่าเก่า</td><td>ENDSIM ทำงานตอนจบการรันเท่านั้น · กด <code>Reset</code> แล้ว <code>Start</code> ให้รันจนจบ</td></tr>
</table>

<h2>ที่มาของตัวเลข และลิงก์อ้างอิง</h2>
<ul>
<li>ตาราง Emission Factor ม.มหิดล 2024 (อ้าง IPCC และ พพ.) — ดีเซลใช้นอกถนน 2.9793, บนถนน 2.7406 kgCO₂e/ลิตร:
<a href="https://rasen.mahidol.ac.th/wp-content/uploads/2024/08/EF-CFO.pdf" target="_blank" rel="noopener">rasen.mahidol.ac.th/…/EF-CFO.pdf</a></li>
<li>สถาบันสิ่งแวดล้อมไทย (TEI) ฉลากลดคาร์บอน — ดีเซล 2.770 kgCO₂e/ลิตร:
<a href="https://tei.or.th/carbonreductionlabel/step-e.html" target="_blank" rel="noopener">tei.or.th/carbonreductionlabel/step-e.html</a></li>
<li>ฐานข้อมูล Emission Factor ของ อบก. (TGO) — ตรวจค่าล่าสุดก่อนใช้กับงานจริง:
<a href="https://thaicarbonlabel.tgo.or.th" target="_blank" rel="noopener">thaicarbonlabel.tgo.or.th</a></li>
<li>Plant Simulation Help 2606 หัวข้อ <em>Load Parts Onto an AGV</em> (หน้า 2287) · AGVPool, Marker, setRoute, GAWizard</li>
</ul>
<div class="note"><strong>ใช้ค่าไหน:</strong> บทนี้ใช้ 2.9793 kgCO₂e/ลิตร (ดีเซลใช้นอกถนน) เพราะ AGV / รถในโรงงานไม่ได้วิ่งบนถนน ·
ค่าทางการล่าสุดของ อบก. ยังไม่ได้ตรวจ ให้ตรวจก่อนใช้ตัวเลขกับงานจริง</div>

<div class="note">
<strong>คำถามฝึกคิด:</strong> ในหัวข้อลองเองของขั้นที่ 4 ทำไมเพิ่ม AGV จาก 2 เป็น 3, 4, 5 คันแล้ว Drain ยังได้ 359 ชิ้นเท่าเดิม?
และถ้าอยากได้มากกว่านี้ควรแก้ที่ไหน?
</div>
<div class="tip"><strong>เฉลย:</strong> เพราะคอขวดคือ Station — ทำชิ้นละ 10 วินาที ทำได้สูงสุด 360 ชิ้น/ชม. และที่ 2 คันขึ้นไป Station ทำงานแล้ว 99.7%
รถที่เพิ่มจึงแค่ว่างมากขึ้น (ระยะวิ่งต่อคันลดจาก 3,287.7 m เหลือ 1,320.9 m) ผลไม่เพิ่ม ถ้าอยากได้มากกว่า 360 ต้องแก้ที่ Station ไม่ใช่จำนวนรถ —
หลักเดียวกับ<a href="lessons-02.html">บท 02 คอขวด และ ParallelStation</a></div>
'''
