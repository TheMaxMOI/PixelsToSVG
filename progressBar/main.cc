#include <chrono>
#include <iostream>
#include <thread>

#include "progressBar.hh"

int main(void)
{
    ProgressBar bar;
    int steps[3] = { 1, 2, 5 };
    size_t maxSteps = 1231;

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
