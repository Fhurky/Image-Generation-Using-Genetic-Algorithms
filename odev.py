from PIL import Image, ImageDraw, ImageChops
import random
import math

# Sabitler
NB_POINTS = 360     #çizgi sayısı
CANVAS_SIZE = 360  # dairedeki nokta sayısı
POP_SIZE = 1000   # popülasyon boyutu
NB_GENERATION = 50  # İterasyon sayısı
LINE_WIDTH = 2 # çizgi kalığı
MUTATION_RATE = 0.01  # Mutasyon oranı

# İmaj yükleme ve çemberin etrafındaki noktaları belirleme
def load_image(image_path):
    return Image.open(image_path).convert('RGB').resize((CANVAS_SIZE, CANVAS_SIZE))

def generate_circle_individual():
    lines = [(random.randint(0, NB_POINTS - 1), random.randint(0, NB_POINTS - 1)) for _ in range(NB_POINTS)]
    return Individual(lines)

# Birey sınıfı
class Individual(object):
    def __init__(self, lines=None):
        if lines is not None:
            assert len(lines) == NB_POINTS
            self.lines = lines
            return
        self.lines = []

# İmajı tuvale çizme
def draw_image(individual):
    img = Image.new('RGB', (CANVAS_SIZE, CANVAS_SIZE), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for start, end in individual.lines:
        draw.line([points[start], points[end]], fill="black", width=LINE_WIDTH)
    return img

def hamming_distance(image1, image2):
    diff = ImageChops.difference(image1, image2).convert('L')
    total_diff = sum(diff.getdata())
    return total_diff / (CANVAS_SIZE * CANVAS_SIZE)

def genetic_algorithm(image):
    population = [generate_circle_individual() for _ in range(POP_SIZE)]
    for generation in range(NB_GENERATION):
        population = evolve_population(population, image)
        best_individual = min(population, key=lambda x: hamming_distance(image, draw_image(x)))
        fitness = hamming_distance(image, draw_image(best_individual))
        save_image(draw_image(best_individual), f'einsteinSON/generation_{generation}.png')  
        print(f'Generation {generation}, Best fitness (Hamming): {fitness:.2f}')

# Yeni nesil oluşturma
def evolve_population(population, image):
    new_population = []
    for _ in range(POP_SIZE):
        parent1, parent2 = random.choices(population, k=2)
        child = crossover(parent1, parent2)
        mutate(child)
        new_population.append(child)
    return new_population

# Çaprazlama
def crossover(parent1, parent2):
    crossover_point = random.randint(1, NB_POINTS - 1)
    child_lines = parent1.lines[:crossover_point] + parent2.lines[crossover_point:]
    return Individual(child_lines)

# Mutasyon
def mutate(individual):
    if random.random() < MUTATION_RATE:
        mutation_point = random.randint(0, NB_POINTS - 1)
        individual.lines[mutation_point] = (random.randint(0, NB_POINTS - 1), random.randint(0, NB_POINTS - 1))

# İmaj noktalarını oluşturma
points = [(int(CANVAS_SIZE / 2 + CANVAS_SIZE / 2 * math.cos(2 * math.pi * i / NB_POINTS)), 
           int(CANVAS_SIZE / 2 + CANVAS_SIZE / 2 * math.sin(2 * math.pi * i / NB_POINTS))) for i in range(NB_POINTS)]

# Resmi kaydetme
def save_image(img, filename):
    img.save(filename)

if __name__ == "__main__":
    image_path = 'einstein.jpg'
    image = load_image(image_path)
    genetic_algorithm(image)
