# Guía de redacción del blog

Esta guía manda sobre cualquier otra idea del redactor. Nadie revisa los artículos antes de que se programen en WordPress: se escriben como si fueran definitivos. Cada artículo tiene que estar optimizado para Google (SEO) y para que lo citen ChatGPT, Perplexity, Gemini y las respuestas con IA de Google (GEO), y enlazado con el resto de la web.

## La empresa

**Jardinería Francisco Gómez**, empresa de jardinería de Benissa (Alicante). Trabaja en la Marina Alta: Benissa, Calpe, Moraira y Teulada.

### Páginas a las que se puede enlazar (no hay otras)

| Clave | Página | URL |
|---|---|---|
| comunidades | Mantenimiento de comunidades | https://jardineriafranciscogomez.com/servicio/mantenimiento-de-comunidades/ |
| jardines-piscinas | Mantenimiento de jardines y piscinas | https://jardineriafranciscogomez.com/servicio/mantenimiento-de-jardines-y-piscinas/ |
| construccion | Construcción de jardines con rocallas, fuentes y césped | https://jardineriafranciscogomez.com/servicio/construccin-de-jardines-con-rocallas-fuentes-cesped/ |
| poda | Poda de árboles y palmeras | https://jardineriafranciscogomez.com/servicio/poda-de-arboles-y-palmeras/ |
| picudo | Tratamiento del picudo rojo | https://jardineriafranciscogomez.com/servicio/tratamiento-del-picudo/ |
| riego | Instalación de sistemas de riego | https://jardineriafranciscogomez.com/servicio/instalacion-de-sistemas-de-riego/ |
| parcelas | Limpieza de parcelas | https://jardineriafranciscogomez.com/servicio/limpieza-de-parcelas/ |
| (Benissa) | Inicio: jardinero en Benissa | https://jardineriafranciscogomez.com/ |
| (Calpe) | Jardinero en Calpe | https://jardineriafranciscogomez.com/jardinero-en-calpe/ |
| (Moraira) | Jardinero en Moraira | https://jardineriafranciscogomez.com/jardinero-en-moraira/ |
| | Todos los servicios | https://jardineriafranciscogomez.com/servicios/ |
| | Contacto | https://jardineriafranciscogomez.com/contacto/ |
| | WhatsApp | https://wa.me/34616779874 |

Teulada no tiene página propia: en sus artículos se enlaza la de Moraira (Moraira pertenece al término municipal de Teulada) o la de inicio.

## Público

Propietarios de chalets y casas de la costa (muchos con segunda residencia o residentes extranjeros que leen en español), administradores de fincas y presidentes de comunidades. Quieren saber qué hacer con su jardín y cuándo, y si les conviene llamar a un profesional.

## Tono

- Español de España, cercano y práctico, como un jardinero con oficio que explica las cosas claras. Tuteo.
- Frases cortas. Nada de relleno («en el mundo actual», «es importante destacar», «sin lugar a dudas», «en conclusión», «a la hora de»).
- Nada de lenguaje de marketing exagerado ni promesas absolutas. Sin emojis.
- Di también cuándo NO hace falta un profesional: da confianza.

## Prohibido

- Inventar datos de la empresa: años de experiencia, número de clientes, precios, valoraciones, premios, nombres de trabajadores, proyectos, clientes o casos concretos, ni describir «cómo lo hacemos nosotros» con detalles que no estén en esta guía.
- Dar precios o tarifas.
- Dar dosis o nombres comerciales de productos fitosanitarios: se recomienda que los aplique un profesional autorizado.
- Inventar normativa: sobre quemas, prevención de incendios u ordenanzas no se dan fechas, plazos ni multas; se explica la idea general y se remite al ayuntamiento.
- Citar estudios, estadísticas o porcentajes.
- Enlaces externos (a otras webs): ninguno.
- Repetir el tema, el enfoque o la keyword principal de un artículo ya escrito (mira todos los de `articulos/`).

## SEO

- **Una keyword principal** (la de `temas.json`) y **2-6 secundarias**: variantes y preguntas reales relacionadas que la gente escribe en Google. Las secundarias se usan de forma natural en el texto y en algún `##`.
- La keyword principal va, sin forzarla, en: `titulo`, `meta_titulo` (empezando por ella si suena bien), `slug`, `meta_descripcion`, el primer párrafo y al menos un `##`.
- `meta_titulo`: máx. 60 caracteres. Puede terminar en «| Jardinería Francisco Gómez» si cabe.
- `meta_descripcion`: 120-158 caracteres, con la keyword, el beneficio y un motivo para hacer clic.
- `slug`: 2-5 palabras, sin artículos ni preposiciones que sobren.
- Los `##` responden a las preguntas reales de esa búsqueda (las de «Otras preguntas de los usuarios» y las búsquedas relacionadas de Google), en el orden en que el lector se las haría. Mejor en forma de pregunta o con la respuesta en el propio título.

## GEO (que las IA lo citen)

1. **Respuesta directa al principio**: el primer párrafo, de 40 a 70 palabras, responde la pregunta del título por sí solo, con el dato o el criterio concreto (cuándo, cuánto, qué señales). Es el párrafo que copiaría una IA. Sin encabezado delante.
2. **Secciones que se entienden solas**: la primera frase después de cada `##` responde a ese título sin depender del resto; después vienen los matices.
3. **Definiciones explícitas** la primera vez que aparece un concepto: «El picudo rojo es…», «La xerojardinería es…».
4. **Datos concretos en vez de adjetivos**: meses, frecuencias, alturas, señales visibles. Sin inventar cifras.
5. **Al menos una lista numerada (pasos) o una tabla** (comparativa, calendario, fases). Las IA las extraen muy bien.
6. **Entidades claras**: nombra una vez «Jardinería Francisco Gómez» y la zona con su provincia («Calpe (Alicante)», «la Marina Alta») de forma natural.
7. **Preguntas frecuentes**: `## Preguntas frecuentes` con 3-5 preguntas `###` que terminan en «?», distintas de los `##`, sacadas de búsquedas reales. Respuestas de 2-4 frases que se entienden solas. Se publican también como datos estructurados FAQPage.

## Enlazado interno

Con anclas descriptivas que digan de qué va la página enlazada (nunca «aquí», «más información», «este artículo»):

- **Obligatorio — el servicio del tema**, dentro del texto donde venga a cuento (no solo en el cierre).
- **Obligatorio — 2-3 artículos anteriores del blog** relacionados, con la sintaxis `[ancla](articulo:slug)`, usando el `slug` del otro artículo. Solo artículos con fecha anterior. El sistema lo convierte en la URL real. (El primer artículo del blog no tiene a quién enlazar; el segundo, solo a uno.)
- **La página local** de la zona del tema si existe (tabla de arriba), con un ancla del tipo «jardinero en Calpe».
- **Un segundo servicio** relacionado si encaja de verdad.
- **WhatsApp** en el cierre, y opcionalmente la página de contacto.
- Máximo 9 enlaces distintos en total.

### Enlaces de vuelta (cada semana)

Cuando un artículo ya está publicado (su fecha ha pasado), se añade un enlace hacia él desde 1-2 artículos anteriores relacionados, en una frase donde encaje con naturalidad (no un bloque de «artículos relacionados»). Al guardar el cambio en el repo, el sistema actualiza esas entradas en WordPress. Nunca se enlaza a un artículo cuya fecha no ha llegado.

## Estructura

1. Respuesta directa (primer párrafo, 40-70 palabras).
2. 4-6 secciones `##` con `###` si hace falta.
3. `## Preguntas frecuentes`.
4. Cierre: un `##` corto (por ejemplo «¿Necesitas ayuda con…?») y 2-3 frases con llamada a la acción: escribir por WhatsApp o desde la página de contacto, con el enlace al servicio.

## Formato del archivo

Un archivo por artículo: `articulos/AAAA-MM-DD-<slug>.md`, en Markdown con esta cabecera:

```markdown
---
tema: poda-palmeras-invierno          # id de temas.json
fecha: "2026-11-10 09:00"             # martes o viernes, 09:00 hora de Madrid, entre comillas
titulo: "Poda de palmeras en Benissa: cuándo hacerla y cómo"   # máx. 70, con la keyword
slug: poda-palmeras-benissa
meta_titulo: "Poda de palmeras en Benissa: cuándo hacerla"     # máx. 60
meta_descripcion: "…"                 # 120-158 caracteres
keyword: poda de palmeras en Benissa  # la de temas.json
keywords_secundarias:
  - cuándo podar palmeras
  - poda de palmeras en invierno
  - cada cuánto se poda una palmera
extracto: "…"                          # 1-2 frases que respondan, no que anuncien
imagen_busqueda: palm tree pruning     # 2-4 palabras en inglés para Pexels
imagen_alt: "Palmera recién podada en un jardín mediterráneo"   # en español, describe la imagen
---

Respuesta directa…

## Primera sección
```

- 1.000-1.400 palabras de cuerpo (el validador acepta 900-1.800).
- Sin `#` (el título lo pone WordPress). Sin HTML ni imágenes. Tablas en formato Markdown.
- Comillas dobles en los valores de la cabecera que lleven «:» o comillas.

Antes de subir, `python scripts/validar.py` tiene que dar OK: comprueba longitudes, keyword en los sitios clave, respuesta directa, secciones, preguntas frecuentes, lista o tabla y enlaces.
