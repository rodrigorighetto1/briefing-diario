---
name: protocolo
description: Use este skill para o briefing diário GERAL de mercado — cobre bolsas mundiais (EUA, Europa, Ásia, Ibovespa), juros e política monetária (Fed, BCE, BoJ, Copom) e câmbio. Acione quando o usuário pedir o "morning call", "briefing de mercado" ou um panorama amplo do pregão, sem foco exclusivo em câmbio.
---

# Protocolo — fluxo Geral

Este skill conduz o briefing diário amplo de mercado, cobrindo os quatro blocos abaixo. Siga sempre as regras do CLAUDE.md da raiz (navegador para cotações, live-blogs para notícias, regra de nunca inventar dado, dois blocos de saída).

## 1. Bolsas mundiais
- EUA: futuros e/ou fechamento de S&P 500, Nasdaq, Dow Jones.
- Europa: principais índices (Stoxx 600, DAX, FTSE, CAC) e o tom do pregão europeu.
- Ásia: Nikkei, Hang Seng, CSI 300/Xangai — como fecharam, sinalizando o tom para o dia.
- Ibovespa: nível atual, variação do dia, principais movimentações setoriais.

## 2. Juros e política monetária
- Fed: postura atual, próximas decisões, falas recentes de dirigentes (somente se confirmadas).
- BCE: postura e decisões relevantes para o fluxo europeu.
- BoJ: política monetária japonesa e seu efeito sobre o iene e o carry trade.
- Copom: postura do BC brasileiro, expectativas de Selic, comunicados oficiais.

## 3. Câmbio
- USD/BRL, EUR/BRL, JPY/BRL — sempre via navegador, conforme regra do CLAUDE.md.
- Leitura do câmbio como canal de transmissão das notícias acima (ex.: fala do Fed → DXY → USD/BRL).

## 4. Interpretação e mecanismo de transmissão
Para cada bloco, não pare na descrição do fato: explique o canal de transmissão (juros, câmbio, commodity, fluxo, prêmio de risco) e o efeito de segunda ordem sobre o Brasil, como definido no papel do CLAUDE.md.

## Saída
Sempre nos dois blocos definidos no CLAUDE.md: Morning Call (Bloco 1) e texto para WhatsApp em bloco de código (Bloco 2). Este fluxo é independente do fluxo FX (skill `protocolofx`) — nunca aciona ou depende dele.
