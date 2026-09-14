# Render path: Keynote via AppleScript

A scaffold Sangho finishes by hand: AppleScript creates the document, adds one blank slide per
beat, sets the copy and the notes, and leaves the figures to him. The canon was authored in
Keynote, so this is the path that lands in the tool he actually uses.

## It does not work on this machine, and the reason matters

**Apple Keynote is not installed here.** `tell application "Keynote"` nonetheless resolves — to
`/Applications/Keynote Creator Studio.app`, a third-party application that **declares Apple's
bundle identifier**:

```
$ osascript -e 'POSIX path of (path to application "Keynote")'
/Applications/Keynote Creator Studio.app/

$ codesign -dv --verbose=2 "/Applications/Keynote Creator Studio.app"
Identifier=com.apple.Keynote
TeamIdentifier=JCRTNEU7GK
```

So the usual check — does the bundle id match? — **passes on the impostor.** An AppleScript
targeting "Keynote" here does not fail; it is delivered to a different program, which will either
error somewhere confusing or do something you did not ask for.

## The gate

**Verify the signature, not the bundle id.** Before sending a single AppleScript command:

```bash
KN="$(osascript -e 'POSIX path of (path to application "Keynote")' 2>/dev/null)"
[ "$KN" = "/Applications/Keynote.app/" ] || echo "REFUSE: resolves to $KN"
codesign -dv --verbose=2 "$KN" 2>&1 | grep -E 'Identifier|TeamIdentifier|Authority'
```

Refuse the path unless **both** hold:

1. The resolved path is `/Applications/Keynote.app`.
2. `codesign` shows no third-party `TeamIdentifier` — Apple's own applications do not carry one.
   `TeamIdentifier=JCRTNEU7GK`, or any other team id, is a refusal.

Print the `codesign` output in the handback either way, so the decision is checkable rather than
asserted.

**If the gate fails, say so and offer another path.** Do not fall back to driving whatever answered
to the name — that is the failure this gate exists to prevent. Do not offer to install anything.

## The scaffold, for when the gate passes

Keynote's AppleScript dictionary is thin: it can make a document, add slides against a named master,
set the text of existing placeholders, and set presenter notes. It cannot draw. So the scaffold's
job is the structure and the words; the figures are his.

```applescript
tell application "Keynote"
  set doc to make new document with properties {width:1920, height:1080}
  tell doc
    -- one slide per storyboard beat, in order
    set s to make new slide with properties {base slide:master slide "Blank" of doc}
    tell s
      set presenter notes to "…"
    end tell
  end tell
end tell
```

Three things to carry from the corpus:

- **Master "Blank", every slide.** The other eleven stock masters in the White theme carry title and
  bullet placeholders. `controller-findings.md` records that the twelve master names in the Luminate
  file are the **stock White-theme catalog** and that no slide records which master it uses — that
  is the theme's menu, not evidence of what he picks. Do not read the catalog as a layout system.
- **Presenter notes are the reason to prefer this path over the canvas.** Keynote has a real notes
  field and he works from it: 35 of Luminate's 55 slides carry one, several with wall-clock cues
  (`00:00 - 00:20 (20 s)`). Set them, and repeat a note verbatim across a build's consecutive slides
  the way the corpus does rather than rewriting it per step.
- **One slide per build step.** As everywhere else.

Then hand it over as a scaffold, explicitly: list which slides are structurally complete and which
are waiting on a figure, so he is not hunting for the gaps.
