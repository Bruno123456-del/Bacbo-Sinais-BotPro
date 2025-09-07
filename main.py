M
My Workspace


b
Bacbo-Sinais-BotPro
Menu
Background Worker
Bacbo-Sinais-BotPro
Python 3
Starter

Connect

Manual Deploy
Service ID:
srv-d1vu2n6uk2gs73eqj0m0

Bruno123456-del / Bacbo-Sinais-BotPro
main
September 7, 2025 at 9:09 AM
live
351ddf4
Update main.py

All logs
Search
Search

Live tail
GMT-3

Menu

==> Cloning from https://github.com/Bruno123456-del/Bacbo-Sinais-BotPro
==> Checking out commit 351ddf4d6817aa3e49f10541816633ae1ca0cdef in branch main
==> Downloading cache...
==> Transferred 77MB in 7s. Extraction took 2s.
==> Using Python version 3.13.4 (default)
==> Docs on specifying a Python version: https://render.com/docs/python-version
==> Using Poetry version 2.1.3 (default)
==> Docs on specifying a Poetry version: https://render.com/docs/poetry-version
==> Running build command 'pip install -r requirements.txt'...
Collecting python-dotenv (from -r requirements.txt (line 1))
  Using cached python_dotenv-1.1.1-py3-none-any.whl.metadata (24 kB)
Collecting Flask (from -r requirements.txt (line 3))
  Using cached flask-3.1.2-py3-none-any.whl.metadata (3.2 kB)
Collecting Flask-Cors (from -r requirements.txt (line 4))
  Using cached flask_cors-6.0.1-py3-none-any.whl.metadata (5.3 kB)
Collecting Pillow (from -r requirements.txt (line 5))
  Using cached pillow-11.3.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (9.0 kB)
Collecting python-telegram-bot[job-queue] (from -r requirements.txt (line 2))
  Using cached python_telegram_bot-22.3-py3-none-any.whl.metadata (17 kB)
Collecting httpx<0.29,>=0.27 (from python-telegram-bot[job-queue]->-r requirements.txt (line 2))
  Using cached httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting apscheduler<3.12.0,>=3.10.4 (from python-telegram-bot[job-queue]->-r requirements.txt (line 2))
  Using cached APScheduler-3.11.0-py3-none-any.whl.metadata (6.4 kB)
Collecting tzlocal>=3.0 (from apscheduler<3.12.0,>=3.10.4->python-telegram-bot[job-queue]->-r requirements.txt (line 2))
  Using cached tzlocal-5.3.1-py3-none-any.whl.metadata (7.6 kB)
Collecting anyio (from httpx<0.29,>=0.27->python-telegram-bot[job-queue]->-r requirements.txt (line 2))
  Using cached anyio-4.10.0-py3-none-any.whl.metadata (4.0 kB)
Collecting certifi (from httpx<0.29,>=0.27->python-telegram-bot[job-queue]->-r requirements.txt (line 2))
  Using cached certifi-2025.8.3-py3-none-any.whl.metadata (2.4 kB)
Collecting httpcore==1.* (from httpx<0.29,>=0.27->python-telegram-bot[job-queue]->-r requirements.txt (line 2))
  Using cached httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting idna (from httpx<0.29,>=0.27->python-telegram-bot[job-queue]->-r requirements.txt (line 2))
  Using cached idna-3.10-py3-none-any.whl.metadata (10 kB)
Collecting h11>=0.16 (from httpcore==1.*->httpx<0.29,>=0.27->python-telegram-bot[job-queue]->-r requirements.txt (line 2))
  Using cached h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting blinker>=1.9.0 (from Flask->-r requirements.txt (line 3))
  Using cached blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
Collecting click>=8.1.3 (from Flask->-r requirements.txt (line 3))
  Using cached click-8.2.1-py3-none-any.whl.metadata (2.5 kB)
Collecting itsdangerous>=2.2.0 (from Flask->-r requirements.txt (line 3))
  Using cached itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Collecting jinja2>=3.1.2 (from Flask->-r requirements.txt (line 3))
  Using cached jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting markupsafe>=2.1.1 (from Flask->-r requirements.txt (line 3))
  Using cached MarkupSafe-3.0.2-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.0 kB)
Collecting werkzeug>=3.1.0 (from Flask->-r requirements.txt (line 3))
  Using cached werkzeug-3.1.3-py3-none-any.whl.metadata (3.7 kB)
Collecting sniffio>=1.1 (from anyio->httpx<0.29,>=0.27->python-telegram-bot[job-queue]->-r requirements.txt (line 2))
  Using cached sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)
Using cached python_dotenv-1.1.1-py3-none-any.whl (20 kB)
Using cached python_telegram_bot-22.3-py3-none-any.whl (717 kB)
Using cached APScheduler-3.11.0-py3-none-any.whl (64 kB)
Using cached httpx-0.28.1-py3-none-any.whl (73 kB)
Using cached httpcore-1.0.9-py3-none-any.whl (78 kB)
Using cached flask-3.1.2-py3-none-any.whl (103 kB)
Using cached flask_cors-6.0.1-py3-none-any.whl (13 kB)
Using cached pillow-11.3.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (6.6 MB)
Using cached blinker-1.9.0-py3-none-any.whl (8.5 kB)
Using cached click-8.2.1-py3-none-any.whl (102 kB)
Using cached h11-0.16.0-py3-none-any.whl (37 kB)
Using cached itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Using cached jinja2-3.1.6-py3-none-any.whl (134 kB)
Using cached MarkupSafe-3.0.2-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (23 kB)
Using cached tzlocal-5.3.1-py3-none-any.whl (18 kB)
Using cached werkzeug-3.1.3-py3-none-any.whl (224 kB)
Using cached anyio-4.10.0-py3-none-any.whl (107 kB)
Using cached idna-3.10-py3-none-any.whl (70 kB)
Using cached sniffio-1.3.1-py3-none-any.whl (10 kB)
Using cached certifi-2025.8.3-py3-none-any.whl (161 kB)
Installing collected packages: tzlocal, sniffio, python-dotenv, Pillow, markupsafe, itsdangerous, idna, h11, click, certifi, blinker, werkzeug, jinja2, httpcore, apscheduler, anyio, httpx, Flask, python-telegram-bot, Flask-Cors
Successfully installed Flask-3.1.2 Flask-Cors-6.0.1 Pillow-11.3.0 anyio-4.10.0 apscheduler-3.11.0 blinker-1.9.0 certifi-2025.8.3 click-8.2.1 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.10 itsdangerous-2.2.0 jinja2-3.1.6 markupsafe-3.0.2 python-dotenv-1.1.1 python-telegram-bot-22.3 sniffio-1.3.1 tzlocal-5.3.1 werkzeug-3.1.3
[notice] A new release of pip is available: 25.1.1 -> 25.2
[notice] To update, run: pip install --upgrade pip
==> Uploading build...
==> Uploaded in 4.2s. Compression took 1.1s
==> Build successful 🎉
==> Deploying...
==> Your service is live 🎉
==> Running 'python main.py'
  File "/opt/render/project/src/main.py", line 153
    ),rta_maluca": (
                ^
SyntaxError: unterminated string literal (detected at line 153)
==> Running 'python main.py'
  File "/opt/render/project/src/main.py", line 153
    ),rta_maluca": (
                ^
SyntaxError: unterminated string literal (detected at line 153)
==> Running 'python main.py'
  File "/opt/render/project/src/main.py", line 153
    ),rta_maluca": (
                ^
SyntaxError: unterminated string literal (detected at line 153)
==> Running 'python main.py'
  File "/opt/render/project/src/main.py", line 153
    ),rta_maluca": (
                ^
SyntaxError: unterminated string literal (detected at line 153)
==> Running 'python main.py'
  File "/opt/render/project/src/main.py", line 153
    ),rta_maluca": (
                ^
SyntaxError: unterminated string literal (detected at line 153)
Need better ways to work with logs? Try theRender CLI, Render MCP Server, or set up a log stream integration 

0 services selected:

Move

Generate Blueprint

Resume

Suspend

