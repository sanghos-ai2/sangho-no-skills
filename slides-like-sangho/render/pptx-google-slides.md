# Render path: PPTX → Google Drive → Google Slides

The path to a **natively web-editable** deck. Generate a `.pptx` locally, upload it through the
Drive connector, and let Drive convert it to a Google Slides presentation on the way in.

Pick it when Sangho wants to edit in a browser, hand the deck to a co-author, or present from
Google Slides.

## Read this before anything else

**`create_file` with `mimeType: application/vnd.google-apps.presentation` produces an EMPTY deck.**
The connector's own description says the three Google first-party types "can be created without
providing content", and that is all it does — there is **no Slides structural API exposed here**,
so there is no way to add a slide, a text box or an image to a deck created that way. You get a
presentation with one blank slide and no route to fill it.

**PPTX-then-convert is the only route that carries content.** Do not reach for the Google mime type
because it looks more direct; it is the one call that cannot work.

## Step 1 — build the `.pptx`

```bash
uv run --with python-pptx python build_deck.py
```

`python-pptx` is not installed on this machine; `uv run --with python-pptx` fetches it per run and
needs no install step.

The mechanics that matter for this corpus:

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu

prs = Presentation()
prs.slide_width  = Inches(13.333)   # 1920 px at 144 dpi
prs.slide_height = Inches(7.5)      # 1080 px

BLANK = prs.slide_layouts[6]        # the only layout to use — see below
slide = prs.slides.add_slide(BLANK)
```

- **Use the blank layout for every slide** (`slide_layouts[6]` in the default template). Every other
  layout carries a title placeholder, and a placeholder is a slot that wants filling — which is
  precisely what never-list entry 2 (`structural`) is about. Add text boxes where the composition
  puts them.
- **The slide is 13.333 × 7.5 in, so 1 pt = 1 px at 1920 × 1080.** The derived scale transfers
  unchanged: `Pt(112)` / `Pt(84)` / `Pt(50)` / `Pt(36)` / `Pt(24)`.
- **Presenter notes have a real field here** and this is the only path where they do:
  `slide.notes_slide.notes_text_frame.text = "..."`. Use it. In the corpus a note belongs to a beat
  and is repeated verbatim across consecutive build steps — reproduce that rather than inventing a
  new note per step.
- **Fonts must exist on the reader's machine or Google's.** A brand face like PP Telegraf will not
  survive the conversion; Google substitutes silently. Say which face you asked for and which one
  you expect to render, or pick from Google Fonts when the deck is destined for Slides.
- **Vector figures do not survive as vectors.** python-pptx can place autoshapes and images; complex
  drawn figures are easier to render as SVG → PNG at 2× (3840 × 2160) and place as a picture. Say
  in the handback which slides carry a rasterised figure, since those are the ones he cannot edit.

## Step 2 — upload and convert

```
mcp__claude_ai_Google_Drive__create_file(
  title: "<deck title>",
  base64Content: "<base64 of the .pptx>",
  contentMimeType: "application/vnd.openxmlformats-officedocument.presentationml.presentation"
)
```

Drive converts supported content to the Google first-party type **by default**, so a `.pptx`
uploaded this way lands as `application/vnd.google-apps.presentation` — editable in Slides, with
its text, shapes, images and speaker notes intact. Setting `disableConversionToGoogleType: true`
would leave it as a `.pptx` file sitting in Drive instead; that is the wrong flag for this path.

Two practical notes: the content goes up **base64-encoded**, so a deck carrying several full-bleed
screenshots gets large — keep images to what the slide actually needs at 2× and check the encoded
size before sending. And pass `parentId` if he named a folder; otherwise it lands in My Drive root.

## Step 3 — verify

Read the returned file's `id` and confirm its `mimeType` is `application/vnd.google-apps.presentation`.
If it came back as the PPTX mime type, the conversion did not happen and he has a file, not a deck.

Give him the link. Keep the `.pptx` and the build script in the output directory — the script is
how the deck gets rebuilt after a storyboard change, and re-running it is cheaper than re-editing
slides by hand.
