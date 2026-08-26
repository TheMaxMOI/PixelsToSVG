#include <iostream>
#include <thread>
#include <chrono>
#include "progressBar.hh"

int main(void)
{
    ProgressBar bar{1};
    int steps[3] = {1, 2, 5};
    size_t maxSteps = 123102;

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