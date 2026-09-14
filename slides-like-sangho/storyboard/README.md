# The interactive storyboard editor

`SKILL.md` requires a hard stop at the storyboard. This is what to hand over at that
stop: a published Claude artifact he can read, reorder, rewrite and annotate, whose
edits you read back to build the deck. It replaces pasting a storyboard into chat.

## The pipeline

```bash
# 1. author the talk as a payload, then build the editor
python3 storyboard/build_storyboard.py payload.json -o editor.html
#    publish it with capabilities: {db: {}}   <- the db is where his edits live

# 2. he edits. when he says he is done, read the database back:
#    read_db  db_op:get   collection:meta  doc_id:order  out_dir:storyboard-db/
#    read_db  db_op:list  collection:beats                out_dir:storyboard-db/

# 3. merge his edits over the payload, then render
python3 render/html/build_deck_json.py payload.json storyboard-db/ -o deck.json
python3 render/html/gen_deck.py deck.json -a assets.json -o deck.html
```

The payload is the talk; `editor-template.html` is the skill. Never edit the template to
add a talk's beats — that is what the payload is for.

## What the editor gives him

- **Slide type** — a dropdown of the 23 measured archetypes grouped by purpose, each
  labelled with how often it appears in his own decks. This drives the mock's renderer.
- **Background** — cream / reversed dark-teal / black, from the brand's own ground tokens.
- **Figure and table pickers** — a table can be *recreated in type* (renders live in the
  mock, because a table is text) or *cropped from the paper* (a named reference, with the
  measured on-slide type size stated so he can judge legibility before committing).
- **Editable fields** for title, message, section header, slide words, notes.
- **Insert / delete / reorder** with drag or arrow buttons.
- **Save** — manual flush plus ⌘S, over the top of a 700ms autosave.

## Four things that failed silently here, all now guarded

1. **A saved edit must beat an authored default.** Inverted once, it printed a placeholder
   over a byline that was in the database the whole time. Nothing errored: a placeholder is
   still text. `build_deck_json.py` states this rule at the top.
2. **Anything the mock renders must have an editable field.** Authored text lived in a
   `lines` array that the mock drew but no input exposed, so one slide's text was visible
   and unreachable — he cleared every field he could see and it stayed. The template seeds
   the words box from `lines`.
3. **A stale tab must not write its running order back.** The client wrote its whole
   in-memory order on every save with no idea the stored copy had moved on, which silently
   undid a nine-slide cut. The template now records the stamp it loaded, watches
   `meta/order`, and refuses to write the order while stale — per-slide saves keep working.
4. **`save()` must return its promise.** Without it `saveAll` collected `undefined`, so a
   failed slide save reported "All changes saved".

## Editing his data

The `beats/` collection is his working copy. Read it freely; write to it only when he asks.
Removing slides means deleting their documents as well as trimming `meta/order` — the
editor's heal step re-inserts any saved document missing from the order, so trimming alone
is undone on the next load. Back the documents up to a file first, and use `db_op: update`
on `meta/order` so the `extras` skeletons for his added slides survive.
