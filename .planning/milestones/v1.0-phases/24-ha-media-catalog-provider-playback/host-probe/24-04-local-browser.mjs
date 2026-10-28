import assert from 'node:assert/strict';
import { readFile, mkdir } from 'node:fs/promises';
import { createRequire } from 'node:module';
import path from 'node:path';
import os from 'node:os';

const workspace = process.cwd();
const require = createRequire(path.join(workspace, 'modules/bridge/web_ui/package.json'));
const { chromium, expect } = require('@playwright/test');
const bundle = await readFile(path.join(workspace, 'modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js'));
const dist = path.join(workspace, 'modules/bridge/web_ui/dist');
const output = path.join(os.tmpdir(), 'bl-haos-plan24-04-visual');
await mkdir(output, { recursive: true });
const origin = 'http://catalog.fixture.invalid';
const browser = await chromium.launch({ headless: true });
const evidence = [];
try {
  for (const width of [375, 768, 1440]) {
    for (const reducedMotion of ['no-preference', 'reduce']) {
      const page = await browser.newPage({ viewport: { width, height: 900 }, reducedMotion });
      const pageErrors = [];
      const outsideRequests = [];
      page.on('pageerror', (error) => pageErrors.push(error.message));
      await page.route('**/*', async (route) => {
        const url = new URL(route.request().url());
        if (url.origin !== origin) { outsideRequests.push(url.origin); await route.abort(); return; }
        if (url.pathname === '/panel.js') { await route.fulfill({ contentType: 'text/javascript', body: bundle }); return; }
        if (url.pathname === '/api/image/serve/fixture/512x512') {
          await route.fulfill({ contentType: 'image/png', body: Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aX1sAAAAASUVORK5CYII=', 'base64') }); return;
        }
        await route.fulfill({ contentType: 'text/html', body: '<!doctype html><html><head><title>Local injected HA fixture</title><style>html,body{margin:0;height:100%;background:#151a23}</style></head><body><bl-haos-media-panel></bl-haos-media-panel><script type="module" src="/panel.js"></script></body></html>' });
      });
      await page.goto(origin);
      await page.waitForFunction(() => customElements.get('bl-haos-media-panel'));
      await page.evaluate(() => {
        const playlist = {
          title: 'Evening provider playlist with an unusually long complete title '.repeat(4).trim(),
          media_content_id: 'media-source://provider/opaque%2Fid?order=a%2Bb',
          media_content_type: 'provider/playlist;opaque=Yes', media_class: 'playlist', can_play: true, can_expand: false,
          thumbnail: '/api/image/serve/fixture/512x512',
        };
        const folder = { title: 'I', media_content_id: 'media-source://provider/folder', media_content_type: 'app', can_play: false, can_expand: true };
        const root = { title: 'A', media_content_id: 'media-source://', media_content_type: 'app', can_play: false, can_expand: true, can_search: true, children: [folder, playlist, ...Array.from({ length: 18 }, (_, index) => ({ ...playlist, title: `Audio playlist ${index + 1}`, media_content_id: `media-source://provider/${index}` }))] };
        window.fixture = { calls: [], services: [], failRoot: true, failSearch: true, failPlay: true, playlist, root };
        const speaker = { entity_id: 'media_player.kitchen', state: 'idle', attributes: { friendly_name: 'Kitchen speaker with an unusually long but fully readable room and device name', bluetooth_address: 'aa:bb:cc:dd:ee:01', adapter: 'hci0' } };
        window.fixture.hass = {
          connection: { connected: true }, user: { id: 'injected-local-fixture' }, states: { [speaker.entity_id]: speaker },
          callWS: async (message) => {
            window.fixture.calls.push(message);
            if (window.fixture.failRoot) { window.fixture.failRoot = false; throw new Error('private root failure'); }
            if (message.type === 'media_source/search_media') {
              if (window.fixture.failSearch) { window.fixture.failSearch = false; throw new Error('private search failure'); }
              return { result: [playlist] };
            }
            if (message.media_content_id === folder.media_content_id) return { ...folder, children: [playlist] };
            return root;
          },
          callService: async (...args) => {
            window.fixture.services.push(args);
            if (window.fixture.failPlay) { window.fixture.failPlay = false; throw new Error('private provider failure'); }
          },
        };
        document.querySelector('bl-haos-media-panel').hass = window.fixture.hass;
      });
      const panel = page.locator('bl-haos-media-panel');
      const selector = panel.getByRole('combobox', { name: 'Play on' });
      const rootRetry = panel.getByRole('button', { name: 'Retry media sources' });
      await expect(rootRetry).toBeVisible();
      const originalAlert = await panel.getByRole('alert').textContent();
      await selector.selectOption('media_player.kitchen');
      await page.evaluate(() => {
        document.querySelector('bl-haos-media-panel').hass = { ...window.fixture.hass, states: { ...window.fixture.hass.states } };
      });
      await expect(selector).toHaveValue('media_player.kitchen');
      await expect(rootRetry).toBeVisible();
      await expect(panel.getByRole('alert')).toHaveText(originalAlert);
      await expect(panel.getByRole('alert')).not.toContainText('private root failure');
      assert.equal(await page.evaluate(() => window.fixture.calls.length), 1);
      await rootRetry.click();
      await expect(panel.getByRole('listitem')).toHaveCount(20);
      const rootCalls = await page.evaluate(() => window.fixture.calls);
      assert.equal(rootCalls.length, 2); assert.deepEqual(rootCalls[1], rootCalls[0]);
      await expect(panel.getByRole('alert')).toHaveCount(0);
      assert.equal(await page.evaluate(() => window.fixture.services.length), 0);
      await selector.focus();
      await page.keyboard.press('Tab');
      await expect(panel.getByRole('link', { name: 'Close catalog' })).toBeFocused();
      const layout = await panel.evaluate((element) => {
        const shadow = element.shadowRoot;
        const main = shadow.querySelector('main');
        const body = shadow.querySelector('.catalog-body');
        const selector = shadow.querySelector('select');
        const bounds = selector.getBoundingClientRect();
        return {
          horizontalOverflow: main.scrollWidth > main.clientWidth,
          bodyScroll: body.scrollHeight > body.clientHeight,
          selectorWithinViewport: bounds.left >= 0 && bounds.right <= innerWidth,
          smallControls: [...shadow.querySelectorAll('button,select,a,input')].filter((control) => {
            const box = control.getBoundingClientRect();
            return box.width < 44 || box.height < 44;
          }).length,
          transition: getComputedStyle(shadow.querySelector('button')).transitionDuration,
          focusOutline: getComputedStyle(shadow.querySelector('.close-catalog')).outlineStyle,
          imageReady: [...shadow.querySelectorAll('img')].some((image) => image.complete && image.naturalWidth > 0),
        };
      });
      assert.equal(layout.horizontalOverflow, false);
      assert.equal(layout.selectorWithinViewport, true);
      assert.equal(layout.bodyScroll, true);
      assert.equal(layout.smallControls, 0);
      assert.equal(layout.focusOutline, 'solid');
      assert.equal(layout.imageReady, true);
      assert.equal(layout.transition, reducedMotion === 'reduce' ? '0s' : '0.15s');
      const screenshot = path.join(output, `panel-${width}-${reducedMotion}.png`);
      const pixels = await page.screenshot({ path: screenshot });
      const pixelCheck = await page.evaluate(async (imageData) => {
        const image = new Image(); image.src = `data:image/png;base64,${imageData}`; await image.decode();
        const canvas = document.createElement('canvas'); canvas.width = image.width; canvas.height = image.height;
        const context = canvas.getContext('2d'); context.drawImage(image, 0, 0);
        const data = context.getImageData(0, 0, canvas.width, canvas.height).data;
        const colors = new Set();
        for (let index = 0; index < data.length; index += 160) colors.add(`${data[index]},${data[index + 1]},${data[index + 2]}`);
        return { colors: colors.size, width: image.width, height: image.height };
      }, pixels.toString('base64'));
      assert.ok(pixelCheck.colors > 20);
      const title = await page.evaluate(() => window.fixture.playlist.title);
      await panel.getByRole('button', { name: `Play ${title}`, exact: true }).click();
      const speakerName = await page.evaluate(() => window.fixture.hass.states['media_player.kitchen'].attributes.friendly_name);
      await expect(panel.getByRole('alert')).not.toContainText('private provider failure');
      assert.equal(await page.evaluate(() => window.fixture.services.length), 1);
      await panel.getByRole('button', { name: `Retry ${title} on ${speakerName}`, exact: true }).click();
      await expect(panel.getByRole('status')).toContainText(`Starting playback on ${speakerName}`);
      const services = await page.evaluate(() => window.fixture.services);
      assert.equal(services.length, 2); assert.deepEqual(services[1], services[0]);
      assert.equal(services[0][2].media_content_id, 'media-source://provider/opaque%2Fid?order=a%2Bb');
      assert.deepEqual(services[0][3], { entity_id: 'media_player.kitchen' });
      await panel.getByRole('button', { name: 'Open I', exact: true }).click();
      await expect(panel.getByRole('heading', { name: 'I', exact: true })).toBeVisible();
      const breadcrumb = panel.getByRole('navigation', { name: 'Catalog path' }).getByRole('button', { name: 'A', exact: true });
      const breadcrumbBox = await breadcrumb.boundingBox();
      assert.ok(breadcrumbBox.width >= 44, `breadcrumb width ${breadcrumbBox.width}`);
      assert.ok(breadcrumbBox.height >= 44, `breadcrumb height ${breadcrumbBox.height}`);
      const controls = await panel.evaluate((element) => [...element.shadowRoot.querySelectorAll('button,select,a,input')].map((control) => {
        const box = control.getBoundingClientRect();
        return { label: control.getAttribute('aria-label') || control.textContent, width: box.width, height: box.height };
      }));
      for (const control of controls) {
        assert.ok(control.width >= 44 && control.height >= 44, JSON.stringify(control));
      }
      await panel.getByRole('button', { name: 'Back', exact: true }).focus();
      await page.keyboard.press('Escape');
      await expect(panel.getByRole('button', { name: 'Open I', exact: true })).toBeFocused();
      const search = panel.getByRole('searchbox', { name: 'Search media' });
      await search.fill('evening'); await search.press('Enter');
      const searchRetry = panel.getByRole('button', { name: 'Retry search' });
      await expect(searchRetry).toBeVisible();
      const searchCalls = await page.evaluate(() => window.fixture.calls.length);
      await search.fill('different');
      await selector.selectOption('');
      await expect(searchRetry).toBeVisible();
      assert.equal(await page.evaluate(() => window.fixture.calls.length), searchCalls);
      await searchRetry.click();
      await expect(panel.getByRole('listitem')).toHaveCount(1);
      assert.deepEqual(await page.evaluate(() => window.fixture.calls.at(-1)), { type: 'media_source/search_media', media_content_id: 'media-source://', search_query: 'evening' });
      const capturedSearchCalls = await page.evaluate(() => window.fixture.calls.slice(-2));
      assert.deepEqual(capturedSearchCalls[1], capturedSearchCalls[0]);
      await selector.selectOption('media_player.kitchen');
      await page.evaluate(() => {
        const hass = window.fixture.hass; hass.states['media_player.kitchen'].state = 'unavailable';
        document.querySelector('bl-haos-media-panel').hass = { ...hass };
      });
      await expect(panel.getByRole('button', { name: `Play ${title}`, exact: true })).toBeDisabled();
      await expect(selector).toHaveValue('media_player.kitchen');
      assert.deepEqual(pageErrors, []); assert.deepEqual(outsideRequests, []);
      evidence.push({ width, reducedMotion, layout, breadcrumb: { width: breadcrumbBox.width, height: breadcrumbBox.height }, controls, rootRetry: { callsBeforeManual: 1, callsAfterManual: rootCalls.length, identical: true }, searchRetry: { capturedQuery: 'evening', identical: true }, pixelCheck, screenshot, services: services.length });
      await page.close();
    }
  }

  const ingress = await browser.newPage({ viewport: { width: 375, height: 900 } });
  const apiRequests = [];
  await ingress.routeWebSocket('**', (socket) => socket.close());
  await ingress.route('**/*', async (route) => {
    const url = new URL(route.request().url());
    assert.equal(url.origin, origin);
    if (url.pathname === '/frame') { await route.fulfill({ contentType: 'text/html', body: '<iframe title="Ingress fixture" src="/ingress/" style="border:0;width:100%;height:850px"></iframe>' }); return; }
    if (url.pathname.includes('/api/')) {
      apiRequests.push(url.pathname);
      await route.fulfill({ json: url.pathname.endsWith('/adapters') || url.pathname.endsWith('/devices') ? [] : { native_transport_ready: true } }); return;
    }
    if (url.pathname.startsWith('/ingress/assets/')) {
      await route.fulfill({ body: await readFile(path.join(dist, 'assets', path.basename(url.pathname))), contentType: url.pathname.endsWith('.css') ? 'text/css' : 'text/javascript' }); return;
    }
    if (url.pathname === '/bl-haos-media') { await route.fulfill({ contentType: 'text/html', body: '<h1>Registered route fixture, not authenticated HA</h1>' }); return; }
    await route.fulfill({ contentType: 'text/html', body: await readFile(path.join(dist, 'index.html')) });
  });
  await ingress.goto(`${origin}/frame`);
  const link = ingress.frameLocator('iframe').getByRole('link', { name: 'Open Media Catalog' });
  await expect(link).toBeVisible();
  const anchorBox = await link.boundingBox(); assert.ok(anchorBox.width >= 44 && anchorBox.height >= 44);
  await link.focus(); await expect(link).toBeFocused();
  const beforeClick = apiRequests.length;
  await link.press('Enter');
  await expect(ingress).toHaveURL(`${origin}/bl-haos-media`);
  assert.equal(apiRequests.length, beforeClick);
  await ingress.close();
  console.log(JSON.stringify({ scope: 'offline injected fixture; no HA/provider/auth acceptance', evidence, ingress: { topFrameNavigation: true, additionalApiCalls: 0 }, output }, null, 2));
} finally {
  await browser.close();
}