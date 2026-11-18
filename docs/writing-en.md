# Writing guide for the English blog

This guide overrides any other idea the writer may have. Nobody reviews the articles before they are scheduled in WordPress: write them as if they were final. Every article must be optimised for Google (SEO) and for being quoted by ChatGPT, Perplexity, Gemini and Google's AI answers (GEO), and linked to the rest of the site.

The English blog is smaller than the Spanish one: **one article every other Thursday at 09:00 (Madrid time)**, starting on Thursday 3 December 2026 (3 Dec, 17 Dec, 31 Dec, 14 Jan…). It is not a translation of the Spanish blog: it has its own topics (`temas_en.json`) and only links to English pages and English articles.

## The company

**Jardinería Francisco Gómez**, a gardening company based in Benissa (Alicante). It works across the Marina Alta: Benissa, Calpe, Moraira, Teulada, Altea and Xaló. It has been working in the area for more than 30 years. **It does not do swimming pool maintenance.**

### Pages you may link to (there are no others)

| Key | Page | URL |
|---|---|---|
| comunidades | Community garden maintenance | https://jardineriafranciscogomez.com/en/servicio/community-garden-maintenance/ |
| jardines | Garden maintenance | https://jardineriafranciscogomez.com/en/servicio/garden-maintenance/ |
| construccion | Garden design and landscaping | https://jardineriafranciscogomez.com/en/servicio/garden-design-and-landscaping/ |
| poda | Tree and palm pruning | https://jardineriafranciscogomez.com/en/servicio/tree-and-palm-pruning/ |
| picudo | Red palm weevil treatment | https://jardineriafranciscogomez.com/en/servicio/red-palm-weevil-treatment/ |
| riego | Irrigation installation | https://jardineriafranciscogomez.com/en/servicio/irrigation-installation/ |
| parcelas | Land clearing | https://jardineriafranciscogomez.com/en/servicio/land-clearing/ |
| (Benissa) | Home: gardener in Benissa | https://jardineriafranciscogomez.com/en/ |
| (Calpe) | Gardener in Calpe | https://jardineriafranciscogomez.com/en/gardener-calpe/ |
| (Moraira) | Gardener in Moraira | https://jardineriafranciscogomez.com/en/gardener-moraira/ |
| | All services | https://jardineriafranciscogomez.com/en/services/ |
| | About us | https://jardineriafranciscogomez.com/en/about-us/ |
| | Projects | https://jardineriafranciscogomez.com/en/projects/ |
| | Contact | https://jardineriafranciscogomez.com/en/contact/ |
| | WhatsApp | https://wa.me/34616779874 |

Teulada has no page of its own: in its articles link the Moraira page (Moraira is part of the municipality of Teulada) or the home page. Altea and Xaló link the home page.

Never link to Spanish pages (without `/en/`) or to Spanish articles.

## Audience

Foreign residents and second-home owners in the Marina Alta: British, Irish, Dutch, Scandinavian, German and other Europeans who read in English. Many own a villa with a garden and palms, spend part of the year away, live in an urbanisation with shared gardens, or have bought a property with a plot. They want to know what to do with their garden and when, what is different about gardening in a Mediterranean climate compared with home, and whether it is worth calling a professional.

Things that help this reader: explaining local terms the first time (urbanisation, *comunidad de propietarios*, *ayuntamiento*/town hall, *picudo rojo*), comparing with a northern European garden when it is useful ("unlike in the UK, the growing season here is autumn to spring"), and thinking about absent owners (timers, what to leave done before leaving, what can wait).

## Tone

- British English spelling and vocabulary (colour, organise, metre, autumn, garden centre, hosepipe ban). Dates as "3 December".
- Friendly and practical, like an experienced gardener explaining things clearly. Address the reader as "you".
- Short sentences. No filler ("in today's world", "it is important to note", "without a doubt", "in conclusion", "when it comes to").
- No exaggerated marketing language or absolute promises. No emojis.
- Also say when you do NOT need a professional: it builds trust.

## Forbidden

- Inventing company facts: years of experience, number of clients, prices, reviews, awards, staff names, projects, clients or specific cases, or describing "how we do it" with details that are not in this guide.
- Giving prices or rates.
- Giving doses or brand names of plant protection products: recommend that a licensed professional applies them.
- Inventing regulations: for burning, fire prevention or local bylaws do not give dates, deadlines or fines; explain the general idea and refer the reader to the town hall (*ayuntamiento*).
- Quoting studies, statistics or percentages.
- External links (to other websites): none.
- Repeating the topic, angle or main keyword of an article already written in English (check every file in `articulos/en/`).
- Presenting pools as a company service: Jardinería Francisco Gómez does not maintain or clean swimming pools. A pool can be mentioned as part of the garden ("don't plant a tree right next to the pool"), never offered as a service.
- Using as the main keyword a service name plus a town, or a hiring search ("gardener in Moraira", "palm tree pruning Calpe", "community garden maintenance", "red palm weevil treatment", "land clearing", "irrigation installation", "garden landscaping"). Those searches belong to the service pages; if the blog uses them, it competes with them. The blog targets informational searches: "when…", "how…", "what…", "signs…", "how often…".

## SEO

- **One main keyword** (the one in `temas_en.json`) and **2-6 secondary keywords**: variants and real related questions people type into Google. Use the secondary ones naturally in the text and in some `##`.
- The main keyword goes, without forcing it, into: `titulo`, `meta_titulo` (starting with it if it reads well), `slug`, `meta_descripcion`, the first paragraph and at least one `##`. The validator checks that every word of three letters or more of the keyword appears in the title, the meta description, the first 100 words and some `##`.
- `meta_titulo`: max. 60 characters. It may end in "| Jardinería Francisco Gómez" if it fits.
- `meta_descripcion`: 120-158 characters, with the keyword, the benefit and a reason to click.
- `slug`: 2-5 words in English, with no unnecessary articles or prepositions.
- The `##` headings answer the real questions for that search (Google's "People also ask" and related searches), in the order the reader would ask them. Preferably as a question or with the answer in the heading itself.

## GEO (getting quoted by AI)

1. **Direct answer first**: the first paragraph, 40-70 words, answers the title's question on its own, with the specific fact or criterion (when, how often, which signs). It is the paragraph an AI would copy. No heading before it.
2. **Self-contained sections**: the first sentence after each `##` answers that heading without depending on the rest; nuances come after.
3. **Explicit definitions** the first time a concept appears: "The red palm weevil is…", "Xeriscaping is…".
4. **Concrete facts instead of adjectives**: months, frequencies, heights, visible signs. Without inventing figures.
5. **At least one numbered list (steps) or a table** (comparison, calendar, stages). AIs extract them very well.
6. **Clear entities**: name "Jardinería Francisco Gómez" once and the area with its province ("Moraira (Alicante)", "the Marina Alta", "the Costa Blanca") naturally.
7. **Frequently asked questions**: `## Frequently asked questions` with 3-5 `###` questions ending in "?", different from the `##` headings, taken from real searches. Answers of 2-4 sentences that stand on their own. They are also published as FAQPage structured data.

## Internal links

Use descriptive anchors that say what the linked page is about (never "here", "click here", "read more", "this article", "more information"):

- **Required — the service for the topic** (`/en/servicio/…`), inside the text where it fits (not only in the closing section).
- **Required — 2-3 earlier English articles** on related topics, using the syntax `[anchor](articulo:slug)` with the other article's `slug`. Only articles with an earlier date and only English articles. The system turns it into the real URL (`/en/<slug>/`). (The first English article has nothing to link to; the second, only one.)
- **The local page** for the topic's area if there is one (table above), with an anchor such as "gardener in Calpe".
- **A second service** if it is genuinely related.
- **WhatsApp** in the closing section, and optionally the contact page.
- Maximum 9 different links in total.

### Backlinks (each time a new article goes out)

When an English article has been published (its date has passed), add a link to it from 1-2 earlier related English articles, in a sentence where it fits naturally (not a "related articles" block). When the change is saved in the repo, the system updates those posts in WordPress. Never link to an article whose date has not arrived yet.

## Areas

Spread the articles across Benissa, Calpe, Moraira, Teulada, Altea and Xaló (the `zona` field in `temas_en.json`). Moraira and Calpe have the largest English-speaking communities: name the town in the text when the article is about its area and link its local page.

## Featured image

Every post has a featured image. If there is no Pexels key or no photo is found, the publisher uses a real company photo according to the topic's service (see `FOTOS_PROPIAS` in `scripts/publicar.py`).

## Structure

1. Direct answer (first paragraph, 40-70 words).
2. 4-6 `##` sections, with `###` if needed.
3. `## Frequently asked questions`.
4. Closing: a short `##` (for example "Need a hand with…?") and 2-3 sentences with a call to action: message us on WhatsApp or through the contact page, with the link to the service.

## File format

One file per article: `articulos/en/YYYY-MM-DD-<slug>.md`, in Markdown with this header (field names stay in Spanish; values in English):

```markdown
---
tema: away-winter-garden               # id from temas_en.json
idioma: en
fecha: "2026-12-03 09:00"              # a Thursday, every other week from 3 Dec 2026, 09:00 Madrid time, in quotes
titulo: "…"                            # max. 70, with the keyword
slug: away-winter-garden
meta_titulo: "…"                       # max. 60
meta_descripcion: "…"                  # 120-158 characters
keyword: looking after your garden when you're away for the winter   # the one in temas_en.json
keywords_secundarias:
  - …
  - …
extracto: "…"                          # 1-2 sentences that answer, not announce
imagen_busqueda: mediterranean garden winter   # 2-4 words in English for Pexels
imagen_alt: "…"                        # in English, describes the image
---

Direct answer…

## First section
```

- 1,000-1,400 words of body text (the validator accepts 900-1,800).
- No `#` (WordPress adds the title). No HTML or images. Tables in Markdown.
- Double quotes around header values that contain ":" or quotes (and the apostrophe in "you're" is fine inside double quotes).

Before pushing, `python scripts/validar.py` must say OK: it checks lengths, the keyword in the key places, the direct answer, sections, FAQ, list or table, links, that the date is a Thursday and that `articulo:` links point to English articles only.
