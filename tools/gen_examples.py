# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_site import page_html, write

BODY = '''        <h1>Example File: ตัวอย่างโมเดลจริง</h1>
        <p class="lead" style="max-width:46em;">
          ไฟล์ตัวอย่างประกอบเนื้อหาแต่ละระดับ ฝึกทำตามเพื่อความเข้าใจที่ลึกขึ้น ไฟล์ <code>.spp</code> จริงวางเพิ่มได้ในโฟลเดอร์
          <code>examples/</code> ของ repo นี้
        </p>

        <div class="note">
          <strong>วิธีเพิ่มไฟล์ตัวอย่างจริง:</strong> วางไฟล์ <code>.spp</code> ลงในโฟลเดอร์ <code>examples/</code>
          แล้วใส่ลิงก์ดาวน์โหลดในหน้านี้ เช่น <code>&lt;a href="examples/line-01.spp"&gt;ดาวน์โหลด&lt;/a&gt;</code>
        </div>

        <h2>ตัวอย่างที่ 1: สายการผลิตเดี่ยว (Single Line)</h2>
        <p>เกี่ยวข้องกับ <a href="basic-01.html">Basic บทที่ 01</a></p>
        <p><strong>โครงสร้าง:</strong> <code>Source → Buffer → Station → Drain</code></p>
        <ul>
          <li>Source: สร้างชิ้นงานทุก 6 วินาที (Interval = 6s)</li>
          <li>Buffer: ความจุ 10 ชิ้น</li>
          <li>Station: เวลาแปรรูป 8 วินาที/ชิ้น</li>
        </ul>
        <p><strong>คำถามฝึกคิด:</strong> เพราะ Station ใช้เวลานานกว่า Source ผลิต (8s &gt; 6s) จะเกิดอะไรขึ้นกับ Buffer เมื่อรันไปนานๆ?</p>
        <div class="tip"><strong>เฉลย:</strong> Buffer จะเต็มเรื่อยๆ เพราะ Station ระบายชิ้นงานออกช้ากว่าที่ Source ป้อนเข้ามา สุดท้าย Source จะถูก Block — นี่คือตัวอย่างคอขวด (Bottleneck) แบบง่ายที่สุด</div>

        <h2>ตัวอย่างที่ 2: สายการผลิตคู่ขนาน (Parallel Stations)</h2>
        <p>เกี่ยวข้องกับ <a href="intermediate-01.html">Intermediate บทที่ 1</a> และ <a href="advanced-02.html">Advanced บทที่ 2</a></p>
        <p><strong>โครงสร้าง:</strong> <code>Source → (Station1 / Station2) → Drain</code> โดยใช้ Object ประเภท Sorter แยกชิ้นงานไปสองเส้นทาง</p>
        <p>Method ผูกกับ Sorter เพื่อเลือกเส้นทางแบบสลับกัน (round robin) — ใช้ตัวแปรนับรอบแยกต่างหาก (<code>RoundRobinCounter</code>
        เป็น Object ประเภท Variable) แทนการอิงค่าสถิติภายในของ Sorter เขียนด้วย SimTalk 2.0 syntax ที่ยืนยันแล้ว:</p>
        <pre><code>->void;
var target
RoundRobinCounter := RoundRobinCounter + 1
if RoundRobinCounter mod 2 = 0
    target := Station1
else
    target := Station2
end
@.MU := target</code></pre>

        <h2>ตัวอย่างที่ 3: เก็บสถิติ Throughput ด้วย Method</h2>
        <p>เกี่ยวข้องกับ <a href="advanced-02.html">Advanced บทที่ 2</a> และ <a href="advanced-03.html">บทที่ 3</a></p>
        <p>ผูก Method นี้ไว้ที่ <code>Drain.ExecuteAt.Entrance</code> เพื่อนับจำนวนชิ้นงานที่ผลิตสำเร็จต่อชั่วโมง
        (ต้องสร้างตัวแปร <code>GlobalCounter</code> เป็น Object ประเภท <strong>Variable</strong> ผ่าน <code>.Node("Variable")</code> ไว้ก่อนใช้งาน — ดู Advanced บทที่ 3)</p>
        <pre><code>->void;
GlobalCounter := GlobalCounter + 1
if EventController.SimTime > 0
    print "Throughput: " + to_str(GlobalCounter / (EventController.SimTime / 3600)) + " pcs/hour"
end</code></pre>

        <div class="page-nav">
          <a href="advanced-07.html">← ก่อนหน้า: Advanced บทที่ 7</a>
          <a href="index.html">กลับหน้าแรก</a>
        </div>'''

if __name__ == "__main__":
    write("examples.html", page_html("Example File", BODY, active_top="examples"))
