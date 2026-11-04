# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_site import (SECTIONS, QUIZ_PAGES, page_html, write, chapter_filename, chapter_numbers,
                      chapter_title, chapter_label, HUB_CARD_DESC)


def quiz_card(page, badge, desc):
    return f'''        <div class="card-grid">
          <a href="{page}" class="card">
            <div class="icon number">{badge}</div>
            <h3>{QUIZ_PAGES[page]["title"]}</h3>
            <p>{desc}</p>
          </a>
        </div>'''


def cards(section):
    out = []
    for n, i in enumerate(chapter_numbers(section)):
        out.append(f'''          <a href="{chapter_filename(section, i)}" class="card">
            <div class="icon number">{chapter_label(section, i)}</div>
            <h3>{chapter_title(section, i)}</h3>
            <p>{HUB_CARD_DESC[section][n]}</p>
          </a>''')
    return "\n".join(out)


BODY = f'''        <section id="banner">
          <h1>เรียนรู้ Siemens Tecnomatix Plant Simulation</h1>
          <p class="tagline">ชุดสอน Step by Step บน Plant Simulation 2606 ภาษาไทย</p>
          <p class="intro">
            เริ่มจากรู้จักโปรแกรมและเปิดโมเดลตัวอย่าง แล้วสร้างโมเดลเองทีละบท ตั้งแต่ Source → Station → Drain
            ไปจนถึงคนงานและกะทำงาน การขนส่งด้วย Transporter และ AMR การเขียน SimTalk และการควบคุมด้วย Python
            — ทุกบทมีภาพหน้าจอจริงพร้อมเลขกำกับ และตัวเลขที่วัดจริงใน Plant Simulation 2606
          </p>
        </section>

        <h2>เริ่มที่นี่</h2>
{quiz_card("pre-test.html", "ก่อน", "แบบทดสอบ 20 ข้อ และความคาดหวังต่อการเรียน ประมาณ 15 นาที — ใช้เทียบคะแนนกับหลังเรียน")}

        <h2>{SECTIONS["overview"]["label"]}</h2>
        <p>รู้จัก Plant Simulation และเปิดโมเดลตัวอย่างที่ติดมากับโปรแกรม — ยังไม่ต้องสร้างโมเดลเอง</p>
        <div class="card-grid">
{cards("overview")}
        </div>

        <h2>Step by Step 01–09</h2>
        <p>สร้างโมเดลเองทีละบท แต่ละบทมีไฟล์ <code>.spp</code> ของบทที่มีหลาย Frame เล่าเรื่องเดียวกัน
        เปิดไฟล์ของบทได้เลย ไม่ต้องทำบทก่อนหน้าให้เสร็จ</p>
        <div class="card-grid">
{cards("lessons")}
        </div>

        <h2>เรียนจบแล้ว</h2>
{quiz_card("post-test.html", "หลัง", "แบบทดสอบ 20 ข้อชุดเดียวกับก่อนเรียน และประเมินการเรียน (Feedback) — ผลสอบส่งให้ทางอีเมล")}'''

if __name__ == "__main__":
    write("index.html", page_html("หน้าแรก", BODY, active_top="index"))
