# PlantSimulation

เว็บไซต์สอนการใช้งาน Siemens Tecnomatix Plant Simulation (ภาษาไทย) — เผยแพร่ผ่าน GitHub Pages

## โครงสร้างเว็บ

แต่ละเมนูมีโฟลเดอร์ของตัวเอง — หน้ารวมบท (hub) อยู่ที่ `<section>/index.html` และบทย่อยอยู่ที่ `<section>/01.html`, `02.html`, ...
ทำให้เพิ่มบทใหม่ในอนาคตได้โดยแค่เพิ่มไฟล์ในโฟลเดอร์เดิม ไม่ต้องยุ่งกับไฟล์อื่น:

- [index.html](index.html) — หน้าแรก
- **Basic — พื้นฐาน** ([basic/](basic/index.html)) — 6 บท (`basic/01.html` .. `06.html`)
- **Intermediate — ขั้นกลาง** ([intermediate/](intermediate/index.html)) — 6 บท (`intermediate/01.html` .. `06.html`)
- **Advanced — ขั้นสูง** ([advanced/](advanced/index.html)) — 7 บท (`advanced/01.html` .. `07.html`)
- **Object Reference — สาธิต Object** ([object-reference/](object-reference/index.html)) — 3 หมวด (`object-reference/01.html` .. `03.html`)
- **Step-by-Step File — ไฟล์สอนของ Siemens** ([step-by-step/](step-by-step/index.html)) — 8 บท (`step-by-step/01.html` .. `08.html`) เดินตามไฟล์สอนต้นฉบับของ Siemens `2404_Plant_Simulation_Step_by_Step.spp` (18 เฟรม) ทีละหัวข้อ
- **Case Study — ตัวอย่างอุตสาหกรรม** ([case-study/](case-study/index.html)) — 4 บท (`case-study/01.html` .. `04.html`)
- **Tips and Tricks — เทคนิคการทำงาน** ([tips-tricks/](tips-tricks/index.html)) — 4 หมวด (`tips-tricks/01.html` .. `04.html`)
- [examples.html](examples.html) — ตัวอย่างโมเดลจริงเพิ่มเติม (อยู่ที่ root เหมือนเดิม ไม่ใช่ hub ของหมวดที่มีบทย่อย)
- [assets/style.css](assets/style.css) / [assets/main.js](assets/main.js) — สไตล์และสคริปต์ sidebar กลางของทุกหน้า (อยู่ที่ root เสมอ)
- [examples/](examples/) — ไฟล์ตัวอย่าง `.spp` (เพิ่มเองได้)

Layout เป็นแบบ off-canvas sidebar (เมนูเลื่อนออกจากด้านซ้ายเมื่อกดปุ่ม ☰) ทุกหน้าใช้ header/sidebar/footer ชุดเดียวกัน

## สร้าง/แก้ไขหน้าเว็บด้วยสคริปต์ (ไม่แก้ไฟล์ .html ตรงๆ)

หน้าเว็บทั้งหมด **ถูก generate จากสคริปต์ Python ในโฟลเดอร์ [tools/](tools/)** ไม่ควรแก้ไฟล์ `.html` ในโฟลเดอร์เนื้อหาตรงๆ
เพราะจะถูกเขียนทับเมื่อรัน generator ใหม่ โครงสร้างเมนู/สารบัญ/เนื้อหาบทเรียนทั้งหมดอยู่ในสคริปต์เหล่านี้:

- [tools/gen_site.py](tools/gen_site.py) — โครงสร้างเมนู (`SECTIONS`, `SECTION_ORDER`), เทมเพลต HTML กลาง (header/sidebar/footer),
  และตัว `write()` ที่ย้ายไฟล์ไปโฟลเดอร์ที่ถูกต้องพร้อมแก้ลิงก์ภายในให้อัตโนมัติ
- [tools/gen_chapters.py](tools/gen_chapters.py) — เนื้อหาแต่ละบท (`OBJECTIVES`, `BODY` ต่อ `(section, เลขบท)`)
- [tools/gen_index.py](tools/gen_index.py) — เนื้อหาหน้าแรก
- [tools/gen_examples.py](tools/gen_examples.py) — เนื้อหาหน้า Example File

**เพิ่มบทใหม่ในหมวดที่มีอยู่แล้ว:** เพิ่มชื่อบทใน `SECTIONS[section]["chapters"]` ใน `gen_site.py`, เพิ่ม `OBJECTIVES[(section, เลขบท)]`
และ `BODY[(section, เลขบท)]` ใน `gen_chapters.py` แล้วรันสคริปต์ทั้ง 4 ตัวใหม่ตามลำดับ — sidebar/page-nav ของทุกหน้าจะอัปเดตอัตโนมัติ

**เพิ่มหมวดเมนูใหม่ทั้งหมด:** เพิ่ม entry ใหม่ใน `SECTIONS` และ `SECTION_ORDER` ใน `gen_site.py` (ดูตัวอย่าง `object-reference`/
`case-study`/`tips-tricks` เป็นแบบอ้างอิง) แล้วเพิ่มเนื้อหาใน `gen_chapters.py` เหมือนขั้นตอนข้างบน

รันตามลำดับนี้เสมอหลังแก้สคริปต์ จากโฟลเดอร์ `tools/` (`gen_chapters.py`/`gen_index.py`/`gen_examples.py` import จาก `gen_site.py`):

```bash
cd tools
python gen_site.py
python gen_chapters.py
python gen_index.py
python gen_examples.py
```

## รูปภาพและวิดีโอในบทเรียน

- **วิดีโอ (YouTube)**: ฝังด้วย `youtube_embed(video_id, title, caption=None)` จาก `tools/gen_site.py` — responsive 16:9,
  ไม่กินพื้นที่ repo เลยเพราะวิดีโอยังอยู่บน YouTube ทั้งหมด ใช้ `video_id` (ส่วนหลัง `watch?v=` หรือ `youtu.be/`) ไม่ใช่ URL เต็ม
  ตัวอย่างการใช้งานจริงอยู่ใน `BODY[("basic", 2)]`
- **รูปภาพ (screenshot ทีละขั้นตอน)**: ฝังด้วย `screenshot(img_path, alt, caption=None)` — เก็บไฟล์ไว้ที่
  `assets/images/<section>/<เลขบท>-<ลำดับ>.png` ดูรายละเอียด naming convention เต็มๆ ที่ [assets/images/README.md](assets/images/README.md)
- ทั้งสอง helper ต้อง `import` เข้า `gen_chapters.py` (มีอยู่แล้ว) และ `BODY[(section, idx)]` ที่จะใช้ต้องเป็น f-string
  (`f'''...'''`) เพื่อ interpolate `{youtube_embed(...)}` / `{screenshot(...)}` เข้าไปได้
- **ขนาดไฟล์**: GitHub บล็อกไฟล์เดี่ยวที่เกิน 100MB (เตือนตั้งแต่ 50MB) และแนะนำให้ repo รวมไม่เกิน ~1GB — รูปภาพประกอบ
  บทเรียน (compress ดีๆ ให้ไม่เกิน ~300-500KB ต่อรูป) ใส่ได้สบายๆ หลายร้อยรูป แต่**ห้าม commit ไฟล์วิดีโอ (.mp4) ขึ้น repo
  โดยตรงเด็ดขาด** — ต้องอัปโหลดขึ้น YouTube แล้วฝังลิงก์แทนเสมอ

## วิธีเปิดใช้งานเป็นเว็บไซต์ (GitHub Pages)

1. ไปที่ repo บน GitHub → **Settings → Pages**
2. หัวข้อ **Build and deployment** เลือก Source เป็น **Deploy from a branch**
3. เลือก branch `main` และโฟลเดอร์ `/ (root)` แล้วกด **Save**
4. รอสักครู่ เว็บจะออนไลน์ที่ `https://<username>.github.io/PlantSimulation/`

## ทดสอบในเครื่องก่อน push

หน้าเว็บเป็น static HTML ธรรมดา ไม่มี build step — ทดสอบด้วย static server เช่น `python -m http.server 8000` จากโฟลเดอร์นี้
แล้วเปิด `http://localhost:8000/` (ดู [Git.md](Git.md) สำหรับพื้นฐาน Git/GitHub เวลาจะ commit + push)
