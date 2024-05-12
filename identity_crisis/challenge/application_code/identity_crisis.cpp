#include "resource.h"
// Windows Header Files
#include <windows.h>
#define WIN32_LEAN_AND_MEAN    // Exclude rarely-used stuff from Windows headers
// libs
#include <Wincrypt.h>
#pragma comment(lib, "Crypt32.lib")

int const RESULTING_FLAG_SIZE = 27885;

// taken from
// https://www.experts-exchange.com/articles/3216/Fast-Base64-Encode-and-Decode.html
int to_base64(char* source,
              int   source_size,
              char* destination,
              int   destination_size)
{
    DWORD size_out = destination_size;
    BOOL  result_ok
        = CryptBinaryToStringA((const BYTE*)source,
                               source_size,
                               CRYPT_STRING_BASE64 | CRYPT_STRING_NOCRLF,
                               destination,
                               &size_out);
    if (!result_ok) size_out = 0;    // failed
    return (size_out);
}

int main()
{

    auto flag_resource
        = FindResource(NULL, MAKEINTRESOURCE(IDI_FLAG), RT_RCDATA);
    auto loaded_resource  = LoadResource(NULL, flag_resource);
    auto resource_size    = SizeofResource(NULL, flag_resource);
    auto resource_address = (char*)LockResource(loaded_resource);

    char* resulting_flag = new char[RESULTING_FLAG_SIZE];
    to_base64(
        resource_address, resource_size, resulting_flag, RESULTING_FLAG_SIZE);

    MessageBoxA(
        NULL,
        resulting_flag,
        "What even am I anymore? - Tip: to copy, focus window and press CTRL-C",
        MB_OK);
}
