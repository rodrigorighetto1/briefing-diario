"""
=============================================================
  BRIEFING DIÁRIO DE NOTÍCIAS — Rodrigo
  Versão 2 — SMTP (sem OAuth, funciona na nuvem)
=============================================================
"""

import feedparser
import anthropic
import smtplib
import json
import os
import re
import hashlib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
EMAIL_DESTINO     = os.getenv("EMAIL_DESTINO")
EMAIL_REMETENTE   = os.getenv("EMAIL_REMETENTE")
GMAIL_SMTP_SENHA  = os.getenv("GMAIL_SMTP_SENHA")

BASE_DIR   = Path(__file__).parent
CACHE_FILE = BASE_DIR / "noticias_cache.json"

RSS_FEEDS = [
    {"nome": "UOL",       "url": "https://rss.uol.com.br/feed/noticias.xml",                        "cat": ["politica", "brasil"]},
    {"nome": "UOL Econ",  "url": "https://rss.uol.com.br/feed/economia.xml",                        "cat": ["economia", "brasil"]},
    {"nome": "Estadão",   "url": "https://feeds.estadao.com.br/rss/rss2.0/economia.xml",             "cat": ["economia", "brasil"]},
    {"nome": "Estadão Pol","url": "https://feeds.estadao.com.br/rss/rss2.0/politica.xml",            "cat": ["politica", "brasil"]},
    {"nome": "Folha",     "url": "https://feeds.folha.uol.com.br/folha/dinheiro/rss091.xml",         "cat": ["economia", "brasil"]},
    {"nome": "Folha Pol", "url": "https://feeds.folha.uol.com.br/folha/brasil/rss091.xml",           "cat": ["politica", "brasil"]},
    {"nome": "WSJ",       "url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",                     "cat": ["geopolitica", "economia"]},
    {"nome": "WSJ Mkt",   "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",                   "cat": ["mercados"]},
    {"nome": "Investing",  "url": "https://br.investing.com/rss/news_288.rss",                       "cat": ["mercados", "economia"]},
    {"nome": "Inv Cripto", "url": "https://br.investing.com/rss/news_301.rss",                       "cat": ["cripto"]},
    {"nome": "Bloomberg",  "url": "https://feeds.bloomberg.com/markets/news.rss",                    "cat": ["mercados", "economia"]},
    {"nome": "InfoMoney",  "url": "https://www.infomoney.com.br/feed/",                              "cat": ["mercados", "brasil", "cripto"]},
    {"nome": "InfoM Cri",  "url": "https://www.infomoney.com.br/mercados/criptomoedas/feed/",        "cat": ["cripto"]},
]

KEYWORDS = {
    "geopolitica": ["guerra", "conflito", "otan", "nato", "rússia", "ukraine", "ucrânia",
                    "oriente médio", "israel", "hamas", "houthi", "mar vermelho", "china",
                    "taiwan", "militares", "sanções", "geopolítica"],
    "politica":    ["congresso", "senado", "câmara", "lula", "governo federal", "ministério",
                    "partido", "eleição", "reforma", "aprovado", "votação", "presidente"],
    "economia":    ["fed", "banco central", "juros", "inflação", "pib", "recessão",
                    "dólar", "euro", "câmbio", "commodity", "petróleo", "ouro", "estímulo",
                    "powell", "bce", "fmi", "banco mundial"],
    "brasil":      ["brasil", "brasileiro", "bovespa", "ibovespa", "selic", "ipca",
                    "b3", "petrobras", "vale", "embraer", "real", "brl"],
    "cripto":      ["bitcoin", "btc", "ethereum", "eth", "cripto", "blockchain",
                    "altcoin", "defi", "nft", "halving", "binance", "coinbase", "etf cripto"],
    "mercados":    ["ibovespa", "s&p", "nasdaq", "dow jones", "bolsa", "ações",
                    "mercado", "pregão", "alta", "queda", "volatilidade", "índice"],
}

def carregar_cache() -> set:
    if CACHE_FILE.exists():
        try:
            data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            cutoff = (datetime.now() - timedelta(days=3)).isoformat()
            return {k for k, v in data.items() if v > cutoff}
        except Exception:
            return set()
    return set()

def salvar_cache(cache: set):
    agora = datetime.now().isoformat()
    data = {h: agora for h in cache}
    CACHE_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

def hash_noticia(titulo: str) -> str:
    return hashlib.md5(titulo.lower().strip().encode()).hexdigest()

def detectar_categoria(texto: str) -> list:
    texto_lower = texto.lower()
    cats = []
    for cat, kws in KEYWORDS.items():
        if any(kw in texto_lower for kw in kws):
            cats.append(cat)
    return cats or ["geral"]

def limpar_html(texto: str) -> str:
    return re.sub(r"<[^>]+>", "", texto or "").strip()

def buscar_noticias() -> list:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Buscando feeds RSS...")
    cache = carregar_cache()
    todas = []
    ontem = datetime.now() - timedelta(hours=30)

    for feed_cfg in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_cfg["url"])
            for entry in feed.entries[:15]:
                titulo = limpar_html(getattr(entry, "title", ""))
                if not titulo:
                    continue
                h = hash_noticia(titulo)
                if h in cache:
                    continue
                pub = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub = datetime(*entry.published_parsed[:6])
                    if pub < ontem:
                        continue
                resumo = limpar_html(
                    getattr(entry, "summary", "") or getattr(entry, "description", "")
                )[:600]
                link = getattr(entry, "link", "")
                cats_detectadas = detectar_categoria(titulo + " " + resumo)
                cats_finais = list(set(feed_cfg["cat"] + cats_detectadas))
                todas.append({
                    "id": h, "titulo": titulo, "resumo": resumo,
                    "link": link, "fonte": feed_cfg["nome"],
                    "cats": cats_finais,
                    "pub": pub.isoformat() if pub else datetime.now().isoformat(),
                })
                cache.add(h)
        except Exception as e:
            print(f"  [ERRO] {feed_cfg['nome']}: {e}")

    salvar_cache(cache)
    print(f"  → {len(todas)} notícias novas coletadas")
    return todas

def deduplicar(noticias: list) -> list:
    grupos = []
    usadas = set()
    for i, n in enumerate(noticias):
        if i in usadas:
            continue
        grupo = [n]
        palavras_i = set(re.sub(r'\W+', ' ', n["titulo"].lower()).split())
        for j, m in enumerate(noticias):
            if j <= i or j in usadas:
                continue
            palavras_j = set(re.sub(r'\W+', ' ', m["titulo"].lower()).split())
            stop = {"de","da","do","das","dos","e","o","a","os","as","em","no",
                    "na","por","para","com","um","uma","que","se","é"}
            pi = palavras_i - stop
            pj = palavras_j - stop
            overlap = len(pi & pj) / max(len(pi), len(pj), 1)
            if overlap > 0.40:
                grupo.append(m)
                usadas.add(j)
        usadas.add(i)
        melhor_titulo = max(grupo, key=lambda x: len(x["titulo"]))["titulo"]
        fontes = list(dict.fromkeys(g["fonte"] for g in grupo))
        resumos_por_fonte = []
        frases_vistas = set()
        for g in grupo:
            frases = [f.strip() for f in re.split(r'(?<=[.!?])\s+', g["resumo"]) if len(f.strip()) > 20]
            novas = []
            for frase in frases:
                fp = " ".join(frase.lower().split()[:6])
                if fp not in frases_vistas:
                    frases_vistas.add(fp)
                    novas.append(frase)
            if novas:
                resumos_por_fonte.append(f"[{g['fonte']}] " + " ".join(novas))
        resumo_combinado = " | ".join(resumos_por_fonte)
        cats = list(set(cat for g in grupo for cat in g["cats"]))
        grupos.append({
            **grupo[0],
            "titulo": melhor_titulo,
            "fontes": fontes,
            "resumo": resumo_combinado,
            "links":  [g["link"] for g in grupo if g.get("link")],
            "cats":   cats,
        })
    return grupos

def gerar_resumo_claude(noticias: list) -> str:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Gerando resumo com Claude...")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    by_cat = {
        "geopolitica": [], "politica": [], "economia": [],
        "brasil": [], "cripto": [], "mercados": [], "geral": []
    }
    for n in noticias:
        colocado = False
        for cat in ["cripto", "mercados", "brasil", "economia", "geopolitica", "politica"]:
            if cat in n["cats"]:
                by_cat[cat].append(n)
                colocado = True
                break
        if not colocado:
            by_cat["geral"].append(n)

    noticias_json = json.dumps(
        {cat: [{"titulo": n["titulo"], "resumo": n["resumo"],
                "fontes": n.get("fontes", [n["fonte"]]), "link": n["link"]}
               for n in items[:8]]
         for cat, items in by_cat.items() if items},
        ensure_ascii=False, indent=2
    )

    data_hoje = datetime.now().strftime("%d de %B de %Y")
    prompt = f"""Você é um analista financeiro e jornalista especializado em mercados globais.
Hoje é {data_hoje}.

Abaixo estão notícias já pré-agrupadas por assunto, coletadas de múltiplas fontes
(UOL, Estadão, Folha, WSJ, Bloomberg, Investing, InfoMoney).
Cada entrada já vem com trechos separados por fonte no formato: [NomeFonte] texto | [NomeFonte] texto

Crie um BRIEFING DIÁRIO completo e profissional em HTML para email.

REGRAS CRÍTICAS:
1. Cada assunto aparece UMA SÓ VEZ
2. Para cada notícia, escreva UM parágrafo unificado de 3-5 linhas que incorpora
   APENAS informações NOVAS e COMPLEMENTARES de cada fonte
3. Cite todas as fontes ao final: [Bloomberg, WSJ, InfoMoney]
4. Destaque implicações para investidores brasileiros
5. Adicione seção "Conexões Macro" ao final

FORMATO HTML para email (tabelas, sem CSS externo):
- Fundo #ffffff, títulos #1a1a2e, texto #333333, destaques #0f3460
- Tag de categoria colorida antes de cada título
- Fontes em cinza discreto ao final de cada item

Notícias:
{noticias_json}

Retorne APENAS o HTML do corpo (sem DOCTYPE, html, head ou body).
"""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def enviar_email(html_content: str, num_noticias: int):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Enviando email...")
    data_str = datetime.now().strftime("%d/%m/%Y")

    html_completo = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Georgia,serif;">
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f4f4f4">
<tr><td align="center" style="padding:20px 10px;">
<table width="660" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;">
<tr><td style="background:#1a1a2e;padding:28px 32px;">
  <div style="font-size:11px;color:#7a8bb0;letter-spacing:3px;text-transform:uppercase;margin-bottom:4px;">Briefing Diário</div>
  <div style="font-size:24px;font-weight:bold;color:#ffffff;">Resumo de Mercados & Notícias</div>
  <div style="font-size:13px;color:#8892b0;margin-top:6px;">{data_str} · {num_noticias} tópicos analisados</div>
</td></tr>
<tr><td style="padding:28px 32px;">{html_content}</td></tr>
<tr><td style="background:#f8f9fa;border-top:1px solid #e9ecef;padding:16px 32px;">
  <div style="font-size:11px;color:#999999;">
    Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")} BRT<br>
    Fontes: UOL, Estadão, Folha, WSJ, Bloomberg, Investing.com, InfoMoney
  </div>
</td></tr>
</table></td></tr></table>
</body></html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Briefing Diário — {datetime.now().strftime('%d/%m/%Y')}"
    msg["From"]    = EMAIL_REMETENTE
    msg["To"]      = EMAIL_DESTINO
    msg.attach(MIMEText(html_completo, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_REMETENTE, GMAIL_SMTP_SENHA)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())

    print(f"  → Email enviado para {EMAIL_DESTINO}")

def main():
    print("=" * 60)
    print(f"  BRIEFING DIÁRIO — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    try:
        noticias_raw = buscar_noticias()
        if not noticias_raw:
            print("[AVISO] Nenhuma notícia nova encontrada.")
            return
        noticias = deduplicar(noticias_raw)
        print(f"  → {len(noticias)} tópicos únicos após deduplicação")
        html_resumo = gerar_resumo_claude(noticias)
        backup_file = BASE_DIR / f"briefing_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
        backup_file.write_text(html_resumo, encoding="utf-8")
        print(f"  → Backup salvo: {backup_file.name}")
        enviar_email(html_resumo, len(noticias))
        print("\n✅ Briefing enviado com sucesso!")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()