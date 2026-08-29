# -*- coding: utf-8 -*-
"""Generator for the Plant Simulation Tutorial site's boilerplate-heavy pages.
All body/nav content is authored using the old flat filenames (e.g. "basic-01.html",
"object-reference-01.html") as href targets -- write() below relocates every page into
its section folder (basic/01.html, object-reference/01.html, ...) and rewrites every
href/src that points at a known old flat filename to the correct relative path for
the new location. This means chapter bodies never need to know their own folder depth.
"""
import os
import re
import posixpath

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

FONT_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@300;400;500;600;700&family=Noto+Sans+Thai:wght@300;400;500;600;700&display=swap">'''

SECTIONS = {
    "basic": {
        "label": "Basic — พื้นฐาน",
        "hub": "basic.html",
        "chapters": [
            "Plant Simulation คืออะไร",
            "หน้าตาโปรแกรม",
            "Object พื้นฐาน 6 ตัว",
            "สร้างโมเดลแรก",
            "รันและอ่านผล Statistics",
            "บันทึกและเปิดไฟล์โมเดล",
        ],
    },
    "intermediate": {
        "label": "Intermediate — ขั้นกลาง",
        "hub": "intermediate.html",
        "chapters": [
            "Object ขั้นกลาง",
            "MU และ MU Class",
            "ค่าที่ไม่คงที่ (Distribution)",
            "ความเสียหายของเครื่องจักร",
            "Chart และ Bottleneck Analyzer",
            "จัดกลุ่มโมเดลเป็น Sub-frame",
        ],
    },
    "advanced": {
        "label": "Advanced — ขั้นสูง",
        "hub": "advanced.html",
        "chapters": [
            "SimTalk 2.0 พื้นฐาน",
            "Method ผูกกับ Event",
            "DataTable และ Variable",
            "สร้าง Object ด้วยโค้ด",
            "Experiment Manager",
            "Optimization ด้วย GAWizard",
            "ควบคุมจากภายนอกผ่าน COM/Python",
        ],
    },
    "object-reference": {
        "label": "Object Reference — สาธิต Object",
        "hub": "object-reference.html",
        "chapters": [
            "Material Flow Objects",
            "Information Flow Objects",
            "Resources &amp; Tools",
        ],
    },
    "case-study": {
        "label": "Case Study — ตัวอย่างอุตสาหกรรม",
        "hub": "case-study.html",
        "chapters": [
            "อุตสาหกรรมยานยนต์ (Automotive)",
            "คลังสินค้าและโลจิสติกส์ (Warehouse &amp; Logistics)",
            "อิเล็กทรอนิกส์ (Electronics / SMT)",
            "อาหารและเครื่องดื่ม (Food &amp; Beverage)",
        ],
    },
    "tips-tricks": {
        "label": "Tips and Tricks — เทคนิคการทำงาน",
        "hub": "tips-tricks.html",
        "chapters": [
            "UI และ Workflow",
            "การสร้างโมเดลและดีบัก",
            "ประสิทธิภาพการรัน (Performance)",
            "SimTalk และ Scripting",
        ],
    },
}

SECTION_ORDER = ["basic", "intermediate", "advanced", "object-reference", "case-study", "tips-tricks"]


def chapter_filename(section, idx):
    return f"{section}-{idx:02d}.html"


def sidebar_html(expand_section=None, active_top=None, active_chapter=None):
    parts = []
    parts.append('      <nav id="menu">')
    parts.append('        <header class="major"><h2>เมนู</h2></header>')
    parts.append('        <ul>')
    home_active = ' class="active"' if active_top == "index" else ''
    parts.append(f'          <li{home_active}><a href="index.html">หน้าแรก</a></li>')

    for sec in SECTION_ORDER:
        info = SECTIONS[sec]
        li_classes = ["has-children"]
        if expand_section == sec:
            li_classes.append("expanded")
        if active_top == sec and active_chapter is None:
            li_classes.append("active")
        cls = " ".join(li_classes)
        parts.append(f'          <li class="{cls}">')
        parts.append(f'            <a href="{info["hub"]}">{info["label"]}</a>')
        parts.append(f'            <button class="submenu-toggle" aria-label="แสดง/ซ่อนเมนู {sec}">▾</button>')
        parts.append('            <ul class="submenu">')
        for i, title in enumerate(info["chapters"], start=1):
            fname = chapter_filename(sec, i)
            li_active = ' class="active"' if (active_top == sec and active_chapter == i) else ''
            parts.append(f'              <li{li_active}><a href="{fname}">{i}. {title}</a></li>')
        parts.append('            </ul>')
        parts.append('          </li>')

    ex_active = ' class="active"' if active_top == "examples" else ''
    parts.append(f'          <li{ex_active}><a href="examples.html">Example File</a></li>')
    parts.append('        </ul>')
    parts.append('      </nav>')
    return "\n".join(parts)


def page_html(title, body, expand_section=None, active_top=None, active_chapter=None):
    sb = sidebar_html(expand_section, active_top, active_chapter)
    return f'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Plant Simulation Tutorial</title>
{FONT_LINKS}
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div id="wrapper">
  <div id="main">
    <div class="inner">
      <header id="header">
        <a href="index.html" class="logo"><span>Plant Simulation Tutorial</span></a>
        <button class="menu-toggle" aria-label="เปิดเมนู">☰</button>
      </header>

      <main>
{body}
      </main>

      <footer class="site-footer">
        Plant Simulation Tutorial — เอกสารประกอบการเรียนรู้ภายในทีม
      </footer>
    </div>
  </div>

  <div id="sidebar">
    <div class="inner">
{sb}
      <footer id="footer"><p class="copyright">Plant Simulation Tutorial — เอกสารประกอบการเรียนรู้ภายในทีม</p></footer>
    </div>
  </div>
  <div id="sidebar-overlay"></div>
</div>
<script src="assets/main.js"></script>
</body>
</html>
'''


def hub_page(section):
    info = SECTIONS[section]
    cards = []
    for i, title in enumerate(info["chapters"], start=1):
        fname = chapter_filename(section, i)
        desc = HUB_CARD_DESC[section][i - 1]
        cards.append(f'''          <a href="{fname}" class="card">
            <div class="icon number">{i}</div>
            <h3>{title}</h3>
            <p>{desc}</p>
          </a>''')
    cards_html = "\n".join(cards)

    prev_section = None
    idx = SECTION_ORDER.index(section)
    prev_html = '<a href="index.html">← กลับหน้าแรก</a>'
    if idx > 0:
        prev_sec = SECTION_ORDER[idx - 1]
        prev_html = f'<a href="{SECTIONS[prev_sec]["hub"]}">← ก่อนหน้า: {SECTIONS[prev_sec]["label"]}</a>'
    first_chapter = chapter_filename(section, 1)

    body = f'''        <h1>{info["label"]}</h1>
        <p class="lead" style="max-width:46em;">{HUB_INTRO[section]}</p>

        <div class="card-grid">
{cards_html}
        </div>

        <div class="page-nav">
          {prev_html}
          <a href="{first_chapter}">เริ่มบทที่ 1: {info["chapters"][0]} →</a>
        </div>'''
    return page_html(info["label"].split(" — ")[0], body, expand_section=section, active_top=section)


HUB_INTRO = {
    "basic": "สำหรับผู้ที่ยังไม่เคยเปิดโปรแกรมมาก่อน เริ่มจากรู้จักหน้าตาโปรแกรม ไปจนถึงสร้างและรันโมเดลจำลองแรกของคุณ ทั้งหมด 6 บท เรียงตามลำดับที่ควรทำตาม",
    "intermediate": "สำหรับผู้ที่สร้างโมเดลง่ายๆ ได้แล้ว และต้องการให้โมเดลสมจริงขึ้น — ใช้ Object เพิ่มเติม ค่าที่ไม่คงที่ ความเสียหายของเครื่องจักร และการวิเคราะห์ผลลัพธ์ ทั้งหมด 6 บท",
    "advanced": "สำหรับผู้ที่ต้องการควบคุมโมเดลด้วยสคริปต์ SimTalk สร้าง Object ด้วยโค้ด และทำ Optimization อัตโนมัติ ไปจนถึงควบคุมโปรแกรมจากภายนอกผ่าน COM ทั้งหมด 7 บท",
    "object-reference": "รวม Object ที่ใช้บ่อยเป็นหมวดหมู่ พร้อมสาธิตการทำงานสั้นๆ ที่ลองทำตามได้ทันที — ใช้เป็นที่เปิดหาอ้างอิงเร็วๆ เวลาจำไม่ได้ว่า Object ไหนใช้ทำอะไร",
    "case-study": "ตัวอย่างการใช้ Plant Simulation แก้โจทย์จริงจาก 4 อุตสาหกรรม เห็นภาพว่าความรู้แต่ละบทที่เรียนมาถูกเอาไปประกอบกันอย่างไรในสถานการณ์จริง",
    "tips-tricks": "เทคนิคเล็กๆ น้อยๆ ที่ช่วยประหยัดเวลาและลดข้อผิดพลาดในการทำงาน แบ่งเป็นหมวดตามลักษณะงาน",
}

HUB_CARD_DESC = {
    "basic": [
        "รู้จักแนวคิด Discrete Event Simulation และประโยชน์ของโปรแกรมนี้",
        "Class Library, Frame, Toolbar, Console — ส่วนประกอบหลักที่ต้องรู้จัก",
        "Source, Line, SingleProc, Buffer, Drain, EventController",
        "ลงมือสร้างสายการผลิตง่ายๆ ทีละขั้นตอน",
        "ดูค่า Working / Waiting / Blocked และความหมายของแต่ละค่า",
        "จัดการไฟล์ .spp อย่างปลอดภัย พร้อมนิสัยสำรองไฟล์ที่ควรมี",
    ],
    "intermediate": [
        "Buffer/Store, AssemblyStation, Track, Transporter — เมื่อไหร่ควรใช้ตัวไหน",
        "Part/Container/Transporter และการสร้าง MU class ของตัวเอง",
        "ตั้งค่า Interval/ProcTime แบบสุ่มตามสถิติแทนค่าคงที่",
        "จำลอง MTTR/MTBF ให้โมเดลสะท้อนความเสียหายของเครื่องจักรจริง",
        "อ่านผลลัพธ์เชิงลึกและหาคอขวดของสายการผลิต",
        "ห่อโมเดลย่อยเป็นโมดูลใช้ซ้ำได้หลายจุด",
    ],
    "advanced": [
        "Syntax ที่ยืนยันแล้วจริง — var, for...next, if...end",
        "ผูก Method เข้ากับ Entrance/Exit/Trigger ให้ทำงานอัตโนมัติตามเหตุการณ์",
        "เก็บและอ่านค่าข้อมูลจากโค้ด ด้วย DataTable และ Variable",
        "createObject และ Connector.connect — สร้างและต่อโมเดลด้วยสคริปต์ล้วนๆ",
        "รันหลาย Scenario เปรียบเทียบผลลัพธ์อัตโนมัติ",
        "ค้นหาค่าพารามิเตอร์ที่ดีที่สุดด้วย Genetic Algorithm",
        "เชื่อมต่อ Plant Simulation จาก Python ผ่าน COM สำหรับงาน automation",
    ],
    "object-reference": [
        "Source, Line, SingleProc, Buffer, Drain, EventController, AssemblyStation, Store, Track, Transporter, Diverter",
        "Method, Variable, DataTable, Trigger — Object ที่ขับเคลื่อนด้วยตรรกะและข้อมูล",
        "Worker/Resource, BottleneckAnalyzer, ExperimentManager, GAWizard",
    ],
    "case-study": [
        "จำลองสายการประกอบรถยนต์ วิเคราะห์คอขวดของสถานีติดตั้งชิ้นส่วน",
        "จำลองคลังสินค้าและระบบ AGV ขนย้ายพาเลท",
        "จำลองสาย SMT วางชิ้นส่วนอิเล็กทรอนิกส์ที่ต้องการความแม่นยำสูง",
        "จำลองสายบรรจุภัณฑ์อาหารที่มีข้อจำกัดเรื่องอายุการเก็บรักษา",
    ],
    "tips-tricks": [
        "ทางลัดและนิสัยที่ช่วยให้ทำงานในโปรแกรมเร็วขึ้น",
        "ข้อผิดพลาดที่เจอบ่อยและวิธีเช็คก่อนสรุปว่าโมเดลพัง",
        "เทคนิคทำให้รันโมเดลใหญ่เร็วขึ้นโดยไม่เสียความแม่นยำ",
        "กับดัก syntax และ COM ที่เจอบ่อยเวลาเขียนสคริปต์",
    ],
}


def youtube_embed(video_id, title, caption=None):
    """Responsive 16:9 YouTube embed. video_id is just the id (the part after
    watch?v= or youtu.be/), not the full URL. Uses youtube-nocookie.com."""
    cap_html = f'\n<p class="video-caption">{caption}</p>' if caption else ""
    return f'''<div class="video-embed">
  <iframe src="https://www.youtube-nocookie.com/embed/{video_id}" title="{title}"
          loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen></iframe>
</div>{cap_html}'''


def screenshot(img_path, alt, caption=None):
    """img_path is authored as a repo-root-relative path, e.g.
    'assets/images/basic/04-01.png' -- write() rewrites it for the page's
    actual folder depth automatically (see _relocate_links)."""
    cap_html = f'\n  <figcaption>{caption}</figcaption>' if caption else ""
    return f'''<figure class="screenshot">
  <img src="{img_path}" alt="{alt}" loading="lazy">{cap_html}
</figure>'''


def step_list(items):
    """Numbered circular-badge list (like the reference ZukenE3 style) instead
    of a plain browser <ol> counter. items is a list of HTML strings."""
    lis = "\n".join(
        f'    <li><span class="num">{i}</span><span class="text">{text}</span></li>'
        for i, text in enumerate(items, start=1)
    )
    return f'''<ol class="step-list">
{lis}
  </ol>'''


def side_by_side(left_html, right_html):
    """Two-column layout (image/diagram on the left, explanatory content such
    as a step_list() on the right) -- stacks to one column on narrow screens."""
    return f'''<div class="side-by-side">
  <div>{left_html}</div>
  <div>{right_html}</div>
</div>'''


def _build_old_to_new():
    mapping = {
        "index.html": "index.html",
        "examples.html": "examples.html",
        "assets/style.css": "assets/style.css",
        "assets/main.js": "assets/main.js",
    }
    for sec in SECTION_ORDER:
        info = SECTIONS[sec]
        mapping[info["hub"]] = f"{sec}/index.html"
        for i in range(1, len(info["chapters"]) + 1):
            mapping[chapter_filename(sec, i)] = f"{sec}/{i:02d}.html"
    return mapping


OLD_TO_NEW = _build_old_to_new()
_LINK_RE = re.compile(r'(href|src)="([^"]+)"')


def _relocate_links(html, new_relpath):
    cur_dir = posixpath.dirname(new_relpath) or "."

    def repl(m):
        attr, target = m.group(1), m.group(2)
        new_target = OLD_TO_NEW.get(target)
        if new_target is None:
            # assets/* (css/js/images) are authored as repo-root-relative paths
            # everywhere and always live at the repo root, regardless of how deep
            # the current page ended up -- no per-file registration needed.
            if target.startswith("assets/"):
                new_target = target
            else:
                return m.group(0)
        rel = posixpath.relpath(new_target, start=cur_dir)
        return f'{attr}="{rel}"'

    return _LINK_RE.sub(repl, html)


def write(relpath, content):
    new_relpath = OLD_TO_NEW.get(relpath, relpath)
    content = _relocate_links(content, new_relpath)
    path = os.path.join(ROOT, *new_relpath.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", new_relpath)


if __name__ == "__main__":
    for sec in SECTION_ORDER:
        if sec == "basic":
            continue  # regenerated by gen_chapters.py for full consistency
        write(SECTIONS[sec]["hub"], hub_page(sec))
