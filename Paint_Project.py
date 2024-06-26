#from cProfile import label
#from calendar import c
#from distutils.cmd import Command
#from turtle import color, fillcolor
from configparser import Interpolation
from ctypes import resize
import cv2
import pyautogui as pg
import numpy as np
from tkinter import *
import math
from tkinter import filedialog
from tkinter import colorchooser
from tkinter.font import BOLD
from PIL import ImageTk, Image, ImageGrab

class PaintApp:
    def __init__(self, width, height, title):
        self.screen = Tk()
        self.screen.title(title)
        self.screen.geometry(str(width) + 'x' + str(height))
        self.last_x, self.last_y = None, None
        self.brush_color = 'black'
        self.erase_clr = 'white'
        self.fill_clr = ""
        self.clr2 = 0 
        self.clr = 0
        self.draw_width = 2
        self.shape_id = None

        #button area
        self.button_area = Frame(self.screen, width = width, height = 120, bg = "dark grey")
        self.button_area.pack()

        #create canvas
        self.canvas = Canvas(self.screen, width=width, height=height, bg="white")
        self.canvas.pack()

        #create menu bar
        self.my_menu = Menu(self.screen)
        self.screen.config(menu=self.my_menu)
        self.file_menu = Menu(self.my_menu)
        self.my_menu.add_cascade(label= "File",menu=self.file_menu)
        self.file_menu.add_command(label="New",command=self.clear_canvas)
        self.file_menu.add_command(label="Save",command=self.saveFile)
        self.file_menu.add_command(label="Open",command=self.loadFile)

        self.edit_menu = Menu(self.my_menu)
        self.my_menu.add_cascade(label= "Edit",menu=self.edit_menu)
        self.edit_menu.add_command(label= "Cut")
        self.edit_menu.add_command(label= "Copy")
        self.edit_menu.add_command(label= "Paste")

        #basic clear buttons
        Button(self.button_area, text = "Clear Screen", command = self.clear_canvas).place(x=5, y=5)
        Button(self.button_area, text = "Clear Text", command= self.clear_text).place(x=5, y=71)
        Button(self.button_area, text = "  <-  ").place(x=5, y=38)
        Button(self.button_area, text = "  ->  ").place(x=44, y=38)

        #tools area
        Button(self.button_area, text = " Text ", command=self.on_text, fg="red",bg="light yellow").place(x=120,y=38)
        Button(self.button_area, text = " Pencil ",command=self.on_Pencil,fg="red",bg="light yellow").place(x=120,y=5)
        Button(self.button_area, text = " Eraser ",command = self.on_eraser,fg="red",bg="light yellow").place(x=176 ,y=5)
        Button(self.button_area, text = "Z-In",command=self.on_zoomIn_pressed,fg="red",bg="light yellow").place(x=205,y=38)
        Button(self.button_area, text = "Z-Out",command=self.on_zoomOut_pressed,fg="red",bg="light yellow").place(x=245,y=38)
        Button(self.button_area,text = " Fill  ",fg = "red",bg="light yellow").place(x=165,y=38)
        Button(self.button_area,text = " Pick ",command= self.pick_clr,fg="red",bg="light yellow").place(x=200,y=69)
        Button(self.button_area,text = "Drop",command= self.dropPixel,fg="red",bg="light yellow").place(x=245,y=69)
        Button(self.button_area,text = " Select Area ",fg="red",bg="light yellow").place(x=120,y=69)
        self.width_button = Button(self.button_area, text = "  Width ",command=self.width_menu,fg="red",bg="light yellow").place(x=230,y=5)
        Label(self.button_area,text="Tools",padx=63,font=('arial',10,BOLD),fg="Red",bg="light yellow").place(x=120,y=98)

        #select colour button
        Button(self.button_area,bg=self.brush_color,padx=19,pady=19,command=self.choose_clr1).place(x=890, y=25)
        Label(self.button_area,text="Clr1",font=('arial',11,BOLD),fg="White",bg=self.brush_color).place(x=895,y=40)
        Button(self.button_area,bg=self.erase_clr,padx=19,pady=19,command=self.choose_clr2).place(x=950, y=25)
        Label(self.button_area,text="Clr2",font=('arial',11,BOLD),fg="black",bg=self.erase_clr).place(x=955,y=40)
        Button(self.button_area,bg="black",padx=5,pady=0.001,command=self.on_color1).place(x=705, y=5)
        Button(self.button_area,bg="white",padx=5,pady=0.001,command=self.on_color2).place(x=705, y=35)
        Button(self.button_area,bg="brown",padx=5,pady=0.001,command=self.on_color3).place(x=730, y=5)
        Button(self.button_area,bg="#C4A484",padx=5,pady=0.001,command=self.on_color4).place(x=730, y=35)
        Button(self.button_area,bg="purple",padx=5,pady=0.001,command=self.on_color5).place(x=755, y=5)
        Button(self.button_area,bg="#A865C9",padx=5,pady=0.001,command=self.on_color6).place(x=755, y=35)
        Button(self.button_area,bg="dark blue",padx=5,pady=0.001,command=self.on_color7).place(x=780, y=5)
        Button(self.button_area,bg="light blue",padx=5,pady=0.001,command=self.on_color8).place(x=780, y=35)
        Button(self.button_area,bg="dark green",padx=5,pady=0.001,command=self.on_color9).place(x=805, y=5)
        Button(self.button_area,bg="light green",padx=5,pady=0.001,command=self.on_color10).place(x=805, y=35)
        Button(self.button_area,bg="red",padx=5,pady=0.001,command=self.on_color11).place(x=830, y=5)
        Button(self.button_area,bg="pink",padx=5,pady=0.001,command=self.on_color12).place(x=830, y=35)
        Button(self.button_area,bg="orange",padx=5,pady=0.001,command=self.on_color13).place(x=855, y=5)
        Button(self.button_area,bg="yellow",padx=5,pady=0.001,command=self.on_color14).place(x=855, y=35)
        Button(self.button_area, text = "More Colour",padx=5, command=self.select_color).place(x=750, y=68)
        Label(self.button_area,text="Colours",padx=60,font=('arial',10,BOLD),fg="dark green",bg="light green").place(x=705,y=98)
        #Shapes button
        self.var = IntVar()
        Checkbutton(self.button_area,text="Fill ",bg="light blue",fg="dark blue",variable=self.var,command=self.fill_check).place(x=614,y=38)
        Button(self.button_area, text = "Circle",bg="dark Blue",fg="light blue",padx=9, command = self.on_circle).place(x=420,y=5)
        Button(self.button_area, text = "Oval",bg="dark Blue",fg="light blue",padx=10, command = self.on_oval).place(x=483,y=5)
        Button(self.button_area, text = "Line",bg="dark Blue",fg="light blue",padx=10, command = self.on_line).place(x=543,y=5)
        Button(self.button_area, text = "Arc 90",bg="dark Blue",fg="light blue",padx=9, command = self.on_arc90).place(x=600,y=5)
        Button(self.button_area, text = "Rectangle",bg="dark Blue",fg="light blue", command = self.on_rectangle).place(x=420,y=38)
        Button(self.button_area, text = " Square ",bg="dark Blue",fg="light blue", command = self.on_square).place(x=488,y=38)
        Button(self.button_area, text = "Triangle",padx=4,bg="dark Blue",fg="light blue", command = self.on_triangle).place(x=545,y=38)
        Button(self.button_area, text = " Pantagon ",bg="dark Blue",fg="light blue", command = self.on_pentagon).place(x=420,y=69)
        Button(self.button_area, text = "  Hexagon  ",bg="dark Blue",fg="light blue", command = self.on_hex_button).place(x=494,y=69)
        Button(self.button_area, text="  More Shapes  ", fg="dark Blue",bg="light blue",command=self.more_shapes).place(x=570,y=69)
        Label(self.button_area,text="Shapes",font=('arial',10,BOLD),fg="dark Blue",bg="light blue",padx=95).place(x=420,y=98)

        
        #bind the function to the mouse event
        self.canvas.bind("<B1-Motion>",self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>", self.brush_draw_end)


    def on_zoomIn_pressed(self):
       self.canvas.unbind("<B1-Motion>")
       self.canvas.unbind("<ButtonRelease-1>")
       self.canvas.bind("<B1-Motion>",self.zoomIn)
    def zoomIn(self,event):
        if self.last_x is None:
           self.last_x,self.last_y=event.x,event.y
           return 
        x,y=event.x,event.y
        self.id=self.canvas.scale("object",x,y,1.01,1.01)
    def on_zoomOut_pressed(self):
       self.canvas.unbind("<B1-Motion>")
       self.canvas.unbind("<ButtonRelease-1>")
       self.canvas.bind("<B1-Motion>",self.zoomOut)
    def zoomOut(self,event):
       x,y=event.x,event.y
       self.canvas.scale("object",x,y,0.99,0.99)


    #pick clr

    def pick_clr(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>",self.pickClr)
    def pickClr(self,event):
        x=event.x
        y=event.y
        r=self.canvas.itemcget( self.canvas.find_closest(x,y), 'fill')
        self.fill_clr=r
    def dropPixel(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>",self.dropPixel1)
    def dropPixel1(self,event):
        x=event.x
        y=event.y
        self.id= self.canvas.find_closest(x,y)
        self.canvas.itemconfig(self.id,fill=self.fill_clr)

    #shapes
    def more_shapes(self):
        self.top = Toplevel(bg="light blue")
        self.top.title("More Shapes")
        self.top.geometry("200x200")
        Button(self.top, text = " Curve ",fg="dark Blue",bg="light blue", command = self.onCurve1).pack()
        Button(self.top, text = "  Star ",fg="dark Blue",bg="light blue", command = self.on_star).pack()
        Button(self.top, text = "Arc(90-180)",fg="dark Blue",bg="light blue", command = self.on_arc180).pack()
        Button(self.top, text = "Arc(180-270)",fg="dark Blue",bg="light blue", command = self.on_arc270).pack()
        Button(self.top, text = "Arc(270-360)",fg="dark Blue",bg="light blue", command = self.on_arc360).pack()
        Button(self.top, text = "N-Polygon!",bg="light Blue",fg="dark blue", command = self.on_n_poly).pack()
        

    #line
    def on_line(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.draw_line_end)
    def draw_line(self, event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.shape_id = self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=self.draw_width,fill=self.brush_color,tags="object")
    def draw_line_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None 

    #circle
    def on_circle(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_circle)
        self.canvas.bind("<ButtonRelease-1>", self.draw_circle_end)
    def draw_circle(self, event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x-event.x) + abs(self.last_y-event.y)
        x1, y1 = (self.last_x - radius),(self.last_y - radius)
        x2, y2 = (self.last_x + radius),(self.last_y + radius)
        self.shape_id = self.canvas.create_oval(x1, y1, x2, y2, outline=self.brush_color,tags="object", width=self.draw_width,fill=self.fill_clr)
    def draw_circle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None
    
    #oval
    def on_oval(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_oval)
        self.canvas.bind("<ButtonRelease-1>", self.draw_oval_end)
    def draw_oval(self, event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.shape_id = self.canvas.create_oval(self.last_x, self.last_y, event.x, event.y, outline=self.brush_color,tags="object", width=self.draw_width, fill = self.fill_clr)
    def draw_oval_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None
    
    #rectangle
    def on_rectangle(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.draw_rectangle_end)
    def draw_rectangle(self, event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.shape_id = self.canvas.create_rectangle(self.last_x, self.last_y, event.x, event.y, outline=self.brush_color,tags="object", width=self.draw_width, fill = self.fill_clr)
    def draw_rectangle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    #square
    def on_square(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_square)
        self.canvas.bind("<ButtonRelease-1>", self.draw_square_end)
    def draw_square(self, event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x-event.x) + abs(self.last_y-event.y)
        x1, y1 = (self.last_x - radius),(self.last_y - radius)
        x2, y2 = (self.last_x + radius),(self.last_y + radius)
        self.shape_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.brush_color, width=self.draw_width, fill = self.fill_clr,tags="object")
    def draw_square_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None
        
    #star
    def on_star(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_star)
        self.canvas.bind("<ButtonRelease-1>", self.draw_star_end)
    def draw_star(self,event):
         if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
         if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
         radius1 = abs(event.x - self.last_x)
         radius2 = abs(event.y - self.last_y)
         x_center = self.last_x + radius1
         y_center = self.last_y + radius2
         points = []
         angle = 2 * math.pi / 10
         for i in range(10):
             radius = radius1 if i % 2 == 0 else radius2
             x = x_center + radius * math.cos(i * angle)
             y = y_center + radius * math.sin(i * angle)
             points.append((x, y))
         self.shape_id = self.canvas.create_polygon(points, outline=self.brush_color, width=self.draw_width, fill= self.fill_clr,tags="object")
    def draw_star_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    #arc90
    def on_arc90(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_arc)
        self.canvas.bind("<ButtonRelease-1>", self.draw_arc_end)
    def draw_arc(self, event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x-event.x) + abs(self.last_y-event.y)
        x1, y1 = (self.last_x - radius),(self.last_y - radius)
        x2, y2 = (self.last_x + radius),(self.last_y + radius)
        self.shape_id = self.canvas.create_arc(x1, y1, x2, y2, outline=self.brush_color, width=self.draw_width, fill = self.fill_clr,tags="object")
    def draw_arc_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None 

    #arc 180
    def on_arc180(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_arc180)
        self.canvas.bind("<ButtonRelease-1>", self.draw_arc180_end)
    def draw_arc180(self, event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x-event.x) + abs(self.last_y-event.y)
        x1, y1 = (self.last_x - radius),(self.last_y - radius)
        x2, y2 = (self.last_x + radius),(self.last_y + radius)
        self.shape_id = self.canvas.create_arc(x1, y1, x2, y2,start=90, fill = self.fill_clr, outline=self.brush_color, width=self.draw_width,tags="object")
    def draw_arc180_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None 

    #arc 270
    def on_arc270(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_arc270)
        self.canvas.bind("<ButtonRelease-1>", self.draw_arc270_end)
    def draw_arc270(self, event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x-event.x) + abs(self.last_y-event.y)
        x1, y1 = (self.last_x - radius),(self.last_y - radius)
        x2, y2 = (self.last_x + radius),(self.last_y + radius)
        self.shape_id = self.canvas.create_arc(x1, y1, x2, y2,start=180, outline=self.brush_color, width=self.draw_width, fill = self.fill_clr,tags="object")
    def draw_arc270_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None 

    #arc 360
    def on_arc360(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_arc360)
        self.canvas.bind("<ButtonRelease-1>", self.draw_arc360_end)
    def draw_arc360(self, event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x-event.x) + abs(self.last_y-event.y)
        x1, y1 = (self.last_x - radius),(self.last_y - radius)
        x2, y2 = (self.last_x + radius),(self.last_y + radius)
        self.shape_id = self.canvas.create_arc(x1, y1, x2, y2,start=270, outline=self.brush_color, width=self.draw_width , fill = self.fill_clr,tags="object")
    def draw_arc360_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None 

    #pencil
    def on_Pencil(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>", self.brush_draw_end)
    
    #pentagon
    def on_pentagon(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_pentagon)
        self.canvas.bind("<ButtonRelease-1>", self.draw_pentagon_end)
    def draw_pentagon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x - event.x) + abs(self.last_y - event.y)
        angle = 2 * math.pi / 5
        points = []
        for i in range(5):
            x = self.last_x + radius * math.cos(i * angle)
            y = self.last_y + radius * math.sin(i * angle)
            points.append((x, y))
        self.shape_id = self.canvas.create_polygon(points, outline=self.brush_color, width=self.draw_width,fill= self.fill_clr,tags="object")
    def draw_pentagon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None    

    #hexagon
    def on_hex_button(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.hex_draw)
        self.canvas.bind("<ButtonRelease-1>", self.hex_draw_end)
    def hex_draw(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x - event.x) + abs(self.last_y - event.y)
        angle = 2 * math.pi / 6
        points = []
        for i in range(6):
            x = self.last_x + radius * math.cos(i * angle)
            y = self.last_y + radius * math.sin(i * angle)
            points.append((x, y))
        self.shape_id = self.canvas.create_polygon(points, outline=self.brush_color, width=self.draw_width,fill=self.fill_clr,tags="object")
    def hex_draw_end(self, event):
        self.last_x, self.last_y = None, None 
        self.shape_id = None

    #n polygon
    def on_n_poly(self):
        self.e = Entry(self.top,width=15)
        self.e.pack()
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.n_draw)
        self.canvas.bind("<ButtonRelease-1>", self.n_draw_end)
    def n_draw(self, event):
        n = int(self.e.get())
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x - event.x) + abs(self.last_y - event.y)
        angle = 2 * math.pi / n
        points = []
        for i in range(n):
            x = self.last_x + radius * math.cos(i * angle)
            y = self.last_y + radius * math.sin(i * angle)
            points.append((x, y))
        self.shape_id = self.canvas.create_polygon(points, outline = self.brush_color, width=self.draw_width , fill = self.fill_clr,tags="object")
    def n_draw_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    #triangle
    def on_triangle(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.triangle_draw)
        self.canvas.bind("<ButtonRelease-1>", self.triangle_draw_end)
    def triangle_draw(self, event):
         if self.shape_id != None:
            self.canvas.delete(self.shape_id)
         if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
         x1, y1 = self.last_x, self.last_y
         x2, y2 = event.x, event.y
         x3, y3 = (self.last_x - (event.x - self.last_x)), event.y
         self.shape_id = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=self.brush_color, width=self.draw_width, fill = self.fill_clr,tags="object")
    def triangle_draw_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None


    #color selection
    def choose_clr1(self):
        self.clr = 0
    def choose_clr2(self):
        self.clr = 1
    def on_color1(self):
        c = "black"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color2(self):
        c = "white"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color3(self):
        c = "brown"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color4(self):
        c = "#C4A484"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color5(self):
        c = "purple"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color6(self):
        c = "#A865C9"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color7(self):
        c = "dark blue" 
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color8(self):
        c = "light blue"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color9(self):
        c = "dark green"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color10(self):
        c =  "light green"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color11(self):
        c = "red"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color12(self):
        c = "pink"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color13(self):
        c =  "orange"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def on_color14(self):
        c = "yellow"
        if self.clr == 0:
            self.brush_color = c
        elif self.clr == 1:
            self.erase_clr = c

    def select_color(self):
        selected_color = colorchooser.askcolor()
        self.brush_color = selected_color[1]

    def clear_canvas(self):
        self.canvas.delete("all")
    
    #text box
    def on_text(self):
        self.my_text = Text(self.canvas,width=30,height=10,bg="light green")
        self.my_text.place(x=0,y=0)
    def clear_text(self):
        self.my_text.place_forget()

    #width menu
    def clickWidth(self):
        self.draw_width=self.r.get()
    def width_menu(self):
        self.r=IntVar()
        self.r.set("2")
        x1, y1 = 0, 0
        val = [("1", 1),("2",2),("3",3),("4",4),("5",5),("6  ",6),("7  ",7),("8  ",8),("9  ",9),("10",10)]
        for txt,var in val:
            Radiobutton(self.width_button, text=txt,variable=self.r, value=var,command=self.clickWidth,fg="red",bg="light yellow").place(x=290+x1,y=2+y1)
            y1=y1+24
            if var == 5:
                x1=40
                y1=0

    #eraser
    def on_eraser(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.eraser)
        self.canvas.bind("<ButtonRelease-1>", self.eraser_end)
    def eraser(self, event):
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=self.draw_width, capstyle=ROUND, fill = self.erase_clr,tags="object")
        self.last_x, self.last_y = event.x, event.y
    def eraser_end(self, event):
        self.last_x, self.last_y = None, None

    def saveFile(self):
        self.save_file_Path = filedialog.asksaveasfile()
        self.save_file = str(self.canvas)
        self.save_file_Path.write(self.save_file)
        self.save_file_Path.close()

    def loadFile(self):
        self.Load_file_Path = filedialog.askopenfilename()
        self.load_img = ImageTk.PhotoImage(Image.open(self.Load_file_Path))
        self.my_img = Label(self.canvas,image=self.load_img)
        self.my_img.pack()

    def fill_check(self):
        if self.var.get() == 1:
            self.fill_clr = self.brush_color
        else:
            self.fill_clr = ""

    def run(self):
        self.screen.mainloop()
    
    def brush_draw(self, event):
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,tags="object", width=self.draw_width, capstyle=ROUND, fill = self.brush_color)
        self.last_x, self.last_y = event.x, event.y
    def brush_draw_end(self, event):
        self.last_x, self.last_y = None, None

    def on_curve(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.onCurve1)
        self.canvas.bind("<ButtonRelease-1>", self.on_curveEnd)
    def onCurve2(self,canvas,points):
        n = len(points)
        if n < 2:
            return
        def binomial_coefficient(n, k):
            if k == 0 or k == n:
                return 1
            return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)
        def calculate_position(t):
            x = 0
            y = 0
            for i in range(n):
                coefficient = binomial_coefficient(n - 1, i)
                factor1 = coefficient * (t ** i) * ((1 - t) ** (n - 1 - i))
                factor2 = points[i][0]
                factor3 = points[i][1]
                x += factor1 * factor2
                y += factor1 * factor3
            return x, y
        for t in range(0, 101):  
            t /= 100
            x, y = calculate_position(t)
            self.canvas.create_oval(x, y, x + 1, y + 1, fill=self.fill_clr)
    def onCurve1(self,event):
        if self.shape_id != None:
            self.canvas.delete(self.shape_id)
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        control_points = []
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        x3, y3 = (self.last_x - (event.x - self.last_x)), event.y
        control_points.append((x1, y1,x2,y2,x3,y3))
        if len(control_points) > 1:
            self.onCurve2(self.canvas, control_points)

    def on_curveEnd(self,event):
        self.last_x, self.last_y = None, None
        self.shape_id = None 


PaintApp(1000,800,"Paint App").run()