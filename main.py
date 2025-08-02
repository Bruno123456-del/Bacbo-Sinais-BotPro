

    await asyncio.sleep(120)

    if random.random() < CHANCE_WIN_ENTRADA_INICIAL:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN)
        await asyncio.sleep(2)
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_ENTRADA, 'rb'), caption="✅ WIN NA ENTRADA PRINCIPAL!
💰 LUCRO ALCANÇADO: +4%")
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown')
        return

    await bot.send_message(chat_id=CHAT_ID, text="⚠️ Ativando GALE 1.")
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_1:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN)
        await asyncio.sleep(2)
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_GALE1, 'rb'), caption="✅ WIN NO GALE 1!
💰 LUCRO TOTAL: +8%")
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown')
        return

    await bot.send_message(chat_id=CHAT_ID, text="⚠️ Ativando GALE 2.")
    await asyncio.sleep(120)
    if random.random() < CHANCE_WIN_GALE_2:
        placar["greens"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_WIN)
        await asyncio.sleep(2)
        await bot.send_photo(chat_id=CHAT_ID, photo=open(IMG_WIN_GALE2, 'rb'), caption="✅ WIN NO GALE 2!
💰 LUCRO TOTAL: +16%")
        await bot.send_message(chat_id=CHAT_ID, text=random.choice(reforco_pos_win), parse_mode='Markdown')
    else:
        placar["reds"] += 1
        await bot.send_animation(chat_id=CHAT_ID, animation=GIF_RED, caption="❌ STOP LOSS

Encerramos para proteger o capital.")

async def ciclo_de_sinais(bot: Bot):
    sinais_enviados = 0
    while True:
        await simular_e_enviar_sinal(bot)
        sinais_enviados += 1

        if sinais_enviados % 3 == 0:
            await bot.send_message(chat_id=CHAT_ID, text=f"📊 PLACAR
✅ Greens: {placar['greens']}
❌ Reds: {placar['reds']}", parse_mode='Markdown')
            try:
                imagem = random.choice(PROVAS_SOCIAIS)
                texto = random.choice([
                    "🔥 Veja esse resultado incrível!",
                    "🚀 Nossa comunidade está lucrando pesado!",
                    "💰 Resultado que fala por si só!"
                ])
                await bot.send_photo(chat_id=CHAT_ID, photo=open(imagem, 'rb'), caption=texto)
            except Exception as e:
                print(f"Erro ao enviar prova social: {e}")

        await asyncio.sleep(15 * 60)

async def gestao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Protocolo de Gestão Avançada...", parse_mode='Markdown')

async def enviar_e_fixar_mensagem_inicial(bot: Bot):
    try:
        msg = await bot.send_message(chat_id=CHAT_ID, text=mensagem_fixada_texto, parse_mode='Markdown')
        await bot.pin_chat_message(chat_id=CHAT_ID, message_id=msg.message_id)
    except Exception as e:
        print(f"Erro ao fixar mensagem: {e}")

async def enviar_mensagem_recorrente(bot: Bot):
    while True:
        await asyncio.sleep(6 * 60 * 60)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=mensagem_automatica_recorrente, parse_mode='Markdown')
        except Exception as e:
            print(f"Erro mensagem recorrente: {e}")

async def main():
    print("Iniciando Bot BAC BO com estratégia Escada Asiática...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("gestao", gestao))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    bot = application.bot
    asyncio.create_task(enviar_e_fixar_mensagem_inicial(bot))
    asyncio.create_task(ciclo_de_sinais(bot))
    asyncio.create_task(enviar_mensagem_recorrente(bot))

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot finalizado.")
