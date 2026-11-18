# Blog de Jardinería Francisco Gómez

Blog automático de [jardineriafranciscogomez.com](https://jardineriafranciscogomez.com): 2 entradas a la semana en español, martes y viernes a las 09:00, y 1 en inglés cada dos jueves a las 09:00 (desde el 3 de diciembre de 2026).

## Cómo funciona

1. **Cada domingo** una tarea programada de Claude escribe las 2 entradas de la semana siguiente en `articulos/`, siguiendo `docs/redaccion.md` y los temas de `temas.json`, y las sube a `main`.
   Ese mismo día añade enlaces desde artículos anteriores hacia los que ya se han publicado (enlazado interno en los dos sentidos).
2. **GitHub Actions** (`.github/workflows/publicar.yml`) valida los artículos (SEO, GEO y enlaces) y los manda a WordPress como **entradas programadas** para su fecha, con imagen destacada de Pexels, los campos de Yoast y datos estructurados FAQPage. Si un artículo ya enviado cambia en el repo, actualiza la entrada en WordPress sin tocar su fecha. Lo enviado queda apuntado en `publicados.json`.
3. **Del domingo al martes** puedes revisarlas en WordPress → Entradas → *Programadas*. Si no las tocas, se publican solas.

### Blog en inglés

- Artículos en `articulos/en/` (cabecera igual más `idioma: en`), temas en `temas_en.json`, guía en `docs/writing-en.md`.
- La tarea del domingo escribe el del jueves que toca (cada dos semanas desde el 3/12/2026) y los enlaces de vuelta entre artículos en inglés.
- Se enlazan solo páginas `/en/` y artículos en inglés. En WordPress van con el idioma inglés de Polylang, en la categoría «Gardening tips», y su dirección es `/en/<slug>/`. El idioma y la categoría los pone el mu-plugin (campo REST `jfg_lang`), así que necesita la versión 3 de `wordpress/yoast-rest-meta.php`.

Cada mañana el workflow vuelve a pasar por si algo falló.

## Puesta en marcha (una vez)

**En WordPress**
1. Usuario `redaccion` con rol *Editor*.
2. En su perfil → *Contraseñas de aplicación* → crea una («github blog») y cópiala.
3. Instala el snippet `wordpress/yoast-rest-meta.php` (con el plugin Code Snippets o como mu-plugin) para que Yoast reciba título SEO, descripción y keyword.
4. Elementor → Theme Builder: plantilla de *Entrada individual* y de *Archivo*; enlace «Blog» en el menú.

**En GitHub** → Settings → Secrets and variables → Actions:
- `WP_USER` = `redaccion`
- `WP_APP_PASSWORD` = la contraseña de aplicación
- `PEXELS_API_KEY` = clave gratuita de pexels.com/api (opcional; sin ella no hay imagen destacada)

Después: pestaña *Actions* → *Publicar en WordPress* → *Run workflow*.

## Si algo falla

- **401 / 403 al conectar**: el hosting o un plugin de seguridad bloquea la cabecera `Authorization`. En Apache se arregla añadiendo al `.htaccess`: `SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1`.
- **Aviso «Yoast no ha recibido los metadatos»**: falta el snippet del paso 3.
- **Aviso «la entrada no ha quedado en inglés»**: falta la versión 3 del snippet o Polylang no está activo. Se reintenta en la siguiente ejecución.
- **Un artículo no pasa la validación**: el error dice qué campo; se corrige el `.md` y se sube.

## Cambiar cosas

- **Una entrada antes de publicarse**: edítala directamente en WordPress. El repo no vuelve a tocar lo ya enviado.
- **Temas**: añade al final de `temas.json` (o `temas_en.json`). Cuando quedan pocos, la tarea del domingo añade más ella misma.
- **Estilo**: `docs/redaccion.md` (inglés: `docs/writing-en.md`).
