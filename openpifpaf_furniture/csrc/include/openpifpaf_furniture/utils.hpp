#pragma once

#include <iostream>


#ifdef _WIN32
#if defined(OPENPIFPAF_FURNITURE_DLLEXPORT)
#define OPENPIFPAF_FURNITURE_API __declspec(dllexport)
#else
#define OPENPIFPAF_FURNITURE_API __declspec(dllimport)
#endif
#else
#define OPENPIFPAF_FURNITURE_API
#endif


namespace openpifpaf_furniture {

inline bool quiet = false;
void set_quiet(bool v = true);

// use template args to unpack __VA_ARGS__ from template
template<typename ...Args>
void cout_info(const char* file_name, int line_number, Args&& ...args) {
    std::cout << file_name << ':' << line_number << ": UserInfo: " << (... << args) << '\n';
}
#define OPENPIFPAF_FURNITURE_INFO(...) if (!quiet) { cout_info(__FILE__, __LINE__, __VA_ARGS__); }
#define OPENPIFPAF_FURNITURE_WARN(...) if (!quiet) { TORCH_WARN(__VA_ARGS__); }

}  // namespace openpifpaf_furniture
