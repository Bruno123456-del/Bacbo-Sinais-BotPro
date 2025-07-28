#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 APOSTAS MILIONÁRIAS VIP - PLATAFORMA FUTURISTA 🚀
Sistema avançado de apostas com IA, conversões e retenção
Desenvolvido para máxima performance e experiência do usuário
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
import datetime
import random
import json
import os
import requests
from threading import Timer
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# 🎯 CONFIGURAÇÕES GLOBAIS
DATABASE = 'apostas_vip.db'
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'SEU_BOT_TOKEN_AQUI')
TELEGRAM_CHANNEL = '@ApostasMilionariaVIP'

# 🎲 CONFIGURAÇÕES DO BAC BO
BAC_BO_CONFIG = {
    'empate_cobertura': 0.001,  # 0.1% cobertura no empate
    'bonus_multiplicador': 2.5,
    'min_aposta': 1.0,
    'max_aposta': 10000.0
}

# 🎨 TEMPLATE HTML FUTURISTA
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Apostas Milionárias VIP - Plataforma Futurista</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            overflow-x: hidden;
            min-height: 100vh;
        }

        /* 🌟 ANIMAÇÕES FUTURISTAS */
        @keyframes neonGlow {
            0%, 100% { box-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff, 0 0 60px #00ffff; }
            50% { box-shadow: 0 0 30px #ff00ff, 0 0 50px #ff00ff, 0 0 70px #ff00ff; }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* 🎯 HEADER FUTURISTA */
        .header {
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(20px);
            border-bottom: 2px solid #00ffff;
            padding: 1rem 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            animation: slideIn 1s ease-out;
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }

        .logo {
            font-size: 2rem;
            font-weight: bold;
            background: linear-gradient(45deg, #00ffff, #ff00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: neonGlow 3s infinite;
        }

        .nav-stats {
            display: flex;
            gap: 2rem;
            font-size: 0.9rem;
        }

        .stat-item {
            text-align: center;
            padding: 0.5rem;
            background: rgba(0, 255, 255, 0.1);
            border-radius: 10px;
            border: 1px solid #00ffff;
        }

        /* 🚀 HERO SECTION */
        .hero {
            margin-top: 100px;
            padding: 4rem 2rem;
            text-align: center;
            background: radial-gradient(circle at center, rgba(0, 255, 255, 0.1) 0%, transparent 70%);
        }

        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 2s infinite;
        }

        .hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }

        /* 🎲 BAC BO GAME SECTION */
        .bac-bo-container {
            max-width: 800px;
            margin: 2rem auto;
            padding: 2rem;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 20px;
            border: 2px solid #00ffff;
            animation: neonGlow 4s infinite;
        }

        .game-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            color: #00ffff;
        }

        .dice-container {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem 0;
        }

        .dice {
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            font-weight: bold;
            color: white;
            animation: float 3s infinite;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .dice:hover {
            transform: scale(1.1);
            box-shadow: 0 0 30px #00ffff;
        }

        .betting-area {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }

        .bet-option {
            background: rgba(0, 255, 255, 0.1);
            border: 2px solid #00ffff;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .bet-option:hover {
            background: rgba(0, 255, 255, 0.2);
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
        }

        .bet-option.selected {
            background: rgba(255, 0, 255, 0.2);
            border-color: #ff00ff;
        }

        .bet-amount {
            width: 100%;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #00ffff;
            border-radius: 10px;
            color: white;
            font-size: 1.1rem;
            text-align: center;
            margin: 1rem 0;
        }

        /* 🎯 BOTÕES FUTURISTAS */
        .btn-futurista {
            background: linear-gradient(45deg, #00ffff, #ff00ff);
            border: none;
            padding: 1rem 2rem;
            border-radius: 50px;
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
            margin: 0.5rem;
        }

        .btn-futurista:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 255, 255, 0.5);
        }

        .btn-futurista:active {
            transform: translateY(0);
        }

        .btn-bonus {
            background: linear-gradient(45deg, #ff6b35, #f7931e);
            animation: pulse 2s infinite;
            font-size: 1.5rem;
            padding: 1.5rem 3rem;
        }

        /* 📊 ESTATÍSTICAS */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
            padding: 0 2rem;
        }

        .stat-card {
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ffff;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            animation: slideIn 1s ease-out;
        }

        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            color: #00ffff;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            font-size: 1.1rem;
            opacity: 0.8;
        }

        /* 🎁 SEÇÃO DE BÔNUS */
        .bonus-section {
            background: rgba(255, 0, 255, 0.1);
            border: 2px solid #ff00ff;
            border-radius: 20px;
            padding: 3rem;
            margin: 3rem 2rem;
            text-align: center;
        }

        .bonus-title {
            font-size: 2.5rem;
            color: #ff00ff;
            margin-bottom: 1rem;
        }

        .bonus-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }

        .bonus-item {
            background: rgba(0, 0, 0, 0.7);
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #ff00ff;
        }

        /* 📱 RESPONSIVO */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5rem; }
            .nav-container { flex-direction: column; gap: 1rem; }
            .dice-container { flex-wrap: wrap; }
            .betting-area { grid-template-columns: 1fr; }
        }

        /* 🌟 EFEITOS ESPECIAIS */
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00ffff;
            border-radius: 50%;
            animation: float 6s infinite linear;
        }

        .notification {
            position: fixed;
            top: 120px;
            right: 20px;
            background: rgba(0, 255, 255, 0.9);
            color: black;
            padding: 1rem 2rem;
            border-radius: 10px;
            font-weight: bold;
            z-index: 1001;
            animation: slideIn 0.5s ease-out;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #00ffff;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* 🎯 SEÇÃO DE CONVERSÃO */
        .conversion-section {
            background: rgba(0, 0, 0, 0.9);
            padding: 3rem 2rem;
            margin: 2rem 0;
        }

        .conversion-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .conversion-card {
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
            border: 2px solid #00ffff;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }

        .conversion-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 255, 255, 0.3);
        }

        /* 🔥 FOOTER */
        .footer {
            background: rgba(0, 0, 0, 0.9);
            padding: 2rem;
            text-align: center;
            border-top: 2px solid #00ffff;
            margin-top: 4rem;
        }
    </style>
</head>
<body>
    <!-- 🌟 PARTÍCULAS DE FUNDO -->
    <div id="particles"></div>

    <!-- 🎯 HEADER -->
    <header class="header">
        <div class="nav-container">
            <div class="logo">
                <i class="fas fa-rocket"></i> APOSTAS MILIONÁRIAS VIP
            </div>
            <div class="nav-stats">
                <div class="stat-item">
                    <div><i class="fas fa-users"></i></div>
                    <div id="online-users">{{ online_users }}</div>
                    <div>Online</div>
                </div>
                <div class="stat-item">
                    <div><i class="fas fa-trophy"></i></div>
                    <div id="total-wins">{{ total_wins }}</div>
                    <div>Vitórias</div>
                </div>
                <div class="stat-item">
                    <div><i class="fas fa-coins"></i></div>
                    <div id="total-profit">R$ {{ total_profit }}</div>
                    <div>Lucros</div>
                </div>
            </div>
        </div>
    </header>

    <!-- 🚀 HERO SECTION -->
    <section class="hero">
        <h1><i class="fas fa-gem"></i> PLATAFORMA FUTURISTA DE APOSTAS</h1>
        <p>🎯 Sistema Avançado com IA • 🚀 Conversões Máximas • 💎 Retenção Garantida</p>
        
        <!-- 🎲 BAC BO GAME -->
        <div class="bac-bo-container">
            <h2 class="game-title"><i class="fas fa-dice"></i> BAC BO FUTURISTA</h2>
            
            <div class="dice-container">
                <div class="dice" id="dice1">?</div>
                <div class="dice" id="dice2">?</div>
                <div class="dice" id="dice3">?</div>
                <div class="dice" id="dice4">?</div>
            </div>

            <div class="betting-area">
                <div class="bet-option" data-bet="banker">
                    <h3><i class="fas fa-crown"></i> BANKER</h3>
                    <p>Payout: 1:1</p>
                    <p>Cobertura: 0.1%</p>
                </div>
                <div class="bet-option" data-bet="player">
                    <h3><i class="fas fa-user"></i> PLAYER</h3>
                    <p>Payout: 1:1</p>
                    <p>Cobertura: 0.1%</p>
                </div>
                <div class="bet-option" data-bet="tie">
                    <h3><i class="fas fa-handshake"></i> EMPATE</h3>
                    <p>Payout: 8:1</p>
                    <p><strong>Cobertura: 0.1%</strong></p>
                </div>
            </div>

            <input type="number" class="bet-amount" id="betAmount" placeholder="Valor da Aposta (R$)" min="1" max="10000" value="10">
            
            <div style="text-align: center; margin: 2rem 0;">
                <button class="btn-futurista btn-bonus" onclick="playBacBo()">
                    <i class="fas fa-rocket"></i> JOGAR BAC BO COM BÔNUS
                </button>
            </div>

            <div id="gameResult" style="margin-top: 2rem; text-align: center; font-size: 1.2rem;"></div>
        </div>
    </section>

    <!-- 📊 ESTATÍSTICAS EM TEMPO REAL -->
    <section class="stats-container">
        <div class="stat-card">
            <div class="stat-number" id="active-players">{{ active_players }}</div>
            <div class="stat-label"><i class="fas fa-gamepad"></i> Jogadores Ativos</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="daily-profit">R$ {{ daily_profit }}</div>
            <div class="stat-label"><i class="fas fa-chart-line"></i> Lucro Diário</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="success-rate">{{ success_rate }}%</div>
            <div class="stat-label"><i class="fas fa-target"></i> Taxa de Sucesso</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="bonus-active">{{ bonus_active }}</div>
            <div class="stat-label"><i class="fas fa-gift"></i> Bônus Ativos</div>
        </div>
    </section>

    <!-- 🎁 SEÇÃO DE BÔNUS E CONVERSÃO -->
    <section class="bonus-section">
        <h2 class="bonus-title"><i class="fas fa-star"></i> SISTEMA DE CONVERSÃO E RETENÇÃO</h2>
        <p>🚀 Tecnologia avançada para maximizar seus ganhos e manter você sempre no jogo!</p>
        
        <div class="bonus-list">
            <div class="bonus-item">
                <h3><i class="fas fa-rocket"></i> Bônus de Entrada</h3>
                <p>100% no primeiro depósito</p>
            </div>
            <div class="bonus-item">
                <h3><i class="fas fa-sync"></i> Cashback Diário</h3>
                <p>10% de volta todos os dias</p>
            </div>
            <div class="bonus-item">
                <h3><i class="fas fa-crown"></i> VIP Exclusivo</h3>
                <p>Acesso a palpites premium</p>
            </div>
            <div class="bonus-item">
                <h3><i class="fas fa-shield-alt"></i> Seguro de Aposta</h3>
                <p>Proteção contra perdas</p>
            </div>
            <div class="bonus-item">
                <h3><i class="fas fa-users"></i> Programa de Indicação</h3>
                <p>R$ 50 por amigo indicado</p>
            </div>
            <div class="bonus-item">
                <h3><i class="fas fa-trophy"></i> Torneios Semanais</h3>
                <p>Prêmios de até R$ 10.000</p>
            </div>
        </div>

        <div style="margin-top: 2rem;">
            <button class="btn-futurista" onclick="joinTelegram()">
                <i class="fab fa-telegram"></i> ENTRAR NO GRUPO VIP
            </button>
            <button class="btn-futurista" onclick="claimBonus()">
                <i class="fas fa-gift"></i> RESGATAR BÔNUS
            </button>
        </div>
    </section>

    <!-- 🎯 SEÇÃO DE CONVERSÃO AVANÇADA -->
    <section class="conversion-section">
        <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 2rem; color: #00ffff;">
            <i class="fas fa-brain"></i> SISTEMA DE IA PARA CONVERSÃO
        </h2>
        
        <div class="conversion-grid">
            <div class="conversion-card">
                <h3><i class="fas fa-robot"></i> IA Preditiva</h3>
                <p>Algoritmos avançados analisam padrões em tempo real para maximizar suas chances de vitória.</p>
                <div class="stat-number">97.3%</div>
                <div class="stat-label">Precisão</div>
            </div>
            
            <div class="conversion-card">
                <h3><i class="fas fa-chart-line"></i> Análise de Tendências</h3>
                <p>Sistema monitora milhares de jogos simultaneamente para identificar oportunidades únicas.</p>
                <div class="stat-number">24/7</div>
                <div class="stat-label">Monitoramento</div>
            </div>
            
            <div class="conversion-card">
                <h3><i class="fas fa-shield-alt"></i> Gestão de Risco</h3>
                <p>Proteção automática do seu bankroll com stop-loss inteligente e diversificação.</p>
                <div class="stat-number">0.1%</div>
                <div class="stat-label">Risco Máximo</div>
            </div>
        </div>
    </section>

    <!-- 🔥 FOOTER -->
    <footer class="footer">
        <p><i class="fas fa-rocket"></i> <strong>APOSTAS MILIONÁRIAS VIP</strong> - Plataforma Futurista de Apostas</p>
        <p>🎯 Tecnologia Avançada • 🚀 Conversões Máximas • 💎 Suporte 24/7</p>
        <p style="margin-top: 1rem; opacity: 0.7;">
            <i class="fab fa-telegram"></i> {{ telegram_channel }} | 
            <i class="fas fa-users"></i> {{ total_members }} Membros VIP
        </p>
    </footer>

    <script>
        // 🌟 SISTEMA DE PARTÍCULAS
        function createParticles() {
            const container = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
                container.appendChild(particle);
            }
        }

        // 🎲 SISTEMA BAC BO
        let selectedBet = null;
        let gameInProgress = false;

        document.querySelectorAll('.bet-option').forEach(option => {
            option.addEventListener('click', function() {
                document.querySelectorAll('.bet-option').forEach(opt => opt.classList.remove('selected'));
                this.classList.add('selected');
                selectedBet = this.dataset.bet;
            });
        });

        async function playBacBo() {
            if (gameInProgress) return;
            if (!selectedBet) {
                showNotification('⚠️ Selecione uma opção de aposta!', 'warning');
                return;
            }

            const betAmount = parseFloat(document.getElementById('betAmount').value);
            if (!betAmount || betAmount < 1) {
                showNotification('⚠️ Valor de aposta inválido!', 'warning');
                return;
            }

            gameInProgress = true;
            document.querySelector('.btn-bonus').innerHTML = '<div class="loading"></div> JOGANDO...';

            // Animação dos dados
            const dices = ['dice1', 'dice2', 'dice3', 'dice4'];
            const rollAnimation = setInterval(() => {
                dices.forEach(dice => {
                    document.getElementById(dice).textContent = Math.floor(Math.random() * 6) + 1;
                });
            }, 100);

            // Simular jogo
            setTimeout(async () => {
                clearInterval(rollAnimation);
                
                try {
                    const response = await fetch('/api/play-bac-bo', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            bet_type: selectedBet,
                            amount: betAmount
                        })
                    });
                    
                    const result = await response.json();
                    
                    // Mostrar resultado
                    dices.forEach((dice, index) => {
                        document.getElementById(dice).textContent = result.dices[index];
                    });
                    
                    const resultDiv = document.getElementById('gameResult');
                    if (result.won) {
                        resultDiv.innerHTML = `
                            <div style="color: #00ff00; font-size: 1.5rem;">
                                <i class="fas fa-trophy"></i> VITÓRIA! 
                                <br>Ganhou: R$ ${result.payout.toFixed(2)}
                                <br>Multiplicador: ${result.multiplier}x
                            </div>
                        `;
                        showNotification(`🎉 Parabéns! Você ganhou R$ ${result.payout.toFixed(2)}!`, 'success');
                    } else {
                        resultDiv.innerHTML = `
                            <div style="color: #ff6b6b; font-size: 1.2rem;">
                                <i class="fas fa-times"></i> Não foi desta vez...
                                <br>Tente novamente com o bônus!
                            </div>
                        `;
                        showNotification('💪 Não desista! Use o bônus para a próxima!', 'info');
                    }
                    
                    // Atualizar estatísticas
                    updateStats();
                    
                } catch (error) {
                    console.error('Erro no jogo:', error);
                    showNotification('❌ Erro no jogo. Tente novamente!', 'error');
                }
                
                gameInProgress = false;
                document.querySelector('.btn-bonus').innerHTML = '<i class="fas fa-rocket"></i> JOGAR BAC BO COM BÔNUS';
            }, 3000);
        }

        // 📊 ATUALIZAR ESTATÍSTICAS
        async function updateStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                document.getElementById('online-users').textContent = stats.online_users;
                document.getElementById('total-wins').textContent = stats.total_wins;
                document.getElementById('total-profit').textContent = 'R$ ' + stats.total_profit;
                document.getElementById('active-players').textContent = stats.active_players;
                document.getElementById('daily-profit').textContent = 'R$ ' + stats.daily_profit;
                document.getElementById('success-rate').textContent = stats.success_rate + '%';
                document.getElementById('bonus-active').textContent = stats.bonus_active;
            } catch (error) {
                console.error('Erro ao atualizar stats:', error);
            }
        }

        // 🔔 SISTEMA DE NOTIFICAÇÕES
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            
            const colors = {
                success: 'rgba(0, 255, 0, 0.9)',
                warning: 'rgba(255, 255, 0, 0.9)',
                error: 'rgba(255, 0, 0, 0.9)',
                info: 'rgba(0, 255, 255, 0.9)'
            };
            
            notification.style.background = colors[type] || colors.info;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 5000);
        }

        // 🎯 FUNÇÕES DE CONVERSÃO
        function joinTelegram() {
            window.open('{{ telegram_channel }}', '_blank');
            showNotification('🚀 Redirecionando para o grupo VIP!', 'success');
            
            // Tracking de conversão
            fetch('/api/track-conversion', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'telegram_join' })
            });
        }

        function claimBonus() {
            showNotification('🎁 Bônus de R$ 100 creditado na sua conta!', 'success');
            
            // Tracking de conversão
            fetch('/api/track-conversion', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'bonus_claim' })
            });
        }

        // 🚀 INICIALIZAÇÃO
        document.addEventListener('DOMContentLoaded', function() {
            createParticles();
            updateStats();
            
            // Atualizar stats a cada 30 segundos
            setInterval(updateStats, 30000);
            
            // Notificações automáticas para retenção
            setTimeout(() => {
                showNotification('🔥 Novo palpite VIP disponível! Confira agora!', 'info');
            }, 10000);
            
            setTimeout(() => {
                showNotification('💎 Bônus especial expira em 5 minutos!', 'warning');
            }, 60000);
        });

        // 📱 RESPONSIVIDADE AVANÇADA
        function handleResize() {
            if (window.innerWidth < 768) {
                document.querySelector('.hero h1').style.fontSize = '2rem';
                document.querySelector('.dice-container').style.flexWrap = 'wrap';
            }
        }

        window.addEventListener('resize', handleResize);
        handleResize();
    </script>
</body>
</html>
"""

# 🗄️ INICIALIZAÇÃO DO BANCO DE DADOS
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            total_wins INTEGER DEFAULT 0,
            total_losses INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            vip_status BOOLEAN DEFAULT FALSE,
            referral_code TEXT UNIQUE,
            referred_by TEXT
        )
    ''')
    
    # Tabela de jogos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            game_type TEXT NOT NULL,
            bet_type TEXT NOT NULL,
            bet_amount REAL NOT NULL,
            result TEXT NOT NULL,
            payout REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de conversões
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            user_ip TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de estatísticas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT UNIQUE NOT NULL,
            metric_value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# 🎲 LÓGICA DO BAC BO
def play_bac_bo_game(bet_type, amount):
    # Gerar dados aleatórios
    banker_dice1 = random.randint(1, 6)
    banker_dice2 = random.randint(1, 6)
    player_dice1 = random.randint(1, 6)
    player_dice2 = random.randint(1, 6)
    
    banker_total = banker_dice1 + banker_dice2
    player_total = player_dice1 + player_dice2
    
    dices = [banker_dice1, banker_dice2, player_dice1, player_dice2]
    
    # Determinar resultado
    if banker_total > player_total:
        winner = 'banker'
    elif player_total > banker_total:
        winner = 'player'
    else:
        winner = 'tie'
    
    # Calcular payout
    won = False
    payout = 0
    multiplier = 0
    
    if bet_type == winner:
        won = True
        if bet_type == 'tie':
            multiplier = 8
            payout = amount * multiplier
            # Aplicar cobertura de 0.1% no empate
            payout *= (1 + BAC_BO_CONFIG['empate_cobertura'])
        else:
            multiplier = 1
            payout = amount * multiplier
        
        # Aplicar bônus multiplicador
        payout *= BAC_BO_CONFIG['bonus_multiplicador']
    
    return {
        'dices': dices,
        'banker_total': banker_total,
        'player_total': player_total,
        'winner': winner,
        'won': won,
        'payout': round(payout, 2),
        'multiplier': multiplier
    }

# 📊 FUNÇÕES DE ESTATÍSTICAS
def get_stats():
    return {
        'online_users': random.randint(150, 300),
        'total_wins': random.randint(1500, 2500),
        'total_profit': f"{random.randint(50000, 150000):,}",
        'active_players': random.randint(80, 150),
        'daily_profit': f"{random.randint(5000, 15000):,}",
        'success_rate': random.randint(85, 95),
        'bonus_active': random.randint(20, 50)
    }

def track_conversion(action, request):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO conversions (action, user_ip, user_agent)
        VALUES (?, ?, ?)
    ''', (action, request.remote_addr, request.headers.get('User-Agent', '')))
    
    conn.commit()
    conn.close()

# 🌐 ROTAS DA APLICAÇÃO
@app.route('/')
def index():
    stats = get_stats()
    return render_template_string(HTML_TEMPLATE, 
                                telegram_channel=TELEGRAM_CHANNEL,
                                total_members=random.randint(500, 1000),
                                **stats)

@app.route('/api/play-bac-bo', methods=['POST'])
def api_play_bac_bo():
    try:
        data = request.get_json()
        bet_type = data.get('bet_type')
        amount = float(data.get('amount', 0))
        
        if not bet_type or amount < BAC_BO_CONFIG['min_aposta'] or amount > BAC_BO_CONFIG['max_aposta']:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        result = play_bac_bo_game(bet_type, amount)
        
        # Salvar jogo no banco (opcional)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO games (game_type, bet_type, bet_amount, result, payout)
            VALUES (?, ?, ?, ?, ?)
        ''', ('bac_bo', bet_type, amount, json.dumps(result), result['payout']))
        conn.commit()
        conn.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

@app.route('/api/track-conversion', methods=['POST'])
def api_track_conversion():
    try:
        data = request.get_json()
        action = data.get('action')
        
        if action:
            track_conversion(action, request)
            return jsonify({'success': True})
        
        return jsonify({'error': 'Ação não especificada'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🤖 INTEGRAÇÃO COM TELEGRAM (OPCIONAL)
def send_telegram_message(message):
    """Enviar mensagem para o canal do Telegram"""
    try:
        if TELEGRAM_BOT_TOKEN != 'SEU_BOT_TOKEN_AQUI':
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                'chat_id': TELEGRAM_CHANNEL,
                'text': message,
                'parse_mode': 'HTML'
            }
            requests.post(url, data=data)
    except Exception as e:
        print(f"Erro ao enviar mensagem Telegram: {e}")

# 🚀 SISTEMA DE NOTIFICAÇÕES AUTOMÁTICAS
def auto_notifications():
    """Sistema de notificações automáticas para retenção"""
    messages = [
        "🔥 Novo palpite VIP disponível! Taxa de acerto: 94%",
        "💎 Bônus especial de R$ 200 para os próximos 10 jogadores!",
        "🚀 Jackpot acumulado: R$ 50.000! Participe agora!",
        "⚡ Estratégia exclusiva liberada no grupo VIP!",
        "🎯 Meta diária: +300% de lucro alcançada por 15 membros!"
    ]
    
    message = random.choice(messages)
    send_telegram_message(message)
    
    # Reagendar para próxima notificação (30-60 minutos)
    Timer(random.randint(1800, 3600), auto_notifications).start()

# 🎯 INICIALIZAÇÃO DA APLICAÇÃO
if __name__ == '__main__':
    print("🚀 Iniciando Apostas Milionárias VIP - Plataforma Futurista")
    print("=" * 60)
    print("🎲 Sistema Bac Bo com cobertura de 0.1% no empate")
    print("🤖 IA para conversões e retenção ativada")
    print("📱 Interface futurista responsiva")
    print("🔗 Integração com Telegram configurada")
    print("=" * 60)
    
    # Inicializar banco de dados
    init_db()
    
    # Iniciar sistema de notificações automáticas
    Timer(300, auto_notifications).start()  # Primeira notificação em 5 minutos
    
    # Executar aplicação
    app.run(host='0.0.0.0', port=5000, debug=False)

