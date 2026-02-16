# AI HOST — Arquitetura Tecnica

## Visao Geral

```
┌─────────────────────────────────────────────────────────┐
│                      OBS Studio                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │ Camera Feed  │  │ Avatar 9:16 │  │ HUD Overlay     │ │
│  │ (voce)       │  │ (Browser    │  │ (Browser Source) │ │
│  │              │  │  Source)     │  │ so voce ve      │ │
│  └─────────────┘  └──────┬──────┘  └────────┬────────┘ │
│                          │                    │          │
└──────────────────────────┼────────────────────┼──────────┘
                           │                    │
                    WebSocket              WebSocket
                           │                    │
              ┌────────────┴────────────────────┴──────────┐
              │            BACKEND (Node + Express)         │
              │                                             │
              │  ┌──────────┐ ┌──────────┐ ┌────────────┐ │
              │  │ Live     │ │ OBS      │ │ Memory     │ │
              │  │ Brain    │ │ Director │ │ Core       │ │
              │  │          │ │          │ │            │ │
              │  │ - STT    │ │ - Scenes │ │ - History  │ │
              │  │ - Script │ │ - Sources│ │ - Style    │ │
              │  │ - Track  │ │ - Layout │ │ - Learning │ │
              │  └──────────┘ └──────────┘ └────────────┘ │
              │                                             │
              │  ┌──────────┐ ┌──────────┐ ┌────────────┐ │
              │  │ SEO/AEO  │ │ Copy     │ │ TTS        │ │
              │  │ Engine   │ │ Engine   │ │ Engine     │ │
              │  │          │ │          │ │            │ │
              │  │ - Title  │ │ - Hooks  │ │ - Google   │ │
              │  │ - Desc   │ │ - CTAs   │ │ - Visemes  │ │
              │  │ - Tags   │ │ - Retain │ │ - Lip sync │ │
              │  └──────────┘ └──────────┘ └────────────┘ │
              │                                             │
              └──────────────────┬──────────────────────────┘
                                 │
                          ┌──────┴──────┐
                          │  POST ENGINE │
                          │  (Remotion)  │
                          │              │
                          │  - Cortes    │
                          │  - Shorts    │
                          │  - Thumbnail │
                          │  - Export    │
                          └──────┬──────┘
                                 │
                          ┌──────┴──────┐
                          │  YouTube    │
                          │  API v3     │
                          │             │
                          │  - Upload   │
                          │  - Analytics│
                          │  - SEO      │
                          └─────────────┘
```

---

## Modulos

### 1. LIVE BRAIN
**Responsabilidade**: Tudo que acontece ao vivo.

| Componente | Funcao | Tecnologia |
|-----------|--------|-----------|
| STT Listener | Transcreve voz em tempo real | Google Cloud Speech-to-Text (streaming) |
| Script Tracker | Compara transcricao com roteiro | Fuzzy matching + posicao sequencial |
| Context Monitor | Detecta se voce saiu do assunto | Comparacao de similaridade de texto |
| Alert System | Envia alertas pro HUD | WebSocket events |
| TTS Speaker | Fala com voce | Google Cloud Text-to-Speech |
| Viseme Generator | Gera dados de lip sync do audio TTS | Analise de fonemas do audio |

**Fluxo ao vivo**:
```
Microfone → STT → Texto → Script Tracker → Posicao no roteiro
                                          → Alertas pro HUD
                                          → Proximo ponto
```

### 2. OBS DIRECTOR
**Responsabilidade**: Controlar o OBS programaticamente.

| Componente | Funcao | Tecnologia |
|-----------|--------|-----------|
| OBS Connector | Conexao persistente com OBS | obs-websocket-js (v5) |
| Scene Manager | Criar/trocar cenas | OBS WebSocket API |
| Source Manager | Gerenciar fontes (camera, overlay) | OBS WebSocket API |
| Layout Engine | Posicionar elementos | OBS WebSocket transforms |
| Auto Config | Configuracao inicial do OBS | Script de setup |

**Setup inicial do OBS** (Fase 1):
```
Cena: "AI Host Live"
├── Source: Camera (voce) - 16:9
├── Source: Avatar Browser (9:16) - posicionado a direita
├── Source: HUD Browser - fullscreen, invisivel pro stream
└── Source: Audio (mic + desktop)
```

### 3. SEO/AEO ENGINE
**Responsabilidade**: Otimizacao de conteudo para busca.

| Componente | Funcao |
|-----------|--------|
| Keyword Researcher | Pesquisa termos relevantes |
| Title Generator | Gera 5+ opcoes de titulo otimizado |
| Description Writer | Descricao com keywords + CTA |
| Tag Generator | Tags relevantes |
| Chapter Marker | Gera timestamps de capitulos |
| AEO Optimizer | Estrutura FAQ/schema para respostas de IA |

### 4. COPY ENGINE
**Responsabilidade**: Copywriting magnetica.

| Componente | Funcao |
|-----------|--------|
| Hook Generator | Primeiros 30 segundos (curiosity gap) |
| Retention Mapper | Estrutura de retencao (reset points) |
| CTA Builder | Calls to action naturais |
| Thumbnail Copy | Texto para thumbnail |

### 5. POST ENGINE (Remotion)
**Responsabilidade**: Edicao automatizada pos-gravacao.

| Componente | Funcao |
|-----------|--------|
| Silence Detector | Remove pausas longas |
| Highlight Extractor | Marca melhores momentos |
| Shorts Generator | Corta verticais 9:16 < 60s |
| Thumbnail Capture | Seleciona melhor frame |
| Renderer | Renderiza via Node |

### 6. MEMORY CORE
**Responsabilidade**: Persistencia e aprendizado.

**Estrutura** (JSON local):
```
memory/
├── broadcasts.json        # Historico de lives/gravacoes
├── scripts.json           # Roteiros usados
├── performance.json       # Metricas por video
├── style.json             # Seu estilo (palavras, ritmo, tom)
├── audience.json          # Perfil da audiencia
└── mistakes.json          # Erros para nao repetir
```

---

## Comunicacao entre Modulos

Tudo via **WebSocket** interno + **Event Emitter**.

```
Evento                    → Quem escuta
─────────────────────────────────────────
speech:transcribed        → Live Brain (Script Tracker)
script:position_updated   → Frontend (HUD)
script:lost_context       → Frontend (Alert) + TTS
obs:scene_change          → OBS Director
obs:source_update         → OBS Director
render:start              → Post Engine
render:complete           → YouTube uploader
memory:save               → Memory Core
```

---

## Portas e Servicos

| Servico | Porta | Descricao |
|---------|-------|-----------|
| Backend API | 3001 | Express REST + WebSocket |
| Avatar Frontend | 3000 | React dev server |
| HUD Frontend | 3002 | React dev server (overlay) |
| OBS WebSocket | 4455 | OBS WebSocket Server (padrao OBS) |

---

## APIs Externas

| API | Uso | Auth |
|-----|-----|------|
| Google Cloud STT | Transcricao de voz | API Key |
| Google Cloud TTS | Voz do avatar | API Key |
| YouTube Data API v3 | Upload, analytics, metadata | OAuth 2.0 |
| OBS WebSocket v5 | Controle do OBS | Password local |
