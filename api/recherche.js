// Recherche IA dans les éditions passées (fonction serveur Vercel).
// La clé est lue dans la variable d'environnement ANTHROPIC_API_KEY,
// réglée dans Vercel : jamais dans le code.
const corpus = require("./corpus.json");

const MODELE = "claude-haiku-5-5";
const CORPUS_TEXTE = corpus
  .map(e => `<edition n="${e.n}" url="${e.url}" titre="${e.titre}">\n${e.texte}\n</edition>`)
  .join("\n\n");

// Limite simple : 10 recherches par minute et par adresse (par instance).
const vus = new Map();
function trop(ip) {
  const now = Date.now();
  const l = (vus.get(ip) || []).filter(t => now - t < 60000);
  l.push(now);
  vus.set(ip, l);
  return l.length > 10;
}

module.exports = async (req, res) => {
  if (req.method !== "POST") return res.status(405).json({ erreur: "POST attendu" });
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0] || "?";
  if (trop(ip)) return res.status(429).json({ erreur: "Trop de recherches, réessayez dans une minute." });

  const q = String((req.body && req.body.q) || "").trim().slice(0, 300);
  if (q.length < 3) return res.status(400).json({ erreur: "Décrivez un peu plus ce que vous cherchez." });

  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: MODELE,
      max_tokens: 800,
      system: [
        {
          type: "text",
          text:
            "Tu aides un lecteur à retrouver un sujet dans les éditions passées de « La Newsletter IA ». " +
            "Réponds UNIQUEMENT par un JSON : {\"resultats\":[{\"n\":<numéro>,\"url\":\"<url>\",\"pourquoi\":\"<une phrase en français>\"}]}, " +
            "au plus 3 éditions, la plus pertinente d'abord, liste vide si rien ne correspond. N'invente rien.",
        },
        { type: "text", text: CORPUS_TEXTE, cache_control: { type: "ephemeral" } },
      ],
      messages: [{ role: "user", content: q }],
    }),
  });

  if (!r.ok) {
    console.error("Anthropic", r.status, await r.text());
    return res.status(502).json({ erreur: "La recherche est indisponible pour le moment." });
  }
  const data = await r.json();
  const brut = (data.content || []).map(c => c.text || "").join("");
  try {
    const json = JSON.parse(brut.slice(brut.indexOf("{"), brut.lastIndexOf("}") + 1));
    const titres = Object.fromEntries(corpus.map(e => [e.n, e.titre]));
    const resultats = (json.resultats || [])
      .filter(x => titres[x.n])
      .map(x => ({ n: x.n, url: `editions/n${x.n}.html`, titre: titres[x.n], pourquoi: x.pourquoi }));
    res.status(200).json({ resultats });
  } catch {
    res.status(502).json({ erreur: "Réponse illisible, reformulez votre recherche." });
  }
};
