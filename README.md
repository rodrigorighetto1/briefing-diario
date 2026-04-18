# 📊 Briefing Diário de Notícias

Envia automaticamente um resumo de notícias por Gmail todos os dias no horário configurado.

## Fontes cobertas
- **UOL** — Notícias gerais e economia do Brasil  
- **Estadão** — Economia e política  
- **Folha de S.Paulo** — Dinheiro e Brasil  
- **WSJ** — Mercados e notícias mundiais  
- **Bloomberg** — Mercados e economia global  
- **Investing.com BR** — Mercados e criptomoedas  
- **InfoMoney** — Mercados, Brasil e cripto  

## Categorias analisadas
🔴 Guerras & Geopolítica | 🔵 Política | 🟡 Economia Global | 🟢 Brasil | 🟣 Criptomoedas | ⚫ Mercados & Bolsa

---

## Instalação rápida

### Opção 1 — Script automático (Windows)
```
Clique duas vezes em: setup_e_agendamento.bat
```
*(Execute como Administrador para criar a tarefa agendada)*

### Opção 2 — Manual

**1. Instalar dependências:**
```bash
pip install feedparser anthropic google-auth google-auth-oauthlib \
    google-auth-httplib2 google-api-python-client python-dotenv requests
```

**2. Configurar variáveis:**
```
Renomeie .env para .env e preencha:
- ANTHROPIC_API_KEY  → obtenha em console.anthropic.com
- EMAIL_DESTINO      → seu email de destino
- EMAIL_REMETENTE    → seu Gmail autenticado
```

**3. Configurar Gmail OAuth:**
- Acesse https://console.cloud.google.com/
- Crie um projeto → Ative Gmail API
- Crie credenciais OAuth 2.0 (tipo: Desktop)
- Baixe o JSON → renomeie para `credentials_gmail.json`
- Coloque na mesma pasta que `briefing_diario.py`

**4. Primeira autenticação:**
```bash
python briefing_diario.py
```
*(Na primeira execução, abrirá o navegador para autorizar o Gmail)*

**5. Agendar no Windows:**
```cmd
schtasks /create /tn "BriefingDiario" /tr "python C:\caminho\briefing_diario.py" /sc DAILY /st 07:00
```

---

## Arquivos do projeto

```
📁 daily_briefing/
├── briefing_diario.py          ← Script principal
├── setup_e_agendamento.bat     ← Instalador Windows
├── .env                        ← Suas chaves (NÃO compartilhe!)
├── credentials_gmail.json      ← Credenciais OAuth Google
├── token_gmail.json            ← Token gerado automaticamente
├── noticias_cache.json         ← Cache para evitar duplicatas
└── briefing_YYYYMMDD_HHMM.html ← Backups dos emails enviados
```

---

## Como funciona

```
1. RSS Feeds → 2. Deduplicação → 3. Claude API → 4. Gmail
   7 fontes       Agrupa por         Gera análise    Envia email
   ~100 itens     similaridade       profissional    formatado
                  ~25-40 tópicos
```

## Verificar tarefa agendada

```cmd
schtasks /query /tn "BriefingDiarioNoticias"
```

## Remover agendamento

```cmd
schtasks /delete /tn "BriefingDiarioNoticias" /f
```

---

*Desenvolvido para automação pessoal. Mantenha suas chaves de API seguras.*
