# Image naming convention

Screenshots for a chapter go in a subfolder named after the section, using the
same chapter numbering as the `.html` files:

```
assets/images/<section>/<chapter-number>-<sequence>.jpg
```

Example: the 3rd screenshot in lesson 04 is `assets/images/lessons/04-03.jpg`;
the 2nd in Overview page 2 (Factory 51) is `assets/images/overview/02-02.jpg`.

## Adding a screenshot to a chapter

In the chapter's file `tools/chapters/<section>_<NN>.py`, use the `screenshot()`
helper inside `BODY` (an f-string):

```python
BODY = f'''
...
{screenshot("assets/images/lessons/04-01.jpg", "หน้าต่าง WorkerPool", caption="...")}
...
'''
```

Author the path as repo-root-relative (`assets/images/...`) always — `write()`
in `gen_site.py` rewrites it to the correct relative path for whatever folder
the page lands in.

Images are cut from the chapter's slide deck (the screenshot area with its red
number callouts, without the slide title or footer) and saved as JPG at most
1600 px wide, ideally under ~300 KB each.

## Adding a YouTube video to a chapter

Same pattern with `youtube_embed()` (import it from `gen_site` in the chapter file):

```python
{youtube_embed("l-p1UY2W5CY", "1. Getting Started - Plant Simulation")}
```
