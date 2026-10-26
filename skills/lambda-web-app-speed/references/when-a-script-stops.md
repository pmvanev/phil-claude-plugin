# When a Script Stops

Each script stops with a message instead of a report when its input cannot support one. Follow the
entry for the message, and say in the report what happened.

## `cold-path.py`, in Step 3

- *Not a complete response*: the fetch was cut off. Move the window's start later by half its length,
  refetch, and say the window was narrowed.
- *SnapStart restores*: stop and say this version does not divide restores.
- *No REPORT line*: the function served nothing in the window. Where the window starts at the last
  change, measure `--days 14` and say it mixes versions; otherwise report that it served nothing.
- *Truncated*, in the report itself: the fetch hit its item cap, and the report names where it stopped.
  Say so beside the numbers; they cover the window up to that moment.

## `phases.py`, in Step 4

- *Not a complete response*: the fetch was cut off. Move the start later by half the window's length,
  and refetch.
- *No Embedded Metric Format line*: check the filter names one of the line's phases; then treat the
  layer as having no timing line.
- *Breaks the phase convention*: treat the layer as having no timing line, and say why.

## `warmth.py`, in Step 6

- *Truncated*: the fetch hit its item cap, so its traffic covers part of the window. Price nothing, and
  say so.
- *No traffic to price*: `cold-path.py` stopped before it; follow `cold-path.py`'s entry above.
- *Cannot price*: the price list could not be fetched or read, or holds no such Region. Price nothing.

## `firstbyte.py`, in Step 7

- *Not 2xx*: a redirect or a refusal may never have reached the function. Report the first byte unsplit.
- *No REPORT line*: fetch again once; CloudWatch receives lines seconds late. Then report it unsplit.
- *Several REPORT lines*, or *longer than the first byte*: other traffic shared the window, or the
  match was wrong. Report it unsplit.
