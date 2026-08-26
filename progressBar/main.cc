#include <iostream>
#include <thread>
#include <chrono>
#include "progressBar.hh"

int main() {
    ProgressBar bar;
    size_t maxSteps = 100;

    for (size_t i = 0; i <= maxSteps; ++i) {
        bar.updateAndShow(i, maxSteps);
        
        // Pause briefly so you can watch it update in real time
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    return 0;
} 