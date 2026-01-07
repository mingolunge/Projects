#include "raylib.h"
#include "stdio.h"

int main(void)
{
    bool panning = false;
    Vector2 offset = {0};
    Vector2 zoom = {1.0f, 1.0f};
    bool dragging = false;
    Vector2 co = {0};
    Vector2 prevMouse = {0};

    Vector2 center = {0.0f, 0.0f};

    int screenWidth = 1920;
    int screenHeight = 1080;

    SetConfigFlags(FLAG_WINDOW_TRANSPARENT);
    SetConfigFlags(FLAG_WINDOW_RESIZABLE);

    InitWindow(screenWidth, screenHeight, "Fractals");

    Shader shader = LoadShader(0, "shader.frag");
    int timeLoc = GetShaderLocation(shader, "time");
    int resLoc  = GetShaderLocation(shader, "resolution");
    int mouseLoc = GetShaderLocation(shader, "mouse");
    int zoomLoc = GetShaderLocation(shader, "zoom");
    int coLoc = GetShaderLocation(shader, "co");
    int offsetLoc = GetShaderLocation(shader, "offset");

    RenderTexture2D target = LoadRenderTexture(screenWidth, screenHeight);

    SetTargetFPS(60);
    int i = 0;

    while (!WindowShouldClose())
    {
        screenWidth = GetScreenWidth();
        screenHeight = GetScreenHeight();

        if (i > 100) {
            UnloadShader(shader);
            shader = LoadShader(0, "shader.frag");
            i = 0;
        }
        i++;

        Vector2 mouse = GetMousePosition();
        SetShaderValue(shader, mouseLoc, &mouse, SHADER_UNIFORM_VEC2);

        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            prevMouse = mouse;
            dragging = true;
        }

        if (dragging) {
            Vector2 delta = { mouse.x - prevMouse.x, mouse.y - prevMouse.y };
            co.x -= delta.x * zoom.x / 1000.0f;
            co.y += delta.y * zoom.y / 1000.0f;
            prevMouse = mouse;
        }

        if (IsMouseButtonReleased(MOUSE_BUTTON_LEFT)) {
            dragging = false;
        }

        SetShaderValue(shader, coLoc, &co, SHADER_UNIFORM_VEC2);

        if (IsMouseButtonPressed(MOUSE_BUTTON_RIGHT)) {
            panning = true;
            prevMouse = mouse;
        }

        if (panning && IsMouseButtonDown(MOUSE_BUTTON_RIGHT)) {
            Vector2 delta = { mouse.x - prevMouse.x, mouse.y - prevMouse.y };
            offset.x -= delta.x * zoom.x / 300;
            offset.y += delta.y * zoom.y / 300;
            prevMouse = mouse;
        }

        if (IsMouseButtonReleased(MOUSE_BUTTON_RIGHT)) {
            panning = false;
        }

        float wheel = GetMouseWheelMove();
        if (wheel != 0.0f)
        {
            float factor = (wheel > 0.0f) ? 0.9f : 1.1f;

            Vector2 res = { (float)screenWidth, (float)screenHeight };
            Vector2 uv = {
                mouse.x / res.x - 0.5f,
                mouse.y / res.y - 0.5f
            };
            uv.x *= res.x / res.y;

            Vector2 before = {
                uv.x * zoom.x + offset.x,
                uv.y * zoom.y + offset.y
            };

            zoom.x *= factor;
            zoom.y *= factor;

            Vector2 after = {
                uv.x * zoom.x + offset.x,
                uv.y * zoom.y + offset.y
            };

            offset.x += (before.x - after.x) * 3.0f;
            offset.y -= (before.y - after.y) * 3.0f;
        }

        // 🔥 INFINITE ZOOM REBASE (THIS IS THE FIX)
        if (zoom.x < 1e-6f) {
            center.x += offset.x * zoom.x;
            center.y += offset.y * zoom.y;
            offset = (Vector2){0, 0};
            zoom = (Vector2){1.0f, 1.0f};
        }

        SetShaderValue(shader, zoomLoc, &zoom, SHADER_UNIFORM_VEC2);
        SetShaderValue(shader, offsetLoc, &offset, SHADER_UNIFORM_VEC2);

        float t = GetTime();
        SetShaderValue(shader, timeLoc, &t, SHADER_UNIFORM_FLOAT);

        Vector2 res = { (float)screenWidth, (float)screenHeight };
        SetShaderValue(shader, resLoc, &res, SHADER_UNIFORM_VEC2);

        BeginTextureMode(target);
            ClearBackground(BLANK);
        EndTextureMode();

        BeginDrawing();
            ClearBackground(BLANK);
            BeginShaderMode(shader);
                DrawTextureRec(
                    target.texture,
                    (Rectangle){ 0, 0, (float)screenWidth, -(float)screenHeight },
                    (Vector2){ 0, 0 },
                    WHITE
                );
            EndShaderMode();
        EndDrawing();
    }

    UnloadRenderTexture(target);
    UnloadShader(shader);
    CloseWindow();
    return 0;
}
