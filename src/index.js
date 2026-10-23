export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/ip") {
      return Response.json({
        ip: request.headers.get("CF-Connecting-IP"),
        country: request.cf?.country ?? null,
      });
    }

    // the page posts its results here
    if (url.pathname === "/submit" && request.method === "POST") {
      const id = url.searchParams.get("id") || "";
      if (id.length < 16) return new Response("bad id", { status: 400 });
      const body = await request.text();
      if (body.length > 1_000_000) return new Response("too large", { status: 413 });
      await env.RESULTS.put("r:" + id, body, { expirationTtl: 3600 });
      return Response.json({ ok: true });
    }

    // Luau reads them here
    if (url.pathname === "/result") {
      const id = url.searchParams.get("id") || "";
      const v = id.length >= 16 ? await env.RESULTS.get("r:" + id) : null;
      if (!v) return Response.json({ error: "none" }, { status: 404 });
      return new Response(v, { headers: { "content-type": "application/json" } });
    }

    return env.ASSETS.fetch(request);
  },
};