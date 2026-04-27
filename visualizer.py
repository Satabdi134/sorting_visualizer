import pygame
import random
import time

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 600
NUM_BARS = 100
MIN_VAL, MAX_VAL = 10, 500
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 149, 237)

# ---------- INIT ----------
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualizer")

clock = pygame.time.Clock()

# ---------- DRAW ----------
def draw_list(arr, color_positions={}, clear_bg=True):
    if clear_bg:
        win.fill(BLACK)

    bar_width = WIDTH // len(arr)

    for i, val in enumerate(arr):
        x = i * bar_width
        y = HEIGHT - val

        color = BLUE
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(win, color, (x, y, bar_width, val))

    pygame.display.update()


# ---------- GENERATE ----------
def generate_array():
    return [random.randint(MIN_VAL, MAX_VAL) for _ in range(NUM_BARS)]


# ---------- SORTING ALGORITHMS ----------
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            draw_list(arr, {j: RED, j + 1: GREEN})
            yield True

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

            draw_list(arr, {j: RED, j + 1: GREEN})
            yield True

        arr[j + 1] = key

    return arr


def merge_sort(arr, l, r):
    if l >= r:
        return

    mid = (l + r) // 2
    yield from merge_sort(arr, l, mid)
    yield from merge_sort(arr, mid + 1, r)

    left = arr[l:mid+1]
    right = arr[mid+1:r+1]

    i = j = 0
    k = l

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1

        draw_list(arr, {k: GREEN})
        yield True
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
        draw_list(arr, {k: GREEN})
        yield True

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
        draw_list(arr, {k: GREEN})
        yield True


def quick_sort(arr, low, high):
    if low >= high:
        return

    pivot = arr[high]
    i = low

    for j in range(low, high):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            draw_list(arr, {i: GREEN, j: RED})
            yield True
            i += 1

    arr[i], arr[high] = arr[high], arr[i]
    draw_list(arr, {i: GREEN})
    yield True

    yield from quick_sort(arr, low, i - 1)
    yield from quick_sort(arr, i + 1, high)


# ---------- MAIN LOOP ----------
def main():
    run = True
    arr = generate_array()

    sorting = False
    sorting_algo = bubble_sort
    sorting_name = "Bubble Sort"
    sorting_gen = None

    while run:
        clock.tick(FPS)

        if sorting:
            try:
                next(sorting_gen)
            except StopIteration:
                sorting = False

        else:
            draw_list(arr)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    arr = generate_array()
                    sorting = False

                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    if sorting_algo == bubble_sort:
                        sorting_gen = sorting_algo(arr)
                    elif sorting_algo == insertion_sort:
                        sorting_gen = sorting_algo(arr)
                    elif sorting_algo == merge_sort:
                        sorting_gen = sorting_algo(arr, 0, len(arr) - 1)
                    elif sorting_algo == quick_sort:
                        sorting_gen = sorting_algo(arr, 0, len(arr) - 1)

                elif event.key == pygame.K_b:
                    sorting_algo = bubble_sort
                    sorting_name = "Bubble Sort"

                elif event.key == pygame.K_i:
                    sorting_algo = insertion_sort
                    sorting_name = "Insertion Sort"

                elif event.key == pygame.K_m:
                    sorting_algo = merge_sort
                    sorting_name = "Merge Sort"

                elif event.key == pygame.K_q:
                    sorting_algo = quick_sort
                    sorting_name = "Quick Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
