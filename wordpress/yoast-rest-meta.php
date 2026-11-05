<?php
/**
 * Plugin Name: Yoast meta por REST
 * Description: Permite escribir el título SEO, la meta descripción y la keyword de Yoast desde la REST API (blog automático).
 *
 * Dos formas de instalarlo:
 *  - Como mu-plugin: subir este archivo a wp-content/mu-plugins/
 *  - Con el plugin Code Snippets: nuevo snippet PHP con el bloque add_action de abajo, "Ejecutar en todas partes", activar.
 */

add_action('init', function () {
    foreach (['_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw'] as $key) {
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
