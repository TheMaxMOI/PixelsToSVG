#pragma once

#include <cstddef>
#include <ctime>
#include <string>

/* TODO
Make it print without delaying the thread
Make it print a bar followed by the actual percentage then the time of the ongoing task
example : █████▒▒░░░░░ 51.5% - time : 4305ms

TODO : later if size = 1
\
|
/
-
\
|
/
-
*/

class ProgressBar
{
private:
    enum Style
    {
        LARGE,
        SHORT,
    };

private:
    size_t currentVal_;
    size_t maxVal_;
    const time_t startingDate_;
    size_t previousLen_ = 0; // holds the len of the last printed bar and stats
    const Style style_;
    const size_t size_;

    double percentage_() const;
    void wipe_(size_t n);
    std::string getBar_(double percent, size_t intPercent) const;
    std::string getLargeBar_(double percent, size_t intPercent) const;
    std::string getShortBar_(size_t intPercent) const;
    size_t trueBarSize_() const;

public:
    ProgressBar(size_t size = 100);
    void set(size_t current, size_t max);
    void print();
    void updateAndShow(size_t current, size_t max);
};