<?php
/**
 * Plugin Name: Blog automático — Yoast y FAQ por REST
 * Description: Permite escribir desde la REST API el título SEO, la meta descripción y la keyword de Yoast, y unos datos estructurados FAQPage que se imprimen en la cabecera de cada entrada.
 * Version: 2.0
 *
 * Instalación: subir este archivo a wp-content/mu-plugins/ (crear la carpeta si no existe). Se activa solo.
 */

if (!defined('ABSPATH')) {
    exit;
}

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
