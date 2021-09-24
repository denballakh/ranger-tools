// optimization=3
/*
Программа для перебора ключей шифрования датников
Открывает датник и пытается подобрать такой ключ,
    чтобы в расшифрованных данных был заголовок ZL01
Выводит несколько чисел, одно из них является
    настоящим ключом

Ключи для разных форматов датников:
keys = {
    'HDMain': -1310144887,
    'HDCache': -359710921,
    'ReloadMain': 1050086386,
    'ReloadCache': 1929242201,
    'SR1': 0,
}
*/

#include <ctime>    // clock_t, clock(), CLOCKS_PER_SEC
#include <cstdint>
#include <cstdio>   // printf
#include <fstream>  // ifstream

using namespace std;

inline int32_t rnd(int32_t seed) {
    seed = (seed % 0x1f31d) * 0x41a7 - (seed / 0x1f31d) * 0xb14;
    if (seed < 1)
        seed += 0x7fffffff;
    
    return seed;
}

int main(int argc, char *argv[]) {
    // for (int i = 0; i < argc; i++)
    //     printf("argv[%d] = %s\n", i, argv[i]);

    if (argc != 2 && argc != 3) {
        printf("Usage: this.exe file [signed_flag]\n");
        return 1;
    }

    ifstream file;
    string filename = argv[1];
    file.open(filename, ios::in | ios::binary);

    if (!file.is_open()) {
        printf("Error while opening file!\n");
        return 1;
    }

    if (argc == 3) { // Skipping 8 bytes of sign
        for (int i = 0; i < 8; i++)
            file.get();
    }

    uint8_t hash_0 = file.get(); // Unused
    uint8_t hash_1 = file.get();
    uint8_t hash_2 = file.get();
    uint8_t hash_3 = file.get();

    uint8_t seed_0 = file.get();
    uint8_t seed_1 = file.get();
    uint8_t seed_2 = file.get();
    uint8_t seed_3 = file.get();
    int32_t _seed = int32_t(seed_0) + (int32_t(seed_1) << 8) + (int32_t(seed_2) << 16) + (int32_t(seed_3) << 24);
    
    uint8_t zl01_0 = file.get();
    uint8_t zl01_1 = file.get();
    uint8_t zl01_2 = file.get();
    uint8_t zl01_3 = file.get();

    file.close();

    clock_t t_start = clock();

    int32_t seed;

    uint8_t zl01_0_decoded;
    uint8_t zl01_1_decoded;
    uint8_t zl01_2_decoded;
    uint8_t zl01_3_decoded;

    for (int32_t key = -0x80000000; key < +0x7fffffff; key++) {
        seed = _seed ^ key;

        seed = rnd(seed);
        zl01_0_decoded = zl01_0 ^ ((seed & 0xff) - 1);

        seed = rnd(seed);
        zl01_1_decoded = zl01_1 ^ ((seed & 0xff) - 1);

        seed = rnd(seed);
        zl01_2_decoded = zl01_2 ^ ((seed & 0xff) - 1);

        seed = rnd(seed);
        zl01_3_decoded = zl01_3 ^ ((seed & 0xff) - 1);

        if (zl01_0_decoded == 'Z')
        if (zl01_1_decoded == 'L')
        if (zl01_2_decoded == '0')
        if (zl01_3_decoded == '1' || zl01_3_decoded == '2' || zl01_3_decoded == '3')
            printf("%+11d %#010x %c%c%c%c\n", key, key, zl01_0_decoded, zl01_1_decoded, zl01_2_decoded, zl01_3_decoded);
    }

    clock_t t_end = clock();

    printf("\n");
    printf("Time taken:  %.3lf s\n", (double)(t_end - t_start) / CLOCKS_PER_SEC);

    return 0;
}
