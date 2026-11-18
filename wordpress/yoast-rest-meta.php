<?php
/**
 * Plugin Name: Blog automático — Yoast, FAQ e idioma por REST
 * Description: Permite escribir desde la REST API el título SEO, la meta descripción y la keyword de Yoast, unos datos estructurados FAQPage que se imprimen en la cabecera de cada entrada, y el idioma de Polylang de la entrada (campo jfg_lang; las entradas en inglés van a la categoría «Gardening tips»).
 * Version: 3.0
 *
 * Instalación: subir este archivo a wp-content/mu-plugins/ (crear la carpeta si no existe). Se activa solo.
 */

if (!defined('ABSPATH')) {
    exit;
}

const JFG_CATEGORIA_EN = 'Gardening tips';
const JFG_CATEGORIA_EN_SLUG = 'gardening-tips';

add_action('init', function () {
    $keys = ['_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw', '_jfg_faq_schema'];
    foreach ($keys as $key) {
        register_post_meta('post', $key, [
            'show_in_rest'  => true,
            'single'        => true,
            'type'          => 'string',
            'auth_callback' => function () {
                return current_user_can('edit_posts');
            },
        ]);
    }
});

/**
 * Id de la categoría «Gardening tips» en inglés; la crea (y le pone el idioma inglés) si no existe.
 */
function jfg_categoria_en() {
    $terms = get_terms([
        'taxonomy'   => 'category',
        'slug'       => JFG_CATEGORIA_EN_SLUG,
        'hide_empty' => false,
        'lang'       => '', // sin el filtro de idioma de Polylang
    ]);
    if (!is_wp_error($terms) && !empty($terms)) {
        $term_id = (int) $terms[0]->term_id;
    } else {
        $nuevo = wp_insert_term(JFG_CATEGORIA_EN, 'category', ['slug' => JFG_CATEGORIA_EN_SLUG]);
        if (is_wp_error($nuevo)) {
            return $nuevo;
        }
        $term_id = (int) $nuevo['term_id'];
    }
    if (function_exists('pll_set_term_language') && function_exists('pll_get_term_language')
        && pll_get_term_language($term_id) !== 'en') {
        pll_set_term_language($term_id, 'en');
    }
    return $term_id;
}

// Idioma de la entrada (Polylang). Se escribe después de las categorías del REST, así que manda sobre ellas.
add_action('rest_api_init', function () {
    register_rest_field('post', 'jfg_lang', [
        'get_callback' => function ($post) {
            return function_exists('pll_get_post_language') ? (pll_get_post_language($post['id']) ?: null) : null;
        },
        'update_callback' => function ($value, $post) {
            if (!function_exists('pll_set_post_language')) {
                return new WP_Error('jfg_sin_polylang', 'Polylang no está activo: no se puede asignar el idioma.', ['status' => 500]);
            }
            if (!current_user_can('edit_post', $post->ID)) {
                return new WP_Error('jfg_sin_permiso', 'No puedes editar esta entrada.', ['status' => 403]);
            }
            $lang = sanitize_key($value);
            pll_set_post_language($post->ID, $lang);
            if ($lang === 'en') {
                $cat = jfg_categoria_en();
                if (is_wp_error($cat)) {
                    return $cat;
                }
                wp_set_post_categories($post->ID, [$cat], false);
            }
            return true;
        },
        'schema' => [
            'description' => 'Idioma de Polylang de la entrada (es, en).',
            'type'        => 'string',
            'enum'        => ['es', 'en'],
            'context'     => ['view', 'edit'],
        ],
    ]);
});

// Datos estructurados FAQPage de la entrada (generados por el blog automático)
add_action('wp_head', function () {
    if (!is_singular('post')) {
        return;
    }
    $json = get_post_meta(get_queried_object_id(), '_jfg_faq_schema', true);
    if (!$json) {
        return;
    }
    $data = json_decode($json, true);
    if (!is_array($data) || ($data['@type'] ?? '') !== 'FAQPage') {
        return;
    }
    echo "\n<script type=\"application/ld+json\">" . wp_json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "</script>\n";
}, 20);
