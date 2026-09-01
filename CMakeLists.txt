cmake_minimum_required(VERSION 3.16)

project(PixelsToSVG LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

enable_testing()

add_subdirectory(lib)

add_executable(mutateAndScore
    src/mutateAndScore/main.cc
    src/mutateAndScore/mutator.cc
    src/randomize/randomSVG.cc
)

target_include_directories(mutateAndScore PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(mutateAndScore PRIVATE svg)