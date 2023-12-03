#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Structure to store relevant lines from the file
typedef struct {
    char *line;
} FailedLoginEntry;

int main() {
    // Open the file in read mode
    FILE *file = fopen("auth.log", "r");
    if (file == NULL) {
        perror("Error opening the file");
        return 1;
    }

    // Initialize a dynamic array to store the entries
    FailedLoginEntry *failedLogins = NULL;
    size_t numEntries = 0;

    // Read the file line by line
    char *line = NULL;
    size_t lineLength = 0;
    size_t read;

    while ((read = getline(&line, &lineLength, file)) != -1) {
        // Check if the line contains the keyword "Failed"
        if (strstr(line, "Failed") != NULL) {
            // Add the line to the dynamic array
            FailedLoginEntry entry;
            entry.line = strdup(line); // Use strdup to duplicate the string
            failedLogins = realloc(failedLogins, (numEntries + 1) * sizeof(FailedLoginEntry));
            if (failedLogins == NULL) {
                perror("Error allocating memory");
                return 1;
            }
            failedLogins[numEntries++] = entry;
        }
    }

    // Close the file after reading
    fclose(file);

    // Print the stored lines
    for (size_t i = 0; i < numEntries; ++i) {
        printf("%s", failedLogins[i].line);
        free(failedLogins[i].line); // Free the memory allocated for each line
    }

    // Free the memory of the dynamic array
    free(failedLogins);
    free(line); // Free the memory allocated for the line from getline

    return 0;
}
