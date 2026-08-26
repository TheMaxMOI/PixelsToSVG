#include "progressBar.hh"

#define DONE "█"
#define BEFORE_DONE "▒"
#define TODO "░"

#include <cmath>
#include <sstream>
#include <format>
#include <iostream>

#define MAX(a, b) \
    (((a) <= (b)) ? (b) : (a))

ProgressBar::ProgressBar()
    : currentVal_{0}, maxVal_{0}, startingDate_{time(nullptr)}
{
}

void ProgressBar::set(size_t current, size_t max)
{
    currentVal_ = current;
    maxVal_ = max;
}

void ProgressBar::updateAndShow(size_t current, size_t max)
{
    set(current, max);
    print();
}

double ProgressBar::percentage_() const
{
    if (maxVal_ == 0 || currentVal_ >= maxVal_)
    {
        return 100;
    }

    return double(currentVal_) / double(maxVal_) * 100;
};

void ProgressBar::wipe_(size_t n)
{
    int max = MAX(n, previousLen_);
    for (int i = 0; i < max; i++)
    {
        std::cout << ' ';
    }

    std::cout << '\r';

    previousLen_ = max;
}

void ProgressBar::print()
{
    double percent = percentage_();
    size_t intPercent = floor(percent);

    std::stringstream barMaking;

    if (percent == 100)
    {
        for (int i = 0; i < 100; i++)
        {
            barMaking << DONE;
        }
    }
    else // (percent < 100)
    {
        int numDone = (intPercent >= 2) ? intPercent - 2 : 0;
        int numBeforeDone = intPercent - numDone;
        int numTodo = 100 - intPercent;

        for (int i = 0; i < numDone; i++)
        {
            barMaking << DONE;
        }
        for (int i = 0; i < numBeforeDone; i++)
        {
            barMaking << BEFORE_DONE;
        }
        for (int i = 0; i < numTodo; i++)
        {
            barMaking << TODO;
        }
    }

    barMaking << ' ' << std::format("{:.2f}", percent) << '%';
    barMaking << " - time: " << time(nullptr) - startingDate_ << "ms";

    barMaking << (percent > 99) ? '\n' : '\r';

    const auto &str = barMaking.str();

    wipe_(str.length());
    std::cout << str;
}