---
name: protocolo
description: Resumo diário de mercado (geral) com Morning Call e bloco pronto para WhatsApp
---

# Protocolo — Resumo de mercado (geral)

## Passo 0 — Hora
Rode `TZ=America/Sao_Paulo date`. Todo dado leva o horário a que se refere. Dado de horas atrás é rotulado como tal, nunca apresentado como "agora".

## Passo 1 — Cotações (via navegador, obrigatório)
Playwright com Chromium headless. Abra a página, espere o JavaScript renderizar, leia o valor NA TELA. Nunca use WebFetch para cotação — devolve HTML pré-JS cacheado.

Colete: USD/BRL, EUR/BRL, JPY/BRL, USD/JPY.
- USD/BRL, EUR/BRL: 4 casas decimais
- JPY/BRL: por 1 unidade de iene, NUNCA por lote de 100, 4 casas decimais
- USD/JPY: 2 casas decimais

Anote o timestamp de cada página. Se o navegador falhar, reporte o erro exato e marque como não confirmada. Nunca preencha com estimativa silenciosa.

## Passo 2 — Notícias (live-blogs primeiro)
Abra COM O NAVEGADOR as páginas de tempo real, que atualizam durante o pregão:
- infomoney.com.br/mercados/ibovespa-hoje-bolsa-de-valores-ao-vivo-DDMMAAAA
- infomoney.com.br/mercados/dolar-hoje-abertura-fechamento-comercial-turismo-DDMMAAAA
- moneytimes.com.br (matéria "tempo real" do dia)

Busca indexada é fallback, não fonte primária. Sempre confirme se o texto descreve o pregão de HOJE — matéria com título "hoje" frequentemente recicla números de ontem. Complemente com Reuters, Valor, Bloomberg Línea, CNBC para contexto internacional.

## Passo 3 — Bloco 1: Morning Call
Escreva como analista sênior de mercado. Não liste notícia solta: explique o mecanismo de transmissão. Para cada fato relevante, quando houver base factual:
- qual ativo é atingido primeiro e por qual canal (juros, câmbio, commodity, fluxo, prêmio de risco)
- qual o efeito de segunda ordem sobre o Brasil (Ibovespa, curva de juros, real)
- se o movimento é técnico ou fundamental; quando analistas citados na fonte disserem que é técnico, diga

Cubra: bolsas (EUA, Europa, Ásia, Ibovespa), juros e política monetária (Fed, BCE, BoJ, Copom), câmbio, commodities que estejam movendo mercado.

Regra inviolável: nunca invente cotação, nível técnico, fala de dirigente ou número para sustentar a leitura. Sem confirmação, diga que não confirmou.

## Passo 4 — Bloco 2: WhatsApp
Dentro de um bloco de código, para o botão de copiar funcionar. Sem markdown de blog (nada de ** ou #). Só formatação nativa do WhatsApp: *negrito*, _itálico_.
Compacto mas denso: cada linha carrega um fato com número, nunca frase vaga. Cotações sempre no FINAL, nesta ordem exata.

Modelo:

📊 Resumo mercado — DD/MM, HHhMM

🇧🇷 Ibovespa: [nível, variação, driver em poucas palavras]
🇺🇸 [Wall Street ou dado macro americano do dia]
🌏 [Ásia/Europa ou geopolítica, se relevante]
📈 [juros/Treasury/banco central]
🛢️ [commodity, se estiver movendo mercado]
[1 a 2 linhas extras só se houver fato com número que mereça]

💱 Cotações (HHhMM)
USD/BRL R$ X,XXXX
EUR/BRL R$ X,XXXX
JPY/BRL R$ 0,0XXX
USD/JPY XXX,XX

_Leitura: [uma frase — o que vigiar hoje, não resumo do que já foi dito]_

Cotação não confirmada entra como "não confirmada", nunca como número sem fonte.

## Saída
Só texto na tela. Nunca gere arquivo.
