#include "helpers/symbol_table.h"
#include "helpers/global_types.h"

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HASH_MULTIPLICATOR 113
#define LIST_INITIAL_SIZE 1
#define LIST_SIZE_MULTIPLICATOR 2
#define STRING_BUFFER_CHUNK_SIZE 20 * 1000
#define STRING_BUFFER_CHUNK_COUNT 100

typedef uintmax_t KeyType;

// String section

static char **String_buffer = NULL;
static size_t String_buffer_used_chunk_size;
static size_t String_buffer_virtual_size;
static size_t String_buffer_real_size;

static size_t
max (size_t a, size_t b)
{
  return a > b ? a : b;
}

static char *
StringAllocation (size_t size)
{
  if (String_buffer == NULL)
    {
      String_buffer = (char **) malloc( sizeof(char *) *
                                        STRING_BUFFER_CHUNK_COUNT );
      String_buffer[0] = (char *) malloc( STRING_BUFFER_CHUNK_SIZE );
      String_buffer_used_chunk_size = 0;
      String_buffer_virtual_size = 0;
      String_buffer_real_size = STRING_BUFFER_CHUNK_COUNT;
    }

  if (String_buffer_used_chunk_size + size + 1 > STRING_BUFFER_CHUNK_SIZE)
    {
      ++ String_buffer_virtual_size;

      if (String_buffer_virtual_size == String_buffer_real_size)
        {
          String_buffer_real_size += STRING_BUFFER_CHUNK_COUNT;
          String_buffer = (char **)
                          realloc( String_buffer,
                                   sizeof(char *) * String_buffer_real_size );
        }

      String_buffer_used_chunk_size = 0;

      String_buffer[ String_buffer_virtual_size ] = (char *)
        malloc( max(STRING_BUFFER_CHUNK_SIZE, size + 1) );
    }

  char *result = String_buffer[String_buffer_virtual_size] +
                 String_buffer_used_chunk_size;
  String_buffer_used_chunk_size += size + 1;

  for (size_t i = 0; i < size; ++ i)
    result[i] = ' ';
  result[size] = 0;

  return result;
}

static void
StringDeallocation (String s)
{
  if (String_buffer[String_buffer_virtual_size] <= s &&
      s < String_buffer[String_buffer_virtual_size] +
           STRING_BUFFER_CHUNK_SIZE &&
      s - String_buffer[String_buffer_virtual_size] + strlen(s) + 1 ==
        String_buffer_used_chunk_size )
    String_buffer_used_chunk_size -= strlen(s) + 1;
}

static String
ToLowercase (String s)
{
  size_t length = strlen(s);
  char *result = StringAllocation(length);

  for (size_t i = 0; i <= length; ++ i)
    if ('A' <= s[i] && s[i] <= 'Z' )
      result[i] = s[i] - 'A' + 'a';
    else
      result[i] = s[i];

  return result;
}


// Hash section

static KeyType
Hash (String s)
{
  KeyType result = 0;
  for (size_t i = 0; s[i] != 0; ++ i)
    result = result * HASH_MULTIPLICATOR + s[i]; // dirty hack
  return result;
}


// List section

typedef struct symbol_struct ValueType;

typedef struct list
{
  size_t virtual_size;
  size_t real_size;
  ValueType array[];
} *List;


static List
NewList (void)
{
  List list = (List) malloc( sizeof(struct list) +
                             sizeof(ValueType) * LIST_INITIAL_SIZE );
  list->real_size = LIST_INITIAL_SIZE;
  list->virtual_size = 0;
}

static void
DeleteList (List list)
{
  free(list);
}

static Symbol
AppendList (List *plist)
{
  List list = *plist;

  if (list->virtual_size == list->real_size)
    {
      list->real_size *= LIST_SIZE_MULTIPLICATOR;
      *plist = list = (List) realloc(list, sizeof(struct list) +
                                           sizeof(ValueType) * list->real_size);
    }

  Symbol symbol = &( list->array[list->virtual_size] );

  ++ list->virtual_size;

  return symbol;
}

static Symbol
SearchList (String s, List list)
{
  for (size_t i = 0; i < list->virtual_size; ++ i)
    if ( strcmp(list->array[i].name, s) == 0 )
      return &( list->array[i] );

  return NULL;
}


// Splay tree section

typedef struct node
{
  struct node *left;
  struct node *right;
  struct node *parent;
  KeyType key;
  List list;
} *Node;

typedef Node *Tree;


static Tree
NewTree (void)
{
  Tree root = (Tree) malloc( sizeof(Node) );
  *root = NULL;
  return root;
}

static Node
NewNode (KeyType key)
{
  Node x = (Node) malloc( sizeof(struct node) );
  x->list = NewList();
  x->key = key;
  x->left = NULL;
  x->right = NULL;
  x->parent = NULL;
  return x;
}

static void
DeleteNode (Node x)
{
  if (x != NULL)
    {
      DeleteNode(x->left);
      DeleteNode(x->right);
      DeleteList(x->list);
      free(x);
    }
}

static void
DeleteTree (Tree root)
{
  DeleteNode(*root);
  free(root);
}

static void
EmptyTree (Tree root)
{
  DeleteNode(*root);
  *root = NULL;
}


static void
Rotate (Node x, Node p)
{
  Node v, u;

  /*
   *
   *       u            u
   *       |            |
   *       p            x
   *      / \    =>    / \
   *     x   n        m   p
   *    / \              / \
   *   m   v            v   n
   *
   */

  u = p->parent;

  if (x == p->left)
    {
      p->left = v = x->right;
      x->right = p;
    }
  else
    {
      p->right = v = x->left;
      x->left = p;
    }
  p->parent = x;

  if (v != NULL)
    v->parent = p;

  if (u != NULL)
    {
      if (u->left == p)
        u->left = x;
      else
        u->right = x;
    }
  x->parent = u;
}

static void
Splay (Node x, Tree root)
{
  Node p = x->parent;

  while (p != NULL)
  {
    Node pp = p->parent;

    if (pp == NULL)
      Rotate(x, p);
    else if ((x == p->left)  && (p == pp->left) ||
             (x == p->right) && (p == pp->right))
      {
        Rotate(p, pp);
        Rotate(x, p);
      }
    else
      {
        Rotate(x, p);
        Rotate(x, pp);
      }

    p = x->parent;
  }

  *root = x;
}

static Node
CreateNode (KeyType key, Tree root)
{
  Node x = NewNode(key);

  Tree t = root;
  Node p = NULL;

  while (*t != NULL)
  {
    p = *t;
    if (key < (*t)->key)
      t = &((*t)->left);
    else
      t = &((*t)->right);
  }

  *t = x;
  x->parent = p;

  Splay(x, root);

  return x;
}

static Node
SearchNode (KeyType key, Tree root)
{
  Node x = *root;

  while (x != NULL)
  {
    if (key < x->key)
      x = x->left;
    else if (x->key < key)
      x = x->right;
    else
      {
        Splay(x, root);
        return x;
      }
  }

  return NULL;
}

static Node
GetNode (KeyType key, Tree root)
{
  Node x = SearchNode(key, root);
  if (x == NULL)
    x = CreateNode(key, root);

  return x;
}

// Hashmap section

static Symbol
CreateSymbol (String s, Tree root)
{
  KeyType key = Hash(s);

  Node x = GetNode(key, root);

  Symbol symbol = AppendList(&(x->list));

  symbol->name = s;

  return symbol;
}

static Symbol
SearchSymbol (String s, Tree root)
{
  KeyType key = Hash(s);

  Node x = SearchNode(key, root);
  if (x == NULL)
    return NULL;
  else
    return SearchList(s, x->list);
}

// Symbol section

Symbol
GetSymbol (String s, SymbolTable root)
{
  s = ToLowercase(s);

  Symbol symbol = SearchSymbol(s, root);
  if (symbol == NULL)
    symbol = CreateSymbol(s, root);
  else
    StringDeallocation(s);

  return symbol;
}

