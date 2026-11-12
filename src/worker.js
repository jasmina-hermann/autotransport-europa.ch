// Leitet alle Varianten auf eine einzige Adresse um, damit Google nur
// https://www.autotransport-europa.ch/... sieht (keine Duplikate).
const HOST = 'www.autotransport-europa.ch';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // http://, autotransport-europa.ch (ohne www) und *.workers.dev -> https://www.
    const wrongHost = url.hostname === 'autotransport-europa.ch' || url.hostname.endsWith('.workers.dev');
    if (wrongHost || (url.hostname === HOST && url.protocol === 'http:')) {
      url.protocol = 'https:';
      url.hostname = HOST;
      return Response.redirect(url.toString(), 301);
    }

    const res = await env.ASSETS.fetch(request);

    // Cloudflare leitet /index.html -> / und /agb.html -> /agb nur
    // vorübergehend (307) um. Für Google dauerhaft (301) daraus machen.
    if (res.status === 307 || res.status === 308) {
      const location = res.headers.get('Location');
      if (location) return Response.redirect(new URL(location, url).toString(), 301);
    }
    return res;
  },
};
