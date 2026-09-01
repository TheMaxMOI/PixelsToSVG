#include <chrono>
#include <iostream>
#include <thread>

#include "../progressBar.hh"

#define BAR_SIZE 100

int main(void)
{
    ProgressBar bar{ BAR_SIZE };
    int steps[3] = { 1, 2, 5 };
    size_t maxSteps = 12310;

    size_t i = 0;
    while (i <= maxSteps)
    {
        bar.updateAndShow(i, maxSteps);
        int step = steps[i % 3];
        i += step;
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }

    return 0;
}
