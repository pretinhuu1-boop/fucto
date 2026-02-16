# AI HOST — Super Contexto

## O que e isso

Um AI Co-Host operacional pessoal para live streaming e producao de conteudo.
Ele aparece como avatar 3D no OBS, fala com voce ao vivo, opera o OBS,
guia seu roteiro, e depois cuida da pos-producao e publicacao no YouTube.

**Tipo**: Sistema interno pessoal. Rapido e funcional. Sem SaaS, sem over-engineering.

---

## Os 3 Pilares

### 1. LIVE (durante a transmissao)
- Avatar 3D (Ready Player Me + React Three Fiber) em formato 9:16 transparente
- Overlay no OBS via Browser Source
- Teleprompter inteligente: escuta voce (STT), rastreia posicao no roteiro
- HUD invisivel pro publico: noticias, proximos pontos, alertas
- Controle do OBS via WebSocket API
- Ve sua tela, ouve voce, fala com voce (TTS)

### 2. POS-PRODUCAO (depois da gravacao)
- Remotion para edicao automatizada
- Cortes automaticos, remocao de silencios
- Geracao de Shorts (9:16)
- Thumbnail automatica
- Export multi-formato (9:16, 16:9)

### 3. PUBLICACAO + OTIMIZACAO
- SEO YouTube (titulos, descricoes, keywords, capitulos)
- AEO (otimizacao para respostas de IA)
- Copy magnetica (hooks, retencao, gatilhos psicologicos)
- Publicacao via YouTube Data API
- Leitura de analytics para aprender e melhorar

---

## Stack

| Camada       | Tecnologia                          |
|-------------|--------------------------------------|
| Backend     | Node.js + Express                    |
| Frontend    | React + React Three Fiber            |
| Avatar      | Ready Player Me + Viseme lip sync    |
| STT         | Google Cloud Speech-to-Text API      |
| TTS         | Google Cloud Text-to-Speech API      |
| OBS         | OBS WebSocket v5 API                 |
| Video       | Remotion                             |
| YouTube     | YouTube Data API v3                  |
| Memoria     | JSON local (evolui depois)           |
| Comunicacao | WebSocket (backend <-> frontend)     |

---

## Decisoes Tomadas

- **STT/TTS**: Google Cloud API (chave ja disponivel)
- **Avatar**: Three.js + Ready Player Me (melhor visual 3D, lip sync nativo)
- **Modo ao vivo**: Avatar fala com TTS + aparece visualmente
- **Modo HUD**: So texto no overlay (invisivel pro publico)
- **OBS**: Instalado, nada configurado. Configuramos do zero.
- **Memoria**: JSON local para comecar. Sem vector DB, sem embeddings complexos.
- **Escopo**: Pessoal, funcional, evolutivo.

---

## Regras de Execucao

1. Uma task por vez
2. Codigo completo em cada task (nada de placeholder)
3. Explicar decisoes tecnicas
4. Nao avancar sem validacao
5. Sempre entregar algo funcional
6. Simplicidade > Elegancia
7. Funciona > Perfeito

---

## 5 Fases

| Fase | O que entrega | Resultado |
|------|--------------|-----------|
| 1    | Node backend + OBS WebSocket + React overlay 9:16 + Avatar | Avatar aparece no OBS e se comunica |
| 2    | STT + rastreamento de roteiro + HUD + alertas | Teleprompter inteligente funcionando |
| 3    | SEO/AEO engine + Copy generator | Videos nascem otimizados |
| 4    | Remotion: corte, shorts, thumbnail, export | Pos-producao semi-automatica |
| 5    | Memoria + analytics + aprendizado | Sistema evolui com voce |

---

## Estrutura de Pastas

```
ai-host/
├── docs/                    # Documentacao
│   ├── SUPER_CONTEXT.md     # Este documento
│   ├── ARCHITECTURE.md      # Arquitetura tecnica
│   ├── AGENT_SPEC.md        # Personalidade e regras do agente
│   ├── TASKS.md             # Board de tasks
│   └── PHASE_1_PLAN.md      # Plano detalhado fase 1
├── src/
│   ├── backend/             # Node + Express + WebSocket server
│   ├── frontend/            # React + Three.js avatar overlay
│   ├── obs-agent/           # OBS WebSocket controller
│   ├── seo-engine/          # SEO/AEO/Copy engine
│   ├── remotion-pipeline/   # Edicao de video automatizada
│   └── memory/              # Sistema de memoria local
└── config/                  # Configs (OBS, API keys, etc)
```
