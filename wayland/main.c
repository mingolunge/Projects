#define _POSIX_C_SOURCE 200112L
#include <wayland-client.h>
#include <EGL/egl.h>
#include <GLES2/gl2.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "wlr-layer-shell-unstable-v1-client-protocol.h"

static struct wl_display *display;
static struct wl_compositor *compositor;
static struct zwlr_layer_shell_v1 *layer_shell;
static struct wl_surface *surface;
static struct zwlr_layer_surface_v1 *layer_surface;

static EGLDisplay egl_display;
static EGLContext egl_context;
static EGLSurface egl_surface;

static int configured = 0;

/* ---------- Wayland registry ---------- */

static void registry_add(void *data, struct wl_registry *reg,
                         uint32_t name, const char *iface, uint32_t ver)
{
    if (strcmp(iface, wl_compositor_interface.name) == 0) {
        compositor = wl_registry_bind(reg, name,
                                      &wl_compositor_interface, 4);
    } else if (strcmp(iface, zwlr_layer_shell_v1_interface.name) == 0) {
        layer_shell = wl_registry_bind(reg, name,
                                       &zwlr_layer_shell_v1_interface, 1);
    }
}

static void registry_remove(void *data, struct wl_registry *reg, uint32_t name) {}

static const struct wl_registry_listener registry_listener = {
    .global = registry_add,
    .global_remove = registry_remove,
};

/* ---------- Layer surface ---------- */

static void layer_configure(void *data,
                            struct zwlr_layer_surface_v1 *surf,
                            uint32_t serial,
                            uint32_t w, uint32_t h)
{
    zwlr_layer_surface_v1_ack_configure(surf, serial);
    configured = 1;
}

static void layer_closed(void *data,
                          struct zwlr_layer_surface_v1 *surf)
{
    wl_display_disconnect(display);
    exit(0);
}

static const struct zwlr_layer_surface_v1_listener layer_listener = {
    .configure = layer_configure,
    .closed = layer_closed,
};

/* ---------- EGL ---------- */

static void init_egl()
{
    egl_display = eglGetDisplay((EGLNativeDisplayType)display);
    eglInitialize(egl_display, NULL, NULL);

    EGLint cfg_attribs[] = {
        EGL_SURFACE_TYPE, EGL_WINDOW_BIT,
        EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,
        EGL_RED_SIZE, 8,
        EGL_GREEN_SIZE, 8,
        EGL_BLUE_SIZE, 8,
        EGL_ALPHA_SIZE, 8,
        EGL_NONE
    };

    EGLConfig cfg;
    EGLint count;
    eglChooseConfig(egl_display, cfg_attribs, &cfg, 1, &count);

    EGLint ctx_attribs[] = {
        EGL_CONTEXT_CLIENT_VERSION, 2,
        EGL_NONE
    };

    egl_context = eglCreateContext(egl_display, cfg,
                                   EGL_NO_CONTEXT, ctx_attribs);

    egl_surface = eglCreateWindowSurface(
        egl_display, cfg,
        (EGLNativeWindowType)surface, NULL);

    eglMakeCurrent(egl_display, egl_surface,
                   egl_surface, egl_context);
}

/* ---------- Rendering ---------- */

static void draw()
{
    glClearColor(0.0, 0.0, 0.0, 0.5); // transparent black
    glClear(GL_COLOR_BUFFER_BIT);
    eglSwapBuffers(egl_display, egl_surface);
}

/* ---------- Main ---------- */

int main()
{
    display = wl_display_connect(NULL);
    if (!display) return 1;

    struct wl_registry *registry = wl_display_get_registry(display);
    wl_registry_add_listener(registry, &registry_listener, NULL);
    wl_display_roundtrip(display);

    surface = wl_compositor_create_surface(compositor);

    layer_surface = zwlr_layer_shell_v1_get_layer_surface(
        layer_shell,
        surface,
        NULL,
        ZWLR_LAYER_SHELL_V1_LAYER_OVERLAY,
        "overlay"
    );

    zwlr_layer_surface_v1_set_anchor(
        layer_surface,
        ZWLR_LAYER_SURFACE_V1_ANCHOR_TOP |
        ZWLR_LAYER_SURFACE_V1_ANCHOR_BOTTOM |
        ZWLR_LAYER_SURFACE_V1_ANCHOR_LEFT |
        ZWLR_LAYER_SURFACE_V1_ANCHOR_RIGHT
    );

    zwlr_layer_surface_v1_set_size(layer_surface, 0, 0);
    zwlr_layer_surface_v1_add_listener(layer_surface,
                                       &layer_listener, NULL);

    wl_surface_commit(surface);

    init_egl();

    while (wl_display_dispatch(display)) {
        if (configured)
            draw();
    }

    return 0;
}
