# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS VIP/FREE - VERSÃO ESTRATÉGICA PROFISSIONAL
# PARTE 1: CONFIGURAÇÕES, IMPORTS E FUNCIONALIDADES BÁSICAS
# ===================================================================================

import logging
import os
import random
import asyncio
import json
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, JobQueue
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv

# ==========================================
# CARREGANDO VARIÁVEIS DE AMBIENTE
# ==========================================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID"))         # Canal Free
VIP_CANAL_ID = int(os.getenv("VIP_CANAL_ID")) # Canal VIP
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ==========================================
# CONFIGURAÇÃO DE LOGS
# ==========================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==========================================
# ESTRUTURAS DE DADOS E VARIÁVEIS GLOBAIS
# ==========================================
usuarios_vip = set()        # Guarda IDs VIP
usuarios_free = set()       # Guarda IDs Free
usuarios_dados = {}         # Dados completos dos usuários
estatisticas_bot = {
    "sinais_enviados": 0,
    "conversoes_vip": 0,
    "usuarios_ativos": 0,
    "taxa_conversao": 0.0
}

# ==========================================
# SISTEMA DE GESTÃO DE BANCA E GALES
# ==========================================
class GestorBanca:
    def __init__(self, banca_inicial=100.0):
        self.banca_inicial = banca_inicial
        self.banca_atual = banca_inicial
        self.historico_operacoes = []
        self.sequencia_gales = [4, 8, 16]  # Percentuais para gales
        
    def calcular_entrada(self, percentual=2.0):
        """Calcula valor da entrada baseado no percentual da banca"""
        return self.banca_atual * (percentual / 100)
    
    def executar_gale(self, nivel_gale=0):
        """Executa estratégia de gale com percentuais crescentes"""
        if nivel_gale >= len(self.sequencia_gales):
            return None
        percentual = self.sequencia_gales[nivel_gale]
        return self.calcular_entrada(percentual)
    
    def aplicar_juros_compostos(self, dias=30, taxa_diaria=0.02):
        """Simula crescimento com juros compostos"""
        valor_final = self.banca_inicial * ((1 + taxa_diaria) ** dias)
        return valor_final
    
    def registrar_operacao(self, tipo, valor, resultado):
        """Registra operação no histórico"""
        operacao = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "valor": valor,
            "resultado": resultado,
            "banca_pos": self.banca_atual
        }
        self.historico_operacoes.append(operacao)

# ==========================================
# MENSAGENS ESTRATÉGICAS PARA CONVERSÃO
# ==========================================
mensagens_free_limitadas = [
    "🎯 SINAL FREE LIMITADO\n💰 Entrada: 2% da banca\n⚡ Válido por 5 minutos\n\n🔥 QUER SINAIS ILIMITADOS? Entre no VIP e ganhe 90 DIAS GRÁTIS!",
    "📊 ANÁLISE IA DETECTOU OPORTUNIDADE\n💎 Confiança: 87%\n⏰ Janela: 3 minutos\n\n🚀 No VIP você tem sinais 24/7 + bônus de R$600!",
    "🎲 PADRÃO IDENTIFICADO\n💸 Potencial: Alto\n🎯 Precisão: 91%\n\n⭐ Upgrade para VIP e receba material trader avançado!"
]

mensagens_vip_exclusivas = [
    "👑 SINAL VIP EXCLUSIVO\n💰 Gestão de banca otimizada\n📈 Juros compostos ativos\n🎯 Entrada calculada: {valor}%\n\n🏆 Torneio VIP: Maldivas + Rolex + Lamborghini",
    "🔥 OPORTUNIDADE PREMIUM\n💎 Análise IA avançada\n📊 Probabilidade: 94%\n💰 Gale automático configurado\n\n🎁 Bônus ativo: Viagem Dubai para 2 pessoas",
    "⚡ SINAL FLASH VIP\n🎯 Entrada: {valor} (otimizada)\n📈 Projeção: +{ganho}% em 24h\n🏅 Ranking: Top 1%\n\n🎊 Próximo sorteio: MacBook Pro 16\""
]

ofertas_promocionais = {
    "oferta_especial": {
        "titulo": "🔥 OFERTA ESPECIAL",
        "descricao": "Faça seu primeiro depósito e ganhe acesso VIP GRATUITO!",
        "prazo": "Envie o print em até 12 horas!",
        "beneficios": [
            "🚀 Grupo VIP Pago Gratuito",
            "🤖 Sinais com análise de IA em tempo real", 
            "📅 Sinais organizados por horários",
            "🧠 Mentalidade e gestão de banca",
            "🎁 Sorteios exclusivos",
            "📚 Material trader avançado",
            "💰 Bônus de até R$600",
            "⚡ Sinais ilimitados em todos os jogos"
        ]
    },
    "torneio_vip": {
        "titulo": "🏆 Torneio VIP Exclusivo",
        "premios": [
            "✈️ Mala de dinheiro + viagem a Dubai para duas pessoas",
            "🚗 Lamborghini Urus",
            "⌚ Rolex Datejust 41", 
            "🎫 Ingressos para o BKFC Dubai",
            "💻 MacBook Pro 16\"",
            "📱 iPhone 16 Pro Max"
        ],
        "call_to_action": "🔥 Gostaria de ganhar o mesmo?\nToque no botão abaixo e entre para o clube privado\nO jogo pelos prêmios mais desejados começa aqui 🏆"
    },
    "codigo_promocional": {
        "codigo": "GESTAO",
        "beneficios": [
            "🎁 Bônus Extra",
            "⭐ Vantagens VIP", 
            "📱 Fácil de Usar"
        ],
        "instrucoes": "Cole o código durante o cadastro para ativar os benefícios"
    }
}

# ==========================================
# FUNÇÕES DE UTILIDADE E FORMATAÇÃO
# ==========================================
def formatar_valor_brasileiro(valor):
    """Formata valores em reais brasileiro"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_emoji_aleatorio():
    """Gera emoji aleatório para dar dinamismo"""
    emojis = ["🚀", "💎", "🔥", "⚡", "🎯", "💰", "🏆", "⭐", "🎊", "💸"]
    return random.choice(emojis)

def calcular_taxa_conversao():
    """Calcula taxa de conversão atual"""
    if len(usuarios_free) == 0:
        return 0.0
    return (len(usuarios_vip) / (len(usuarios_free) + len(usuarios_vip))) * 100

# ==========================================
# SISTEMA DE USUÁRIOS E DADOS
# ==========================================
def inicializar_usuario(user_id, username=None):
    """Inicializa dados do usuário"""
    if user_id not in usuarios_dados:
        usuarios_dados[user_id] = {
            "id": user_id,
            "username": username,
            "data_entrada": datetime.now(),
            "tipo": "free",
            "sinais_recebidos": 0,
            "interacoes": 0,
            "ultima_atividade": datetime.now(),
            "gestor_banca": GestorBanca(),
            "vip_expira": None
        }

def promover_para_vip(user_id, dias_vip=90):
    """Promove usuário para VIP com período definido"""
    if user_id in usuarios_dados:
        usuarios_dados[user_id]["tipo"] = "vip"
        usuarios_dados[user_id]["vip_expira"] = datetime.now() + timedelta(days=dias_vip)
        usuarios_vip.add(user_id)
        usuarios_free.discard(user_id)
        return True
    return False

def verificar_vip_expirado(user_id):
    """Verifica se VIP do usuário expirou"""
    if user_id in usuarios_dados and usuarios_dados[user_id]["vip_expira"]:
        if datetime.now() > usuarios_dados[user_id]["vip_expira"]:
            usuarios_dados[user_id]["tipo"] = "free"
            usuarios_dados[user_id]["vip_expira"] = None
            usuarios_vip.discard(user_id)
            usuarios_free.add(user_id)
            return True
    return False
# -*- coding: utf-8 -*-
# ===================================================================================
# BOT DE SINAIS VIP/FREE - VERSÃO ESTRATÉGICA PROFISSIONAL  
# PARTE 2: HANDLERS, AUTOMAÇÃO E EXECUÇÃO PRINCIPAL
# ===================================================================================

# ==========================================
# FUNÇÕES DE ENVIO DE MENSAGENS ESTRATÉGICAS
# ==========================================
async def enviar_sinal_free_limitado(context: ContextTypes.DEFAULT_TYPE):
    """Envia sinal free limitado com call-to-action forte para VIP"""
    bot = context.bot
    mensagem = random.choice(mensagens_free_limitadas)
    
    keyboard = [
        [InlineKeyboardButton("🔓 ENTRAR NO VIP AGORA", url="https://win-agegate-promo-68.lovable.app/")],
        [InlineKeyboardButton("🎁 USAR CUPOM GESTAO", callback_data="cupom_gestao")],
        [InlineKeyboardButton("🏆 VER TORNEIO VIP", callback_data="torneio_vip")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await bot.send_message(
            chat_id=CANAL_ID, 
            text=mensagem,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        estatisticas_bot["sinais_enviados"] += 1
        logger.info("Sinal FREE limitado enviado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao enviar sinal free: {e}")

async def enviar_sinal_vip_exclusivo(context: ContextTypes.DEFAULT_TYPE):
    """Envia sinal VIP com gestão de banca e ofertas exclusivas"""
    bot = context.bot
    
    # Simula cálculo de gestão de banca
    gestor = GestorBanca(1000.0)  # Banca exemplo
    valor_entrada = gestor.calcular_entrada(2.5)
    ganho_projetado = random.randint(15, 35)
    
    mensagem_base = random.choice(mensagens_vip_exclusivas)
    mensagem = mensagem_base.format(
        valor=f"{valor_entrada:.2f}",
        ganho=ganho_projetado
    )
    
    # Adiciona informações de gestão de banca
    info_banca = f"\n\n📊 GESTÃO DE BANCA ATIVA:\n"
    info_banca += f"💰 Entrada otimizada: {formatar_valor_brasileiro(valor_entrada)}\n"
    info_banca += f"📈 Projeção 30 dias: {formatar_valor_brasileiro(gestor.aplicar_juros_compostos())}\n"
    info_banca += f"⚡ Gales: 4% → 8% → 16% (automático)\n"
    
    mensagem_completa = mensagem + info_banca
    
    keyboard = [
        [InlineKeyboardButton("🎯 COPIAR SINAL", callback_data="copiar_sinal")],
        [InlineKeyboardButton("📊 GESTÃO DE BANCA", callback_data="gestao_banca")],
        [InlineKeyboardButton("🏆 RANKING VIP", callback_data="ranking_vip")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await bot.send_message(
            chat_id=VIP_CANAL_ID,
            text=mensagem_completa,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        logger.info("Sinal VIP exclusivo enviado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao enviar sinal VIP: {e}")

async def enviar_oferta_urgente(bot, user_id: int):
    """Envia oferta urgente personalizada para conversão"""
    oferta = ofertas_promocionais["oferta_especial"]
    
    mensagem = f"🔥 {oferta['titulo']}\n\n"
    mensagem += f"💎 {oferta['descricao']}\n"
    mensagem += f"⏰ {oferta['prazo']}\n\n"
    mensagem += "🎁 BENEFÍCIOS INCLUSOS:\n"
    
    for beneficio in oferta['beneficios']:
        mensagem += f"{beneficio}\n"
    
    mensagem += f"\n📸 Como Garantir seu Acesso VIP:\n"
    mensagem += f"• Faça seu depósito pelo link oficial\n"
    mensagem += f"• Envie o print do depósito + cupom em até 12 horas\n"
    mensagem += f"• Receba seu link de acesso VIP instantaneamente\n"
    
    keyboard = [
        [InlineKeyboardButton("🎁 ENVIAR PRINT NO GRUPO", url="https://t.me/seu_grupo_suporte")],
        [InlineKeyboardButton("💰 FAZER DEPÓSITO AGORA", url="https://win-agegate-promo-68.lovable.app/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await bot.send_message(
            chat_id=user_id,
            text=mensagem,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        logger.info(f"Oferta urgente enviada para usuário {user_id}")
    except Exception as e:
        logger.error(f"Erro ao enviar oferta urgente: {e}")

# ==========================================
# HANDLERS DE COMANDOS
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler do comando /start com onboarding estratégico"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    inicializar_usuario(user_id, username)
    usuarios_free.add(user_id)
    
    mensagem_boas_vindas = (
        f"👋 Bem-vindo ao sistema de sinais mais avançado do Brasil!\n\n"
        f"🎯 Você está no grupo FREE com sinais limitados\n"
        f"💡 Para desbloquear o potencial completo, veja as ofertas abaixo:\n\n"
        f"🔥 OFERTA ESPECIAL ATIVA:\n"
        f"• 90 dias VIP GRÁTIS no primeiro depósito\n"
        f"• Bônus de até R$600\n"
        f"• Material trader profissional\n"
        f"• Gestão de banca com juros compostos\n\n"
        f"⏰ Vagas limitadas! Garante já a sua!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔓 ENTRAR NO VIP", url="https://win-agegate-promo-68.lovable.app/")],
        [InlineKeyboardButton("🎁 CUPOM: GESTAO", callback_data="cupom_gestao")],
        [InlineKeyboardButton("🏆 VER PRÊMIOS VIP", callback_data="premios_vip")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        mensagem_boas_vindas,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def promover_vip_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando admin para promover usuário a VIP"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Acesso negado!")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Use: /vip <user_id>")
        return
    
    try:
        user_id = int(context.args[0])
        if promover_para_vip(user_id, 90):
            await update.message.reply_text(f"✅ Usuário {user_id} promovido a VIP por 90 dias!")
            estatisticas_bot["conversoes_vip"] += 1
        else:
            await update.message.reply_text(f"❌ Erro ao promover usuário {user_id}")
    except ValueError:
        await update.message.reply_text("❌ ID de usuário inválido!")

async def status_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra estatísticas detalhadas do bot"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    taxa_conversao = calcular_taxa_conversao()
    
    mensagem_status = (
        f"📊 ESTATÍSTICAS DO BOT\n\n"
        f"👥 Usuários Free: {len(usuarios_free)}\n"
        f"👑 Usuários VIP: {len(usuarios_vip)}\n"
        f"📈 Taxa de Conversão: {taxa_conversao:.1f}%\n"
        f"📡 Sinais Enviados: {estatisticas_bot['sinais_enviados']}\n"
        f"💰 Conversões VIP: {estatisticas_bot['conversoes_vip']}\n"
        f"🕐 Última atualização: {datetime.now().strftime('%H:%M:%S')}"
    )
    
    await update.message.reply_text(mensagem_status)

# ==========================================
# HANDLERS DE CALLBACK (BOTÕES)
# ==========================================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para botões inline"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "cupom_gestao":
        cupom_info = ofertas_promocionais["codigo_promocional"]
        mensagem = (
            f"🎁 CUPOM DE DESCONTO EXCLUSIVO\n\n"
            f"📋 Código: {cupom_info['codigo']}\n\n"
            f"✨ Benefícios:\n"
        )
        for beneficio in cupom_info['beneficios']:
            mensagem += f"{beneficio}\n"
        
        mensagem += f"\n{cupom_info['instrucoes']}"
        
        keyboard = [
            [InlineKeyboardButton("📋 COPIAR CÓDIGO", callback_data="copiar_codigo")],
            [InlineKeyboardButton("🎯 USAR CUPOM E CADASTRAR", url="https://win-agegate-promo-68.lovable.app/")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(mensagem, reply_markup=reply_markup)
    
    elif data == "torneio_vip" or data == "premios_vip":
        torneio = ofertas_promocionais["torneio_vip"]
        mensagem = f"🏆 {torneio['titulo']}\n\n"
        mensagem += "🎁 Prêmios Incríveis:\n"
        
        for premio in torneio['premios']:
            mensagem += f"{premio}\n"
        
        mensagem += f"\n{torneio['call_to_action']}"
        
        keyboard = [
            [InlineKeyboardButton("💎 ENTRAR NO CLUBE PRIVADO VIP", url="https://win-agegate-promo-68.lovable.app/")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(mensagem, reply_markup=reply_markup)

# ==========================================
# SISTEMA DE AUTOMAÇÃO E AGENDAMENTO
# ==========================================
async def autosinal_estrategico(context: ContextTypes.DEFAULT_TYPE):
    """Sistema de sinais automáticos com estratégia de conversão"""
    # Envia sinal free limitado
    await enviar_sinal_free_limitado(context)
    
    # Envia ofertas urgentes para usuários free selecionados
    usuarios_free_lista = list(usuarios_free)
    if usuarios_free_lista:
        # Seleciona até 3 usuários aleatórios para receber oferta urgente
        usuarios_selecionados = random.sample(
            usuarios_free_lista, 
            min(3, len(usuarios_free_lista))
        )
        
        bot = context.bot
        for user_id in usuarios_selecionados:
            await enviar_oferta_urgente(bot, user_id)
            await asyncio.sleep(2)  # Evita spam

async def autosinal_vip(context: ContextTypes.DEFAULT_TYPE):
    """Sinais automáticos exclusivos para VIP"""
    if usuarios_vip:
        await enviar_sinal_vip_exclusivo(context)

async def verificar_vips_expirados(context: ContextTypes.DEFAULT_TYPE):
    """Verifica e remove VIPs expirados"""
    usuarios_para_verificar = list(usuarios_vip)
    for user_id in usuarios_para_verificar:
        if verificar_vip_expirado(user_id):
            logger.info(f"VIP expirado removido: {user_id}")

# ==========================================
# CONFIGURAÇÃO DO AGENDADOR
# ==========================================
scheduler = AsyncIOScheduler()

# Sinais free estratégicos a cada 25 minutos
scheduler.add_job(
    autosinal_estrategico,
    trigger=IntervalTrigger(minutes=25),
    id="autosinal_free",
    replace_existing=True
)

# Sinais VIP exclusivos a cada 15 minutos
scheduler.add_job(
    autosinal_vip,
    trigger=IntervalTrigger(minutes=15),
    id="autosinal_vip", 
    replace_existing=True
)

# Verificação de VIPs expirados a cada hora
scheduler.add_job(
    verificar_vips_expirados,
    trigger=IntervalTrigger(hours=1),
    id="verificar_vips",
    replace_existing=True
)

# ==========================================
# INICIALIZAÇÃO E EXECUÇÃO PRINCIPAL
# ==========================================
async def main():
    """Função principal do bot"""
    logger.info("🚀 Iniciando Bot de Sinais Estratégico...")
    
    # Criar aplicação do bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Registrar handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vip", promover_vip_comando))
    app.add_handler(CommandHandler("status", status_bot))
    
    # Registrar handler de callbacks
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    # Iniciar agendador
    scheduler.start()
    logger.info("📅 Agendador de tarefas iniciado")
    
    # Iniciar bot
    await app.start()
    logger.info("🤖 Bot iniciado com sucesso!")
    logger.info(f"📊 Configurações: FREE={len(usuarios_free)} | VIP={len(usuarios_vip)}")
    
    # Iniciar polling
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
    finally:
        logger.info("🔚 Bot finalizado")


