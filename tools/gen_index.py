# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_site import (SECTIONS, page_html, write, chapter_filename, chapter_numbers,
                      chapter_title, chapter_label, HUB_CARD_DESC)


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
        </div>'''

if __name__ == "__main__":
    write("index.html", page_html("หน้าแรก", BODY, active_top="index"))
