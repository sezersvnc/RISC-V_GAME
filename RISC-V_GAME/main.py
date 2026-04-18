import pygame
import sys
import os

# Pygame Initialization
pygame.init()

# Color Palette
BG_COLOR = (30, 30, 40)
QUESTION_BG = (15, 25, 45) 
WHITE = (240, 240, 240)
GREEN = (50, 200, 80)
RED = (220, 50, 50)
GRAY = (100, 100, 110)
YELLOW = (255, 200, 50)
BLUE = (70, 130, 200)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 50)

# Screen Settings
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conquest: RISC-V Edition")

# Map Loading Function
def load_image(file_name):
    try:
        img = pygame.image.load(file_name)
        return pygame.transform.scale(img, (WIDTH, HEIGHT))
    except:
        print(f"WARNING: '{file_name}' not found! Background will remain black.")
        return None

maps = {
    "easy": load_image("harita.png"),
    "medium": load_image("duzce.png"),
    "hard": load_image("marmara.png")
}

# Fonts
winner_font=pygame.font.SysFont("Arial",25,bold=True)
title_font = pygame.font.SysFont("Arial", 40, bold=True)
question_font = pygame.font.SysFont("Arial", 24)
button_font = pygame.font.SysFont("Arial", 26, bold=True)
small_font = pygame.font.SysFont("Arial", 18, bold=True)
option_font = pygame.font.SysFont("Arial", 22, bold=True)

# LEVEL 1: EASY (TURKEY)
data_easy = {
    "Marmara": {"pos": (160, 180), "conquered": False, "question": "Which is the 'Load Word' instruction in RV32I architecture?", "options": {"A": "sw", "B": "lw", "C": "ld"}, "answer": "B"},
    "Aegean": {"pos": (140, 340), "conquered": False, "question": "Which instruction is used to make a system call?", "options": {"A": "syscall", "B": "ecall", "C": "ebreak"}, "answer": "B"},
    "Mediterranean": {"pos": (350, 490), "conquered": False, "question": "How many integer registers are there in the base RV32I architecture?", "options": {"A": "16", "B": "32", "C": "64"}, "answer": "B"},
    "Central Anatolia": {"pos": (450, 310), "conquered": False, "question": "Which instruction is used for the 'Branch if Equal' operation?", "options": {"A": "beq", "B": "bne", "C": "jmp"}, "answer": "A"},
    "Black Sea": {"pos": (350, 150), "conquered": False, "question": "Which register is used to hold the return address?", "options": {"A": "x0", "B": "x1 (ra)", "C": "x2 (sp)"}, "answer": "B"},
    "Eastern Anatolia": {"pos": (750, 260), "conquered": False, "question": "What value does the zero register (x0) always read?", "options": {"A": "-1", "B": "Memory address", "C": "0"}, "answer": "C"},
    "S.Eastern Anatolia": {"pos": (680, 410), "conquered": False, "question": "Which instruction is used to add an immediate value to a register?", "options": {"A": "add", "B": "addi", "C": "addu"}, "answer": "B"}
}

# LEVEL 2: MEDIUM (DUZCE)
data_medium = {
    "Akçakoca": {"pos": (320, 130), "conquered": False, "question": "What does the RISC-V 'JAL' (Jump and Link) instruction do?", "options": {"A": "Jumps and saves the return address", "B": "Only jumps", "C": "Reads from memory"}, "answer": "A"},
    "Cumayeri": {"pos": (150, 220), "conquered": False, "question": "Which bits of the register does the LUI instruction write to?", "options": {"A": "Lower 12 bits", "B": "Upper 20 bits", "C": "All bits"}, "answer": "B"},
    "Gümüşova": {"pos": (170, 280), "conquered": False, "question": "How many bits long is each instruction in the RV32I architecture?", "options": {"A": "16 bits", "B": "32 bits", "C": "64 bits"}, "answer": "B"},
    "Çilimli": {"pos": (260, 250), "conquered": False, "question": "What does AUIPC stand for?", "options": {"A": "Add Upper Immediate to PC", "B": "Arithmetic Unit PC", "C": "Add Unsigned PC"}, "answer": "A"},
    "Düzce": {"pos": (400, 280), "conquered": False, "question": "What is filled into the emptied bits in the Shift Left Logical (sll) instruction?", "options": {"A": "1", "B": "0", "C": "Sign bit"}, "answer": "B"},
    "Gölyaka": {"pos": (200, 390), "conquered": False, "question": "Which RISC-V register is used as the 'Stack Pointer' (sp)?", "options": {"A": "x1", "B": "x2", "C": "x3"}, "answer": "B"},
    "Kaynaşlı": {"pos": (420, 350), "conquered": False, "question": "In the 'Store Word' (sw) format, which register holds the memory base address?", "options": {"A": "rs1", "B": "rs2", "C": "rd"}, "answer": "A"},
    "Yığılca": {"pos": (590, 200), "conquered": False, "question": "What does Little-Endian ordering mean in RISC-V?", "options": {"A": "Lowest byte at lowest address", "B": "Highest byte at lowest address", "C": "Random"}, "answer": "A"}
}

# LEVEL 3: HARD (MARMARA)
data_hard = {
    "Edirne": {"pos": (120, 220), "conquered": False, "question": "How does the 'blt' (Branch if Less Than) instruction compare?", "options": {"A": "Signed", "B": "Unsigned", "C": "Neither"}, "answer": "A"},
    "Kırklareli": {"pos": (330, 90), "conquered": False, "question": "What is used in hardware to resolve data hazards?", "options": {"A": "Branch Prediction", "B": "Forwarding (Bypass)", "C": "Cache"}, "answer": "B"},
    "Tekirdağ": {"pos": (330, 200), "conquered": False, "question": "Which instruction is used to read/write the Control and Status Register?", "options": {"A": "csrrw", "B": "csrread", "C": "lcsr"}, "answer": "A"},
    "İstanbul": {"pos": (530, 220), "conquered": False, "question": "In M-mode, which register bit globally disables interrupts?", "options": {"A": "MIE", "B": "SIE", "C": "UIE"}, "answer": "A"},
    "Kocaeli": {"pos": (680, 240), "conquered": False, "question": "For what purpose is the 'ebreak' instruction used?", "options": {"A": "To exit a loop", "B": "To trigger a debugger", "C": "To shut down system"}, "answer": "B"},
    "Sakarya": {"pos": (800, 250), "conquered": False, "question": "In RV64I, how many bytes of data does 'ld' (Load Doubleword) read?", "options": {"A": "4 Bytes", "B": "8 Bytes", "C": "16 Bytes"}, "answer": "B"},
    "Yalova": {"pos": (610, 290), "conquered": False, "question": "What happens if Branch Prediction fails?", "options": {"A": "Pipeline is Flushed", "B": "Stall occurs", "C": "System crashes"}, "answer": "A"},
    "Bilecik": {"pos": (760, 360), "conquered": False, "question": "How is the target address of the JALR instruction calculated?", "options": {"A": "PC + Immediate", "B": "rs1 + Immediate", "C": "rs1 + rs2"}, "answer": "B"},
    "Bursa": {"pos": (550, 380), "conquered": False, "question": "In the RISC-V Vector (RVV) extension, what does 'vsetvli' determine?", "options": {"A": "Vector length/type", "B": "Number of vector registers", "C": "Address"}, "answer": "A"},
    "Balıkesir": {"pos": (400, 420), "conquered": False, "question": "In the privileged architecture, what does the 'mret' instruction do?", "options": {"A": "Return from an interrupt handler", "B": "Write to memory", "C": "System reset"}, "answer": "A"},
    "Çanakkale": {"pos": (220, 390), "conquered": False, "question": "In the RV 'F' (Single-Precision Float) extension, how many f registers are there?", "options": {"A": "16", "B": "32", "C": "64"}, "answer": "B"}
}

# Game Variables
state = "MENU" 
current_regions = {}
active_region = None
result_message = ""
is_correct = False
result_time = 0
active_map_img = None

def reset_game(dataset, map_type):
    global current_regions, state, active_map_img
    current_regions = {k: v.copy() for k, v in dataset.items()} 
    for b in current_regions.values():
        b["conquered"] = False
    active_map_img = maps[map_type]
    state = "MAP"

def draw_text(text, font, color, x, y, center=False, bg=True, bg_alpha=170):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center: rect.center = (x, y)
    else: rect.topleft = (x, y)
    
    if bg:
        bg_surface = pygame.Surface((rect.width + 16, rect.height + 8))
        bg_surface.set_alpha(bg_alpha)
        bg_surface.fill(BLACK)
        bg_rect = bg_surface.get_rect(center=rect.center)
        screen.blit(bg_surface, bg_rect)
        
    screen.blit(text_surface, rect)
    return rect

clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "MENU":
                if 200 <= mouse_pos[0] <= 700:
                    if 220 <= mouse_pos[1] <= 290: reset_game(data_easy, "easy")
                    elif 320 <= mouse_pos[1] <= 390: reset_game(data_medium, "medium")
                    elif 420 <= mouse_pos[1] <= 490: reset_game(data_hard, "hard")
            
            elif state == "MAP":
                if 720 <= mouse_pos[0] <= 880 and 20 <= mouse_pos[1] <= 60:
                    state = "MENU"
                    continue

                for name, data in current_regions.items():
                    distance = ((mouse_pos[0] - data["pos"][0])**2 + (mouse_pos[1] - data["pos"][1])**2)**0.5
                    if distance <= 30 and not data["conquered"]:
                        active_region = name
                        state = "QUESTION"
                        break
                        
            elif state == "QUESTION":
                selection = None
                if 150 <= mouse_pos[0] <= 750:
                    if 280 <= mouse_pos[1] <= 340: selection = "A"
                    elif 360 <= mouse_pos[1] <= 420: selection = "B"
                    elif 440 <= mouse_pos[1] <= 500: selection = "C"
                
                if selection:
                    if selection == current_regions[active_region]["answer"]:
                        current_regions[active_region]["conquered"] = True
                        result_message = "CORRECT! REGION CONQUERED!"
                        is_correct = True
                    else:
                        result_message = f"WRONG! CORRECT ANSWER: {current_regions[active_region]['answer']}"
                        is_correct = False
                    
                    state = "RESULT"
                    result_time = pygame.time.get_ticks()

    # --- SCREEN DRAWING ---
    if state == "MENU":
        screen.fill(BG_COLOR)
        draw_text("KNOW AND CONQUER: RISC-V", title_font, YELLOW, WIDTH//2, 100, center=True, bg=False)
        draw_text("Choose Your Target, Commander!", question_font, WHITE, WIDTH//2, 160, center=True, bg=False)
        
        buttons = [
            ("EASY: Map of Turkey (7 Regions)", 220, GREEN),
            ("MEDIUM: Map of Düzce (8 Districts)", 320, BLUE),
            ("HARD: Map of Marmara (11 Provinces)", 420, RED)
        ]
        
        for text, y, color in buttons:
            rect = pygame.Rect(200, y, 500, 70) 
            b_color = YELLOW if rect.collidepoint(mouse_pos) else color
            pygame.draw.rect(screen, b_color, rect, border_radius=15)
            pygame.draw.rect(screen, WHITE, rect, 3, border_radius=15)
            draw_text(text, button_font, WHITE if b_color != YELLOW else BLACK, WIDTH//2, y + 35, center=True, bg=False)

    elif state == "MAP":
        screen.fill(BG_COLOR)
        if active_map_img:
            screen.blit(active_map_img, (0, 0))
        
        reset_rect = pygame.Rect(720, 20, 160, 40) 
        r_color = RED if reset_rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(screen, r_color, reset_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, reset_rect, 2, border_radius=8)
        draw_text("Return to Menu", small_font, WHITE, 800, 40, center=True, bg=False)
        
        conquered_count = sum(1 for b in current_regions.values() if b["conquered"])
        if conquered_count == len(current_regions):
            draw_text("ALL REGIONS CONQUERED! CONGRATULATIONS!", winner_font, GREEN, WIDTH//2, 580, center=True, bg_alpha=200)

        for name, data in current_regions.items():
            color = GREEN if data["conquered"] else RED 
            distance = ((mouse_pos[0] - data["pos"][0])**2 + (mouse_pos[1] - data["pos"][1])**2)**0.5
            if distance <= 30 and not data["conquered"]:
                color = YELLOW 
                
            pygame.draw.circle(screen, color, data["pos"], 20)
            pygame.draw.circle(screen, WHITE, data["pos"], 20, 3) 
            
            draw_text(name, small_font, WHITE, data["pos"][0], data["pos"][1] + 30, center=True)

    elif state == "QUESTION":
        screen.fill(QUESTION_BG)

        b_data = current_regions[active_region]
        draw_text(f"Target: {active_region}", title_font, RED, WIDTH//2, 80, center=True, bg=False)
        
        draw_text(b_data["question"], question_font, YELLOW, WIDTH//2, 180, center=True, bg=False)
        
        options = [("A", 280), ("B", 360), ("C", 440)]
        for letter, y in options:
            rect = pygame.Rect(150, y, 600, 60)
            b_color = DARK_GRAY if rect.collidepoint(mouse_pos) else GRAY
            pygame.draw.rect(screen, b_color, rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, rect, 3, border_radius=10)
            
            letter_bg = pygame.Rect(150, y, 60, 60)
            pygame.draw.rect(screen, BLUE, letter_bg, border_top_left_radius=10, border_bottom_left_radius=10)
            pygame.draw.rect(screen, WHITE, letter_bg, 3, border_top_left_radius=10, border_bottom_left_radius=10)
            
            text_surface = button_font.render(letter, True, WHITE)
            screen.blit(text_surface, text_surface.get_rect(center=(180, y + 30)))
            
            option_text = option_font.render(b_data["options"][letter], True, WHITE)
            screen.blit(option_text, (230, y + 17))

    elif state == "RESULT":
        # Green background for correct, Red for wrong
        bg_color_result = GREEN if is_correct else RED
        screen.fill(bg_color_result)
        
        # White text in center
        draw_text(result_message, title_font, WHITE, WIDTH//2, HEIGHT//2, center=True, bg=False)
        
        if pygame.time.get_ticks() - result_time > 2000: # 2 seconds delay
            state = "MAP"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
