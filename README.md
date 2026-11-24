# The World in One Day — Tuesday 24 November 2026

A one-page front page summing up the world news of Tuesday 24 November
2026: 37 verified stories from seven regions, drawn entirely by code.

## The image

- **Headline:** Tankers hit mines in the Strait of Hormuz as Iran vows to
  defy the US blockade — Tehran says ships that defied its rules struck
  mines and caught fire; the US Navy holds the strait.
- **North America:** Nvidia reinstates Jensen Huang as CEO (Nasdaq +6.5%);
  Trump pardons turkeys Freedom and Feather; ninth measles death in
  Pennsylvania (1,638 cases); Army cleared to detonate unstable explosives
  in Iowa; Oregon and Virginia sue SpaceX over Grok images.
- **Europe:** Russia warns Estonia of open war over border closures; Spain
  amnesties Puigdemont; Germany first to access Ukraine's Delta system; UK
  warns of Russian sabotage risk; EU to rethink climate-summit rules after
  COP31 collapsed; bomb threats hit schools in Denmark and Germany.
- **Asia-Pacific:** Russian jets enter South Korea's defence zone; China
  opens a corruption probe into Politburo member Chen Jining; Hasina plans
  a Dec. 16 return to Bangladesh; Malaysia to return Rohingya to Myanmar;
  World Court rules Myanmar committed genocide against the Rohingya; Hanoi
  restaurant blast kills six; 5.3 quake in Nepal's Koshi province.
- **Latin America:** Car bomb injures 23 in Villavicencio, Colombia; Mexico
  captures "El Chapo Isidro"; Salvadoran troops die in a Haiti camp blast;
  Brazil cuts its 2027 growth forecast.
- **Middle East:** Israel kills Hamas security chief Naeem Abu Nahel in Gaza;
  Houthis hit Riyadh's tallest tower (11 hurt); Iraq takes over Kurdish
  oilfields; Ukraine sinks a Russian corvette off Libya; Libya's Haftar
  visits Turkey.
- **Africa:** Senegal reinstated as AFCON champions by CAS; fighting traps
  Ebola responders in DR Congo; Congo pushes foreign miners to share
  locally; Somalia and Uganda step up the al-Shabaab fight; UN urges a
  probe into the Benghazi port attacks.
- **Science & Sport:** Super Bowl LXI heads to IMAX; Pope Francis's diary
  made public; Adelaide rocket test keeps medicine stable in space; Russia's
  Progress 97 cargo ship launches for the space station.

Sources checked: AP, Reuters, Just Security (Early Edition, 24 Nov 2026),
Nature, NASA, the Court of Arbitration for Sport, UN News, and same-day
news digests. Stories are events that happened or were first reported on
24 November 2026 (COP31's collapse itself was 22 Nov; the item carried is
the 24 Nov fallout — the EU's move to overhaul summit rules).

## How it is built

`render.py` draws the whole page with Pillow: masthead, headline, a flat
vector tanker scene for the Strait of Hormuz, one small flat icon per
region, and the story columns. No network, no randomness, no timestamps —
two runs of `render.py` write byte-identical `entry.png` files.

`main.ts` (Node 22) copies the shipped `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).

## Run it

```sh
python3 render.py            # regenerate entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
