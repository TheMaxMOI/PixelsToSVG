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

ProgressBar::ProgressBar(size_t size)
    : currentVal_{0}, maxVal_{0}, startingDate_{time(nullptr)}, style_{(size == 1) ? SHORT : LARGE}, size_{size}
{
    if (!size)
    {
        throw std::logic_error("0-sized bar doesn't make sense!");
    }
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

std::string ProgressBar::getLargeBar_(double percent, size_t intPercent) const
{
    std::stringstream barMaking;

    if (percent == 100)
    {
        for (int i = 0; i < size_; i++)
        {
            barMaking << DONE;
        }
    }
    else // (percent < 100)
    {
        int maxBeforeDone = MAX(round(2.0 * size_ / 100.0), 1);
        int resizedPercent = round(intPercent / 100.0 * size_);

        int numDone = (resizedPercent >= maxBeforeDone) ? resizedPercent - maxBeforeDone : 0;
        int numBeforeDone = resizedPercent - numDone;
        int numTodo = size_ - resizedPercent;

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

    return barMaking.str();
}

#define FRAME_AMOUNT 4
static const char* frames = "\\|/-";
std::string ProgressBar::getShortBar_(size_t intPercent) const
{
    return std::string{frames[intPercent%FRAME_AMOUNT]};
}

std::string ProgressBar::getBar_(double percent, size_t intPercent) const
{
    switch (style_)
    {
    case SHORT:
        return getShortBar_(intPercent);
    case LARGE:
        return getLargeBar_(percent, intPercent);
    default:
        return {};
    }
}

size_t ProgressBar::trueBarSize_() const
{
    switch (style_)
    {
    case LARGE:
        return size_;
    case SHORT:
        return 1;
    default:
        return 0;
    }
}

void ProgressBar::print()
{
    double percent = percentage_();
    size_t intPercent = floor(percent);

    const auto &bar = getBar_(percent, intPercent);

    std::stringstream statsMaking;
    statsMaking << ' ' << std::format("{:.2f}", percent) << '%';
    statsMaking << " - time: " << time(nullptr) - startingDate_ << "s";

    const auto &stats = statsMaking.str();
    const auto &full_bar = bar + stats;

    std::cout << '\r' << full_bar;
    wipe_(trueBarSize_() + stats.length());

    if (percent >= 100)
    {
        std::cout << '\n';
    }
}