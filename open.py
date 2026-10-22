<<<<<<< HEAD
from playwright.sync_api import sync_playwright
import time

JS = """() => new Promise(resolve => {
    const pc = new RTCPeerConnection({iceServers:[{urls:'stun:stun.l.google.com:19302'}]});
    const out = [];
    pc.createDataChannel('x');
    pc.onicecandidate = e => e.candidate ? out.push(e.candidate.candidate) : resolve(out);
    pc.createOffer().then(o => pc.setLocalDescription(o));
    setTimeout(() => resolve(out), 4000);
})"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=False)      # visible window
    page = b.new_page()
    page.goto("http://localhost:8000/index.html")
    page.wait_for_function("window.Fingerprint", timeout=30000)

    candidates = page.evaluate(JS)

    text = "\n".join(candidates) if candidates else "No WebRTC candidates (blocked or none found)"
    print(text)

    # show the result on the page itself
    page.evaluate("""(t) => {
        const d = document.createElement('pre');
        d.textContent = 'WebRTC result:\\n' + t;
        d.style.cssText = 'position:fixed;top:10px;right:10px;z-index:99999;background:#000;color:#0f0;padding:12px;max-width:600px;white-space:pre-wrap;font:12px monospace;';
        document.body.appendChild(d);
    }""", text)

    time.sleep(600)    # keep the window open
=======
from playwright.sync_api import sync_playwright
import time

JS = """() => new Promise(resolve => {
    const pc = new RTCPeerConnection({iceServers:[{urls:'stun:stun.l.google.com:19302'}]});
    const out = [];
    pc.createDataChannel('x');
    pc.onicecandidate = e => e.candidate ? out.push(e.candidate.candidate) : resolve(out);
    pc.createOffer().then(o => pc.setLocalDescription(o));
    setTimeout(() => resolve(out), 4000);
})"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=False)      # visible window
    page = b.new_page()
    page.goto("http://localhost:8000/index.html")
    page.wait_for_function("window.Fingerprint", timeout=30000)

    candidates = page.evaluate(JS)

    text = "\n".join(candidates) if candidates else "No WebRTC candidates (blocked or none found)"
    print(text)

    # show the result on the page itself
    page.evaluate("""(t) => {
        const d = document.createElement('pre');
        d.textContent = 'WebRTC result:\\n' + t;
        d.style.cssText = 'position:fixed;top:10px;right:10px;z-index:99999;background:#000;color:#0f0;padding:12px;max-width:600px;white-space:pre-wrap;font:12px monospace;';
        document.body.appendChild(d);
    }""", text)

    time.sleep(600)    # keep the window open
>>>>>>> 0e4fb2169589d002539e1c9eef918bf2dc4c0060
    b.close()