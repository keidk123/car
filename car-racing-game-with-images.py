import pygame
import random
import sys
import os
import time

# تهيئة مكتبة pygame
pygame.init()

# أبعاد الشاشة
WIDTH = 800
HEIGHT = 600

# الألوان
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# إنشاء الشاشة
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة سباق السيارات")

# تحميل الصور
def load_images():
    # ملاحظة: يجب أن تكون الصور موجودة في نفس المجلد مع هذا الملف
    # أو يمكنك تعديل المسارات لتناسب تنظيم ملفاتك
    
    try:
        # محاولة تحميل الصور الفعلية
        player_car = pygame.image.load("car0.png").convert_alpha()
        enemy_car = pygame.image.load("car1.png").convert_alpha()
        road_image = pygame.image.load("rode.png").convert()
        splash_image = pygame.image.load("splash.jpg").convert_alpha()
        
    except pygame.error as e:
        # إذا لم تكن الصور موجودة، سنقوم بإنشاء صور بديلة
        print(f"تعذر تحميل بعض الصور. سيتم استخدام الصور الافتراضية. {e}")
        
        # إنشاء صورة سيارة اللاعب
        player_car = pygame.Surface((50, 100), pygame.SRCALPHA)
        pygame.draw.rect(player_car, RED, (0, 0, 50, 100))
        pygame.draw.rect(player_car, (150, 0, 0), (5, 10, 40, 80))
        pygame.draw.rect(player_car, BLACK, (5, 15, 10, 20))  # نافذة
        pygame.draw.rect(player_car, BLACK, (35, 15, 10, 20))  # نافذة
        pygame.draw.rect(player_car, BLACK, (10, 60, 30, 30))  # نافذة خلفية
        
        # إنشاء صورة سيارة العدو
        enemy_car = pygame.Surface((50, 100), pygame.SRCALPHA)
        pygame.draw.rect(enemy_car, BLUE, (0, 0, 50, 100))
        pygame.draw.rect(enemy_car, (0, 0, 150), (5, 10, 40, 80))
        pygame.draw.rect(enemy_car, BLACK, (5, 15, 10, 20))  # نافذة
        pygame.draw.rect(enemy_car, BLACK, (35, 15, 10, 20))  # نافذة
        pygame.draw.rect(enemy_car, BLACK, (10, 60, 30, 30))  # نافذة خلفية
        
        # إنشاء صورة الطريق
        road_image = pygame.Surface((WIDTH, HEIGHT))
        road_image.fill((50, 50, 50))  # لون الإسفلت الرمادي

        # إنشاء صورة الشاشة الافتتاحية
        splash_image = pygame.Surface((WIDTH, HEIGHT))
        splash_image.fill(BLACK)
        font = pygame.font.SysFont(None, 72)
        title = font.render("لعبة سباق السيارات", True, RED)
        splash_image.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - title.get_height()//2))
    
    # تحجيم الصور إذا لزم الأمر
    player_car = pygame.transform.scale(player_car, (60, 120))
    enemy_car = pygame.transform.scale(enemy_car, (60, 120))
    road_image = pygame.transform.scale(road_image, (WIDTH, HEIGHT))
    splash_image = pygame.transform.scale(splash_image, (WIDTH, HEIGHT))
    
    return player_car, enemy_car, road_image, splash_image

# عرض شاشة البداية
def show_splash_screen(splash_image, duration=2):
    start_time = time.time()
    running = True
    
    while running and time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # السماح للاعب بتخطي شاشة البداية بالضغط على أي مفتاح
            elif event.type == pygame.KEYDOWN:
                running = False
        
        screen.blit(splash_image, (0, 0))
        pygame.display.flip()

# فئة سيارة اللاعب
class PlayerCar:
    def __init__(self, car_image):
        self.image = car_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed = 7
        
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# فئة سيارة العدو
class EnemyCar:
    def __init__(self, car_image):
        self.image = car_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(4, 8)
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            return True
        return False
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# فئة الطريق المتحرك
class Road:
    def __init__(self, road_image):
        self.image = road_image
        self.y1 = 0
        self.y2 = -HEIGHT
        self.speed = 5
        self.line_width = 10
        self.line_height = 50
        self.line_gap = 50
        
    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed
        
        if self.y1 >= HEIGHT:
            self.y1 = -HEIGHT
        
        if self.y2 >= HEIGHT:
            self.y2 = -HEIGHT
    
    def draw(self, surface):
        # رسم صورة الطريق مرتين للحصول على تأثير التمرير المستمر
        surface.blit(self.image, (0, self.y1))
        surface.blit(self.image, (0, self.y2))
        
        # رسم خطوط الطريق
        # y = -self.line_height
        # while y < HEIGHT:
        #    pygame.draw.rect(surface, YELLOW, (WIDTH // 2 - self.line_width // 2, y, self.line_width, self.line_height))
        #    y += self.line_height + self.line_gap

# فئة للتأثيرات الصوتية والموسيقى
class SoundEffects:
    def __init__(self):
        self.has_sound = False
        try:
            pygame.mixer.init()
            self.crash_sound = pygame.mixer.Sound("crash.mp3")
            self.point_sound = pygame.mixer.Sound("point.mp3")
            self.has_sound = True
            
            # محاولة تحميل وتشغيل موسيقى الخلفية
            pygame.mixer.music.load("background_music.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # تشغيل الموسيقى بشكل متكرر
        except Exception as e:
            print(f"تعذر تحميل ملفات الصوت. سيتم تعطيل المؤثرات الصوتية. {e}")
    
    def play_crash(self):
        if self.has_sound:
            self.crash_sound.play()
    
    def play_point(self):
        if self.has_sound:
            self.point_sound.play()

# الدالة الرئيسية للعبة
def main():
    clock = pygame.time.Clock()
    running = True
    game_over = False
    score = 0
    level = 1
    enemy_frequency = 60  # كل كم إطار يتم إنشاء عدو جديد
    frame_count = 0
    
    # تحميل الصور
    player_car_img, enemy_car_img, road_img, splash_img = load_images()
    
    # عرض شاشة البداية لمدة ثانيتين
    show_splash_screen(splash_img, 2)
    
    # إنشاء الكائنات
    player = PlayerCar(player_car_img)
    road = Road(road_img)
    enemies = []
    
    # تهيئة المؤثرات الصوتية
    sounds = SoundEffects()
    
    # الخط المستخدم للنصوص
    font = pygame.font.SysFont(None, 36)
    
    while running:
        # معالجة الأحداث
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    # إعادة تشغيل اللعبة
                    game_over = False
                    score = 0
                    level = 1
                    enemies.clear()
                    player.rect.center = (WIDTH // 2, HEIGHT - 100)
                    enemy_frequency = 60
        
        if not game_over:
            # تحريك اللاعب
            keys = pygame.key.get_pressed()
            player.move(keys)
            
            # تحديث الطريق
            road.update()
            
            # إنشاء أعداء جدد
            frame_count += 1
            if frame_count >= enemy_frequency:
                enemies.append(EnemyCar(enemy_car_img))
                frame_count = 0
            
            # تحديث الأعداء
            for enemy in enemies[:]:
                if enemy.update():
                    enemies.remove(enemy)
                    score += 1
                    sounds.play_point()
                    # زيادة مستوى الصعوبة كل 10 نقاط
                    if score % 10 == 0:
                        level += 1
                        enemy_frequency = max(10, 60 - level * 5)
            
            # فحص الاصطدام
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    sounds.play_crash()
                    game_over = True
            
            # الرسم
            road.draw(screen)
            player.draw(screen)
            
            for enemy in enemies:
                enemy.draw(screen)
            
            # عرض النتيجة والمستوى
            score_text = font.render(f"scoring: {score}", True, WHITE)
            level_text = font.render(f"level: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))
        
        else:
            # عرض شاشة انتهاء اللعبة
            game_over_text = font.render("Game Over!", True, RED)
            score_text = font.render(f"Score: {score}", True, WHITE)
            restart_text = font.render(" ENTER ", True, GREEN)
            
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

# تشغيل اللعبة
if __name__ == "__main__":
    main()
