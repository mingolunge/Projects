#include <stdio.h>
#include <stdlib.h>
#include <json-c/json.h>

#define WORKSPACES_CMD "hyprctl -j workspaces"
#define ACTIVE_CMD "hyprctl activeworkspace -j"

int main(void) {
    // Get current workspace
    FILE *fp = popen(ACTIVE_CMD, "r");

	json_object_put
	
    if (found)
        printf("Current workspace %d is not empty.\n", current_workspace);
    else {
        printf("Current workspace %d is empty.\n", current_workspace);
        popen("pkill -SIGUSR1 waybar", "r");
	}
    json_object_put(workspaces_json);
    return 0;
}
