
import time
from setup import *
import random
class Game:
    def __init__(self):
        self.slimeframe = 0
        self.slime_y = 20
        self.slimestate = "idle"
        self.slime_x = 48
        self.slime_spd = 1
        self.slime_flip = moveframes
        self.slime_timer = time.ticks_ms()
        self.slime_timer_num = random.randint(5000, 20000)
        self.food_visible = False
        self.food_x = self.slime_x+22
        self.food_y = 39
        self.btn_a_condition = True
        self.btn_b_condition = True
        self.hunger = 10
        self.health = 20 
        self.fun = 0
        self.timehunger = time.ticks_ms()
        self.timefun = time.ticks_ms()
        self.run = True
        self.sel_tab = 0
        self.coins = 100
        self.sel_item = 0
        self.sel_market_item = None
        self.market = {"apple":{"price": 5, "description": "+5 hunger +1 fun"},
                "bread": {"price": 10, "description": "+10 hunger"},
                "medkit": {"price": 20, "description": "+10 health"}}
        self.all_bodyparts = {
                            "eyes":[
                                    {"name" : "stalk eyes", 
                                     "type" : 0, 
                                     "sprite normal":(stalk_eye_fb, stalk_eye_flip_fb), 
                                     "sprite angry":(stalk_eye_angry_fb, stalk_eye_angry_flip_fb), 
                                     "transparency": 0,
                                     "offset": 13 },
                                    {"name" : "standard  eyes", 
                                     "type" : 1, 
                                     "sprite normal":(eye_standard_fb, eye_standard_fb), 
                                     "sprite angry":(eye_standard_angry_fb, eye_standard_angry_flip_fb), 
                                     "transparency": 1,
                                     "offset": 5  }],
                            "arms":[
                                   {"name": "crab amrs", "type" : 1, "sprite normal" : crab_arm_fb}]}
        self.my_bodyparts = []
        self.inv = ["apple", "bread","apple", "bread"]
        self.sel_market_item = None
        self.slimeframe = 0
        self.timewalk = time.ticks_ms()
        self.max_width=128
        self.state = "normal"
        self.now = time.ticks_ms()
        self.eaten_food = None
        self.btn_left_condition = True
        self.btn_right_condition = True
        self.not_hungry_randomnum = 0
        self.angrytimer = time.ticks_ms() -20000
        self.cooldown = False
        self.growth = 20
        self.growtimer = time.ticks_ms()
        self.main_state = 0
    def draw_pet(self, oled, anim, x, y):
        if anim == "idle":
            frames = idleframes
        elif anim == "move":
            frames = moveframes
        elif anim == "move_flip":
            frames = moveframes
        elif anim == "angry":
            frames = angryframes
        elif anim == "eat":
            frames = eatframes
        else:
            frames = idleframes
        self.slimeframe = self.slimeframe % len(frames)
        oled.blit(frames[self.slimeframe], x, y, 0)
        for i in self.my_bodyparts:
            off = offsets[anim][i["type"]]
            if self.slimeframe >= len(off):
                continue
            ox = off[self.slimeframe][0]
            oy = off[self.slimeframe][1]
            if anim == "angry":
                oled.blit(i["sprite angry"][1],x+ox,y+oy,i["transparency"])
                oled.blit(i["sprite angry"][0],x+ox+i["offset"],y+oy,i["transparency"])
            else:
                oled.blit(i["sprite normal"][1],x+ox,y+oy,0)
                oled.blit(i["sprite normal"][0],x+ox+i["offset"],y+oy,0)             
    def draw_text_block(self, oled, text, x, y):
        max_chars = (self.max_width - x) // 8  # 8px per character
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
    def display_bodyparts(self,type,oled):
        oled.rect(48,16,80,32,1)
        for i, part in enumerate(self.all_bodyparts[type]):
            x = 49 + 16*i
            y = 17
            oled.blit(part["sprite normal"][0], x, y)
           #  if i == self.sel_bodypart:
                #oled.rect()
    def bar(self, x, var,oled):
        for i in range(var-1):
            oled.pixel(x + i, 59, 1)
            oled.pixel(x + i, 60, 1)
            oled.pixel(x + i, 61, 1)
            oled.pixel(x + i, 62, 1)
    def draw_menu(self, list, oled, x,y, width , height, distance_x  = 12, distance_y = 12):
        width = width - (width % distance_x)
        height = height - (height % distance_y)
        rows = width // distance_x
        for i in range(0, len(list)):
            item = list[i]
            if item == "apple":
                item = apple_fb
            elif item == "bread":
                item = bread_fb
            elif item == "medkit":
                item = medkit_fb
            item_x = x + (i % rows) * distance_x
            item_y = y + (i // rows) * distance_y
            oled.blit(item, item_x, item_y)
            if i == self.sel_item:
                oled.rect(item_x, item_y, distance_x, distance_y, 1)
            oled.rect(x, y, width, height, 1)
    def draw(self, oled):
        oled.fill(0)
        for i in range(0, 2):
            if self.sel_tab == i:
                oled.rect(i*16, 0, 16,16, 1)
        self.bar(13, self.health,oled)
        oled.rect(44, 58, 20, 6, 1)
        self.bar(45, self.fun,oled)
        oled.rect(76, 58, 20, 6, 1)
        self.bar(77, self.growth, oled)
        oled.rect(108, 58, 20, 6, 1)
        self.bar(109, self.hunger,oled)
        oled.blit(heart_fb, 0, 52,0)
        oled.blit(face_fb, 32, 52,0)
        oled.blit(arrow_fb, 64, 52,0)
        oled.blit(apple_fb, 96, 53,0)
        oled.rect(12, 58, 20, 6, 1)
        if self.main_state == 0:
            if self.cooldown:
                oled.blit(lock_fb, 1,1)
            else:
                oled.blit(apple_fb, 1,1)
            oled.blit(basket_fb, 17,1)
        elif self.main_state == 1:
            oled.blit(eye_fb, 1,1)
            self.draw_pet(oled, "idle",16,16)
        if self.state == "evolution":
            pass
        if self.state == "eyes" or self.state == "arms":
            body_list = list()
            for i, part in enumerate(self.all_bodyparts[self.state]):
                body_list.append(part["sprite normal"][0])
            self.draw_menu(body_list, oled, 48,16,80,32)
        if self.state == "normal":
            self.draw_pet(oled, self.slimestate,self.slime_x,self.slime_y)
        if self.state == "market":
            oled.text("coins: " + str(self.coins), 1, 37, 1)
            keys = list(self.marketp.keys())
            self.draw_menu(keys, oled, 0,16,128,38)
        if self.state == "description":
            oled.rect(0,16,128,38,1)
            oled.text("coins: " + str(self.coins), 1, 37, 1)
            if self.sel_market_item is not None:

                keys = list(self.market.keys())
                for i in range(0, len(keys)):
                    item = keys[i]
                    if item == self.sel_market_item:
                        self.draw_text_block(oled, self.market[item]["description"], 1, 17)
        if self.state == "feed":
            self.draw_menu(self.inv, oled, 0,16,128,38)
        if self.food_visible:
            if self.eaten_food == "apple":
                oled.blit(apple_fb, self.food_x, self.food_y,0)
            elif self.eaten_food == "bread":
                oled.blit(bread_fb, self.food_x, self.food_y,0)
            elif self.eaten_food == "medkit":
                oled.blit(medkit_fb, self.food_x, self.food_y,0)
        oled.show()


    def btn_handling(self):
        self.now = time.ticks_ms()
        if time.ticks_diff(self.now, self.timefun)>10000:
            self.fun -= 1
            self.timefun = self.now
        self.hunger = max(0, min(20, self.hunger))
        self.fun = max(0, min(20, self.fun))
        self.health = max(0, min(20, self.health))
        self.growth =  max(0, min(20, self.growth))
        if self.health == 0:
            self.run = False
        if btn_a.value() == 1:
            self.btn_a_condition = True 
        if btn_b.value() == 1:
            self.btn_b_condition = True
        if btn_left.value() == 1:
            self.btn_left_condition = True
        if btn_right.value() == 1:
            self.btn_right_condition = True

        # --A BUTTON--
        if self.btn_a_condition and btn_a.value() == 0:
            if self.state == "normal":
                if self.sel_tab == 0:
                    if not self.cooldown:
                        self.state = "feed"
                if self.sel_tab == 1:
                    self.state = "market"
            elif self.state == "feed":
                self.slimestate = "eat"
                self.food_x = self.slime_x + 22
                self.slimeframe = 0
                
                if not self.cooldown:
                    chance_to_succeed = self.fun * 5
                    if random.randint(1, 100) <= chance_to_succeed:
                        pass
                    else:
                        self.slimestate = "angry"
                        self.angrytimer = self.now
                        return
                else:
                    self.slimestate = "angry"
                    return
                if self.sel_food is not None:
                    if self.sel_food == "apple":
                        self.eaten_food = "apple"
                        self.hunger += 5
                        self.fun += 1
                    elif self.sel_food == "bread":
                        self.eaten_food = "bread"
                        self.hunger += 10
                    elif self.sel_food == "medkit":
                        self.eaten_food = "medkit"
                        self.health += 10
                    self.inv.pop(self.sel_item)
                    if self.sel_item >= len(self.inv):
                        self.sel_item = 0
            elif self.state == "market":
                self.state = "description"
            elif self.state == "description":
                if self.sel_market_item is not None:
                    if not self.coins < self.market[self.sel_market_item]["price"]:
                        self.coins -= self.market[self.sel_market_item]["price"]
                        self.inv.append(self.sel_market_item)
            elif self.state == "evolution":
                if self.sel_tab == 0:
                    self.state = "eyes"
                elif self.sel_tab == 1:
                    self.state = "arms"
            elif self.state == "eyes":
                self.my_bodyparts.append(self.all_bodyparts["eyes"][0])
            self.btn_a_condition = False


        # --B BUTTON--
        if self.btn_b_condition and btn_b.value() == 0:
            if self.state == "feed" or self.state == "market":
                self.state = "normal"
            elif self.state == "description":
                self.state = "market"
            elif self.state == "eyes" or self.state == "arms":
                self.state = "evolution"
            elif self.state == "evolution":
                self.state = "normal"
                self.main_state = 0
                self.growth = 0
                self.my_bodyparts.append(self.all_bodyparts["eyes"][1])
            self.btn_b_condition = False


        # --LEFT BUTTON--
        if self.btn_left_condition and btn_left.value() == 0:
            if self.state == "normal" or self.state == "evolution":
                self.sel_tab += 1
                if self.sel_tab > 1: 
                    self.sel_tab = 0
            if self.state == "market" or self.state == "feed" or self.state == "eyes" or self.state == "arms":
                self.sel_item = (self.sel_item+1) % len(list(self.market.keys()))
            self.btn_left_condition = False


        # --RIGHT BUTTON--
        if self.btn_right_condition and btn_right.value() == 0:
            if self.state == "normal "or self.state == "evolution":
                self.sel_tab -= 1
                if self.sel_tab < 0:
                    self.sel_tab = 1 
            if self.state == "market" or self.state == "feed":
                self.sel_item = (self.sel_item-1) % len(list(self.market.keys()))
            self.btn_right_condition = False


    def game_logic(self):
        self.now = time.ticks_ms()
        if time.ticks_diff(self.now, self.angrytimer) > 10000:
            self.cooldown = False
        else:
            self.cooldown = True


        if time.ticks_diff(self.now, self.growtimer) > 1000000:
            self.growth += 1
            self.growtimer = self.now 
        if len(self.inv) == 0:
            self.sel_food = None
            self.sel_item = 0
        else:
            self.sel_item = self.sel_item % len(self.inv)
            self.sel_food = self.inv[self.sel_item]
        if len(self.market) == 0:
            self.sel_market_item = None
            self.sel_item = 0
        else:
            self.sel_item = self.sel_item % len(self.market)
            self.sel_market_item = list(self.market.keys())[self.sel_item]
        if self.growth == 20 and self.main_state == 0:
            self.main_state = 1
            self.state = "evolution"
        if time.ticks_diff(self.now, self.timehunger)>5000:
            if self.hunger == 0:
                self.health -= 1
            else:
                self.hunger -= 1
            self.timehunger = self.now
            # slime animation and movement
        # ----- state switching every 10 seconds -----
        if time.ticks_diff(self.now, self.slime_timer) > self.slime_timer_num:
            if self.slimestate == "idle":
                self.slimestate = "move"
            else:
                self.slimestate = "idle"
            self.slime_timer = self.now
            self.slimeframe = 0  
            self.slime_timer_num = random.randint(5000, 20000)
        # ----- animate every loop -----
        if self.slimestate == "idle":
            self.slimeframe = move_sel_left(self.slimeframe, idleframes)

        elif self.slimestate == "move" or self.slimestate == "move_flip":
            self.slimeframe = move_sel_left(self.slimeframe, moveframes)
            self.slime_x += self.slime_spd

            if self.slime_x > 96:
                self.slimestate = "move_flip"
                self.slime_spd = -1

            if self.slime_x < 0:
                self.slimestate = "move"
                self.slime_spd = 1
        elif self.slimestate == "eat":
            self.state = "normal"
            self.slimeframe += 1
            self.food_visible = True
            if self.slimeframe > 9:
                self.food_x -= 1
            if self.slimeframe >= len(eatframes):
                self.slimestate = "idle"
                self.slimeframe = 0
                self.food_visible = False
            else:
                pass
        elif self.slimestate == "angry":
            self.state = "normal"
            self.slimeframe += 1
            if self.slimeframe >= len(angryframes):
                self.slimestate = "idle"
                self.slimeframe = 0
            else:
                pass



        


def move_sel_left(var, item_list):
    var = (var+1) % len(item_list)
    return var

def move_sel_right(var, item_list):
    var = (var-1) % len(item_list)
    return var
game = Game()
while game.run:
    game.game_logic()
    game.btn_handling()
    game.draw(oled)
    time.sleep_ms(50) 
name = "1234567890ß!§$%&/()=?"
if not game.run:
    oled.fill(0)
    oled.text(name + "died",0,0)
    oled.show()