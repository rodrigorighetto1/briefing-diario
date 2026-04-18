@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║         INSTALAÇÃO — Briefing Diário de Notícias         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado! Instale em https://python.org
    pause
    exit /b 1
)
echo [OK] Python encontrado

:: Instala dependências
echo.
echo Instalando dependências Python...
pip install feedparser anthropic google-auth google-auth-oauthlib ^
    google-auth-httplib2 google-api-python-client python-dotenv requests

echo.
echo ══════════════════════════════════════════════════════════
echo  CONFIGURAÇÃO DO GMAIL (OAuth 2.0)
echo ══════════════════════════════════════════════════════════
echo.
echo  Passos necessários:
echo  1. Acesse: https://console.cloud.google.com/
echo  2. Crie um novo projeto (ex: "Briefing Diario")
echo  3. Ative a API: APIs e Serviços → Biblioteca → "Gmail API"
echo  4. Crie credenciais: APIs e Serviços → Credenciais
echo     → Criar credenciais → ID do cliente OAuth 2.0
echo     → Tipo: Aplicativo para computador
echo  5. Baixe o JSON e salve como "credentials_gmail.json"
echo     na mesma pasta deste script
echo  6. Execute o script uma vez para autenticar:
echo     python briefing_diario.py
echo     (abrirá o navegador para autorizar o Gmail)
echo.
echo ══════════════════════════════════════════════════════════
echo  EDITANDO O .env
echo ══════════════════════════════════════════════════════════
echo.
echo  Abra o arquivo .env e preencha:
echo  - ANTHROPIC_API_KEY=sua_chave_aqui
echo  - EMAIL_DESTINO=seu.email@gmail.com
echo  - EMAIL_REMETENTE=seu.email@gmail.com
echo.

:: Pergunta o horário para agendamento
set /p HORA="Digite o horário de envio (ex: 07:00): "

:: Cria a tarefa no Windows Task Scheduler
set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%briefing_diario.py
set PYTHON_PATH=python

echo.
echo Criando tarefa agendada para %HORA% todos os dias...

schtasks /create ^
    /tn "BriefingDiarioNoticias" ^
    /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" ^
    /sc DAILY ^
    /st %HORA% ^
    /ru "%USERNAME%" ^
    /f

if errorlevel 1 (
    echo [AVISO] Erro ao criar tarefa. Tente como Administrador.
) else (
    echo [OK] Tarefa "BriefingDiarioNoticias" criada com sucesso!
    echo      Execução diária às %HORA%
)

echo.
echo ══════════════════════════════════════════════════════════
echo  VERIFICAR AGENDAMENTO
echo ══════════════════════════════════════════════════════════
echo.
echo  Para ver as tarefas agendadas:
echo    schtasks /query /tn "BriefingDiarioNoticias"
echo.
echo  Para executar agora (teste):
echo    python briefing_diario.py
echo.
echo  Para remover o agendamento:
echo    schtasks /delete /tn "BriefingDiarioNoticias" /f
echo.
echo ✅ Instalação concluída!
echo.
pause
