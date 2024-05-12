
#include "raylib.h"

#include "./data.h"

// uhctf{slyvdiaxgbwmnrkeozqjp}
static const char alfabet[] = {
    12, // a
    15, // b
    2,  // c
    10, // d
    21, // e
    4,  // f
    14, // g
    1,  // h
    11, // i
    25, // j
    20, // k
    7,  // l
    17, // m
    18, // n
    22, // o
    26, // p
    24, // q
    19, // r
    6,  // s
    3,  // t
    0,  // u
    9,  // v
    16, // w
    13, // x
    8,  // y
    23, // z
};

int main(int argc, char const *argv[])
{
    // Initialization
    //--------------------------------------------------------------------------------------
    const int screenWidth = 800;
    const int screenHeight = 450;

    InitWindow(screenWidth, screenHeight, "screen");

    int ImWidth = 280;
    int ImHeight = 22;

    int letterWidth = ImWidth / 28;
    int letterHeight = ImHeight;

    Image img;

    img.data = ImageData;
    img.width = ImWidth;
    img.height = ImHeight;
    img.format = PIXELFORMAT_UNCOMPRESSED_R8G8B8;
    img.mipmaps = 1;

    Texture2D texture = LoadTextureFromImage(img);

    Rectangle src = {0, 0, ImWidth, ImHeight};
    Rectangle dst = {0, 0, 800, 450};
    Vector2 org = {0, 0};

    char text[] = "im sure    the flag is in       here";
    int textLen = 37;

    int rots[] = {-3, 0, 3, -3, 0, 3, -3, 0, 3, -3, 0, 3, -3, 0, 3,-3, 0, 3,-3, 0, 3,-3, 0, 3,-3, 0, 3,-3, 0, 3,-3, 0, 3,-3, 0, 3,-3};

    SetTargetFPS(60); // Set our game to run at 60 frames-per-second
    //--------------------------------------------------------------------------------------

    // Main game loop
    while (!WindowShouldClose()) // Detect window close button or ESC key
    {
        // Update
        //----------------------------------------------------------------------------------
        // TODO: Update your variables here
        //----------------------------------------------------------------------------------

        // Draw
        //----------------------------------------------------------------------------------
        BeginDrawing();

        ClearBackground(LIGHTGRAY);

        Rectangle let_src = {0, 0, ImWidth, ImHeight};
        Rectangle let_dst = {0, 0, 80, 100};
        Vector2 let_org = {0, 0};

        for (int i = 0; i < textLen - 1; i++)
        {
            char let = text[i];
            float rot = rots[i];
            if (let != ' ')
            {
                int index = alfabet[('a' - let) * -1];

                let_src.x = letterWidth * index;
                let_src.width = letterWidth;

                DrawTexturePro(texture, let_src, let_dst, let_org, rot, WHITE);
            }

            let_org.x -= 80;
            if (let_org.x <= screenWidth * -1)
            {
                let_org.x = 0;
                let_org.y -= 100;
            }
        }

        // DrawTexturePro(texture, src, dst, org, 0, WHITE);

        EndDrawing();
        //----------------------------------------------------------------------------------
    }

    // De-Initialization
    //--------------------------------------------------------------------------------------
    CloseWindow(); // Close window and OpenGL context
    //--------------------------------------------------------------------------------------

    return 0;
}
