// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;

int wordcount;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        return false;
    }
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        node *cursor = root;

        ///Going through the word
          for(int i = 0, Length = strlen(word); i < Length; i++)
            {
                //Create a letter variable
                int number;

                if (word[i] != '\'')
                    {
                        number = tolower(word[i]) - 'a';
                    }

                else number = 26;

                if (cursor->children[number] == NULL)
                {
                    node *new_node = malloc(sizeof(node));
                    if (new_node == NULL)
                    {
                        return false;
                    }
                for (int z = 0; z < 27; z++)
                    {
                    new_node->children[z] = NULL;
                    }

                new_node->is_word = false;
                cursor->children[number] = new_node;
                }

                cursor = cursor->children[number];

            }


        cursor->is_word = true;

        wordcount++;

    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordcount;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
     int index;
    // create a pointer to first node
    node* curs = root;

    for (int i = 0; word[i] != '\0'; i++)
    {
        // if letter is apostrophe
        if (word[i] == '\'')
        {
            index = 26;
        }
        else
        // convert each letter to an index, e.g a is 0
        {
            index = tolower(word[i]) - 'a';
        }

        // traverse to next letter
        curs = curs->children[index];

        // if NULL, word is misspelled
        if (curs == NULL)
        {
            return false;
        }
    }

    // once at end of word, check if is_word is true
    if (curs->is_word == true)
    {
        return true;
    }
    else
    {
        return false;
    }
}

void delete(node* children)
{
    for (int i = 0; i < 27; i++)
    {
        if (children->children[i] != NULL)
        {
            delete(children->children[i]);
        }
    }

    free(children);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node* curz = root;
    delete(curz);
    return true;
}
