import pygame as pg
import random

from pygame.constants import QUIT
pg.init()
pg.mixer.init()

win_width = 800
win_height = 400

game_window = pg.display.set_mode((win_width,win_height))
pg.display.set_caption('Snake Game')

clock = pg.time.Clock()

# This function gets system default font for game_window
font = pg.font.SysFont(None,40) # Second argument specifies size of font

def display_text(txt,clr,x,y):
        text = font.render(txt,True,clr)
        game_window.blit(text,[x,y])    # [x,y] is coordinate of text on window
        # This updates the window with text

def game():

    def draw_snake(where,color,coordinate_list,size): # position_list is of the form [[x1,y1],[x2,y2],...]
        for x,y in coordinate_list:   # This for loop creates {len(position_list)} rectangles
            pg.draw.rect(where,color,[x,y,size,size])

    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 100
    snake_y = 50
    snake_size = 20
    apple_size = snake_size
    velocity_x = 0
    velocity_y = 0
    Vx_init = 0
    Vy_init = 0
    fps = 50
    apple_x = random.randint(win_width/10,win_width-300)
    apple_y = random.randint(win_height/10,win_height-40)
    score = 0
    snake_len = 1   # If initialized with 0, then no snake will be created, nor its length will change
    body_list = list()    # This list stores the coordinates of every block of snake's body
    level = 1
    cur_score = 0
    with open('highscore.txt','r') as r:
        h_score = r.read()

    # Gameloop
    while not exit_game:

        # Collision logic
        if snake_x < 0 or snake_x > win_width:
            game_over = True
        elif snake_y < 0 or snake_y > win_height:
            game_over = True
        else:
            pass

        if game_over:

            game_window.fill((255,255,255))
            display_text('GAME OVER!!!',(0,0,0),win_width/3,win_height/2.5)
            display_text('Press Enter to continue',(0,0,0),win_width/3,win_height/2)
            display_text(f'Your score : {cur_score}',(255,0,0),win_width/3,win_height/4)

            pg.mixer.music.load('game_over.mp3')    # This loads music to python file
            pg.mixer.music.play()   # This adds music to the game

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        welcome()
                    else:
                        pass
                else:
                    pass
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game = True

                elif event.type == pg.KEYDOWN:  # Velocity handling
                    if event.key == pg.K_UP:
                        velocity_y = -(Vy_init + 2)
                        velocity_x = 0
                    elif event.key == pg.K_DOWN:
                        velocity_y = Vy_init + 2
                        velocity_x = 0
                    elif event.key == pg.K_RIGHT:
                        velocity_y = 0
                        velocity_x = Vx_init + 2
                    elif event.key == pg.K_LEFT:
                        velocity_y = 0
                        velocity_x = -(Vx_init + 2)
                    else:
                        pass
                else:
                    pass
                
            game_window.fill((153,204,255))

            snake_x += velocity_x   # Updating the position in a while loop, thus giving it a velocity
            snake_y += velocity_y

            if abs(snake_x-apple_x) < apple_size and abs(snake_y-apple_y) < apple_size:  # abs() returns absolute values, i.e. default modulus function
            # If we would have made desired changes when coordinates of snake and apple were equal, then while playing, we would have to exactly match their coordinates, which is unwanted. What we want is that if the apple and snake are at close vicinity, desired changes should take place
                
                pg.mixer.music.load('beep.mp3')
                pg.mixer.music.play()

                score += 10
                apple_x = random.randint(win_width/10,win_width-350)
                apple_y = random.randint(win_height/10,win_height-40)
                snake_len += snake_size-10  # snake_len is updating every time, when snake eats the apple
                cur_score = score

                if cur_score == 100:
                    pg.mixer.music.load('achievement.mp3')
                    pg.mixer.music.play()
                elif cur_score > 100:
                    Vx_init = 2
                    Vy_init = 2
                    level = 2
                elif cur_score == 500:
                    pg.mixer.music.load('achievement.mp3')
                    pg.mixer.music.play()
                elif cur_score > 500:
                    Vx_init = 4
                    Vy_init = 4
                    level = 3
                elif cur_score == 1000:
                    pg.mixer.music.load('achievement.mp3')
                    pg.mixer.music.play()
                elif cur_score > 1000:
                    Vx_init = 6
                    Vy_init = 6
                    level = 4
                else:
                    pass

                if cur_score > int(h_score):
                    h_score = str(cur_score)
                else:
                    pass
                with open('highscore.txt','w') as w:
                    w.write(h_score)

            else:
                pass

            snake_head = list() # Every time an empty list is being created

            # Coordinates of the snake block at an instance is being appended to snake_head
            snake_head.append(snake_x)
            snake_head.append(snake_y)
            # snake_head is such a list which stores coordinate of snake's head at any instance

            body_list.append(snake_head)  # body_list is being appended, which was initially empty
            # Each time the while loop runs, a coordinate element of the form [x,y] is appended to body_list
            # snake_head is the last element of body_list

            if len(body_list) > snake_len:
                del body_list[0]
                # This statement prevents the draw_snake() function to increase the length of snake at every position change, as it deletes the first element of body_list and thus new sqaure gets formed with deletion of existing square
            else:
                pass

            if snake_head in body_list[:-1]:  # This implies {if last element of a list is also at some other index of that list, then execute the command}
                game_over = True
                # This statement make sures, that if coordinate of snake's head coincide with any block of its body, the game should be over
            else:
                pass
            
            # Scorer
            display_text(f'Score : {score}',(255,255,255),win_width-200,20)
            display_text(f'High Score : {h_score}',(255,255,255),win_width-250,50)
            display_text(f'Level : {level}',(255,0,0),win_width-120,win_height-30)

            pg.draw.rect(game_window,(255,0,0),[apple_x,apple_y,apple_size,apple_size])
            
            draw_snake(game_window,(178,255,102),body_list,snake_size)

        clock.tick(fps)
            
        pg.display.update()

    pg.quit()
    quit()

def welcome():
    # Specific variables
    exit_game = False

    # Loop
    while not exit_game:
        game_window.fill('yellow')
        display_text('Welcome to Snakes','black',win_width/3,win_height/3)
        display_text('Press Spacebar to Begin','black',win_width/3.3,win_height/2.2)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_game = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pg.mixer.music.load('game_begin.mp3')
                    pg.mixer.music.play()
                    game()
                else:
                    pass
            else:
                pass
        
        pg.display.update()
        
    pg.quit()
    quit()

welcome()