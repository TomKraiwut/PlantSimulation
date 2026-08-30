# Image naming convention

Screenshots for a chapter go in a subfolder named after the section, using the
same chapter numbering as the `.html` files:

```
assets/images/<section>/<chapter-number>-<sequence>.png
```

Example: the 3rd screenshot in Basic chapter 4 is
`assets/images/basic/04-03.png`.

## Adding a screenshot to a chapter

In `tools/gen_chapters.py`, use the `screenshot()` helper from `gen_site.py`
inside the relevant `BODY[(section, idx)]` entry (convert that entry to an
f-string if it isn't one already):

```python
BODY[("basic", 4)] = f'''
...
{screenshot("assets/images/basic/04-01.png", "หน้าจอสร้างโมเดลใหม่", caption="ลาก Source/Station/Drain มาวางบน Frame")}
...
'''
```

Author the path as repo-root-relative (`assets/images/...`) always — `write()`
in `gen_site.py` rewrites it to the correct relative path for whatever folder
the page actually lands in, so the same string works whether the chapter ends
up as `basic/04.html` or anywhere else.

Keep each exported screenshot compressed (PNG optimized or JPG, ideally under
~300-500KB) — see the "รูปภาพและวิดีโอ" section in the top-level README.md for
why.

## Adding a YouTube video to a chapter

Same pattern with the `youtube_embed()` helper:

```python
BODY[("basic", 2)] = f'''
...
{youtube_embed("l-p1UY2W5CY", "1. Getting Started - Plant Simulation")}
...
'''
```

`youtube_embed`/`screenshot` are defined in `tools/gen_site.py` and already
imported into `tools/gen_chapters.py`.
