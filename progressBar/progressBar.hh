#pragma once

#include <cstddef>
#include <ctime>

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

#define SIZE 100

class ProgressBar
{
// private:
//     enum Style{
//         LARGE,
//         SHORT,
//     };

private:
    size_t currentVal_;
    size_t maxVal_;
    time_t startingDate_;
    size_t previousLen_ = 0; // holds the len of the last printed bar and stats

    double percentage_() const;
    void wipe_(size_t n);

public:
    ProgressBar(/*size_t size = 100*/);
    void set(size_t current, size_t max);
    void print();
    void updateAndShow(size_t current, size_t max);
};