# AI HOST — Fase 1: Base Operacional (Plano Detalhado)

## Objetivo
Ao final desta fase, o avatar 3D aparece no OBS com fundo transparente,
o backend Node esta rodando, e existe comunicacao bidirecional via WebSocket.

---

## Pre-requisitos

### No seu Mac
- Node.js 18+ instalado
- OBS Studio instalado
- OBS WebSocket Server habilitado (Ferramentas > WebSocket Server Settings)
  - Porta: 4455 (padrao)
  - Senha: definir uma senha
- Google Cloud API Key configurada

### Dependencias principais
```
# Backend
express
ws
obs-websocket-js
dotenv
cors

# Frontend (Avatar)
react
@react-three/fiber
@react-three/drei
three
@readyplayerme/visage (ou carregamento direto do .glb)
```

---

## Passo a Passo de Implementacao

### Bloco 1: Backend (Tasks T-101 a T-105)

**Estrutura**:
```
src/backend/
├── server.js              # Express + WebSocket server
├── events.js              # EventEmitter central
├── routes/
│   ├── health.js          # GET /api/health
│   └── status.js          # GET /api/status
├── websocket/
│   └── handler.js         # WebSocket message handler
└── config/
    └── loader.js          # Le .env e config.json
```

**server.js** deve:
- Subir Express na porta 3001
- Subir WebSocket server no mesmo HTTP server
- Registrar rotas REST
- Registrar WebSocket handler
- Logar conexoes/desconexoes

**Protocolo WebSocket**:
```json
{
  "type": "string",     // tipo do evento
  "payload": {},        // dados
  "timestamp": "ISO"    // quando foi enviado
}
```

Tipos de mensagem:
- `avatar:speak` — backend manda texto pro avatar falar
- `avatar:animate` — backend manda animacao pro avatar
- `hud:update` — backend atualiza HUD
- `hud:alert` — backend envia alerta
- `obs:command` — backend envia comando pro OBS
- `client:ready` — frontend avisa que carregou

---

### Bloco 2: OBS Director (Tasks T-111 a T-117)

**Estrutura**:
```
src/obs-agent/
├── director.js            # Classe OBSDirector
├── scenes.js              # Gerenciamento de cenas
├── sources.js             # Gerenciamento de fontes
└── setup.js               # Setup inicial automatizado
```

**OBSDirector** deve:
- Conectar ao OBS via `obs-websocket-js`
- Manter conexao viva (reconnect automatico)
- Expor metodos: `listScenes()`, `switchScene()`, `createScene()`, `addSource()`

**Setup inicial** (script que roda uma vez):
1. Criar cena "AI Host Live"
2. Adicionar source: Webcam (Video Capture)
3. Adicionar source: Browser Source "Avatar" (URL: http://localhost:3000, 1080x1920)
4. Adicionar source: Browser Source "HUD" (URL: http://localhost:3002, 1920x1080)
5. Posicionar avatar na lateral direita
6. HUD como overlay fullscreen

---

### Bloco 3: Avatar Frontend (Tasks T-121 a T-128)

**Estrutura**:
```
src/frontend/
├── package.json
├── vite.config.js
├── index.html             # Canvas transparente
├── src/
│   ├── App.jsx            # Componente principal
│   ├── Avatar.jsx         # Ready Player Me 3D model
│   ├── LipSync.jsx        # Viseme controller
│   ├── Animations.jsx     # Idle + gestos
│   └── ws.js              # WebSocket client
└── public/
    └── avatar.glb         # Modelo Ready Player Me
```

**Canvas**:
- Fundo transparente (`alpha: true` no WebGLRenderer)
- Tamanho: 1080x1920 (9:16)
- HTML/body com `background: transparent`

**Avatar**:
- Carregar .glb do Ready Player Me
- Aplicar morph targets para visemas (lip sync)
- Animacao idle: leve respiracao, piscar, movimento sutil de cabeca
- Receber comandos do backend via WebSocket

**Como criar o avatar**:
1. Ir em https://readyplayer.me
2. Criar avatar (pode usar foto)
3. Baixar o .glb
4. Colocar em `public/avatar.glb`

---

### Bloco 4: HUD Frontend (Tasks T-131 a T-135)

**Estrutura**:
```
src/frontend-hud/
├── package.json
├── vite.config.js
├── index.html
├── src/
│   ├── App.jsx
│   ├── Teleprompter.jsx   # Area do roteiro
│   ├── NewsTicker.jsx     # Noticias scrolling
│   ├── AlertBar.jsx       # Alertas do sistema
│   └── ws.js              # WebSocket client
```

**Layout do HUD**:
```
┌─────────────────────────────┐
│  [ALERTA]                   │  ← AlertBar (topo, aparece quando necessario)
│                             │
│  ROTEIRO                    │
│  ► Ponto atual              │  ← Teleprompter (centro)
│    Proximo ponto            │
│    ...                      │
│                             │
│  ─────────────────────────  │
│  📰 Noticia 1 | Noticia 2  │  ← NewsTicker (rodape, scrolling)
└─────────────────────────────┘
```

- Fundo: semi-transparente escuro
- Texto: branco, alto contraste
- Ponto atual: highlight (amarelo ou verde)
- Alertas: vermelho/laranja, piscando

---

## Validacao da Fase 1

A fase esta completa quando:

- [ ] `npm start` sobe o backend na porta 3001
- [ ] `npm run dev` sobe o avatar na porta 3000
- [ ] `npm run dev:hud` sobe o HUD na porta 3002
- [ ] Backend conecta no OBS via WebSocket
- [ ] Avatar aparece no OBS como Browser Source com fundo transparente
- [ ] HUD aparece no OBS como overlay
- [ ] Backend envia mensagem → Avatar reage
- [ ] Backend envia mensagem → HUD exibe

---

## Prompt para Execucao Autonoma

Copie e cole isso para o Claude executar a Fase 1:

```
Voce e um engenheiro backend/frontend. Leia os documentos:
- docs/SUPER_CONTEXT.md
- docs/ARCHITECTURE.md
- docs/AGENT_SPEC.md
- docs/PHASE_1_PLAN.md
- docs/TASKS.md

Execute as tasks da FASE 1 uma por uma, comecando pela T-101.
Para cada task:
1. Implemente codigo completo e funcional
2. Explique brevemente suas decisoes
3. Marque a task como [x] no TASKS.md
4. So avance para a proxima task depois de concluir a atual

Stack: Node + Express + WebSocket (backend), React + Vite + React Three Fiber (frontend)
Nao use placeholder. Codigo real, funcional.
Comece pela T-101.
```
