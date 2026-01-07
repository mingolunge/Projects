#include "raylib.h"
#include "stdio.h"

int main(void)
{
    int screenWidth = 1920;
    int screenHeight = 1080;
    
   	SetConfigFlags(FLAG_WINDOW_TRANSPARENT);
   	SetConfigFlags(FLAG_WINDOW_RESIZABLE);

    InitWindow(screenWidth, screenHeight, "shaderWall");

    // Load shader (no vertex shader = raylib default)
    Shader shader = LoadShader(0, "/home/milo/Projects/shader/shader.frag");
    int timeLoc = GetShaderLocation(shader, "time");
    int resLoc  = GetShaderLocation(shader, "resolution");
    // int mouseLoc = GetShaderLocation(shader, "mouse");
    
    

    // Render texture to apply shader to
    RenderTexture2D target = LoadRenderTexture(screenWidth, screenHeight);

    SetTargetFPS(60);
	int i = 0;
    while (!WindowShouldClose())
    {
    	// if (i>100){
    	// 	UnloadShader(shader);
   	 //    	shader = LoadShader(0, "shader.frag");
   	 //    	i = 0;
    	// }
    	i++;
    	float t = GetTime();
    	SetShaderValue(shader, timeLoc, &t, SHADER_UNIFORM_FLOAT);
    	
    	Vector2 res = { (float)screenWidth, (float)screenHeight };
    	SetShaderValue(shader, resLoc, &res, SHADER_UNIFORM_VEC2);

		
        // Draw scene to texture
        BeginTextureMode(target);
            ClearBackground(BLANK);
        EndTextureMode();

        // Draw texture with shader
        BeginDrawing();
            ClearBackground(BLANK);
            BeginShaderMode(shader);
                // NOTE: RenderTexture is flipped vertically
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
