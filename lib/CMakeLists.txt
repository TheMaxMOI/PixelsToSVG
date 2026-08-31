cmake_minimum_required(VERSION 3.16)

project(lib LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_compile_options(
    -Wall
    -Wextra
    -Werror
    -pedantic
    -Wold-style-cast
)

# ============================================================
# Library sources
# ============================================================

set(RGB_SOURCES
    rgb/rgb.cc
)

set(XMLGEN_SOURCES
    xmlGen/comment.cc
    xmlGen/declaration.cc
    xmlGen/tag.cc
)

set(SVG_SOURCES
    svg/svg.cc

    svg/elements/appearance.cc
    svg/elements/element.cc

    svg/elements/path/cursor.cc
    svg/elements/path/path.cc
    svg/elements/path/turtle.cc

    svg/elements/polypoint/polygon.cc
    svg/elements/polypoint/polyline.cc
    svg/elements/polypoint/polypoint.cc

    svg/elements/round/circle.cc
    svg/elements/round/ellipse.cc
    svg/elements/round/round.cc

    svg/elements/shapes/line.cc
    svg/elements/shapes/rectangle.cc
    svg/elements/shapes/text.cc

    svg/elements/utils/concatStr.cc
    svg/elements/utils/doubleFormat.cc
    svg/elements/utils/mathHelpers.cc
)

# ============================================================
# Libraries
# ============================================================

add_library(rgb STATIC ${RGB_SOURCES})
target_include_directories(rgb PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(xmlGen STATIC ${XMLGEN_SOURCES})
target_include_directories(xmlGen PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(svg STATIC ${SVG_SOURCES})
target_include_directories(svg PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(svg PUBLIC
    rgb
    xmlGen
)

# ============================================================
# Tests
# ============================================================

function(add_svg_test TEST_NAME)
    add_executable(${TEST_NAME}
        svg/tests/${TEST_NAME}.cc
    )

    target_link_libraries(${TEST_NAME} PRIVATE svg)

    target_include_directories(${TEST_NAME} PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
    )
endfunction()

add_svg_test(hexagonLines)
add_svg_test(hexagonPolygon)
add_svg_test(hexagonPolyLine)
add_svg_test(hexagonTurtle)
add_svg_test(simplerSvg)
add_svg_test(snowFlakeTurtle)
add_svg_test(tspanCheck)


function(add_xmlgen_test TEST_NAME)
    add_executable(${TEST_NAME}
        xmlGen/tests/${TEST_NAME}.cc
    )

    target_link_libraries(${TEST_NAME} PRIVATE xmlGen)

    target_include_directories(${TEST_NAME} PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
    )
endfunction()

add_xmlgen_test(aSvg)
add_xmlgen_test(tagTest)

# ============================================================
# CTest
# ============================================================

enable_testing()

add_test(NAME hexagonLines     COMMAND hexagonLines)
add_test(NAME hexagonPolygon   COMMAND hexagonPolygon)
add_test(NAME hexagonPolyLine  COMMAND hexagonPolyLine)
add_test(NAME hexagonTurtle    COMMAND hexagonTurtle)
add_test(NAME simplerSvg       COMMAND simplerSvg)
add_test(NAME snowFlakeTurtle  COMMAND snowFlakeTurtle)
add_test(NAME tspanCheck       COMMAND tspanCheck)

add_test(NAME xmlgen_svg       COMMAND aSvg)
add_test(NAME xmlgen_tagTest   COMMAND tagTest)