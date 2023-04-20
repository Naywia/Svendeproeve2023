#include <M5Stack.h>

class Numpad
{
public:
    // Numpad and text-length
    // char keymap[2][4][10] = {{{'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'}, {'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '~'}, {'^', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', '<'}, {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}}, {{'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'}, {'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '~'}, {'^', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ' ', '<'}, {'<', '>', ',', '.', '-', '_', '+', '*', '/', '\\'}}};
    char keymap[2][6] = {
        {'0', '1', '2', '3', '4', '<'},
        {'5', '6', '7', '8', '9', '~'}};
    int csel = 0;
    int rsel = 0;
    int textLength = 0;

    // Keeping track of stuff
    bool showNumpad = false;
    bool deletingSecondKeystring = false;

#define KEYSTRING_BUFFER_SIZE (31)
    char keystring[KEYSTRING_BUFFER_SIZE];
    // Keystring length including string terminator
#define KEYSTRINGS_BUFFER_SIZE (17)
    char firstKeystring[KEYSTRINGS_BUFFER_SIZE];
    char secondKeystring[KEYSTRINGS_BUFFER_SIZE];

    char *start()
    {
        // Setup
        M5.Lcd.drawRect(0, 208, 106, 32, BLUE);
        M5.Lcd.drawRect(106, 208, 107, 32, BLUE);
        M5.Lcd.drawRect(213, 208, 106, 32, BLUE);
        M5.Lcd.drawString("Kolonne", 30, 215, 2); // Default first num 80
        M5.Lcd.drawString("Vaelg", 143, 215, 2);  // Default first num 80
        M5.Lcd.drawString("Raekke", 245, 215, 2); // Default first num 80

        // Pre-fill keystrings with null terminator
        memset(keystring, 0x00, 31);
        memset(secondKeystring, 0x00, 17);
        memset(firstKeystring, 0x00, 17);

        // During startup, update button-clicks to avoid clicking a button on the numpad
        if (!showNumpad)
        {
            delay(1);
            M5.update();
            showNumpad = true;
        }

        // Set cursor and update text and numpad
        firstKeystring[0] = '|';
        updateText();
        firstKeystring[0] = 0x00;
        updateNumpad();

        // Numpad while loop
        while (showNumpad)
        {
            if (M5.BtnA.wasPressed())
            {
                csel = csel + 1;
                if (csel > 5)
                {
                    csel = 0;
                }
                updateNumpad();
            }

            if (M5.BtnC.wasPressed())
            {
                rsel = rsel + 1;
                if (rsel > 1)
                {
                    rsel = 0;
                }
                updateNumpad();
            }

            if (M5.BtnB.wasPressed())
            {
                // Cursor pipe index
                int cursorPipe;

                if ((rsel == 1) && (csel == 5))
                {
                    // RETURN / ENTER
                    M5.Lcd.clear();
                    mergeKeystrings();
                    showNumpad = false;
                }
                else if ((rsel == 0) && (csel == 5))
                {
                    // Backspace
                    if (textLength > 0)
                    {
                        // If more than 15 characters have been typed in
                        if (strlen(secondKeystring) > 0)
                        {
                            cursorPipe = strlen(secondKeystring) - 1;
                        }
                        else
                        // If less than 15 characters have been typed in
                        {
                            // If  the second row was just removed
                            if (strlen(secondKeystring) == 0)
                            {
                                deletingSecondKeystring = true;
                            }
                            cursorPipe = strlen(firstKeystring) - 1;
                        }
                    }
                    else
                    {
                        cursorPipe = textLength;
                    }
                }
                else
                {
                    // Max input is 30 characters
                    if (textLength < 30)
                    {
                        // If less than 15 characters have been typed in
                        if (strlen(firstKeystring) < 15)
                        {
                            firstKeystring[strlen(firstKeystring)] = keymap[rsel][csel];

                            // If exactly 15 characters have been typed in
                            if (strlen(firstKeystring) == 15)
                            {
                                cursorPipe = 0;
                            }
                            else
                            {
                                cursorPipe = strlen(firstKeystring);
                            }
                        }
                        // If more than 15 characters have been typed in
                        else
                        {
                            secondKeystring[strlen(secondKeystring)] = keymap[rsel][csel];
                            cursorPipe = strlen(secondKeystring);
                        }
                    }
                }

                // Insert cursorPipe and update text
                // If  the second row was just removed
                if (deletingSecondKeystring)
                {
                    firstKeystring[cursorPipe] = '|';
                    updateText();
                    firstKeystring[cursorPipe] = 0x00;
                }
                else
                {
                    if (textLength >= 14)
                    {
                        secondKeystring[cursorPipe] = '|';
                        updateText();
                        secondKeystring[cursorPipe] = 0x00;
                    }
                    else
                    {
                        firstKeystring[cursorPipe] = '|';
                        updateText();
                        firstKeystring[cursorPipe] = 0x00;
                    }
                }
                // TextLength is calculated
                textLength = strlen(firstKeystring) + strlen(secondKeystring);
            }
            delay(1);
            M5.update();
        }

        return keystring;
    }

    void mergeKeystrings()
    {
        int j, i;
        for (i = 0; i < strlen(firstKeystring); i++)
        {
            keystring[i] = firstKeystring[i];
        }

        for (j = 0; j < strlen(secondKeystring); j++)
        {
            keystring[i] = secondKeystring[j];
            i++;
        }
    }

    void updateText()
    {
        int indent = 40;
        int firstTextY = 18;
        int secondTextY = 48;
        int fontSize = 4;

        // Write the updated text on the screen
        if (showNumpad)
        {
            M5.Lcd.fillRect(0, 18, 320, 60, BLACK); // Clear text

            // Create pointer to char array "firstKeystring" or "secondKeystring"
            // Write new text
            // If secondKeystring was just deleted
            if (deletingSecondKeystring)
            {
                deletingSecondKeystring = false;
                char *firstText = firstKeystring;
                M5.Lcd.drawString(firstText, indent, secondTextY, fontSize);
            }
            else
            {
                // "More than or equal to" half the length of the text
                if (textLength >= 14)
                {
                    char *firstText = firstKeystring;
                    M5.Lcd.drawString(firstText, indent, firstTextY, fontSize);

                    char *secondText = secondKeystring;
                    M5.Lcd.drawString(secondText, indent, secondTextY, fontSize);
                }
                else
                {
                    char *firstText = firstKeystring;
                    M5.Lcd.drawString(firstText, indent, secondTextY, fontSize);
                }
            }
        }
    }

    void updateNumpad()
    {
        // M5.Speaker.tone(561, 40); // Speaker sound every time you move around on the numpad
        int x, y;
        M5.Lcd.fillRect(0, 128, 320, 72, BLACK); // Clear the numpad, so it can be re-drawn
        for (int r = 0; r < 2; r++)
        {
            for (int c = 0; c < 6; c++)
            {
                x = (c * 40 + 40); // x coordinates for where to start drawing numpad
                y = (128 + (r * 40)); // y coordinates for where to start drawing numpad
                // Drawing squares
                if ((csel == c) && (rsel == r))
                {
                    // If the square being drawn is currently selected
                    M5.Lcd.setTextColor(TFT_BLACK, TFT_WHITE);
                    M5.Lcd.fillRect(x, y, 32, 32, WHITE);
                }
                else
                {
                    // Otherwise draw a blue square
                    M5.Lcd.drawRect(x, y, 32, 32, BLUE);
                }

                // Drawing symbols inside squares
                if ((r == 1) && (c == 5))
                {
                    // ENTER / RETURN
                    M5.Lcd.drawString("<-'", x + 10, y + 7, 2);
                }
                else if ((r == 0) && (c == 5))
                {
                    // Backspace
                    M5.Lcd.drawString("<-", x + 10, y + 7, 2);
                }
                else
                {
                    // Show any other part of the numpad on the display
                    M5.Lcd.drawString(String(keymap[r][c]), x + 12, y + 7, 2);
                }
                M5.Lcd.setTextColor(TFT_WHITE, TFT_BLACK);
            }
        }
    }
};