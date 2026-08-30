# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_site import page_html, write

BODY = '''        <section id="banner">
          <h1>เรียนรู้ Siemens Tecnomatix Plant Simulation</h1>
          <p class="tagline">เว็บไซต์สอนการใช้งานโปรแกรมจำลองการผลิตและโลจิสติกส์ (Discrete Event Simulation) ภาษาไทย</p>
          <p class="intro">
            เนื้อหาแบ่งเป็น 3 ระดับ ตั้งแต่ยังไม่เคยเปิดโปรแกรมมาก่อน ไปจนถึงเขียนสคริปต์ SimTalk
            ควบคุมโมเดลและทำ Optimization อัตโนมัติ พร้อมส่วนอ้างอิง Object, Case Study จากอุตสาหกรรมจริง
            และ Tips and Tricks — เลือกเริ่มจากระดับที่ตรงกับพื้นฐานของคุณได้เลย
          </p>
        </section>

        <div class="features">
          <div class="feature">
            <h3>🎯 เรียงตามลำดับการใช้งานจริง</h3>
            <p>แต่ละบทต่อยอดจากบทก่อนหน้า ไม่ต้องท่องจำ ทำตามได้ทันที</p>
          </div>
          <div class="feature">
            <h3>🧪 มีตัวอย่างและคำถามฝึกคิด</h3>
            <p>ทุกบทมีตัวอย่างที่ลองทำตามได้ พร้อมคำถามท้ายบทเพื่อเช็กความเข้าใจ</p>
          </div>
          <div class="feature">
            <h3>✅ Syntax ที่ยืนยันแล้วจริง</h3>
            <p>โค้ด SimTalk ในระดับ Advanced อ้างอิงจาก syntax ที่ทดสอบรันได้จริง ไม่ใช่ตัวอย่างทั่วไป</p>
          </div>
        </div>

        <h2>เลือกระดับที่จะเรียน</h2>
        <div class="card-grid">
          <a href="basic.html" class="card">
            <div class="icon">🧩</div>
            <h3>Basic — พื้นฐาน</h3>
            <p>รู้จักหน้าตาโปรแกรม, Object พื้นฐาน, สร้างโมเดลแรกและรันซิมูเลชัน (6 บท)</p>
          </a>
          <a href="intermediate.html" class="card">
            <div class="icon">🔧</div>
            <h3>Intermediate — ขั้นกลาง</h3>
            <p>MU, Distribution แบบสุ่ม, Failure, Bottleneck Analyzer และการจัดกลุ่มโมเดล (6 บท)</p>
          </a>
          <a href="advanced.html" class="card">
            <div class="icon">⚙️</div>
            <h3>Advanced — ขั้นสูง</h3>
            <p>เขียนสคริปต์ SimTalk, สร้าง Object ด้วยโค้ด, Experiment Manager, GAWizard และ COM automation (7 บท)</p>
          </a>
        </div>

        <h2>เนื้อหาเสริม</h2>
        <div class="card-grid">
          <a href="object-reference.html" class="card">
            <div class="icon">📖</div>
            <h3>Object Reference</h3>
            <p>สาธิตการทำงานของแต่ละ Object เป็นหมวดหมู่ ใช้เปิดอ้างอิงเร็วๆ (3 หมวด)</p>
          </a>
          <a href="step-by-step.html" class="card">
            <div class="icon">🗂️</div>
            <h3>Step-by-Step File</h3>
            <p>เดินตามไฟล์สอนต้นฉบับของ Siemens (18 เฟรม) ทีละหัวข้อ จัดกลุ่มใหม่เป็น 8 บท</p>
          </a>
          <a href="case-study.html" class="card">
            <div class="icon">🏭</div>
            <h3>Case Study</h3>
            <p>ตัวอย่างการใช้งานจากสถานการณ์จริงใน 4 อุตสาหกรรม</p>
          </a>
          <a href="tips-tricks.html" class="card">
            <div class="icon">💡</div>
            <h3>Tips and Tricks</h3>
            <p>เทคนิคเล็กๆ น้อยๆ ที่ช่วยประหยัดเวลาและลดข้อผิดพลาด (4 หมวด)</p>
          </a>
        </div>

        <h2>Plant Simulation คืออะไร?</h2>
        <p class="lead">
          Plant Simulation (Tecnomatix Plant Simulation) เป็นซอฟต์แวร์จำลองสถานการณ์แบบ Discrete Event Simulation (DES)
          ของ Siemens ใช้สำหรับจำลองกระบวนการผลิต สายการประกอบ คลังสินค้า และระบบโลจิสติกส์ ก่อนลงทุนจริง
          ช่วยให้วิศวกรวิเคราะห์คอขวด (Bottleneck), อัตราการใช้งานเครื่องจักร (Utilization), และ Throughput ได้โดยไม่ต้องหยุดสายการผลิตจริง
        </p>

        <h2>ตัวอย่างไฟล์</h2>
        <p>
          มีไฟล์ตัวอย่างจริงประกอบเนื้อหาบางบทที่ <a href="examples.html">หน้า Example File</a>
          และในโฟลเดอร์ <code>examples/</code> ของ repo นี้
        </p>'''

if __name__ == "__main__":
    write("index.html", page_html("หน้าแรก", BODY, active_top="index"))
