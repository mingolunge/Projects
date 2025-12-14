#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "raylib.h"

float dx = 0;
float dy = 0;

// Gradient function with offsets
unsigned char function(int x, int y, int screenWidth, int noise){
    int val = -(int)(0.01*(x - screenWidth / 2 + dx)*y + dy - noise * 5);
    if(val < 0) val = 0;
    if(val > 255) val = 255;
    return (unsigned char)val;
}

int main(void)
{
    int screenWidth = 1920;
    int screenHeight = 1080;

    SetConfigFlags(FLAG_WINDOW_TRANSPARENT);
    InitWindow(screenWidth, screenHeight, "gradient + noise");
    SetTargetFPS(30);

    // Initialize random
    srand(time(NULL));

    // Create texture
    Image img = GenImageColor(screenWidth, screenHeight, BLANK);
    Texture2D texture = LoadTextureFromImage(img);
    UnloadImage(img);

    // Allocate pixel buffer once for speed
    Color *pixels = (Color *)malloc(screenWidth * screenHeight * sizeof(Color));

    while (!WindowShouldClose())
    {
        Vector2 mousePos = GetMousePosition();
        // Controls
        if (IsKeyDown(KEY_Q)) CloseWindow();
		dx = -mousePos.x / 40;
		dy = mousePos.y / 20 - 150;
        // Update pixels with noise
        for (int iy = 0; iy < screenHeight; iy++){
            for (int ix = 0; ix < screenWidth; ix++){
                int noise = rand() % 15 - 10; // noise range [-10,10]
                unsigned char c = function(ix, iy, screenWidth, noise);
                pixels[iy * screenWidth + ix] = (Color){c, c, c, 100};
            }
        }
        UpdateTexture(texture, pixels);

        // Draw
        BeginDrawing();
            ClearBackground(BLANK);
            DrawTexture(texture, 0, 0, WHITE);
        EndDrawing();
    }

    free(pixels);
    UnloadTexture(texture);
    CloseWindow();
    return 0;
}
