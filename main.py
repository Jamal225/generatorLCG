import numpy as np
from nistrng import *
import matplotlib.pyplot as plt
import seaborn as sns


# линейный конгруэнтный генератор (LCG)
def lcg_generator(seed, size):
    a = 6097
    c = 749060
    m = 127
    sequence = []
    x = seed
    for _ in range(size):
        x = (a * x + c) % m
        sequence.append(x)
    return sequence


# генератор Mersenne Twister
def mersenne_twister_generator(seed, size):
    rng = np.random.default_rng(seed)
    return rng.integers(low=-128, high=128, size=size)


def heat_map(binary_sequence, ax, title):
    def determine_image_size(length):
        side_length = int(np.ceil(np.sqrt(length)))
        return side_length, side_length

    image_size = determine_image_size(len(binary_sequence))

    if len(binary_sequence) < image_size[0] * image_size[1]:
        binary_sequence = \
            np.pad(binary_sequence, (0, image_size[0] * image_size[1] - len(binary_sequence)), mode='constant')

    binary_sequence_2d = binary_sequence.reshape(image_size)

    sns.heatmap(binary_sequence_2d, cmap='Greys', cbar=False, square=True, ax=ax)
    ax.set_title(title)


def create_binary_sequence(seed, size):
    sequence_lcg = lcg_generator(seed, size)
    sequence_mersenne = mersenne_twister_generator(seed, size)
    print(f'Сгенерированная последовательность: {sequence_lcg}')
    binary_str = ''.join(format(num, 'b') for num in sequence_lcg)
    print(f'Размер битового представления: {len(binary_str)}')
    print(f'Битовое представление: {binary_str}')
    sequence_lcg_np = np.array(sequence_lcg, dtype=int)
    sequence_mersenne_np = np.array(sequence_mersenne, dtype=int)

    return pack_sequence(sequence_lcg_np), pack_sequence(sequence_mersenne_np)


def test_for_binary_sequence(binary_sequence, eligible_battery):
    results = run_all_battery(binary_sequence, eligible_battery, False)
    for result, elapsed_time in results:
        if result.passed:
            print(
                f"- PASSED - score: {np.round(result.score, 3)} - {result.name} - elapsed time: {elapsed_time} ms")
        else:
            print(
                f"- FAILED - score: {np.round(result.score, 3)} - {result.name} - elapsed time: {elapsed_time} ms")


if __name__ == "__main__":
    seed = int(input("Seed:"))
    size = int(input("Size:"))
    # генерим числовые последовательности и переводим их в бинарный вид
    binary_sequence_lcg, binary_sequence_mersenne = create_binary_sequence(seed, size)

    # проверка пригодности тестов для последовательностей
    eligible_battery_lcg = check_eligibility_all_battery(binary_sequence_lcg, SP800_22R1A_BATTERY)
    eligible_battery_mersenne = check_eligibility_all_battery(binary_sequence_mersenne, SP800_22R1A_BATTERY)

    # ----------------TEST BLOCK-------------------------------
    print("Eligible tests for LCG and Mersenne Twister :")
    for name in eligible_battery_lcg.keys():
        print("- " + name)

    # проведение тестов для LCG
    print("\nTest results for LCG:")
    test_for_binary_sequence(binary_sequence_lcg, eligible_battery_lcg)

    # проведение тестов для Mersenne Twister
    print("\nTest results for Mersenne Twister:")
    test_for_binary_sequence(binary_sequence_mersenne, eligible_battery_mersenne)

    # -------------VISUALIZATION-----------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    heat_map(binary_sequence_lcg, axes[0], 'Binary Sequence LCG')
    heat_map(binary_sequence_mersenne, axes[1], 'Binary Sequence Mersenne')
    plt.show()
