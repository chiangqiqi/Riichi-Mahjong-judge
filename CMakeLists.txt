project(client)
cmake_minimum_required(VERSION 3.16)
set (CMAKE_CXX_STANDARD 11)

set(CMAKE_CXX_COMPILER /usr/local/bin/clang++)

find_package(PkgConfig REQUIRED)

link_directories(/usr/local/lib)

pkg_check_modules(JSONCPP jsoncpp)
# include dir
include_directories(
  ${JSONCPP_INCLUDE_DIRS}
)
include_directories(/usr/local/opt/llvm/include/c++/v1/)

# to speed things up
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O2")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2")

add_executable(client client.cc)
target_link_libraries(client ${JSONCPP_LIBRARIES})

file(GLOB MJ_SRC "src/*.h" "src/*.cpp")
find_package(Boost REQUIRED)
if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})

    MESSAGE( STATUS "Boost_INCLUDE_DIRS = ${Boost_INCLUDE_DIRS}.")
    MESSAGE( STATUS "Boost_LIBRARIES = ${Boost_LIBRARIES}.")
    MESSAGE( STATUS "Boost_LIB_VERSION = ${Boost_LIB_VERSION}.")
    add_executable(mahjong ${MJ_SRC})
    target_link_libraries (mahjong ${Boost_LIBRARIES})
    target_link_libraries(mahjong ${JSONCPP_LIBRARIES})

endif()
