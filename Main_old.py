from setup import *
import random
def draw_text_block(oled, text, x, y):
    max_chars = (max_width - x) // 8  # 8px per character
    words = text.split(" ")
    
    line = ""
    line_num = 0
    
    for word in words:
        if len(line) + len(word) + 1 <= max_chars:
            if line:
                line += " "
            line += word
        else:
            oled.text(line, x, y + line_num * 10, 1)
            line = word
            line_num += 1
    
    if line:
        oled.text(line, x, y + line_num * 10, 1)

def bar(x, var):
    for i in range(var-1):
        oled.pixel(x + i, 59, 1)
        oled.pixel(x + i, 60, 1)
        oled.pixel(x + i, 61, 1)
        oled.pixel(x + i, 62, 1)
def update():
    oled.fill(0)
    #add the icons and bars
    bar(13, health)
    oled.rect(44, 58, 20, 6, 1)
    bar(45, fun)
    oled.rect(76, 58, 20, 6, 1)
    oled.rect(108, 58, 20, 6, 1)
    bar(109, hunger)
    oled.blit(heart_fb, 0, 52,0)
    oled.blit(face_fb, 32, 52,0)
    oled.blit(arrow_fb, 64, 52,0)
    oled.blit(apple_fb, 96, 53,0)
    oled.rect(12, 58, 20, 6, 1)
    #add the top row of tabs
    oled.blit(apple_fb, 1, 1)
    oled.blit(basket_fb, 17, 1)
    for i in range(0, 2):
        if sel_tab == i:
            oled.rect(i*16, 0, 16,16, 1)
    if state == "normal":
        if slimestate == "idle":
            oled.blit(idleframes[slimeframe], slime_x, slime_y)
        elif slimestate == "move":  
            oled.blit(slime_flip[slimeframe], slime_x, slime_y)
        elif slimestate == "eat":
            oled.blit(eatframes[slimeframe], slime_x, slime_y)  
    if state == "market":
        oled.rect(0,16,128,38,1)
        oled.text("coins: " + str(coins), 1, 37, 1)
        keys = list(market.keys())   
        for i in range(0, len(keys)):
            item = keys[i]          
            if item == "apple":
                oled.blit(apple_fb, 1 + (i % 7) * 32, 17 + (i // 7) * 32)
                oled.text(str(market[item]["price"]), 17 + (i % 7) * 32, 17 + (i // 7) * 32)
            if item == "bread":
                oled.blit(bread_fb, 1 + (i % 7) * 32, 17 + (i // 7) * 32)
                oled.text(str(market[item]["price"]), 17 + (i % 7) * 32, 17 + (i // 7) * 32)
            if item == "medkit":
                oled.blit(medkit_fb, 1 + (i % 7) * 32, 17 + (i // 7) * 32)
                oled.text(str(market[item]["price"]), 17 + (i % 7) * 32, 17 + (i // 7) * 32)
            if i == sel_market_num:
                oled.rect(1 + (i % 7) * 32, 17 + (i // 7) * 32, 12, 12, 1)
                oled.rect(1 + (i % 7) * 32, 17 + (i // 7) * 32, 12, 12, 1)
    if state == "description":
        oled.rect(0,16,128,38,1)
        oled.text("coins: " + str(coins), 1, 37, 1)
        if sel_market_item is not None:
            keys = list(market.keys())
            for i in range(0, len(keys)):
                item = keys[i]
                if item == sel_market_item:
                    draw_text_block(oled, market[item]["description"], 1, 17)
    if state == "feed":
        oled.rect(0,16,128,38,1)
        for i in range(0, int(len(inv))):
            if inv[i] == "apple":
                oled.blit(apple_fb, 1 + (i % 7) * 16, 17 + (i // 7) * 16)
            if inv[i] == "bread":
                oled.blit(bread_fb, 1 + (i % 7) * 16, 17 + (i // 7) * 16)
            if inv[i] == "medkit":
                oled.blit(medkit_fb, 1 + (i % 7) * 16, 17 + (i // 7) * 16)
            if i == sel_food_num:
                oled.rect(1 + (i % 7) * 16, 17 + (i // 7) * 16, 12, 12, 1)
    if food_visible:
        if eaten_food == "apple":
            oled.blit(apple_fb, food_x, food_y,0)
        elif eaten_food == "bread":
            oled.blit(bread_fb, food_x, food_y,0)
        elif eaten_food == "medkit":
            oled.blit(medkit_fb, food_x, food_y,0)
    oled.show()
update()


def move_sel_left(var, item_list):
    var += 1
    if var >= len(item_list):
        var = 0
    return var

def move_sel_right(var, item_list):
    var -= 1
    if var < 0:
        var = len(item_list) - 1
    return var

while run:
    oldhunger = hunger
    oldhealth = health
    oldfun = fun
    oldstate = state
    oldsel_food_num = sel_food_num
    oldsel_tab = sel_tab
    now = time.ticks_ms()
    oldcoins = coins
    oldselmarket_num = sel_market_num
    oldsel_market_item = sel_market_item
    oldslimeframe = slimeframe
    oldslimestate = slimestate
    oldslime_x = slime_x
    oldinv_len = len(inv)
    oldslime_y = slime_y
    oldfood_visible = food_visible
    oldfood_x = food_x
    oldfood_y = food_y
    # update the selected food and market item
    if len(inv) == 0:
        sel_food = None
        sel_food_num = 0
    else:
        sel_food_num = sel_food_num % len(inv)
        sel_food = inv[sel_food_num]
    if len(market) == 0:
        sel_market_item = None
        sel_market_num = 0
    else:
        sel_market_num = sel_market_num % len(market)
        sel_market_item = list(market.keys())[sel_market_num]
    if time.ticks_diff(now, timehunger)>5000:
        if hunger == 0:
            health -= 1
        else:
            hunger -= 1
        timehunger = now

        # slime animation and movement
    # ----- state switching every 10 seconds -----
    if time.ticks_diff(now, slime_timer) > slime_timer_num:
        if slimestate == "idle":
            slimestate = "move"
        else:
            slimestate = "idle"
        slime_timer = now
        slimeframe = 0  
        slime_timer_num = random.randint(5000, 20000)
    # ----- animate every loop -----
    if slimestate == "idle":
        slimeframe = move_sel_left(slimeframe, idleframes)

    elif slimestate == "move":
        slimeframe = move_sel_left(slimeframe, moveframes)
        slime_x += slime_spd

        if slime_x > 96:
            slime_flip = moveframes_flipped
            slime_spd = -1

        if slime_x < 0:
            slime_flip = moveframes
            slime_spd = 1
    elif slimestate == "eat":
        state = "normal"
        slimeframe += 1
        food_visible = True
        if slimeframe > 9:
            food_x -= 1
        if slimeframe >= len(eatframes):
            slimestate = "idle"
            slimeframe = 0
            food_visible = False
        else:
            pass
    elif slimestate == "angry":
        state = "normal"
        slimeframe += 1
        if slimeframe >= len(angryframes):
            slimestate = "idle"
            slimeframe = 0
        else:
            pass

    # button handlings
    if time.ticks_diff(now, timefun)>10000:
        fun -= 1
        timefun = now
    hunger = max(0, min(20, hunger))
    fun = max(0, min(20, fun))
    health = max(0, min(20, health))
    if health == 0:
        run = False
    if btn_a.value() == 1:
        btn_a_condition = True 
    if btn_b.value() == 1:
        btn_b_condition = True
    if btn_left.value() == 1:
        btn_left_condition = True
    if btn_right.value() == 1:
        btn_right_condition = True
    if btn_a_condition and btn_a.value() == 0:
        if state == "normal":
            if sel_tab == 0:
                state = "feed"
            if sel_tab == 1:
                state = "market"
        elif state == "feed":
            slimestate = "eat"
            food_x = slime_x+22
            slimeframe = 0
            if is_hungry:
                if sel_food is not None:
                    if sel_food == "apple":
                        eaten_food = "apple"
                        hunger += 5
                        fun += 1
                    elif sel_food == "bread":
                        eaten_food = "bread"
                        hunger += 10
                    elif sel_food == "medkit":
                        eaten_food = "medkit"
                        health += 10
                    inv.pop(sel_food_num)
                    if sel_food_num >= len(inv):
                        sel_food_num = 0
            else:
                slimestate = "angry"
        elif state == "market":
            state = "description"
        elif state == "description":
            if sel_market_item is not None:
                if not coins < market[sel_market_item]["price"]:
                    coins -= market[sel_market_item]["price"]
                    inv.append(sel_market_item)
        btn_a_condition = False
    if btn_b_condition and btn_b.value() == 0:
        if state != "normal":
            state = "normal"
        btn_b_condition = False
    if btn_left_condition and btn_left.value() == 0:
        if state == "normal":
            sel_tab += 1
            if sel_tab > 1: 
                sel_tab = 0
        if state == "feed":
            sel_food_num = move_sel_left(sel_food_num, inv)
        if state == "market":
            sel_market_num = move_sel_left(sel_market_num, market)
        btn_left_condition = False
    if btn_right_condition and btn_right.value() == 0:
        if state == "normal":
            sel_tab -= 1
            if sel_tab < 0:
                sel_tab = 1 
        if state == "feed":
            sel_food_num = move_sel_right(sel_food_num, inv)
        if state == "market":
            sel_market_num = move_sel_right(sel_market_num, market)
        btn_right_condition = False
    if (
        oldhunger != hunger or
        oldhealth != health or
        oldfun != fun or
        oldsel_food_num != sel_food_num or
        oldsel_tab != sel_tab or
        oldselmarket_num != sel_market_num or
        oldcoins != coins or
        oldsel_market_item != sel_market_item or
        oldslimeframe != slimeframe or
        oldslimestate != slimestate or
        oldslime_x != slime_x or
        oldslime_y != slime_y or
        oldfood_visible != food_visible or
        oldfood_x != food_x or
        oldfood_y != food_y or
        oldinv_len != len(inv) or
        oldstate != state
    ):
        update()
    time.sleep_ms(50) 

if not run:
    oled.fill(0)
    oled.text("you died",0,0)
    oled.show()