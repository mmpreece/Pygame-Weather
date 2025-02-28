# mason.mmp.work@gmail.com

import pygame, weather
from datetime import datetime

# Initialize Pygame, set up window
pygame.init()
SCREEN = pygame.display.set_mode((400, 525))
pygame.display.set_caption("Weather")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Global variables
BG_COLOUR = (62, 69, 81)
BLACK = (0, 0, 0)
CITY = weather.get_city()
SELECTED_DAY: int = 0
clock = pygame.time.Clock()
init_box_y_upper: int = 525/2
init_box_y_lower: int = 525/2

mask = pygame.Surface((317, 421), pygame.SRCALPHA)
pygame.draw.rect(mask, (BG_COLOUR), (0, 0, 317, 421))
pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, 317, 421), border_radius=15)

font_temperature = pygame.font.Font(None, 80)
font_city = pygame.font.Font(None, 39)
font_date = pygame.font.Font(None, 20)
font_fah = pygame.font.Font(None, 35)
font_time = pygame.font.Font(None, 60)

""" Licensed font ver
font_temperature = pygame.font.Font("fonts/Segoe UI Bold.ttf", 45)
font_city = pygame.font.Font(None, 39)
font_date = pygame.font.Font("fonts/Segoe UI.ttf", 20)
font_fah = pygame.font.Font("fonts/Minerva Modern Bold.otf", 20)
font_time = pygame.font.Font("fonts/Minerva Modern Bold.otf", 40)

"""

# Weather for this week
DAY_0 = weather.WeatherData(0, CITY)
DAY_1 = weather.WeatherData(1, CITY)
DAY_2 = weather.WeatherData(2, CITY)
DAY_3 = weather.WeatherData(3, CITY)
DAY_4 = weather.WeatherData(4, CITY)
DAY_5 = weather.WeatherData(5, CITY)
DAY_6 = weather.WeatherData(6, CITY)

# Global functions
def get_date_time() -> tuple:
    NOW = datetime.now()
    HOUR = NOW.hour
    MINUTE = NOW.minute
    MONTH = NOW.month
    DAY = NOW.day
    DAY_OF_WEEK = NOW.strftime("%a")

    return HOUR, MINUTE, MONTH, DAY, DAY_OF_WEEK

def fetch_weather_icon(weather_code: int, hour: int) -> str:
    local_weather_code: int = weather_code
    weather_icon: str = None
    
    # Get the weather icon
    match local_weather_code:
        case 0: # Clear skies
            weather_icon = "img/weather_icon/sunny.png"

            if hour > 20:
                weather_icon = "img/weather_icon/nighttime.png"
        case 1: # Mainly clear
           weather_icon = "img/weather_icon/partly_cloudy.png"
        case 2: # Partly cloudy
            weather_icon = "img/weather_icon/partly_cloudy.png"
        case 3: # Overcast
            weather_icon = "img/weather_icon/overcast.png"
        case 45 | 48: # Fog
            weather_icon = "img/weather_icon/fog.png"
        case 51 | 52 | 53 | 54 | 55: # Drizzle
            weather_icon = "img/weather_icon/drizzle.png"
        case 61 | 62 | 63 | 64 | 65: # Rain
            weather_icon = "img/weather_icon/rain.png"
        case 71 | 72 | 73 | 74 | 75: # Snow
            weather_icon = "img/weather_icon/snow.png"
        case 80 | 81 | 82: # Rain showers
            weather_icon = "img/weather_icon/rain.png"
        case 95 | 96 | 97 | 98 | 99: # Thunder storms
            weather_icon = "img/weather_icon/thunderstorm.png"
        case _: # Case else
            weather_icon = "img/weather_icon/nighttime.png"

    if weather_icon is not None:
        del local_weather_code
        return weather_icon

def increment_time(day: int, month: int, change: int) -> int:
    local_day = day
    local_month = month
    local_change = change

    local_day += local_change

    match local_month:
        case 1, 3, 5, 7, 8, 10, 12: # 31
            if local_day > 31:
                local_month += 1
                local_day = abs(31 - local_day)
        case 4, 6, 9, 11: # 30
            if local_day > 30:
                local_month += 1
                local_day = abs(30 - local_day)
        case 2: # 28
            if local_day > 28:
                local_month += 1
                local_day = abs(28 - local_day)

    day = local_day
    month = local_month
    return day, month

def increment_day_of_week(day_of_the_week: str, change: int) -> str:
    local_day_of_the_week = day_of_the_week
    
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]
    pos_in_arr = 0

    for i in range(0, 7):
        if weekdays[i] == day_of_the_week:
            pos_in_arr = i
            break

    new_day = pos_in_arr + change
    str_day = "Mon"

    if new_day <= -1:
        str_day = weekdays[6 - pos_in_arr]
    elif new_day >= 7:
        str_day =  weekdays[pos_in_arr - 1]
    else:
        str_day = weekdays[new_day]
     
    return str_day

def fetch_bg_image(hour: int, weather_code: int) -> str:
    local_hour: int = hour
    local_weather_code: int = weather_code

    if local_hour > 18: # If nighttime
        del local_hour
    
        match local_weather_code:
            case 0:
                return "img/bg/night/bg_nighttime.png"
            case 1:
                return "img/bg/night/bg_nighttime.png"
            case 2:
                return "img/bg/night/bg_nighttime.png"
            case 3:
                return "img/bg/night/bg_fog.png"
            case 45 | 48:
                return "img/bg/night/bg_fog.png"
            case 51 | 52 | 53 | 54 | 55:
                return "img/bg/night/bg_drizzle.png"
            case 61 | 62 | 63 | 64 | 65:
                return "img/bg/night/bg_rain.png"
            case 71 | 72 | 73 | 74 | 75:
                return "img/bg/night/bg_snow.png"
            case 80 | 81 | 82:
                return "img/bg/night/bg_rain.png"
            case 95 | 96 | 97 | 98 | 99:
                return "img/bg/night/bg_thunderstorms.png"
            case _:
                return "img/bg/night/bg_nighttime.png"
    else: # If daytime
        del local_hour

        match local_weather_code:
            case 0:
                return "img/bg/day/bg_sunny.png"
            case 1:
                return "img/bg/day/bg_partly_cloudy.png"
            case 2:
                return "img/bg/day/bg_partly_cloudy.png"
            case 3:
                return "img/bg/day/bg_overcast.png"
            case 45 | 48:
                return "img/bg/day/bg_fog.png"
            case 51 | 52 | 53 | 54 | 55:
                return "img/bg/day/bg_rain.png"
            case 61 | 62 | 63 | 64 | 65:
                return "img/bg/day/bg_rain.png"
            case 71 | 72 | 73 | 74 | 75:
                return "img/bg/day/bg_snow.png"
            case 80 | 81 | 82:
                return "img/bg/day/bg_rain.png"
            case 95 | 96 | 97 | 98 | 99:
                return "img/bg/day/bg_thunderstorm.png"
            case _:
                return "img/bg/day/bg_sunny.png"
        
# Sprite
class SpriteBackground(pygame.sprite.Sprite):
    _spr_width: int = 0
    _spr_height: int = 0
    _spr_colour = None

    def __init__(self, spr_width, spr_height, colour) -> None:
        super().__init__()
        self._spr_width = spr_height
        self._spr_height = spr_height
        self._spr_colour = colour
    
        self.image = pygame.Surface((self._spr_width, self._spr_height))
        self.rect = self.image.get_rect()
        self.rect.center = (self._spr_width // 2, self._spr_height // 2)

    def update(self) -> None:
        self.rect.x = 41
        self.rect.y = 80

# Check if a city has been fetched
while True:
    if CITY is not None:
        break
    else:
        CITY = "Cardiff"
        break

# Create sprite group for the background
bg_sprites_group = pygame.sprite.Group()
background_sprite = SpriteBackground(10, 10, BLACK)
bg_sprites_group.add(background_sprite)

# Run main loop if Pygame is initiated
if pygame.get_init():
    running: bool = True
    # Main loop
    while running:

        # Set variables for this loop
        CURRENT_WEATHER_CLASS = None
        CURRENT_HOUR, CURRENT_MINUTE, CURRENT_MONTH, CURRENT_DAY, CURRENT_DAY_OF_WEEK = get_date_time()

        # Input register
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # If "W" is pressed
                    SELECTED_DAY -= 1

                    if SELECTED_DAY < 0:
                        SELECTED_DAY = 0
                elif event.key == pygame.K_d:  # If Escape is pressed
                    SELECTED_DAY += 1

                    if SELECTED_DAY > 6:
                        SELECTED_DAY = 6
        
        match SELECTED_DAY:
            case 0:
                CURRENT_WEATHER_CLASS = DAY_0
            case 1:
                CURRENT_WEATHER_CLASS = DAY_1
            case 2:
                CURRENT_WEATHER_CLASS = DAY_2
            case 3:
                CURRENT_WEATHER_CLASS = DAY_3
            case 4:
                CURRENT_WEATHER_CLASS = DAY_4 
            case 5:
                CURRENT_WEATHER_CLASS = DAY_5
            case 6:
                CURRENT_WEATHER_CLASS = DAY_6
            case _:
                CURRENT_WEATHER_CLASS = DAY_0

        # React to input
        CURRENT_WEATHER_CODE = CURRENT_WEATHER_CLASS._weather_code
        CURRENT_TEMPERATURE = CURRENT_WEATHER_CLASS._temp_mean
        CURRENT_LOCALE = CURRENT_WEATHER_CLASS._location

        # Update sprite
        bg_sprites_group.update()
        bg_sprites_group.draw(SCREEN)

        # Render
        SCREEN.fill(BG_COLOUR) # Background

        # Draw background with masking
        # Dimensions of the bg image: 317 X 421
        temp_cur_weather_bg = fetch_bg_image(CURRENT_HOUR, CURRENT_WEATHER_CODE)
        background_image = pygame.image.load(temp_cur_weather_bg).convert_alpha()

        rounded_image = background_image.copy()
        rounded_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGB_MIN)

        SCREEN.blit(rounded_image, (background_sprite.rect.x, background_sprite.rect.y))

        # Draw lines
        pygame.draw.line(SCREEN, (249, 252, 39), (-20, 0), (400, 0), 50)
        pygame.draw.line(SCREEN, (254, 172, 39), (-30, 0), (425, 0), 46)
        pygame.draw.line(SCREEN, (255, 255, 255), (-40, 0), (450, 0), 42)
        pygame.draw.line(SCREEN, (253, 46, 13), (-50, 0), (475, 0), 38)
        pygame.draw.line(SCREEN, (255, 248, 139), (-60, 0), (500, 0), 34)

        # Draw rectangles
        pygame.draw.rect(SCREEN, (234,234,232), (10, 10, 136, 47), border_radius=10) # Time box
        #pygame.draw.rect(SCREEN, (0 ,0 ,0), (45, 80, 317, 421), border_radius=10) # Placeholder box where the image is displayed

        # Draw Weather Icon
        current_weather_icon = pygame.image.load(fetch_weather_icon(CURRENT_WEATHER_CODE, CURRENT_HOUR))
        SCREEN.blit(current_weather_icon, (65, 99))
        """
        # Draw Data
        # Show temperature
        temp_fahren = round(9/5*(CURRENT_WEATHER_CLASS._temp_mean)+32, 2)

        temp_text = font_temperature.render(f'{CURRENT_WEATHER_CLASS._temp_mean}°C', True, (255, 255, 255))
        SCREEN.blit(temp_text, (150, 89))

        temp_text_fah = font_fah.render(f'{temp_fahren}°F', True, (255, 255, 255))
        SCREEN.blit(temp_text_fah, (150, 140))

        # Show location
        temp_locale = font_city.render(f'{CITY}', True, (255, 255, 255))
        SCREEN.blit(temp_locale, (65, 182))

        # Show date
        temp_current_day, temp_current_month = increment_time(CURRENT_DAY, CURRENT_MONTH, SELECTED_DAY)
        temp_current_weekday = increment_day_of_week(CURRENT_DAY_OF_WEEK, SELECTED_DAY)
        current_date = font_date.render(f'{temp_current_day}/{temp_current_month} - {temp_current_weekday}', True, (255, 255, 255))
        SCREEN.blit(current_date, (65, 207))

        # Show the weather in plain text
        current_weather_pretext = font_date.render(f"{weather.weathercode_decypher(CURRENT_WEATHER_CODE)}", True, (255, 255, 255))
        SCREEN.blit(current_weather_pretext, (62, 465))

        # Show time
        format_minute = None
        format_hour = None

        if CURRENT_MINUTE < 10:
            format_minute = f'0{CURRENT_MINUTE}'
        else:
            format_minute = CURRENT_MINUTE
        
        if CURRENT_HOUR < 10:
            format_hour = f'0{CURRENT_HOUR}'
        else:
            format_hour = CURRENT_HOUR

        text_hour = font_time.render(f'{format_hour}:{format_minute}', True, (0, 0, 0))
        SCREEN.blit(text_hour, (30, 10))
        """

        # Draw Data
        # Show temperature
        temp_fahren = round(9/5*(CURRENT_WEATHER_CLASS._temp_mean)+32, 2)

        temp_text = font_temperature.render(f'{CURRENT_WEATHER_CLASS._temp_mean}°C', True, (255, 255, 255))
        SCREEN.blit(temp_text, (150, 91))

        temp_text_fah = font_fah.render(f'{temp_fahren}°F', True, (255, 255, 255))
        SCREEN.blit(temp_text_fah, (150, 150))

        # Show location
        temp_locale = font_city.render(f'{CITY}', True, (255, 255, 255))
        SCREEN.blit(temp_locale, (65, 182))

        # Show date
        temp_current_day, temp_current_month = increment_time(CURRENT_DAY, CURRENT_MONTH, SELECTED_DAY)
        temp_current_weekday = increment_day_of_week(CURRENT_DAY_OF_WEEK, SELECTED_DAY)
        current_date = font_date.render(f'{temp_current_day}/{temp_current_month} - {temp_current_weekday}', True, (255, 255, 255))
        SCREEN.blit(current_date, (65, 207))

        # Show the weather in plain text
        current_weather_pretext = font_date.render(f"{weather.weathercode_decypher(CURRENT_WEATHER_CODE)}", True, (255, 255, 255))
        SCREEN.blit(current_weather_pretext, (62, 465))

        # Show time
        format_minute = None
        format_hour = None

        if CURRENT_MINUTE < 10:
            format_minute = f'0{CURRENT_MINUTE}'
        else:
            format_minute = CURRENT_MINUTE
        
        if CURRENT_HOUR < 10:
            format_hour = f'0{CURRENT_HOUR}'
        else:
            format_hour = CURRENT_HOUR

        text_hour = font_time.render(f'{format_hour}:{format_minute}', True, (0, 0, 0))
        SCREEN.blit(text_hour, (25,18))

        # Show greeting message
        time_of_day_img = None

        if CURRENT_HOUR < 7:
            time_of_day_img = "img/greeting/0_early_morning.png"

        elif CURRENT_HOUR < 12 & CURRENT_HOUR >= 7:
            time_of_day_img = "img/greeting/1_morning.png"

        elif CURRENT_HOUR >= 12 & CURRENT_HOUR < 17:
            time_of_day_img = "img/greeting/2_daytime.png"

        elif CURRENT_HOUR >= 17 & CURRENT_HOUR < 19:
            time_of_day_img = "img/greeting/3_afternoon.png"

        elif CURRENT_HOUR >= 19:
            time_of_day_img = "img/greeting/4_evening.png"

        if time_of_day_img is not None:
            time_of_day_msg = pygame.image.load(time_of_day_img)
            SCREEN.blit(time_of_day_msg, (160, 26))
    
        clock.tick(25)
        pygame.display.flip() # Update display at the end of the frame

pygame.quit() # End program