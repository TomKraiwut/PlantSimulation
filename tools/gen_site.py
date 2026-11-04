# -*- coding: utf-8 -*-
"""Generator for the Plant Simulation Tutorial site's boilerplate-heavy pages.
All body/nav content is authored using flat filenames (e.g. "overview-02.html",
"lessons-03.html") as href targets -- write() below relocates every page into
its section folder (overview/02.html, lessons/03.html, ...) and rewrites every
href/src that points at a known flat filename to the correct relative path for
the new location. This means chapter bodies never need to know their own folder depth.
"""
import hashlib
import os
import re
import posixpath

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def _asset_version(relpath):
    """Short content hash appended as ?v=... so browsers (and phones especially) fetch a
    changed style.css / main.js right away instead of keeping a cached copy."""
    with open(os.path.join(ROOT, *relpath.split("/")), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


CSS_HREF = f"assets/style.css?v={_asset_version('assets/style.css')}"
JS_SRC = f"assets/main.js?v={_asset_version('assets/main.js')}"

FONT_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@300;400;500;600;700&family=Noto+Sans+Thai:wght@300;400;500;600;700&display=swap">'''

# Course structure (Plant Simulation 2606 Step by Step). Each chapter's objectives and body
# live in tools/chapters/<section>_<NN>.py -- see gen_chapters.py.
SECTIONS = {
    "overview": {
        "label": "Plant Simulation Overview",
        "hub": "overview.html",
        "chapters": [
            "Introduction to Plant Simulation",
            "โรงงานตัวอย่าง Factory 51",
            "Small Parts Production",
            "Python GA Demo",
        ],
    },
    "lessons": {
        "label": "Step by Step 01–09",
        "hub": "lessons.html",
        # "flat": each chapter is its own top-level menu item instead of a collapsible group
        "flat": True,
        "chapters": [
            "สร้างโมเดลแรก",
            "คอขวด และ ParallelStation",
            "Conveyor, Buffer, เครื่องเสีย และ OEE",
            "คน และกะทำงาน",
            "ประกอบ และถอด (Assembly / Dismantle)",
            "Track และ Transporter",
            "SimTalk และ Method",
            "AMR — AGVPool และ GAWizard",
            "Python ใน Plant Simulation",
        ],
    },
}

SECTION_ORDER = ["overview", "lessons"]


def _chapter_stem(idx):
    return f"{idx:02d}" if isinstance(idx, int) else idx


def chapter_filename(section, idx):
    return f"{section}-{_chapter_stem(idx)}.html"


def chapter_numbers(section):
    """Chapter ids of a section in reading order -- 1..N, or the section's own "ids"
    list (strings such as "00a", "01") when it sets one."""
    return SECTIONS[section].get("ids") or list(range(1, len(SECTIONS[section]["chapters"]) + 1))


def chapter_title(section, idx):
    return SECTIONS[section]["chapters"][chapter_numbers(section).index(idx)]


def chapter_label(section, idx):
    """Chapter number as shown to readers: lessons are "01".."09", other sections "1".."N"."""
    if SECTIONS[section].get("flat") and isinstance(idx, int):
        return f"{idx:02d}"
    return str(idx).upper()


def sidebar_html(expand_section=None, active_top=None, active_chapter=None):
    parts = []
    parts.append('      <nav id="menu">')
    parts.append('        <header class="major"><button class="sidebar-close" aria-label="ปิดเมนู">✕</button><h2>เมนู</h2></header>')
    parts.append('        <ul>')
    home_active = ' class="active"' if active_top == "index" else ''
    parts.append(f'          <li{home_active}><a href="index.html">หน้าแรก</a></li>')

    for sec in SECTION_ORDER:
        info = SECTIONS[sec]
        if info.get("flat"):
            for i in chapter_numbers(sec):
                li_active = ' class="active"' if (active_top == sec and active_chapter == i) else ''
                parts.append(f'          <li{li_active}><a href="{chapter_filename(sec, i)}">'
                             f'{chapter_label(sec, i)}. {chapter_title(sec, i)}</a></li>')
            continue
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
        for i in chapter_numbers(sec):
            fname = chapter_filename(sec, i)
            li_active = ' class="active"' if (active_top == sec and active_chapter == i) else ''
            parts.append(f'              <li{li_active}><a href="{fname}">{chapter_label(sec, i)}. {chapter_title(sec, i)}</a></li>')
        parts.append('            </ul>')
        parts.append('          </li>')

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
<link rel="stylesheet" href="{CSS_HREF}">
</head>
<body>
<div id="wrapper">
  <div id="main">
    <div class="inner">
      <header id="header">
        <a href="index.html" class="logo"><span>Plant Simulation Tutorial</span></a>
        <button class="menu-toggle" aria-label="เปิดเมนู" aria-expanded="false">☰</button>
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
<script src="{JS_SRC}"></script>
</body>
</html>
'''


def hub_page(section):
    info = SECTIONS[section]
    cards = []
    for n, i in enumerate(chapter_numbers(section)):
        fname = chapter_filename(section, i)
        desc = HUB_CARD_DESC[section][n]
        cards.append(f'''          <a href="{fname}" class="card">
            <div class="icon number">{chapter_label(section, i)}</div>
            <h3>{chapter_title(section, i)}</h3>
            <p>{desc}</p>
          </a>''')
    cards_html = "\n".join(cards)

    idx = SECTION_ORDER.index(section)
    prev_html = '<a href="index.html">← กลับหน้าแรก</a>'
    if idx > 0:
        prev_sec = SECTION_ORDER[idx - 1]
        prev_html = f'<a href="{SECTIONS[prev_sec]["hub"]}">← ก่อนหน้า: {SECTIONS[prev_sec]["label"]}</a>'
    first_no = chapter_numbers(section)[0]
    first_chapter = chapter_filename(section, first_no)

    body = f'''        <h1>{info["label"]}</h1>
        <p class="lead" style="max-width:46em;">{HUB_INTRO[section]}</p>

        <div class="card-grid">
{cards_html}
        </div>

        <div class="page-nav">
          {prev_html}
          <a href="{first_chapter}">เริ่ม {chapter_label(section, first_no)}. {info["chapters"][0]} →</a>
        </div>'''
    return page_html(info["label"], body, expand_section=section, active_top=section)


HUB_INTRO = {
    "overview": "เริ่มจากรู้จัก Plant Simulation และแนวคิด Discrete Event Simulation แล้วเปิดโมเดลตัวอย่าง 3 ตัวที่ติดมากับโปรแกรม "
                "(Factory 51, Small Parts Production, Python GA Demo) เพื่อเห็นภาพว่าเรียนจบแล้วจะทำอะไรได้ ยังไม่ต้องสร้างโมเดลเอง",
    "lessons": "ชุดสอน Step by Step บน Plant Simulation 2606 ทั้งหมด 9 บท แต่ละบทมีไฟล์ <code>.spp</code> ของบทที่มีหลาย Frame "
               "เล่าเรื่องเดียวกัน (Model → Model2 → …) เปิดไฟล์ของบทได้เลย ไม่ต้องทำบทก่อนหน้าให้เสร็จ "
               "ทุกตัวเลขในบทเรียนวัดจริงใน Plant Simulation 2606",
}

HUB_CARD_DESC = {
    "overview": [
        "Discrete Event Simulation คืออะไร, Simulation กับ Digital Twin และ Plant Simulation ใช้แก้ปัญหาแบบไหน",
        "เปิดโมเดลตัวอย่างแรก ฝึกซูม เลื่อน หมุน 3D คลิกวัตถุ เปิด Frame และสั่ง Start / Reset ผ่าน EventController",
        "หาคอขวดของไลน์ประกอบ เพิ่ม Buffer หาขนาดด้วย Experiment Manager และดูพลังงาน",
        "Python + pymoo หาลำดับงานและขนาด Buffer 2 เป้าหมาย อ่าน Pareto แล้วใส่คำตอบกลับโมเดล (452 → 732 ชิ้น/วัน)",
    ],
    "lessons": [
        "วาง Source → Station → Drain ตั้งค่า ใส่ Display รัน 1 ชั่วโมง ได้ 359 ชิ้น แล้วบันทึก / Pack and Go",
        "หาคอขวดด้วย Chart แล้วแก้ 2 วิธี: เพิ่มเครื่องขนาน หรือ ParallelStation (177 → 354 ชิ้น/ชม.)",
        "วาดสายพานตรง/โค้ง แยกงานดี/เสียด้วย Percentage เวลาสุ่ม Uniform กราฟ Buffer และคำนวณ OEE จากเครื่องเสีย",
        "Workplace / WorkerPool / Broker จำนวนคน ความเร็ว กะทำงาน ผัง I กับ U ช่างตั้งเครื่อง และช่างซ่อม (94 → 356 ชิ้น/ชม.)",
        "ชิ้นงานขึ้นพาเลทด้วย AssemblyStation ถอดด้วย DismantleStation พาเลทวนกลับ และหาจำนวนพาเลทด้วย ExperimentManager",
        "วาด Track วงปิดให้ Transporter วิ่ง ใช้ PickAndPlace ขนชิ้นงานโดยไม่เขียน Method และ TwoLaneTrack รถวิ่งสวน 2 เลน",
        "เขียน SimTalk 2.0 ใน Method ผูก Entrance/Exit control ใช้ @ และ ? แยกทาง ประกอบ/ถอด OrderParts จนถึง Job Shop จากตาราง",
        "สั่ง AGV ด้วย setRoute / getIdleAGV แล้วให้ GAWizard หาเส้นทางสั้นสุด ลดเวลาวิ่ง 24%",
        "ติดตั้ง Python + pandas/matplotlib, PythonModule, อ่าน/เขียนค่าโมเดล, เรียก def จาก SimTalk และกราฟผลผลิตต่อชั่วโมง",
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
    'assets/images/lessons/04-01.jpg' -- write() rewrites it for the page's
    actual folder depth automatically (see _relocate_links)."""
    cap_html = f'\n  <figcaption>{caption}</figcaption>' if caption else ""
    # linked to the full-size file so wide multi-panel screenshots can be opened and zoomed
    return f'''<figure class="screenshot">
  <a href="{img_path}" target="_blank" rel="noopener"><img src="{img_path}" alt="{alt}" loading="lazy"></a>{cap_html}
</figure>'''


def step_list(items):
    """Numbered circular-badge list instead of a plain browser <ol> counter.
    items is a list of HTML strings."""
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
        "assets/style.css": "assets/style.css",
        "assets/main.js": "assets/main.js",
    }
    for sec in SECTION_ORDER:
        info = SECTIONS[sec]
        mapping[info["hub"]] = f"{sec}/index.html"
        for i in chapter_numbers(sec):
            mapping[chapter_filename(sec, i)] = f"{sec}/{_chapter_stem(i)}.html"
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
        write(SECTIONS[sec]["hub"], hub_page(sec))
