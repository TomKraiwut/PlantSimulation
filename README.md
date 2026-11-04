# PlantSimulation

เว็บไซต์สอนการใช้งาน Siemens Tecnomatix Plant Simulation 2606 แบบ Step by Step (ภาษาไทย) — เผยแพร่ผ่าน GitHub Pages
ที่ https://tomkraiwut.github.io/PlantSimulation/

## โครงสร้างเว็บ

เมนูมี 2 ส่วน ตามชุดสอน Plant Simulation 2606:

- [index.html](index.html) — หน้าแรก (การ์ดของทุกบท)
- **Plant Simulation Overview** ([overview/](overview/index.html)) — เมนูย่อย 4 หน้า
  - `overview/01.html` Introduction to Plant Simulation (DES, Simulation และ Digital Twin)
  - `overview/02.html` Factory 51 — จาก `PtS2606_1_Factory51.pptx`
  - `overview/03.html` Small Parts Production — จาก `PtS2606_2_SmallPartsProduction.pptx`
  - `overview/04.html` Python GA Demo — จาก `PtS2606_3_PythonGADemo.pptx`
- **บท 01–09** ([lessons/](lessons/index.html)) — แต่ละบทเป็นเมนูหลักของตัวเอง `lessons/01.html` .. `09.html`
  จาก `01_Create_Simple_Model.pptx` .. `09_Python.pptx`
- [assets/style.css](assets/style.css) / [assets/main.js](assets/main.js) — สไตล์และสคริปต์เมนูกลางของทุกหน้า
  โทนสี (แดง / เทา / ขาว ตามสไลด์) กำหนดเป็นตัวแปรที่ `:root` ใน `style.css`

Layout เป็นแบบ off-canvas sidebar (เมนูเลื่อนออกจากด้านขวาเมื่อกดปุ่ม ☰) ใช้งานบนมือถือได้ ทุกหน้าใช้ header/เมนู/footer ชุดเดียวกัน

## สร้าง/แก้ไขหน้าเว็บด้วยสคริปต์ (ไม่แก้ไฟล์ .html ตรงๆ)

หน้าเว็บทั้งหมด **ถูก generate จากสคริปต์ Python ในโฟลเดอร์ [tools/](tools/)** ไฟล์ `.html` จะถูกเขียนทับเมื่อรัน generator ใหม่:

- [tools/gen_site.py](tools/gen_site.py) — โครงสร้างเมนู (`SECTIONS`, `SECTION_ORDER`): ชื่อบท, คำอธิบายบนการ์ด (`HUB_CARD_DESC`),
  เทมเพลต HTML กลาง และ `write()` ที่ย้ายไฟล์ไปโฟลเดอร์ที่ถูกต้องพร้อมแก้ลิงก์ภายในให้อัตโนมัติ
- [tools/chapters/](tools/chapters/) — **เนื้อหาบทละ 1 ไฟล์** `<section>_<NN>.py` (เช่น `lessons_04.py`) มี `OBJECTIVES` (วัตถุประสงค์)
  และ `BODY` (HTML ของบท เป็น f-string ที่เรียก `screenshot()` / `step_list()` / `side_by_side()` ได้)
- [tools/gen_chapters.py](tools/gen_chapters.py) — อ่านไฟล์ใน `tools/chapters/` แล้วสร้างทุกหน้าบท + หน้ารวมบท
  บทที่ยังไม่มีไฟล์จะขึ้นหน้า "กำลังจัดทำ"
- [tools/gen_index.py](tools/gen_index.py) — หน้าแรก (การ์ดสร้างจากรายชื่อบทใน `SECTIONS` อัตโนมัติ)

**แก้เนื้อหาบท:** แก้ไฟล์ใน `tools/chapters/` · **เปลี่ยนชื่อบทหรือคำอธิบายการ์ด:** แก้ `SECTIONS` / `HUB_CARD_DESC` ใน `gen_site.py`
· **เพิ่มบท:** เพิ่มชื่อใน `SECTIONS[section]["chapters"]` + คำอธิบายใน `HUB_CARD_DESC` แล้วสร้าง `tools/chapters/<section>_<NN>.py`

ลิงก์ภายในในเนื้อหาเขียนแบบชื่อแบน เช่น `href="lessons-03.html"`, `href="overview-02.html"` — `write()` แปลงเป็น path จริงให้

รันตามลำดับนี้หลังแก้ จากโฟลเดอร์ `tools/`:

```bash
cd tools
python gen_site.py
python gen_chapters.py
python gen_index.py
```

**ข้อควรระวังใน f-string ของ `BODY`:** ปีกกา `{` `}` ที่เป็นตัวอักษรจริง (เช่นในโค้ด SimTalk/Python) ต้องเขียนเป็น `{{` `}}`

## รูปภาพและวิดีโอในบทเรียน

- **รูปภาพ**: ตัดมาจากสไลด์ PowerPoint ของแต่ละบท (เฉพาะส่วนภาพหน้าจอพร้อมเลขกำกับสีแดง ไม่รวมหัวสไลด์/footer)
  บีบอัดเป็น JPG กว้างไม่เกิน 1600px เก็บที่ `assets/images/<section>/<NN>-<ลำดับ>.jpg` — ดู [assets/images/README.md](assets/images/README.md)
  ลำดับเลขในภาพตรงกับ `step_list()` ใต้ภาพ
- **วิดีโอ (YouTube)**: ฝังด้วย `youtube_embed(video_id, title, caption=None)` จาก `tools/gen_site.py`
- **ขนาดไฟล์**: GitHub บล็อกไฟล์เดี่ยวที่เกิน 100MB — รูปภาพควรไม่เกิน ~300KB ต่อรูป
  **ห้าม commit ไฟล์วิดีโอ (.mp4) ขึ้น repo** ให้อัปโหลดขึ้น YouTube แล้วฝังลิงก์แทน

## ไฟล์โมเดล (.spp) ให้ดาวน์โหลด

ทุกบท 01–09 มีปุ่ม "ดาวน์โหลดไฟล์ของบท" ใต้วัตถุประสงค์ ลิงก์ไปที่ไฟล์แนบของ **GitHub Release ล่าสุด**
(`https://github.com/TomKraiwut/PlantSimulation/releases/latest/download/<ชื่อไฟล์>`) — ไฟล์ .spp ไม่อยู่ใน repo
ชื่อไฟล์ของแต่ละบทอยู่ที่ `SECTIONS["lessons"]["downloads"]` ใน `gen_site.py`

อัปเดตไฟล์: GitHub → **Releases → Draft a new release** → ตั้ง tag ใหม่ (เช่น `v2026.11.04`) → แนบไฟล์ .spp
**ชื่อไฟล์ต้องตรงกับรายชื่อเดิม** → **Publish release** — หน้าเว็บไม่ต้องแก้ ลิงก์ชี้ไป release ล่าสุดเอง
(โมเดลตัวอย่างใน Overview เป็นไฟล์ของ Siemens ที่มากับโปรแกรมใน `Examples\Demo` จึงไม่แนบ)

## วิธีเปิดใช้งานเป็นเว็บไซต์ (GitHub Pages)

1. ไปที่ repo บน GitHub → **Settings → Pages**
2. หัวข้อ **Build and deployment** เลือก Source เป็น **Deploy from a branch**
3. เลือก branch `main` และโฟลเดอร์ `/ (root)` แล้วกด **Save**

## ทดสอบในเครื่องก่อน push

หน้าเว็บเป็น static HTML ธรรมดา — ทดสอบด้วย `python -m http.server 8000` จากโฟลเดอร์นี้ แล้วเปิด `http://localhost:8000/`
(ดู [Git.md](Git.md) สำหรับพื้นฐาน Git/GitHub)
