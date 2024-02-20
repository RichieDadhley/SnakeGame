#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:00:21 2024

@author: richiedadhley
"""

from tkinter import * 
import random 

# Defining constants. Convention is to use capital letters
GAME_WIDTH = 700 
GAME_HEIGHT = 700
SPEED = 150 # Lower the number, faster the game
SPACE_SIZE = 50 
BODY_PARTS = 3 # Starting size of snake
SNAKE_COLOUR = '#00FF00' # This is the code for green
FOOD_COLOUR = '#FF0000' # Red
BACKGROUND_COLOUR = '#000000' # Black 


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range(0,BODY_PARTS):
            self.coordinates.append([0,0]) # Snake starts in top left corner
        
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOUR, tag ="snake")
            self.squares.append(square)
        
        
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE
        
        self.coordinates = [x,y]
        
        canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOUR, tag="food")
        
        
def next_turn(snake, food):
    
    x,y = snake.coordinates[0]
    
    if direction == "up":
        y  -= SPACE_SIZE
        
    elif direction == "down":
        y += SPACE_SIZE
        
    elif direction == "left":
        x -= SPACE_SIZE
    
    elif direction == "right":
        x += SPACE_SIZE
        
        
    if x < 0:
        x = GAME_WIDTH
    elif x >= GAME_WIDTH:
        x = 0
    
    if y < 0:
        y = GAME_HEIGHT
    elif y >= GAME_HEIGHT:
        y = 0
        
        
    # Update Snake coordinates
    snake.coordinates.insert(0,(x,y)) # 0 means the head of the snake 
    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y + SPACE_SIZE, fill= SNAKE_COLOUR)
    snake.squares.insert(0, square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score 
        global SPEED 
        
        score += 1
        
        if SPEED != 5:
            SPEED -= 5
        
        label.config(text="Score:{}".format(score))
        
        # Remove this food 
        canvas.delete("food")
        
        # Place new food 
        food = Food()
    
    # Only delete the square if didn't eat something 
    else:
        # Delete the snake square from where it's moved from
        del snake.coordinates[-1]
        
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    
    if check_collisions(snake):
        game_over()
        
    else:  
        window.after(SPEED, next_turn, snake, food)



def change_direction(new_direction):
    
    global direction 
    
    if new_direction == "left":
        if direction != 'right':
            direction = new_direction
    
    elif new_direction == "right":
        if direction != 'left':
            direction = new_direction
            
    elif new_direction == "up":
        if direction != 'down':
            direction = new_direction
    
    elif new_direction == "down":
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    
    x,y = snake.coordinates[0]
    
    for body_part in snake.coordinates[1:]: # All the body parts after the head
        if x == body_part[0] and y == body_part[1]:
            print("Game Over")
            return True
    
    return False 
    
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text = "GAME OVER", fill ="red", 
                       tag="gameover")
    restart_button.place(x = canvas.winfo_width()/2 - 50, y = canvas.winfo_height()/2+100)

def restart_game():
    global snake, food, score, direction, SPEED 
    
    snake.coordinates = []
    snake.squares = []
    restart_button.place(x=0, y=0)

    # Reset game variables to initial values
    canvas.delete(ALL)
    SPEED = 150 
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)
    

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0 
direction = 'down'

label = Label(window, text="Score:{}".format(score), font =('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

#Centre window when it appears
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Find x and y adjust 
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")


window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


restart_button = Button(window, text="Restart", command=restart_game, font=('consolas', 20))
restart_button.place(x=0, y=0)


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()