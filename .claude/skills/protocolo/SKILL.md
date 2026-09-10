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

Anote o timestamp de **cada** cotação individualmente — não um horário único de "consulta geral". Se uma perna estiver mais desatualizada que as outras (ex.: USD/BRL só com matéria de ontem enquanto EUR/BRL tem tick de minutos atrás), isso aparece explícito ao lado do número no output, não escondido em rodapé. Falha em confirmar vira erro reportado e cotação marcada como não confirmada, nunca estimativa silenciosa.

**Cache da ferramenta de busca:** a ferramenta de leitura de página cacheia por ~15 min por URL. Se reconsultar a mesma URL nesta sessão e o timestamp vier idêntico, segundo a segundo, ao de uma leitura anterior, isso é cache, não mercado parado — force bypass (parâmetro variável na URL, ex: `?cb=<algo único>`) e refaça antes de confiar no número.

## Passo 1.5 — Commodities (bullet fixo)
Colete petróleo (Brent e WTI), minério de ferro e ouro — sempre, mesmo em dia parado, dado o peso de Petrobras e Vale no Ibovespa. Mesma disciplina de fonte do Passo 1: número extraído de matéria do dia ou tela ao vivo via Playwright, nunca estimado. Preços de commodities costumam fechar em horários diferentes entre si (minério de ferro fecha antes do petróleo, por exemplo) — sinalize quando os preços não estão sincronizados no mesmo horário em vez de apresentá-los como se fossem do mesmo instante.

## Passo 1.6 — Agenda econômica do dia
Busque o calendário econômico do dia (Investing.com/calendário, InfoMoney) e liste eventos com horário (Brasília) já conhecidos no momento da execução — decisões de banco central, divulgação de indicadores, discursos de dirigentes. Cada evento leva 4 campos próprios: **horário, evento, consenso, valor anterior**. Consenso fica "não disponível" se a fonte não fornecer — nunca estimado. Se citar pesquisa de economistas (ex.: Reuters) sobre decisão de BC, deixe claro que é proporção de entrevistados, não probabilidade implícita de mercado — são coisas diferentes, não conflate.

## Passo 2 — Notícias
Fontes primárias: InfoMoney, Investing.com (br.investing.com), UOL Economia, Bloomberg/Bloomberg Línea, Forbes Brasil. Investing.com é a fonte primária definida para números/cotações; as demais primárias servem para contexto.
Complementares (quando as primárias não bastarem): Reuters, Valor Econômico, Estadão Economia, CNN Money, MarketWatch, CNBC.
Bloomberg trava fetch direto por robots.txt — use-o só via busca/snippet, nunca dependa dele para número de cotação.

Dentro do InfoMoney, priorize os live-blogs, que atualizam durante o pregão:
- infomoney.com.br/mercados/ibovespa-hoje-bolsa-de-valores-ao-vivo-DDMMAAAA
- infomoney.com.br/mercados/dolar-hoje-abertura-fechamento-comercial-turismo-DDMMAAAA
Confirme sempre se o texto descreve o pregão de HOJE — matéria com título "hoje" frequentemente recicla números de ontem.

## Passo 3 — Bloco 1: Morning Call
Abra com 2 linhas fixas antes de qualquer conteúdo: (1) data/horário da execução em Brasília + "/protocolo"; (2) banner de sincronismo — se as cotações/dados coletados estão todos numa janela próxima entre si, diga isso; se algum dado está defasado em relação aos outros, diga isso explicitamente aqui, não só na linha individual.

Depois do banner, um resumo executivo de 2-3 linhas ("o que importa agora") — a síntese que orienta a leitura, sem repetir número, antes do corpo do texto.

Escreva como analista sênior de mercado. Não liste notícia solta: explique o mecanismo de transmissão. Para cada fato relevante, com base factual:
- qual ativo é atingido primeiro e por qual canal (juros, câmbio, commodity, fluxo, prêmio de risco)
- qual o efeito de segunda ordem sobre o Brasil (Ibovespa, curva de juros, real)
- se o movimento é técnico ou fundamental; quando analistas citados na fonte disserem que é técnico, diga
Cubra: bolsas (EUA, Europa, Ásia, Ibovespa), juros e política monetária (Fed, BCE, BoJ, Copom), câmbio, commodities (Passo 1.5) e agenda econômica do dia (Passo 1.6) — cite os eventos que ainda vão sair e o que o mercado deve reagir a eles, com base no que a fonte disse, não em palpite.
Regra inviolável: nunca invente cotação, nível técnico, fala de dirigente ou número. Sem confirmação, diga que não confirmou.

## Passo 4 — Bloco 2: WhatsApp
Dentro de bloco de código, para o botão de copiar funcionar. Sem markdown de blog. Só *negrito* e _itálico_. Compacto mas denso: cada linha carrega um fato com número. Cotações sempre no FINAL, nesta ordem.

Modelo:

📊 Resumo mercado — DD/MM, HHhMM

🇧🇷 Ibovespa: [nível, variação, driver]
🇺🇸 [Wall Street ou macro americano]
🌏 [Ásia/Europa ou geopolítica]
📈 [juros/Treasury/banco central]
🛢️ Brent US$ XX,XX | WTI US$ XX,XX | Minério US$ XX,XX/t | Ouro US$ X.XXX
📅 [próximos eventos da agenda relevantes ao dia, com horário]

💱 Cotações (cada uma com seu horário de fonte, HHhMM)
USD/BRL R$ X,XXXX (HHhMM)
EUR/BRL R$ X,XXXX (HHhMM)
JPY/BRL R$ 0,0XXX (HHhMM)
USD/JPY XXX,XX (HHhMM)

_Leitura: [uma frase — o que vigiar hoje]_

Cotação não confirmada entra como "não confirmada", nunca número sem fonte.

## Saída
Só texto na tela. Nunca gere arquivo.
