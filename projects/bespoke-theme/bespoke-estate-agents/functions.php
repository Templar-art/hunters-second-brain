<?php
/**
 * Bespoke Estate Agents theme functions.
 */
if (!defined('ABSPATH')) exit;

/** Live media base (assets uploaded to the WP media library). */
define('BEA_UP', 'https://bespoke.agents.10xvisuals.co/wp-content/uploads/2026/07');

/** Brand asset URLs, one place to change them. */
function bea_asset($file) { return BEA_UP . '/' . $file; }

function bea_setup() {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array('search-form', 'gallery', 'caption', 'style', 'script'));
    register_nav_menus(array('primary' => __('Primary Menu', 'bespoke')));
}
add_action('after_setup_theme', 'bea_setup');

function bea_assets() {
    $v = wp_get_theme()->get('Version');
    wp_enqueue_style('bea-main', get_stylesheet_uri(), array(), $v);
    wp_enqueue_script('bea-site', get_template_directory_uri() . '/assets/js/site.js', array(), $v, true);
}
add_action('wp_enqueue_scripts', 'bea_assets');

/** Favicon (from the live media library). */
function bea_favicon() {
    echo '<link rel="icon" type="image/png" href="' . esc_url(bea_asset('favicon.png')) . '">' . "\n";
}
add_action('wp_head', 'bea_favicon');

/**
 * Output a run of numbered gallery images in EXACT order, e.g. cairngorm-01..19.
 * $extra is an optional list of full filenames appended after the numbered run
 * (used for boulevard-location.jpg).
 */
function bea_gallery($prefix, $count, $extra = array()) {
    $out = '';
    for ($i = 1; $i <= $count; $i++) {
        $n = sprintf('%02d', $i);
        $url = bea_asset($prefix . '-' . $n . '.jpg');
        $out .= '<img src="' . esc_url($url) . '" alt="' . esc_attr(ucfirst($prefix) . ' photo ' . $i) . '" loading="lazy">' . "\n";
    }
    foreach ($extra as $file) {
        $out .= '<img src="' . esc_url(bea_asset($file)) . '" alt="' . esc_attr($prefix . ' location') . '" loading="lazy">' . "\n";
    }
    return $out;
}

/** Is this the given page slug? (for nav highlighting) */
function bea_is($slug) { return is_page($slug); }

/**
 * On activation: create the 6 pages, set the static front page, and build the
 * primary menu. Safe to run repeatedly (skips anything that already exists).
 */
function bea_provision() {
    $pages = array(
        'home'          => 'Home',
        'about'         => 'About',
        'services'      => 'Services',
        'sold-listings' => 'Sold Listings',
        'projects'      => 'Projects',
        'contact'       => 'Contact',
    );
    $ids = array();
    foreach ($pages as $slug => $title) {
        $existing = get_page_by_path($slug);
        if ($existing) { $ids[$slug] = $existing->ID; continue; }
        $ids[$slug] = wp_insert_post(array(
            'post_title'   => $title,
            'post_name'    => $slug,
            'post_status'  => 'publish',
            'post_type'    => 'page',
            'post_content' => '',
        ));
    }

    if (!empty($ids['home'])) {
        update_option('show_on_front', 'page');
        update_option('page_on_front', $ids['home']);
    }

    // Build the primary menu if it does not exist yet.
    $menu_name = 'Bespoke Primary';
    if (!wp_get_nav_menu_object($menu_name)) {
        $menu_id = wp_create_nav_menu($menu_name);
        foreach (array('home', 'about', 'services', 'sold-listings', 'projects', 'contact') as $slug) {
            if (empty($ids[$slug])) continue;
            wp_update_nav_menu_item($menu_id, 0, array(
                'menu-item-title'     => $pages[$slug],
                'menu-item-object'    => 'page',
                'menu-item-object-id' => $ids[$slug],
                'menu-item-type'      => 'post_type',
                'menu-item-status'    => 'publish',
            ));
        }
        $locations = get_theme_mod('nav_menu_locations', array());
        $locations['primary'] = $menu_id;
        set_theme_mod('nav_menu_locations', $locations);
    }
}
add_action('after_switch_theme', 'bea_provision');
