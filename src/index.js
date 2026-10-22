export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/ip") {
      return Response.json({
        ip: request.headers.get("CF-Connecting-IP"),
        country: request.cf?.country ?? null,
      });
    }

    // everything else: serve your static site from docs/
    return env.ASSETS.fetch(request);
  },
};