# 🚀 Asteroids Game

Um clássico jogo Asteroids desenvolvido em Python usando Pygame, com gráficos modernos, efeitos de partículas e sistema de pontuação.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Descrição

Este projeto é uma implementação completa do clássico jogo Asteroids, onde você controla uma espaçonave em um campo de asteroides no espaço. Destrua os asteroides para ganhar pontos, evite colisões e tente quebrar seu próprio recorde!

## 🎮 Características

- **Sistema de Vidas**: 3 vidas para começar
- **Sistema de Pontuação**: Ganha pontos destruindo asteroides
- **High Score**: Recorde salvo automaticamente
- **Efeitos Visuais**: Sistema de partículas para explosões
- **Campo de Estrelas**: Fundo animado para imersão
- **Controles Responsivos**: Movimentação fluida da espaçonave
- **Sistema de Pause**: Pause o jogo com ESC
- **Tela de Game Over**: Reinicie pressionando qualquer tecla
- **Asteroides Dinâmicos**: Asteroides se dividem quando destruídos

## 🎯 Controles

| Tecla | Ação |
|-------|------|
| `W` | Mover para frente |
| `S` | Mover para trás |
| `A` | Rotacionar à esquerda |
| `D` | Rotacionar à direita |
| `ESPAÇO` | Atirar |
| `ESC` | Pausar/Despausar |
| `Qualquer tecla` | Reiniciar (quando game over) |

## 🏗️ Arquitetura

O projeto é organizado em módulos especializados:

- **`main.py`**: Loop principal do jogo e gerenciamento de eventos
- **`player.py`**: Lógica da espaçonave do jogador
- **`asteroid.py`**: Comportamento e divisão dos asteroides
- **`asteroidfield.py`**: Geração contínua de asteroides
- **`shot.py`**: Sistema de projéteis
- **`particles.py`**: Efeitos de partículas e explosões
- **`starfield.py`**: Fundo de estrelas animado
- **`circleshape.py`**: Classe base para objetos circulares
- **`audio.py`**: Gerenciamento de efeitos sonoros
- **`constants.py`**: Constantes do jogo (velocidades, tamanhos, etc.)

## ⚙️ Instalação e Execução

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou baixe o projeto**
   ```bash
   # Se usando git
   git clone <url-do-repositorio>
   cd asteroids

   # Ou simply extraia o arquivo ZIP baixado
   ```

2. **Instale as dependências**
   ```bash
   pip install pygame==2.6.1
   ```

3. **Execute o jogo**
   ```bash
   python main.py
   ```

## 🕹️ Como Jogar

1. **Objetivo**: Destrua todos os asteroides para ganhar pontos
2. **Movimento**: Use as teclas WASD para controlar sua espaçonave
3. **Atirar**: Pressione ESPAÇO para atirar projéteis
4. **Asteroides Grandes**: São os mais valiosos em pontos
5. **Asteroides Pequenos**: Menos pontos, mas se movem mais rápido
6. **Evite Colisões**: Uma colisão custos uma vida
7. **Game Over**: Quando perder todas as vidas

## 🎨 Pontuação

O sistema de pontuação varia baseado no tamanho do asteroid destruído:
- **Asteroides Grandes**: Mais pontos
- **Asteroides Pequenos**: Menos pontos

Tente quebrar seu próprio recorde!

## 🔧 Configurações

Você pode ajustar as configurações do jogo editando o arquivo `constants.py`:

```python
# Configurações de Tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Configurações de Asteroides
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8

# Configurações do Jogador
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_SHOOT_COOLDOWN = 0.2
```

## 📁 Estrutura de Arquivos

```
asteroids/
├── main.py              # Arquivo principal
├── player.py            # Lógica do jogador
├── asteroid.py          # Lógica dos asteroides
├── asteroidfield.py     # Campo de asteroides
├── shot.py              # Sistema de disparos
├── particles.py         # Efeitos de partículas
├── starfield.py         # Fundo de estrelas
├── circleshape.py       # Classe base
├── audio.py             # Sistema de áudio
├── constants.py         # Constantes
├── requirements.txt     # Dependências
├── README.md           # Este arquivo
├── highscore.txt       # Pontuação máxima (gerado automaticamente)
└── .gitignore          # Arquivos ignorados pelo git
```

## 🎵 Funcionalidades Avançadas

- **Sistema de Partículas**: Explosões realistas com partículas coloridas
- **Campo de Estrelas**: Fundo dinâmico que se move continuamente
- **Proteção Temporária**: Jogador fica invulnerável após colisão
- **Efeitos Sonoros**: Feedback auditivo para ações do jogo
- **Tela de Pause**: Pause o jogo a qualquer momento
- **Salvamento Automático**: High score salvo automaticamente

## 🐛 Possíveis Melhorias Futuras

- [ ] Sistema de níveis progressivos
- [ ] Diferentes tipos de power-ups
- [ ] Múltiplas naves jogáveis
- [ ] Efeitos sonoros customizados
- [ ] Música de fundo
- [ ] Sistema de conquistas
- [ ] Modo multiplayer
- [ ] Temas visuais diferentes

## 🤝 Contribuição

Este é um projeto de código aberto! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Implementar novas funcionalidades
- Melhorar a documentação

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🙏 Créditos

Desenvolvido como uma implementação moderna do clássico jogo Asteroids.

---

**Divirta-se jogando! 🎮🚀**