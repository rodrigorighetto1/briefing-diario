---
name: protocolofx
description: Resumo diário aprofundado de câmbio (FX-only) com bloco pronto para WhatsApp
---

# Protocolo FX — Resumo de câmbio

Só câmbio. Não cubra bolsa, balanço ou notícia setorial, exceto quando o fato move diretamente uma moeda.

## Passo 0 — Hora
Rode `TZ=America/Sao_Paulo date`. Todo dado leva o horário a que se refere.

## Passo 1 — Cotações (procedimento obrigatório, nesta ordem)
Cotações sempre em tempo real — nunca reaproveite valor de execução anterior desta mesma sessão ou de qualquer conversa passada.

1. Busque a matéria de notícia do dia (ex.: "dólar hoje DD/MM/AAAA" — o InfoMoney publica uma por dia, HTML estático, confiável) e extraia a cotação do texto. Confira sempre se a matéria é do pregão de HOJE — frases como "à espera da ata do Fed [de uma reunião já ocorrida]" denunciam matéria reciclada de dias atrás.
2. Se essa checagem falhar ou o texto não trouxer número confiável, leia a cotação renderizada via Playwright/Chromium (JavaScript renderizado, valor NA TELA). Use isso como segundo recurso, não primeiro: a maioria das fontes com cotação dinâmica (Google Finance, br.investing.com/currencies/*, XE, conversor do InfoMoney) devolve valor cacheado mesmo parecendo ao vivo, e APIs de câmbio (BCB, AwesomeAPI, Yahoo, Stooq, MarketWatch, CNBC) tendem a bloquear por robots.txt/403.
3. Se nenhuma das duas funcionar, sinalize claramente a ausência de confirmação no output. Nunca arrisque um número não confirmado.

Colete: USD/BRL, EUR/BRL, EUR/USD, JPY/BRL, USD/JPY, DXY.
- USD/BRL, EUR/BRL, EUR/USD: 4 casas decimais
- JPY/BRL: por 1 unidade de iene, NUNCA por lote de 100, 4 casas decimais (se a fonte só der por lote de 100, divida por 100)
- USD/JPY, DXY: 2 casas decimais

Se EUR/BRL ou JPY/BRL não tiverem fonte direta confiável, calcule por cruzamento: EUR/BRL = USD/BRL × EUR/USD; JPY/BRL = USD/BRL ÷ USD/JPY. Sinalize explicitamente se alguma perna do cruzamento vier de fonte não confiável.

Anote o timestamp de **cada** cotação individualmente — não um horário único de "consulta geral". Se uma perna estiver mais desatualizada que as outras (ex.: USD/BRL de matéria de ontem enquanto DXY tem tick de minutos atrás), isso aparece explícito ao lado do número no output. Falha em confirmar vira erro reportado, não estimativa.

## Passo 1.5 — Agenda econômica relevante ao câmbio
Busque o calendário econômico do dia (Investing.com/calendário, InfoMoney) e liste os eventos ainda por vir que podem mover câmbio: decisões de banco central (Fed/BCE/BoJ/BCB), payroll, CPI/PPI, PMIs, discursos de dirigentes. Cada evento leva 4 campos próprios: **horário, evento, consenso, valor anterior**. Consenso fica "não disponível" se a fonte não fornecer — nunca estimado. Se citar pesquisa de economistas sobre decisão de BC, deixe claro que é proporção de entrevistados, não probabilidade implícita de mercado — são coisas diferentes, não conflate.

## Passo 2 — Notícias e dados de câmbio
Fontes primárias: InfoMoney, Investing.com, UOL Economia, Bloomberg/Bloomberg Línea, Forbes Brasil. Investing.com é a fonte primária definida para números/cotações; as demais primárias servem para contexto.
Complementares (quando as primárias não bastarem, e específicas de FX): Reuters, Valor Econômico, Estadão Economia, CNN Money, MarketWatch, CNBC, FXStreet, Money Times.
Bloomberg trava fetch direto por robots.txt — use-o só via busca/snippet, nunca dependa dele para número de cotação.

Priorize páginas que atualizam ao vivo. Colete:
- fluxo cambial e movimento do dia no real
- diferencial de juros: Selic vs Fed funds; yield do Treasury de 10 anos
- falas de dirigentes de banco central (Fed, BCE, BoJ, BCB) no dia
- risco de intervenção do BoJ/MOF: nível atual vs faixa tratada como gatilho
- níveis técnicos CITADOS pelas fontes (nunca invente nível)

## Passo 3 — Bloco 1: leitura de analista sênior de FX
Abra com 2 linhas fixas antes de qualquer conteúdo: (1) data/horário da execução em Brasília + "/protocolofx"; (2) banner de sincronismo — se as cotações coletadas estão todas numa janela próxima entre si, diga isso; se alguma perna está defasada em relação às outras, diga isso explicitamente aqui, não só na linha individual.

Depois do banner, um resumo executivo de 2-3 linhas ("o que importa agora em câmbio") — a síntese que orienta a leitura, sem repetir número, antes do corpo do texto.

USD/BRL é bullet obrigatório TODO dia, mesmo parado — se não houve movimento relevante, diga isso.
Cubra, cada um com o mecanismo por trás:
- USD/BRL: driver do dia, fluxo, componente doméstico (fiscal, eleitoral) vs externo
- EUR/BRL e EUR/USD: o que move o euro e quanto chega no cruzamento com o real
- JPY/BRL e USD/JPY: carry trade, política do BoJ, distância do nível de intervenção
- DXY: direção do dólar global e se o real segue ou descola
- Diferencial de juros: Selic vs Fed, Treasury 10 anos, efeito no carry
- Agenda (Passo 1.5): eventos ainda por vir no dia e o que o mercado deve reagir a eles, com base no que a fonte disse
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
📅 [próximos eventos da agenda relevantes ao câmbio, com horário]

💱 Cotações (cada uma com seu horário de fonte, HHhMM)
USD/BRL R$ X,XXXX (HHhMM)
EUR/BRL R$ X,XXXX (HHhMM)
JPY/BRL R$ 0,0XXX (HHhMM)
USD/JPY XXX,XX (HHhMM)
EUR/USD X,XXXX (HHhMM)
DXY XX,XX (HHhMM)

_Leitura: [uma frase — o risco ou gatilho a vigiar]_

## Saída
Só texto na tela. Nunca gere arquivo.
