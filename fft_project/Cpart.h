#pragma once

#ifdef CPART_DLL
#define DLL_EXPORT _declspec(dllexport)
#else
#define DLL_EXPORT _declspec(dllexport)
#endif

extern "C"{
    int      mInSec    (char * path);
    int      fileSize  (char * path);
    int    * readf     (char * path, double sInMeas);
    double * transform (double * in, int sectorLength, int pos);
    double * amplitude (double * in, int sectorLength, int pos);
}
