const ENTITY_NAME = "BL-HAOS Phase24 Probe Sink";
const SENTINEL = "media-source://bl_haos_phase24_probe/nonplaying-sentinel";

class Phase24Probe extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._running = false;
    this._status = "ready";
  }

  set hass(value) {
    this._hass = value;
    this._render();
  }

  get hass() {
    return this._hass;
  }

  connectedCallback() {
    this._render();
  }

  _render() {
    const output = document.createElement("pre");
    output.textContent = JSON.stringify({
      status: this._status,
      version: this.hass?.config?.version ?? null,
      injected: Boolean(this.hass),
      callWS: typeof this.hass?.callWS === "function",
      callService: typeof this.hass?.callService === "function",
      ...this._result,
    }, null, 2);
    this.shadowRoot.replaceChildren(output);
  }

  _probeEntity() {
    const matches = Object.values(this.hass?.states ?? {}).filter((state) =>
      state.entity_id.startsWith("media_player.") &&
      state.attributes.friendly_name === ENTITY_NAME &&
      state.attributes.probe_sink === true
    );
    return matches.length === 1 ? matches[0] : null;
  }

  async runContractChecks() {
    if (this._running) return { busy: true };
    this._running = true;
    const result = {
      version: this.hass?.config?.version ?? null,
      injected: Boolean(this.hass),
      browse: false,
      service: false,
      recorded: false,
      entity_id: null,
      call_count: 0,
      media_type: null,
    };
    this._status = "running";
    this._result = result;
    this._render();
    try {
      if (result.version !== "2026.10.3") return result;
      try {
        const root = await this.hass.callWS({ type: "media_source/browse_media" });
        result.browse = Boolean(root && typeof root === "object");
      } catch {
        result.browse = false;
      }
      const entity = this._probeEntity();
      if (!entity) return result;
      result.entity_id = entity.entity_id;
      const before = entity.attributes.call_count;
      if (!Number.isInteger(before)) return result;
      try {
        await this.hass.callService("media_player", "play_media", {
          media_content_id: SENTINEL,
          media_content_type: "music",
        }, { entity_id: entity.entity_id });
        result.service = true;
        for (let attempt = 0; attempt < 40; attempt += 1) {
          const updated = this._probeEntity();
          if (updated?.entity_id === entity.entity_id) {
            result.call_count = updated.attributes.call_count;
            result.media_type = updated.attributes.last_media_type;
            result.recorded = result.call_count === before + 1 && result.media_type === "music";
          }
          if (result.recorded) break;
          await new Promise((resolve) => setTimeout(resolve, 50));
        }
      } catch {
        result.service = false;
      }
      return result;
    } finally {
      this._running = false;
      this._status = result.browse && result.service && result.recorded ? "passed" : "failed";
      this._render();
    }
  }
}

customElements.define("bl-haos-phase24-probe", Phase24Probe);