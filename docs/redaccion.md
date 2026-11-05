# Guía de redacción del blog

Esta guía manda sobre cualquier otra idea del redactor. Nadie revisa los artículos antes de que se programen en WordPress: se escriben como si fueran definitivos.

## La empresa

**Jardinería Francisco Gómez**, empresa de jardinería de Benissa (Alicante). Trabaja en la Marina Alta: Benissa, Calpe, Moraira y Teulada.

Servicios (cada uno con su página, para el enlace interno):

| Clave en temas.json | Servicio | URL |
|---|---|---|
| comunidades | Mantenimiento de comunidades | https://jardineriafranciscogomez.com/servicio/mantenimiento-de-comunidades/ |
| jardines-piscinas | Mantenimiento de jardines y piscinas | https://jardineriafranciscogomez.com/servicio/mantenimiento-de-jardines-y-piscinas/ |
| construccion | Construcción de jardines con rocallas, fuentes y césped | https://jardineriafranciscogomez.com/servicio/construccin-de-jardines-con-rocallas-fuentes-cesped/ |
| poda | Poda de árboles y palmeras | https://jardineriafranciscogomez.com/servicio/poda-de-arboles-y-palmeras/ |
| picudo | Tratamiento del picudo rojo | https://jardineriafranciscogomez.com/servicio/tratamiento-del-picudo/ |
| riego | Instalación de sistemas de riego | https://jardineriafranciscogomez.com/servicio/instalacion-de-sistemas-de-riego/ |
| parcelas | Limpieza de parcelas | https://jardineriafranciscogomez.com/servicio/limpieza-de-parcelas/ |

Otras páginas: contacto https://jardineriafranciscogomez.com/contacto/ · servicios https://jardineriafranciscogomez.com/servicios/

WhatsApp: https://wa.me/34616779874 (teléfono 616 77 98 74).

## Público

Propietarios de chalets y casas de la costa (muchos con segunda residencia o residentes extranjeros que leen en español), administradores de fincas y presidentes de comunidades. Quieren saber qué hacer con su jardín y cuándo, y si les conviene llamar a un profesional.

## Tono

- Español de España, cercano y práctico, como un jardinero con oficio que explica las cosas claras. Tuteo.
- Frases cortas. Nada de relleno («en el mundo actual», «es importante destacar», «sin lugar a dudas», «en conclusión»).
- Nada de lenguaje de marketing exagerado ni promesas absolutas. Sin emojis.

## Contenido

- Consejos adaptados al clima de la Marina Alta: veranos secos y calurosos, inviernos suaves, levante, suelos calcáreos, agua escasa y con mucha cal.
- Que encajen con la estación de la fecha de publicación.
- La zona del tema se menciona de forma natural 1-3 veces, sin listas forzadas de pueblos.
- Información útil de verdad: cuándo hacerlo, cómo detectar un problema, errores habituales, qué puede hacer uno mismo y cuándo conviene un profesional.

## Prohibido

- Inventar datos de la empresa: años de experiencia, número de clientes, precios, valoraciones, premios, nombres de trabajadores, proyectos o clientes concretos.
- Dar precios o tarifas.
- Dar dosis o nombres comerciales de productos fitosanitarios: se recomienda que los aplique un profesional autorizado.
- Inventar normativa: sobre quemas, prevención de incendios u ordenanzas no se dan fechas, plazos ni multas; se explica la idea general y se remite al ayuntamiento.
- Citar estudios o estadísticas.
- Repetir el tema, el enfoque o la keyword principal de un artículo ya escrito (mira todos los de `articulos/`).

## Estructura

1. Introducción de 2-3 frases que responda directamente a la pregunta del título (la que copiaría Google o una IA). Sin encabezado.
2. 4-6 secciones `##`, con `###` si hace falta. Listas cuando ayuden. La keyword en al menos un `##`.
3. `## Preguntas frecuentes` con 3-4 preguntas en `###` y respuestas de 2-4 frases que se entiendan solas.
4. Cierre (sin encabezado o con un `##` corto) de 2-3 frases con llamada a la acción: escribir por [WhatsApp](https://wa.me/34616779874) o en la página de contacto, con enlace al servicio relacionado.

## Formato del archivo

Un archivo por artículo: `articulos/AAAA-MM-DD-<slug>.md`, en Markdown con esta cabecera:

```markdown
---
tema: poda-palmeras-invierno          # id de temas.json
fecha: "2026-11-10 09:00"             # martes o viernes, 09:00, hora de Madrid (entre comillas)
titulo: "Cuándo podar las palmeras en Benissa"        # máx. 70, con la keyword
slug: cuando-podar-palmeras                           # 2-6 palabras, sin tildes
meta_titulo: "Cuándo podar palmeras | Jardinería Francisco Gómez"   # máx. 60
meta_descripcion: "…"                 # 120-160 caracteres, keyword + motivo para hacer clic
keyword: poda de palmeras en Benissa  # la de temas.json
extracto: "…"                          # 1-2 frases que respondan, no que anuncien
imagen_busqueda: palm tree pruning     # 2-4 palabras en inglés para Pexels
imagen_alt: "Jardinero podando una palmera"           # en español
---

Introducción…

## Primera sección
```

- 900-1.300 palabras de cuerpo (el validador acepta 800-1.700).
- Sin `#` (el título lo pone WordPress). Sin HTML, sin imágenes, sin tablas salvo que aporten mucho.
- Enlaces en Markdown con URL completa y ancla descriptiva (nunca «aquí»). Obligatorio: el servicio del tema y el WhatsApp. Como mucho 3 enlaces internos además del WhatsApp.
- Comillas dobles en los valores de la cabecera que lleven «:» o comillas.

Antes de subir, `python scripts/validar.py` tiene que dar OK.
