---
name: protocolo
description: Resumo diário de mercado (geral) com Morning Call e bloco pronto para WhatsApp
---

# Protocolo — Resumo de mercado (geral)

## Passo 0 — Hora
Rode `TZ=America/Sao_Paulo date`. Todo dado leva o horário a que se refere. Dado de horas atrás é rotulado como tal, nunca apresentado como "agora".

## Passo 1 — Cotações (procedimento obrigatório, nesta ordem)
Cotações sempre em tempo real — nunca reaproveite valor de execução anterior desta mesma sessão ou de qualquer conversa passada.

1. Busque a matéria de notícia do dia (ex.: "dólar hoje DD/MM/AAAA" — o InfoMoney publica uma por dia, HTML estático, confiável) e extraia a cotação do texto. Confira sempre se a matéria é do pregão de HOJE — frases como "à espera da ata do Fed [de uma reunião já ocorrida]" denunciam matéria reciclada de dias atrás.
2. Se essa checagem falhar ou o texto não trouxer número confiável, leia a cotação renderizada via Playwright/Chromium (JavaScript renderizado, valor NA TELA). Use isso como segundo recurso, não primeiro: a maioria das fontes com cotação dinâmica (Google Finance, br.investing.com/currencies/*, XE, conversor do InfoMoney) devolve valor cacheado mesmo parecendo ao vivo, e APIs de câmbio (BCB, AwesomeAPI, Yahoo, Stooq, MarketWatch, CNBC) tendem a bloquear por robots.txt/403.
3. Se nenhuma das duas funcionar, sinalize claramente a ausência de confirmação no output. Nunca arrisque um número não confirmado.

Colete: USD/BRL, EUR/BRL, JPY/BRL, USD/JPY.
- USD/BRL, EUR/BRL: 4 casas decimais
- JPY/BRL: por 1 unidade de iene, NUNCA por lote de 100, 4 casas decimais (se a fonte só der por lote de 100, divida por 100)
- USD/JPY: 2 casas decimais

Se EUR/BRL ou JPY/BRL não tiverem fonte direta confiável, calcule por cruzamento: EUR/BRL = USD/BRL × EUR/USD; JPY/BRL = USD/BRL ÷ USD/JPY. Sinalize explicitamente se alguma perna do cruzamento vier de fonte não confiável.

Anote o timestamp de cada fonte usada. Falha em confirmar vira erro reportado e cotação marcada como não confirmada, nunca estimativa silenciosa.

## Passo 2 — Notícias
Fontes primárias: InfoMoney, Investing.com (br.investing.com), UOL Economia, Bloomberg/Bloomberg Línea, Forbes Brasil. Investing.com é a fonte primária definida para números/cotações; as demais primárias servem para contexto.
Complementares (quando as primárias não bastarem): Reuters, Valor Econômico, Estadão Economia, CNN Money, MarketWatch, CNBC.
Bloomberg trava fetch direto por robots.txt — use-o só via busca/snippet, nunca dependa dele para número de cotação.

Dentro do InfoMoney, priorize os live-blogs, que atualizam durante o pregão:
- infomoney.com.br/mercados/ibovespa-hoje-bolsa-de-valores-ao-vivo-DDMMAAAA
- infomoney.com.br/mercados/dolar-hoje-abertura-fechamento-comercial-turismo-DDMMAAAA
Confirme sempre se o texto descreve o pregão de HOJE — matéria com título "hoje" frequentemente recicla números de ontem.

## Passo 3 — Bloco 1: Morning Call
Escreva como analista sênior de mercado. Não liste notícia solta: explique o mecanismo de transmissão. Para cada fato relevante, com base factual:
- qual ativo é atingido primeiro e por qual canal (juros, câmbio, commodity, fluxo, prêmio de risco)
- qual o efeito de segunda ordem sobre o Brasil (Ibovespa, curva de juros, real)
- se o movimento é técnico ou fundamental; quando analistas citados na fonte disserem que é técnico, diga
Cubra: bolsas (EUA, Europa, Ásia, Ibovespa), juros e política monetária (Fed, BCE, BoJ, Copom), câmbio, commodities que movam mercado.
Regra inviolável: nunca invente cotação, nível técnico, fala de dirigente ou número. Sem confirmação, diga que não confirmou.

## Passo 4 — Bloco 2: WhatsApp
Dentro de bloco de código, para o botão de copiar funcionar. Sem markdown de blog. Só *negrito* e _itálico_. Compacto mas denso: cada linha carrega um fato com número. Cotações sempre no FINAL, nesta ordem.

Modelo:

📊 Resumo mercado — DD/MM, HHhMM

🇧🇷 Ibovespa: [nível, variação, driver]
🇺🇸 [Wall Street ou macro americano]
🌏 [Ásia/Europa ou geopolítica]
📈 [juros/Treasury/banco central]
🛢️ [commodity, se relevante]

💱 Cotações (HHhMM)
USD/BRL R$ X,XXXX
EUR/BRL R$ X,XXXX
JPY/BRL R$ 0,0XXX
USD/JPY XXX,XX

_Leitura: [uma frase — o que vigiar hoje]_

Cotação não confirmada entra como "não confirmada", nunca número sem fonte.

## Saída
Só texto na tela. Nunca gere arquivo.
