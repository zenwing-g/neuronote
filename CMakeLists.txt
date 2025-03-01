cmake_minimum_required(VERSION 3.14)
project(mybackend)

# Use C++20 (or C++17 if you prefer)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python and Pybind11
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

# Create a shared library
add_library(mybackend MODULE backend.cpp)
target_link_libraries(mybackend PRIVATE pybind11::module)
