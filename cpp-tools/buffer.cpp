#include <cstdint>
#include <cassert>
#include <string>

typedef int T;

template <typename T>
class Stack {
    T* data;
    uint32_t size;
    uint32_t pos;
};

class Buffer {
 private:
    uint8_t* data;
    uint32_t size;
    uint32_t pos;

    Stack<uint32_t> position_stack;

 public:
    Buffer(uint32_t size = 0) {
        this->size = size;
        this->pos = 0;
        this->data = new uint8_t[this->size];
        for (int i = 0; i < this->size; i++)
            this->data[i] = 0;
    }
    Buffer(const Buffer& buffer) {
        this->size = buffer.size;
        this->pos = 0;
        this->data = new uint8_t[this->size];
        for (int i = 0; i < this->size; i++)
            this->data[i] = buffer.data[i];
    }
    ~Buffer() {
        delete[] this->data;
    }

    bool operator==(const Buffer& other) const {}

    uint8_t& operator[](int index) const {
        return this->data[index + (index >= 0 ? 0 : this->size)];
    }
    operator bool() const { return !this->is_end(); }

    bool is_end() const {}
    int bytes_remains() const {}

    uint32_t pop_pos() const {}
    void push_pos(uint32_t pos) const {}

    // seek
    // reset
    // skip
    // load
    // save

    // load_file
    // save_file
    // static from_file


    // T read(int pos = -1) const {}
    // void write(T value, int pos = -1) {}

    template <typename T>
    T read(int pos = -1) const {
        if (pos != -1) this->push_pos(pos);
        T result = *(T*)&this->data[this->pos];
        if (pos != -1) this->pop_pos();
        return result;
    }

    template <typename T>
    void write(T value, int pos = -1) {
        if (pos != -1) this->push_pos(pos);
        *(T*)&this->data[this->pos] = value;
        if (pos != -1) this->pop_pos();
    }

    T read_str    (int pos = -1) const {
        if (pos != -1) this->push_pos(pos);
        T result = *(T*)&this->data[this->pos];
        if (pos != -1) this->pop_pos();
        return result;
    }
    T read_wstr   (int pos = -1) const {
        if (pos != -1) this->push_pos(pos);
        T result = *(T*)&this->data[this->pos];
        if (pos != -1) this->pop_pos();
        return result;
    }
    void write_str   (T value, int pos = -1) {}
    void write_wstr  (T value, int pos = -1) {}
};
