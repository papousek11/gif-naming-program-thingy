from PIL import Image, ImageSequence
from os import walk
import os.path
import random
import pygame



files = []
Image_origin_loader = Image
Image_origin_loader_for_rendering = Image
Image_Size = (260,144)
Display_image_out = pygame.image.load("zacatek.png")
Image_Index = 0
name = ""
editing_mode = False
animated_gif_warning = False

def CheckForDirectories():
    #took me like 10 minutes to realize os.path.isfile does not work on directories
    if (not os.path.exists("./import")):
        os.mkdir("./import")
    if (not os.path.exists("./export")):
        os.mkdir("./export")



def velmi_dulezita_random_int_funkce():
    #jestli se budou jmenovat dva stejně tak to tak chtel bůh asi
    randoms = random.randint(0,100000)
    return randoms

def Save_current_image():
    global name
    if(files[Image_Index-1][-4:] == ".gif"):
        if(getattr(Image_origin_loader_for_rendering, "is_animated", False)):
            
            gif_frames = [gif_frame.copy() for gif_frame in ImageSequence.Iterator(Image_origin_loader_for_rendering)]
            if(name == ""):
                gif_frames[0].save("./export/nauc_se_kurva_pojemnovavat_veci_ty_kokot"+str(velmi_dulezita_random_int_funkce())+".gif",
                save_all = True, append_images=gif_frames[1:],optimize=False,loop=0,duration=100,)
            else:
                gif_frames[0].save("./export/"+name+".gif",
                save_all = True, append_images=gif_frames[1:],optimize=False,loop=0,duration=100,)
            pass
        else:
            if(name == ""):
                Image_origin_loader_for_rendering.save("./export/nauc_se_kurva_pojemnovavat_veci_ty_kokot"+str(velmi_dulezita_random_int_funkce())+".gif")
            else:
                Image_origin_loader_for_rendering.save("./export/"+name+".gif")
    else:
        if(name == ""):
            Image_origin_loader_for_rendering.save("./export/nauc_se_kurva_pojemnovavat_veci_ty_kokot"+str(velmi_dulezita_random_int_funkce())+".gif")
        else:
            Image_origin_loader_for_rendering.save("./export/"+name+".gif")
    name = ""
    return

def ImagesNames():
    for(dirpath, dirnames, filenames) in walk("./import"):
        files.extend(filenames)
    
    print(files)
    
    

def Temp_image_edit():
    global Image_Index
    global Display_image_out
    global editing_mode
    global Image_origin_loader_for_rendering
    global animated_gif_warning
    
    animated_gif_warning = False
    if(Image_Index >= len(files)): 
        Display_image_out = pygame.image.load("./konec.png")
    else:
        Image_origin_loader_for_rendering = Image.open("./import/"+files[Image_Index])
        Image_origin_loader = Image_origin_loader_for_rendering.resize(Image_Size)
        if(getattr(Image_origin_loader_for_rendering, "is_animated", False)):
            animated_gif_warning = True
            print(animated_gif_warning)
        
        if Image_origin_loader.mode not in ("RGB", "RGBA"):
            Image_origin_loader = Image_origin_loader.convert("RGBA")
        
        mode = Image_origin_loader.mode
        data = Image_origin_loader.tobytes()
        Display_image_out = pygame.image.fromstring(data, Image_Size, mode)
    if(Image_Index >= len(files)): 
        pass
    else:
        Image_Index = Image_Index + 1
    print(Image_Index)
    print(len(files))
    editing_mode = True
    return
    

CheckForDirectories()
ImagesNames()
pygame.init()
pygame.freetype.init()

font = pygame.freetype.SysFont(None, 24)
window = pygame.display.set_mode((1200,700))
pygame.display.set_caption("naming thing")

run = True
while run:
    pygame.time.delay(50)
    window.fill("#aae5a4")
    if(animated_gif_warning == True):
        window.blit(font.render("Warning: you are editing an animated gif. The gifs are fixed to 10fps for now.", (0, 0, 0))[0], (100, 70))
    window.blit(Display_image_out,(100,100))
    window.blit(font.render(name, (0, 0, 0))[0], (100, 260))
    pygame.display.update()
    
    
    
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RETURN):
                if(editing_mode == False):
                    Temp_image_edit()
                else:
                    Save_current_image()
                    Temp_image_edit()
            else:
                if(len(pygame.key.name(event.key)) > 1):
                    print(pygame.key.name(event.key))
                    if(event.key == pygame.K_SPACE):
                        name = name + " "
                    elif(event.key == pygame.K_BACKSPACE):
                        if(name == ""):
                            pass
                        else:
                            name = name[:-1]
                    elif pygame.key.name(event.key)[1] in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                        name = name + pygame.key.name(event.key)[1]
                    else:
                        pass
                else:
                    name = name + pygame.key.name(event.key)
                    
                
                break
                
                
            
            
        if(event.type == pygame.QUIT):
            run = False
            
pygame.quit()