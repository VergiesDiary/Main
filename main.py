import pygame
import random
import sys
from time import sleep as wait

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("UltraBeing")
pygame.display.set_icon(pygame.image.load("icon.png"))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
LIGHT_BLUE = (173, 216, 230)

# Fonts
pygame.font.init()
header_font = pygame.font.SysFont('comicsansms', int(24 * WIDTH / 800), bold=True)
body_font = pygame.font.SysFont('comicsansms', int(18 * WIDTH / 800))
stat_font = pygame.font.SysFont('comicsansms', int(18 * WIDTH / 1000))
cartoon_font = pygame.font.SysFont('comicsansms', int(20 * WIDTH / 800))

# Utility functions
def draw_text(surface, text, font, color, rect):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, rect)

def draw_button(surface, text, font, color, rect):
    pygame.draw.rect(surface, color, rect)
    draw_text(surface, text, font, WHITE, rect.move(10, 5))

def draw_progress_bar(surface, x, y, width, height, percentage, border_color):
    if percentage >= 70:
        fill_color = GREEN
    elif percentage < 70 and percentage >= 50:
        fill_color = ORANGE
    elif percentage < 50 and percentage > 30:
        fill_color = YELLOW
    elif percentage <= 30:
        fill_color = RED
    # Draw border
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2)
    # Draw inner bar (filled based on percentage)
    inner_width = int(width * (percentage / 100))
    pygame.draw.rect(surface, LIGHT_BLUE, (x, y, width, height))
    pygame.draw.rect(surface, fill_color, (x, y, inner_width, height))

last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

class Job:
    def __init__(self, name, rank, progress, reputation, coworkers, supervisor, ranks, income):
        self.name = name
        self.rank = rank
        self.progress = progress
        self.reputation = reputation
        self.coworkers = coworkers
        self.supervisor = supervisor
        self.ranks = ranks
        self.income = income
    
    def pay(self, player):
        player.money += random.randint(self.income // 2, self.income)
    
    def work(self, amount="random"):
        if self.progress < 100:
            if amount == "random":
                self.progress += random.randint(5, 20)
            elif isinstance(amount, int):
                self.progress += amount
            else:
                add_message(player, "Invalid amount!")
            if self.progress > 100:
                self.progress = 100
    
    def promote(self, amount=1):
        ranks = {}
        rev_ranks = {}
        for i, rank in enumerate(self.ranks.keys(), start=1):
            ranks.update({rank: i})
            rev_ranks.update({i: rank})
        next_rank = rev_ranks[ranks[self.rank] + amount]
        self.rank = next_rank
        self.income = self.ranks[self.rank]
        self.add_reputation()
    
    def demote(self, amount=1):
        ranks = {}
        rev_ranks = {}
        for i, rank in enumerate(self.ranks.keys(), start=1):
            ranks.update({rank: i})
            rev_ranks.update({i: rank})
        next_rank = rev_ranks[ranks[self.rank] - amount]
        self.rank = next_rank
        self.income = self.ranks[self.rank]
        self.lose_reputation()
    
    def add_reputation(self, amount="random"):
        if self.reputation < 100:
            if amount == "random":
                self.reputation += random.randint(5, 20)
            elif isinstance(amount, int):
                self.reputation += amount
            else:
                add_message(player, "Invalid amount!")
            if self.reputation > 100:
                self.reputation = 100
                
    def lose_reputation(self, amount="random"):
        if self.reputation < 100:
            if amount == "random":
                self.reputation += random.randint(5, 20)
            elif isinstance(amount, int):
                self.reputation += amount
            else:
                add_message(player, "Invalid amount!")
            if self.reputation > 100:
                self.reputation = 100

class Activity:
    def __init__(self, name, level, skill_boost):
        self.name = name
        self.level = level
        self.skill_boost = skill_boost
    
    def skill_up(self, skill):
        if skill.level < 5:
            skill.level += self.skill_boost
            if skill.level > 5:
                skill.level = 5

def generate_random_name(name_type, last_name=None):
    global last_names
    if name_type == "male":
        first_names = [
            "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
            "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
            "Kenneth", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
            "Jacob", "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin", "Scott", "Brandon",
            "Frank", "Benjamin", "Gregory", "Raymond", "Samuel", "Patrick", "Alexander", "Jack", "Dennis", "Jerry"
        ]
    elif name_type == "female":
        first_names = [
            "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
            "Nancy", "Margaret", "Lisa", "Betty", "Dorothy", "Sandra", "Ashley", "Kimberly", "Donna", "Emily",
            "Michelle", "Carol", "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia",
            "Kathleen", "Amy", "Shirley", "Angela", "Helen", "Anna", "Brenda", "Pamela", "Nicole", "Emma", "Samantha",
            "Katherine", "Christine", "Debra", "Rachel", "Catherine", "Carolyn", "Janet", "Maria", "Heather", "Diane"
        ]
    if name_type in ["male", "female"]:
        if last_name is None:
            last_name = random.choice(last_names)
        
        return random.choice(first_names) + " " + last_name

events = [
    # Events for babies (ages 0-4)
    {"age_range": (0, 4), "type": "neutral", "description": "I said mama."},
    {"age_range": (0, 4), "type": "good", "description": "I got a new toy!", "effect": {"happiness": 10}},
    {"age_range": (0, 4), "type": "bad", "description": "I caught a cold.", "effect": {"health": -10}},
    {"age_range": (0, 4), "type": "good", "description": "I said dada", "effect": {"smarts": 10}},
    {"age_range": (0, 4), "type": "neutral", "description": "I had a quiet day at home."},
    # Events for children (ages 5-12)
    {"age_range": (5, 12), "type": "bad", "description": "I fell off my bike and scraped my knee.", "effect": {"health": -5}},
    {"age_range": (5, 12), "type": "neutral", "description": "I had a fun day at the park."},
    {"age_range": (5, 12), "type": "good", "description": "I got a new toy!", "effect": {"happiness": 10}},
    {"age_range": (5, 12), "type": "bad", "description": "I caught a cold.", "effect": {"health": -10}},
    {"age_range": (5, 12), "type": "good", "description": "I won a class spelling bee!", "effect": {"smarts": 10}},
    {"age_range": (5, 12), "type": "neutral", "description": "I had a quiet day at school."},
    {"age_range": (5, 12), "type": "bad", "description": "I got into a fight with a classmate.", "effect": {"happiness": -10, "health": -5}},
    # Events for teenagers (ages 13-19)
    {"age_range": (13, 19), "type": "bad", "description": "I got grounded for breaking curfew.", "effect": {"happiness": -15}},
    {"age_range": (13, 19), "type": "neutral", "description": "I spent the day playing video games."},
    {"age_range": (13, 19), "type": "bad", "description": "I got into a car accident. -$200, -20 health.", "effect": {"money": -200, "health": -20}},
    # Events for young adults (ages 20-35)
    {"age_range": (20, 35), "type": "neutral", "description": "I had a relaxing weekend."},
    {"age_range": (20, 35), "type": "neutral", "description": "I watched a movie."},
    {"age_range": (20, 35), "type": "bad", "description": "I got into a car accident. -$500, -20 health.", "effect": {"money": -500, "health": -20}},
    # Events for middle-aged adults (ages 36-55)
    {"age_range": (36, 55), "type": "bad", "description": "I had a mid-life crisis.", "effect": {"happiness": -20}},
    {"age_range": (36, 55), "type": "neutral", "description": "I took up a new hobby."},
    {"age_range": (36, 55), "type": "neutral", "description": "I had a quiet day at home."},
    {"age_range": (36, 55), "type": "good", "description": "I took a vacation to a tropical island.", "effect": {"happiness": 20}},
    {"age_range": (36, 55), "type": "bad", "description": "I were diagnosed with a chronic illness.", "effect": {"health": -30}},
    {"age_range": (36, 55), "type": "neutral", "description": "I spent the weekend with family."},
    # Events for seniors (ages 56+)
    {"age_range": (56, 100), "type": "bad", "description": "I were diagnosed with a serious illness.", "effect": {"health": -50}},
    {"age_range": (56, 100), "type": "good", "description": "I traveled the world!", "effect": {"happiness": 40}},
    {"age_range": (56, 100), "type": "bad", "description": "I had a major surgery.", "effect": {"health": -40}},
    {"age_range": (56, 100), "type": "neutral", "description": "I spent the day gardening."},
    {"age_range": (56, 100), "type": "bad", "description": "I had a fall and broke a bone.", "effect": {"health": -20}},
    {"age_range": (56, 100), "type": "good", "description": "I wrote a memoir.", "effect": {"happiness": 25, "smarts": 10}},
    {"age_range": (56, 100), "type": "neutral", "description": "I reflected on my life."},
]

def random_event(player):
    global events
    
    # Filter events based on age
    available_events = [event for event in events if player.age >= event["age_range"][0] and player.age <= event["age_range"][1]]
    
    event = random.choice(available_events)
    
    if "effect" in event:
        for key, value in event["effect"].items():
            current_value = getattr(player, key)
            if current_value + value > 100:
                setattr(player, key, 100)
            elif current_value + value < 0 and key != "money":
                setattr(player, key, 0)
            else:
                setattr(player, key, current_value + value)
    
    if player.health == 0 or player.age >= player.lifespan:
        player.death()
    else:
        return event["description"]

# Game classes
class Character:
    def __init__(self, npc=False):
            global last_names, jobs
            random_gender = random.choice(["male", "female"])
            self.first_name = generate_random_name(random_gender, None).split()[0]
            self.last_name = generate_random_name(random_gender, None).split()[0]
            self.lifespan = random.randint(0, 200)
            self.health = random.randint(20, 80)
            self.happiness = random.randint(20, 80)
            self.smarts = random.randint(20, 80)
            self.looks = random.randint(20, 80)
            self.craziness = random.randint(20, 80)
            self.willpower = random.randint(20, 80)
            self.sexuality = random.choice(["Straight", "Gay", "Bisexual"])
            self.gender = random_gender.capitalize()
            self.petulance = random.randint(20, 100)
            self.generosity = random.randint(20, 100)
            self.karma = random.randint(20, 100)
            self.job = None
            self.family = {}
            self.mother = None
            self.father = None
            self.is_jr = False
            self.is_sr = False
            month = random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
            day = random.randint(1, 31)
            year = random.choice(["2018", "2019", "2020", "2021", "2022", "2023", "2024"])
            self.birthday = f"{month}, {day}, {year}"
            if npc == False:
                self.age = -1
                self.messages = []
                self.money = 0
                self.education = None
                self.assets = {"cars": {}, "houses": {}}
            else:
                self.age = 0
                self.relationship_with_player = None
                self.money = random.randint(100, 2000)
                self.education = None
                self.assets = {"cars": {}, "houses": {}}
            self.relationships = {}
            self.hobbies = {}
            self.school = {
                "type": "Kindergarten",
                "grade": 0,
                "teachers": {},
                "classmates": {},
                "nurse_visits": 0,
                "activities": {
                    "Art": Activity("Art", 1, 0.5),
                    "Music": Activity("Music", 1, 0.5),
                    "Sports": Activity("Sports", 1, 0.5),
                    "Drama": Activity("Drama", 1, 0.5)
                },
                "taken_activities": {}
            }

    def randomize_stats(self, npc=False):
            global last_names, jobs
            random_gender = random.choice(["male", "female"])
            self.first_name = generate_random_name(random_gender, None).split()[0]
            self.last_name = generate_random_name(random_gender, None).split()[0]
            self.lifespan = random.randint(0, 200)
            self.health = random.randint(20, 80)
            self.happiness = random.randint(20, 80)
            self.smarts = random.randint(20, 80)
            self.looks = random.randint(20, 80)
            self.craziness = random.randint(20, 80)
            self.willpower = random.randint(20, 80)
            self.sexuality = random.choice(["Straight", "Gay", "Bisexual"])
            self.gender = random_gender.capitalize()
            self.petulance = random.randint(20, 100)
            self.generosity = random.randint(20, 100)
            self.karma = random.randint(20, 100)
            self.job = None
            self.family = {}
            self.mother = None
            self.father = None
            self.is_jr = False
            self.is_sr = False
            month = random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
            day = random.randint(1, 31)
            year = random.choice(["2018", "2019", "2020", "2021", "2022", "2023", "2024"])
            self.birthday = f"{month}, {day}, {year}"
            if npc == False:
                self.age = -1
                self.messages = []
                self.money = 0
                self.education = None
                self.assets = {"cars": {}, "houses": {}}
            else:
                self.age = 0
                self.relationship_with_player = None
                self.money = random.randint(100, 2000)
                self.education = None
                self.assets = {"cars": {}, "houses": {}}
            self.relationships = {}
            self.hobbies = {}
            self.school = {
                "type": "Kindergarten",
                "grade": 0,
                "teachers": {},
                "classmates": {},
                "nurse_visits": 0,
                "activities": {
                    "Art": Activity("Art", 1, 0.5),
                    "Music": Activity("Music", 1, 0.5),
                    "Sports": Activity("Sports", 1, 0.5),
                    "Drama": Activity("Drama", 1, 0.5)
                },
                "taken_activities": {}
            }

    def age_up(self):
        self.age += 1
        add_message(self, f"[event_BLUE] Age {self.age}: ", "age")
        if self.age == 1:
            add_message(self, "I started crawling.")
        elif self.age == 3:
            add_message(self, "I started walking.")
        elif self.age == 5:
            add_message(self, "I started talking.")
        elif self.age == 16:
            add_message(self, "I can get a driver's license!")
        if self.age != 0:
            add_message(self, random_event(self))
        else:
            if self.family[self.father].is_sr:
                father_name = f"{self.father} Sr."
            else:
                father_name = self.father
            if self.family[self.mother].is_sr:
                mother_name = f"{self.mother} Sr."
            else:
                mother_name = self.mother
            add_message(self, f"I am {self.first_name} {self.last_name}, a {self.gender}, I was born to {mother_name} and {father_name} on {self.birthday}!")
    
    def generate_family(self, family_type="npc"):
        if family_type == "player":
            last_name = self.last_name
        else:
            last_name = None
        female_name = generate_random_name("female", last_name).split(" ")
        male_name = generate_random_name("male", last_name).split(" ")
        mom = Character(True)
        mom.first_name = female_name[0]
        mom.last_name = female_name[1]
        mom.gender = "Female"
        dad = Character(True)
        dad.first_name = male_name[0]
        dad.last_name = male_name[1]
        dad.gender = "Male"
        self.add_family_member(mom, "Mother")
        self.add_family_member(dad, "Father")
        
        if random.choice([True, False]):
            num_siblings = random.randint(1, 3)
            for _ in range(num_siblings):
                sib_gender = random.choice(["female", "male"])
                sibling_name = generate_random_name(sib_gender, last_name).split(" ")
                sibling = Character(True)
                sibling_first_name = sibling_name[0]
                father_first_name = self.father.split(" ")[0]
                mother_first_name = self.mother.split(" ")[0]

                if sibling_first_name == (father_first_name or mother_first_name):
                    sibling.is_jr = True
                    
                    if sibling_first_name == father_first_name:
                        self.family[self.father].is_sr = True
                    elif sibling_first_name == mother_first_name:
                        self.family[self.mother].is_sr = True

                sibling.first_name = sibling_name[0]
                sibling.last_name = sibling_name[1]
                sibling.gender = sib_gender.capitalize()
                if sibling.gender == "Male":
                    sib_type = "Older Brother"
                else:
                    sib_type = "Older Sister"
                self.add_family_member(sibling, f"{sib_type}")

    def add_family_member(self, member, relationship):
        if relationship == "Mother":
            self.mother = f"{member.first_name} {member.last_name}"
        elif relationship == "Father":
            self.father = f"{member.first_name} {member.last_name}"
        member.relationship_with_player = relationship
        self.family.update({f"{member.first_name} {member.last_name}": member})

    def add_relationship(self, person, relationship="Friend"):
        person.relationship_with_player = relationship
        self.relationships.update({f"{person.first_name} {person.last_name}": person})

    def interact_with_relationship(self, person, interaction_type):
        if f"{person.first_name} {person.last_name}" in self.family:
            if person.relationship_with_player in ["Mother", "Father", "Older Brother", "Older Sister", "Younger Brother", "Younger Sister", "Twin Brother"]:
                person_called = f"my {person.relationship_with_player.lower()}, {person.first_name}"
        if interaction_type == "Spend Time":
            interaction_effect = random.randint(5, 20)
            add_message(self, f"[event_GREEN] I spent time with {person_called}. Closeness increased by {interaction_effect}.")
            person.relationships["Closeness"] = min(person.relationships.get("Closeness", 50) + interaction_effect, 100)
        elif interaction_type == "Argue":
            interaction_effect = random.randint(-20, -5)
            add_message(self, f"[event_RED] I argued with {person_called}. Closeness decreased by {-interaction_effect}.")
            person.relationships["Closeness"] = max(person.relationships.get("Closeness", 50) + interaction_effect, 0)
        elif interaction_type == "Give Gift":
            interaction_effect = random.randint(10, 30)
            add_message(self, f"[event_GREEN] I gave a gift to {person_called}. Closeness increased by {interaction_effect}.")
            person.relationships["Closeness"] = min(person.relationships.get("Closeness", 50) + interaction_effect, 100)
        else:
            add_message(self, "[event_RED] Invalid interaction type.")

    def death(self):
        self.randomize_stats()
        add_message(self, "[event_RED] I died!")
        self.messages.clear()
        initial_aged = False
        self.generate_family("player")

def generate_character(amount=1):
    chars = {}
    for i in range(amount):
        char_gender = random.choice(["male", "female"])
        char_name = generate_random_name(char_gender)
        char = Character(True)
        char.first_name = char_name[0]
        char.last_name = char_name[1]
        char.gender = char_gender.capitalize()
        chars.update({char_name: char})
    return chars

jobs = {
    "Babysitter": Job("Babysitter", "Babysitter", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {"Babysitter": 5000}, 5000),
    "Dog Walker": Job("Dog Walker", "Dog Walker", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {"Dog Walker": 3000}, 3000),
}

# Create player character
player = Character()
player.generate_family("player")

# UI Elements positions
header_height = int(50 * HEIGHT / 600)
footer_height = int(50 * HEIGHT / 600)
message_height = HEIGHT - header_height - 2 * footer_height

header_rect = pygame.Rect(0, 0, WIDTH, header_height)
top_footer_rect = pygame.Rect(0, HEIGHT - 2 * footer_height, WIDTH, footer_height)
bottom_footer_rect = pygame.Rect(0, HEIGHT - footer_height, WIDTH, footer_height)
message_rect = pygame.Rect(0, header_height, WIDTH, message_height)

# Buttons
button_width = int(140 * WIDTH / 800)
button_height = int(40 * HEIGHT / 600)
button_gap = int(10 * WIDTH / 800)

career_button_rect = pygame.Rect(button_gap, HEIGHT - 2 * footer_height + 5, button_width, button_height)
assets_button_rect = pygame.Rect(career_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)
age_up_button_rect = pygame.Rect(assets_button_rect.right + button_gap, career_button_rect.top, button_height, button_height)
relationships_button_rect = pygame.Rect(age_up_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)
activities_button_rect = pygame.Rect(relationships_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)

relationship_menu_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
relationship_buttons = {}

def add_message(player, msg, msg_type="normal"):
    if msg_type == "normal":
        msg = f"    {msg}"
    player.messages.append(msg)

def display_relationships_menu():
    pygame.draw.rect(screen, LIGHT_BLUE, relationship_menu_rect)
    draw_text(screen, "Relationships", header_font, BLACK, (relationship_menu_rect.x + 10, relationship_menu_rect.y + 10))
    
    y_offset = 50
    people = {**player.relationships, **player.family}

    for i, (name, person) in enumerate(people.items()):
        rel_button_rect = pygame.Rect(relationship_menu_rect.x + 20, relationship_menu_rect.y + y_offset, relationship_menu_rect.width - 40, 40)
        
        # Use a tuple of rectangle coordinates and size as the key
        rel_button_key = (rel_button_rect.x, rel_button_rect.y, rel_button_rect.width, rel_button_rect.height)
        relationship_buttons[rel_button_key] = (rel_button_rect, person)  # Store the rect and the person
        
        closeness = person.relationships.get('Closeness', 50)
        if person.is_jr:
            name = f"{name} Jr."
        elif person.is_sr:
            name = f"{name} Sr."
        draw_button(screen, f"{name} - Closeness: {closeness}", body_font, GREEN, rel_button_rect)
        
        y_offset += 50

# Main game loop
running = True
relationships_menu_active = False
initial_aged = False
while running:
    if initial_aged == False:
        player.age_up()
        initial_aged = True
    screen.fill(WHITE)

    # Draw Header
    pygame.draw.rect(screen, BLUE, header_rect)
    if player.gender == "Male":
        gender_char = "M"
    else:
        gender_char = "F"
    draw_text(screen, f"{player.first_name} {player.last_name} ({gender_char})", header_font, WHITE, header_rect.move(10, 10))
    draw_text(screen, "UltraBeing", header_font, WHITE, header_rect.move(WIDTH // 2 - 50, 10))
    if player.money > 0:
        money_color = GREEN
    else:
        money_color = RED
    draw_text(screen, f"Money: ${player.money:,}", header_font, money_color, header_rect.move(WIDTH - 300, 10))

    # Draw Footers
    pygame.draw.rect(screen, BLUE, top_footer_rect)
    pygame.draw.rect(screen, BLUE, bottom_footer_rect)

    # Draw Buttons
    draw_button(screen, "Career", cartoon_font, RED, career_button_rect)
    draw_button(screen, "Assets", cartoon_font, RED, assets_button_rect)
    draw_button(screen, "+", cartoon_font, RED, age_up_button_rect)
    draw_button(screen, "Relationships", cartoon_font, RED, relationships_button_rect)
    draw_button(screen, "Activities", cartoon_font, RED, activities_button_rect)
    
    # Draw Progress Bars for each stat
    bar_x, bar_y = 20, HEIGHT - footer_height - 70  # Initial position of the first bar
    bar_width, bar_height = 200, 20
    bar_y = 690

    # Health Bar
    draw_progress_bar(screen, 140, bar_y, bar_width, bar_height, player.health, BLACK)

    # Happiness Bar
    bar_x += 400  # Move the next bar down
    draw_progress_bar(screen, bar_x, bar_y, bar_width, bar_height, player.happiness, BLACK)

    # Smarts Bar
    bar_x += 300
    draw_progress_bar(screen, bar_x, bar_y, bar_width, bar_height, player.smarts, BLACK)

    # Looks Bar
    bar_x += 300
    draw_progress_bar(screen, bar_x, bar_y, bar_width, bar_height, player.looks, BLACK)

    # Define stats
    stats = {
        "Health": player.health,
        "Happpiness": player.happiness,
        "Smarts": player.smarts,
        "Looks": player.looks
    }

    # Draw Stats
    img_placeholder = f"[IMG]"
    draw_text(screen, img_placeholder, stat_font, WHITE, bottom_footer_rect.move(10, 10))
    
    # Draw health text
    health_txt = f"Health: {player.health}%"
    draw_text(screen, health_txt, stat_font, WHITE, bottom_footer_rect.move(200, 23))
    
    # Draw happiness text
    happiness_txt = f"Happiness: {player.happiness}%"
    draw_text(screen, happiness_txt, stat_font, WHITE, bottom_footer_rect.move(450, 23))
    
    # Draw smarts text
    smarts_txt = f"Smarts: {player.smarts}%"
    draw_text(screen, smarts_txt, stat_font, WHITE, bottom_footer_rect.move(780, 23))
    
    # Draw looks text
    looks_txt = f"Looks: {player.looks}%"
    draw_text(screen, looks_txt, stat_font, WHITE, bottom_footer_rect.move(1100, 23))

    # Draw Messages
    for i, msg in enumerate(player.messages[-17:]):
        color_events = ["[event_RED]", "[event_GREEN]", "[event_BLUE]", "[event_ORANGE]", "[event_YELLOW]", "[event_LIGHT_BLUE]", "[event_WHITE]"]
        if msg.startswith("[event_RED]") or msg.startswith("    [event_RED]"):
            msg = msg.replace("[event_RED]", "")
            draw_text(screen, msg, body_font, RED, message_rect.move(10, 10 + i * 30))
        elif msg.startswith("[event_GREEN]") or msg.startswith("    [event_GREEN]"):
            msg = msg.replace("[event_GREEN]", "")
            draw_text(screen, msg, body_font, GREEN, message_rect.move(10, 10 + i * 30))
        elif msg.startswith("[event_BLUE]") or msg.startswith("    [event_BLUE]"):
            msg = msg.replace("[event_BLUE]", "")
            draw_text(screen, msg, body_font, BLUE, message_rect.move(10, 10 + i * 30))
        elif msg.startswith("[event_ORANGE]") or msg.startswith("    [event_ORANGE]"):
            msg = msg.replace("[event_ORANGE]", "")
            draw_text(screen, msg, body_font, ORANGE, message_rect.move(10, 10 + i * 30))
        elif msg.startswith("[event_YELLOW]") or msg.startswith("    [event_YELLOW]"):
            msg = msg.replace("[event_YELLOW]", "")
            draw_text(screen, msg, body_font, YELLOW, message_rect.move(10, 10 + i * 30))
        elif msg.startswith("[event_LIGHT_BLUE]") or msg.startswith("    [event_LIGHT_BLUE]"):
            msg = msg.replace("[event_LIGHT_BLUE]", "")
            draw_text(screen, msg, body_font, LIGHT_BLUE, message_rect.move(10, 10 + i * 30))
        elif msg.startswith("[event_WHITE]") or msg.startswith("    [event_WHITE]"):
            msg = msg.replace("[event_WHITE]", "")
            draw_text(screen, msg, body_font, WHITE, message_rect.move(10, 10 + i * 30))
        else:
            draw_text(screen, msg, body_font, BLACK, message_rect.move(10, 10 + i * 30))

    # Handle relationship menu display
    if relationships_menu_active:
        display_relationships_menu()

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if relationships_menu_active:
                for rel_button_key, (rel_button_rect, person) in relationship_buttons.items():
                    if rel_button_rect.collidepoint(x, y):
                        player.interact_with_relationship(person, "Spend Time")
                relationships_menu_active = False
            elif career_button_rect.collidepoint(x, y):
                add_message(player, "[event_RED] Career feature not implemented yet.")
            elif assets_button_rect.collidepoint(x, y):
                add_message(player, "[event_RED] Assets feature not implemented yet.")
            elif age_up_button_rect.collidepoint(x, y):
                player.age_up()
            elif relationships_button_rect.collidepoint(x, y):
                relationships_menu_active = True
            elif activities_button_rect.collidepoint(x, y):
                add_message(player, "[event_RED] Activities feature not implemented yet.")
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            header_height = int(50 * HEIGHT / 600)
            footer_height = int(50 * HEIGHT / 600)
            message_height = HEIGHT - header_height - 2 * footer_height

            header_rect = pygame.Rect(0, 0, WIDTH, header_height)
            top_footer_rect = pygame.Rect(0, HEIGHT - 2 * footer_height, WIDTH, footer_height)
            bottom_footer_rect = pygame.Rect(0, HEIGHT - footer_height, WIDTH, footer_height)
            message_rect = pygame.Rect(0, header_height, WIDTH, message_height)

            button_width = int(140 * WIDTH / 800)
            button_height = int(40 * HEIGHT / 600)
            button_gap = int(10 * WIDTH / 800)

            career_button_rect = pygame.Rect(button_gap, HEIGHT - 2 * footer_height + 5, button_width, button_height)
            assets_button_rect = pygame.Rect(career_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)
            age_up_button_rect = pygame.Rect(assets_button_rect.right + button_gap, career_button_rect.top, button_height, button_height)
            user_stats_button_rect = pygame.Rect(age_up_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)
            other_button_rect = pygame.Rect(user_stats_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)

            header_font = pygame.font.SysFont('comicsansms', int(24 * WIDTH / 800), bold=True)
            body_font = pygame.font.SysFont('comicsansms', int(18 * WIDTH / 800))
            cartoon_font = pygame.font.SysFont('comicsansms', int(24 * WIDTH / 800))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
