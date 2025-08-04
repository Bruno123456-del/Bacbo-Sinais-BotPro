 [\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
            resultado_msg = f"✅✅✅ **GREEN NO EMPATE!** ✅✅✅\n\n💰 **LUCRO MASSIVO!**\nA aposta principal foi devolvida e a cobertura no empate multiplicou a banca!\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_EMPATE, caption=resultado_msg)
            try:
                await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            except Exception as e:
                logger.error(f"Erro ao enviar GIF comemorativo: {e}")
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode=\'Markdown\', disable_web_page_preview=False)
            return

        # Resultado ENTRADA
        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.65:
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data[\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
            resultado_msg = f"✅✅✅ **GREEN NA ENTRADA!** ✅✅✅\n\n💰 **LUCRO: +4%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_ENTRADA, caption=resultado_msg)
            try:
                await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            except Exception as e:
                logger.error(f"Erro ao enviar GIF comemorativo: {e}")
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode=\'Markdown\', disable_web_page_preview=False)
            return

        # Gale 1
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ **Não bateu!** Vamos para a primeira proteção.\n\nAcionando **Gale 1**...", reply_to_message_id=msg_sinal_enviada.message_id)

        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.75:
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data[\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 1!** ✅✅✅\n\n💰 **LUCRO TOTAL: +8%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE1, caption=resultado_msg)
            try:
                await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            except Exception as e:
                logger.error(f"Erro ao enviar GIF comemorativo: {e}")
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode=\'Markdown\', disable_web_page_preview=False)
            return

        # Gale 2
        await context.bot.send_message(chat_id=CANAL_ID, text="⚠️ **Ainda não veio!** Usando nossa última proteção.\n\nAcionando **Gale 2**...", reply_to_message_id=msg_sinal_enviada.message_id)

        await asyncio.sleep(random.randint(80, 100))
        if random.random() < 0.85:
            bot_data["diario_win"] += 1
            placar = f"📊 Placar do dia: {bot_data[\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
            resultado_msg = f"✅✅✅ **GREEN NO GALE 2!** ✅✅✅\n\n💰 **LUCRO TOTAL: +16%**\n\n{placar}"
            await context.bot.send_photo(chat_id=CANAL_ID, photo=IMG_WIN_GALE2, caption=resultado_msg)
            try:
                await context.bot.send_animation(chat_id=CANAL_ID, animation=random.choice(GIFS_COMEMORACAO))
            except Exception as e:
                logger.error(f"Erro ao enviar GIF comemorativo: {e}")
            await context.bot.send_message(chat_id=CANAL_ID, text=MENSAGEM_POS_WIN, parse_mode=\'Markdown\', disable_web_page_preview=False)
            return

        # RED
        bot_data["diario_loss"] += 1
        placar = f"📊 Placar do dia: {bot_data[\'diario_win\']}W / {bot_data[\'diario_loss\']}L"
        resultado_msg = f"❌❌❌ **RED!** ❌❌❌\n\nO mercado não foi a nosso favor. Disciplina é a chave. Voltaremos mais fortes na próxima!\n\n{placar}"
        try:
            await context.bot.send_animation(chat_id=CANAL_ID, animation=GIF_LOSS, caption=resultado_msg)
        except Exception as e:
            logger.error(f"Erro ao enviar GIF de loss: {e}")
            # Se falhar, tenta enviar como texto simples
            await context.bot.send_message(chat_id=CANAL_ID, text=resultado_msg)
        logger.info(f"Resultado: RED. {placar}")

    except Exception as e:
        logger.error(f"Ocorreu um erro no ciclo de sinal: {e}")

async def resumo_diario(context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    win_count = bot_data.get("diario_win", 0)
    loss_count = bot_data.get("diario_loss", 0)

    if win_count == 0 and loss_count == 0:
        logger.info("Sem operações hoje. Resumo diário não enviado.")
        return

    resumo = (
        f"📊 **RESUMO DO DIA** 📊\n\n"
        f"✅ **Greens:** {win_count}\n"
        f"❌ **Reds:** {loss_count}\n\n"
        f"Obrigado por operar com a gente hoje! Amanhã buscaremos mais resultados. 🚀"
    )
    await context.bot.send_message(chat_id=CANAL_ID, text=resumo, parse_mode=\'Markdown\')
    logger.info("Resumo diário enviado.")
    
    bot_data["diario_win"] = 0
    bot_data["diario_loss"] = 0

# --- 6. FUNÇÃO PRINCIPAL QUE INICIA TUDO ---

def main():
    logger.info("Iniciando o bot...")

application = Application.builder().token(BOT_TOKEN).post_init(inicializar_contadores).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

job_queue = application.job_queue

intervalo_aleatorio = random.randint(900, 1500)
job_queue.run_repeating(enviar_sinal, interval=intervalo_aleatorio, first=10)

job_queue.run_daily(resumo_diario, time=time(hour=22, minute=0))

if __name__ == "__main__":
    application.run_polling()


