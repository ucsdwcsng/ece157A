INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_WES wes)

FIND_PATH(
    WES_INCLUDE_DIRS
    NAMES wes/api.h
    HINTS $ENV{WES_DIR}/include
        ${PC_WES_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    WES_LIBRARIES
    NAMES gnuradio-wes
    HINTS $ENV{WES_DIR}/lib
        ${PC_WES_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/wesTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(WES DEFAULT_MSG WES_LIBRARIES WES_INCLUDE_DIRS)
MARK_AS_ADVANCED(WES_LIBRARIES WES_INCLUDE_DIRS)
