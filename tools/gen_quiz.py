# -*- coding: utf-8 -*-
"""Pre-test and post-test pages. The tests themselves are Google Forms (built by
_No_Upload/quiz/Code.gs, which also holds the answer key and is never committed);
these pages explain the test and embed the form whose link is set in gen_site.QUIZ_PAGES."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_site import QUIZ_PAGES, page_html, write, chapter_filename, chapter_numbers, chapter_title, chapter_label


def form_block(url):
    if not url:
        return '''
<div class="note"><strong>ยังไม่เปิดให้ทำ:</strong> แบบทดสอบนี้กำลังเตรียม — กลับมาอีกครั้งภายหลัง</div>'''
    embed = url + ("&" if "?" in url else "?") + "embedded=true"
    return f'''
<div class="download">
  <a class="download-btn" href="{url}" target="_blank" rel="noopener">เปิดแบบทดสอบในหน้าต่างใหม่</a>
  <p>แนะนำบนมือถือ หรือถ้าฟอร์มด้านล่างไม่แสดง</p>
</div>
<div class="form-embed">
  <iframe src="{embed}" title="แบบทดสอบ" loading="lazy">กำลังโหลด…</iframe>
</div>'''


def pre_body(info):
    first = chapter_numbers("overview")[0]
    return f'''        <h1>{info["title"]}</h1>
        <p class="lead" style="max-width:46em;">ก่อนเริ่มเรียน ทำแบบทดสอบ <strong>20 ข้อ</strong> (ปรนัย ข้อละ 1 คะแนน)
        และตอบแบบสอบถามความคาดหวังสั้นๆ ใช้เวลาประมาณ 15 นาที — ยังไม่ต้องรู้คำตอบทุกข้อ ตอบตามความเข้าใจตอนนี้</p>

<div class="tip"><strong>สำคัญ:</strong> กรอกอีเมลที่ใช้ประจำ และใช้อีเมลเดียวกันตอนทำ<a href="post-test.html">แบบทดสอบหลังเรียน</a>
— ใช้เทียบคะแนนก่อน–หลังเรียน และส่งผลสอบให้ทางอีเมล</div>
{form_block(info["form"])}

        <div class="page-nav">
          <a href="index.html">← หน้าแรก</a>
          <a href="{chapter_filename("overview", first)}">ถัดไป: เริ่มเรียน {chapter_label("overview", first)}. {chapter_title("overview", first)} →</a>
        </div>'''


def post_body(info):
    last = chapter_numbers("lessons")[-1]
    return f'''        <h1>{info["title"]}</h1>
        <p class="lead" style="max-width:46em;">เรียนครบแล้ว ทำแบบทดสอบ <strong>20 ข้อ</strong> ชุดเดียวกับก่อนเรียน (สลับลำดับข้อ)
        และประเมินการเรียน (Feedback) ใช้เวลาประมาณ 15 นาที ความเห็นของคุณช่วยปรับปรุงบทเรียนรอบต่อไป</p>

<div class="tip"><strong>สำคัญ:</strong> ใช้อีเมลเดียวกับตอนทำ<a href="pre-test.html">แบบทดสอบก่อนเรียน</a>
เพื่อเทียบคะแนนก่อน–หลังเรียน · ผลสอบจะส่งให้ทางอีเมล</div>
{form_block(info["form"])}

        <div class="page-nav">
          <a href="{chapter_filename("lessons", last)}">← ก่อนหน้า: {chapter_label("lessons", last)}. {chapter_title("lessons", last)}</a>
          <a href="index.html">กลับหน้าแรก</a>
        </div>'''


if __name__ == "__main__":
    for name, build in (("pre-test.html", pre_body), ("post-test.html", post_body)):
        info = QUIZ_PAGES[name]
        write(name, page_html(info["title"], build(info), active_top=name))
