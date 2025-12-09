#include "raylib.h"
#include "math.h"


float distance;
Vector2 dir;

typedef struct{
    Vector2 pos;
    Vector2 vel;
    float m;
    float r;
} Planet;

Planet get_vector(Planet a, Planet b){
	dir.x = b.pos.x - a.pos.x;
	dir.y = b.pos.y - a.pos.y;

	distance = sqrtf(dir.x*dir.x + dir.y*dir.y);

	Vector2 dir_norm = { dir.x / distance, dir.y / distance };
	a.vel.x += dir_norm.x * a.m * GetFrameTime();
	a.vel.y += dir_norm.y * a.m * GetFrameTime();
	a.pos.x += a.vel.x * GetFrameTime();
	a.pos.y += a.vel.y * GetFrameTime();
	return a;
}

int main(void)
{
    int screenWidth = 1280;//GetScreenWidth();
    int screenHeight = 720;//GetScreenHeight();
    //SetConfigFlags(FLAG_WINDOW_RESIZABLE);
	SetConfigFlags(FLAG_WINDOW_TRANSPARENT);
    InitWindow(screenWidth, screenHeight, "gravity sim");
    SetTargetFPS(30);
    /////////////////////////////////////////////////////////////////////////////////
    
	Planet c = {{600, 600}, {0,100}, 500, 50};
    Planet a = {{200, 50}, {100, -40}, 350, 35};
    Planet b = {{500, 300}, {10,20}, 400, 40};

    bool dragging = false;

    while (!WindowShouldClose())
    {
    	if (IsKeyDown(KEY_Q)){
    		CloseWindow();
    	}
    	screenWidth = 1280;//GetScreenWidth();
    	screenHeight = 720;//GetScreenHeight();
    	Vector2 mousePos = GetMousePosition();
    	if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)){
    		dragging = true;
    	}

    	if (dragging){
    		b.pos.x = mousePos.x;
    		b.pos.y = mousePos.y;
    		b.vel.x = 0;
    		b.vel.y = 0;
    	}

    	if (IsMouseButtonReleased(MOUSE_BUTTON_LEFT)){
    		dragging = false;
    	}

		a = get_vector(a, b);
		a = get_vector(a, c);
		b = get_vector(b, a);
		b = get_vector(b, c);
		c = get_vector(c, b);
		c = get_vector(c, a);

        // --- DRAW ---
        BeginDrawing();
            ClearBackground(BLANK);
            DrawCircleGradient(a.pos.x, a.pos.y, a.r, GREEN, BLANK);
            DrawCircleGradient(b.pos.x, b.pos.y, b.r, RED, BLANK);
            DrawCircleGradient(c.pos.x, c.pos.y, c.r, PURPLE, BLANK);
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
