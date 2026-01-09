#include "raylib.h"
#include "stdio.h"

int main(void)
{
    int screenWidth = 1280;//GetScreenWidth();
    int screenHeight = 720;//GetScreenHeight();
    //SetConfigFlags(FLAG_WINDOW_RESIZABLE);
	SetConfigFlags(FLAG_WINDOW_TRANSPARENT);
    InitWindow(screenWidth, screenHeight, "pong");
    SetTargetFPS(60);
    bool up;
    bool down;
    /////////////////////////////////////////////////////////////////////////////////
    struct Ball {
    	Vector2 pos;
    	float r;
    	Vector2 d;
    }; 
    Vector2	player = {10, 500};
	struct Ball ball = {{screenWidth/2, screenHeight/2}, 30, {-5, 5}};
    while (!WindowShouldClose())
    {
    	screenWidth = GetScreenWidth();
    	screenHeight = GetScreenHeight();
    	if (IsKeyPressed(KEY_W)){
    		up = true;
    	}
    	if (IsKeyReleased(KEY_W)){
    		up = false;
    	}
    	if (IsKeyPressed(KEY_S)){
    		down = true;
    	}
    	if (IsKeyReleased(KEY_S)){
    		down = false;
    	}

		if (IsKeyPressed(KEY_R)){
			ball.pos.x = screenWidth/2;
			ball.pos.y = screenHeight/2;
			ball.d.x = -5;
			ball.d.y = 5;
		}

    	if (up){
    		player.y -= 6;
    	}

    	if (down) {
    		player.y += 6;
    	}

		ball.pos.x = ball.pos.x + ball.d.x;
		ball.pos.y = ball.pos.y + ball.d.y;

		if (ball.pos.x + ball.r <= player.x + 10 && ball.pos.y + ball.r > player.y && ball.pos.y + ball.r < player.y + 60) {
			ball.d.x = -ball.d.x;
		}
		if (ball.pos.y + ball.r < 0 || ball.pos.y > screenHeight) {
			ball.d.y = -ball.d.y ;
		}
		
    	
        BeginDrawing();
            ClearBackground(BLANK);
            DrawRectangle(player.x, player.y, 10, 60, WHITE);
            DrawCircle(ball.pos.x, ball.pos.y, ball.r, WHITE);
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
