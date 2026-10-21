import os
from flask import Blueprint, make_response, redirect, render_template_string, request
paywall_bp = Blueprint("paywall", __name__, url_prefix="/paywall")

DONATE_URL = os.environ.get("DONATE_URL", "https://ko-fi.com/zzyzx_x")
PRICE_TEXT = "Free"

COOKIE_NAME = "ads_removed"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365

ADS = [
    {"slot": "top", "title": "Your ad could be here", "text": "Wide banner, top of the page"},
    {"slot": "left", "title": "Advertise here", "text": "Tall banner, left side"},
    {"slot": "right", "title": "Advertise here", "text": "Tall banner, right side"},
    {"slot": "bottom", "title": "Your ad could be here", "text": "Wide banner, bottom of the page"},
]

def ads_removed() -> bool:
    return request.cookies.get(COOKIE_NAME) == "1"
 
 
@paywall_bp.post("/remove-ads")
def remove_ads():

    response = make_response(redirect("/"))
    response.set_cookie(COOKIE_NAME, "1", max_age=COOKIE_MAX_AGE, samesite="Lax", httponly=True)
    return response

@paywall_bp.post("/restore-ads")
def restore_ads():
    response = make_response(redirect("/"))
    response.delete_cookie(COOKIE_NAME, samesite="Lax")
    return response


@paywall_bp.after_app_request
def add_paywall_ui(response):
    
    if response.status_code != 200 or response.direct_passthrough or response.mimetype != "text/html":
        return response
 
    html = response.get_data(as_text=True)
    end = html.rfind("</body>")
    if end == -1:
        return response
 
    ui = render_template_string(
        UI_TEMPLATE,
        ads=ADS,
        ads_removed=ads_removed(),
        donate_url=DONATE_URL,
        price=PRICE_TEXT,
    )
    response.set_data(html[:end] + ui + html[end:])
    response.vary.add("Cookie")  # the page differs depending on the cookie
    return response



UI_TEMPLATE = """
<style>
    /*buttons*/
  .pw-bar {
    position: fixed; z-index: 950; left: 50%; transform: translateX(-50%);
    bottom: 16px; display: flex; gap: 10px;
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  }
  .pw-bar.with-ads { bottom: 100px; }
  .pw-btn {
    font: 600 14px/1 system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: 11px 18px; border-radius: 999px; border: 0; cursor: pointer;
    text-decoration: none; display: inline-block; white-space: nowrap;
  }
  .pw-btn.remove { background: #fff; color: #111; }
  .pw-btn.donate { background: #f2b134; color: #1a1200; }
  .pw-btn:hover { filter: brightness(0.92); }
  .pw-btn:focus-visible { outline: 3px solid #8fc7ff; outline-offset: 2px; }
 
  /*ads*/
  .pw-ad {
    position: fixed; z-index: 900; box-sizing: border-box; overflow: hidden;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 3px; padding: 8px; text-align: center; text-decoration: none;
    border: 1px dashed rgba(255, 255, 255, 0.35); border-radius: 6px;
    background: rgba(255, 255, 255, 0.07); color: #fff;
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  }
  .pw-ad .pw-tag { font-size: 11px; opacity: 0.55; }
  .pw-ad strong { font-size: 15px; font-weight: 600; }
  .pw-ad .pw-sub { font-size: 12px; opacity: 0.8; }
  .pw-top, .pw-bottom { left: 50%; transform: translateX(-50%); width: min(728px, calc(100% - 16px)); height: 80px; }
  .pw-top { top: 8px; }
  .pw-bottom { bottom: 8px; }
  .pw-left, .pw-right { top: 50%; transform: translateY(-50%); width: 140px; height: min(600px, calc(100% - 240px)); }
  .pw-left { left: 8px; }
  .pw-right { right: 8px; }
 
  /* Keep the existing page content clear of the ads (only while ads are showing). */
  .pw-has-ads .gradient { box-sizing: border-box; padding: 96px 164px 190px; overflow-y: auto; }
 
  /* Phones: no room for the tall side ads, so they step aside. */
  @media (max-width: 720px) {
    .pw-left, .pw-right { display: none; }
    .pw-has-ads .gradient { padding-left: 16px; padding-right: 16px; }
  }
 
  /* ---- paywall popup ---- */
  #pw-dialog {
    border: 0; border-radius: 14px; padding: 28px; width: min(380px, calc(100% - 32px));
    background: #1d1d1d; color: #fff; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  }
  #pw-dialog::backdrop { background: rgba(0, 0, 0, 0.65); }
  #pw-dialog h2 { margin: 0 0 6px; font-size: 22px; }
  #pw-dialog p { margin: 0 0 18px; line-height: 1.5; color: #d0d0d0; }
  #pw-dialog .pw-price { font-size: 40px; font-weight: 700; margin: 0 0 4px; color: #fff; }
  #pw-dialog .pw-actions { display: flex; gap: 10px; flex-wrap: wrap; }
  #pw-dialog .pw-btn.ghost { background: transparent; color: #fff; box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.4); }
  @media (prefers-reduced-motion: no-preference) {
    #pw-dialog[open] { animation: pw-pop 0.18s ease-out; }
    @keyframes pw-pop { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
  }
</style>
 
{% if not ads_removed %}
  <script>document.body.classList.add("pw-has-ads");</script>
  {% for ad in ads %}
    {% if ad.url %}<a class="pw-ad pw-{{ ad.slot }}" href="{{ ad.url }}" target="_blank" rel="sponsored noopener noreferrer" aria-label="Advertisement">
    {% else %}<div class="pw-ad pw-{{ ad.slot }}" aria-label="Advertisement">{% endif %}
      <span class="pw-tag">Advertisement</span>
      <strong>{{ ad.title }}</strong>
      <span class="pw-sub">{{ ad.text }}</span>
    {% if ad.url %}</a>{% else %}</div>{% endif %}
  {% endfor %}
{% endif %}
 
<div class="pw-bar {{ 'with-ads' if not ads_removed }}">
  <button type="button" class="pw-btn remove" id="pw-open">{{ 'Ads are off' if ads_removed else 'Remove ads' }}</button>
  <a class="pw-btn donate" href="{{ donate_url }}" target="_blank" rel="noopener noreferrer">Donate</a>
</div>
 
<dialog id="pw-dialog" aria-labelledby="pw-title">
  {% if ads_removed %}
    <form method="post" action="/paywall/restore-ads">
      <h2 id="pw-title">Ads are off</h2>
      <p>You won't see ads on this device. Want them back?</p>
      <div class="pw-actions">
        <button type="button" class="pw-btn remove" data-pw-close>Keep them off</button>
        <button type="submit" class="pw-btn ghost">Bring ads back</button>
      </div>
    </form>
  {% else %}
    <form method="post" action="/paywall/remove-ads">
      <h2 id="pw-title">Remove ads</h2>
      <div class="pw-price">{{ price }}</div>
      <p>No card and no account. One click and the ads are gone on this device. If you like the site, the Donate button helps keep it running.</p>
      <div class="pw-actions">
        <button type="submit" class="pw-btn remove">Remove ads for {{ price|lower }}</button>
        <button type="button" class="pw-btn ghost" data-pw-close>Not now</button>
      </div>
    </form>
  {% endif %}
</dialog>
 
<script>
  (function () {
    var dialog = document.getElementById("pw-dialog");
    var open = document.getElementById("pw-open");
    if (!dialog || !open || !dialog.showModal) return;
    open.addEventListener("click", function () { dialog.showModal(); });
    dialog.querySelectorAll("[data-pw-close]").forEach(function (b) {
      b.addEventListener("click", function () { dialog.close(); });
    });
  })();
</script>
"""