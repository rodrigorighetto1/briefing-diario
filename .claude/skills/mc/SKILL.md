---
name: mc
description: Resumo factual do fechamento do dia anterior (bolsas, juros, câmbio), sem leitura do dia atual
---

# MC — Resumo do dia anterior

Só o retrato do pregão anterior. Nunca inclua leitura de impacto sobre o dia atual — isso é escopo do /protocolo.

## Passo 0 — Hora
Rode `TZ=America/Sao_Paulo date`. Todo dado leva o horário/pregão a que se refere.

## Passo 1 — Cotações (procedimento obrigatório, nesta ordem)
Cotações do fechamento/nível mais recente do pregão anterior — nunca reaproveite valor de execução anterior desta mesma sessão ou de qualquer conversa passada.

1. Busque a matéria de notícia do dia (ex.: "dólar hoje DD/MM/AAAA" — o InfoMoney publica uma por dia, HTML estático, confiável) e extraia a cotação do texto. Confira sempre se a matéria é do pregão de HOJE — frases como "à espera da ata do Fed [de uma reunião já ocorrida]" denunciam matéria reciclada de dias atrás.
2. Se essa checagem falhar ou o texto não trouxer número confiável, leia a cotação renderizada via Playwright/Chromium (JavaScript renderizado, valor NA TELA). Use isso como segundo recurso, não primeiro: a maioria das fontes com cotação dinâmica (Google Finance, br.investing.com/currencies/*, XE, conversor do InfoMoney) devolve valor cacheado mesmo parecendo ao vivo, e APIs de câmbio (BCB, AwesomeAPI, Yahoo, Stooq, MarketWatch, CNBC) tendem a bloquear por robots.txt/403.
3. Se nenhuma das duas funcionar, sinalize claramente a ausência de confirmação no output. Nunca arrisque um número não confirmado.

Colete: USD/BRL, EUR/BRL, JPY/BRL, USD/JPY.
- USD/BRL, EUR/BRL: 4 casas decimais
- JPY/BRL: por 1 unidade de iene, NUNCA por lote de 100, 4 casas decimais (se a fonte só der por lote de 100, divida por 100)
- USD/JPY: 2 casas decimais

Se EUR/BRL ou JPY/BRL não tiverem fonte direta confiável, calcule por cruzamento: EUR/BRL = USD/BRL × EUR/USD; JPY/BRL = USD/BRL ÷ USD/JPY. Sinalize explicitamente se alguma perna do cruzamento vier de fonte não confiável.

## Passo 2 — Notícias
Fontes primárias: InfoMoney, Investing.com (br.investing.com), UOL Economia, Bloomberg/Bloomberg Línea, Forbes Brasil. Complementares (quando as primárias não bastarem): Reuters, Valor Econômico, Estadão Economia, CNN Money, MarketWatch, CNBC. Bloomberg trava fetch direto por robots.txt — use-o só via busca/snippet.

Busque as matérias que cobrem o fechamento do pregão anterior (bolsas, juros, câmbio). Confirme que a matéria descreve o pregão que você está resumindo, não uma reciclada de outro dia.

## Passo 3 — Bloco 1: resumo do fechamento anterior
Resumo denso e factual de como fecharam os principais mercados e quais foram as notícias mais relevantes do pregão anterior. **Sem interpretação, sem leitura de impacto sobre hoje** — é retrato do que já aconteceu, com números e fatos.

**"Dia anterior" não é um corte único de calendário — cada praça tem seu próprio último fechamento, e os fusos não se alinham:**
- **Wall Street (EUA):** fechamento do pregão anterior — já fechado há horas no horário de Brasília.
- **Europa:** idem, último fechamento já concluído.
- **Ásia (Nikkei, Hang Seng, CSI300/Xangai etc.):** dependendo do horário em que o comando for rodado, o pregão asiático do dia pode estar em andamento. Nesse caso, puxe o comportamento em tempo real (variação até agora, não um fechamento) e deixe explícito no texto que o pregão segue aberto — nunca trate como "fechamento" um pregão que ainda não fechou.
- **Ibovespa:** normalmente o fechamento do dia anterior, salvo se o comando for rodado durante o próprio pregão.

Cubra: bolsas (EUA, Europa, Ásia, Ibovespa), juros e política monetária (Fed, BCE, BoJ, Copom), câmbio. Regra inviolável: nunca invente cotação, nível técnico, fala de dirigente ou número. Sem confirmação, diga que não confirmou.

## Passo 4 — Bloco 2: WhatsApp
Dentro de bloco de código, para o botão de copiar funcionar. Sem markdown de blog. Só *negrito* e _itálico_. Compacto mas denso: cada linha carrega um fato com número, sem leitura de impacto sobre hoje. Cotações sempre no FINAL.

Modelo:

📊 Fechamento anterior — DD/MM

🇧🇷 Ibovespa: [nível, variação, driver do pregão]
🇺🇸 [Wall Street: fechamento e driver]
🌏 [Ásia/Europa: fechamento ou, se ainda aberto, variação até agora — sinalizando isso]
📈 [juros/Treasury/banco central: fato do pregão]

💱 Cotações (fechamento/nível mais recente)
USD/BRL R$ X,XXXX
EUR/BRL R$ X,XXXX
JPY/BRL R$ 0,0XXX
USD/JPY XXX,XX

Cotação não confirmada entra como "não confirmada", nunca número sem fonte.

## Saída
Só texto na tela. Nunca gere arquivo.
