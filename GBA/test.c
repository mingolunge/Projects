#include "stdio.h"
#include "/opt/devkitpro/libtonc/include/tonc.h"

#define SCREEN_WIDTH = 240
#define SCREEN_HEIGHT = 160

typedef struct {
	int x;
	int y;
} Player;

int main() {
    // Initialize the hardware
    REG_DISPCNT = DCNT_MODE3 | DCNT_BG2;

    // Initialize the player character
    Player player;
player.x = SCREEN_WIDTH / 2;
player.y = SCREEN_HEIGHT - 16;

while (1) {
        // Clear the screen
        m3_fill(RGB15(0, 0, 0));

        // Read input
key_poll();
if (key_is_down(KEY_LEFT) &&player.x> 0) {
player.x--;
        }
if (key_is_down(KEY_RIGHT) &&player.x< SCREEN_WIDTH - 16) {
player.x++;
        }

        // Draw the player character
        m3_rect(player.x, player.y, 16, 16, RGB15(31, 0, 0));

        // Wait for VBlank
vid_vsync();
    }

return 0;
}	
