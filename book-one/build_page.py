#!/usr/bin/env python3
"""Adapt the Muse Book One timeline into house style and write index.html."""
from pathlib import Path
import re
import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SRC = Path("/workspace/muse/extracted/book-one-timeline.html")
OUT = ROOT / "index.html"
QR_URL = "https://robmac10.github.io/the-story-contents/book-one/"
ASSET_V = "20261127a"

def make_qr():
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(QR_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#241b10", back_color="#f6efe1").convert("RGB")
    # emblem-style quiet cream square
    path = ROOT / "assets" / "book-one-timeline-qr.png"
    img.save(path, "PNG")
    return path

EXTRA_CSS = """
  meta-robots-placeholder {}
  .notice{
    max-width:1120px;margin:0 auto;padding:0 20px 8px;
  }
  .notice p{
    margin:0 0 18px;padding:12px 16px;border-left:4px solid var(--ochre);
    background:var(--paper-2);color:var(--ink-soft);font-size:.92rem;max-width:62em;
  }
  .topnav{
    max-width:1120px;margin:0 auto;padding:18px 20px 0;
    display:flex;flex-wrap:wrap;gap:12px 22px;align-items:center;justify-content:space-between;
  }
  .topnav a{color:var(--sea);font-weight:700;text-decoration:none;font-size:.95rem}
  .topnav a:hover,.topnav a:focus-visible{text-decoration:underline;text-underline-offset:3px}
  .qrbox{display:flex;align-items:center;gap:10px;color:var(--muted);font-size:.8rem;max-width:16rem}
  .qrbox img{width:72px;height:72px;border:1px solid var(--line);background:#fff;flex:0 0 auto}
  /* images fit the screen and tap to enlarge */
  figure{margin:0}
  figure img, .card figure img{
    max-width:100%;height:auto;max-height:70vh;width:auto;object-fit:contain;
    cursor:zoom-in;border-radius:10px 10px 0 0;
  }
  @media (max-width:600px){
    figure img, .card figure img{max-height:60vh}
  }
  button.zoom{
    display:block;width:100%;margin:0;padding:0;border:0;background:transparent;cursor:zoom-in;
    font:inherit;color:inherit;
  }
  .lightbox[hidden]{display:none}
  .lightbox{
    position:fixed;inset:0;z-index:80;background:rgba(16,12,8,.92);
    display:flex;flex-direction:column;align-items:center;justify-content:center;padding:16px;
  }
  .lightbox-stage{max-width:100%;max-height:90vh;display:flex;align-items:center;justify-content:center}
  .lightbox-stage img{max-width:100%;max-height:88vh;width:auto;height:auto;object-fit:contain}
  .lightbox-close{
    position:absolute;top:10px;right:12px;min-width:44px;min-height:44px;border:0;border-radius:999px;
    background:#f6efe1;color:#241b10;font-size:1.6rem;cursor:pointer;line-height:1;
  }
  .teacher{
    max-width:1120px;margin:28px auto 0;padding:8px 20px 48px;
  }
  .teacher details{
    background:var(--card);border:1px solid var(--line);border-radius:14px;padding:8px 18px 16px;
  }
  .teacher summary{
    cursor:pointer;font-family:"Newsreader",Georgia,serif;font-weight:600;font-size:1.2rem;
    padding:12px 0;min-height:44px;
  }
  .teacher p,.teacher li{color:var(--ink-soft);font-size:.95rem}
  .teacher ul{padding-left:1.2em}
  footer.site{
    max-width:1120px;margin:0 auto;padding:8px 20px 48px;color:var(--muted);font-size:.88rem;
  }
  footer.site a{color:var(--sea)}
  figcaption .credit{
    display:block;margin-top:.45em;font-size:.88em;line-height:1.4;color:var(--muted);
  }
  figcaption .credit a{color:var(--sea)}
"""

NOTICE = """
<nav class="topnav">
  <a href="../">← The four books</a>
  <div class="qrbox">
    <img src="assets/book-one-timeline-qr.png?v=20261127a" width="72" height="72" alt="QR code for this Book One timeline">
    <span>Open on a phone: this page. The code does not go to a case file.</span>
  </div>
</nav>
<div class="notice">
  <p>Aboriginal and Torres Strait Islander readers are advised that this timeline names people who have died, and discusses colonisation and dispossession. No photographs of deceased Aboriginal or Torres Strait Islander people are used, and no rock art is shown.</p>
</div>
"""

FOOT = """
<section class="teacher" id="teacher-note">
  <details>
    <summary>Teacher Note</summary>
    <p>This page is a Book One timeline for <i>Reopen the Record: Australian Histories</i>. It was rebuilt from a writing draft so that it matches the other companion pages: images stay on the screen and tap to enlarge, there is no audio, and student cards do not carry year levels or case numbers. Book chapter labels (for example “Book One · Ch. 1”) stay, because they point to the book, not to a case number.</p>
    <p>A Kakadu rock-art photograph was in the writing draft, as the opening image for Madjedbebe. It has been left out, in line with the series rule against showing rock art. The dating dispute (about 65,000 years, or about 50,000–55,000 years) is unchanged: both findings are on the card, and students are left to weigh them.</p>
    <p>The Blue Mountains stop (May 1813 — Blaxland, Lawson and Wentworth) now has a published case in the casebook reader: <a href="https://robmac10.github.io/reopen-the-record/#p=70" target="_blank" rel="noopener">Crossing the Blue Mountains, from page 70</a>. The four paper-and-flag steps of the British claim (1770–1829) have their own case in the same reader: <a href="https://robmac10.github.io/reopen-the-record/#p=37" target="_blank" rel="noopener">Britain Claims Australia, from page 37</a>. The two investigations are related in time, but they are not the same file. The Claim story app remains the companion for the landing at Kamay, Possession Island, and the early years of the colony.</p>
    <p>Image notes: Lake Mungo shows the dry lake and lunette, not ancestral remains. Each image on the cards now has a credit and licence line. The Eureka image is Raffaello Carboni’s 1855 illustration, not a photograph of the conserved flag. The Federation image is a public-domain photograph, about 1903, of Tom Roberts at work on the painting, not a modern colour photograph of the finished canvas. A Kakadu rock-art photograph remains omitted.</p>
    <p>Curriculum links and year levels belong in teacher planning, not on the student cards. Companion case apps open in a new tab.</p>
  </details>
</section>
<footer class="site">
  <p>Reopen the Record · Australian Histories · Book One timeline — Deep Time to Federation. A writing draft, rebuilt for class use. <a href="../">Back to the four books</a>.</p>
</footer>
<div id="lightbox" class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Magnified image">
  <button type="button" class="lightbox-close" aria-label="Close the magnified image">&times;</button>
  <div class="lightbox-stage"><img alt=""></div>
</div>
"""

LIGHTBOX_JS = """
<script>
(function(){
  var box = document.getElementById('lightbox');
  if(!box) return;
  var stageImg = box.querySelector('.lightbox-stage img');
  var closeBtn = box.querySelector('.lightbox-close');
  function open(src, alt){
    stageImg.src = src; stageImg.alt = alt || '';
    box.hidden = false; closeBtn.focus();
  }
  function close(){
    box.hidden = true; stageImg.src = '';
  }
  document.querySelectorAll('button.zoom').forEach(function(btn){
    btn.addEventListener('click', function(){
      var img = btn.querySelector('img');
      if(img) open(img.currentSrc || img.src, img.alt);
    });
  });
  closeBtn.addEventListener('click', close);
  box.addEventListener('click', function(e){ if(e.target === box) close(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && !box.hidden) close(); });
})();
</script>
"""

def main():
    make_qr()
    html = SRC.read_text(encoding="utf-8")

    html = html.replace(
        "<title>Deep Time to Federation</title>",
        "<title>Deep Time to Federation · Book One timeline · Reopen the Record</title>\n"
        '<meta name="robots" content="noindex, nofollow">\n'
        '<meta name="description" content="Book One timeline for Reopen the Record: Australian Histories, from deep time to Federation and the vote in 1902.">',
        1,
    )

    # Extra CSS before closing style
    html = html.replace("  .endmark{", EXTRA_CSS + "\n  .endmark{", 1)

    # Top nav + cultural notice after progress bar, before header
    html = html.replace(
        '<header class="simple-head">',
        NOTICE + '<header class="simple-head">',
        1,
    )

    # Remove rock art figure; do not replace with another Country photograph
    html = re.sub(
        r"<figure>\s*<img src=\"assets/rock-art\.jpg\"[^>]*>\s*<figcaption>Rock art in Kakadu[^<]*</figcaption>\s*</figure>",
        "",
        html,
        count=1,
        flags=re.S,
    )

    # Credits and licence lines, and any file replacements, so a Muse rebuild keeps them.
    def vsrc(name):
        return f"assets/{name}?v={ASSET_V}"

    def clink(href, label):
        return f'<a href="{href}" target="_blank" rel="noopener">{label}</a>'

    CC0 = clink("https://creativecommons.org/publicdomain/zero/1.0/", "CC0 1.0")
    CCBYSA = clink("https://creativecommons.org/licenses/by-sa/4.0/", "CC BY-SA 4.0")
    IMAGE_RIGHTS = {
        "lake-mungo.png": {
            "src": "lake-mungo.jpg",
            "alt": "The eroded lunettes known as the Walls of China at Lake Mungo, in evening light",
            "caption": "Lake Mungo at evening — the dry lake where the oldest human remains in Australia were found.",
            "credit": "Photograph: Caroline Jones, 7 June 2016, via Flickr / "
                      + clink("https://commons.wikimedia.org/wiki/File:Walls_of_China_in_Mungo_National_Park_(27464678334).jpg", "Wikimedia Commons")
                      + f". {CC0}.",
        },
        "hartog-plate.jpg": {
            "src": "hartog-plate.jpg",
            "alt": "The weathered pewter Hartog plate of 1616, its Dutch inscription still partly legible",
            "caption": "The Hartog plate, 1616 — now in the Rijksmuseum, Amsterdam.",
            "credit": "Dirck Hartogh dish, 1616, "
                      + clink("https://id.rijksmuseum.nl/200311613", "Rijksmuseum, Amsterdam")
                      + ", object NG-NM-825. Photograph: Rijksmuseum, "
                      + clink("https://commons.wikimedia.org/wiki/File:Dirck_Hartogh-schotel,_NG-NM-825.jpg", "via Wikimedia Commons")
                      + f". {CC0}. Credit: Rijksmuseum, Amsterdam.",
        },
        "batavia.jpg": {
            "src": "batavia.jpg",
            "alt": "The recovered stern of the Batavia and the stone gateway in the Shipwreck Galleries, Fremantle",
            "caption": "The Batavia’s stern and the stone gateway it was carrying — Shipwreck Galleries, Fremantle.",
            "credit": "Photograph: Vunz, 18 November 2014, "
                      + clink("https://commons.wikimedia.org/wiki/File:Shipwreck_Galleries,_Fremantle,_WA.JPG", "Wikimedia Commons")
                      + f". {CCBYSA}. This copy has been resized.",
        },
        "eureka-flag.jpg": {
            "src": "eureka-flag.jpg",
            "alt": "Raffaello Carboni’s 1855 illustration of the Eureka flag, a cross and stars within a floral border",
            "caption": "The Eureka flag, as illustrated on the cover of Raffaello Carboni’s <i>The Eureka Stockade</i>, 1855 — the flag was flown at Bakery Hill on 30 November 1854.",
            "credit": "Raffaello Carboni, <i>The Eureka Stockade</i>, 1855. Public domain. "
                      + clink("https://commons.wikimedia.org/wiki/File:Carboni_Eureka_flag_illustration.png", "Wikimedia Commons") + ".",
        },
        "federation.jpg": {
            "src": "federation.jpg",
            "alt": "Photograph, about 1903, of Tom Roberts sitting beside his unfinished painting of the opening of the first Commonwealth Parliament, in the Royal Exhibition Building, Melbourne",
            "caption": "Tom Roberts at work on <i>The Opening of the First Parliament of the Commonwealth of Australia</i>, 9 May 1901, in the Royal Exhibition Building, Melbourne. The painting was completed in 1903. Photograph, about 1903.",
            "credit": "Gelatin silver print, about 1903, Mitchell Library, State Library of New South Wales. Public domain (Australia). Please acknowledge the Mitchell Library, State Library of New South Wales. "
                      + clink("https://commons.wikimedia.org/wiki/File:TomRobertsUnfinished.jpg", "Wikimedia Commons") + ".",
        },
    }

    def apply_rights(m):
        fname = m.group(1)
        info = IMAGE_RIGHTS.get(fname)
        if not info:
            return m.group(0)
        img = (
            f'<img src="{vsrc(info["src"])}" alt="{info["alt"]}" loading="lazy" />'
        )
        cap = f'{info["caption"]} <span class="credit">{info["credit"]}</span>'
        return f"<figure>\n        {img}\n        <figcaption>{cap}</figcaption>\n      </figure>"

    html, n_rights = re.subn(
        r'<figure>\s*<img src="assets/([^"?]+)[^>]*>\s*<figcaption>(.*?)</figcaption>\s*</figure>',
        apply_rights,
        html,
        flags=re.S,
    )
    if n_rights != 5:
        raise SystemExit(f"timeline builder: expected 5 credited figures, applied {n_rights}")
    if "lake-mungo.png" in html:
        raise SystemExit("timeline builder: old Lake Mungo filename still present")

    # Wrap remaining figures' images for lightbox
    def wrap_fig(m):
        img = m.group(1)
        cap = m.group(2)
        # don't double-wrap
        if "button class=\"zoom\"" in img:
            return m.group(0)
        return f"<figure>\n        <button type=\"button\" class=\"zoom\" aria-label=\"Enlarge the image\">{img}</button>\n        <figcaption>{cap}</figcaption>\n      </figure>"

    html = re.sub(
        r"<figure>\s*(<img[^>]+>)\s*<figcaption>(.*?)</figcaption>\s*</figure>",
        wrap_fig,
        html,
        flags=re.S,
    )

    # Strip year levels from student cards
    html = html.replace('<span class="tag">Full case in Year 9 series</span>', "")
    html = re.sub(r"Full case in Year 9 series", "", html)

    # Casebook links, kept here so a rebuild from the Muse source does not drop them.
    BC = "https://robmac10.github.io/reopen-the-record/#p=37"
    BM = "https://robmac10.github.io/reopen-the-record/#p=70"
    btn_bc = (
        '<a class="appbtn small light" href="%s" target="_blank" rel="noopener">'
        "Britain Claims case \u2192</a>" % BC
    )
    btn_bm = (
        '<a class="appbtn small" href="%s" target="_blank" rel="noopener">'
        "Blue Mountains case \u2192</a>" % BM
    )
    def add_btn(html, after, btn, label):
        if after not in html:
            raise SystemExit("timeline builder: %s block not found" % label)
        if btn in html.split(after, 1)[1][:400]:
            return html
        return html.replace(after, after + "\n          " + btn, 1)

    html = add_btn(
        html,
        '          <a class="appbtn small light" href="https://robmac10.github.io/the-claim/" target="_blank" rel="noopener">The Claim \u2192</a>',
        btn_bc,
        "Kamay / The Claim button",
    )
    html = add_btn(
        html,
        '          <a class="appbtn small light" href="https://robmac10.github.io/cook-case/" target="_blank" rel="noopener">Cook case \u2192</a>',
        btn_bc,
        "Possession Island / Cook case button",
    )
    # Warrane: the first The Claim button after that heading
    _w = 'Warrane \u2014 The Fleet Moves to Sydney Cove'
    if _w not in html:
        raise SystemExit("timeline builder: Warrane heading not found")
    pre, rest = html.split(_w, 1)
    needle = '          <a class="appbtn small" href="https://robmac10.github.io/the-claim/" target="_blank" rel="noopener">The Claim \u2192</a>'
    if needle not in rest:
        raise SystemExit("timeline builder: Warrane The Claim button not found")
    rest = rest.replace(needle, needle + "\n          " + btn_bc, 1)
    html = pre + _w + rest
    # Blue Mountains: on the Bungaree card, uniquely followed by the 1804-1838 Frontier card
    _bm = "Bungaree Sails Around the Continent"
    if _bm not in html:
        raise SystemExit("timeline builder: Bungaree/Blue Mountains heading not found")
    pre, rest = html.split(_bm, 1)
    if needle not in rest:
        raise SystemExit("timeline builder: Bungaree The Claim button not found")
    rest = rest.replace(needle, needle + "\n          " + btn_bm, 1)
    html = pre + _bm + rest


    # Footer + lightbox + JS before </body>
    html = html.replace("</body>", FOOT + LIGHTBOX_JS + "\n</body>", 1)

    # lang
    html = html.replace('<html lang="en">', '<html lang="en-AU">', 1)

    OUT.write_text(html, encoding="utf-8")
    # sanity
    text = OUT.read_text(encoding="utf-8")
    assert "rock-art.jpg" not in text
    assert "lake-mungo.png" not in text
    assert "noindex" in text
    assert "Year 9" not in text
    assert "lightbox" in text
    assert f"v={ASSET_V}" in text
    assert "CC0 1.0" in text
    assert "Rijksmuseum, Amsterdam" in text
    assert "CC BY-SA 4.0" in text
    assert "Vunz" in text
    assert "Raffaello Carboni" in text
    assert "The Eureka Stockade" in text
    assert "The original Eureka flag, conserved" not in text
    assert "Mitchell Library, State Library of New South Wales" in text
    assert "Robin" not in text
    assert "McKean" not in text
    assert "reopen-the-record/#p=37" in text
    assert "reopen-the-record/#p=70" in text
    assert text.count("reopen-the-record/#p=37") >= 3  # three claim cards plus teacher note
    assert text.count("reopen-the-record/#p=70") >= 2  # mountains card plus teacher note
    print("wrote", OUT, "bytes", OUT.stat().st_size)

if __name__ == "__main__":
    main()
