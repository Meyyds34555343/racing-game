# Importing all libraries
import time
import pygame, sys
from button import Button

# Importing data base
import sqlite3 as sq

db = sq.connect("database.db")

# Create a table if not created
try:
    st = """
        CREATE TABLE num
        (id TEXT)
        """
    
    # Putting zero value if table is not created
    db.execute(st)
    insert = "INSERT INTO num(id) VALUES ('{}')".format(1)
    db.execute(insert)
    db.commit()

except:
    pass

# Taking value from database
fetc = """SELECT id FROM num"""
data = db.execute(fetc)
img_counter = 0

# Getting value 
for row in data:
    img_counter = ''.join(row)

# Convert it into integer and put in limit variable
limit = int(img_counter)

# Initializing fonts
pygame.init()

# WIDTH and HEIGHT of window
WIDTH,HEIGHT = 900,600

# Initializing window
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

#Caption of window
pygame.display.set_caption("Menu")

pygame.mixer.init()

# Importing images
BG = pygame.image.load("assets/Background.jpg")
BG = pygame.transform.scale(BG,(WIDTH,HEIGHT+100))

garage = pygame.image.load("assets/garage.jpg")
garage = pygame.transform.scale(garage,(WIDTH,HEIGHT))

BG_r = pygame.image.load("assets/BG_r.jpg")
BG_r= pygame.transform.scale(BG_r,(WIDTH,HEIGHT))

car = pygame.image.load("assets/car_sk1.png")
car= pygame.transform.scale(car,(200,170))

rally = pygame.image.load("assets/rally_sk.png")
rally= pygame.transform.scale(rally,(190,100))

tire_ahead = pygame.image.load("assets/tire.png")
tire_ahead= pygame.transform.scale(tire_ahead,(260,167))

meter = pygame.image.load("assets/tachometer.png")
meter= pygame.transform.scale(meter,(210,210))

meter_stick = pygame.image.load("assets/meter_stick.png")
meter_stick = pygame.transform.scale(meter_stick,(20,150))


Finish = pygame.image.load("assets/Finish.png")
Finish = pygame.transform.scale(Finish,(150,150))
# Imporing fonts and size
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


# Play function
def play():

    # Limit is globalised to be manipulated(Limit indicates level as well)
    global limit

    # x1 is the inital road placement
    x1 = 0

    # Speed of road
    speed = 3

    # placement of car
    x_move = 100

    # placement of opponent car
    x_move2 = 120

    # The wheel angle as it is turning every second
    wheel_angle = 0

    # Car's y axis to make car move slightly up and down to make it more natural
    car_Y_move = 430

    # Initial placement of meter
    meter_turn = 0

    # Meter turning speed 
    meter_speed = 0.2

    # How fast wheels look
    wheel_speed = 3

    # Wheels speed for opponent
    wheel_angle2 = 0
    wheel_speed2 = 3

    # Initial gear
    gears = 0

    # This one indicates previous gear
    inititial_gear = 0

    #Sound
    sound = pygame.mixer.Sound('Assets/accelerate.mp3')
    raw_array = sound.get_raw()

    # Cutting the sound
    raw_array = raw_array[100000:250000]
    cut_sound = pygame.mixer.Sound(buffer=raw_array)

    # THis indicates opponent speed
    inc_of_op = 0

    # Change speed is used to make it false when user wins or loses
    change_speed2 = True

    # This indicates how fast opponent will get each time
    x_r = -0.1

    # This indicates the sound cut
    arr1 = 100000
    arr2  = 400000
    cut_sound.play(-1)

    # opponents gear
    op_gear = 0
    
    # How long the race will be
    meters = 500

    # Finish meter simply checks when we are about to win
    Finish_meter = 900

    # This indicates milliseconds to go back to menu after user has won or lost
    go_back = 0

    # Amount of gears
    gear_amount = 6

    # Making Opponent harder by changing gear speed depending on level
    if limit<7:
        gear_speed2 = 70 - limit*5 
    else:
        gear_amount = 7
        gear_speed2 = 20
    # Checks if user should be given gear 7

        

    while True:

        # Changing wheels angle
        wheel_angle +=wheel_speed
        wheel_angle2 +=wheel_speed2

        # reducing meters
        meters -= 0.1
        

        # Transform the images to rotate them
        image = pygame.transform.rotate(tire_ahead, wheel_angle)
        meter_stic = pygame.transform.rotate(meter_stick,meter_turn)
        image2 = pygame.transform.rotate(tire_ahead, wheel_angle2)

        
        # Speed change of opponent
        inc_of_op+=0.2

     

        # Finish line to appear once user is near
        if meters<8:
            Finish_meter-=10


            
        # Changing speed of opponent
        if inc_of_op >gear_speed2 and op_gear<9:
            x_r+=0.09
            inc_of_op = 0
            wheel_speed2+=3
            op_gear+=1

        # If meter reached the final value it remains there
        if meter_turn>-255:
            meter_turn -=meter_speed
        else:
            meter_turn+=3

        
        # Converting meter rod and tire to rectangle so it can move how we want it to
        pivot2 = [755,120]
        rect3 = meter_stic.get_rect()
        rect3.center = pivot2

        rect = image.get_rect()
        pivot = [x_move+49,534]
        rect.center = pivot

        rect2 = image.get_rect()
        rect2.center = [x_move+160,534]

        rect4 = image2.get_rect()
        pivot4 = [x_move2+39,502]
        rect4.center = pivot4

        rect5 = image2.get_rect()
        pivot5 = [x_move2+150,502]
        rect5.center = pivot5

        # Wheel goes 0 after 180 to avoid to many number
        if wheel_angle >=180:
            wheel_angle = 0
        
        # Same for opponent
        if wheel_angle2 >=180:
            wheel_angle2 = 0

        
        
        #Car going slightly up and down
        car_Y_move-=0.1

        # How fast opponent is moving
        x_move2 += x_r

        if car_Y_move <=425:
            car_Y_move=430
        
        # Showing every image parameters are image,(x-axis,y-axis)
        SCREEN.blit(BG_r, (x1+900, 0))
        SCREEN.blit(BG_r, (x1, 0))
        SCREEN.blit(rally,(x_move2,car_Y_move))
        SCREEN.blit(image2,rect4)
        SCREEN.blit(image2,rect5)
        SCREEN.blit(Finish,(int(Finish_meter),400))
        SCREEN.blit(car,(x_move,car_Y_move))
        SCREEN.blit(image,rect)
        SCREEN.blit(image,rect2)
        SCREEN.blit(meter,(650,10))
        SCREEN.blit(meter_stic,rect3)

        # A black rectangle
        pygame.draw.rect(SCREEN,'black',(705,220,100,30))

        # Gear text
        Gear_text = get_font(12).render('GEAR :'+ str(gears),0,'white')
        SCREEN.blit(Gear_text,(710,230))

        # Showing how many meters are left
        if meters>0:
            Meter_text = get_font(15).render(str(int(meters))+'m',0,'black')
            SCREEN.blit(Meter_text,(560,10))

       # Check if user has won
        if meters<0:
            
            # Based on how far we are from the opponents car
            if x_move>x_move2:
                text = get_font(30).render('VICTORY!',0,'RED')
                SCREEN.blit(text,(350,300))
                if change_speed2:
                    # Level saved
                    limit+=1
                    insert = "UPDATE num SET id = "+ str(limit) 
                    db.execute(insert)
                    db.commit()
                
                change_speed2  = False
                x_move+=4
                x_move2+=4
                go_back +=1
                cut_sound.stop()

            elif x_move<x_move2:
                text = get_font(30).render('DEFEAT!',0,'RED')
                SCREEN.blit(text,(350,300))
                change_speed2  = False
                x_move+=4
                x_move2+=4
                go_back+=1
                cut_sound.stop()

            # Going back to menu
            if go_back>300:
                
                main_menu()
            
            
        # Checks if user has changed gear
        if gears>inititial_gear and gears <=gear_amount:

            # Opponent to get closer
            x_r-= 0.14
            
            # Speed increase
            speed+=8
            meter_speed+=0.2
            wheel_speed +=3
            meter_turn = 0
            inititial_gear+=1
         
            # STop the previous sound
            cut_sound.stop()

            # Cutting sound from the audio again
            sound = pygame.mixer.Sound('Assets/accelerate.mp3')
            raw_array = sound.get_raw()
            arr1+=300000
            arr2+=300000
            raw_array = raw_array[arr1:arr2]
            cut_sound = pygame.mixer.Sound(buffer=raw_array)
            cut_sound.play(-1)

        # Same but for reverse gear
        elif gears<inititial_gear and gears >=0:
          

            x_r+= 0.14
            speed-=8
            meter_speed-=0.1
            wheel_speed -=3
            meter_turn = 0
            inititial_gear-=1
            cut_sound.stop()
            sound = pygame.mixer.Sound('Assets/accelerate.mp3')
            raw_array = sound.get_raw()
            arr1-=300000
            arr2-=300000
            raw_array = raw_array[arr1:arr2]
            cut_sound = pygame.mixer.Sound(buffer=raw_array)
            cut_sound.play(-1)
        
       

        # Road changes
        if x1<-900:
            x1 = 0

        # Road speed
        x1-=speed

        #Events of pygame
        for event in pygame.event.get():

            # Checks if user wants to quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # IF user presses keys and they are allowed to change gears 
            if event.type == pygame.KEYDOWN and change_speed2:

                # Checks if users meter stick is at right place to change gear
                if event.key == pygame.K_SPACE and meter_turn<-180 and meter_turn>-202 and gears<gear_amount:
                    inititial_gear = gears
                    gears +=1

                # Checks if users meter stick is at wrong place
                elif event.key == pygame.K_SPACE and meter_turn<0  and gears >0:
                    inititial_gear = gears
                    gears -=1
                
                # checks if user is at 0 gear
                elif event.key == pygame.K_SPACE :
                    meter_turn = 0
                

                # Moves the car slightly ahead
                if event.key == pygame.K_RIGHT and x_move<700 :
                    x_move +=2
                  
                # Moves the car slightly back
                elif event.key == pygame.K_LEFT and x_move>0 :
                    x_move -=2
                    meter_turn -=1

                elif event.key == pygame.K_ESCAPE:
                    cut_sound.stop()
                    main_menu()

        #Update
        pygame.display.update()

# Backgrounds list
backgrounds = [
    "assets/BG_r.jpg",
    "assets/city.png",
    "assets/night2.png"
]
bg_index = 0

# Current background
BG_r = pygame.image.load(backgrounds[bg_index])
BG_r = pygame.transform.scale(BG_r, (WIDTH, HEIGHT))


def change_background():
    """Cycles through available backgrounds."""
    global BG_r, bg_index
    bg_index += 1
    if bg_index >= len(backgrounds):
        bg_index = 0  # loop back

    BG_r = pygame.image.load(backgrounds[bg_index])
    BG_r = pygame.transform.scale(BG_r, (WIDTH, HEIGHT))


# Customize car
def customize():
    global car, limit
    num = 1
    limit = 5  # total number of cars (1–5)

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Load car preview and actual car sprite
        car_show = pygame.image.load(f"assets/car{num}.png")
        car_show = pygame.transform.scale(car_show, (200, 170))

        car = pygame.image.load(f"assets/car_sk{num}.png")
        car = pygame.transform.scale(car, (200, 170))

        # Draw background and car
        SCREEN.blit(garage, (0, 0))
        SCREEN.blit(car_show, (350, 350))

        # Buttons
        High = Button(image=None, pos=(870, 300),
                      text_input=">", font=get_font(60),
                      base_color="white", hovering_color="green")
        Low = Button(image=None, pos=(50, 300),
                     text_input="<", font=get_font(60),
                     base_color="white", hovering_color="green")
        Back = Button(image=None, pos=(130, 50),
                      text_input="BACK", font=get_font(60),
                      base_color="RED", hovering_color="green")

        # Smaller, centered Change BG button
        ChangeBG = Button(
            image=None,
            pos=(WIDTH // 2, 200),  # centered
            text_input="Change BG",
            font=get_font(40),  # smaller text
            base_color="white",
            hovering_color="green"
        )

        # Load small preview of current background
        bg_preview = pygame.image.load(backgrounds[bg_index])
        bg_preview = pygame.transform.scale(bg_preview, (120, 70))  # small thumbnail

        # Show buttons
        for button in [High, Low, Back, ChangeBG]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Draw preview beside ChangeBG button
        SCREEN.blit(bg_preview, (WIDTH // 2 -50, 105))  # slightly right of button

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if High.checkForInput(MENU_MOUSE_POS):
                    num += 1
                    if num > limit:
                        num = 1
                if Low.checkForInput(MENU_MOUSE_POS):
                    num -= 1
                    if num < 1:
                        num = limit
                if Back.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                if ChangeBG.checkForInput(MENU_MOUSE_POS):
                    change_background()  # call new background function

        pygame.display.update()

def main_menu():
    global limit
  
    fetc = """SELECT id FROM num"""
    data = db.execute(fetc)
    img_counter = 0
    for row in data:
        img_counter = ''.join(row)
        
    limit = int(img_counter)

    
    while True:
        # Background of main menu
        SCREEN.blit(BG, (0, -100))
        
        # Mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Text of main menu(size,text,color)
        MENU_TEXT = get_font(70).render("DRIFTnDRAG", True, "red")

        # Placement of it
        MENU_RECT = MENU_TEXT.get_rect(center=(470, 70))

        # Creating button(Images,position,text,font,size,base color and the color changed when the mouse is above it)
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(470, 200), 
                            text_input="PLAY", font=get_font(60), base_color="white", hovering_color="green")
        # Creating button(Images,position,text,font,size,base color and the color changed when the mouse is above it)
        CUSTOMIZE = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(470, 350), 
                            text_input="CUSTOMIZE", font=get_font(60), base_color="white", hovering_color="green")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(470, 500), 
                            text_input="QUIT", font=get_font(60), base_color="white", hovering_color="green")

        # Showing Text
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Showing buttons
        for button in [PLAY_BUTTON,CUSTOMIZE,  QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        # Events
        for event in pygame.event.get():

            # Checks if user wants to quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Checks if mouse is pressed down and on which button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                    
                if CUSTOMIZE.checkForInput(MENU_MOUSE_POS):
                    customize()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Main function is called
main_menu()