PROJECT(ClapackPackageTest)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()


file(GLOB TEST_SOURCES
  ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp
)

ADD_EXECUTABLE(test_lapack ${TEST_SOURCES})
TARGET_LINK_LIBRARIES(test_lapack ${CONAN_LIBS})
