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

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
EMAIL_DESTINO     = os.environ.get("EMAIL_DESTINO", "")
EMAIL_REMETENTE   = os.environ.get("EMAIL_REMETENTE", "")
GMAIL_SMTP_SENHA  = os.environ.get("GMAIL_SMTP_SENHA", "")

BASE_DIR   = Path(__file__).parent
CACHE_FILE = BASE_DIR / "noticias_cache.json"

RSS_FEEDS = [
    {"nome": "UOL",        "url": "https://rss.uol.com.br/feed/noticias.xml",                      "cat": ["politica", "brasil"]},
    {"nome": "UOL Econ",   "url": "https://rss.uol.com.br/feed/economia.xml",                      "cat": ["economia", "brasil"]},
    {"nome": "Estadao",    "url": "https://feeds.estadao.com.br/rss/rss2.0/economia.xml",           "cat": ["economia", "brasil"]},
    {"nome": "Estadao Pol","url": "https://feeds.estadao.com.br/rss/rss2.0/politica.xml",           "cat": ["politica", "brasil"]},
    {"nome": "Folha",      "url": "https://feeds.folha.uol.com.br/folha/dinheiro/rss091.xml",       "cat": ["economia", "brasil"]},
    {"nome": "Folha Pol",  "url": "https://feeds.folha.uol.com.br/folha/brasil/rss091.xml",         "cat": ["politica", "brasil"]},
    {"nome": "WSJ",        "url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",                   "cat": ["geopolitica", "economia"]},
    {"nome": "WSJ Mkt",    "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",                 "cat": ["mercados"]},
    {"nome": "Investing",  "url": "https://br.investing.com/rss/news_288.rss",                     "cat": ["mercados", "economia"]},
    {"nome": "Inv Cripto", "url": "https://br.investing.com/rss/news_301.rss",                     "cat": ["cripto"]},
    {"nome": "Bloomberg",  "url": "https://feeds.bloomberg.com/markets/news.rss",                  "cat": ["mercados", "economia"]},
    {"nome": "InfoMoney",  "url": "https://www.infomoney.com.br/feed/",                            "cat": ["mercados", "brasil", "cripto"]},
    {"nome": "InfoM Cri",  "url": "https://www.infomoney.com.br/mercados/criptomoedas/feed/",      "cat": ["cripto"]},
]

KEYWORDS = {
    "geopolitica": ["guerra","conflito","otan","nato","russia","ukraine","ucr","oriente medio","israel","hamas","houthi","mar vermelho","china","taiwan","militares","sancoes","geopolitica"],
    "politica":    ["congresso","senado","camara","lula","governo federal","ministerio","partido","eleicao","reforma","aprovado","votacao","presidente"],
    "economia":    ["fed","banco central","juros","inflacao","pib","recessao","dolar","euro","cambio","commodity","petroleo","ouro","estimulo","powell","bce","fmi","banco mundial"],
    "brasil":      ["brasil","brasileiro","bovespa","ibovespa","selic","ipca","b3","petrobras","vale","embraer","real","brl"],
    "cripto":      ["bitcoin","btc","ethereum","eth","cripto","blockchain","altcoin","defi","nft","halving","binance","coinbase"],
    "mercados":    ["ibovespa","s&p","nasdaq","dow jones","bolsa","acoes","mercado","pregao","alta","queda","volatilidade","indice"],
}

def carregar_cache():
    if CACHE_FILE.exists():
        try:
            data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            cutoff = (datetime.now() - timedelta(days=3)).isoformat()
            return {k for k, v in data.items() if v > cutoff}
        except Exception:
            return set()
    return set()

def salvar_cache(cache):
    agora = datetime.now().isoformat()
    data = {h: agora for h in cache}
    CACHE_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

def hash_noticia(titulo):
    return hashlib.md5(titulo.lower().strip().encode()).hexdigest()

def detectar_categoria(texto):
    texto_lower = texto.lower()
    cats = []
    for cat, kws in KEYWORDS.items():
        if any(kw in texto_lower for kw in kws):
            cats.append(cat)
    return cats or ["geral"]

def limpar_html(texto):
    return re.sub(r"<[^>]+>", "", texto or "").strip()

def buscar_noticias():
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
                resumo = limpar_html(getattr(entry, "summary", "") or getattr(entry, "description", ""))[:600]
                link = getattr(entry, "link", "")
                cats = list(set(feed_cfg["cat"] + detectar_categoria(titulo + " " + resumo)))
                todas.append({"id": h, "titulo": titulo, "resumo": resumo, "link": link, "fonte": feed_cfg["nome"], "cats": cats, "pub": pub.isoformat() if pub else datetime.now().isoformat()})
                cache.add(h)
        except Exception as e:
            print(f"  [ERRO] {feed_cfg['nome']}: {e}")
    salvar_cache(cache)
    print(f"  -> {len(todas)} noticias novas coletadas")
    return todas

def deduplicar(noticias):
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
            stop = {"de","da","do","das","dos","e","o","a","os","as","em","no","na","por","para","com","um","uma","que","se"}
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
        grupos.append({**grupo[0], "titulo": melhor_titulo, "fontes": fontes, "resumo": " | ".join(resumos_por_fonte), "links": [g["link"] for g in grupo if g.get("link")], "cats": list(set(cat for g in grupo for cat in g["cats"]))})
    return grupos

def gerar_resumo_claude(noticias):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Gerando resumo com Claude...")
    
    api_key = ANTHROPIC_API_KEY.strip().strip('"').strip("'")
    print(f"API key primeiros chars: {api_key[:10]}")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    by_cat = {"geopolitica": [], "politica": [], "economia": [], "brasil": [], "cripto": [], "mercados": [], "geral": []}
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
        {cat: [{"titulo": n["titulo"], "resumo": n["resumo"], "fontes": n.get("fontes", [n["fonte"]]), "link": n["link"]} for n in items[:8]]
         for cat, items in by_cat.items() if items},
        ensure_ascii=False, indent=2
    )
    
    data_hoje = datetime.now().strftime("%d de %B de %Y")
    prompt = f"""Voce e um analista financeiro e jornalista especializado em mercados globais.
Hoje e {data_hoje}.

Abaixo estao noticias ja pre-agrupadas por assunto de multiplas fontes.

Crie um BRIEFING DIARIO completo em HTML para email.

REGRAS:
1. Cada assunto aparece UMA SO VEZ
2. Para cada noticia, escreva UM paragrafo de 3-5 linhas combinando informacoes complementares de cada fonte
3. Cite todas as fontes ao final: [Bloomberg, WSJ, InfoMoney]
4. Destaque implicacoes para investidores brasileiros
5. Adicione secao Conexoes Macro ao final

FORMATO HTML para email (tabelas, sem CSS externo):
- Fundo #ffffff, titulos #1a1a2e, texto #333333

Noticias:
{noticias_json}

Retorne APENAS o HTML do corpo (sem DOCTYPE, html, head ou body).
"""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def enviar_email(html_content, num_noticias):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Enviando email...")
    data_str = datetime.now().strftime("%d/%m/%Y")
    smtp_senha = GMAIL_SMTP_SENHA.strip().strip('"').strip("'")
    
    html_completo = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Georgia,serif;">
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f4f4f4">
<tr><td align="center" style="padding:20px 10px;">
<table width="660" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;">
<tr><td style="background:#1a1a2e;padding:28px 32px;">
  <div style="font-size:11px;color:#7a8bb0;letter-spacing:3px;text-transform:uppercase;margin-bottom:4px;">Briefing Diario</div>
  <div style="font-size:24px;font-weight:bold;color:#ffffff;">Resumo de Mercados & Noticias</div>
  <div style="font-size:13px;color:#8892b0;margin-top:6px;">{data_str} - {num_noticias} topicos analisados</div>
</td></tr>
<tr><td style="padding:28px 32px;">{html_content}</td></tr>
<tr><td style="background:#f8f9fa;border-top:1px solid #e9ecef;padding:16px 32px;">
  <div style="font-size:11px;color:#999999;">
    Gerado em {datetime.now().strftime("%d/%m/%Y as %H:%M")} BRT<br>
    Fontes: UOL, Estadao, Folha, WSJ, Bloomberg, Investing.com, InfoMoney
  </div>
</td></tr>
</table></td></tr></table>
</body></html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Briefing Diario - {datetime.now().strftime('%d/%m/%Y')}"
    msg["From"]    = EMAIL_REMETENTE
    msg["To"]      = EMAIL_DESTINO
    msg.attach(MIMEText(html_completo, "html", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()\n        server.login(EMAIL_REMETENTE, smtp_senha)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())

    print(f"  -> Email enviado para {EMAIL_DESTINO}")

def main():
    print("=" * 60)
    print(f"  BRIEFING DIARIO - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    try:
        noticias_raw = buscar_noticias()
        if not noticias_raw:
            print("[AVISO] Nenhuma noticia nova encontrada.")
            return
        noticias = deduplicar(noticias_raw)
        print(f"  -> {len(noticias)} topicos unicos apos deduplicacao")
        html_resumo = gerar_resumo_claude(noticias)
        enviar_email(html_resumo, len(noticias))
        print("\n Briefing enviado com sucesso!")
    except Exception as e:
        print(f"\n ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()