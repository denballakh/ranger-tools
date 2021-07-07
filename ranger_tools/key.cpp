/*
Программа для перебора ключей шифрования датников
Она открывает датник и пытается подобрать такой ключ, 
    чтобы в расшифрованных данных был заголовок ZL01
Программа выводит несколько чисел, одно из них является
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
#define FILENAME "find_keys_reload_cache.dat"

#include <iostream>
#include <fstream>

using namespace std;

int rnd(int seed) {
    seed = (seed % 0x1f31d) * 0x41a7 - (seed / 0x1f31d) * 0xb14;
    if (seed < 1)
        seed += 0x7fffffff;
    
    return seed;
}

int main() {
    ifstream file;
    file.open(FILENAME, ios::in | ios::binary);

    if (!file.is_open()) {
        cout << "Error while opening file!" << endl;
        getchar();
        return 0;
    }

    unsigned char hash_0 = file.get();
    unsigned char hash_1 = file.get();
    unsigned char hash_2 = file.get();
    unsigned char hash_3 = file.get();

    unsigned char seed_0 = file.get();
    unsigned char seed_1 = file.get();
    unsigned char seed_2 = file.get();
    unsigned char seed_3 = file.get();
    
    unsigned char zl01_0 = file.get();
    unsigned char zl01_1 = file.get();
    unsigned char zl01_2 = file.get();
    unsigned char zl01_3 = file.get();

    file.close();
    
    int _seed = int(seed_0) + (int(seed_1) << 8) + (int(seed_2) << 16) + (int(seed_3) << 24);

    for (int key = -2147483648; key < 2147483647; key++) {
        int seed = _seed ^ key;

        unsigned char zl01_0_decoded;
        unsigned char zl01_1_decoded;
        unsigned char zl01_2_decoded;
        unsigned char zl01_3_decoded;

        seed = rnd(seed);
        zl01_0_decoded = zl01_0 ^ ((seed & 0xff) - 1);

        seed = rnd(seed);
        zl01_1_decoded = zl01_1 ^ ((seed & 0xff) - 1);

        seed = rnd(seed);
        zl01_2_decoded = zl01_2 ^ ((seed & 0xff) - 1);

        seed = rnd(seed);
        zl01_3_decoded = zl01_3 ^ ((seed & 0xff) - 1);

        if (zl01_0_decoded == 'Z' && zl01_1_decoded == 'L' && zl01_2_decoded == '0' && zl01_3_decoded == '1') {
            cout << key << endl;
        }
    }
    cout << "END" << endl;
    getchar();
}
