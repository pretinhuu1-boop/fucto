# AI HOST — MCPs, Skills e Ferramentas

## Resumo Executivo

Este documento mapeia todos os MCPs e skills que o sistema precisa
para funcionar como pipeline completo: design → imagem → animacao → video → publicacao.

---

## Stack de MCPs Escolhida

### TIER 1 — Essenciais (Fase 1-2)

| MCP | O que faz | Install |
|-----|-----------|---------|
| **@_davideast/stitch-mcp** | Google Stitch — gera UI completa de texto/imagem, exporta HTML+Tailwind, extrai Design DNA | `npx @_davideast/stitch-mcp proxy` |
| **royshil/obs-mcp** | Controla OBS: cenas, fontes, gravacao, streaming, transicoes | `npx -y obs-mcp@latest` |
| **@remotion/mcp** | Busca semantica na doc do Remotion (ajuda o agente a escrever codigo correto) | `npm install @remotion/mcp --save-exact` |
| **remotion-media-mcp** | Gera assets: imagens (Nano Banana Pro), video (Veo 3.1), musica (Suno), TTS (ElevenLabs), SFX, legendas | `npx remotion-media-mcp` |
| **elevenlabs-mcp** | TTS avancado, voice design, voice cloning, sound effects, transcricao | `uvx elevenlabs-mcp` |

### TIER 2 — Producao Visual (Fase 3-4)

| MCP | O que faz | Install |
|-----|-----------|---------|
| **comfyui-mcp-server** | Stable Diffusion local via ComfyUI, workflows customizados | `pip install` do repo joenorton |
| **mcp-video-gen** | RunwayML + Luma AI: text-to-video, image-to-video | Clone wheattoast11/mcp-video-gen |
| **PixVerse-MCP** | Video + lip sync + sound effects | `uvx pixverse-mcp` |
| **misbahsy/video-audio-mcp** | FFmpeg completo: corte, overlay, transicoes, remocao silencio | Clone + pip install |
| **sharp-mcp** | Processamento de imagem: resize, crop, otimizacao | `npx sharp-mcp` |

### TIER 3 — Publicacao e SEO (Fase 4-5)

| MCP | O que faz | Install |
|-----|-----------|---------|
| **youtube-mcp-server** | Upload, metadata, thumbnail, analytics YouTube | Clone adamanz/youtube-mcp-server |
| **dataforseo-mcp** | Keyword research, SERP analysis, backlinks | Config com API key DataForSEO |
| **seo-review-tools-mcp** | Otimizacao de conteudo, readability, plagiarism | Config com API key |

### TIER 4 — Opcionais (quando precisar)

| MCP | O que faz | Install |
|-----|-----------|---------|
| **figma-mcp** | Se quiser design no Figma em vez do Stitch | `npx figma-developer-mcp` |
| **blender-mcp** | Modelagem 3D se precisar de assets 3D custom | Addon Blender |
| **heygen-mcp** | Avatar hiper-realista com lip sync (alternativa ao RPM) | Config com HEYGEN_API_KEY |
| **suno-mcp** | Musica AI independente (fora do kie.ai) | Config com Suno API |
| **playwright-mcp** | Automacao de browser pra testes | `npx @playwright/mcp` |

---

## Google Stitch — Detalhes

### O que e
Ferramenta do Google (Labs) que gera UI completa a partir de texto ou imagem.
Usa Gemini por baixo. Exporta HTML+Tailwind e Figma.

### Tools disponiveis via MCP

| Tool | Funcao |
|------|--------|
| `generate_screen_from_text` | Gera tela de UI a partir de prompt |
| `extract_design_context` | Extrai "Design DNA" (fontes, cores, layout) |
| `fetch_screen_code` | Baixa HTML/CSS da tela gerada |
| `fetch_screen_image` | Baixa screenshot em alta resolucao |
| `create_project` | Cria projeto novo |
| `list_projects` | Lista projetos |
| `list_screens` | Lista telas de um projeto |
| `build_site` | Monta site completo mapeando telas a rotas |

### Workflow pro nosso projeto
1. Usar `extract_design_context` em referencia visual que voce curtir
2. Usar `generate_screen_from_text` com esse contexto pra gerar telas do avatar overlay, HUD, painel de controle
3. `fetch_screen_code` pra pegar o HTML+Tailwind
4. Converter pra React no nosso projeto

### Limites
- Gera so HTML+Tailwind (precisa converter pra React)
- Demora 2-10 min por tela
- 350 geracoes/mes (Flash) ou 200/mes (Pro)
- Gratis

### Setup
```bash
npx @_davideast/stitch-mcp init -c claude-code
```
Precisa de projeto Google Cloud (voce ja tem API key do Google).

---

## Nano Banana Pro — Detalhes

### O que e
Modelo de geracao de imagem do Google (Gemini 3 Pro Image).
Melhor text rendering do mercado. Resolucao ate 4K nativa.

### Por que escolhemos
- **Texto em imagem**: 94% de acuracia (melhor que DALL-E, Midjourney, Flux)
- **4K nativo**: Perfeito pra producao de video
- **Reference images**: Ate 14 imagens de referencia pra manter consistencia
- **Edicao conversacional**: Edita imagem com linguagem natural
- **Aspect ratios**: 1:1, 9:16, 16:9, 21:9 — todos os formatos de video

### Comparativo rapido

| | Nano Banana Pro | DALL-E 3 | Midjourney V7 | Flux Pro |
|--|----------------|----------|---------------|----------|
| Texto em imagem | Melhor | Bom | Ruim | Pessimo |
| Resolucao max | 4K | 1K | 1K | 2K |
| Velocidade | 8-12s | 15-25s | 20-30s | ~10s |
| Fotorrealismo | Muito bom | Bom | Bom | Melhor |
| Arte criativa | Bom | Bom | Melhor | Bom |
| Custo/imagem | $0.09-0.24 | $0.02-0.12 | Sub mensal | $0.05 |

### Uso via remotion-media-mcp
```
generate_image:
  prompt: "descricao da imagem"
  output_name: "nome_arquivo"
  aspect_ratio: "16:9"
  resolution: "2K"
  image_urls: ["ref1.jpg", "ref2.jpg"]  # ate 8 referencias
```

### Custo via Kie.ai
- 1K-2K: ~$0.09-0.12 por imagem
- 4K: ~$0.24 por imagem
- Creditos a partir de $5, sem assinatura

---

## Remotion — Pipeline Completo

### 3 pecas que se complementam

```
@remotion/mcp          → Ajuda o agente a escrever codigo Remotion correto
Remotion Agent Skills  → Ensina padroes de animacao frame-accurate
remotion-media-mcp     → Gera os assets (imagem, video, audio, legenda)
```

### remotion-media-mcp — 10 Tools

| Tool | Servico | O que faz |
|------|---------|-----------|
| `generate_image` | Nano Banana Pro | Gera imagem AI |
| `generate_video_from_text` | Google Veo 3.1 | Texto → video |
| `generate_video_from_image` | Google Veo 3.1 | Anima imagem |
| `generate_music` | Suno V3.5-V5 | Gera musica AI |
| `generate_sound_effect` | ElevenLabs SFX | Gera efeito sonoro |
| `generate_speech` | ElevenLabs TTS | Texto → fala (21 vozes) |
| `generate_subtitles` | Whisper (local) | Audio → legenda SRT |
| `list_assets` | Airtable | Lista biblioteca de assets |
| `backup_asset` | Airtable | Salva asset na biblioteca |
| `get_asset` | Airtable | Baixa asset por ID |

### Workflow de producao
1. Gerar imagens com `generate_image` (thumbnails, b-roll, graficos)
2. Animar imagens com `generate_video_from_image` (transicoes, motion)
3. Gerar musica de fundo com `generate_music`
4. Gerar narracao com `generate_speech`
5. Gerar efeitos sonoros com `generate_sound_effect`
6. Gerar legendas com `generate_subtitles`
7. Tudo cai em `public/` → `staticFile()` → Remotion renderiza

### API Key unica
Tudo via **KIE_API_KEY** (kie.ai) — um gateway so, pay-as-you-go.

---

## OBS MCP — Opcoes

### royshil/obs-mcp (Recomendado — simples)
```bash
npx -y obs-mcp@latest
# Env: OBS_WEBSOCKET_PASSWORD
```
Controla cenas, fontes, gravacao, streaming, transicoes.

### ironystock/agentic-obs (Avancado — 69 tools)
Go-based. TUI dashboard, web dashboard. Pra quem quer controle total.

---

## Skills do Remotion

```bash
npx create-video@latest my-video && cd my-video
npx skills add remotion-dev/skills
```

Instala `SKILL.md` em `.claude/skills/remotion/` que ensina:
- Animacoes frame-synchronized
- Uso correto de `useCurrentFrame()`, `interpolate()`, `spring()`
- Workflow de verificacao (renderiza antes de entregar)

---

## Skills do Stitch

```bash
npx skills add google-labs-code/stitch-skills --skill stitch-loop --global
```

| Skill | O que faz |
|-------|-----------|
| `stitch-loop` | Gera site multi-pagina de um prompt |
| `react-components` | Converte telas Stitch em componentes React |
| `enhance-prompt` | Refina prompt vago em prompt otimizado |
| `remotion` | Gera walkthrough video de projetos Stitch |
| `design-md` | Cria documentacao de design |

---

## Configuracao MCP no Claude Code

Arquivo `.mcp.json` na raiz do projeto:

```json
{
  "mcpServers": {
    "stitch": {
      "command": "npx",
      "args": ["@_davideast/stitch-mcp", "proxy"]
    },
    "obs": {
      "command": "npx",
      "args": ["-y", "obs-mcp@latest"],
      "env": {
        "OBS_WEBSOCKET_PASSWORD": "${OBS_WS_PASSWORD}"
      }
    },
    "remotion-docs": {
      "command": "npx",
      "args": ["@remotion/mcp"]
    },
    "remotion-media": {
      "command": "npx",
      "args": ["remotion-media-mcp"],
      "env": {
        "KIE_API_KEY": "${KIE_API_KEY}"
      }
    },
    "elevenlabs": {
      "command": "uvx",
      "args": ["elevenlabs-mcp"],
      "env": {
        "ELEVENLABS_API_KEY": "${ELEVENLABS_API_KEY}"
      }
    },
    "ffmpeg": {
      "command": "python",
      "args": ["-m", "video_audio_mcp"],
      "env": {}
    },
    "sharp": {
      "command": "npx",
      "args": ["sharp-mcp"]
    }
  }
}
```

---

## Chaves de API Necessarias

| Chave | Servico | Obrigatoria | Custo |
|-------|---------|-------------|-------|
| `GOOGLE_API_KEY` | Google Cloud STT/TTS | Sim | Pay per use |
| `KIE_API_KEY` | Kie.ai (Nano Banana, Veo, Suno, ElevenLabs) | Sim | A partir de $5 |
| `ELEVENLABS_API_KEY` | ElevenLabs (TTS direto, fora do kie) | Opcional | Free tier 10k chars |
| `OBS_WS_PASSWORD` | OBS WebSocket local | Sim | Gratis |
| `YOUTUBE_CLIENT_ID` | YouTube Data API | Fase 4 | Gratis |
| `YOUTUBE_CLIENT_SECRET` | YouTube Data API | Fase 4 | Gratis |
| `AIRTABLE_API_KEY` | Asset library | Opcional | Free tier |
| `DATAFORSEO_LOGIN` | SEO research | Fase 5 | Pay per use |
