from tkinter import Canvas,Tk,messagebox,font
from itertools import cycle
from random import randrange
#import turtle 

canvas_width=800
canvas_height=400

root=Tk()
c=Canvas(root,width=canvas_width,height=canvas_height,background='light blue')
c.create_rectangle(0,300,800,400,fill='yellow')
#c.create_oval(-100,-100,100,100,fill='blue')
c.pack()

color_cycle=cycle(['blue','green','black','brown','orange'])
egg_width=45
egg_height=55
egg_score=10
egg_speed=500
egg_interval=5000

#difficult_factor=0.95

catcher_color = 'blue' 
catcher_width = 100
catcher_height = 100  
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height - catcher_height - 20 
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height
catcher = c.create_arc(catcher_start_x, catcher_start_y,catcher_start_x2, catcher_start_y2, start=200,extent=140,style='arc', outline=catcher_color, width=3)

game_font = font.nametofont('TkFixedFont')  
game_font.config(size=18)  
score = 0  
score_text = c.create_text(10, 10, anchor='nw', font=game_font, fill='darkblue',text='score: ' + str(score))
lives_remaining = 3  
lives_text = c.create_text(canvas_width - 10, 10, anchor='ne', font=game_font, fill='darkblue',text='Lives: ' + str(lives_remaining))


eggs=[]

def create_egg():
    if lives_remaining>0:
        x=randrange(50,750)
        y=10
        new_egg=c.create_oval(x,y,x+egg_width,y+egg_height,fill=next(color_cycle))
        eggs.append(new_egg)
        root.after(egg_interval,create_egg)



def move_eggs(): 
    for egg in eggs: 
        (egg_x,egg_y,egg_x2,egg_y2)=c.coords(egg) 
        c.move(egg, 0, 10) 
        if egg_y2 > canvas_height-20: 
            #egg_dropped(egg) 
            global lives_remaining,egg_speed,egg_interval
            lives_remaining-=1
            c.itemconfigure(lives_text, text='lives: ' + str(lives_remaining)) 
            # c.itemconfigure(lives_remaining)
            eggs.remove(egg)
            c.delete(egg)
            egg_speed=egg_speed-10
            egg_interval=egg_interval-100
        if lives_remaining<=0:
            messagebox.showinfo('game over',' your score:'+str(score))
            root.destroy()
            break        
    root.after(egg_speed, move_eggs) 

#def egg_dropped(egg):
#    eggs.remove(egg)
#    c.delete(egg)
    #loss_a_lives_remaining()
    #lives_remaining=lives_remaining-1
    #c.itemconfigure('lives_text',text=lives_remaining)
#    if lives_remaining==0:
#        messagebox.showinfo('game over your score:'+str(score))
#    root.destroy()

#def loss_a_lives_remaining():
#    global lives_remaining
#    lives_remaining-=1
#    #c.itemconfigure_lives_remaining(lives_remaining)
#    c.itemconfigure('lives_text',text=lives_remaining)

def check_catcher():
    (catcher_x,catcher_y,catcher_x2,catcher_y2)=c.coords(catcher)
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2)=c.coords(egg)
        if catcher_x<egg_x and catcher_x2>egg_x2 and catcher_y2-egg_y2<40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(points)
    root.after(100,check_catcher)

points=10

def increase_score(points):
    global score,egg_speed,egg_interval
    score+=points
    #eggs_speed=int(egg_speed+difficult_factor)
    #egg_interval=int(egg_interval+difficult_factor)
    c.itemconfigure(score_text, text='score: ' + str(score)) 

def move_left(event): 
    (x1, y1, x2, y2) = c.coords(catcher) 
    if x1 > 0: 
        c.move(catcher, -20, 0)

def move_right(event): 
    (x1, y1, x2, y2) = c.coords(catcher) 
    if x2 < canvas_width: 
        c.move(catcher, 20, 0)

c.bind('<Left>', move_left) 
c.bind('<Right>', move_right) 
c.focus_set()

root.after(1000,create_egg)
root.after(1000,move_eggs)
root.after(1000,check_catcher)

root.mainloop()

