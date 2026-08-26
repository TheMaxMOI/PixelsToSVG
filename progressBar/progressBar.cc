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
    if (previousLen_ > n)
    {
        std::cout << std::string(previousLen_ - n, ' ');
    }

    previousLen_ = n;
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

    std::stringstream statsMaking;
    statsMaking << ' ' << std::format("{:.2f}", percent) << '%';
    statsMaking << " - time: " << time(nullptr) - startingDate_ << "s";

    const auto &stats = statsMaking.str();
    const auto &full_bar = barMaking.str() + stats;

    size_t trueSize = 100 + stats.length();

    std::cout << '\r' << full_bar;
    wipe_(trueSize);

    if (percent >= 100)
    {
        std::cout << '\n';
    }
}