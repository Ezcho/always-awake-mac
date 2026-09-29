#include <CoreServices/CoreServices.h>
#include <stdio.h>

// Finder's icvp record still consumes an AliasRecord. Let macOS populate
// disk-image volume metadata; a generic local-disk alias does not resolve here.
int main(int argc, char **argv) {
    if (argc != 3) return 2;
    AliasHandle alias = NULL;
    OSStatus result = FSNewAliasFromPath(NULL, argv[1], 0, &alias, NULL);
    if (result != noErr || alias == NULL) {
        fprintf(stderr, "Cannot create background alias (%d)\n", result);
        return 1;
    }
    FILE *output = fopen(argv[2], "wb");
    if (output == NULL) { DisposeHandle((Handle)alias); return 1; }
    size_t count = (size_t)GetHandleSize((Handle)alias);
    size_t written = fwrite(*alias, 1, count, output);
    int closed = fclose(output);
    DisposeHandle((Handle)alias);
    return written == count && closed == 0 ? 0 : 1;
}
