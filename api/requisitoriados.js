export default async function handler(req, res) {
  const { q } = req.query;
  if (!q) return res.status(400).json({ error: "Missing q" });

  const tokenSuffix = "BVQbU1vEVO";
  const encoded = encodeURIComponent(q.trim().toLowerCase());
  const target = `https://recompensas.pe/requisitoriados/list/N-${encoded}-${tokenSuffix}`;

  try {
    const resp = await fetch(target, {
      headers: {
        "User-Agent": "Mozilla/5.0 (VercelFetcher)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "es-PE,es;q=0.9,en;q=0.7",
        "Cache-Control": "no-cache"
      }
    });

    const html = await resp.text();
    res.status(200).json({
      status: resp.status,
      ok: resp.ok,
      target,
      length: html.length,
      html
    });
  } catch (e) {
    res.status(500).json({ error: e.message, target });
  }
}
