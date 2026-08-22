---
name: protocolofx
description: Resumo diário aprofundado de câmbio (FX-only) com bloco pronto para WhatsApp
---

# Protocolo FX — Resumo de câmbio

Só câmbio. Não cubra bolsa, balanço ou notícia setorial, exceto quando o fato move diretamente uma moeda.

## Passo 0 — Hora
Rode `TZ=America/Sao_Paulo date`. Todo dado leva o horário a que se refere.

## Passo 1 — Cotações (via navegador, obrigatório)
Playwright com Chromium headless, lendo o valor renderizado na tela. Nunca WebFetch para cotação.
Colete: USD/BRL, EUR/BRL, EUR/USD, JPY/BRL, USD/JPY, DXY.
- USD/BRL, EUR/BRL, EUR/USD: 4 casas decimais
- JPY/BRL: por 1 unidade de iene, NUNCA por lote de 100, 4 casas decimais
- USD/JPY, DXY: 2 casas decimais
Falha do navegador vira erro reportado, não estimativa.

## Passo 2 — Notícias e dados de câmbio
Priorize, com o navegador, páginas que atualizam ao vivo. Colete:
- fluxo cambial e movimento do dia no real
- diferencial de juros: Selic vs Fed funds; yield do Treasury de 10 anos
- falas de dirigentes de banco central (Fed, BCE, BoJ, BCB) no dia
- risco de intervenção do BoJ/MOF: nível atual vs faixa tratada como gatilho
- níveis técnicos CITADOS pelas fontes (nunca invente nível)
Fontes: InfoMoney, Investing.com, Money Times, Reuters, Bloomberg Línea, FXStreet, Valor.

## Passo 3 — Bloco 1: leitura de analista sênior de FX
USD/BRL é bullet obrigatório TODO dia, mesmo parado — se não houve movimento relevante, diga isso.
Cubra, cada um com o mecanismo por trás:
- USD/BRL: driver do dia, fluxo, componente doméstico (fiscal, eleitoral) vs externo
- EUR/BRL e EUR/USD: o que move o euro e quanto chega no cruzamento com o real
- JPY/BRL e USD/JPY: carry trade, política do BoJ, distância do nível de intervenção
- DXY: direção do dólar global e se o real segue ou descola
- Diferencial de juros: Selic vs Fed, Treasury 10 anos, efeito no carry
Separe sempre movimento global do dólar de risco Brasil. Nunca invente número, nível ou fala.

## Passo 4 — Bloco 2: WhatsApp
Mesmas regras: bloco de código, sem markdown de blog, só *negrito* e _itálico_, compacto e denso, cotações no final.

Modelo:

💱 Resumo FX — DD/MM, HHhMM

💵 USD/BRL: [movimento e driver]
🌎 [dólar global: DXY e direção]
💶 [euro: driver do dia]
💴 [iene: BoJ, carry, risco de intervenção]
🏦 [diferencial de juros / Treasury 10a]
🗣️ [fala de banco central, se houve]
📐 [níveis técnicos citados pelas fontes]

💱 Cotações (HHhMM)
USD/BRL R$ X,XXXX
EUR/BRL R$ X,XXXX
JPY/BRL R$ 0,0XXX
USD/JPY XXX,XX
EUR/USD X,XXXX
DXY XX,XX

_Leitura: [uma frase — o risco ou gatilho a vigiar]_

## Saída
Só texto na tela. Nunca gere arquivo.
