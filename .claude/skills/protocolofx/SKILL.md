---
name: protocolofx
description: Use este skill para o briefing FX-only, mais profundo que o fluxo geral — foco exclusivo em câmbio (USD/BRL, EUR/BRL, EUR/USD, JPY/BRL, USD/JPY, DXY), diferencial de juros, Treasury de 10 anos e risco de intervenção BoJ/MOF. Acione quando o usuário pedir especificamente análise de câmbio/FX, mesmo em dia parado sem notícia relevante.
---

# ProtocoloFX — fluxo FX-only

Este skill conduz o briefing diário focado exclusivamente em câmbio, mais profundo que o fluxo Geral (skill `protocolo`). Siga sempre as regras do CLAUDE.md da raiz (navegador para cotações, live-blogs para notícias, regra de nunca inventar dado, dois blocos de saída).

## Cotações obrigatórias
- **USD/BRL**: bullet obrigatório todo dia, mesmo em dia parado sem notícia relevante. Nunca omitir.
- **EUR/BRL** e **EUR/USD**.
- **JPY/BRL** e **USD/JPY** — sempre mencionar o risco de intervenção do BoJ/MOF (Ministério das Finanças do Japão) quando o iene estiver em nível sensível.
- **DXY** (índice do dólar).

Todas as cotações via navegador (Playwright/Chromium headless), lendo o valor renderizado. JPY/BRL sempre por 1 unidade de iene, 4 casas decimais, conforme CLAUDE.md.

## Diferencial de juros e Treasury
- Diferencial de juros entre EUA, Zona do Euro, Japão e Brasil, quando houver dado confirmado.
- Yield da Treasury de 10 anos — nível e variação do dia, como referência para o fluxo de capital e o DXY.

## Falas de dirigentes de banco central
- Fed, BCE, BoJ, BC brasileiro — reportar apenas falas confirmadas, com horário exato. Nunca parafrasear ou inferir declaração não confirmada.

## Níveis técnicos
- Reportar apenas níveis técnicos (suporte, resistência, médias) explicitamente citados pelas fontes consultadas. Nunca inventar nível técnico.

## Interpretação
Para cada dado, explicar o canal de transmissão (juros, fluxo, prêmio de risco) e o efeito de segunda ordem sobre o câmbio brasileiro, como definido no papel do CLAUDE.md.

## Saída
Sempre nos dois blocos definidos no CLAUDE.md: Morning Call (Bloco 1) e texto para WhatsApp em bloco de código (Bloco 2). Este fluxo é independente do fluxo Geral (skill `protocolo`) — nunca aciona ou depende dele.
